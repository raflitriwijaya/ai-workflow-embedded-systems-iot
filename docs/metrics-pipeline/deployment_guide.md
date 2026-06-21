# Engineering Metrics Pipeline — Deployment Guide

> Audience: [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps Platform Engineer]]  
> Prerequisite: Read `PIPELINE_README.md` first for architecture context  
> Tags: #engineering-metrics-pipeline #build #process-health

---

## Deployment checklist

- [ ] Secrets provisioned in Vault / Secrets Manager
- [ ] PostgreSQL database and schema initialised
- [ ] InfluxDB buckets created with correct retention policies
- [ ] Python dependencies installed in Airflow worker image
- [ ] DAG file deployed to Airflow DAGs folder
- [ ] Airflow Variables set
- [ ] Airflow ingestion pool created
- [ ] ADR/CCR repository cloned to worker-accessible path
- [ ] Grafana dashboard imported
- [ ] Smoke test: manual DAG trigger passes all tasks
- [ ] Grafana panels return data

---

## 1. Infrastructure provisioning (Terraform / IaC)

### 1.1 InfluxDB

```hcl
# terraform/modules/influxdb/main.tf
resource "influxdb_bucket" "raw" {
  name  = "engineering_metrics_raw"
  org_id = var.influxdb_org_id

  retention_rules {
    type               = "expire"
    every_seconds      = 31536000   # 365 days
    shard_group_duration_seconds = 604800
  }
}

resource "influxdb_bucket" "agg" {
  name  = "engineering_metrics_agg"
  org_id = var.influxdb_org_id

  retention_rules {
    type               = "expire"
    every_seconds      = 94608000   # 1095 days (36 months)
    shard_group_duration_seconds = 2592000
  }
}

resource "influxdb_authorization" "metrics_writer" {
  org_id      = var.influxdb_org_id
  description = "Engineering metrics pipeline write token"

  permissions {
    action = "write"
    resource { type = "buckets" id = influxdb_bucket.raw.id }
  }
  permissions {
    action = "write"
    resource { type = "buckets" id = influxdb_bucket.agg.id }
  }
  permissions {
    action = "read"
    resource { type = "buckets" id = influxdb_bucket.raw.id }
  }
  permissions {
    action = "read"
    resource { type = "buckets" id = influxdb_bucket.agg.id }
  }
}
```

### 1.2 PostgreSQL (RDS / Cloud SQL / bare-metal)

```hcl
# terraform/modules/postgres/main.tf
resource "aws_db_instance" "eng_metrics" {
  identifier           = "eng-metrics-pg"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.medium"
  allocated_storage    = 50
  max_allocated_storage = 500
  db_name              = "eng_metrics"
  username             = "postgres"
  password             = var.pg_master_password   # injected from Vault
  deletion_protection  = true
  backup_retention_period = 14
  skip_final_snapshot  = false
  final_snapshot_identifier = "eng-metrics-final"

  tags = {
    service = "engineering-metrics-pipeline"
  }
}
```

Apply schema after instance is available:
```bash
psql "$PG_DSN_ADMIN" -f schema.sql
```

---

## 2. Secrets management (HashiCorp Vault)

### Vault path structure

```
secret/engineering-metrics-pipeline/
  git/
    api_token          # GitHub API token
  jira/
    api_email
    api_token
  influxdb/
    token
  postgres/
    dsn                # Full DSN including password
  slack/
    webhook_url
```

### Write secrets

```bash
vault kv put secret/engineering-metrics-pipeline/git \
  api_token="ghp_..."

vault kv put secret/engineering-metrics-pipeline/jira \
  api_email="svc-metrics@example.com" \
  api_token="ATATT..."

vault kv put secret/engineering-metrics-pipeline/influxdb \
  token="influxdb-operator-token..."

vault kv put secret/engineering-metrics-pipeline/postgres \
  dsn="postgresql://metrics_writer:CHANGE_ME@pg-host:5432/eng_metrics"

vault kv put secret/engineering-metrics-pipeline/slack \
  webhook_url="https://hooks.slack.com/services/..."
```

### Airflow Vault integration

Use the `apache-airflow-providers-hashicorp` package and set:
```ini
[secrets]
backend = airflow.providers.hashicorp.secrets.vault.VaultBackend
backend_kwargs = {"connections_path": "airflow-connections", "variables_path": "engineering-metrics-pipeline", "mount_point": "secret", "url": "https://vault.internal:8200", "token": "s.VAULT_TOKEN"}
```

