---
title: "ADR Schema — Architecture Decision Record"
owning_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "Any role (initiator)"
consuming_roles:
  - "All roles"
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "ARB (Architecture Review Board)"
version: "1.0.0"
tags:
  - schema
  - adr
  - architecture
  - machine-parseable
  - governance
---

# ADR Schema — Architecture Decision Record

## Purpose

An Architecture Decision Record (ADR) captures a significant architectural decision made during the project lifecycle. It records the context, options considered, decision rationale, and downstream impact. The machine-parseable schema ensures AI agents can validate completeness, route for approval, detect conflicts with existing decisions, and aggregate decision patterns.

**Standards referenced:** ISO/IEC/IEEE 42010:2011 (Architecture Description), NIST SP 800-160 Vol. 1 (Systems Security Engineering).

---

## YAML Schema Definition

```yaml
# ADR Schema v1.0.0
# All fields marked (required) must be present for a valid instance.
# All fields marked (optional) may be omitted.

schema_version: "1.0.0"           # (required) string — schema version for forward-compatibility

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) ADR-NNNN format, e.g. "ADR-0042"
title: string                      # (required) ≤120 chars, imperative mood, e.g. "Use MQTT over CoAP for telemetry transport"
date_created: date                 # (required) ISO 8601 date, e.g. "2026-03-15"
date_decided: date                 # (optional) ISO 8601 date — null until status = DECIDED
date_superseded: date              # (optional) ISO 8601 date — only when status = SUPERSEDED

# ── Classification ────────────────────────────────────────────────────────────
status:                            # (required) enum
  type: string
  allowed_values:
    - PROPOSED          # Under discussion, not yet decided
    - DECIDED           # Approved by required approvers
    - DEPRECATED        # Still in effect but discouraged
    - SUPERSEDED        # Replaced by another ADR (link required)
    - REJECTED          # Formally rejected after deliberation

decision_class:                    # (required) enum — architectural impact level
  type: string
  allowed_values:
    - STRATEGIC         # Cross-system, multi-wave impact (ARB approval required)
    - TACTICAL          # Within-system, affects ≥2 roles (Lead Architect approval)
    - LOCAL             # Single-role bounded (role-lead approval only)

tier:                              # (required) enum — system layer affected
  type: string
  allowed_values:
    - HARDWARE
    - FIRMWARE
    - EMBEDDED-SOFTWARE
    - EDGE-AI
    - CONNECTIVITY
    - CLOUD-BACKEND
    - DATA-PIPELINE
    - SECURITY
    - DEVOPS
    - CROSS-CUTTING

# ── Ownership ─────────────────────────────────────────────────────────────────
initiator:
  role: string                     # (required) Obsidian wikilink to role SKILL file, e.g. "[[FIRMWARE_ENGINEER_SKILL]]"
  name: string                     # (optional) Human name of initiator

approvers:                         # (required) list — at least 1 entry for status DECIDED
  - role: string                   # (required) Obsidian wikilink to approver role
    name: string                   # (optional) Human name
    approved: boolean              # (required) true = approved, false = rejected
    date: date                     # (required when approved=true) ISO 8601

superseded_by: string              # (optional) ADR-NNNN — only when status = SUPERSEDED
supersedes: string                 # (optional) ADR-NNNN — when this ADR replaces a prior one

# ── Decision Content ──────────────────────────────────────────────────────────
context: string                    # (required) ≥50 chars — situation forcing the decision
problem_statement: string          # (required) ≥30 chars — specific question being resolved

options_considered:                # (required) list — at least 2 entries
  - id: string                     # (required) e.g. "A", "B", "C"
    description: string            # (required) ≥20 chars
    pros: list[string]             # (required) at least 1
    cons: list[string]             # (required) at least 1
    security_implications: string  # (optional) free text
    estimated_effort_days: integer # (optional) non-negative integer

decision: string                   # (required) which option was chosen and why, ≥50 chars
rationale: string                  # (required) ≥50 chars — reasoning beyond the decision text
consequences: string               # (required) ≥30 chars — what changes as a result

# ── Impact Traceability ───────────────────────────────────────────────────────
affected_contracts:                # (optional) list — interface contracts impacted
  - contract_id: string            # e.g. "FW↔ARCH-001"
    impact_description: string

affected_requirements:             # (optional) list — requirement IDs impacted
  - string                         # e.g. "REQ-SEC-042"

linked_adrs:                       # (optional) list — related ADR IDs
  - string                         # e.g. "ADR-0038"

# ── Business Impact ───────────────────────────────────────────────────────────
business_impact_assessment:        # (optional) — populated by [[BUSINESS_CONSULTANT_SKILL]]
  cost_impact:
    delta_usd: number              # negative = saving, positive = added cost
    confidence: string             # allowed: LOW | MEDIUM | HIGH
    notes: string
  schedule_impact_days: integer    # negative = acceleration, positive = delay
  market_impact: string            # free text ≤500 chars
  recommendation: string           # allowed: PROCEED | PROCEED_WITH_MITIGATION | REJECT

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]                 # (optional) kebab-case tags for Obsidian navigation
notes: string                      # (optional) free text — reviewer notes
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "ADR-0007"
title: "Use TLS 1.3 mutual authentication for all Edge-to-Cloud MQTT connections"
date_created: "2026-04-10"
date_decided: "2026-04-18"
date_superseded: null

status: DECIDED
decision_class: STRATEGIC
tier: SECURITY

initiator:
  role: "[[SECURITY_ENGINEER_SKILL]]"
  name: "Rafli Triwijaya"

approvers:
  - role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
    name: "Siti Nurhaliza"
    approved: true
    date: "2026-04-18"
  - role: "[[FIRMWARE_ENGINEER_SKILL]]"
    name: "Budi Santoso"
    approved: true
    date: "2026-04-17"

superseded_by: null
supersedes: "ADR-0003"

context: >
  The platform currently uses TLS 1.2 with server-only authentication. A penetration test
  (PT-2026-Q1) identified that device impersonation is feasible without mutual auth. The
  fleet is scaling to 50,000 devices, making this a high-priority hardening action.

problem_statement: >
  Which TLS version and authentication mode should be mandated for MQTT connections
  between edge gateways and the cloud broker to prevent device impersonation attacks?

options_considered:
  - id: "A"
    description: "Retain TLS 1.2 server-only authentication with stronger cipher suites"
    pros:
      - "No firmware changes required"
      - "Lowest implementation cost"
    cons:
      - "Does not address device impersonation vector"
      - "TLS 1.2 deprecated by NIST SP 800-52 Rev 2"
    security_implications: "Leaves CVE-identified attack vector open"
    estimated_effort_days: 2

  - id: "B"
    description: "Upgrade to TLS 1.3 with mutual X.509 certificate authentication"
    pros:
      - "Eliminates device impersonation"
      - "Aligns with IEC 62443-4-2 CL2 requirements"
      - "Forward secrecy guaranteed"
    cons:
      - "Firmware flash budget increases ~12 KB for mbedTLS upgrade"
      - "PKI provisioning pipeline required"
    security_implications: "Full mutual auth; certificate revocation via OCSP stapling"
    estimated_effort_days: 21

  - id: "C"
    description: "Use pre-shared keys (PSK) with TLS 1.3"
    pros:
      - "Simpler key management than X.509"
    cons:
      - "PSK rotation at fleet scale is operationally complex"
      - "No non-repudiation"
    security_implications: "Weaker identity assurance than certificate-based"
    estimated_effort_days: 14

decision: >
  Option B — TLS 1.3 with mutual X.509 authentication — is adopted. The security risk of
  device impersonation at 50K-device scale outweighs the firmware flash overhead.

rationale: >
  IEC 62443-4-2 CL2 mandates mutual authentication for industrial IoT control-plane
  communications. The PKI provisioning pipeline is already being built for OTA signing
  (ADR-0006), creating a shared infrastructure that amortizes the cost of Option B.

consequences: >
  Firmware Engineer must upgrade mbedTLS to 3.x; flash budget must be re-validated.
  DevOps must deploy an MQTT broker with mTLS support (Mosquitto 2.x or EMQX).
  All new devices provisioned via the PKI pipeline before first connection.

affected_contracts:
  - contract_id: "FW↔CLOUD-MQTT-001"
    impact_description: "TLS version and auth mode fields must be updated to mTLS 1.3"
  - contract_id: "SEC↔DEVOPS-PKI-001"
    impact_description: "Certificate provisioning SLA added to contract"

affected_requirements:
  - "REQ-SEC-014"
  - "REQ-CONN-007"

linked_adrs:
  - "ADR-0003"
  - "ADR-0006"

business_impact_assessment:
  cost_impact:
    delta_usd: 18500
    confidence: MEDIUM
    notes: "PKI infra capex + 21 dev-days; offset by avoided breach cost estimate $2.1M"
  schedule_impact_days: 14
  market_impact: "IEC 62443 compliance enables entry into EU industrial IoT procurement"
  recommendation: PROCEED

tags:
  - security
  - tls
  - mqtt
  - firmware
  - adr-decided

notes: "PT-2026-Q1 report attached in [[docs/security/pentest-2026-q1]]"
```

