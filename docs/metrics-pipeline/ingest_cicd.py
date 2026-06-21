"""
ingest_cicd.py — CI/CD metrics ingestion for the Engineering Metrics Pipeline.

Supports two source modes (set CICD_SOURCE env var):
  - "github_actions"  : GitHub Actions workflow runs API
  - "json_export"     : structured JSON log file dropped by your CI system
                        (path set in CICD_JSON_EXPORT_PATH)

Extracted metrics: build success rate, test pass rate, deployment frequency,
pipeline duration, integration smoke test pass rate.

Environment variables (required):
    CICD_SOURCE             "github_actions" | "json_export"
    INFLUXDB_URL
    INFLUXDB_TOKEN
    INFLUXDB_ORG
    INFLUXDB_BUCKET_RAW

For github_actions mode:
    GIT_API_BASE_URL
    GIT_API_TOKEN
    GIT_ORG
    GIT_REPOS               Comma-separated repo slugs
    CICD_WORKFLOW_NAMES     Comma-separated workflow file names (e.g. ci.yml,deploy.yml)

For json_export mode:
    CICD_JSON_EXPORT_PATH   Absolute path to the exported JSON file

Optional:
    CICD_LOOKBACK_DAYS      Default: 1
    LOG_LEVEL

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CICD_SOURCE: str      = os.environ["CICD_SOURCE"]
INFLUXDB_URL: str     = os.environ["INFLUXDB_URL"]
INFLUXDB_TOKEN: str   = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_ORG: str     = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET: str  = os.environ["INFLUXDB_BUCKET_RAW"]
LOOKBACK_DAYS: int    = int(os.getenv("CICD_LOOKBACK_DAYS", "1"))

# GitHub-specific
GIT_API_BASE_URL: str = os.getenv("GIT_API_BASE_URL", "https://api.github.com").rstrip("/")
GIT_API_TOKEN: str    = os.getenv("GIT_API_TOKEN", "")
GIT_ORG: str          = os.getenv("GIT_ORG", "")
GIT_REPOS: list[str]  = [r.strip() for r in os.getenv("GIT_REPOS", "").split(",") if r.strip()]
WORKFLOW_NAMES: list[str] = [
    w.strip() for w in os.getenv("CICD_WORKFLOW_NAMES", "ci.yml").split(",") if w.strip()
]

# JSON export mode
JSON_EXPORT_PATH: str = os.getenv("CICD_JSON_EXPORT_PATH", "")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("ingest_cicd")

# ---------------------------------------------------------------------------
# HTTP helpers (GitHub Actions)
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {GIT_API_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
})


def _get(url: str, params: dict | None = None, max_retries: int = 5) -> requests.Response:
    for attempt in range(1, max_retries + 1):
        try:
            resp = SESSION.get(url, params=params, timeout=30)
            if resp.status_code in (429, 403):
                sleep = int(resp.headers.get("Retry-After", 60))
                log.warning("Rate limited; sleeping %ds", sleep)
                time.sleep(sleep)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GET failed: {url}")


# ---------------------------------------------------------------------------
# GitHub Actions ingestion
# ---------------------------------------------------------------------------

def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def ingest_github_actions(repo: str, since: datetime) -> list[Point]:
    """Pull workflow runs for one repo and return InfluxDB Points."""
    points: list[Point] = []

    for workflow_name in WORKFLOW_NAMES:
        url = f"{GIT_API_BASE_URL}/repos/{GIT_ORG}/{repo}/actions/workflows/{workflow_name}/runs"
        try:
            resp = _get(url, params={
                "created": f">={since.strftime('%Y-%m-%d')}",
                "per_page": 100,
            })
        except requests.HTTPError as exc:
            log.warning("Cannot fetch workflow %s for repo %s: %s", workflow_name, repo, exc)
            continue

        runs = resp.json().get("workflow_runs", [])
        log.info("repo=%s workflow=%s runs=%d", repo, workflow_name, len(runs))

        # Derive is_deploy from workflow name
        is_deploy = "deploy" in workflow_name.lower() or "release" in workflow_name.lower()
        is_smoke  = "smoke" in workflow_name.lower() or "integration" in workflow_name.lower()

        for run in runs:
            created_at = _parse_iso(run.get("created_at"))
            updated_at = _parse_iso(run.get("updated_at"))
            conclusion = run.get("conclusion") or "in_progress"  # null if still running

            # Duration
            duration_s: float | None = None
            if created_at and updated_at and conclusion not in ("in_progress", None):
                duration_s = (updated_at - created_at).total_seconds()

            success = 1 if conclusion == "success" else 0
            ts = updated_at or created_at or datetime.now(timezone.utc)

            pt = (
                Point("cicd_metrics")
                .tag("repo", repo)
                .tag("workflow", workflow_name)
                .tag("conclusion", conclusion)
                .tag("is_deploy", str(is_deploy).lower())
                .tag("is_smoke_test", str(is_smoke).lower())
                .field("run_success", success)
            )
            if duration_s is not None:
                pt = pt.field("pipeline_duration_seconds", round(duration_s, 1))

            pt = pt.time(ts, WritePrecision.SECONDS)
            points.append(pt)

    return points


# ---------------------------------------------------------------------------
# JSON export ingestion (generic CI/CD log)
# ---------------------------------------------------------------------------
# Expected JSON format (array of objects):
# [
#   {
#     "pipeline": "build-main",
#     "environment": "staging",
#     "repo": "my-service",
#     "status": "success",          # "success" | "failure" | "error"
#     "test_pass_rate": 0.97,       # float 0-1
#     "smoke_pass_rate": 1.0,       # float 0-1, optional
#     "duration_seconds": 245,
#     "is_deploy": true,
#     "timestamp": "2024-01-15T12:34:56Z"
#   }
# ]

def ingest_json_export(since: datetime) -> list[Point]:
    path = Path(JSON_EXPORT_PATH)
    if not path.exists():
        log.error("JSON export file not found: %s", path)
        return []

    with path.open() as fh:
        data: list[dict] = json.load(fh)

    points: list[Point] = []
    for record in data:
        ts = _parse_iso(record.get("timestamp"))
        if not ts or ts < since:
            continue

        status    = record.get("status", "unknown")
        success   = 1 if status == "success" else 0
        pt = (
            Point("cicd_metrics")
            .tag("repo",        record.get("repo", "unknown"))
            .tag("pipeline",    record.get("pipeline", "unknown"))
            .tag("environment", record.get("environment", "unknown"))
            .tag("conclusion",  status)
            .tag("is_deploy",   str(record.get("is_deploy", False)).lower())
            .field("run_success", success)
        )
        if "test_pass_rate" in record:
            pt = pt.field("test_pass_rate", float(record["test_pass_rate"]))
        if "smoke_pass_rate" in record:
            pt = pt.field("smoke_test_pass_rate", float(record["smoke_pass_rate"]))
        if "duration_seconds" in record:
            pt = pt.field("pipeline_duration_seconds", float(record["duration_seconds"]))

        pt = pt.time(ts, WritePrecision.SECONDS)
        points.append(pt)

    log.info("JSON export: loaded %d CI/CD records since %s", len(points), since.date())
    return points


# ---------------------------------------------------------------------------
# InfluxDB write
# ---------------------------------------------------------------------------

def write_points(points: list[Point]) -> None:
    if not points:
        log.info("No CI/CD points to write.")
        return
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        client.write_api(write_options=SYNCHRONOUS).write(bucket=INFLUXDB_BUCKET, record=points)
    log.info("Wrote %d CI/CD points to InfluxDB", len(points))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(lookback_days: int = LOOKBACK_DAYS) -> None:
    since = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    all_points: list[Point] = []

    if CICD_SOURCE == "github_actions":
        for repo in GIT_REPOS:
            try:
                all_points.extend(ingest_github_actions(repo, since))
            except Exception as exc:
                log.error("GitHub Actions ingestion failed for %s: %s", repo, exc, exc_info=True)
    elif CICD_SOURCE == "json_export":
        try:
            all_points.extend(ingest_json_export(since))
        except Exception as exc:
            log.error("JSON export ingestion failed: %s", exc, exc_info=True)
    else:
        raise ValueError(f"Unknown CICD_SOURCE: {CICD_SOURCE!r}. Use 'github_actions' or 'json_export'.")

    write_points(all_points)
    log.info("CI/CD ingestion complete. total_points=%d", len(all_points))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest CI/CD metrics")
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args()
    run(lookback_days=args.lookback_days)
