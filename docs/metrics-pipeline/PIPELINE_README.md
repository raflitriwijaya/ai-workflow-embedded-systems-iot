# Engineering Metrics Pipeline

> Status: Production-ready implementation  
> Owner: [[DATA_ENGINEER_SKILL|Data Engineer]] + [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]]  
> Tags: #engineering-metrics-pipeline #build #process-health

---

## Overview

The Engineering Metrics Pipeline ingests process data from Git, Jira, CI/CD, and the ADR/CCR repositories, validates quality, computes derived KPIs, and serves them to the **Engineering Process Health Dashboard** in Grafana. It powers the [[PROCESS_ARCHITECT_SKILL|Process Architect]]'s EP-4 homeostasis loop and the Engineering Process Review cadence.

```
Git API ──────────────────────────────────────────┐
Jira REST API ────────────────────────────────────┤
CI/CD API / JSON export ──────────────────────────┼──► InfluxDB (raw) ──► transform_metrics.py ──► InfluxDB (agg)
ADR/CCR Git repo (Markdown + YAML frontmatter) ───┤                                                      │
                                                   └──► PostgreSQL (dimensional) ─────────────────────────┘
                                                                                                          │
                                                                                               Grafana Dashboard
```

### Data sources

| Source | Script | Metrics |
|---|---|---|
| Git | `ingest_git.py` | Commit frequency, PR cycle time, review turnaround, PR size |
| Jira | `ingest_jira.py` | Sprint velocity, cycle time, blocked time, defect discovery stage |
| CI/CD | `ingest_cicd.py` | Build success rate, test pass rate, deploy frequency, pipeline duration, smoke test pass rate |
| ADR/CCR | `ingest_adr.py` | ADR turnaround per tier, CCR escalation rate, ADR volume by class |

### Storage

| Store | Purpose | Retention |
|---|---|---|
| InfluxDB bucket `engineering_metrics_raw` | Raw time-series points | 12 months |
| InfluxDB bucket `engineering_metrics_agg` | Derived KPI time-series | 36 months |
| PostgreSQL | Dimensional records (ADR, CCR, defects, initiatives) | 12 months raw / 36 months snapshots |

---

## Prerequisites

| Tool | Minimum version |
|---|---|
| Python | 3.11 |
| Apache Airflow | 2.7 |
| InfluxDB | 2.7 (Flux query language) |
| PostgreSQL | 15 |
| Grafana | 9.0 |

### Python dependencies

```
influxdb-client>=1.38
psycopg2-binary>=2.9
requests>=2.31
pyyaml>=6.0
great-expectations>=0.18
apache-airflow>=2.7
```

Install:
```bash
pip install influxdb-client psycopg2-binary requests pyyaml great-expectations "apache-airflow[postgres]"
```

---

## Environment variables

All secrets must be injected via your secrets manager (HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets). Never hardcode credentials.

### Required — all scripts

| Variable | Description |
|---|---|
| `INFLUXDB_URL` | InfluxDB base URL, e.g. `http://influxdb:8086` |
| `INFLUXDB_TOKEN` | InfluxDB operator token |
| `INFLUXDB_ORG` | InfluxDB organisation name |
| `INFLUXDB_BUCKET_RAW` | Raw metrics bucket name (12-month retention) |
| `INFLUXDB_BUCKET_AGG` | Aggregated metrics bucket name (36-month retention) |
| `PG_DSN` | PostgreSQL DSN, e.g. `postgresql://metrics_writer:secret@pg:5432/eng_metrics` |

### Git ingestion

| Variable | Description |
|---|---|
| `GIT_API_BASE_URL` | GitHub API base URL |
| `GIT_API_TOKEN` | GitHub personal access token or App token (read:repo scope) |
| `GIT_ORG` | GitHub organisation |
| `GIT_REPOS` | Comma-separated repo slugs, e.g. `api-gateway,iot-firmware,data-platform` |
| `GIT_LOOKBACK_DAYS` | Days to look back per run (default: `1`) |

### Jira ingestion

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | Jira Cloud base URL, e.g. `https://yourorg.atlassian.net` |
| `JIRA_API_EMAIL` | Service account email for Basic Auth |
| `JIRA_API_TOKEN` | Jira API token |
| `JIRA_PROJECTS` | Comma-separated project keys, e.g. `PLAT,IOT,SEC` |

