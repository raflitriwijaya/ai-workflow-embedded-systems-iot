"""
airflow_dag.py — Airflow DAG: Engineering Metrics Pipeline.

Schedule: daily at 06:00 UTC (after overnight CI runs complete).
Retry policy: 3 retries, 5-minute exponential back-off.
SLA: pipeline must complete within 2 hours of scheduled start.
Failure alert: email + Slack callback via on_failure_callback.

Task dependency graph:
    ingest_git ──┐
    ingest_jira ─┤
    ingest_cicd ─┼──► validate_data ──► transform_metrics ──► notify_success
    ingest_adr ──┘

Tags: #engineering-metrics-pipeline #build #process-health
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.email import send_email
from airflow.utils.trigger_rule import TriggerRule

# ---------------------------------------------------------------------------
# Default args
# ---------------------------------------------------------------------------

PIPELINE_EMAIL: str = Variable.get("METRICS_PIPELINE_ALERT_EMAIL", default_var="platform-eng@example.com")
SLACK_WEBHOOK: str  = Variable.get("SLACK_WEBHOOK_URL", default_var="")

DEFAULT_ARGS: dict = {
    "owner": "data-platform",
    "depends_on_past": False,
    "email": [PIPELINE_EMAIL],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "execution_timeout": timedelta(hours=1),
}

# ---------------------------------------------------------------------------
# Failure / success callbacks
# ---------------------------------------------------------------------------

def _on_failure(context: dict) -> None:
    """Post to Slack and send email on task failure."""
    task_instance = context["task_instance"]
    dag_id  = context["dag"].dag_id
    task_id = task_instance.task_id
    run_id  = context["run_id"]
    log_url = task_instance.log_url

    msg = (
        f":x: *{dag_id}* — task `{task_id}` FAILED\n"
        f"Run: `{run_id}`\n"
        f"Logs: {log_url}"
    )
    if SLACK_WEBHOOK:
        import requests
        try:
            requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)
        except Exception:
            pass  # non-fatal


def _on_success(context: dict) -> None:
    """Post summary to Slack on DAG completion."""
    if not SLACK_WEBHOOK:
        return
    dag_id = context["dag"].dag_id
    run_id = context["run_id"]
    import requests
    try:
        requests.post(
            SLACK_WEBHOOK,
            json={"text": f":white_check_mark: *{dag_id}* completed successfully. Run: `{run_id}`"},
            timeout=10,
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Python callables (thin wrappers; real logic lives in each ingest_*.py)
# ---------------------------------------------------------------------------

def _run_ingest_git(**kwargs) -> None:
    from ingest_git import run
    lookback = int(Variable.get("GIT_LOOKBACK_DAYS", default_var="1"))
    run(lookback_days=lookback)


def _run_ingest_jira(**kwargs) -> None:
    from ingest_jira import run
    lookback = int(Variable.get("JIRA_LOOKBACK_DAYS", default_var="7"))
    run(lookback_days=lookback)


def _run_ingest_cicd(**kwargs) -> None:
    from ingest_cicd import run
    lookback = int(Variable.get("CICD_LOOKBACK_DAYS", default_var="1"))
    run(lookback_days=lookback)


def _run_ingest_adr(**kwargs) -> None:
    from ingest_adr import run
    lookback = int(Variable.get("ADR_LOOKBACK_DAYS", default_var="7"))
    run(lookback_days=lookback)


def _run_validate(**kwargs) -> None:
    from validate_data import run
    ok = run()
    if not ok:
        raise ValueError("Data validation failed — see validate_data logs for details.")


def _run_transform(**kwargs) -> None:
    from transform_metrics import run
    lookback = int(Variable.get("TRANSFORM_LOOKBACK_DAYS", default_var="30"))
    run(lookback_days=lookback)


def _run_retention_cleanup(**kwargs) -> None:
    """Delete raw mirror rows older than 12 months (PostgreSQL housekeeping)."""
    import psycopg2
    pg_dsn = os.environ["PG_DSN"]
    conn = psycopg2.connect(pg_dsn)
    tables = ["adr_records", "ccr_records", "defect_records", "security_findings"]
    try:
        with conn, conn.cursor() as cur:
            for table in tables:
                cur.execute(
                    f"DELETE FROM {table} WHERE ingested_at < NOW() - INTERVAL '12 months'"
                )
                import logging
                logging.getLogger("airflow.task").info(
                    "Cleaned %d rows from %s", cur.rowcount, table
                )
            cur.execute(
                "DELETE FROM daily_metric_snapshots WHERE snapshot_date < NOW() - INTERVAL '36 months'"
            )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# DAG definition
# ---------------------------------------------------------------------------

with DAG(
    dag_id="engineering_metrics_pipeline",
    default_args=DEFAULT_ARGS,
    description="Ingest, validate, and transform engineering process metrics daily",
    schedule_interval="0 6 * * *",   # 06:00 UTC every day
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["engineering-metrics", "process-health", "data-platform"],
    on_failure_callback=_on_failure,
    sla_miss_callback=None,   # configure via Airflow SLA settings
    doc_md="""
