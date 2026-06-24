---
title: "Evaluation Harness — Operational Build"
date: 2026-06-24
status: draft
tags:
  - evaluation
  - ai-agent
  - transformation
cssclass: evaluation-spec
---

# Evaluation Harness — Operational Build

An operational implementation of the [[EVALUATION_HARNESS_SPEC|Evaluation Harness Specification]]
(v1.0.0). This is the **hard gate** before any AI agent activation
("measure first, delegate second"): every role needs ≥30 human baseline samples
per deliverable, scored blind, before its agent may be turned on.

> **Owner (operate):** [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA & Test Automation Engineer]] (Process Architect)
> **Builder:** [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps/Platform Engineer]]
> **Scope of this build:** Wave 1 (DATA, FE, MLOPS), extensible to all 14 roles.

---

## 1. What this delivers (task → files)

| Task section | Implementation |
|---|---|
| **1. Database schema & storage** | [db/migrations/](db/migrations/) (`0001_core_schema.sql`, `0002_views_and_functions.sql`), [db/seed/](db/seed/) (Wave-1 roles, deliverables, rubrics), [db/migrate.py](db/migrate.py) (versioned, idempotent runner) |
| **2. Scoring engine** | [harness/eval_harness/scoring/](harness/eval_harness/scoring/) — schema validators (ADR/CCR/DQIR/IRD/OCM), AUTO metrics scorer, hybrid combiner, blind HR scoring with adjudication |
| Inter-rater reliability + Welch's t | [harness/eval_harness/stats/](harness/eval_harness/stats/) — Fleiss' κ, ICC(2,1)/(2,k), Welch's t-test, percentiles, readiness |
| **3. Baseline capture tool** | [harness/eval_harness/cli/capture.py](harness/eval_harness/cli/capture.py) + the `POST /api/v1/submissions` endpoint; ≥30 enforcement via `v_sample_progress` / WG-1 |
| **4. Agent evaluation pipeline** | [harness/eval_harness/cli/evaluate.py](harness/eval_harness/cli/evaluate.py) + [service.py](harness/eval_harness/service.py); draft-acceptance + composite + trend via [pipeline/statistical_engine.py](harness/eval_harness/pipeline/statistical_engine.py) |
| **5. Dashboard** | [dashboard/grafana/dashboards/evaluation_harness.json](dashboard/grafana/dashboards/evaluation_harness.json) — spec DASH-1..10 + a time-to-completion panel and an explicit per-role GREEN/YELLOW/RED panel (12 total) + provisioning |
| **6. Deployment guide** | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md), [docker-compose.yml](docker-compose.yml), [.env.example](.env.example), [ci/](ci/) |

## 2. Directory tree

```
docs/evaluation/build/
├── README.md                     ← you are here
├── DEPLOYMENT_GUIDE.md
├── docker-compose.yml · Dockerfile · .env.example
├── db/
│   ├── migrate.py                ← versioned migration runner
│   ├── migrations/               ← 0001 core schema, 0002 views+functions
│   └── seed/                     ← Wave-1 roles, deliverables, rubrics
├── harness/                      ← Python project (pip install ./harness)
│   ├── pyproject.toml · conftest.py
│   ├── eval_harness/
│   │   ├── scoring/  stats/  api/  cli/  pipeline/
│   │   ├── config.py  db.py  service.py  artifacts.py  logging_setup.py
│   └── tests/                    ← 44 unit tests (stdlib-only core)
├── dashboard/grafana/            ← dashboard JSON + provisioning
└── ci/                           ← GitHub Actions, smoke test, Airflow DAG
```

## 3. Quickstart

```bash
cd docs/evaluation/build
cp .env.example .env        # then edit the secrets
docker compose up -d --build
# migrate+seed run automatically; then:
open http://localhost:3000  # Grafana (admin / $GRAFANA_ADMIN_PASSWORD)
curl localhost:8080/healthz
```

Capture a baseline sample and evaluate an agent:

```bash
# inside the api container, or any host with the package + DATABASE_URL set
harness-capture submit --role MLOPS --deliverable D1-ML-4 \
    --artifact ./model_ota.yaml --producer-id ahmad --time-spent 40 --complexity 3
harness-evaluate submit --role MLOPS --deliverable D1-ML-4 \
    --artifact ./agent_ota.yaml --agent-id mlops-agent-v1 --accepted
harness-evaluate readiness --role MLOPS --recompute
```

