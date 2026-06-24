"""Example Airflow DAG for the Statistical Engine (spec §9.1 "every hour").

Drop into your Airflow ``dags/`` folder. It runs the same ``harness-stats``
entry point the docker-compose ``stats`` service runs, on an hourly schedule,
and emits a Phase Transition Readiness Report for Wave 1.

The harness DB connection is taken from the standard PG*/DATABASE_URL env vars
configured on the Airflow worker (no secrets in this file).
"""
from __future__ import annotations

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="evaluation_harness_statistical_engine",
    schedule="@hourly",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["evaluation-harness", "phase-5"],
    default_args={"retries": 1, "retry_delay": pendulum.duration(minutes=5)},
) as dag:
    recompute_readiness = BashOperator(
        task_id="recompute_readiness",
        bash_command="harness-stats",
    )

    # Emit the Phase Transition Readiness Report for Wave 1 once per day at 06:00
    # would normally be a separate DAG; shown here as a chained example.
    wave1_ptrr = BashOperator(
        task_id="wave1_ptrr",
        bash_command="harness-stats --wave 1 --report-dir /opt/airflow/reports/phase-transition",
    )

    recompute_readiness >> wave1_ptrr
