---
title: "Technology Transfer Pack Schema"
owning_roles:
  - "[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]]"
consuming_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "[[SECURITY_ENGINEER_SKILL]]"
version: "1.0.0"
tags:
  - schema
  - technology-transfer
  - research
  - architecture
  - machine-parseable
  - governance
---

# Technology Transfer Pack Schema

## Purpose

A Technology Transfer Pack (TTP) is produced by the IoT/Embedded Systems Researcher when a research output — a new algorithm, hardware component, communication protocol, or ML technique — is deemed ready for integration into the production system. It provides the Architect with a structured briefing: what was validated, what the architecture impact is, what the security posture is, and what resources are required. The schema enables automated readiness gating and prevents premature technology adoption.

**Standards referenced:** ISO/IEC 16085:2006 (Risk Management — Integration into Lifecycle), NIST SP 800-161 (Supply Chain Risk Management), IEC 62443-4-1 §SR-3 (Security Requirements Review).

---

## YAML Schema Definition

```yaml
# Technology Transfer Pack Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) TTP-NNNN format, e.g. "TTP-0004"
date_submitted: date               # (required) ISO 8601
date_approved: date                # (optional) ISO 8601 — filled when status = APPROVED

# ── Technology Description ────────────────────────────────────────────────────
technology:
  name: string                     # (required) short name, e.g. "TinyML Keyword Spotting v2 (DS-CNN)"
  type: string                     # (required) enum: ALGORITHM | HARDWARE_COMPONENT | COMMUNICATION_PROTOCOL |
                                   # ML_MODEL_ARCHITECTURE | FIRMWARE_LIBRARY | SECURITY_PRIMITIVE | TOOLCHAIN
  description: string              # (required) ≥50 chars — what the technology is and what it does
  maturity_level: string           # (required) enum: TRL1 | TRL2 | TRL3 | TRL4 | TRL5 | TRL6 | TRL7
                                   # (Technology Readiness Level per NASA/ESA definition)
  origin: string                   # (required) enum: INTERNAL_RESEARCH | ACADEMIC_PAPER | OPEN_SOURCE |
                                   # VENDOR_SUPPLIED | STANDARDS_BODY
  source_reference: string         # (required) citation — DOI, URL, standard number, or vendor reference
  license: string                  # (required) SPDX license identifier or "PROPRIETARY" or "UNKNOWN"
  license_risk: string             # (required) enum: NONE | LOW | MEDIUM | HIGH
                                   # HIGH = copyleft/GPL risk or no license; review required

# ── Research Summary ──────────────────────────────────────────────────────────
research_summary:
  objective: string                # (required) ≥30 chars — what the research set out to achieve
  methodology: string              # (required) ≥50 chars — how the research was conducted
  key_findings: list[string]       # (required) at least 3 bullet-point findings
  limitations: list[string]        # (required) at least 1 — known constraints or gaps
  open_questions: list[string]     # (optional) unresolved questions for the Architect to consider

# ── Validation Evidence ───────────────────────────────────────────────────────
validation_evidence:
  validated_in_isolation: boolean  # (required) true = tested as standalone unit
  validated_on_target_hardware: boolean # (required) true = tested on production-representative hardware
  target_hardware_id: string       # (required when validated_on_target_hardware = true) hardware ID
  benchmark_results:               # (required) at least 1 entry
    - metric_name: string          # e.g. "Inference latency p95 (ms)", "Keyword detection F1", "Flash usage (KB)"
      value: number
      unit: string
      threshold: number            # acceptance threshold
      threshold_direction: string  # enum: LESS_THAN | GREATER_THAN | EQUAL_TO
      passed: boolean              # computed: value meets threshold
  datasets_used: list[string]      # (required) dataset names/versions used in validation
  test_report_path: string         # (required) path to detailed test report

# ── Architecture Impact Assessment ────────────────────────────────────────────
architecture_impact:
  system_layers_affected: list[string] # (required) enum values from tier list in ADR schema
  contracts_potentially_affected: list[string] # (optional) contract IDs that may need updating
  new_dependencies: list[string]   # (required) new libraries, chips, services introduced (empty list if none)
  replaces_existing: string        # (optional) name of technology being deprecated/replaced
  migration_complexity: string     # (required) enum: NONE | LOW | MEDIUM | HIGH | CRITICAL
  estimated_integration_effort_days: integer # (required) engineering days to integrate
  adr_required: boolean            # (required) true if architectural decision must be formally recorded
  adr_draft_title: string          # (required when adr_required = true) proposed ADR title

# ── Pre-Transfer Security Review ──────────────────────────────────────────────
security_review:
  status: string                   # (required) enum: NOT_STARTED | IN_PROGRESS | COMPLETED | WAIVED
  reviewer:
    role: string                   # (required when status = COMPLETED) "[[SECURITY_ENGINEER_SKILL]]"
    name: string
    date: date
  threat_model_updated: boolean    # (required) true if threat model was updated for this technology
  supply_chain_assessed: boolean   # (required) per NIST SP 800-161
  known_cves: list[string]         # (required) CVE IDs in this technology; empty list if none
  cve_mitigations: list[string]    # (required when known_cves non-empty) mitigation for each CVE
  security_verdict: string         # (required when status = COMPLETED) enum: APPROVED | APPROVED_WITH_CONDITIONS | REJECTED
  security_conditions: list[string] # (optional) conditions when verdict = APPROVED_WITH_CONDITIONS

# ── Resource Estimate ─────────────────────────────────────────────────────────
resource_estimate:
  engineering_days: integer        # (required) integration engineering effort
  hardware_cost_usd: number        # (optional) additional hardware cost (0 if software-only)
  infrastructure_cost_usd_per_month: number # (optional) recurring infrastructure cost
  training_days: integer           # (optional) team training required
  risk_level: string               # (required) enum: LOW | MEDIUM | HIGH — overall integration risk
  risk_justification: string       # (required) ≥30 chars — why this risk level was assigned

# ── Transfer Gate ─────────────────────────────────────────────────────────────
transfer_gate:
  status: string                   # (required) enum: PENDING | APPROVED | REJECTED | DEFERRED
  approved_by:
    role: string                   # (required when status = APPROVED) "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
    name: string
    date: date

# ── Produced By ───────────────────────────────────────────────────────────────
produced_by:
  role: string                     # (required) "[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]]"
  name: string                     # (optional)

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "TTP-0004"
date_submitted: "2026-05-12"
date_approved: null

technology:
  name: "DS-CNN Keyword Spotting TinyML (Wake-Word Detection)"
  type: ALGORITHM
  description: >
    A depthwise separable convolutional neural network (DS-CNN) architecture optimised for
    keyword spotting on microcontrollers. Detects a configurable wake word from raw MFCC
    audio features. Inference runs entirely on-device in <20 ms on Cortex-M4 at 80 MHz,
    enabling always-on, zero-cloud-round-trip wake-word activation.
  maturity_level: TRL5
  origin: ACADEMIC_PAPER
  source_reference: "Zhang et al., 'Hello Edge: Keyword Spotting on Microcontrollers', arXiv:1711.07128"
  license: "Apache-2.0"
  license_risk: NONE

research_summary:
  objective: >
    Determine whether DS-CNN achieves ≥95% keyword detection accuracy within the flash and
    RAM constraints of the GW-STM32H7-Rev-B gateway hardware for always-on wake-word activation.
  methodology: >
    (1) Reproduced DS-CNN architecture in TensorFlow 2.14, trained on Google Speech Commands v2
    dataset + 500 proprietary in-house recordings. (2) Applied INT8 post-training quantization.
    (3) Compiled to TFLite Micro and benchmarked on STM32H7 HIL bench using CMSIS-NN kernels.
    (4) Evaluated false accept rate (FAR) and false reject rate (FRR) over 10,000 test utterances.
  key_findings:
    - "DS-CNN INT8 achieves 96.3% keyword accuracy on Google Speech Commands v2 test set"
    - "Inference latency p95 = 17.8 ms at 80 MHz, comfortably within 20 ms target"
    - "Flash footprint 142 KB with INT8 quantization; within 35% of the 512 KB model budget"
    - "False accept rate 0.12% over 10,000 background noise utterances — meets IEC 62443-4-2 threshold"
    - "CMSIS-NN kernel acceleration provides 4.2× speedup vs. reference implementation"
  limitations:
    - "Accuracy degrades to 91.7% in high-noise environments (SNR < 5 dB); mitigation required"
    - "Only validated on STM32H7; ESP32-S3 porting not yet attempted"
    - "Training data does not include non-English speaker accents; generalization unknown"
  open_questions:
    - "Should noise robustness be addressed with spectral subtraction preprocessing or by extending training data?"
    - "What is the target wake word set — single word or phrase?"

validation_evidence:
  validated_in_isolation: true
  validated_on_target_hardware: true
  target_hardware_id: "GW-STM32H7-Rev-B"
  benchmark_results:
    - metric_name: "Keyword accuracy (%)"
      value: 96.3
      unit: "%"
      threshold: 95.0
      threshold_direction: GREATER_THAN
      passed: true
    - metric_name: "Inference latency p95 (ms)"
      value: 17.8
      unit: "ms"
      threshold: 20.0
      threshold_direction: LESS_THAN
      passed: true
    - metric_name: "Flash footprint (KB)"
      value: 142.0
      unit: "KB"
      threshold: 180.0
      threshold_direction: LESS_THAN
      passed: true
    - metric_name: "Peak RAM (KB)"
      value: 48.0
      unit: "KB"
      threshold: 64.0
      threshold_direction: LESS_THAN
      passed: true
    - metric_name: "False accept rate (%)"
      value: 0.12
      unit: "%"
      threshold: 0.5
      threshold_direction: LESS_THAN
      passed: true
  datasets_used:
    - "google-speech-commands-v2"
    - "proprietary-wake-word-v1"
  test_report_path: "docs/research/ttp-0004/ds-cnn-benchmark-report.pdf"

architecture_impact:
  system_layers_affected:
    - FIRMWARE
    - EDGE-AI
  contracts_potentially_affected:
    - "FW↔ARCH-AI-001"
  new_dependencies:
    - "TensorFlow Lite Micro 2.14 (already in OTA manifest; no new dependency)"
    - "CMSIS-NN 5.9.0 (new; must be added to firmware build)"
  replaces_existing: null
  migration_complexity: LOW
  estimated_integration_effort_days: 8
  adr_required: true
  adr_draft_title: "Adopt DS-CNN INT8 for Always-On Wake-Word Detection on STM32H7"

security_review:
  status: COMPLETED
  reviewer:
    role: "[[SECURITY_ENGINEER_SKILL]]"
    name: "Rizki Permana"
    date: "2026-05-18"
  threat_model_updated: true
  supply_chain_assessed: true
  known_cves: []
  cve_mitigations: []
  security_verdict: APPROVED_WITH_CONDITIONS
  security_conditions:
    - "Model binary must be signed with ED25519 per ADR-0007 before deployment"
    - "Wake-word audio buffer must be zeroed after inference to prevent side-channel data leakage"
    - "FAR must be re-validated after noise robustness mitigation is implemented"

resource_estimate:
  engineering_days: 8
  hardware_cost_usd: 0.0
  infrastructure_cost_usd_per_month: 0.0
  training_days: 1
  risk_level: LOW
  risk_justification: >
    All benchmark targets met on target hardware. Low flash/RAM risk. Single new dependency
    (CMSIS-NN) has established supply chain and Apache-2.0 license. Security review approved
    with tractable conditions.

transfer_gate:
  status: PENDING
  approved_by:
    role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
    name: null
    date: null

produced_by:
  role: "[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]]"
  name: "Ahmad Fauzi"

tags:
  - ttp
  - tinyml
  - keyword-spotting
  - ds-cnn
  - stm32h7
  - pending-approval

notes: "Security conditions SEC-001 and SEC-002 have been acknowledged by Firmware Engineer. ADR draft prepared as ADR-0009 draft."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-TTP-01 | `id` matches regex `^TTP-\d{4}$` |
| V-TTP-02 | `technology.type` is one of the 7 allowed enum values |
| V-TTP-03 | `technology.maturity_level` is one of the 7 TRL values |
| V-TTP-04 | `technology.origin` is one of the 5 allowed enum values |
| V-TTP-05 | `technology.license_risk = HIGH` triggers mandatory legal review before `transfer_gate.status` can be `APPROVED` |
| V-TTP-06 | `research_summary.key_findings` has ≥ 3 entries |
| V-TTP-07 | `research_summary.limitations` has ≥ 1 entry |
| V-TTP-08 | `validation_evidence.benchmark_results` has ≥ 1 entry |
| V-TTP-09 | Each `benchmark_results[*].passed` must be computed consistently with `value`, `threshold`, and `threshold_direction` |
| V-TTP-10 | If `architecture_impact.adr_required = true`, `adr_draft_title` must be non-null |
| V-TTP-11 | `security_review.status` must be `COMPLETED` (not `NOT_STARTED` or `IN_PROGRESS`) for `transfer_gate.status` to be `APPROVED` |
| V-TTP-12 | If `security_review.security_verdict = REJECTED`, `transfer_gate.status` must be `REJECTED` |
| V-TTP-13 | If `known_cves` is non-empty, `cve_mitigations` must have the same number of entries |
| V-TTP-14 | `technology.maturity_level ∈ {TRL5, TRL6, TRL7}` required for `transfer_gate.status = APPROVED` |
| V-TTP-15 | `transfer_gate.approved_by.role = "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"` when `status = APPROVED` |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **TRL gate enforcement**: automatically reject transfer if `technology.maturity_level ∈ {TRL1, TRL2, TRL3, TRL4}` — research is not mature enough for production integration.
2. **Benchmark consistency**: re-evaluate each `benchmark_results[*].passed` by comparing `value` against `threshold` with the correct `threshold_direction`; flag any inconsistency.
3. **Security review prerequisite**: verify `security_review.status = COMPLETED` and `security_verdict ≠ REJECTED` before enabling the Architect's `APPROVED` decision.
4. **License risk escalation**: if `technology.license_risk = HIGH`, route to legal review workflow and block transfer gate until legal clears it.
5. **ADR creation trigger**: if `adr_required = true` and `transfer_gate.status` transitions to `APPROVED`, automatically scaffold a new ADR from `ADR_SCHEMA` with `title = adr_draft_title` and `status = PROPOSED`.
6. **CVE cross-reference**: resolve each CVE ID in `known_cves` against the NVD API to verify severity ratings and confirm `cve_mitigations` are adequate for each severity ≥ HIGH.
7. **Contract impact notification**: for each ID in `contracts_potentially_affected`, notify the contract owner roles (producer and consumer) to review and raise a CCR if needed.
