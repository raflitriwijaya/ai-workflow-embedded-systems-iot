# eval-harness

Python package implementing the Evaluation Harness scoring engine, statistics,
persistence, API, and CLIs. See the build overview in
[../README.md](../README.md) and the specification
[EVALUATION_HARNESS_SPEC](../../EVALUATION_HARNESS_SPEC.md).

## Layout

| Module | Responsibility | Optional deps |
|---|---|---|
| `eval_harness.scoring` | Scorers + schema validators (ADR/CCR/DQIR/IRD/OCM) | none (stdlib) |
| `eval_harness.stats` | Percentiles, Fleiss' κ, ICC, Welch's t, readiness | none (stdlib) |
| `eval_harness.db` | PostgreSQL repository + pool | `db` extra (psycopg2) |
| `eval_harness.service` | Ingest → score → persist, review, readiness | `db` |
| `eval_harness.api` | FastAPI ingest + review portal | `api` extra |
| `eval_harness.cli` | `harness-capture`, `harness-evaluate` | `db` |
| `eval_harness.pipeline` | Statistical engine + Gate Reporter | `db` |
| `eval_harness.artifacts` | URI fetch + YAML/MD-frontmatter parsing | `ingest` extra (PyYAML) |

The `scoring` and `stats` cores have **no third-party dependencies** and are
fully unit-tested with the standard library.

## Develop

```bash
pip install "./harness[dev]"        # ruff + pytest
cd harness && pytest -q             # 44 unit tests
ruff check .
```

## Console scripts

```bash
harness-capture submit --role DATA --deliverable D1-DE-1 --artifact ./dag.py \
    --metrics ./ci_metrics.json --producer-id rani --time-spent 95 --complexity 3
harness-capture status --role DATA
harness-evaluate submit --role MLOPS --deliverable D1-ML-4 --artifact ./ocm.yaml \
    --agent-id mlops-agent-v1 --accepted
harness-evaluate readiness --role MLOPS --recompute
harness-stats --wave 1 --report-dir ./reports
```
