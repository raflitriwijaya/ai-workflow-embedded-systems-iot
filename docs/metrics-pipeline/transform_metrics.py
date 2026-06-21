"""
transform_metrics.py — Derived metrics computation for the Engineering Metrics Pipeline.

Reads raw time-series from InfluxDB and dimensional data from PostgreSQL,
computes derived KPIs, and writes process_health_kpis measurement back to InfluxDB
plus daily_metric_snapshots rows to PostgreSQL.

Derived metrics:
  - shift_left_ratio           : % defects found in Development stage (target ≥60%)
  - production_defect_rate     : % defects found in Production (target ≤10%)
  - security_shift_left_ratio  : % security findings at Design or Implementation Review (target ≥70%)
  - security_post_release_rate : % security findings Post-Release (target ≤5%)
  - contract_clarity_index     : CCRs escalated to ADRs / total CCRs (target ≤20%)
  - adr_sla_compliance_pct     : % ADRs resolved within their tier SLA (per tier and overall)
  - initiative_completion_rate : % process improvement initiatives completed on time (target ≥80%)

Environment variables (required):
    INFLUXDB_URL
    INFLUXDB_TOKEN
    INFLUXDB_ORG
    INFLUXDB_BUCKET_RAW
    INFLUXDB_BUCKET_AGG         Aggregated bucket (36-month retention)
    PG_DSN

Optional:
    TRANSFORM_LOOKBACK_DAYS     Window for aggregation (default: 30)
    LOG_LEVEL

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any

import psycopg2
import psycopg2.extras
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.query_api import QueryApi

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INFLUXDB_URL: str        = os.environ["INFLUXDB_URL"]
INFLUXDB_TOKEN: str      = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_ORG: str        = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET_RAW: str = os.environ["INFLUXDB_BUCKET_RAW"]
INFLUXDB_BUCKET_AGG: str = os.environ["INFLUXDB_BUCKET_AGG"]
PG_DSN: str              = os.environ["PG_DSN"]
LOOKBACK_DAYS: int       = int(os.getenv("TRANSFORM_LOOKBACK_DAYS", "30"))

LOG_LEVEL: str           = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("transform_metrics")

# SLA targets (hours) — must match schema.sql adr_tiers
TIER_SLA_HOURS: dict[int, float] = {1: 4.0, 2: 48.0, 3: 120.0, 4: 240.0}

# ---------------------------------------------------------------------------
# Flux query helpers
# ---------------------------------------------------------------------------

def _flux_range(lookback_days: int) -> str:
    return f"start: -{lookback_days}d"


def _query_flux(query_api: QueryApi, flux: str) -> list[dict]:
    """Execute Flux query and return list of record dicts."""
    tables = query_api.query(flux, org=INFLUXDB_ORG)
    rows: list[dict] = []
    for table in tables:
        for record in table.records:
            rows.append(record.values)
    return rows


# ---------------------------------------------------------------------------
# Shift-left ratio (defects)
# ---------------------------------------------------------------------------

def compute_shift_left(query_api: QueryApi, lookback_days: int) -> dict[str, float]:
    """
    Returns {'Development': pct, 'Execution': pct, 'Production': pct}.
    Reads from jira_metrics measurement, field defect_count, tag discovery_stage.
    """
    flux = f"""
from(bucket: "{INFLUXDB_BUCKET_RAW}")
  |> range({_flux_range(lookback_days)})
  |> filter(fn: (r) => r._measurement == "jira_metrics" and r.metric_type == "defect")
  |> filter(fn: (r) => r._field == "defect_count")
  |> group(columns: ["discovery_stage"])
  |> sum(column: "_value")
"""
    rows = _query_flux(query_api, flux)
    counts: dict[str, int] = {}
    for row in rows:
        stage = row.get("discovery_stage", "Unknown")
        counts[stage] = counts.get(stage, 0) + int(row.get("_value", 0))

    total = sum(counts.values())
    if total == 0:
        log.warning("No defect records in last %d days", lookback_days)
        return {"Development": 0.0, "Execution": 0.0, "Production": 0.0}

    return {
        stage: round(count / total * 100, 2)
        for stage, count in counts.items()
    }


# ---------------------------------------------------------------------------
# Security findings shift-left
# ---------------------------------------------------------------------------

def compute_security_shift_left(pg_conn) -> dict[str, float]:
    """Reads security_findings from PostgreSQL, returns stage distribution %."""
    with pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT sfs.stage_name, COUNT(*) AS cnt
            FROM security_findings sf
            JOIN security_finding_stages sfs ON sfs.stage_id = sf.discovery_stage
            WHERE sf.created_at >= NOW() - INTERVAL '30 days'
            GROUP BY sfs.stage_name
        """)
        rows = cur.fetchall()

    counts = {row["stage_name"]: int(row["cnt"]) for row in rows}
    total = sum(counts.values())
    if total == 0:
        return {}

    return {stage: round(cnt / total * 100, 2) for stage, cnt in counts.items()}


