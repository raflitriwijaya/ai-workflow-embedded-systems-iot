"""
ingest_jira.py — Jira metrics ingestion for the Engineering Metrics Pipeline.

Extracts sprint velocity, defect discovery stage, cycle time, and blocked time
from Jira REST API v3.

Environment variables (required):
    JIRA_BASE_URL           e.g. https://yourorg.atlassian.net
    JIRA_API_EMAIL          Service-account email for Basic auth
    JIRA_API_TOKEN          Jira API token (Atlassian Account)
    JIRA_PROJECTS           Comma-separated Jira project keys, e.g. PLAT,IOT,SEC
    INFLUXDB_URL
    INFLUXDB_TOKEN
    INFLUXDB_ORG
    INFLUXDB_BUCKET_RAW
    PG_DSN                  PostgreSQL DSN, e.g. postgresql://user:pass@host/db

Optional:
    JIRA_LOOKBACK_DAYS      Default: 7 (sprints can span a week)
    JIRA_BLOCKED_LABEL      Jira label that marks blocked issues (default: "blocked")
    LOG_LEVEL

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import logging
import os
import time
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from typing import Any

import psycopg2
import psycopg2.extras
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JIRA_BASE_URL: str    = os.environ["JIRA_BASE_URL"].rstrip("/")
JIRA_EMAIL: str       = os.environ["JIRA_API_EMAIL"]
JIRA_TOKEN: str       = os.environ["JIRA_API_TOKEN"]
JIRA_PROJECTS: list[str] = [p.strip() for p in os.environ["JIRA_PROJECTS"].split(",") if p.strip()]
BLOCKED_LABEL: str    = os.getenv("JIRA_BLOCKED_LABEL", "blocked")
LOOKBACK_DAYS: int    = int(os.getenv("JIRA_LOOKBACK_DAYS", "7"))

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
log = logging.getLogger("ingest_jira")

_AUTH_HEADER = "Basic " + b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": _AUTH_HEADER,
    "Accept": "application/json",
    "Content-Type": "application/json",
})


def _get(url: str, params: dict | None = None, max_retries: int = 5) -> requests.Response:
    for attempt in range(1, max_retries + 1):
        try:
            resp = SESSION.get(url, params=params, timeout=30)
            if resp.status_code == 429:
                sleep = int(resp.headers.get("Retry-After", 60))
                log.warning("Jira rate limit; sleeping %ds", sleep)
                time.sleep(sleep)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed GET {url}")


def _jira_search(jql: str, fields: list[str], max_results: int = 500) -> list[dict]:
    """Paginate Jira issue search."""
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    issues: list[dict] = []
    start_at = 0
    while True:
        resp = _get(url, params={
            "jql": jql,
            "fields": ",".join(fields),
            "maxResults": min(max_results, 100),
            "startAt": start_at,
        })
        data = resp.json()
        batch = data.get("issues", [])
        issues.extend(batch)
        if len(issues) >= data.get("total", 0) or not batch:
            break
        start_at += len(batch)
    return issues


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ---------------------------------------------------------------------------
# Sprint velocity
# ---------------------------------------------------------------------------

def ingest_sprint_velocity(project_key: str) -> list[Point]:
    """Fetch completed sprints and compute velocity (story points done)."""
    # Find board IDs for this project
    board_url = f"{JIRA_BASE_URL}/rest/agile/1.0/board"
    resp = _get(board_url, params={"projectKeyOrId": project_key, "type": "scrum"})
    boards = resp.json().get("values", [])

    points: list[Point] = []
    for board in boards:
        board_id = board["id"]
        sprint_url = f"{JIRA_BASE_URL}/rest/agile/1.0/board/{board_id}/sprint"
        try:
            sprint_resp = _get(sprint_url, params={"state": "closed", "maxResults": 10})
        except requests.HTTPError as exc:
            log.warning("Cannot fetch sprints for board %d: %s", board_id, exc)
            continue

        sprints = sprint_resp.json().get("values", [])
        for sprint in sprints:
            sprint_id = sprint["id"]
            sprint_name = sprint.get("name", str(sprint_id))
            end_date = _parse_iso(sprint.get("completeDate") or sprint.get("endDate"))
            if not end_date:
                continue

            # Issues in sprint
            issue_url = f"{JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
            try:
                issue_resp = _get(issue_url, params={"maxResults": 500, "fields": "story_points,status,customfield_10016"})
                sprint_issues = issue_resp.json().get("issues", [])
            except requests.HTTPError as exc:
                log.warning("Cannot fetch issues for sprint %d: %s", sprint_id, exc)
                continue

            velocity = sum(
                float(i["fields"].get("customfield_10016") or i["fields"].get("story_points") or 0)
                for i in sprint_issues
                if i["fields"].get("status", {}).get("statusCategory", {}).get("key") == "done"
            )

            pt = (
                Point("jira_metrics")
                .tag("project_key", project_key)
                .tag("sprint_name", sprint_name)
                .tag("metric_type", "velocity")
                .field("velocity_points", round(velocity, 2))
                .time(end_date, WritePrecision.SECONDS)
            )
            points.append(pt)
            log.debug("sprint=%s velocity=%.1f", sprint_name, velocity)

    log.info("project=%s sprint velocity points=%d", project_key, len(points))
    return points


# ---------------------------------------------------------------------------
# Cycle time and blocked time
# ---------------------------------------------------------------------------

def ingest_cycle_time(project_key: str, since: datetime) -> list[Point]:
    """Cycle time = in-progress → done. Also measures blocked label time."""
    since_str = since.strftime("%Y-%m-%d")
    jql = (
        f'project = "{project_key}" AND status = Done '
        f'AND updated >= "{since_str}" ORDER BY updated DESC'
    )
    issues = _jira_search(jql, fields=["created", "resolutiondate", "status", "labels", "priority"])

    points: list[Point] = []
    for issue in issues:
        f = issue["fields"]
        created   = _parse_iso(f.get("created"))
        resolved  = _parse_iso(f.get("resolutiondate"))
        labels    = f.get("labels", [])
        is_blocked = BLOCKED_LABEL.lower() in [l.lower() for l in labels]

        if not (created and resolved):
            continue

        cycle_hours = (resolved - created).total_seconds() / 3600.0

        pt = (
            Point("jira_metrics")
            .tag("project_key", project_key)
            .tag("metric_type", "cycle_time")
            .tag("priority", f.get("priority", {}).get("name", "Unknown"))
            .field("cycle_time_hours", round(cycle_hours, 2))
            .field("is_blocked", int(is_blocked))
            .time(resolved, WritePrecision.SECONDS)
        )
        points.append(pt)

    log.info("project=%s cycle_time points=%d", project_key, len(points))
    return points


# ---------------------------------------------------------------------------
# Defect discovery stage
# ---------------------------------------------------------------------------

DEFECT_STAGE_MAP: dict[str, str] = {
    # Jira issue type or label → canonical stage name
    "bug-dev": "Development",
    "bug-qa":  "Execution",
    "bug-prod":"Production",
    # Fallback from environment labels if your project uses different conventions
}

def ingest_defects(project_key: str, since: datetime) -> tuple[list[Point], list[dict]]:
    """Return InfluxDB points + PostgreSQL rows for defect discovery stage."""
    since_str = since.strftime("%Y-%m-%d")
    jql = (
        f'project = "{project_key}" AND issuetype = Bug '
        f'AND created >= "{since_str}" ORDER BY created DESC'
    )
    issues = _jira_search(
        jql,
        fields=["summary", "created", "resolutiondate", "labels", "priority", "customfield_10016"],
    )

    influx_points: list[Point] = []
    pg_rows: list[dict] = []

    for issue in issues:
        f   = issue["fields"]
        key = issue["key"]
        labels = [l.lower() for l in (f.get("labels") or [])]
        created   = _parse_iso(f.get("created"))
        resolved  = _parse_iso(f.get("resolutiondate"))

        # Determine discovery stage from labels
        stage = "Unknown"
        if any(l in labels for l in ("prod-bug", "production", "bug-prod")):
            stage = "Production"
        elif any(l in labels for l in ("qa-bug", "test-bug", "bug-qa", "execution")):
            stage = "Execution"
        elif any(l in labels for l in ("dev-bug", "development", "bug-dev")):
            stage = "Development"

        if created:
            pt = (
                Point("jira_metrics")
                .tag("project_key", project_key)
                .tag("metric_type", "defect")
                .tag("discovery_stage", stage)
                .tag("priority", f.get("priority", {}).get("name", "Unknown"))
                .field("defect_count", 1)
                .time(created, WritePrecision.SECONDS)
            )
            influx_points.append(pt)

        pg_rows.append({
            "jira_key": key,
            "summary": f.get("summary", ""),
            "discovery_stage_name": stage,
            "severity": f.get("priority", {}).get("name"),
            "project_key": project_key,
            "created_at": created,
            "resolved_at": resolved,
        })

    log.info("project=%s defect points=%d", project_key, len(influx_points))
    return influx_points, pg_rows


# ---------------------------------------------------------------------------
# PostgreSQL write
# ---------------------------------------------------------------------------

def write_defects_to_pg(pg_rows: list[dict]) -> None:
    if not pg_rows:
        return
    conn = psycopg2.connect(PG_DSN)
    try:
        with conn, conn.cursor() as cur:
            for row in pg_rows:
                cur.execute(
                    """
                    SELECT stage_id FROM defect_stages WHERE stage_name = %s
                    """,
                    (row["discovery_stage_name"],),
                )
                result = cur.fetchone()
                stage_id = result[0] if result else None
                cur.execute(
                    """
                    INSERT INTO defect_records (jira_key, summary, discovery_stage,
                        severity, project_key, created_at, resolved_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (jira_key) DO UPDATE SET
                        discovery_stage = EXCLUDED.discovery_stage,
                        resolved_at     = EXCLUDED.resolved_at
                    """,
                    (row["jira_key"], row["summary"], stage_id,
                     row["severity"], row["project_key"],
                     row["created_at"], row["resolved_at"]),
                )
        log.info("Upserted %d defect rows to PostgreSQL", len(pg_rows))
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
    log.info("Wrote %d Jira points to InfluxDB", len(points))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(lookback_days: int = LOOKBACK_DAYS) -> None:
    since = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    all_points: list[Point] = []
    all_pg_defects: list[dict] = []

    for project in JIRA_PROJECTS:
        log.info("Ingesting Jira project: %s", project)
        try:
            all_points.extend(ingest_sprint_velocity(project))
            all_points.extend(ingest_cycle_time(project, since))
            influx_pts, pg_rows = ingest_defects(project, since)
            all_points.extend(influx_pts)
            all_pg_defects.extend(pg_rows)
        except Exception as exc:
            log.error("Failed ingesting project %s: %s", project, exc, exc_info=True)

    write_points(all_points)
    write_defects_to_pg(all_pg_defects)
    log.info("Jira ingestion complete. influx_points=%d pg_defects=%d",
             len(all_points), len(all_pg_defects))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest Jira metrics")
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args()
    run(lookback_days=args.lookback_days)
