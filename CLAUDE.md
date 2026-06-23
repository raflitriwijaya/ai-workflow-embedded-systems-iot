# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **document-as-code governance vault**, not an application codebase. It defines *how* an embedded/IoT AI product is built — by which roles, under what interface contracts, and behind which quality gates. The content is Markdown authored for [Obsidian](https://obsidian.md); there is no app to build or run for the vault itself.

The reference product the whole vault is designed and stress-tested against is **AgriSpectra**: an agricultural IoT sensor node doing pre-symptomatic crop-disease detection with a quantized CNN on an STM32H7 MCU, LoRaWAN uplink, solar power, targeting a 50,000-device fleet over a 7-year field lifetime. When a document says "the product," it means AgriSpectra.

Note: `README.md` and `GUIDELINE.md` refer to "CLAUDE.md" as an elaborate "master reference" with sections like §3.10 and §7.4. That document was never written as such — the governing rules are consolidated in this file instead. Treat those cross-references as pointing here.

## Authority order (which document wins)

1. **`*_SKILL.md` (14 role cards)** — always authoritative for role scope, deliverables, and interface contracts.
2. **`docs/schemas/`, `docs/agent-protocol/`, `docs/fmea/`, etc.** — authoritative specs for their subject.
3. **`docs/review_v1/`, `review_v2/`, `review_v3/`** — *historical audit record only*. They explain *why* decisions were made; never edit a SKILL.md to match a review doc. The current verdict lives in `docs/review_v3/REVIEW_V3_FINAL.md`.

## Architecture: the 14-role contract graph

Fourteen primary roles (+ 2 fractional: ARCH-DEP, Process Architect) each own one layer of the edge→gateway→cloud stack and work **concurrently** against frozen interface contracts. Canonical role IDs and their files:

`ARCH` Architect · `FW` Firmware · `HW` Hardware · `ML` Edge AI/ML · `MLOPS` · `DATA` · `DEVOPS` · `BACK` Backend/Cloud · `FRONT` Frontend · `QA` · `SEC` Security · `PO` Product Owner/TPM · `BIZ` Business Consultant · `RES` Researcher. The full ID→file→alias registry is in `docs/automation/RECIPROCITY_AUDIT_SPEC.md` §3.3.

The 14 roles form a fully-connected graph of **91 symmetric interface contracts** (14×13÷2). The Mermaid topology is in `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md` §14, but the per-edge **§6 Interface Contracts** sections in each SKILL.md are authoritative.

### Every SKILL.md has the identical 10-section structure

`§1` Role Identity · `§2` Core Mission & Scope · `§3` Lifecycle Stage Engagement · `§4` Technical Competencies · `§5` Deliverables & Artifacts · `§6` Interface Contracts · `§7` Decision Authority & Governance · `§8` Standards & Best Practices · `§9` AI Agent Execution Guide · `§10` Success Metrics & KPIs. Do not renumber or restructure these.

### The contract-symmetry invariant (most important editing rule)

Each `### 6.X` block states **Provides** / **Requires** / **Cadence**. For any pair A↔B, A's `Provides` to B must mirror B's `Requires` from A (and vice versa), and they must share a Cadence checkpoint. **When you edit any §6 entry, you must update the counterpart role's §6 entry in the same change** — otherwise you introduce an asymmetry. `docs/automation/RECIPROCITY_AUDIT_SPEC.md` defines a deterministic checker (Jaccard match ≥ 0.35) intended to block such asymmetries in CI; it is a **specification only — `tools/reciprocity-audit/` does not exist yet**, so symmetry is currently maintained by hand. Trace a deliverable: producer's `§5` → producer's `§6` Provides → consumer's `§6` Requires.

### Governance artifacts

- **ADR** (Architecture Decision Record, `ADR-NNNN`) — records a significant/irreversible technical decision; required whenever a budget/contract/requirement can't be met as written.
- **CCR** (Contract Clarification Record, `CCR-NNNN`) — changes or clarifies a §6 clause; a **BLOCKING** CCR halts related work.
- **8 machine-parseable YAML schemas** in `docs/schemas/` (ADR, CCR, DQIR, IRD, OCM, SIRC, TTP, BIA) — catalogued in `docs/schemas/SCHEMA_INDEX.md`. Use these structured formats, not prose, when producing those deliverables.

### Current project state — keep documents honest about it

The verdict is **CONDITIONAL GO**. The `docs/fmea/SYSTEM_FMEA_V1.md` has **17 open Critical failure chains** (RPN ≥ 200), detection coverage is **≈ 53% vs. a ≥ 95% gate** (FC-001 RPN 486, FC-022 RPN 405). This gap is written into the documents deliberately — it is the burn-down baseline. Do not "tidy" honest gap figures into optimistic ones.

## Authoring conventions

- **Obsidian wikilinks inside vault docs:** `[[FILE_BASENAME|Display Text]]` (no `.md`, no path for root files). This differs from the GitHub-flavored Markdown links used elsewhere. Match the style of the file you are editing.
- **YAML frontmatter** on most docs: `title`, `date`, `status` (`draft`/`reviewing`/`final`/`superseded`), `tags`, `cssclass`. Preserve it.
- **No `TBD`/placeholder values in any `status: final` document.** If a value is unknown, escalate it (raise an ADR/CCR) rather than inventing a plausible fill-in — "measure-first, delegate-second."
- **Every measurement carries explicit units; define each acronym on first use** (glossary: `docs/ACRONYM_GLOSSARY.md`). Never write "approximately"/"~" in place of a measured figure in a final doc.
- **SemVer on versioned artifacts;** firmware/model artifacts are identified by Git-SHA + SemVer.
- **Permanent human gates (never delegate to an agent):** HG-01 Security release veto · HG-04 Architect production sign-off · QA go/no-go stage transition.

## Commands

The vault has **no build/lint/test of its own**. The only executable code is the engineering-metrics pipeline.

### Metrics pipeline (`docs/metrics-pipeline/`) — Python 3.11+, Airflow 2.7, InfluxDB 2.7, PostgreSQL 15

Each ingest/transform/validate script has a `__main__` block and runs standalone. Set the required env vars first (`INFLUXDB_URL`, `INFLUXDB_TOKEN`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET_RAW`, `INFLUXDB_BUCKET_AGG`, `PG_DSN`, plus per-source vars — see `docs/metrics-pipeline/PIPELINE_README.md` for the full table). Run from `docs/metrics-pipeline/`:

```bash
pip install influxdb-client psycopg2-binary requests pyyaml great-expectations "apache-airflow[postgres]"

python ingest_git.py   --lookback-days 2     # Git: PR cycle time, review turnaround, PR size
python ingest_jira.py  --lookback-days 7     # Jira: velocity, cycle time, defect discovery stage
python ingest_cicd.py  --lookback-days 1     # CI/CD: build/test pass rate, deploy frequency
python ingest_adr.py   --lookback-days 7     # ADR/CCR Markdown (YAML frontmatter) → metrics
python transform_metrics.py --lookback-days 30   # raw InfluxDB → aggregated KPIs
python validate_data.py                          # Great Expectations checks; exits 1 on failure
```

`validate_data.py` is the closest thing to a test gate (non-zero exit = fail; Airflow retries 3× then alerts). `ingest_adr.py` parses YAML frontmatter from ADR/CCR Markdown files — the expected `adr_ref`/`ccr_ref`/`tier`/`status` frontmatter shape is documented in `PIPELINE_README.md`. DB/Airflow/Grafana setup steps are in `PIPELINE_README.md` and `deployment_guide.md`.