Or inject env vars at pod level using Vault Agent Sidecar Injector:
```yaml
# annotations on Airflow worker pods
vault.hashicorp.com/agent-inject: "true"
vault.hashicorp.com/role: "airflow-metrics-pipeline"
vault.hashicorp.com/agent-inject-secret-env: "secret/engineering-metrics-pipeline/git"
vault.hashicorp.com/agent-inject-template-env: |
  {{- with secret "secret/engineering-metrics-pipeline/git" -}}
  export GIT_API_TOKEN="{{ .Data.data.api_token }}"
  {{- end }}
```

---

## 3. Docker image for Airflow workers

```dockerfile
FROM apache/airflow:2.7.3-python3.11

USER root
RUN apt-get update && apt-get install -y git libpq-dev gcc && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Pipeline scripts installed as a package
COPY docs/metrics-pipeline/ /opt/airflow/pipeline/
ENV PYTHONPATH="/opt/airflow/pipeline:${PYTHONPATH}"
```

`requirements.txt`:
```
influxdb-client>=1.38
psycopg2-binary>=2.9
requests>=2.31
pyyaml>=6.0
great-expectations>=0.18
```

Build and push:
```bash
docker build -t registry.example.com/airflow-metrics:latest .
docker push registry.example.com/airflow-metrics:latest
```

---

## 4. DAG deployment

```bash
# Copy to Airflow DAGs sync path (S3, GCS, or local NFS depending on your setup)
cp docs/metrics-pipeline/airflow_dag.py $AIRFLOW_DAGS_PATH/engineering_metrics_pipeline.py

# Rename ingest/transform/validate scripts so they're importable
cp docs/metrics-pipeline/ingest_git.py       $AIRFLOW_DAGS_PATH/ingest_git.py
cp docs/metrics-pipeline/ingest_jira.py      $AIRFLOW_DAGS_PATH/ingest_jira.py
cp docs/metrics-pipeline/ingest_cicd.py      $AIRFLOW_DAGS_PATH/ingest_cicd.py
cp docs/metrics-pipeline/ingest_adr.py       $AIRFLOW_DAGS_PATH/ingest_adr.py
cp docs/metrics-pipeline/transform_metrics.py $AIRFLOW_DAGS_PATH/transform_metrics.py
cp docs/metrics-pipeline/validate_data.py    $AIRFLOW_DAGS_PATH/validate_data.py
```

Verify Airflow picks up the DAG (no import errors):
```bash
airflow dags list | grep engineering_metrics_pipeline
airflow dags test engineering_metrics_pipeline 2024-01-01  # dry-run
```

---

## 5. ADR/CCR repository clone

The Airflow worker needs read access to the ADR/CCR Git repository. Options:

**Option A — Clone on worker startup (ephemeral workers)**
```bash
# In Airflow worker init script or Dockerfile CMD
git clone --depth=1 \
  https://oauth2:${ADR_REPO_TOKEN}@github.com/${GIT_ORG}/adr-repository.git \
  /opt/adr-repo
export ADR_REPO_PATH=/opt/adr-repo
```

**Option B — Persistent volume (stateful workers)**
```yaml
# Kubernetes PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: adr-repo-pvc
spec:
  accessModes: [ReadWriteMany]
  resources:
    requests:
      storage: 1Gi
```
Mount at `/opt/adr-repo`. A Git sync sidecar (k8s-sidecar or git-sync) keeps it fresh.

**Option C — Airflow GitSync (recommended for KubernetesExecutor)**
Use the `gitSync` configuration in the official Airflow Helm chart to auto-sync any number of repos including the ADR repo.

---

## 6. Airflow configuration summary

```bash
# Pool
airflow pools set ingestion_pool 4 "Limits concurrent external API calls"

# Variables
airflow variables set METRICS_PIPELINE_ALERT_EMAIL "platform-eng@example.com"
airflow variables set SLACK_WEBHOOK_URL             "https://hooks.slack.com/..."
airflow variables set GIT_LOOKBACK_DAYS             "1"
airflow variables set JIRA_LOOKBACK_DAYS            "7"
airflow variables set CICD_LOOKBACK_DAYS            "1"
airflow variables set ADR_LOOKBACK_DAYS             "7"
airflow variables set TRANSFORM_LOOKBACK_DAYS       "30"

# Enable DAG
airflow dags unpause engineering_metrics_pipeline
```

---

## 7. Grafana dashboard provisioning (config-as-code)

