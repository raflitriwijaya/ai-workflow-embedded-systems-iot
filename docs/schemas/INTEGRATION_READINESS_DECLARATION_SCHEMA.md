---
title: "Integration Readiness Declaration Schema"
owning_roles:
  - "Any role pair (both roles must co-sign)"
consuming_roles:
  - "[[QA_TEST_AUTOMATION_ENGINEER_SKILL]]"
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "ARB (Architecture Review Board)"
version: "1.0.0"
tags:
  - schema
  - integration
  - readiness
  - testing
  - machine-parseable
  - gate
---

# Integration Readiness Declaration Schema

## Purpose

An Integration Readiness Declaration (IRD) is a bilateral signed assertion that two roles have completed the agreed test scenarios for their shared interface contract and are ready to proceed to formal integration testing. It replaces informal "done" statements with a machine-verifiable record that QA and the Architect can use as a gate condition. The schema ensures no integration phase begins without both roles attesting to their pre-integration obligations.

**Standards referenced:** IEEE 829:2008 (Software Test Documentation), IEC 62443-4-1 §SVV-3 (Integration Testing Requirements).

---

## YAML Schema Definition

```yaml
# Integration Readiness Declaration Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) IRD-NNNN format, e.g. "IRD-0031"
date_declared: date                # (required) ISO 8601 — date both signatories signed
sprint_or_milestone: string        # (required) e.g. "Sprint-12" or "Milestone-M3"

# ── Contract Under Test ───────────────────────────────────────────────────────
contract:
  contract_id: string              # (required) e.g. "FW↔ARCH-001"
  contract_title: string           # (required) human-readable title
  contract_version: string         # (required) semantic version being validated
  open_ccrs: list[string]          # (required) list of open CCR IDs; must be empty for gate PASS
                                   # (agent checks this list against CCR registry)

# ── Roles ─────────────────────────────────────────────────────────────────────
producer_role: string              # (required) Obsidian wikilink
consumer_role: string              # (required) Obsidian wikilink

# ── Gate Outcome ──────────────────────────────────────────────────────────────
gate_result:                       # (required) enum — computed from scenario results
  type: string
  allowed_values:
    - PASS            # All mandatory scenarios pass; no BLOCKING CCRs
    - PASS_WITH_WAIVER # Some non-blocking failures; waiver signed by Architect
    - FAIL            # One or more mandatory scenarios failed
    - INCOMPLETE      # Not all scenarios executed

# ── Test Scenarios ────────────────────────────────────────────────────────────
test_scenarios:                    # (required) list — at least 1 mandatory scenario
  - id: string                     # (required) e.g. "TS-001"
    description: string            # (required) ≥20 chars — what is being tested
    scenario_type: string          # (required) enum: HAPPY_PATH | BOUNDARY | ERROR | SECURITY | PERFORMANCE
    mandatory: boolean             # (required) true = gate fail if this scenario fails
    executed: boolean              # (required) true = scenario was run
    result: string                 # (required when executed = true) enum: PASS | FAIL | SKIP
    failure_details: string        # (required when result = FAIL) ≥20 chars
    linked_test_case: string       # (optional) test case ID in test management system
    evidence_artifact: string      # (optional) path or URI to test evidence (log, screenshot)

# ── Waivers ───────────────────────────────────────────────────────────────────
waivers:                           # (optional) list — only when gate_result = PASS_WITH_WAIVER
  - scenario_id: string            # (required) references test_scenarios[*].id
    waiver_reason: string          # (required) ≥30 chars — justification
    risk_accepted_by: string       # (required) Obsidian wikilink — must be Architect or ARB
    waiver_expiry: date            # (required) ISO 8601 — waiver expires and must be re-evaluated
    linked_issue: string           # (optional) issue tracker reference

# ── Environment ───────────────────────────────────────────────────────────────
test_environment:
  environment_name: string         # (required) e.g. "staging-v2" or "HIL-bench-3"
  environment_type: string         # (required) enum: SIMULATION | HIL | STAGING | PRODUCTION_SHADOW
  firmware_version: string         # (optional) firmware build under test
  software_build: string           # (optional) software build hash or tag
  hardware_revision: string        # (optional) PCB/sensor hardware revision

# ── Metrics ───────────────────────────────────────────────────────────────────
metrics:
  total_scenarios: integer         # (required) total in test_scenarios list
  executed_scenarios: integer      # (required) count where executed = true
  passed_scenarios: integer        # (required) count where result = PASS
  failed_scenarios: integer        # (required) count where result = FAIL
  skipped_scenarios: integer       # (required) count where result = SKIP
  execution_duration_minutes: number # (optional)

# ── Signatories ───────────────────────────────────────────────────────────────
signatories:                       # (required) both producer and consumer must sign
  - role: string                   # (required) Obsidian wikilink
    name: string                   # (optional)
    signed: boolean                # (required)
    date: date                     # (required when signed = true) ISO 8601
    attestation: string            # (required) enum: READY | NOT_READY | READY_WITH_CONDITIONS

architect_review:                  # (required when gate_result = PASS_WITH_WAIVER or FAIL)
  role: string                     # "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  name: string
  reviewed: boolean
  date: date
  decision: string                 # enum: APPROVED | REJECTED | DEFERRED

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "IRD-0018"
date_declared: "2026-05-22"
sprint_or_milestone: "Sprint-14"

contract:
  contract_id: "FW↔CLOUD-MQTT-001"
  contract_title: "Firmware to Cloud MQTT Telemetry Contract"
  contract_version: "2.2.0"
  open_ccrs: []

producer_role: "[[FIRMWARE_ENGINEER_SKILL]]"
consumer_role: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"

gate_result: PASS

test_scenarios:
  - id: "TS-001"
    description: "Valid telemetry payload delivered and acknowledged within 500 ms"
    scenario_type: HAPPY_PATH
    mandatory: true
    executed: true
    result: PASS
    failure_details: null
    linked_test_case: "TC-FW-CLOUD-001"
    evidence_artifact: "docs/test-evidence/ird-0018/ts-001-pass.log"

  - id: "TS-002"
    description: "Payload rejected with MQTT reason 0x83 when clock skew > 5 s"
    scenario_type: ERROR
    mandatory: true
    executed: true
    result: PASS
    failure_details: null
    linked_test_case: "TC-FW-CLOUD-002"
    evidence_artifact: "docs/test-evidence/ird-0018/ts-002-pass.log"

  - id: "TS-003"
    description: "TLS handshake succeeds with mutual X.509 certificates (ADR-0007)"
    scenario_type: SECURITY
    mandatory: true
    executed: true
    result: PASS
    failure_details: null
    linked_test_case: "TC-FW-CLOUD-003"
    evidence_artifact: "docs/test-evidence/ird-0018/ts-003-tls-handshake.pcap"

  - id: "TS-004"
    description: "Sustained 100 msg/s for 30 minutes without message loss"
    scenario_type: PERFORMANCE
    mandatory: true
    executed: true
    result: PASS
    failure_details: null
    linked_test_case: "TC-FW-CLOUD-004"
    evidence_artifact: "docs/test-evidence/ird-0018/ts-004-perf-report.json"

  - id: "TS-005"
    description: "Reconnect and resume delivery within 10 s after broker restart"
    scenario_type: ERROR
    mandatory: false
    executed: true
    result: PASS
    failure_details: null
    linked_test_case: "TC-FW-CLOUD-005"
    evidence_artifact: null

waivers: []

test_environment:
  environment_name: "staging-v3"
  environment_type: STAGING
  firmware_version: "fw-2.4.1-rc3"
  software_build: "cloud-backend-a3f91c2"
  hardware_revision: "PCB-Rev-C"

metrics:
  total_scenarios: 5
  executed_scenarios: 5
  passed_scenarios: 5
  failed_scenarios: 0
  skipped_scenarios: 0
  execution_duration_minutes: 47.3

signatories:
  - role: "[[FIRMWARE_ENGINEER_SKILL]]"
    name: "Budi Santoso"
    signed: true
    date: "2026-05-22"
    attestation: READY
  - role: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"
    name: "Dewi Rahayu"
    signed: true
    date: "2026-05-22"
    attestation: READY

architect_review:
  role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  name: "Siti Nurhaliza"
  reviewed: false
  date: null
  decision: null

tags:
  - ird-pass
  - sprint-14
  - mqtt
  - firmware
  - cloud

notes: "All 5 scenarios passed. Gate cleared for Sprint-15 integration phase."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-IRD-01 | `id` matches regex `^IRD-\d{4}$` |
| V-IRD-02 | `contract.contract_id` resolves in the contract registry |
| V-IRD-03 | `contract.open_ccrs` list is empty for `gate_result = PASS` |
| V-IRD-04 | `gate_result` is one of the 4 allowed enum values |
| V-IRD-05 | `gate_result = PASS` implies `failed_scenarios = 0` and all mandatory scenarios have `result = PASS` |
| V-IRD-06 | `gate_result = FAIL` implies at least one mandatory scenario has `result = FAIL` |
| V-IRD-07 | `gate_result = PASS_WITH_WAIVER` implies `waivers` list is non-empty |
| V-IRD-08 | Each entry in `waivers[*].scenario_id` must match an existing `test_scenarios[*].id` |
| V-IRD-09 | `signatories` must include entries for both `producer_role` and `consumer_role` with `signed = true` |
| V-IRD-10 | `metrics.passed + metrics.failed + metrics.skipped = metrics.executed_scenarios` |
| V-IRD-11 | If `gate_result ∈ {FAIL, PASS_WITH_WAIVER}`, `architect_review.reviewed = true` required before proceeding |
| V-IRD-12 | `signatories[*].attestation` ∈ {READY, NOT_READY, READY_WITH_CONDITIONS} |
| V-IRD-13 | `test_scenarios` must contain at least 1 entry with `scenario_type = SECURITY` per IEC 62443-4-1 §SVV-3 |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Gate enforcement**: before advancing to formal integration testing, verify this IRD exists for the target contract, has `gate_result = PASS` or `PASS_WITH_WAIVER`, and both `signatories` have `signed = true`.
2. **CCR pre-check**: fetch all CCRs where `contract_reference.contract_id` matches and `severity = BLOCKING` and `status ∉ {RESOLVED, CLOSED, WONTFIX}`; populate `open_ccrs` automatically and fail the gate if non-empty.
3. **Metrics consistency**: verify all metric counts are arithmetically consistent with the scenario list.
4. **Waiver expiry**: scan all `PASS_WITH_WAIVER` IRDs; flag any where `waivers[*].waiver_expiry` has passed and `status` is still `PASS_WITH_WAIVER` — re-evaluation is mandatory.
5. **Evidence artifact reachability**: verify each non-null `evidence_artifact` path resolves to an existing file in the repository or artifact store.
6. **Security scenario mandatory**: warn if no scenario with `scenario_type = SECURITY` exists — IEC 62443-4-1 §SVV-3 compliance requires at least one security validation scenario per interface.
