"""PostgreSQL persistence layer (psycopg2).

A small connection pool plus a :class:`Repository` that exposes exactly the
queries the service/CLI/pipeline need. All writes are parameterised; scoring
results are append-only (spec §9.1 "All scoring results immutable once written").

Imported lazily by callers so the pure scoring/stats core never requires
psycopg2 to be installed.
"""
from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool

from .scoring.base import DeliverableSpec, DimensionKind, RubricDimension, ScoreResult
from .scoring.human_review import ReviewerScore

LOG = logging.getLogger("harness.db")


class Database:
    """Owns the connection pool; hands out transactional repositories."""

    def __init__(self, dsn: str, minconn: int = 1, maxconn: int = 10):
        self._pool = ThreadedConnectionPool(minconn, maxconn, dsn=dsn)

    @contextmanager
    def repository(self) -> Iterator[Repository]:
        conn = self._pool.getconn()
        try:
            yield Repository(conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def healthy(self) -> bool:
        try:
            with self.repository() as repo:
                repo.cur.execute("SELECT 1;")
                return repo.cur.fetchone() is not None
        except Exception:  # pragma: no cover
            LOG.exception("db health check failed")
            return False

    def close(self) -> None:
        self._pool.closeall()


class Repository:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # ── lookups ───────────────────────────────────────────────────────────────
    def get_deliverable_spec(self, deliverable_id: str) -> DeliverableSpec | None:
        self.cur.execute(
            """SELECT deliverable_id, role_code, scoring_type, auto_weight, hr_weight,
                      composite_weight, scorer_key, schema_ref, min_sample
               FROM deliverables WHERE deliverable_id = %s AND active;""",
            (deliverable_id,),
        )
        row = self.cur.fetchone()
        if not row:
            return None
        return DeliverableSpec(
            deliverable_id=row["deliverable_id"],
            role_code=row["role_code"],
            scoring_type=row["scoring_type"],
            auto_weight=float(row["auto_weight"]),
            hr_weight=float(row["hr_weight"]),
            composite_weight=float(row["composite_weight"]),
            scorer_key=row["scorer_key"],
            schema_ref=row["schema_ref"],
            min_sample=row["min_sample"],
        )

    def get_rubric_dims(self, deliverable_id: str, rubric_version: str) -> list[RubricDimension]:
        self.cur.execute(
            """SELECT dimension_key, dimension_label, dimension_kind, max_score,
                      threshold, threshold_op, weight, tool
               FROM scoring_rubrics
               WHERE deliverable_id = %s AND rubric_version = %s AND active
               ORDER BY rubric_id;""",
            (deliverable_id, rubric_version),
        )
        dims = []
        for r in self.cur.fetchall():
            dims.append(
                RubricDimension(
                    deliverable_id=deliverable_id,
                    dimension_key=r["dimension_key"],
                    dimension_label=r["dimension_label"],
                    kind=DimensionKind(r["dimension_kind"]),
                    max_score=float(r["max_score"]),
                    threshold=float(r["threshold"]) if r["threshold"] is not None else None,
                    threshold_op=r["threshold_op"],
                    weight=float(r["weight"]),
                    tool=r["tool"],
                )
            )
        return dims

    def rubric_id_map(self, deliverable_id: str, rubric_version: str) -> dict[str, int]:
        self.cur.execute(
            "SELECT dimension_key, rubric_id FROM scoring_rubrics "
            "WHERE deliverable_id = %s AND rubric_version = %s;",
            (deliverable_id, rubric_version),
        )
        return {r["dimension_key"]: r["rubric_id"] for r in self.cur.fetchall()}

    # ── submissions / runs ──────────────────────────────────────────────────────
    def insert_submission(self, **kw) -> dict[str, Any]:
        cols = (
            "role_code", "deliverable_id", "producer_type", "artifact_uri", "artifact_sha256",
            "rubric_version", "agent_id", "task_id", "human_producer_id", "time_spent_minutes",
            "complexity_rating", "human_reviewer_id", "human_accepted", "human_edit_required",
            "edit_effort_minutes", "is_baseline", "metadata_json",
        )
        values = [kw.get(c) for c in cols]
        # JSONB column must be adapted explicitly.
        meta_idx = cols.index("metadata_json")
        values[meta_idx] = psycopg2.extras.Json(kw.get("metadata_json") or {})
        placeholders = ", ".join(["%s"] * len(cols))
        self.cur.execute(
            f"INSERT INTO submissions ({', '.join(cols)}) VALUES ({placeholders}) "
            f"RETURNING submission_id, blind_token;",
            values,
        )
        return self.cur.fetchone()

    def insert_run(self, submission_id: str, rubric_version: str, engine_version: str,
                   result: ScoreResult, rubric_ids: dict[str, int]) -> str:
        self.cur.execute(
            """INSERT INTO evaluation_runs
                 (submission_id, rubric_version, engine_version, status,
                  auto_score, hr_score, composite_score, detail_json, scored_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s, now())
               RETURNING run_id;""",
            (submission_id, rubric_version, engine_version, result.status.value,
             result.auto_score, result.hr_score, result.composite_score,
             psycopg2.extras.Json(result.to_detail_json())),
        )
        run_id = self.cur.fetchone()["run_id"]
        for d in result.dimensions:
            self.cur.execute(
                """INSERT INTO metric_scores
                     (run_id, rubric_id, dimension_key, raw_value, score, max_score, passed, detail)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",
                (run_id, rubric_ids.get(d.dimension_key), d.dimension_key, d.raw_value,
                 d.score, d.max_score, d.passed, d.detail),
            )
        return run_id

    def update_run(self, run_id: str, result: ScoreResult) -> None:
        self.cur.execute(
            """UPDATE evaluation_runs
               SET status=%s, auto_score=%s, hr_score=%s, composite_score=%s,
                   detail_json=%s, scored_at=now()
               WHERE run_id=%s;""",
            (result.status.value, result.auto_score, result.hr_score, result.composite_score,
             psycopg2.extras.Json(result.to_detail_json()), run_id),
        )

    def get_submission(self, submission_id: str) -> dict | None:
        self.cur.execute("SELECT * FROM submissions WHERE submission_id = %s;", (submission_id,))
        return self.cur.fetchone()

    def get_submission_by_blind(self, blind_token: str) -> dict | None:
        self.cur.execute("SELECT * FROM submissions WHERE blind_token = %s;", (blind_token,))
        return self.cur.fetchone()

    def get_run_for_submission(self, submission_id: str) -> dict | None:
        self.cur.execute(
            "SELECT * FROM evaluation_runs WHERE submission_id = %s "
            "ORDER BY created_at DESC LIMIT 1;",
            (submission_id,),
        )
        return self.cur.fetchone()

    # ── finalisation into human_baselines / agent_results ───────────────────────
    def record_finalized(self, submission: dict, run_id: str, result: ScoreResult) -> None:
        if submission["producer_type"] == "HUMAN":
            self.cur.execute(
                """INSERT INTO human_baselines
                     (role_code, deliverable_id, submission_id, run_id, composite_score,
                      time_spent_minutes, complexity_rating, rubric_version)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (submission_id) DO UPDATE SET composite_score = EXCLUDED.composite_score;""",
                (submission["role_code"], submission["deliverable_id"], submission["submission_id"],
                 run_id, result.composite_score, submission.get("time_spent_minutes"),
                 submission.get("complexity_rating"), submission["rubric_version"]),
            )
        else:
            self.cur.execute(
                """INSERT INTO agent_results
                     (role_code, deliverable_id, submission_id, run_id, agent_id, composite_score,
                      human_accepted, human_edit_required, edit_effort_minutes, rubric_version, sprint)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (submission_id) DO UPDATE SET composite_score = EXCLUDED.composite_score,
                     human_accepted = EXCLUDED.human_accepted,
                     human_edit_required = EXCLUDED.human_edit_required;""",
                (submission["role_code"], submission["deliverable_id"], submission["submission_id"],
                 run_id, submission.get("agent_id"), result.composite_score,
                 bool(submission.get("human_accepted")), bool(submission.get("human_edit_required")),
                 submission.get("edit_effort_minutes"), submission["rubric_version"],
                 (submission.get("metadata_json") or {}).get("sprint")),
            )

    # ── human review ────────────────────────────────────────────────────────────
    def insert_review_scores(self, run_id: str, reviewer_id: str,
                             dim_scores: dict[str, float], is_adjudicator: bool) -> None:
        for dim_key, score in dim_scores.items():
            self.cur.execute(
                """INSERT INTO human_review_scores (run_id, reviewer_id, dimension_key, score, is_adjudicator)
                   VALUES (%s,%s,%s,%s,%s)
                   ON CONFLICT (run_id, reviewer_id, dimension_key)
                   DO UPDATE SET score = EXCLUDED.score, submitted_at = now();""",
                (run_id, reviewer_id, dim_key, score, is_adjudicator),
            )

    def get_review_scores(self, run_id: str) -> dict[str, list[ReviewerScore]]:
        self.cur.execute(
            "SELECT reviewer_id, dimension_key, score, is_adjudicator "
            "FROM human_review_scores WHERE run_id = %s ORDER BY submitted_at;",
            (run_id,),
        )
        out: dict[str, list[ReviewerScore]] = {}
        for r in self.cur.fetchall():
            out.setdefault(r["dimension_key"], []).append(
                ReviewerScore(reviewer_id=r["reviewer_id"], score=float(r["score"]),
                              is_adjudicator=r["is_adjudicator"])
            )
        return out

    def review_queue(self) -> list[dict]:
        """Items awaiting human review — blind (no producer identity exposed)."""
        self.cur.execute(
            """SELECT s.blind_token, s.deliverable_id, s.role_code, s.artifact_uri,
                      r.run_id, r.status
               FROM evaluation_runs r
               JOIN submissions s ON s.submission_id = r.submission_id
               WHERE r.status IN ('AWAITING_HR', 'ADJUDICATION')
               ORDER BY r.created_at;"""
        )
        return self.cur.fetchall()

    # ── score distributions for the statistical engine ─────────────────────────
    def baseline_scores(self, role_code: str, deliverable_id: str, rubric_version: str) -> list[float]:
        self.cur.execute(
            "SELECT composite_score FROM human_baselines "
            "WHERE role_code=%s AND deliverable_id=%s AND rubric_version=%s;",
            (role_code, deliverable_id, rubric_version),
        )
        return [float(r["composite_score"]) for r in self.cur.fetchall()]

    def agent_scores(self, role_code: str, deliverable_id: str, rubric_version: str) -> list[float]:
        self.cur.execute(
            "SELECT composite_score FROM agent_results "
            "WHERE role_code=%s AND deliverable_id=%s AND rubric_version=%s;",
            (role_code, deliverable_id, rubric_version),
        )
        return [float(r["composite_score"]) for r in self.cur.fetchall()]

    def draft_acceptance_rate(self, role_code: str, days: int = 90) -> float | None:
        self.cur.execute(
            """SELECT AVG(CASE WHEN draft_accepted THEN 1.0 ELSE 0.0 END) AS rate
               FROM agent_results
               WHERE role_code=%s AND captured_at >= now() - (%s || ' days')::interval;""",
            (role_code, days),
        )
        row = self.cur.fetchone()
        return float(row["rate"]) if row and row["rate"] is not None else None

    def deliverables_for_role(self, role_code: str) -> list[dict]:
        self.cur.execute(
            "SELECT deliverable_id, composite_weight, min_sample FROM deliverables "
            "WHERE role_code=%s AND active ORDER BY deliverable_id;",
            (role_code,),
        )
        return self.cur.fetchall()

    def all_roles(self) -> list[dict]:
        self.cur.execute("SELECT role_code, wave FROM roles ORDER BY wave, role_code;")
        return self.cur.fetchall()

    def upsert_role_readiness(self, **kw) -> None:
        cols = (
            "role_code", "deliverable_id", "rubric_version", "baseline_n", "baseline_mean",
            "baseline_sd", "baseline_p25", "baseline_p75", "baseline_p95", "temporal_stability_flag",
            "agent_n", "agent_mean", "welch_t", "welch_p", "draft_acceptance_rate",
            "sample_threshold_met", "readiness",
        )
        values = [kw.get(c) for c in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        self.cur.execute(
            f"INSERT INTO role_readiness ({', '.join(cols)}) VALUES ({placeholders});",
            values,
        )

    def rubric_integrity_issues(self) -> list[dict]:
        self.cur.execute("SELECT * FROM fn_rubric_integrity_issues();")
        return self.cur.fetchall()

    # ── dashboard / API reads ───────────────────────────────────────────────────
    def latest_readiness(self, role_code: str) -> list[dict]:
        self.cur.execute(
            "SELECT * FROM v_role_readiness_latest WHERE role_code = %s "
            "ORDER BY deliverable_id NULLS FIRST;",
            (role_code,),
        )
        return self.cur.fetchall()

    def wave_gate(self, wave: int) -> dict | None:
        self.cur.execute("SELECT * FROM v_wave_gate_status WHERE wave = %s;", (wave,))
        return self.cur.fetchone()

    def sample_progress(self, role_code: str | None = None) -> list[dict]:
        if role_code:
            self.cur.execute("SELECT * FROM v_sample_progress WHERE role_code = %s "
                             "ORDER BY deliverable_id;", (role_code,))
        else:
            self.cur.execute("SELECT * FROM v_sample_progress ORDER BY role_code, deliverable_id;")
        return self.cur.fetchall()

    def incident_counts(self) -> list[dict]:
        self.cur.execute("SELECT * FROM v_incident_counts;")
        return self.cur.fetchall()