---

## Validation Rules

An ADR instance is **valid** if and only if:

| Rule | Condition |
|------|-----------|
| V-ADR-01 | `id` matches regex `^ADR-\d{4}$` |
| V-ADR-02 | `status` is one of the 5 allowed enum values |
| V-ADR-03 | `decision_class` is one of the 3 allowed enum values |
| V-ADR-04 | `tier` is one of the 10 allowed enum values |
| V-ADR-05 | `options_considered` has ≥ 2 entries |
| V-ADR-06 | Each option has ≥ 1 pro and ≥ 1 con |
| V-ADR-07 | If `status = DECIDED`, `date_decided` is non-null and `approvers` has ≥ 1 entry with `approved = true` |
| V-ADR-08 | If `status = SUPERSEDED`, `superseded_by` is non-null and matches `^ADR-\d{4}$` |
| V-ADR-09 | If `decision_class = STRATEGIC`, at least one approver role must be `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` |
| V-ADR-10 | `context`, `problem_statement`, `decision`, `rationale`, `consequences` all ≥ minimum char counts |
| V-ADR-11 | `date_created` ≤ `date_decided` (when both present) |
| V-ADR-12 | `business_impact_assessment.recommendation` ∈ {PROCEED, PROCEED_WITH_MITIGATION, REJECT} when present |

---

## Machine-Actionability Notes

An AI agent validating this artifact should:

1. **Parse** the YAML frontmatter block between the first `---` delimiters of the ADR Markdown file.
2. **Run schema validation** against this schema definition using a YAML schema validator (e.g., `pykwalify`, `jsonschema` after YAML→JSON conversion, or `yamale`).
3. **Cross-reference** `affected_contracts` IDs against the contract registry at `[[docs/contracts/CONTRACT_REGISTRY]]`.
4. **Check approval quorum**: for `STRATEGIC` ADRs, verify the Architect wikilink appears in `approvers` with `approved: true`.
5. **Detect circular supersession**: traverse `supersedes` / `superseded_by` chains to verify no cycles exist.
6. **Trigger downstream notifications**: when `status` transitions to `DECIDED`, notify all roles listed in `consuming_roles` via the workflow automation layer.
7. **Aggregate metrics**: count ADRs per `tier` and `decision_class` to produce the architecture decision heatmap for governance dashboards.
