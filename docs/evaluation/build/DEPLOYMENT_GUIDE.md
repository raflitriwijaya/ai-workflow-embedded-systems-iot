---
title: "Evaluation Harness — Deployment Guide"
date: 2026-06-24
status: draft
tags:
  - evaluation
  - devops
  - deployment
cssclass: evaluation-spec
---

# Evaluation Harness — Deployment Guide

Operational runbook for the [[EVALUATION_HARNESS_SPEC|Evaluation Harness]] build.
Owner: [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps/Platform Engineer]] (build) /
[[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA Process Architect]] (operate).

---

## 1. Prerequisites

- Docker Engine ≥ 24 + Docker Compose v2 (`docker compose`, not `docker-compose`).
- For local dev without Docker: Python ≥ 3.11 and a reachable PostgreSQL ≥ 13
  (TimescaleDB optional; the migration auto-detects and skips it if absent).
- Network egress to pull the `timescale/timescaledb`, `grafana/grafana`, and
  `python:3.12-slim` images on first build.

## 2. Secrets management

**No credential is ever committed.** Every secret is supplied via environment
variables (task constraint; CLAUDE.md §7.6):

| Variable | Used by | Notes |
|---|---|---|
| `HARNESS_DB_PASSWORD` / `PGPASSWORD` | db, migrate, api, stats | Postgres superuser-equivalent for the harness DB |
| `DATABASE_URL` | migrate, api, cli, stats | Overrides `PG*` if set |
| `GRAFANA_DB_PASSWORD` | grafana-grants, grafana | Read-only role password |
| `GRAFANA_ADMIN_PASSWORD` | grafana | Grafana admin login |
| `S3_ACCESS_KEY` / `S3_SECRET_KEY` | api, cli (s3:// artifacts) | Only if using MinIO/S3 |

Local/staging: copy [.env.example](.env.example) → `.env` and fill in. `.env` is
git-ignored (add to your repo `.gitignore`).

**Production:** do **not** use a `.env` file. Inject the same variables from your
secret manager:
- Kubernetes: a `Secret` mounted as env vars (e.g. External Secrets Operator →
  Vault/AWS Secrets Manager). The migration runner and API read `DATABASE_URL`
  or `PG*` directly.
- Grafana datasource password is read from `$GRAFANA_DB_PASSWORD` at provisioning
  load time (see [dashboard/grafana/provisioning/datasources/postgres.yaml](dashboard/grafana/provisioning/datasources/postgres.yaml)).
- The harness DB is **isolated** from production systems — separate credentials,
  no access to production data (spec §9.1).

## 3. Local / staging deployment (Docker Compose)

```bash
cd docs/evaluation/build
cp .env.example .env        # edit all change-me-* values
docker compose up -d --build
```

Bring-up order is enforced by health checks and `depends_on` conditions:

1. **db** (TimescaleDB) — waits for `pg_isready`.
2. **migrate** — applies `db/migrations/*` then `db/seed/*` (idempotent), exits 0.
3. **grafana-grants** — creates the least-privilege `grafana_ro` role + SELECT grants.
4. **api** — serves the Ingest + Review API on `:${HARNESS_API_PORT}`.
5. **stats** — runs `harness-stats` every `${HARNESS_STATS_INTERVAL}` seconds.
6. **grafana** — provisions the datasource + the 10-panel dashboard.

Verify:

```bash
docker compose ps
curl -fsS localhost:${HARNESS_API_PORT:-8080}/healthz
docker compose logs migrate | tail -20      # "done: N file(s) applied"
open http://localhost:${GRAFANA_PORT:-3000}  # dashboard "Evaluation Harness — AI Agent Readiness"
```

Optional MinIO object store for `s3://` artifacts:

```bash
docker compose --profile objectstore up -d minio
# set HARNESS_ARTIFACT_STORE=s3://eval-harness + S3_* in .env, then recreate api/stats
```

### Re-running migrations

Migrations are versioned and tracked in `schema_migrations`. Re-running is safe:

```bash
docker compose run --rm migrate python db/migrate.py --seed --status   # show applied/pending
docker compose run --rm migrate python db/migrate.py --seed            # apply pending only
```

Editing an already-applied migration file is rejected (checksum drift) — add a
new `000N_*.sql` instead.

## 4. Backups & retention

- `pgdata` volume holds all scores; schedule `pg_dump` (spec §9.1 "daily backups").
  ```bash
  docker compose exec -T db pg_dump -U "$HARNESS_DB_USER" "$HARNESS_DB_NAME" | gzip > backup-$(date +%F).sql.gz
  ```
- Scoring rows are append-only; never `UPDATE`/`DELETE` historical
  `evaluation_runs` / `human_baselines` / `agent_results` (spec §9.1).
- Artifact store retention: 2 years (spec §9.1) — configure on the MinIO/S3 bucket.

## 5. CI/CD integration

[ci/evaluation-harness-ci.yml](ci/evaluation-harness-ci.yml) is a GitHub Actions
workflow. **Install it** by copying to the repo root:

```bash
mkdir -p .github/workflows
cp docs/evaluation/build/ci/evaluation-harness-ci.yml .github/workflows/
```

Pipeline stages:
- **lint-test** — `ruff check` + `pytest` on the dependency-free scoring/stats core.
- **db-smoke** — spins up `postgres:16`, runs `migrate.py --seed`, asserts an
  idempotent re-run, then runs [ci/smoke_test.py](ci/smoke_test.py) end-to-end
  (schema:OCM scoring, hard-block detection, hybrid review→finalise, readiness).
- **docker** — builds the harness image.

**Auto-submission from other CI pipelines** (spec §9.1 "integrate harness into
CI/CD"): a producing role's pipeline POSTs its artifact + tool metrics to the
harness after its own tests pass, e.g.:

```bash
curl -fsS -X POST "$HARNESS_API/api/v1/submissions" \
  -H 'content-type: application/json' \
  -d '{"role_code":"DATA","deliverable_id":"D1-DE-1","producer_type":"AGENT",
       "agent_id":"data-agent-v1","artifact_uri":"s3://eval-harness/sub/'$CI_JOB_ID'/dag.py",
       "metrics":{"lint_pass":true,"dag_import":true,"unit_test_pass_rate":94,
                  "schema_validation":true,"p99_latency_slo_met":true},
       "human_reviewer_id":"'$REVIEWER'","human_accepted":true,"human_edit_required":false}'
```

Scheduled statistical engine in production: use [ci/airflow_dag.py](ci/airflow_dag.py)
(hourly) instead of the compose `stats` loop.

## 6. Scaling & hardening notes

- The API is stateless behind the connection pool; scale horizontally
  (`docker compose up -d --scale api=3` or a K8s Deployment) behind mTLS
  (spec §2.2 "behind mTLS").
- Bind Postgres to localhost only (already done in compose) or keep it on a
  private network; do not expose 5432 publicly.
- Grafana uses a **read-only** DB role (`grafana_ro`); team leads get read-only
  Grafana access (spec §8.1).
- Monitor the harness itself via the existing observability stack (logs are
  single-line JSON by default; set `HARNESS_LOG_FORMAT=plain` for humans).

## 7. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `migrate` exits non-zero with "Checksum drift" | A previously-applied migration was edited. Restore it and add a new migration. |
| `/healthz` 503 | DB unreachable — check `db` health and `PGHOST`/`DATABASE_URL`. |
| Grafana panels empty | No data yet (capture baselines), or `grafana_ro` lacks SELECT — re-run `grafana-grants`. |
| Submission 400 "unknown/inactive deliverable" | `deliverable_id` not seeded for that role, or wrong `role_code`. |
| HYB submission stuck `AWAITING_HR` | Needs **two** blind reviewers via `POST /api/v1/reviews`; divergence >1 needs an adjudicator. |
| `s3://` artifact error | Install `boto3` and set `S3_ENDPOINT_URL`/`S3_*`, or use a `file://` URI. |
