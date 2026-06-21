"""
ingest_git.py — Git metrics ingestion for the Engineering Metrics Pipeline.

Pulls commit frequency, PR cycle time, review turnaround, and PR size from a
Git hosting API (GitHub-compatible; swap base URL + auth header for GitLab/Bitbucket).

Environment variables (required):
    GIT_API_BASE_URL        e.g. https://api.github.com
    GIT_API_TOKEN           Personal access token or app token
    GIT_ORG                 Organisation / namespace
    GIT_REPOS               Comma-separated list of repo slugs to ingest
    INFLUXDB_URL            e.g. http://influxdb:8086
    INFLUXDB_TOKEN          InfluxDB auth token
    INFLUXDB_ORG            InfluxDB organisation name
    INFLUXDB_BUCKET_RAW     Bucket for raw time-series (retention 12 months)

Optional:
    GIT_LOOKBACK_DAYS       Days to look back on each run (default: 1)
    GIT_RATE_LIMIT_SLEEP    Seconds to sleep on 429 (default: 60)
    LOG_LEVEL               DEBUG | INFO | WARNING (default: INFO)

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GIT_API_BASE_URL: str  = os.environ["GIT_API_BASE_URL"].rstrip("/")
GIT_API_TOKEN: str     = os.environ["GIT_API_TOKEN"]
GIT_ORG: str           = os.environ["GIT_ORG"]
GIT_REPOS: list[str]   = [r.strip() for r in os.environ["GIT_REPOS"].split(",") if r.strip()]
INFLUXDB_URL: str      = os.environ["INFLUXDB_URL"]
INFLUXDB_TOKEN: str    = os.environ["INFLUXDB_TOKEN"]
INFLUXDB_ORG: str      = os.environ["INFLUXDB_ORG"]
INFLUXDB_BUCKET: str   = os.environ["INFLUXDB_BUCKET_RAW"]

LOOKBACK_DAYS: int     = int(os.getenv("GIT_LOOKBACK_DAYS", "1"))
RATE_LIMIT_SLEEP: int  = int(os.getenv("GIT_RATE_LIMIT_SLEEP", "60"))
LOG_LEVEL: str         = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("ingest_git")

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {GIT_API_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
})


def _get(url: str, params: dict | None = None, max_retries: int = 5) -> Any:
    """GET with retry, rate-limit back-off, and pagination aggregation."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = SESSION.get(url, params=params, timeout=30)
            if resp.status_code == 429 or resp.status_code == 403:
                retry_after = int(resp.headers.get("Retry-After", RATE_LIMIT_SLEEP))
                log.warning("Rate limited by %s; sleeping %ds (attempt %d)", url, retry_after, attempt)
                time.sleep(retry_after)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == max_retries:
                raise
            sleep = 2 ** attempt
            log.warning("Request error %s; retrying in %ds (%d/%d)", exc, sleep, attempt, max_retries)
            time.sleep(sleep)
    raise RuntimeError(f"Failed to GET {url} after {max_retries} attempts")


def _paginate(url: str, params: dict | None = None) -> list[dict]:
    """Follow GitHub link-based pagination, return all items."""
    items: list[dict] = []
    params = (params or {}).copy()
    params.setdefault("per_page", 100)
    while url:
        resp = _get(url, params=params)
        items.extend(resp.json())
        url = resp.links.get("next", {}).get("url", "")
        params = {}   # pagination URL already contains all params
    return items


# ---------------------------------------------------------------------------
# Metric extraction
# ---------------------------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def ingest_commits(repo: str, since: datetime) -> list[Point]:
    """Return InfluxDB Points for commit frequency."""
    url = f"{GIT_API_BASE_URL}/repos/{GIT_ORG}/{repo}/commits"
    commits = _paginate(url, params={"since": since.isoformat(), "per_page": 100})
    log.info("repo=%s commits=%d since=%s", repo, len(commits), since.date())

    return [
        Point("git_metrics")
        .tag("repo", repo)
        .tag("metric_type", "commit")
        .field("commit_count", len(commits))
        .time(_utc_now(), WritePrecision.SECONDS)
    ]