# Engineering Metrics Pipeline

Daily pipeline that ingests Git, Jira, CI/CD, and ADR/CCR data, validates quality,
computes derived process KPIs, and serves them to the Engineering Process Health Dashboard.

## Schedule
- Runs at 06:00 UTC daily
- SLA: 2 hours (alert if exceeded)
- Lookback windows: Git=1d, Jira=7d, CICD=1d, ADR=7d, Transform=30d

## Data sources
1. Git repository API (GitHub-compatible)
2. Jira REST API v3
3. CI/CD pipeline API or JSON export
4. ADR/CCR Git repository (Markdown + YAML frontmatter)

## See also
- [[DATA_ENGINEER_SKILL]] §5
- [[DEVOPS_PLATFORM_ENGINEER_SKILL]] §3.3
    """,
) as dag:

    # Ingestion tasks (parallel, no dependencies between them)
    t_ingest_git = PythonOperator(
        task_id="ingest_git",
        python_callable=_run_ingest_git,
        on_failure_callback=_on_failure,
        pool="ingestion_pool",     # limit concurrent API calls via Airflow pool
        doc="Ingest Git commit frequency, PR cycle time, review turnaround, PR size",
    )

    t_ingest_jira = PythonOperator(
        task_id="ingest_jira",
        python_callable=_run_ingest_jira,
        on_failure_callback=_on_failure,
        pool="ingestion_pool",
        doc="Ingest Jira sprint velocity, cycle time, blocked time, defect discovery stage",
    )

    t_ingest_cicd = PythonOperator(
        task_id="ingest_cicd",
        python_callable=_run_ingest_cicd,
        on_failure_callback=_on_failure,
        pool="ingestion_pool",
        doc="Ingest CI/CD build success rate, test pass rate, deploy frequency, pipeline duration",
    )

    t_ingest_adr = PythonOperator(
        task_id="ingest_adr",
        python_callable=_run_ingest_adr,
        on_failure_callback=_on_failure,
        pool="ingestion_pool",
        doc="Ingest ADR/CCR turnaround time, escalation rate, ADR volume by decision class",
    )

    # Validation (requires all ingestion to complete)
    t_validate = PythonOperator(
        task_id="validate_data",
        python_callable=_run_validate,
        on_failure_callback=_on_failure,
        doc="Run Great Expectations + SQL validation suites on ingested data",
    )

    # Transformation
    t_transform = PythonOperator(
        task_id="transform_metrics",
        python_callable=_run_transform,
        on_failure_callback=_on_failure,
        doc="Compute shift-left ratio, contract clarity index, SLA compliance, initiative rate",
    )

    # Retention cleanup (runs weekly via schedule within daily DAG logic)
    t_cleanup = PythonOperator(
        task_id="retention_cleanup",
        python_callable=_run_retention_cleanup,
        on_failure_callback=_on_failure,
        trigger_rule=TriggerRule.ALL_SUCCESS,
        doc="Delete raw rows older than 12 months; aggregated rows older than 36 months",
    )

    # Success notification
    t_notify = EmptyOperator(
        task_id="notify_success",
        on_success_callback=_on_success,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # -----------------------------------------------------------------------
    # Dependency graph
    # -----------------------------------------------------------------------
    [t_ingest_git, t_ingest_jira, t_ingest_cicd, t_ingest_adr] >> t_validate
    t_validate >> t_transform >> t_cleanup >> t_notify
