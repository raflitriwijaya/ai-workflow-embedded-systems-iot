"""
ingest_adr.py — ADR/CCR metrics ingestion for the Engineering Metrics Pipeline.

Walks Git-backed ADR and CCR repositories, parses YAML frontmatter from Markdown
files, and extracts:
  - ADR turnaround time per decision tier (target SLAs: T1≤4h, T2≤48h, T3≤120h, T4≤240h)
  - CCR escalation rate (CCRs escalated to ADRs / total CCRs)
  - ADR volume by decision class

ADR frontmatter schema expected (YAML between --- delimiters):
    adr_ref: ADR-0042
    title: "Adopt InfluxDB for time-series storage"
    tier: 2
    decision_class: "Data Architecture"
    status: "resolved"             # proposed | reviewing | resolved | superseded
    submitted_at: "2024-01-10T09:00:00Z"
    resolved_at: "2024-01-11T14:30:00Z"

CCR frontmatter schema:
    ccr_ref: CCR-0017
    title: "Clarify data retention policy"
    status: "escalated"           # open | resolved | escalated
    escalated_to_adr: "ADR-0042"  # present only if escalated
    created_at: "2024-01-09T08:00:00Z"
    resolved_at: "2024-01-11T14:30:00Z"

Environment variables (required):
    ADR_REPO_PATH           Absolute path to the ADR/CCR Git repo (already cloned)
    ADR_GLOB_PATTERN        Glob to find ADR files, default: "**/adr-*.md"
    CCR_GLOB_PATTERN        Glob to find CCR files, default: "**/ccr-*.md"
    INFLUXDB_URL
    INFLUXDB_TOKEN
    INFLUXDB_ORG
    INFLUXDB_BUCKET_RAW
    PG_DSN

Optional:
    ADR_LOOKBACK_DAYS       Only process ADRs resolved within N days (default: 7)
    LOG_LEVEL

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import psycopg2
import psycopg2.extras
import yaml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ADR_REPO_PATH: Path   = Path(os.environ["ADR_REPO_PATH"])
ADR_GLOB: str         = os.getenv("ADR_GLOB_PATTERN", "**/adr-*.md")
CCR_GLOB: str         = os.getenv("CCR_GLOB_PATTERN", "**/ccr-*.md")
LOOKBACK_DAYS: int    = int(os.getenv("ADR_LOOKBACK_DAYS", "7"))

INFLUXDB_URL: str     = os.environ["INFLUXDB_URL"]
INFLUXDB_TOKEN: str   = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_ORG: str     = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET: str  = os.environ["INFLUXDB_BUCKET_RAW"]
PG_DSN: str           = os.environ["PG_DSN"]

LOG_LEVEL: str        = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("ingest_adr")

# Tier SLA targets (hours)
TIER_SLA_HOURS: dict[int, float] = {1: 4.0, 2: 48.0, 3: 120.0, 4: 240.0}

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def _parse_frontmatter(text: str) -> dict[str, Any]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        log.debug("YAML parse error: %s", exc)
        return {}


def _parse_ts(val: Any) -> datetime | None:
    if val is None:
        return None
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val
    if isinstance(val, str):
        try:
            dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
            return dt
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# ADR ingestion
# ---------------------------------------------------------------------------

def _load_adr_files(since: datetime) -> list[dict]:
    records: list[dict] = []
    for path in ADR_REPO_PATH.glob(ADR_GLOB):
        try:
            fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
        except OSError as exc:
            log.warning("Cannot read %s: %s", path, exc)
            continue

        adr_ref = str(fm.get("adr_ref", "")).strip()
        if not adr_ref:
            log.debug("Skipping %s — no adr_ref in frontmatter", path.name)
            continue

        submitted_at  = _parse_ts(fm.get("submitted_at") or fm.get("created_at"))
        resolved_at   = _parse_ts(fm.get("resolved_at"))
        status        = str(fm.get("status", "proposed")).lower()

        # Apply lookback filter on resolved date
        if resolved_at and resolved_at < since:
            continue

        tier_raw = fm.get("tier")
        try:
            tier = int(tier_raw) if tier_raw is not None else None
        except (TypeError, ValueError):
            tier = None

        turnaround_h: float | None = None
        sla_met: bool | None = None
        if submitted_at and resolved_at:
            turnaround_h = (resolved_at - submitted_at).total_seconds() / 3600.0
            if tier and tier in TIER_SLA_HOURS:
                sla_met = turnaround_h <= TIER_SLA_HOURS[tier]

        records.append({
            "adr_ref":         adr_ref,
            "title":           str(fm.get("title", "")).strip(),
            "tier":            tier,
            "decision_class":  str(fm.get("decision_class", "Uncategorised")).strip(),
            "status":          status,
            "submitted_at":    submitted_at,
            "resolved_at":     resolved_at,
            "turnaround_h":    turnaround_h,
            "sla_met":         sla_met,
            "repo_path":       str(path),
        })

    log.info("Loaded %d ADR records (since=%s)", len(records), since.date())
    return records


# ---------------------------------------------------------------------------
# CCR ingestion
# ---------------------------------------------------------------------------

def _load_ccr_files(since: datetime) -> list[dict]:
    records: list[dict] = []
    for path in ADR_REPO_PATH.glob(CCR_GLOB):
        try:
            fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
        except OSError as exc:
            log.warning("Cannot read %s: %s", path, exc)
            continue

        ccr_ref = str(fm.get("ccr_ref", "")).strip()
        if not ccr_ref:
            log.debug("Skipping %s — no ccr_ref", path.name)
            continue

        created_at  = _parse_ts(fm.get("created_at"))
        resolved_at = _parse_ts(fm.get("resolved_at"))

        if created_at and created_at < since:
            continue

        records.append({
            "ccr_ref":           ccr_ref,
            "title":             str(fm.get("title", "")).strip(),
            "status":            str(fm.get("status", "open")).lower(),
            "escalated_to_adr":  fm.get("escalated_to_adr"),
            "created_at":        created_at,
            "resolved_at":       resolved_at,
            "repo_path":         str(path),
        })

    log.info("Loaded %d CCR records (since=%s)", len(records), since.date())
    return records


# ---------------------------------------------------------------------------
# Build InfluxDB points
# ---------------------------------------------------------------------------

def _build_adr_points(adrs: list[dict]) -> list[Point]:
    points: list[Point] = []
    for rec in adrs:
        tier_str = str(rec["tier"]) if rec["tier"] else "unknown"
        pt = (
            Point("adr_metrics")
            .tag("tier", tier_str)
            .tag("decision_class", rec["decision_class"])
            .tag("status", rec["status"])
            .tag("sla_met", str(rec["sla_met"]).lower() if rec["sla_met"] is not None else "unknown")
            .field("adr_count", 1)
        )
        if rec["turnaround_h"] is not None:
            pt = pt.field("turnaround_hours", round(rec["turnaround_h"], 2))
        if rec["sla_met"] is not None:
            pt = pt.field("sla_met_int", int(rec["sla_met"]))

        ts = rec["resolved_at"] or rec["submitted_at"] or datetime.now(timezone.utc)
        pt = pt.time(ts, WritePrecision.SECONDS)
        points.append(pt)
    return points


def _build_ccr_points(ccrs: list[dict], total_ccrs: int) -> list[Point]:
    points: list[Point] = []
    escalated = sum(1 for c in ccrs if c.get("escalated_to_adr"))
    escalation_rate = escalated / total_ccrs if total_ccrs > 0 else 0.0

    summary_pt = (
        Point("adr_metrics")
        .tag("metric_type", "ccr_summary")
        .field("total_ccrs", total_ccrs)
        .field("escalated_ccrs", escalated)
        .field("ccr_escalation_rate", round(escalation_rate, 4))
        .time(datetime.now(timezone.utc), WritePrecision.SECONDS)
    )
    points.append(summary_pt)

    for rec in ccrs:
        pt = (
            Point("adr_metrics")
            .tag("metric_type", "ccr_record")
            .tag("status", rec["status"])
            .tag("escalated", str(bool(rec.get("escalated_to_adr"))).lower())
            .field("ccr_count", 1)
        )
        ts = rec["created_at"] or datetime.now(timezone.utc)
        pt = pt.time(ts, WritePrecision.SECONDS)
        points.append(pt)

    return points


# ---------------------------------------------------------------------------
# PostgreSQL upserts
# ---------------------------------------------------------------------------

def _upsert_adrs_to_pg(adrs: list[dict]) -> None:
    if not adrs:
        return
    conn = psycopg2.connect(PG_DSN)
    try:
        with conn, conn.cursor() as cur:
            for rec in adrs:
                # Ensure decision_class exists
                cur.execute(
                    "INSERT INTO decision_classes (class_name) VALUES (%s) ON CONFLICT DO NOTHING",
                    (rec["decision_class"],),
                )
                cur.execute(
                    "SELECT class_id FROM decision_classes WHERE class_name = %s",
                    (rec["decision_class"],),
                )
                row = cur.fetchone()
                class_id = row[0] if row else None

                cur.execute(
                    """
                    INSERT INTO adr_records
                        (adr_ref, title, tier_id, class_id, status,
                         submitted_at, resolved_at, sla_met, repo_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (adr_ref) DO UPDATE SET
                        title        = EXCLUDED.title,
                        tier_id      = EXCLUDED.tier_id,
                        class_id     = EXCLUDED.class_id,
                        status       = EXCLUDED.status,
                        submitted_at = EXCLUDED.submitted_at,
                        resolved_at  = EXCLUDED.resolved_at,
                        sla_met      = EXCLUDED.sla_met,
                        repo_path    = EXCLUDED.repo_path
                    """,
                    (
                        rec["adr_ref"], rec["title"], rec["tier"], class_id,
                        rec["status"], rec["submitted_at"], rec["resolved_at"],
                        rec["sla_met"], rec["repo_path"],
                    ),
                )
        log.info("Upserted %d ADR records to PostgreSQL", len(adrs))
    finally:
        conn.close()


def _upsert_ccrs_to_pg(ccrs: list[dict]) -> None:
    if not ccrs:
        return
    conn = psycopg2.connect(PG_DSN)
    try:
        with conn, conn.cursor() as cur:
            for rec in ccrs:
                cur.execute(
                    """
                    INSERT INTO ccr_records
                        (ccr_ref, title, status, escalated_to_adr,
                         created_at, resolved_at, repo_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ccr_ref) DO UPDATE SET
                        title            = EXCLUDED.title,
                        status           = EXCLUDED.status,
                        escalated_to_adr = EXCLUDED.escalated_to_adr,
                        resolved_at      = EXCLUDED.resolved_at,
                        repo_path        = EXCLUDED.repo_path
                    """,
                    (
                        rec["ccr_ref"], rec["title"], rec["status"],
                        rec.get("escalated_to_adr"),
                        rec["created_at"], rec["resolved_at"], rec["repo_path"],
                    ),
                )
        log.info("Upserted %d CCR records to PostgreSQL", len(ccrs))
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# InfluxDB write
# ---------------------------------------------------------------------------

def write_points(points: list[Point]) -> None:
    if not points:
        return
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        client.write_api(write_options=SYNCHRONOUS).write(bucket=INFLUXDB_BUCKET, record=points)
    log.info("Wrote %d ADR/CCR points to InfluxDB", len(points))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(lookback_days: int = LOOKBACK_DAYS) -> None:
    since = datetime.now(timezone.utc) - timedelta(days=lookback_days)

    adrs = _load_adr_files(since)
    ccrs = _load_ccr_files(since)

    influx_points: list[Point] = []
    influx_points.extend(_build_adr_points(adrs))
    influx_points.extend(_build_ccr_points(ccrs, total_ccrs=len(ccrs)))

    write_points(influx_points)
    _upsert_adrs_to_pg(adrs)
    _upsert_ccrs_to_pg(ccrs)

    log.info(
        "ADR/CCR ingestion complete. adrs=%d ccrs=%d influx_points=%d",
        len(adrs), len(ccrs), len(influx_points),
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest ADR/CCR metrics")
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args()
    run(lookback_days=args.lookback_days)