def ingest_pull_requests(repo: str, since: datetime) -> list[Point]:
    """Return InfluxDB Points for PR cycle time, review turnaround, and PR size."""
    url = f"{GIT_API_BASE_URL}/repos/{GIT_ORG}/{repo}/pulls"
    closed_prs = _paginate(url, params={"state": "closed", "sort": "updated", "direction": "desc"})
    open_prs   = _paginate(url, params={"state": "open",   "sort": "updated", "direction": "desc"})

    points: list[Point] = []
    cutoff = since

    def _process_pr(pr: dict) -> None:
        created  = _parse_iso(pr.get("created_at"))
        merged   = _parse_iso(pr.get("merged_at"))
        updated  = _parse_iso(pr.get("updated_at"))

        if updated and updated < cutoff:
            return  # outside our window

        # Cycle time: open → merge (hours)
        cycle_time_h: float | None = None
        if created and merged:
            cycle_time_h = (merged - created).total_seconds() / 3600.0

        # PR size (additions + deletions)
        additions  = pr.get("additions", 0) or 0
        deletions  = pr.get("deletions", 0) or 0
        pr_size    = additions + deletions

        # Review turnaround: fetch reviews for merged PRs only
        review_turnaround_h: float | None = None
        pr_number = pr["number"]
        try:
            reviews_url = f"{GIT_API_BASE_URL}/repos/{GIT_ORG}/{repo}/pulls/{pr_number}/reviews"
            reviews = _paginate(reviews_url)
            first_review = next(
                (r for r in reviews if r.get("state") in ("APPROVED", "CHANGES_REQUESTED", "COMMENTED")),
                None,
            )
            if first_review and created:
                first_review_ts = _parse_iso(first_review.get("submitted_at"))
                if first_review_ts:
                    review_turnaround_h = (first_review_ts - created).total_seconds() / 3600.0
        except Exception as exc:
            log.debug("Could not fetch reviews for PR#%d: %s", pr_number, exc)

        pt = (
            Point("git_metrics")
            .tag("repo", repo)
            .tag("metric_type", "pull_request")
            .tag("pr_state", "merged" if merged else "open")
            .field("pr_size_lines", pr_size)
        )
        if cycle_time_h is not None:
            pt = pt.field("pr_cycle_time_hours", round(cycle_time_h, 2))
        if review_turnaround_h is not None:
            pt = pt.field("review_turnaround_hours", round(review_turnaround_h, 2))

        timestamp = merged or updated or _utc_now()
        pt = pt.time(timestamp, WritePrecision.SECONDS)
        points.append(pt)

    for pr in closed_prs + open_prs:
        try:
            _process_pr(pr)
        except Exception as exc:
            log.warning("Skipping PR in %s: %s", repo, exc)

    log.info("repo=%s pr_points=%d", repo, len(points))
    return points


# ---------------------------------------------------------------------------
# InfluxDB write
# ---------------------------------------------------------------------------

def write_points(points: list[Point]) -> None:
    if not points:
        log.info("No points to write.")
        return
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=INFLUXDB_BUCKET, record=points)
    log.info("Wrote %d points to InfluxDB bucket=%s", len(points), INFLUXDB_BUCKET)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(lookback_days: int = LOOKBACK_DAYS) -> None:
    since = _utc_now() - timedelta(days=lookback_days)
    all_points: list[Point] = []

    for repo in GIT_REPOS:
        log.info("Ingesting repo: %s", repo)
        try:
            all_points.extend(ingest_commits(repo, since))
            all_points.extend(ingest_pull_requests(repo, since))
        except Exception as exc:
            log.error("Failed ingesting repo %s: %s", repo, exc, exc_info=True)

    write_points(all_points)
    log.info("Git ingestion complete. total_points=%d", len(all_points))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest Git metrics into InfluxDB")
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args()
    run(lookback_days=args.lookback_days)