### CI/CD ingestion

| Variable | Description |
|---|---|
| `CICD_SOURCE` | `github_actions` or `json_export` |
| `CICD_WORKFLOW_NAMES` | Comma-separated workflow file names (GitHub Actions mode) |
| `CICD_JSON_EXPORT_PATH` | Absolute path to JSON export file (json_export mode) |

### ADR/CCR ingestion

| Variable | Description |
|---|---|
| `ADR_REPO_PATH` | Absolute path to the locally cloned ADR/CCR repository |
| `ADR_GLOB_PATTERN` | Glob to find ADR Markdown files (default: `**/adr-*.md`) |
| `CCR_GLOB_PATTERN` | Glob to find CCR Markdown files (default: `**/ccr-*.md`) |

### Alerting

| Variable | Description |
|---|---|
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL for failure alerts (optional) |
| `METRICS_PIPELINE_ALERT_EMAIL` | Email for Airflow failure notifications |

---

## Database setup

### 1. PostgreSQL

```bash
psql -h $PG_HOST -U postgres -d postgres -c "CREATE DATABASE eng_metrics;"
psql -h $PG_HOST -U postgres -d eng_metrics -f schema.sql
```

The schema file creates all tables, views, indexes, and roles. Change the placeholder passwords in the GRANTS section before running.

### 2. InfluxDB buckets

```bash
influx bucket create \
  --name engineering_metrics_raw \
  --retention 8760h \    # 365 days
  --org "$INFLUXDB_ORG"

influx bucket create \
  --name engineering_metrics_agg \
  --retention 26280h \   # 3 years (1095 days)
  --org "$INFLUXDB_ORG"
```

---

## Airflow setup

### 1. Copy the DAG

```bash
cp airflow_dag.py $AIRFLOW_HOME/dags/engineering_metrics_pipeline.py
```

### 2. Add Airflow Variables (or inject via Vault)

```bash
airflow variables set METRICS_PIPELINE_ALERT_EMAIL "platform-eng@example.com"
airflow variables set SLACK_WEBHOOK_URL "https://hooks.slack.com/services/..."
airflow variables set GIT_LOOKBACK_DAYS "1"
airflow variables set JIRA_LOOKBACK_DAYS "7"
airflow variables set CICD_LOOKBACK_DAYS "1"
airflow variables set ADR_LOOKBACK_DAYS "7"
airflow variables set TRANSFORM_LOOKBACK_DAYS "30"
```

### 3. Create ingestion pool

```bash
airflow pools set ingestion_pool 4 "Limits concurrent external API calls"
```

### 4. Set environment variables in Airflow

Add all required env vars (from the table above) to your Airflow workers, either via:
- `airflow.cfg` `[core] default_env` (non-secret values)
- Vault integration plugin → injected at task execution time
- Kubernetes pod environment (for Kubernetes executor)

### 5. Activate the DAG

```bash
airflow dags unpause engineering_metrics_pipeline
```

The pipeline will first run the next time 06:00 UTC arrives.

---

## Grafana dashboard setup

### Import

1. Open Grafana → **Dashboards → Import**
2. Upload `grafana_dashboard.json`
3. Select your InfluxDB data source when prompted
4. Set dashboard variables:
   - `influxdb_bucket_raw` → `engineering_metrics_raw`
   - `influxdb_bucket_agg` → `engineering_metrics_agg`
5. Click **Import**

### Dashboard panels summary

| # | Panel | Type | Target |
|---|---|---|---|
| 1 | ADR Turnaround vs SLA Target per Tier | Gauge | Green ≤1×, Yellow ≤1.5×, Red >1.5× |
| 2 | ADR SLA Compliance Overall % | Stat | ≥85% |
| 3 | Contract Clarity Index (CCR Escalation Rate) | Gauge | ≤20% |
| 4 | Contract Clarity Index Trend | Time series | Downward is better |
| 5 | Defect Discovery Stage Distribution | Bar chart | ≥60% Development, ≤10% Production |
| 6 | Shift-Left Ratio and Production Defect Rate | Stat | Dev ≥60%, Prod ≤10% |
| 7 | Security Finding Stage Distribution | Bar chart | ≥70% Design+Impl, ≤5% Post-Release |
| 8 | Security Shift-Left and Post-Release Rate | Stat | Shift-left ≥70%, Post-Release ≤5% |
| 9 | Initiative Completion Rate | Gauge | ≥80% |
| 10 | Initiative Completion Rate Trend | Time series | |
| 11 | Cross-Role KPI Trends | Time series | Selectable by `metric_category` |

