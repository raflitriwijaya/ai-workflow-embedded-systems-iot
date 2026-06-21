---
title: "CCR Schema — Contract Clarification Record"
owning_roles:
  - "Any role pair (initiating side raises the CCR)"
consuming_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "ARB (Architecture Review Board)"
  - "Both roles named in the contract reference"
version: "1.0.0"
tags:
  - schema
  - ccr
  - contract
  - interface
  - machine-parseable
  - governance
---

# CCR Schema — Contract Clarification Record

## Purpose

A Contract Clarification Record (CCR) documents a discovered ambiguity, gap, or conflict in an inter-role interface contract. It captures the ambiguity precisely, proposes a clarification, and records the agreed resolution along with signatories. The machine-parseable schema enables AI agents to detect unresolved CCRs before integration gating, ensure signatory completeness, and feed resolutions back into the living contract.

**Standards referenced:** IEEE 29148:2018 (Requirements Engineering), IEC 62443-4-1 §SR-2 (Secure Development Process).

---

## YAML Schema Definition

```yaml
# CCR Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) CCR-NNNN format, e.g. "CCR-0015"
date_raised: date                  # (required) ISO 8601
date_resolved: date                # (optional) ISO 8601 — null until status = RESOLVED

# ── Contract Reference ────────────────────────────────────────────────────────
contract_reference:
  contract_id: string              # (required) e.g. "FW↔ARCH-001" — matches CONTRACT_REGISTRY key
  contract_title: string           # (required) human-readable contract name
  section_reference: string        # (required) e.g. "§3.2 — Timing Constraints"
  contract_version: string         # (required) semantic version of the contract being clarified

# ── Roles ─────────────────────────────────────────────────────────────────────
producer_role: string              # (required) Obsidian wikilink — role producing the artifact under the contract
consumer_role: string              # (required) Obsidian wikilink — role consuming the artifact
raised_by: string                  # (required) Obsidian wikilink — which role raised this CCR

# ── Classification ────────────────────────────────────────────────────────────
ambiguity_class:                   # (required) enum
  type: string
  allowed_values:
    - MISSING_FIELD        # Contract omits a field that is needed at integration
    - CONFLICTING_VALUES   # Two fields or two contracts specify contradictory values
    - UNCLEAR_SEMANTICS    # Field exists but its meaning or units are ambiguous
    - MISSING_CONSTRAINT   # No bound specified where one is required (timing, size, rate)
    - SCOPE_BOUNDARY       # Unclear which role owns a behaviour or data element

severity:                          # (required) enum — impact on integration if unresolved
  type: string
  allowed_values:
    - BLOCKING    # Integration cannot proceed without resolution
    - HIGH        # Integration can be stubbed but not validated
    - MEDIUM      # Workaround exists; resolution needed before release
    - LOW         # Cosmetic or documentation inconsistency only

status:                            # (required) enum
  type: string
  allowed_values:
    - OPEN        # CCR raised, not yet reviewed
    - IN_REVIEW   # Under ARB or bilateral discussion
    - RESOLVED    # Agreed resolution recorded; contract update pending
    - CLOSED      # Contract updated, CCR retired
    - WONTFIX     # Accepted as-is after deliberation

# ── Ambiguity Description ─────────────────────────────────────────────────────
ambiguity_description: string      # (required) ≥50 chars — precise description of what is ambiguous
impact_if_unresolved: string       # (required) ≥30 chars — what breaks or becomes unsafe

# ── Clarification ─────────────────────────────────────────────────────────────
proposed_clarification: string     # (required) ≥30 chars — the initiating role's proposed resolution
proposed_by: string                # (required) Obsidian wikilink — role proposing the clarification

# ── Resolution ────────────────────────────────────────────────────────────────
resolution:                        # (required when status = RESOLVED or CLOSED)
  agreed_clarification: string     # (required) final agreed text ≥30 chars
  resolution_type: string          # (required) enum: CONTRACT_UPDATE | ADR_REQUIRED | PROCESS_CHANGE | ACCEPTED_AMBIGUITY
  contract_update_required: boolean # (required) true if contract text must change
  adr_required: boolean            # (required) true if an ADR must be raised as a result
  linked_adr: string               # (optional) ADR-NNNN — only when adr_required = true

# ── Signatories ───────────────────────────────────────────────────────────────
signatories:                       # (required) list — both roles in contract must sign for CLOSED status
  - role: string                   # (required) Obsidian wikilink
    name: string                   # (optional) human name
    signed: boolean                # (required)
    date: date                     # (required when signed = true) ISO 8601

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]                 # (optional) kebab-case
notes: string                      # (optional) free text
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "CCR-0012"
date_raised: "2026-05-03"
date_resolved: "2026-05-09"

contract_reference:
  contract_id: "FW↔CLOUD-MQTT-001"
  contract_title: "Firmware to Cloud MQTT Telemetry Contract"
  section_reference: "§4.1 — Message Payload Schema"
  contract_version: "2.1.0"

producer_role: "[[FIRMWARE_ENGINEER_SKILL]]"
consumer_role: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"
raised_by: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"

ambiguity_class: MISSING_CONSTRAINT
severity: BLOCKING

status: CLOSED

ambiguity_description: >
  Section §4.1 specifies that the `timestamp` field carries "device local time" but does not
  specify whether this is Unix epoch (seconds or milliseconds), ISO 8601 string, or NTP-synced
  UTC. The cloud ingestion pipeline rejects payloads that are not Unix epoch milliseconds, causing
  100% of current firmware prototypes to fail integration smoke tests.

impact_if_unresolved: >
  Cloud time-series ingestion is blocked. All telemetry dashboards show "no data". Sprint 7
  integration gate cannot be passed.

proposed_clarification: >
  Specify that `timestamp` MUST be a 64-bit unsigned integer representing Unix epoch time in
  milliseconds (UTC), NTP-synchronised to within ±500 ms. Firmware must include NTP sync on
  boot and surface sync-failure as a device health metric.

proposed_by: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"

resolution:
  agreed_clarification: >
    `timestamp` is a uint64 Unix epoch milliseconds (UTC). Devices must synchronise via NTP
    before publishing; NTP sync status exposed in the device shadow as `ntp_synced: boolean`.
    Clock skew > 5 s causes the broker to reject the message with MQTT reason code 0x83.
  resolution_type: CONTRACT_UPDATE
  contract_update_required: true
  adr_required: false
  linked_adr: null

signatories:
  - role: "[[FIRMWARE_ENGINEER_SKILL]]"
    name: "Budi Santoso"
    signed: true
    date: "2026-05-09"
  - role: "[[BACKEND_CLOUD_ENGINEER_SKILL]]"
    name: "Dewi Rahayu"
    signed: true
    date: "2026-05-08"
  - role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
    name: "Siti Nurhaliza"
    signed: true
    date: "2026-05-09"

tags:
  - ccr-closed
  - mqtt
  - timestamp
  - firmware
  - cloud

notes: "Contract v2.2.0 issued 2026-05-11 incorporating this resolution. CCR archived."
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-CCR-01 | `id` matches regex `^CCR-\d{4}$` |
| V-CCR-02 | `contract_reference.contract_id` matches an entry in `docs/contracts/CONTRACT_REGISTRY` |
| V-CCR-03 | `ambiguity_class` is one of the 5 allowed enum values |
| V-CCR-04 | `severity` is one of the 4 allowed enum values |
| V-CCR-05 | `status` is one of the 5 allowed enum values |
| V-CCR-06 | If `status ∈ {RESOLVED, CLOSED}`, `resolution` block must be fully populated |
| V-CCR-07 | If `status = CLOSED`, `signatories` must include entries for both `producer_role` and `consumer_role` with `signed = true` |
| V-CCR-08 | If `resolution.adr_required = true`, `resolution.linked_adr` must be non-null and match `^ADR-\d{4}$` |
| V-CCR-09 | If `resolution.contract_update_required = true`, the contract registry must show a version > `contract_reference.contract_version` within 10 business days of `date_resolved` |
| V-CCR-10 | `date_raised` ≤ `date_resolved` (when both present) |
| V-CCR-11 | `severity = BLOCKING` implies integration gate is held until `status ∈ {RESOLVED, CLOSED, WONTFIX}` |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Scan all open CCRs** before any integration readiness gate: if any `severity = BLOCKING` CCR references the contract under test and `status = OPEN` or `IN_REVIEW`, the gate must fail automatically.
2. **Validate contract cross-reference**: resolve `contract_id` against the contract registry YAML and confirm the `section_reference` string appears in the contract body.
3. **Signatory completeness check**: for `status = CLOSED`, verify that the wikilinks in `signatories[*].role` include at minimum `producer_role` and `consumer_role`.
4. **Contract update tracking**: when `contract_update_required = true` and `status = RESOLVED`, set a 10-business-day deadline timer; if the contract version has not incremented by then, escalate to `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]`.
5. **ADR linkage**: if `adr_required = true`, verify the `linked_adr` exists in the ADR registry with `status ≠ REJECTED`.
6. **Metrics**: aggregate CCRs per `ambiguity_class` and `contract_id` to identify contracts with systemic quality issues.