# ---------------------------------------------------------------------------
# Contract clarity index (CCR escalation rate)
# ---------------------------------------------------------------------------

def compute_contract_clarity_index(pg_conn) -> float:
    """CCRs escalated to ADRs / total CCRs in lookback window. Target ≤0.20."""
    with pg_conn.cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*) FILTER (WHERE escalated_to_adr IS NOT NULL) AS escalated,
                COUNT(*) AS total
            FROM ccr_records
            WHERE created_at >= NOW() - INTERVAL '30 days'
        """)
        row = cur.fetchone()

    escalated, total = (row[0] or 0), (row[1] or 0)
    rate = escalated / total if total > 0 else 0.0
    log.info("CCR escalation rate: %d/%d = %.3f", escalated, total, rate)
    return round(rate, 4)


# ---------------------------------------------------------------------------
# ADR SLA compliance
# ---------------------------------------------------------------------------

def compute_adr_sla_compliance(pg_conn) -> dict[str, float]:
    """
    Returns {'overall': pct, 'tier_1': pct, 'tier_2': pct, 'tier_3': pct, 'tier_4': pct}.
    """
    with pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT
                ar.tier_id,
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE ar.sla_met = TRUE) AS met
            FROM adr_records ar
            WHERE ar.resolved_at >= NOW() - INTERVAL '30 days'
              AND ar.tier_id IS NOT NULL
            GROUP BY ar.tier_id
        """)
        rows = cur.fetchall()

    result: dict[str, float] = {}
    total_all, met_all = 0, 0
    for row in rows:
        tier_id = row["tier_id"]
        total, met = int(row["total"]), int(row["met"])
        total_all += total
        met_all   += met
        pct = round(met / total * 100, 2) if total > 0 else 0.0
        result[f"tier_{tier_id}"] = pct

    result["overall"] = round(met_all / total_all * 100, 2) if total_all > 0 else 0.0
    log.info("ADR SLA compliance: %s", result)
    return result


# ---------------------------------------------------------------------------
# Initiative completion rate
# ---------------------------------------------------------------------------

def compute_initiative_completion_rate(pg_conn) -> float:
    """% of process improvement initiatives completed (status='completed'). Target ≥80%."""
    with pg_conn.cursor() as cur:
        cur.execute("""
            SELECT
                COUNT(*) FILTER (WHERE status = 'completed') AS completed,
                COUNT(*) FILTER (WHERE status IN ('completed','in_progress')) AS total
            FROM process_initiatives
            WHERE target_date <= CURRENT_DATE + INTERVAL '0 days'
        """)
        row = cur.fetchone()

    completed, total = (row[0] or 0), (row[1] or 0)
    rate = round(completed / total * 100, 2) if total > 0 else 0.0
    log.info("Initiative completion rate: %d/%d = %.1f%%", completed, total, rate)
    return rate


# ---------------------------------------------------------------------------
# Build InfluxDB Points
# ---------------------------------------------------------------------------

