"""Service layer — orchestrates ingest → score → persist, review, and readiness.

Shared by the FastAPI app, the CLIs, and the statistical engine so the business
logic lives in exactly one place. Each public function opens its own DB
transaction via ``Database.repository()``.
"""
from __future__ import annotations

import logging
from typing import Any

from .artifacts import parse_artifact, read_bytes, sha256_hex
from .config import Settings
from .db import Database
from .scoring import RunStatus, score_submission
from .stats import compute_deliverable_readiness, roll_up_role
from .stats.readiness import ReadinessResult

LOG = logging.getLogger("harness.service")


class IngestError(ValueError):
    """Raised for caller-correctable ingest problems (unknown deliverable, etc.)."""


def _needs_artifact_parse(spec) -> bool:
    return spec.scorer_key.startswith("schema:") or bool(spec.schema_ref)


def ingest_submission(
    db: Database,
    settings: Settings,
    *,
    role_code: str,
    deliverable_id: str,
    producer_type: str,
    artifact_uri: str,
    raw_bytes: bytes | None = None,
    metrics: dict[str, Any] | None = None,
    is_baseline: bool = False,
    agent_id: str | None = None,
    task_id: str | None = None,
    human_producer_id: str | None = None,
    time_spent_minutes: int | None = None,
    complexity_rating: int | None = None,
    human_reviewer_id: str | None = None,
    human_accepted: bool | None = None,
    human_edit_required: bool | None = None,
    edit_effort_minutes: int | None = None,
    extra_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalise, score, and persist a single artifact submission (spec §2.3)."""
    if producer_type not in ("HUMAN", "AGENT"):
        raise IngestError(f"producer_type must be HUMAN or AGENT, got {producer_type!r}")

    with db.repository() as repo:
        spec = repo.get_deliverable_spec(deliverable_id)
        if spec is None:
            raise IngestError(f"unknown/inactive deliverable {deliverable_id!r}")
        if spec.role_code != role_code:
            raise IngestError(
                f"deliverable {deliverable_id} belongs to {spec.role_code}, not {role_code}"
            )
        dims = repo.get_rubric_dims(deliverable_id, settings.rubric_version)

        if raw_bytes is None:
            raw_bytes = read_bytes(artifact_uri, settings)
        sha = sha256_hex(raw_bytes)
        artifact_data = parse_artifact(artifact_uri, raw_bytes) if _needs_artifact_parse(spec) else None

        metadata = dict(extra_metadata or {})
        if metrics is not None:
            metadata["metrics"] = metrics

        sub = repo.insert_submission(
            role_code=role_code, deliverable_id=deliverable_id, producer_type=producer_type,
            artifact_uri=artifact_uri, artifact_sha256=sha, rubric_version=settings.rubric_version,
            agent_id=agent_id, task_id=task_id, human_producer_id=human_producer_id,
            time_spent_minutes=time_spent_minutes, complexity_rating=complexity_rating,
            human_reviewer_id=human_reviewer_id, human_accepted=human_accepted,
            human_edit_required=human_edit_required, edit_effort_minutes=edit_effort_minutes,
            is_baseline=is_baseline, metadata_json=metadata,
        )
        submission_id = str(sub["submission_id"])

        result = score_submission(spec, dims, metrics=metrics, artifact_data=artifact_data)
        rubric_ids = repo.rubric_id_map(deliverable_id, settings.rubric_version)
        run_id = repo.insert_run(submission_id, settings.rubric_version, settings.engine_version,
                                 result, rubric_ids)

        if result.status == RunStatus.SCORED:
            submission_row = repo.get_submission(submission_id)
            repo.record_finalized(submission_row, run_id, result)

        LOG.info("ingested submission", extra={"submission_id": submission_id, "run_id": run_id,
                                               "role": role_code, "deliverable_id": deliverable_id})
        return {
            "submission_id": submission_id,
            "blind_token": str(sub["blind_token"]),
            "run_id": str(run_id),
            "status": result.status.value,
            "auto_score": result.auto_score,
            "hr_score": result.hr_score,
            "composite_score": result.composite_score,
            "hard_block": result.hard_block,
            "messages": result.messages,
        }


def submit_review(
    db: Database,
    settings: Settings,
    *,
    blind_token: str,
    reviewer_id: str,
    dim_scores: dict[str, float],
    is_adjudicator: bool = False,
) -> dict[str, Any]:
    """Record one reviewer's blind rubric scores and re-aggregate the HR sub-score."""
    with db.repository() as repo:
        sub = repo.get_submission_by_blind(blind_token)
        if sub is None:
            raise IngestError(f"no submission for blind_token {blind_token!r}")
        # Blind-scoring integrity: a reviewer may not score their own artifact.
        if reviewer_id and reviewer_id == sub.get("human_producer_id"):
            raise IngestError("reviewer may not score their own submission (blind-scoring violation)")

        run = repo.get_run_for_submission(str(sub["submission_id"]))
        if run is None:
            raise IngestError("no evaluation run found for submission")
        run_id = str(run["run_id"])

        repo.insert_review_scores(run_id, reviewer_id, dim_scores, is_adjudicator)

        spec = repo.get_deliverable_spec(sub["deliverable_id"])
        dims = repo.get_rubric_dims(sub["deliverable_id"], sub["rubric_version"])
        metrics = (sub.get("metadata_json") or {}).get("metrics")
        reviews = repo.get_review_scores(run_id)

        result = score_submission(spec, dims, metrics=metrics, reviewer_scores=reviews)
        repo.update_run(run_id, result)
        if result.status == RunStatus.SCORED:
            repo.record_finalized(sub, run_id, result)

        return {
            "run_id": run_id,
            "status": result.status.value,
            "hr_score": result.hr_score,
            "composite_score": result.composite_score,
        }


def recompute_readiness(db: Database, settings: Settings) -> dict[str, Any]:
    """Recompute baseline stats + agent-vs-baseline readiness for every role.

    This is the body of the scheduled statistical engine (spec §2.3 step 6).
    Writes one role_readiness row per deliverable plus a role-level rollup
    (deliverable_id = NULL).
    """
    summary: dict[str, Any] = {"roles": {}}
    rv = settings.rubric_version
    with db.repository() as repo:
        roles = repo.all_roles()
        for role in roles:
            role_code = role["role_code"]
            deliverables = repo.deliverables_for_role(role_code)
            if not deliverables:
                continue  # no Wave-1 rubric seeded for this role yet
            draft_rate = repo.draft_acceptance_rate(role_code)
            per_deliverable: dict[str, ReadinessResult] = {}
            weights: dict[str, float] = {}

            for d in deliverables:
                did = d["deliverable_id"]
                weights[did] = float(d["composite_weight"])
                baseline = repo.baseline_scores(role_code, did, rv)
                agent = repo.agent_scores(role_code, did, rv)
                res = compute_deliverable_readiness(
                    baseline, agent, min_sample=d["min_sample"], draft_acceptance_rate=draft_rate
                )
                per_deliverable[did] = res
                repo.upsert_role_readiness(
                    role_code=role_code, deliverable_id=did, rubric_version=rv,
                    baseline_n=res.baseline_n, baseline_mean=res.baseline_mean,
                    baseline_sd=res.baseline_sd, baseline_p25=res.baseline_p25,
                    baseline_p75=res.baseline_p75, baseline_p95=res.baseline_p95,
                    temporal_stability_flag=res.temporal_stability_flag,
                    agent_n=res.agent_n, agent_mean=res.agent_mean,
                    welch_t=res.welch.t if res.welch else None,
                    welch_p=res.welch.p_one_tailed if res.welch else None,
                    draft_acceptance_rate=res.draft_acceptance_rate,
                    sample_threshold_met=res.sample_threshold_met, readiness=res.readiness,
                )

            rollup = roll_up_role(role_code, per_deliverable, weights, draft_rate)
            repo.upsert_role_readiness(
                role_code=role_code, deliverable_id=None, rubric_version=rv,
                baseline_n=sum(r.baseline_n for r in per_deliverable.values()),
                baseline_mean=rollup.composite_baseline_mean, baseline_sd=None,
                baseline_p25=None, baseline_p75=None, baseline_p95=None,
                temporal_stability_flag=any(r.temporal_stability_flag for r in per_deliverable.values()),
                agent_n=sum(r.agent_n for r in per_deliverable.values()),
                agent_mean=rollup.composite_agent_mean, welch_t=None, welch_p=None,
                draft_acceptance_rate=draft_rate,
                sample_threshold_met=all(r.sample_threshold_met for r in per_deliverable.values()),
                readiness=rollup.readiness,
            )
            summary["roles"][role_code] = rollup.as_dict()
    return summary