---

## ADR/CCR frontmatter convention

The `ingest_adr.py` script expects YAML frontmatter in every ADR and CCR Markdown file.

**ADR template:**
```yaml
---
adr_ref: ADR-0042
title: "Adopt InfluxDB for time-series storage"
tier: 2
decision_class: "Data Architecture"
status: resolved        # proposed | reviewing | resolved | superseded
submitted_at: "2024-01-10T09:00:00Z"
resolved_at: "2024-01-11T14:30:00Z"
---
```

**CCR template:**
```yaml
---
ccr_ref: CCR-0017
title: "Clarify data retention policy for IoT sensor readings"
status: escalated       # open | resolved | escalated
escalated_to_adr: ADR-0042
created_at: "2024-01-09T08:00:00Z"
resolved_at: "2024-01-11T14:30:00Z"
---
```

---

## Running scripts locally (for testing)

Each script has a `__main__` block and can be run standalone:

```bash
# Test Git ingestion for last 2 days
python ingest_git.py --lookback-days 2

# Test Jira ingestion
python ingest_jira.py --lookback-days 7

# Test CI/CD ingestion
python ingest_cicd.py --lookback-days 1

# Test ADR/CCR ingestion
python ingest_adr.py --lookback-days 7

# Run transformation
python transform_metrics.py --lookback-days 30

# Run validation (exits non-zero on failure)
python validate_data.py
```

Set all required environment variables before running, e.g.:
```bash
export INFLUXDB_URL=http://localhost:8086
export INFLUXDB_TOKEN=my-dev-token
export INFLUXDB_ORG=my-org
export INFLUXDB_BUCKET_RAW=engineering_metrics_raw
export INFLUXDB_BUCKET_AGG=engineering_metrics_agg
export PG_DSN="postgresql://metrics_writer:secret@localhost:5432/eng_metrics"
export GIT_API_BASE_URL=https://api.github.com
export GIT_API_TOKEN=ghp_...
export GIT_ORG=my-org
export GIT_REPOS=api-gateway,iot-firmware
export JIRA_BASE_URL=https://myorg.atlassian.net
export JIRA_API_EMAIL=svc-metrics@example.com
export JIRA_API_TOKEN=ATATT...
export JIRA_PROJECTS=PLAT,IOT
export CICD_SOURCE=github_actions
export CICD_WORKFLOW_NAMES=ci.yml,deploy.yml
export ADR_REPO_PATH=/path/to/adr-repo
```

---

## Monitoring the pipeline

- **Airflow UI**: `http://airflow:8080/dags/engineering_metrics_pipeline`
- **Failure alerts**: Slack webhook + email (configured in Airflow Variables)
- **Grafana dashboard**: refresh every 5 minutes; time range defaults to last 30 days
- **Validation failures**: `validate_data.py` exits with code 1 — Airflow will retry 3× then alert

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ingest_git` rate-limited | GitHub API rate limit | Increase `GIT_RATE_LIMIT_SLEEP` or use a GitHub App token (higher limits) |
| ADR records missing tier | Missing `tier:` in frontmatter | Add tier field to all ADR Markdown files |
| Grafana panels empty | InfluxDB bucket name mismatch | Check dashboard variables `influxdb_bucket_raw` / `influxdb_bucket_agg` |
| Validation FAIL: unknown_stage_not_majority | >50% defects have no discovery stage label | Add `dev-bug`, `qa-bug`, or `prod-bug` labels in Jira; update `DEFECT_STAGE_MAP` if using different label names |
| Airflow tasks stuck in `queued` | Ingestion pool exhausted | Increase pool size: `airflow pools set ingestion_pool 8 "..."` |

---

## Related specifications

- [[DATA_ENGINEER_SKILL]] §5: Engineering Metrics Pipeline deliverable row
- [[DEVOPS_PLATFORM_ENGINEER_SKILL]] §3.3: Process data source integration
- [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] §5: Engineering Process Health Dashboard
- [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]]: Research metrics integration