Store the dashboard JSON in your Grafana provisioning directory so it redeploys on restart:

```yaml
# grafana/provisioning/dashboards/engineering_metrics.yaml
apiVersion: 1
providers:
  - name: engineering-metrics
    orgId: 1
    type: file
    disableDeletion: true
    updateIntervalSeconds: 60
    allowUiUpdates: false
    options:
      path: /etc/grafana/dashboards
      foldersFromFilesStructure: true
```

```bash
cp grafana_dashboard.json /etc/grafana/dashboards/engineering_process_health.json
# Restart or reload Grafana
systemctl reload grafana-server
```

**Datasource provisioning:**
```yaml
# grafana/provisioning/datasources/influxdb.yaml
apiVersion: 1
datasources:
  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: "${INFLUXDB_ORG}"
      defaultBucket: engineering_metrics_raw
    secureJsonData:
      token: "${INFLUXDB_TOKEN}"
    isDefault: true
    editable: false
```

---

## 8. PostgreSQL retention cron (if not using Airflow cleanup task)

If your Airflow workers don't have access to PostgreSQL admin credentials, schedule retention cleanup separately using `pg_cron`:

```sql
-- Install pg_cron extension (PostgreSQL 15+)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Run daily at 02:00 UTC
SELECT cron.schedule('metrics-raw-cleanup', '0 2 * * *', $$
  DELETE FROM adr_records     WHERE ingested_at < NOW() - INTERVAL '12 months';
  DELETE FROM ccr_records     WHERE ingested_at < NOW() - INTERVAL '12 months';
  DELETE FROM defect_records  WHERE ingested_at < NOW() - INTERVAL '12 months';
  DELETE FROM security_findings WHERE ingested_at < NOW() - INTERVAL '12 months';
  DELETE FROM daily_metric_snapshots WHERE snapshot_date < NOW() - INTERVAL '36 months';
$$);
```

---

## 9. Smoke test procedure

Run after initial deployment to confirm end-to-end data flow:

```bash
# 1. Trigger DAG manually
airflow dags trigger engineering_metrics_pipeline

# 2. Watch task states
airflow tasks states-for-dag-run engineering_metrics_pipeline <run_id>

# 3. Verify InfluxDB has data
influx query '
from(bucket: "engineering_metrics_raw")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "git_metrics")
  |> count()
'

# 4. Verify PostgreSQL
psql "$PG_DSN" -c "SELECT COUNT(*) FROM adr_records;"

# 5. Open Grafana and confirm panels render data
# Navigate to Engineering Process Health Dashboard
# Set time range to "Last 7 days"
# All 6 panel groups should display values
```

---

## 10. Runbook — common failure scenarios

### DAG fails at `validate_data` with exit code 1

1. Check Airflow task logs: `airflow tasks logs engineering_metrics_pipeline validate_data <run_id>`
2. Look for `FAIL:` lines indicating which suite failed
3. Common fixes:
   - `unknown_stage_not_majority` → add Jira labels; see `PIPELINE_README.md` Troubleshooting
   - `escalated_adr_ref_valid` → CCR references an ADR not yet ingested; run `ingest_adr` manually then retry
4. Once fixed, clear the failed task and retry: `airflow tasks clear engineering_metrics_pipeline -t validate_data -s <start_date>`

### InfluxDB write timeout

1. Check InfluxDB health: `curl http://influxdb:8086/health`
2. If healthy, the bucket may be near capacity — check disk usage
3. Increase write timeout: set `INFLUXDB_WRITE_TIMEOUT_MS=30000` in worker env

### Grafana panels show "No data"

1. Confirm InfluxDB datasource is connected: Grafana → Configuration → Data Sources → Test
2. Confirm bucket names in dashboard variables match actual InfluxDB bucket names
3. Run the Flux query manually in InfluxDB Data Explorer to verify data exists for the time range

### ADR ingestion finds 0 records

1. Confirm `ADR_REPO_PATH` is set and the directory exists on the worker
2. Confirm `ADR_GLOB_PATTERN` matches your ADR file naming convention
3. Test locally: `python ingest_adr.py --lookback-days 30`
4. Check that ADR files have valid YAML frontmatter with `adr_ref:` field

---

## See also

- `PIPELINE_README.md` — architecture overview and local development guide
- `schema.sql` — PostgreSQL and InfluxDB schema reference
- [[DATA_ENGINEER_SKILL]] §5
- [[DEVOPS_PLATFORM_ENGINEER_SKILL]] §3.3
- [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] §5
