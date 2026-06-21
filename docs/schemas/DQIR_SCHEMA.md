---
title: "DQIR Schema — Data Quality Issue Report"
owning_roles:
  - "[[EDGE_AI_ML_ENGINEER_SKILL]]"
consuming_roles:
  - "[[DATA_ENGINEER_SKILL]]"
  - "[[MLOPS_ENGINEER_SKILL]]"
version: "1.0.0"
tags:
  - schema
  - dqir
  - data-quality
  - edge-ai
  - machine-parseable
---

# DQIR Schema — Data Quality Issue Report

## Purpose

A Data Quality Issue Report (DQIR) is raised by the Edge AI/ML Engineer when a dataset or data pipeline output fails to meet the quality standards required for model training, validation, or inference. It provides a structured record of the issue type, affected data elements, severity, root cause hypothesis, and correction status. The schema enables automated dataset health dashboards, SLA tracking, and training pipeline gating.

**Standards referenced:** ISO 8000-8:2015 (Data Quality), NIST IR 8259A (IoT Device Cybersecurity — Data Integrity), DMA DAMA-DMBOK2 Data Quality Dimensions.

---

## YAML Schema Definition

```yaml
# DQIR Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) DQIR-NNNN format, e.g. "DQIR-0023"
date_raised: date                  # (required) ISO 8601
date_resolved: date                # (optional) ISO 8601 — null until status = CORRECTED or ACCEPTED

# ── Dataset Reference ─────────────────────────────────────────────────────────
dataset:
  name: string                     # (required) canonical dataset name, e.g. "vibration-edge-v3"
  version: string                  # (required) semantic version or SHA-256 prefix (12 chars)
  source_pipeline: string          # (required) pipeline ID or name producing this dataset
  collection_window:               # (required)
    start: datetime                # ISO 8601 datetime
    end: datetime                  # ISO 8601 datetime
  storage_location: string         # (required) S3/GCS URI or local path prefix

# ── Affected Features ─────────────────────────────────────────────────────────
affected_features:                 # (required) list — at least 1 entry
  - feature_name: string           # (required) exact column/field name
    feature_type: string           # (required) enum: NUMERIC | CATEGORICAL | TIMESTAMP | BINARY | TEXT
    affected_row_count: integer    # (required) non-negative integer
    affected_row_percentage: number # (required) 0.0–100.0
    sample_bad_values: list[string] # (optional) up to 5 example bad values (anonymised if PII)

# ── Issue Classification ──────────────────────────────────────────────────────
issue_type:                        # (required) enum — DAMA-DMBOK2 aligned
  type: string
  allowed_values:
    - MISSING_VALUES       # Null / NaN rate exceeds threshold
    - OUT_OF_RANGE         # Values outside sensor physics bounds
    - DISTRIBUTION_DRIFT   # Statistical distribution shifted vs. baseline
    - LABEL_INCONSISTENCY  # Ground-truth labels contradictory or mislabelled
    - TIMESTAMP_ANOMALY    # Gaps, duplicates, or out-of-order timestamps
    - SCHEMA_MISMATCH      # Feature names, types, or cardinality differ from spec
    - SENSOR_FAULT         # Hardware fault signature detected in data stream
    - PII_LEAKAGE          # Personally identifiable information found in dataset

severity:                          # (required) enum
  type: string
  allowed_values:
    - CRITICAL  # Model training must halt; data unusable; immediate correction required
    - HIGH      # Model performance degraded >5%; correction required before training run
    - MEDIUM    # Model performance degraded ≤5%; correction required before release
    - LOW       # Cosmetic or statistical anomaly; document and monitor

quality_dimension:                 # (required) enum — DAMA-DMBOK2 primary dimension
  type: string
  allowed_values:
    - COMPLETENESS
    - ACCURACY
    - CONSISTENCY
    - TIMELINESS
    - VALIDITY
    - UNIQUENESS

# ── Metrics ───────────────────────────────────────────────────────────────────
metrics:
  total_rows_inspected: integer    # (required) total rows in dataset version
  affected_rows: integer           # (required) rows with at least one quality issue
  affected_row_percentage: number  # (required) computed: affected_rows / total_rows * 100
  null_rate_per_feature: object    # (optional) map of feature_name -> null_percentage

baseline_comparison:               # (optional) — filled when issue_type = DISTRIBUTION_DRIFT
  baseline_dataset_version: string
  ks_test_p_value: number          # Kolmogorov-Smirnov test p-value; < 0.05 = drift
  psi_score: number                # Population Stability Index; > 0.25 = significant drift

# ── Root Cause ────────────────────────────────────────────────────────────────
root_cause:
  hypothesis: string               # (required) ≥30 chars — initial root cause hypothesis
  confirmed: boolean               # (required) false until investigation complete
  confirmed_cause: string          # (optional) ≥30 chars — filled when confirmed = true
  pipeline_stage: string           # (optional) stage where issue originates, e.g. "sensor-ingestion"

# ── Correction ────────────────────────────────────────────────────────────────
correction_status:                 # (required) enum
  type: string
  allowed_values:
    - PENDING       # No correction action started
    - IN_PROGRESS   # Correction being implemented by Data Engineer
    - CORRECTED     # Data re-generated; quality re-validated
    - ACCEPTED      # Issue accepted as-is with documented rationale (MEDIUM/LOW only)
    - WONTFIX       # Correction not feasible; downstream consumers notified

correction_actions:                # (optional) list — actions taken or planned
  - action: string                 # description of correction step
    owner: string                  # Obsidian wikilink to owning role
    due_date: date                 # ISO 8601 target date
    completed: boolean

corrected_dataset_version: string  # (optional) version of the re-generated clean dataset

# ── Downstream Impact ─────────────────────────────────────────────────────────
training_pipeline_blocked: boolean # (required) true if training cannot run with this data
affected_models: list[string]      # (optional) model IDs that use this dataset
estimated_retraining_cost_gpu_hours: number # (optional) GPU-hours to retrain after fix

# ── Signatories ───────────────────────────────────────────────────────────────
raised_by:
  role: string                     # (required) "[[EDGE_AI_ML_ENGINEER_SKILL]]"
  name: string                     # (optional)

acknowledged_by:                   # (optional)
  role: string                     # "[[DATA_ENGINEER_SKILL]]"
  name: string
  date: date

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "DQIR-0008"
date_raised: "2026-05-14"
date_resolved: null

dataset:
  name: "vibration-edge-v4"
  version: "4.2.1"
  source_pipeline: "edge-ingest-pipeline-v3"
  collection_window:
    start: "2026-04-01T00:00:00Z"
    end: "2026-04-30T23:59:59Z"
  storage_location: "s3://iot-datalake/vibration/v4/2026-04/"

affected_features:
  - feature_name: "rms_acceleration_x"
    feature_type: NUMERIC
    affected_row_count: 142800
    affected_row_percentage: 23.8
    sample_bad_values: ["NaN", "NaN", "-9999.0", "NaN", "NaN"]
  - feature_name: "timestamp_device"
    feature_type: TIMESTAMP
    affected_row_count: 8400
    affected_row_percentage: 1.4
    sample_bad_values: ["2026-01-01T00:00:00Z", "1970-01-01T00:00:00Z"]

issue_type: MISSING_VALUES
severity: HIGH
quality_dimension: COMPLETENESS

metrics:
  total_rows_inspected: 600000
  affected_rows: 142800
  affected_row_percentage: 23.8
  null_rate_per_feature:
    rms_acceleration_x: 23.8
    rms_acceleration_y: 0.2
    rms_acceleration_z: 0.1
    timestamp_device: 1.4

baseline_comparison: null

root_cause:
  hypothesis: >
    Accelerometer X-axis on gateway unit GW-047 and GW-051 shows saturation/dropout pattern
    consistent with loose cable or ADC reference voltage failure. Fault began 2026-04-06
    based on timestamp correlation.
  confirmed: false
  confirmed_cause: null
  pipeline_stage: "sensor-ingestion"

correction_status: IN_PROGRESS

correction_actions:
  - action: "Dispatch field technician to inspect GW-047 and GW-051 hardware"
    owner: "[[FIRMWARE_ENGINEER_SKILL]]"
    due_date: "2026-05-20"
    completed: false
  - action: "Implement NaN-imputation filter in edge-ingest-pipeline for ADC dropout signature"
    owner: "[[DATA_ENGINEER_SKILL]]"
    due_date: "2026-05-25"
    completed: false
  - action: "Re-collect 30 days clean data from repaired gateways"
    owner: "[[DATA_ENGINEER_SKILL]]"
    due_date: "2026-06-15"
    completed: false

corrected_dataset_version: null

training_pipeline_blocked: true
affected_models:
  - "vibration-anomaly-detector-v2"
  - "bearing-fault-classifier-v1"
estimated_retraining_cost_gpu_hours: 12.5

raised_by:
  role: "[[EDGE_AI_ML_ENGINEER_SKILL]]"
  name: "Ahmad Fauzi"

acknowledged_by:
  role: "[[DATA_ENGINEER_SKILL]]"
  name: "Rani Kusuma"
  date: "2026-05-15"

tags:
  - dqir-open
  - missing-values
  - accelerometer
  - high-severity
  - training-blocked

notes: "Gateway fault log attached at docs/hw/gw-047-fault-log.md. Models re-queued for 2026-06-20 training run."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-DQIR-01 | `id` matches regex `^DQIR-\d{4}$` |
| V-DQIR-02 | `issue_type` is one of the 8 allowed enum values |
| V-DQIR-03 | `severity` is one of the 4 allowed enum values |
| V-DQIR-04 | `quality_dimension` is one of the 6 allowed enum values |
| V-DQIR-05 | `correction_status` is one of the 5 allowed enum values |
| V-DQIR-06 | `affected_features` has ≥ 1 entry |
| V-DQIR-07 | `affected_row_percentage` = `affected_rows` / `total_rows_inspected` × 100 (±0.1 tolerance) |
| V-DQIR-08 | If `severity ∈ {CRITICAL, HIGH}`, `training_pipeline_blocked` must be `true` |
| V-DQIR-09 | If `correction_status = ACCEPTED`, `severity` must be `MEDIUM` or `LOW` |
| V-DQIR-10 | If `correction_status = CORRECTED`, `corrected_dataset_version` must be non-null |
| V-DQIR-11 | If `issue_type = DISTRIBUTION_DRIFT`, `baseline_comparison` block must be present |
| V-DQIR-12 | `dataset.collection_window.start` < `dataset.collection_window.end` |
| V-DQIR-13 | `sample_bad_values` list length ≤ 5 per feature |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Block training pipeline**: if `training_pipeline_blocked = true` and `correction_status ∈ {PENDING, IN_PROGRESS}`, the MLOps orchestration layer must refuse to schedule a training run for any model in `affected_models`.
2. **Validate arithmetic**: compute `affected_row_percentage` from raw counts and compare to the stated value; flag discrepancies > 0.1%.
3. **Dataset registry cross-reference**: resolve `dataset.name` + `dataset.version` against the data catalog; verify the `storage_location` URI is accessible.
4. **Drift detection integration**: when `issue_type = DISTRIBUTION_DRIFT`, verify that `baseline_comparison.psi_score` and `ks_test_p_value` are populated and consistent with the severity rating.
5. **Correction SLA tracking**: for `severity = CRITICAL`, the correction SLA is 48 hours from `date_raised`; for `HIGH`, 5 business days. Alert if `correction_actions[*].due_date` exceeds the SLA.
6. **PII escalation**: if `issue_type = PII_LEAKAGE`, immediately trigger the data breach notification workflow and escalate to `[[SECURITY_ENGINEER_SKILL]]` regardless of severity.
