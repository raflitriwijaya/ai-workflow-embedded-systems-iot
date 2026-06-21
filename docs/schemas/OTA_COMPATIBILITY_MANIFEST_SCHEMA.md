---
title: "OTA Compatibility Manifest Schema"
owning_roles:
  - "[[MLOPS_ENGINEER_SKILL]]"
consuming_roles:
  - "[[DEVOPS_PLATFORM_ENGINEER_SKILL]]"
  - "[[FIRMWARE_ENGINEER_SKILL]]"
  - "[[SECURITY_ENGINEER_SKILL]]"
version: "1.0.0"
tags:
  - schema
  - ota
  - model-artifact
  - firmware
  - compatibility
  - machine-parseable
  - security
---

# OTA Compatibility Manifest Schema

## Purpose

An OTA Compatibility Manifest (OCM) accompanies every model artifact published for over-the-air deployment to edge devices. It declares all hardware, firmware, and resource constraints that must be satisfied before the model can be safely deployed. The schema is machine-validatable: the DevOps pipeline and Firmware Engineer toolchain can perform automated pre-deployment checks without human inspection of prose documentation.

**Standards referenced:** NIST SP 800-193 (Platform Firmware Resiliency), IEC 62443-4-2 CR 3.4 (Software and Information Integrity), OTA Alliance Reference Specification v2.0.

---

## YAML Schema Definition

