---
title: "Security Implementation Readiness Schema"
owning_roles:
  - "Each implementing role's Security Champion"
  - "[[FIRMWARE_ENGINEER_SKILL]]"
  - "[[BACKEND_CLOUD_ENGINEER_SKILL]]"
  - "[[DEVOPS_PLATFORM_ENGINEER_SKILL]]"
  - "[[DATA_ENGINEER_SKILL]]"
  - "[[MLOPS_ENGINEER_SKILL]]"
consuming_roles:
  - "[[SECURITY_ENGINEER_SKILL]]"
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
version: "1.0.0"
tags:
  - schema
  - security
  - checklist
  - readiness
  - machine-parseable
  - iec-62443
  - nist
---

# Security Implementation Readiness Schema

## Purpose

A Security Implementation Readiness Checklist (SIRC) is submitted by each implementing role's Security Champion before the Security Engineer conducts a formal security review. It replaces prose checklists with a structured, machine-parseable record where every security control is explicitly confirmed, uncertain, or failed — eliminating the ambiguity of "N/A" and undocumented gaps. The schema enables automated pre-review gating and security control coverage dashboards.

**Standards referenced:** IEC 62443-4-1 (Secure Product Development Lifecycle), IEC 62443-4-2 (Technical Security Requirements), NIST SP 800-53 Rev 5, OWASP IoT Security Verification Standard (ISVS) v1.0.

---

## YAML Schema Definition

