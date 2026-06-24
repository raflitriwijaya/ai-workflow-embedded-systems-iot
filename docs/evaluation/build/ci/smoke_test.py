#!/usr/bin/env python3
"""End-to-end smoke test against a live PostgreSQL (spec §9.1 "smoke-tested").

Exercises the full DB + service path that the pure unit tests cannot:
  1. schema:OCM auto deliverable ingests and scores 100,
  2. an OCM with a flash budget FAIL is a hard block,
  3. a hybrid deliverable ingests AWAITING_HR, then two blind reviews finalise it
     into human_baselines,
  4. the statistical engine recomputes readiness for the role.

Requires DATABASE_URL (or PG* vars) pointing at a migrated+seeded harness DB.
Exit code 0 = pass.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import yaml

from eval_harness.config import Settings
from eval_harness.db import Database
from eval_harness import service

HEX64 = "a" * 64


def _valid_ocm(util_pct: float = 35.6) -> dict:
    flash_budget = 524288
    flash_required = int(round(flash_budget * util_pct / 100.0))
    result = "PASS" if util_pct <= 80 else ("WARN" if util_pct <= 95 else "FAIL")
    return {
        "model": {"sha256_hash": HEX64, "framework": "TFLITE_MICRO", "quantization": "INT8"},
        "target_hardware": [{"hardware_id": "GW-1", "validated": True}],
        "firmware_compatibility": {"minimum_version": "2.4.2", "excluded_versions": ["2.5.0"]},
        "resource_budget": {
            "flash_required_bytes": flash_required, "flash_budget_bytes": flash_budget,
            "flash_budget_utilisation_pct": round(flash_required / flash_budget * 100.0, 4),
            "ram_peak_bytes": 204800, "ram_budget_bytes": 327680,
            "ram_budget_utilisation_pct": round(204800 / 327680 * 100.0, 4),
        },
        "flash_budget_check": {"result": result, "margin_bytes": flash_budget - flash_required},
        "ram_budget_check": {"result": "PASS", "margin_bytes": 327680 - 204800},
        "security": {"bundle_signature": "c2ln"},
        "deployment": {"rollout_strategy": "CANARY", "canary_percentage": 5},
        "bundle_contents": [{"filename": "m.tflite", "sha256_hash": HEX64, "size_bytes": 1}],
        "dqir_clearance": ["DQIR-0008"],
    }


def _write(tmp: Path, name: str, data: dict) -> str:
    p = tmp / name
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p.resolve().as_uri()


def main() -> int:
    settings = Settings.load()
    db = Database(settings.dsn(), settings.db_min_conn, settings.db_max_conn)
    tmp = Path(tempfile.mkdtemp())
    failures: list[str] = []

    def check(label: str, cond: bool, extra: str = "") -> None:
        print(f"[{'PASS' if cond else 'FAIL'}] {label} {extra}")
        if not cond:
            failures.append(label)

    try:
        if not db.healthy():
            print("DB not reachable")
            return 1

        # 1. schema:OCM auto deliverable scores 100
        ok = service.ingest_submission(
            db, settings, role_code="MLOPS", deliverable_id="D1-ML-4", producer_type="HUMAN",
            artifact_uri=_write(tmp, "ocm_ok.yaml", _valid_ocm()), is_baseline=True,
            human_producer_id="smoke.human",
        )
        check("OCM valid -> SCORED", ok["status"] == "SCORED", str(ok["composite_score"]))
        check("OCM valid -> composite 100", abs((ok["composite_score"] or 0) - 100.0) < 1e-6)
        check("OCM valid -> no hard block", ok["hard_block"] is False)

        # 2. OCM with flash FAIL -> hard block
        bad = service.ingest_submission(
            db, settings, role_code="MLOPS", deliverable_id="D1-ML-4", producer_type="AGENT",
            artifact_uri=_write(tmp, "ocm_fail.yaml", _valid_ocm(util_pct=97.0)),
            agent_id="mlops-agent-smoke",
        )
        check("OCM flash FAIL -> hard block", bad["hard_block"] is True)

        # 3. hybrid deliverable: ingest AWAITING_HR, then two blind reviews -> SCORED
        hyb = service.ingest_submission(
            db, settings, role_code="DATA", deliverable_id="D1-DE-2", producer_type="HUMAN",
            artifact_uri=_write(tmp, "dq.yaml", {"note": "data quality report"}), is_baseline=True,
            human_producer_id="smoke.dataeng",
            metrics={"required_sections_present": True, "slo_thresholds_flagged": True},
        )
        check("HYB -> AWAITING_HR", hyb["status"] == "AWAITING_HR")
        # One reviewer is not enough — spec §4.2 requires two independent reviewers.
        r1 = service.submit_review(db, settings, blind_token=hyb["blind_token"],
                                   reviewer_id="rev.a", dim_scores={"rca_clarity": 3, "findings_actionability": 3})
        check("HYB after 1 reviewer -> still AWAITING_HR", r1["status"] == "AWAITING_HR")
        # Second reviewer finalises the HR sub-score -> SCORED + recorded as baseline.
        r2 = service.submit_review(db, settings, blind_token=hyb["blind_token"],
                                   reviewer_id="rev.b", dim_scores={"rca_clarity": 3, "findings_actionability": 3})
        check("HYB after 2 reviewers -> SCORED", r2["status"] == "SCORED", str(r2["composite_score"]))

        # 4. readiness recompute produces a role rollup
        summary = service.recompute_readiness(db, settings)
        check("readiness recompute covers MLOPS", "MLOPS" in summary["roles"])
        check("readiness recompute covers DATA", "DATA" in summary["roles"])

        if failures:
            print(f"\n{len(failures)} smoke check(s) failed: {failures}")
            return 1
        print("\nAll smoke checks passed.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