```yaml
# OTA Compatibility Manifest Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Model Identity ────────────────────────────────────────────────────────────
model:
  id: string                       # (required) unique model identifier, e.g. "vibration-anomaly-v3"
  version: string                  # (required) semantic version, e.g. "3.1.2"
  framework: string                # (required) enum: TFLITE | TFLITE_MICRO | ONNX | PYTORCH_MOBILE | CUSTOM
  framework_version: string        # (required) e.g. "2.14.0"
  task_type: string                # (required) enum: CLASSIFICATION | REGRESSION | ANOMALY_DETECTION | OBJECT_DETECTION | SEGMENTATION
  quantization: string             # (required) enum: FLOAT32 | FLOAT16 | INT8 | INT4 | BINARY | NONE
  model_file: string               # (required) filename within the OTA bundle, e.g. "model.tflite"
  sha256_hash: string              # (required) 64-char hex SHA-256 of model_file
  size_bytes: integer              # (required) file size in bytes

# ── Hardware Targeting ────────────────────────────────────────────────────────
target_hardware:                   # (required) list — at least 1 entry
  - hardware_id: string            # (required) canonical hardware ID, e.g. "GW-ESP32S3-Rev-C"
    mcu_family: string             # (required) e.g. "ESP32-S3", "STM32H7", "Cortex-M7"
    architecture: string           # (required) enum: ARM_CORTEX_M | XTENSA_LX7 | RISC_V | x86 | ARM_CORTEX_A
    npu_required: boolean          # (required) true if model requires NPU/DSP acceleration
    npu_family: string             # (optional) e.g. "Edge TPU", "ESP-NN", "CMSIS-NN"
    validated: boolean             # (required) true if model has been validated on this hardware

# ── Firmware Compatibility ────────────────────────────────────────────────────
firmware_compatibility:
  minimum_version: string          # (required) semantic version, e.g. "2.3.0"
  maximum_version: string          # (optional) null means no upper bound
  excluded_versions: list[string]  # (optional) versions with known incompatibility, e.g. ["2.4.0", "2.4.1"]
  required_capabilities:           # (required) list of firmware feature flags that must be enabled
    - string                       # e.g. "TFLITE_MICRO_ENABLED", "OTA_AGENT_V2", "NTP_SYNC"

# ── Resource Budget ───────────────────────────────────────────────────────────
resource_budget:
  tensor_arena_size_bytes: integer # (required) bytes required for TensorFlow Lite tensor arena
  tensor_arena_size_kb: number     # (required) computed: tensor_arena_size_bytes / 1024 (for readability)
  flash_required_bytes: integer    # (required) flash storage required for model file
  flash_budget_bytes: integer      # (required) total flash budget allocated for AI models on target
  flash_budget_utilisation_pct: number # (required) computed: flash_required_bytes / flash_budget_bytes * 100
  ram_peak_bytes: integer          # (required) peak RAM during inference
  ram_budget_bytes: integer        # (required) total RAM budget for inference on target
  ram_budget_utilisation_pct: number # (required) computed: ram_peak_bytes / ram_budget_bytes * 100

flash_budget_check:                # (required) machine-validated field
  result: string                   # (required) enum: PASS | FAIL | WARN
                                   # PASS: utilisation ≤ 80%; WARN: 80–95%; FAIL: > 95%
  margin_bytes: integer            # (required) flash_budget_bytes - flash_required_bytes

ram_budget_check:                  # (required)
  result: string                   # enum: PASS | FAIL | WARN
  margin_bytes: integer

# ── Performance Benchmarks ────────────────────────────────────────────────────
performance:
  inference_latency_ms:            # (required)
    mean: number                   # mean inference time in ms
    p95: number                    # 95th percentile
    p99: number                    # 99th percentile
    measured_on: string            # hardware_id on which benchmark was run
  throughput_inferences_per_second: number # (optional)
  accuracy_metric:                 # (required)
    metric_name: string            # e.g. "F1-Score", "mAP@0.5", "AUC-ROC"
    value: number                  # 0.0–1.0 for ratios, absolute for others
    test_dataset_version: string   # dataset version used for benchmark
  model_size_after_quantization_kb: number # (optional)

# ── Security ──────────────────────────────────────────────────────────────────
security:
  signing_key_id: string           # (required) key ID used to sign the model bundle
  signature_algorithm: string      # (required) e.g. "ED25519", "ECDSA-P256"
  bundle_signature: string         # (required) base64-encoded signature of the complete OTA bundle
  secure_boot_required: boolean    # (required) must match device secure boot policy
  encrypted_at_rest: boolean       # (required)
  encryption_algorithm: string     # (required when encrypted_at_rest = true) e.g. "AES-256-GCM"
  sbom_reference: string           # (optional) URI or path to Software Bill of Materials

# ── Deployment Policy ─────────────────────────────────────────────────────────
deployment:
  rollout_strategy: string         # (required) enum: CANARY | BLUE_GREEN | ROLLING | IMMEDIATE
  canary_percentage: integer       # (required when rollout_strategy = CANARY) 1–100
  rollback_trigger:                # (required) conditions that trigger automatic rollback
    max_inference_error_rate_pct: number # rollback if error rate exceeds this % post-deploy
    max_latency_regression_ms: number    # rollback if p95 latency increases by more than this
  deployment_window:               # (optional) allowed deployment time window
    start_utc: string              # e.g. "02:00"
    end_utc: string                # e.g. "04:00"
  requires_maintenance_mode: boolean # (required) true if device must be offline during update

# ── Bundle Contents ───────────────────────────────────────────────────────────
bundle_contents:                   # (required) complete manifest of files in the OTA bundle
  - filename: string               # (required)
    sha256_hash: string            # (required) 64-char hex
    size_bytes: integer            # (required)
    purpose: string                # (required) e.g. "inference-model", "config", "label-map"

# ── Traceability ──────────────────────────────────────────────────────────────
produced_by:
  role: string                     # (required) "[[MLOPS_ENGINEER_SKILL]]"
  name: string                     # (optional)
  date: date                       # (required) ISO 8601

training_run_id: string            # (required) MLOps training run that produced this model
dqir_clearance: list[string]       # (required) list of DQIR IDs cleared before training; empty = no issues

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

model:
  id: "vibration-anomaly-v3"
  version: "3.1.2"
  framework: TFLITE_MICRO
  framework_version: "2.14.0"
  task_type: ANOMALY_DETECTION
  quantization: INT8
  model_file: "vibration_anomaly_v3_int8.tflite"
  sha256_hash: "a3f9c2e1b4d07f8a5c6e91234abcd5678ef012345678abcdef9012345678abcd"
  size_bytes: 186368

target_hardware:
  - hardware_id: "GW-ESP32S3-Rev-C"
    mcu_family: "ESP32-S3"
    architecture: XTENSA_LX7
    npu_required: false
    npu_family: "ESP-NN"
    validated: true
  - hardware_id: "GW-STM32H7-Rev-B"
    mcu_family: "STM32H7"
    architecture: ARM_CORTEX_M
    npu_required: false
    npu_family: "CMSIS-NN"
    validated: true

firmware_compatibility:
  minimum_version: "2.4.2"
  maximum_version: null
  excluded_versions:
    - "2.4.0"
    - "2.4.1"
  required_capabilities:
    - "TFLITE_MICRO_ENABLED"
    - "OTA_AGENT_V2"
    - "NTP_SYNC"
    - "SECURE_BOOT"

resource_budget:
  tensor_arena_size_bytes: 204800
  tensor_arena_size_kb: 200.0
  flash_required_bytes: 186368
  flash_budget_bytes: 524288
  flash_budget_utilisation_pct: 35.6
  ram_peak_bytes: 204800
  ram_budget_bytes: 327680
  ram_budget_utilisation_pct: 62.5

flash_budget_check:
  result: PASS
  margin_bytes: 337920

ram_budget_check:
  result: PASS
  margin_bytes: 122880

performance:
  inference_latency_ms:
    mean: 18.4
    p95: 23.1
    p99: 28.7
    measured_on: "GW-ESP32S3-Rev-C"
  throughput_inferences_per_second: 43.2
  accuracy_metric:
    metric_name: "AUC-ROC"
    value: 0.967
    test_dataset_version: "vibration-edge-v4-clean-1.0"
  model_size_after_quantization_kb: 182.0

security:
  signing_key_id: "mlops-signing-key-2026-q2"
  signature_algorithm: "ED25519"
  bundle_signature: "base64encodedED25519signatureofbundlecontents=="
  secure_boot_required: true
  encrypted_at_rest: true
  encryption_algorithm: "AES-256-GCM"
  sbom_reference: "docs/sbom/vibration-anomaly-v3-1-2.spdx.json"

deployment:
  rollout_strategy: CANARY
  canary_percentage: 5
  rollback_trigger:
    max_inference_error_rate_pct: 2.0
    max_latency_regression_ms: 10.0
  deployment_window:
    start_utc: "02:00"
    end_utc: "05:00"
  requires_maintenance_mode: false

bundle_contents:
  - filename: "vibration_anomaly_v3_int8.tflite"
    sha256_hash: "a3f9c2e1b4d07f8a5c6e91234abcd5678ef012345678abcdef9012345678abcd"
    size_bytes: 186368
    purpose: "inference-model"
  - filename: "model_config.json"
    sha256_hash: "b2e8d1c0a3f6e9b4c7d012345abcde6789f012345678abcdef9012345678bcde"
    size_bytes: 2048
    purpose: "inference-config"
  - filename: "anomaly_labels.txt"
    sha256_hash: "c1d7c0b9a2e5d8c3b6a012345abcde5678e012345678abcdef9012345678cdef"
    size_bytes: 512
    purpose: "label-map"

produced_by:
  role: "[[MLOPS_ENGINEER_SKILL]]"
  name: "Ahmad Fauzi"
  date: "2026-05-28"

training_run_id: "mlflow-run-4f8a2c1e"
dqir_clearance:
  - "DQIR-0008"

tags:
  - ota-manifest
  - tflite-micro
  - anomaly-detection
  - esp32s3
  - int8
  - canary

notes: "DQIR-0008 was closed 2026-05-27 with corrected dataset v4-clean-1.0 before this training run."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-OCM-01 | `model.sha256_hash` is 64 hex characters |
| V-OCM-02 | `model.framework` is one of the 5 allowed enum values |
| V-OCM-03 | `model.quantization` is one of the 6 allowed enum values |
| V-OCM-04 | `target_hardware` has ≥ 1 entry with `validated = true` |
| V-OCM-05 | `flash_budget_utilisation_pct` = `flash_required_bytes` / `flash_budget_bytes` × 100 (±0.1%) |
| V-OCM-06 | `ram_budget_utilisation_pct` = `ram_peak_bytes` / `ram_budget_bytes` × 100 (±0.1%) |
| V-OCM-07 | `flash_budget_check.result = PASS` iff `flash_budget_utilisation_pct` ≤ 80 |
| V-OCM-08 | `flash_budget_check.result = WARN` iff 80 < `flash_budget_utilisation_pct` ≤ 95 |
| V-OCM-09 | `flash_budget_check.result = FAIL` iff `flash_budget_utilisation_pct` > 95 |
| V-OCM-10 | `flash_budget_check.margin_bytes` = `flash_budget_bytes` − `flash_required_bytes` |
| V-OCM-11 | Each `bundle_contents[*].sha256_hash` is 64 hex characters |
| V-OCM-12 | `security.bundle_signature` is non-empty |
| V-OCM-13 | `deployment.canary_percentage` ∈ [1, 100] when `rollout_strategy = CANARY` |
| V-OCM-14 | If `flash_budget_check.result = FAIL`, deployment is blocked — human approval required |
| V-OCM-15 | `dqir_clearance` list IDs must exist in DQIR registry with `correction_status ∈ {CORRECTED, ACCEPTED}` |
| V-OCM-16 | `firmware_compatibility.minimum_version` must be ≤ any version in `excluded_versions` (exclusion must lie within the compat range) |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Hash verification**: re-compute SHA-256 of `model.model_file` and compare against `model.sha256_hash`; fail the deployment if mismatch.
2. **Budget arithmetic**: independently compute `flash_budget_utilisation_pct` and `ram_budget_utilisation_pct` from raw byte values; compare with stated values.
3. **Budget gate**: if `flash_budget_check.result = FAIL` or `ram_budget_check.result = FAIL`, block OTA dispatch and notify `[[MLOPS_ENGINEER_SKILL]]` and `[[FIRMWARE_ENGINEER_SKILL]]`.
4. **Firmware version check**: query the device fleet management API for target device firmware versions; reject deployment to any device running a version in `excluded_versions` or below `minimum_version`.
5. **Capability flag check**: verify each `required_capabilities` flag is set in the device's firmware capability manifest before dispatch.
6. **Signature verification**: verify `security.bundle_signature` using `security.signing_key_id` from the key management service before deploying.
7. **DQIR clearance**: resolve each ID in `dqir_clearance` against the DQIR registry; block deployment if any referenced DQIR has `correction_status ∈ {PENDING, IN_PROGRESS}`.
8. **Rollback monitor**: post-deployment, continuously check inference error rate and p95 latency against `rollback_trigger` thresholds; automatically initiate rollback if thresholds are breached.
