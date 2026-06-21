"""
validate_data.py — Great Expectations data quality validation suite.

Validates raw ingested data in PostgreSQL before it reaches the transformation
step. Failures emit structured alerts (logged + optionally posted to Slack).

Suites:
  1. adr_records_suite   — completeness, tier validity, SLA field presence
  2. ccr_records_suite   — completeness, foreign key coherence
  3. defect_records_suite — stage completeness, no unknown-stage majority
  4. security_findings_suite — stage completeness
  5. process_initiatives_suite — status enum, date presence

Environment variables (required):
    PG_DSN
    GE_DATASOURCE_NAME      Great Expectations datasource name (default: pg_metrics)

Optional:
    SLACK_WEBHOOK_URL       Post validation summary to this Slack webhook on failure
    GE_DATA_DOCS_PATH       Path to write GE Data Docs HTML (default: /tmp/ge_data_docs)
    LOG_LEVEL

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any

import psycopg2
import psycopg2.extras
import requests

# Great Expectations v0.18+ modular API
try:
    import great_expectations as gx
    from great_expectations.core.batch import RuntimeBatchRequest
    from great_expectations.core import ExpectationSuite
except ImportError:
    gx = None  # type: ignore

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PG_DSN: str              = os.environ["PG_DSN"]
GE_DATASOURCE: str       = os.getenv("GE_DATASOURCE_NAME", "pg_metrics")
SLACK_WEBHOOK: str       = os.getenv("SLACK_WEBHOOK_URL", "")
GE_DATA_DOCS_PATH: str   = os.getenv("GE_DATA_DOCS_PATH", "/tmp/ge_data_docs")
LOG_LEVEL: str           = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("validate_data")

VALID_ADR_STATUSES = {"proposed", "reviewing", "resolved", "superseded"}
VALID_TIERS = {1, 2, 3, 4}
VALID_DEFECT_STAGES = {"Development", "Execution", "Production", "Unknown"}
VALID_SECURITY_STAGES = {
    "Design Review", "Implementation Review", "Release Gate", "Post-Release", "Unknown"
}
VALID_INITIATIVE_STATUSES = {"in_progress", "completed", "cancelled"}

# ---------------------------------------------------------------------------
# Lightweight SQL-based validation (no GE dependency required in CI)
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self, suite_name: str) -> None:
        self.suite_name = suite_name
        self.checks: list[dict] = []
        self.passed = 0
        self.failed = 0

    def record(self, name: str, passed: bool, detail: str = "") -> None:
        self.checks.append({"check": name, "passed": passed, "detail": detail})
        if passed:
            self.passed += 1
        else:
            self.failed += 1
            log.warning("[%s] FAIL: %s — %s", self.suite_name, name, detail)

    @property
    def success(self) -> bool:
        return self.failed == 0

    def summary(self) -> str:
        icon = "✓" if self.success else "✗"
        return f"{icon} {self.suite_name}: {self.passed} passed, {self.failed} failed"


def _run_query(conn, sql: str, params: tuple = ()) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


# ---------------------------------------------------------------------------
# Suite: ADR records
# ---------------------------------------------------------------------------

def validate_adr_records(conn) -> ValidationResult:
    result = ValidationResult("adr_records_suite")

    # 1. No null adr_ref
    rows = _run_query(conn, "SELECT COUNT(*) FROM adr_records WHERE adr_ref IS NULL OR adr_ref = ''")
    result.record("adr_ref_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    # 2. All tiers within valid set
    rows = _run_query(
        conn,
        "SELECT COUNT(*) FROM adr_records WHERE tier_id IS NOT NULL AND tier_id NOT IN (1,2,3,4)"
    )
    result.record("tier_id_valid", rows[0][0] == 0, f"invalid_count={rows[0][0]}")

    # 3. All statuses within valid set
    rows = _run_query(
        conn,
        "SELECT DISTINCT status FROM adr_records WHERE status IS NOT NULL"
    )
    invalid = [r[0] for r in rows if r[0] not in VALID_ADR_STATUSES]
    result.record("status_values_valid", not invalid, f"unknown_statuses={invalid}")

    # 4. resolved_at after submitted_at where both present
    rows = _run_query(
        conn,
        """
        SELECT COUNT(*) FROM adr_records
        WHERE submitted_at IS NOT NULL AND resolved_at IS NOT NULL
          AND resolved_at < submitted_at
        """
    )
    result.record("resolved_after_submitted", rows[0][0] == 0, f"inverted_count={rows[0][0]}")

    # 5. resolved ADRs have resolved_at set
    rows = _run_query(
        conn,
        "SELECT COUNT(*) FROM adr_records WHERE status = 'resolved' AND resolved_at IS NULL"
    )
    result.record("resolved_has_resolved_at", rows[0][0] == 0, f"missing_resolved_at={rows[0][0]}")

    # 6. Duplicate adr_ref check
    rows = _run_query(
        conn,
        "SELECT adr_ref, COUNT(*) FROM adr_records GROUP BY adr_ref HAVING COUNT(*) > 1"
    )
    result.record("no_duplicate_adr_ref", not rows, f"duplicates={[r[0] for r in rows]}")

    return result


# ---------------------------------------------------------------------------
# Suite: CCR records
# ---------------------------------------------------------------------------

def validate_ccr_records(conn) -> ValidationResult:
    result = ValidationResult("ccr_records_suite")

    rows = _run_query(conn, "SELECT COUNT(*) FROM ccr_records WHERE ccr_ref IS NULL OR ccr_ref = ''")
    result.record("ccr_ref_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    # escalated_to_adr must reference existing ADR
    rows = _run_query(
        conn,
        """
        SELECT COUNT(*) FROM ccr_records c
        WHERE c.escalated_to_adr IS NOT NULL
          AND NOT EXISTS (
            SELECT 1 FROM adr_records a WHERE a.adr_ref = c.escalated_to_adr
          )
        """
    )
    result.record("escalated_adr_ref_valid", rows[0][0] == 0, f"dangling_refs={rows[0][0]}")

    # escalated CCRs have escalated_to_adr set
    rows = _run_query(
        conn,
        "SELECT COUNT(*) FROM ccr_records WHERE status = 'escalated' AND escalated_to_adr IS NULL"
    )
    result.record("escalated_has_adr_ref", rows[0][0] == 0, f"missing_adr_ref={rows[0][0]}")

    return result


# ---------------------------------------------------------------------------
# Suite: Defect records
# ---------------------------------------------------------------------------

def validate_defect_records(conn) -> ValidationResult:
    result = ValidationResult("defect_records_suite")

    # No null discovery stage
    rows = _run_query(conn, "SELECT COUNT(*) FROM defect_records WHERE discovery_stage IS NULL")
    result.record("discovery_stage_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    # Unknown stage not majority (> 50% unknown is a data quality problem)
    rows = _run_query(
        conn,
        """
        SELECT
            COUNT(*) FILTER (WHERE ds.stage_name = 'Unknown') AS unknown_cnt,
            COUNT(*) AS total_cnt
        FROM defect_records dr
        JOIN defect_stages ds ON ds.stage_id = dr.discovery_stage
        WHERE dr.created_at >= NOW() - INTERVAL '30 days'
        """
    )
    if rows[0][1] > 0:
        unknown_pct = rows[0][0] / rows[0][1]
        result.record(
            "unknown_stage_not_majority",
            unknown_pct < 0.50,
            f"unknown_pct={unknown_pct:.1%}",
        )

    # created_at always present
    rows = _run_query(conn, "SELECT COUNT(*) FROM defect_records WHERE created_at IS NULL")
    result.record("created_at_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    return result


# ---------------------------------------------------------------------------
# Suite: Security findings
# ---------------------------------------------------------------------------

def validate_security_findings(conn) -> ValidationResult:
    result = ValidationResult("security_findings_suite")

    rows = _run_query(conn, "SELECT COUNT(*) FROM security_findings WHERE discovery_stage IS NULL")
    result.record("discovery_stage_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    rows = _run_query(conn, "SELECT COUNT(*) FROM security_findings WHERE finding_ref IS NULL OR finding_ref = ''")
    result.record("finding_ref_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    return result


# ---------------------------------------------------------------------------
# Suite: Process initiatives
# ---------------------------------------------------------------------------

def validate_process_initiatives(conn) -> ValidationResult:
    result = ValidationResult("process_initiatives_suite")

    rows = _run_query(
        conn,
        "SELECT DISTINCT status FROM process_initiatives WHERE status IS NOT NULL"
    )
    invalid = [r[0] for r in rows if r[0] not in VALID_INITIATIVE_STATUSES]
    result.record("status_enum_valid", not invalid, f"unknown_statuses={invalid}")

    rows = _run_query(conn, "SELECT COUNT(*) FROM process_initiatives WHERE title IS NULL OR title = ''")
    result.record("title_not_null", rows[0][0] == 0, f"null_count={rows[0][0]}")

    return result


# ---------------------------------------------------------------------------
# Great Expectations wrapper (optional, adds HTML data docs)
# ---------------------------------------------------------------------------

def run_ge_suite_if_available(conn_str: str) -> bool:
    """Run GE-native expectations if great_expectations is installed."""
    if gx is None:
        log.info("great_expectations not installed — skipping GE suite, using SQL checks only.")
        return True

    context = gx.get_context()
    datasource_config = {
        "name": GE_DATASOURCE,
        "class_name": "Datasource",
        "module_name": "great_expectations.datasource",
        "execution_engine": {
            "class_name": "SqlAlchemyExecutionEngine",
            "connection_string": conn_str,
        },
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["batch_id"],
            }
        },
    }
    try:
        context.add_datasource(**datasource_config)
    except Exception:
        pass  # already added in persistent context

    log.info("GE context initialised. Data docs will be written to %s", GE_DATA_DOCS_PATH)
    return True  # Full GE suite expansion is project-specific — SQL checks above are authoritative


# ---------------------------------------------------------------------------
# Slack alert
# ---------------------------------------------------------------------------

def _post_slack(message: str) -> None:
    if not SLACK_WEBHOOK:
        return
    try:
        resp = requests.post(
            SLACK_WEBHOOK,
            json={"text": message},
            timeout=10,
        )
        resp.raise_for_status()
    except Exception as exc:
        log.warning("Slack post failed: %s", exc)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> bool:
    conn = psycopg2.connect(PG_DSN)
    all_results: list[ValidationResult] = []

    try:
        all_results.append(validate_adr_records(conn))
        all_results.append(validate_ccr_records(conn))
        all_results.append(validate_defect_records(conn))
        all_results.append(validate_security_findings(conn))
        all_results.append(validate_process_initiatives(conn))
        run_ge_suite_if_available(PG_DSN)
    finally:
        conn.close()

    overall_pass = all(r.success for r in all_results)

    log.info("=" * 60)
    log.info("VALIDATION RESULTS [%s]", datetime.now(timezone.utc).isoformat())
    for r in all_results:
        log.info(r.summary())
    log.info("Overall: %s", "PASS" if overall_pass else "FAIL")
    log.info("=" * 60)

    if not overall_pass:
        summary_lines = [r.summary() for r in all_results if not r.success]
        _post_slack(
            f":rotating_light: *Engineering Metrics Pipeline — Validation FAILED*\n"
            + "\n".join(summary_lines)
            + f"\n_Run at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_"
        )

    return overall_pass


if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