## 4. Scoring model (how a score is produced)

Each rubric **dimension** normalises to `[0,1]`; the sub-score is
`100 × weighted_mean(norm)`:

- **AUTO_BINARY** — pass→1, fail→0 (e.g. `ruff` 0 errors).
- **AUTO_CONTINUOUS** — `clamp(value/threshold)` for higher-is-better (`>=`),
  `clamp(threshold/value)` for lower-is-better (`<=`) (e.g. coverage ≥80%, LCP ≤2.5 s).
- **HR_RUBRIC** — mean of two blind reviewers' 0–3 scores; if they diverge by
  >1 a third adjudicates (median of three); normalised `/3`.
- **schema:NAME** — the auto sub-score is `% of V-<NAME>-NN rules passed`,
  computed by the validator calibrated to [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OCM]],
  [[ADR_SCHEMA|ADR]], [[CCR_SCHEMA|CCR]], [[DQIR_SCHEMA|DQIR]], and
  [[INTEGRATION_READINESS_DECLARATION_SCHEMA|IRD]].

**Composite (HYB):** `auto_weight×AUTO + hr_weight×HR`. **Composite role score:**
weighted average of the 5 deliverables (spec §3 weights). **Readiness (G1):**
GREEN when baselines ≥30 **and** agent mean ≥ baseline mean with one-tailed
Welch p<0.05 **and** draft-acceptance ≥70%.

## 5. Extending to later waves

The harness is data-driven — adding Wave 2–4 requires **no code change**:
1. add `deliverables` + `scoring_rubrics` rows (a new seed file, like
   [db/seed/0002_rubrics_wave1.sql](db/seed/0002_rubrics_wave1.sql));
2. wire any new governance-schema deliverable to `scorer_key='schema:<NAME>'`
   (validator already exists for ADR/CCR/DQIR/IRD/OCM);
3. re-run `migrate.py --seed`.

All 14 roles are already seeded in `roles`; only Wave-1 deliverables/rubrics are
populated per the task constraint.

## 6. Verification status (honest)

- **44/44 unit tests pass**; the statistics are checked against published values
  (t-table critical values, F critical value, Fleiss' κ = ±1 bounds, ICC=1 for
  perfect agreement). `ruff` is clean.
- The pure scoring/statistics core is dependency-free (no scipy/numpy needed); a
  pure-Python incomplete-beta backs the t- and F-distributions. scipy may be
  substituted in production.
- The DB + service + API path is exercised end-to-end by [ci/smoke_test.py](ci/smoke_test.py)
  against a real PostgreSQL in CI ([ci/evaluation-harness-ci.yml](ci/evaluation-harness-ci.yml)).

### Notes & calibration decisions
- **HYB AUTO/HR weight splits** (e.g. D1-DE-2 = 70/30) are **build-time defaults**
  flagged for TSC ratification (spec §10.1): spec §3.1–§3.3 enumerate the AUTO and
  HR sub-metrics but do not give a numeric split. They live in the `deliverables`
  table and change by `UPDATE`, no code change. Recorded in each row's `calibration_note`.
- **Thresholds the spec leaves to a role-owned SLO** (no number stated) are scored
  as AUTO_BINARY booleans emitted by the CI tool, so the harness never invents an
  SLO number (CLAUDE.md §1, "measure-first").
- **Finding:** the OCM schema's own example instance violates **V-OCM-16**
  (`minimum_version: 2.4.2` with `excluded_versions: [2.4.0, 2.4.1]`, which are
  *below* the minimum). The validator implements the rule as written and would
  score that example 15/16; surfaced here rather than silently relaxed
  (CLAUDE.md §10.3 "honesty over polish"). Worth a [[CCR_SCHEMA|CCR]] against the schema.
- **DASH-9** (harness/acceptance alignment) is computed live via PostgreSQL
  `corr()`; the `role_readiness.harness_alignment_r` column is reserved for a
  materialised value if needed later.

## 7. Governance touchpoints

This build does not bypass any HITL gate. It **produces evidence** for the TSC
Wave-activation decision (WG-1/WG-2/WG-3) and the Phase 1→2 gate (G1–G7); the TSC
Chair retains the activation decision (spec §1.2). Scoring results are append-only.