def _build_health_kpi_points(
    shift_left: dict[str, float],
    security_sl: dict[str, float],
    cci: float,
    adr_sla: dict[str, float],
    initiative_rate: float,
    now: datetime,
) -> list[Point]:
    points: list[Point] = []

    # Shift-left (defects)
    sl_dev  = shift_left.get("Development", 0.0)
    sl_prod = shift_left.get("Production", 0.0)
    pt_sl = (
        Point("process_health_kpis")
        .tag("metric_category", "defect_shift_left")
        .field("shift_left_ratio", sl_dev)
        .field("production_defect_rate", sl_prod)
        .time(now, WritePrecision.SECONDS)
    )
    points.append(pt_sl)

    # Security shift-left
    sec_early = (
        security_sl.get("Design Review", 0.0) +
        security_sl.get("Implementation Review", 0.0)
    )
    sec_post = security_sl.get("Post-Release", 0.0)
    pt_sec = (
        Point("process_health_kpis")
        .tag("metric_category", "security_shift_left")
        .field("security_shift_left_ratio", sec_early)
        .field("security_post_release_rate", sec_post)
        .time(now, WritePrecision.SECONDS)
    )
    points.append(pt_sec)

    # Contract clarity index
    pt_cci = (
        Point("process_health_kpis")
        .tag("metric_category", "governance")
        .field("contract_clarity_index", cci)
        .time(now, WritePrecision.SECONDS)
    )
    points.append(pt_cci)

    # ADR SLA compliance
    pt_adr = (
        Point("process_health_kpis")
        .tag("metric_category", "adr_governance")
        .field("adr_sla_compliance_overall", adr_sla.get("overall", 0.0))
    )
    for k, v in adr_sla.items():
        if k != "overall":
            pt_adr = pt_adr.field(f"adr_sla_{k}", v)
    pt_adr = pt_adr.time(now, WritePrecision.SECONDS)
    points.append(pt_adr)

    # Initiative completion rate
    pt_init = (
        Point("process_health_kpis")
        .tag("metric_category", "process_improvement")
        .field("initiative_completion_rate", initiative_rate)
        .time(now, WritePrecision.SECONDS)
    )
    points.append(pt_init)

    return points


# ---------------------------------------------------------------------------
# PostgreSQL snapshot upsert
# ---------------------------------------------------------------------------

def _write_daily_snapshots(metrics: dict[str, float], snapshot_date: date, pg_conn) -> None:
    with pg_conn, pg_conn.cursor() as cur:
        for metric_name, value in metrics.items():
            # Attempt to split "metric:dim_key:dim_val" convention
            parts = metric_name.split(":", 2)
            m_name = parts[0]
            d_key  = parts[1] if len(parts) > 1 else None
            d_val  = parts[2] if len(parts) > 2 else None

            cur.execute(
                """
                INSERT INTO daily_metric_snapshots
                    (snapshot_date, metric_name, metric_value, dimension_key, dimension_value)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (snapshot_date, metric_name, dimension_key, dimension_value)
                    DO UPDATE SET metric_value = EXCLUDED.metric_value,
                                  computed_at  = NOW()
                """,
                (snapshot_date, m_name, value, d_key, d_val),
            )
    log.info("Wrote %d daily snapshot rows for %s", len(metrics), snapshot_date)


# ---------------------------------------------------------------------------
# InfluxDB write
# ---------------------------------------------------------------------------

def write_points(points: list[Point]) -> None:
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=INFLUXDB_BUCKET_AGG, record=points)
    log.info("Wrote %d KPI points to InfluxDB bucket=%s", len(points), INFLUXDB_BUCKET_AGG)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(lookback_days: int = LOOKBACK_DAYS) -> None:
    now = datetime.now(timezone.utc)
    pg_conn = psycopg2.connect(PG_DSN)

    try:
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as influx:
            query_api = influx.query_api()

            shift_left       = compute_shift_left(query_api, lookback_days)
            security_sl      = compute_security_shift_left(pg_conn)
            cci              = compute_contract_clarity_index(pg_conn)
            adr_sla          = compute_adr_sla_compliance(pg_conn)
            initiative_rate  = compute_initiative_completion_rate(pg_conn)

            points = _build_health_kpi_points(
                shift_left, security_sl, cci, adr_sla, initiative_rate, now
            )
            write_points(points)

        # Flatten metrics for snapshot
        flat: dict[str, float] = {
            "shift_left_ratio":           shift_left.get("Development", 0.0),
            "production_defect_rate":     shift_left.get("Production", 0.0),
            "security_shift_left_ratio":  (
                security_sl.get("Design Review", 0.0) +
                security_sl.get("Implementation Review", 0.0)
            ),
            "security_post_release_rate": security_sl.get("Post-Release", 0.0),
            "contract_clarity_index":     cci,
            "adr_sla_compliance_overall": adr_sla.get("overall", 0.0),
            "initiative_completion_rate": initiative_rate,
        }
        for k, v in adr_sla.items():
            flat[f"adr_sla:{k}:"] = v

        _write_daily_snapshots(flat, now.date(), pg_conn)

    finally:
        pg_conn.close()

    log.info("Transform complete.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compute and write derived process KPIs")
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args()
    run(lookback_days=args.lookback_days)