```yaml
# Security Implementation Readiness Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) SIRC-ROLE-SPRINT format, e.g. "SIRC-FW-S14"
sprint_or_milestone: string        # (required) e.g. "Sprint-14" or "Milestone-M3"
date_submitted: date               # (required) ISO 8601
date_reviewed: date                # (optional) ISO 8601 — filled by Security Engineer

# ── Submitting Role ───────────────────────────────────────────────────────────
submitting_role: string            # (required) Obsidian wikilink to role SKILL file
security_champion:
  name: string                     # (required) name of the Security Champion for this role
  attestation: string              # (required) literal: "I attest that all CONFIRMED items have been implemented and verified"

# ── Gate Outcome ──────────────────────────────────────────────────────────────
gate_result:                       # (required) enum — computed from checklist items
  type: string
  allowed_values:
    - READY          # All mandatory items CONFIRMED; no FAILED items
    - READY_WITH_CONDITIONS # Mandatory items all CONFIRMED; some UNCERTAIN with accepted risk
    - NOT_READY      # One or more mandatory items FAILED or UNCERTAIN without accepted risk

# ── Checklist Items ───────────────────────────────────────────────────────────
checklist_items:                   # (required) list — defined per-role; all applicable items must be present
  - id: string                     # (required) e.g. "SEC-FW-01"
    category: string               # (required) enum: AUTHENTICATION | AUTHORIZATION | CRYPTOGRAPHY |
                                   # DATA_PROTECTION | INPUT_VALIDATION | LOGGING_MONITORING |
                                   # SECURE_BOOT | OTA_SECURITY | NETWORK_SECURITY | SUPPLY_CHAIN |
                                   # VULNERABILITY_MANAGEMENT | PHYSICAL_SECURITY
    control_reference: string      # (required) standard citation, e.g. "IEC 62443-4-2 CR 1.1" or "NIST SP 800-53 IA-3"
    description: string            # (required) ≥20 chars — what implementation is being attested
    mandatory: boolean             # (required) true = FAILED means gate fails regardless of waivers
    status: string                 # (required) enum: CONFIRMED | UNCERTAIN | FAILED | NOT_APPLICABLE
    evidence: string               # (required when status = CONFIRMED) path/URI to evidence artifact
    uncertainty_reason: string     # (required when status = UNCERTAIN) ≥20 chars — why uncertain
    failure_reason: string         # (required when status = FAILED) ≥20 chars — what is missing/broken
    na_justification: string       # (required when status = NOT_APPLICABLE) ≥20 chars — why not applicable
    risk_accepted: boolean         # (required when status ∈ {UNCERTAIN, FAILED}) true requires Architect sign-off
    risk_acceptance_rationale: string # (required when risk_accepted = true) ≥30 chars

# ── Summary Metrics ───────────────────────────────────────────────────────────
summary:
  total_items: integer             # (required)
  confirmed_count: integer         # (required)
  uncertain_count: integer         # (required)
  failed_count: integer            # (required)
  not_applicable_count: integer    # (required)
  mandatory_items_total: integer   # (required) count of items with mandatory = true
  mandatory_items_confirmed: integer # (required) count where mandatory = true AND status = CONFIRMED
  coverage_pct: number             # (required) confirmed_count / (total_items - not_applicable_count) * 100

# ── Security Engineer Review ──────────────────────────────────────────────────
security_engineer_review:          # (optional) — filled by [[SECURITY_ENGINEER_SKILL]]
  reviewer:
    role: string                   # "[[SECURITY_ENGINEER_SKILL]]"
    name: string
  date: date
  findings:                        # (optional) issues found during review
    - finding_id: string           # e.g. "FINDING-001"
      checklist_item_id: string    # references checklist_items[*].id
      severity: string             # enum: CRITICAL | HIGH | MEDIUM | LOW | INFO
      description: string
      remediation_required: boolean
      remediation_deadline: date
  overall_decision: string         # enum: APPROVED | APPROVED_WITH_CONDITIONS | REJECTED
  conditions: list[string]         # (optional) conditions when overall_decision = APPROVED_WITH_CONDITIONS

# ── Architect Sign-off ────────────────────────────────────────────────────────
architect_signoff:                 # (optional) required when any risk_accepted = true
  role: string                     # "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  name: string
  date: date
  signed: boolean
  accepted_risks: list[string]     # checklist item IDs where risk is accepted

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "SIRC-FW-S14"
sprint_or_milestone: "Sprint-14"
date_submitted: "2026-05-20"
date_reviewed: null

submitting_role: "[[FIRMWARE_ENGINEER_SKILL]]"
security_champion:
  name: "Budi Santoso"
  attestation: "I attest that all CONFIRMED items have been implemented and verified"

gate_result: READY_WITH_CONDITIONS

checklist_items:
  - id: "SEC-FW-01"
    category: SECURE_BOOT
    control_reference: "IEC 62443-4-2 CR 3.4 / NIST SP 800-193 §3.1"
    description: "Secure boot chain verified: bootloader, firmware image, and model artifact all signature-checked before execution"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/test-evidence/secure-boot/fw-s14-secure-boot-test.log"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-02"
    category: CRYPTOGRAPHY
    control_reference: "IEC 62443-4-2 CR 4.3 / NIST SP 800-175B §3"
    description: "All cryptographic operations use approved algorithms: AES-256-GCM for symmetric, ED25519 for signing, no use of MD5/SHA-1/DES"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/review/crypto-audit-fw-s14.md"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-03"
    category: OTA_SECURITY
    control_reference: "IEC 62443-4-2 CR 3.4 / OTA Alliance Ref Spec §6.2"
    description: "OTA update package verified: SHA-256 hash checked, ED25519 signature verified before flashing"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/test-evidence/ota/fw-s14-ota-signature-test.log"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-04"
    category: AUTHENTICATION
    control_reference: "IEC 62443-4-2 CR 1.1 / NIST SP 800-53 IA-3"
    description: "Device authenticates to cloud broker using X.509 client certificate (ADR-0007); no hardcoded credentials in firmware binary"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/test-evidence/auth/fw-s14-mtls-test.log"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-05"
    category: DATA_PROTECTION
    control_reference: "IEC 62443-4-2 CR 4.1 / NIST SP 800-53 SC-28"
    description: "Sensitive data (device credentials, calibration secrets) stored in encrypted NVS partition; encryption key derived from hardware eFuse"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/review/nvs-encryption-review-s14.md"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-06"
    category: LOGGING_MONITORING
    control_reference: "IEC 62443-4-2 CR 2.8 / NIST SP 800-53 AU-2"
    description: "Security-relevant events (boot failure, auth failure, OTA rejection) logged to tamper-evident local ring buffer and forwarded to cloud SIEM"
    mandatory: false
    status: UNCERTAIN
    evidence: null
    uncertainty_reason: "Cloud SIEM integration not yet deployed in staging; local ring buffer implemented and confirmed. SIEM forwarding scheduled for Sprint-15."
    failure_reason: null
    na_justification: null
    risk_accepted: true
    risk_acceptance_rationale: "Local audit log provides interim traceability. SIEM integration is Sprint-15 committed work; risk window is one sprint."

  - id: "SEC-FW-07"
    category: VULNERABILITY_MANAGEMENT
    control_reference: "IEC 62443-4-1 SM-9 / NIST SP 800-53 RA-5"
    description: "Third-party libraries (esp-idf, mbedTLS, tflite-micro) scanned against CVE database; no unmitigated HIGH/CRITICAL CVEs"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/security/sbom/fw-s14-cve-scan-report.html"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

  - id: "SEC-FW-08"
    category: PHYSICAL_SECURITY
    control_reference: "IEC 62443-4-2 CR 3.1"
    description: "JTAG/UART debug interfaces disabled in production firmware build via eFuse burn"
    mandatory: true
    status: CONFIRMED
    evidence: "docs/test-evidence/hw/fw-s14-efuse-burn-log.txt"
    uncertainty_reason: null
    failure_reason: null
    na_justification: null
    risk_accepted: false
    risk_acceptance_rationale: null

summary:
  total_items: 8
  confirmed_count: 7
  uncertain_count: 1
  failed_count: 0
  not_applicable_count: 0
  mandatory_items_total: 7
  mandatory_items_confirmed: 7
  coverage_pct: 87.5

security_engineer_review:
  reviewer:
    role: "[[SECURITY_ENGINEER_SKILL]]"
    name: "Rizki Permana"
  date: null
  findings: []
  overall_decision: null
  conditions: []

architect_signoff:
  role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  name: "Siti Nurhaliza"
  date: "2026-05-21"
  signed: true
  accepted_risks:
    - "SEC-FW-06"

tags:
  - sirc
  - firmware
  - sprint-14
  - ready-with-conditions
  - iec-62443

notes: "SEC-FW-06 accepted risk expires Sprint-15. SIEM integration must be CONFIRMED in SIRC-FW-S15."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-SIRC-01 | `id` matches regex `^SIRC-[A-Z]+-S\d+$` or `^SIRC-[A-Z]+-M\d+$` |
| V-SIRC-02 | `gate_result` is one of the 3 allowed enum values |
| V-SIRC-03 | `gate_result = READY` implies `failed_count = 0` and all items with `mandatory = true` have `status = CONFIRMED` |
| V-SIRC-04 | `gate_result = NOT_READY` implies `failed_count > 0` OR a mandatory item has `status = UNCERTAIN` with `risk_accepted = false` |
| V-SIRC-05 | `status` is one of {CONFIRMED, UNCERTAIN, FAILED, NOT_APPLICABLE} |
| V-SIRC-06 | If `status = CONFIRMED`, `evidence` must be non-null |
| V-SIRC-07 | If `status = UNCERTAIN`, `uncertainty_reason` must be non-null and ≥ 20 chars |
| V-SIRC-08 | If `status = FAILED`, `failure_reason` must be non-null and ≥ 20 chars |
| V-SIRC-09 | If `status = NOT_APPLICABLE`, `na_justification` must be non-null and ≥ 20 chars |
| V-SIRC-10 | If `risk_accepted = true`, `risk_acceptance_rationale` must be non-null and ≥ 30 chars |
| V-SIRC-11 | If any `risk_accepted = true`, `architect_signoff.signed = true` is required |
| V-SIRC-12 | `summary.confirmed + summary.uncertain + summary.failed + summary.not_applicable = summary.total_items` |
| V-SIRC-13 | `coverage_pct` = `confirmed_count` / (`total_items` − `not_applicable_count`) × 100 (±0.1%) |
| V-SIRC-14 | Every mandatory item (`mandatory = true`) must have a `control_reference` citing an IEC 62443, NIST, or OWASP standard |
| V-SIRC-15 | Security Engineer cannot approve (`overall_decision = APPROVED`) if any mandatory item has `status = FAILED` |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Pre-review gate**: before scheduling a Security Engineer review, verify `gate_result ∈ {READY, READY_WITH_CONDITIONS}` and that no mandatory item has `status = FAILED`.
2. **Evidence reachability**: for each item with `status = CONFIRMED`, verify the `evidence` path resolves to an existing file in the repository or artifact store.
3. **Arithmetic consistency**: validate all `summary` counts by iterating `checklist_items` and counting status values; flag any discrepancy.
4. **Risk acceptance chain**: for every item where `risk_accepted = true`, verify `architect_signoff.signed = true` and that the item's `id` appears in `architect_signoff.accepted_risks`.
5. **Control reference validation**: parse `control_reference` strings and verify they cite known standard codes (IEC 62443, NIST SP 800-*, OWASP ISVS).
6. **Sprint-to-sprint continuity**: for items with `status = UNCERTAIN` and `risk_accepted = true`, automatically create a follow-up check in the next sprint's SIRC template to confirm the item is resolved.
7. **Coverage dashboard**: aggregate `coverage_pct` across all SIRCs per sprint to produce a security implementation coverage trend chart for the governance dashboard.
