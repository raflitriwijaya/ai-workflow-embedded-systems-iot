---
title: "Contract Registry Schema — Machine-Readable Interface Contracts"
version: "1.0.0"
date_created: "2026-06-21"
status: draft
owning_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
consuming_roles:
  - "All 14 roles (as instantiated AI agents)"
  - "ARB (Architecture Review Board)"
cssclass: protocol-spec
tags:
  - multi-agent
  - coordination-protocol
  - MACP
  - autonomy
  - contract-registry
  - interface-contracts
  - machine-parseable
---

# Contract Registry Schema — Machine-Readable Interface Contracts

> **Pillar 2 of the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]].** Closes the Phase-3 gap *"No machine-readable contract registry exists"* ([[REVIEW_V2_PHASE3_AI_AGENT]] §6.1, scored 2/5). Makes all **91 symmetric interface contracts** queryable so an agent can ask *"Who requires what I produce?"* and *"Who produces what I require?"*

#multi-agent #coordination-protocol #MACP #autonomy

**Acronyms (defined on first use):** MACP (Multi-Agent Coordination Protocol), SKILL.md (the role definition / skill card), YAML (YAML Ain't Markup Language), SHA-256 (Secure Hash Algorithm, 256-bit), SemVer (Semantic Versioning), CCR (Contract Clarification Record), ADR (Architecture Decision Record), CI (Continuous Integration), SLA (Service Level Agreement), DQIR (Data Quality Issue Report), OTA (Over-the-Air).

---

## 1. Purpose

The 91 interface contracts currently live as **§6 Provides/Requires/Cadence triples** inside 14 Markdown SKILL.md files. A human can read them; an agent cannot programmatically answer:

- *Who consumes the artifact I just produced?*
- *Who produces the input I am waiting on?*
- *What is the cadence/SLA for this obligation, and is it overdue?*
- *Is there an open CCR blocking this contract?*
- *What schema must my deliverable validate against?*

The Contract Registry is the **single, generated, queryable index** that answers all of these. It is derived from the §6 sections, kept synchronized as contracts change, and never hand-edited.

---

## 2. Contract Identity Scheme

Each symmetric pair gets a canonical contract ID, matching the convention already used in [[CCR_SCHEMA]] and [[ADR_SCHEMA]] (e.g., `FW↔CLOUD-MQTT-001`, `SEC↔DEVOPS-PKI-001`):

```
<ROLE_A>↔<ROLE_B>[-<TOPIC>]-<NNN>
```

- `ROLE_A`, `ROLE_B` — the two role codes ([[MULTI_AGENT_COORDINATION_PROTOCOL]] §3), ordered by the **canonical role ordering** below so each pair has exactly one ID regardless of who initiates.
- `TOPIC` — optional uppercase topic tag when a pair has multiple distinct contracts (e.g., `MQTT`, `PKI`, `OTA-MODEL`).
- `NNN` — zero-padded sequence number within the pair.

**Canonical role ordering** (for deterministic pair IDs):
`RES < ARCH < HW < FW < ML < DATA < MLOPS < BACK < DEVOPS < FE < QA < SEC < PO < BIZ`

So the Firmware↔Data telemetry contract is `FW↔DATA-001` (FW precedes DATA). With 14 roles, the registry contains all **C(14,2) = 91** base pairs; topics add further contracts where a pair has more than one.

---

## 3. Registry Entry Schema

The registry is a single YAML file (`docs/agent-protocol/registry/CONTRACT_REGISTRY.yaml`) containing a list of contract entries.

```yaml
# Contract Registry Entry Schema v1.0.0

schema_version: "1.0.0"

# ── Identity ──────────────────────────────────────────────────────────────────
contract_id: string                 # (required) e.g. "FW↔DATA-001" — matches CCR/ADR contract_id references
contract_title: string              # (required) human-readable name
contract_version: string            # (required) SemVer of the contract text itself, e.g. "2.1.0"
status:                             # (required) enum
  type: string
  allowed_values:
    - ACTIVE        # in force
    - DRAFT         # proposed, not yet ratified
    - DEPRECATED    # being phased out
    - SUPERSEDED    # replaced (link via superseded_by)
superseded_by: string               # (optional) contract_id

# ── Parties ───────────────────────────────────────────────────────────────────
role_a:
  role_code: string                 # (required) e.g. "FW"
  wikilink: string                  # (required) e.g. "[[FIRMWARE_ENGINEER_SKILL]]"
role_b:
  role_code: string                 # (required) e.g. "DATA"
  wikilink: string                  # (required) e.g. "[[DATA_ENGINEER_SKILL]]"

# ── Directional Obligations (the §6 Provides/Requires triple, made directional) ─
provides:                           # (required) what role_a provides to role_b (and vice-versa for symmetric pairs)
  - artifact: string                # (required) canonical artifact type, e.g. "device-telemetry-schema-implementation"
    from_role: string               # (required) role_code of the producer
    to_role: string                 # (required) role_code of the consumer
    payload_schema: string          # (optional) named schema the artifact validates against, e.g. "[[DQIR_SCHEMA]]" or "null" if prose-only (flagged for RB-2)
    description: string             # (required) verbatim or normalized text from the §6 Provides field

requires:                           # (required) what each role needs from the other (mirror of provides)
  - artifact: string
    required_by: string             # role_code of the consumer
    from_role: string               # role_code of the producer

# ── Cadence (machine-actionable scheduling) ───────────────────────────────────
cadence:                            # (required) list — one per synchronization point
  - name: string                    # (required) e.g. "Schema-Change Joint Review"
    type: string                    # (required) enum: CALENDAR | TRIGGER | SLA_FROM_EVENT | CONTINUOUS
    # For CALENDAR:
    calendar_rule: string           # (optional) e.g. "second Tuesday of Jan/Apr/Jul/Oct"
    # For TRIGGER / SLA_FROM_EVENT:
    trigger_event: string           # (optional) e.g. "schema-change-proposal-raised"
    trigger_source: string          # (optional) monitoring query/source, e.g. "prometheus: telemetry_loss_ratio > 0.01" (links RB-6)
    sla: string                     # (optional) e.g. "5 business days"
    decision_tier: string           # (required) Tier-1|Tier-2|Tier-3|Tier-4 — drives agent authority ([[MULTI_AGENT_COORDINATION_PROTOCOL]] §4)

# ── Governance State ──────────────────────────────────────────────────────────
open_ccrs: list[string]             # (required) list of CCR-NNNN currently OPEN/IN_REVIEW against this contract (auto-populated from CCR registry)
linked_adrs: list[string]           # (optional) ADR-NNNN that modified this contract
breaking_change_policy: string      # (required) where a breaking change must route, e.g. "ADR with [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] as approver"

# ── Obligation Tracking ───────────────────────────────────────────────────────
next_deliverable:
  artifact: string                  # (optional) next scheduled deliverable under this contract
  due: date                         # (optional) ISO 8601 — computed from cadence
  obligation_status: string         # (optional) PENDING | IN_PROGRESS | SATISFIED | OVERDUE

# ── Provenance (synchronization) ──────────────────────────────────────────────
source:
  skill_md_paths: list[string]      # (required) the SKILL.md file(s) and §6 subsections this entry was derived from
  source_section: string            # (required) e.g. "FIRMWARE_ENGINEER_SKILL.md §6.8"
  source_sha256: string             # (required) SHA-256 of the source §6 subsection text at generation time (drift detection)
  generated_at: date                # (required) ISO 8601 — registry build timestamp

tags: list[string]                  # (optional) kebab-case
```

---

## 4. Transformation: §6 Markdown → Registry YAML

The registry is produced by a deterministic **registry-build job** that parses the §6 sections of every SKILL.md. The transformation is specified so it is reproducible and auditable.

### 4.1 Parsing Rules

For each SKILL.md, the job:

1. **Locates §6 "Interface Contracts."** Each `### 6.x <Collaborator>` subsection defines this role's side of one contract pair.
2. **Resolves the pair.** The collaborator heading (wikilink or role name) → counterpart role code. The two role codes → canonical `contract_id` (§2 ordering).
3. **Extracts the triple:**
   - `**Provides:**` bullet → `provides[]` entries (`from_role = this role`, `to_role = counterpart`).
   - `**Requires:**` bullet → `requires[]` entries.
   - `**Cadence:**` bullet → one or more `cadence[]` entries, classified by pattern (§4.2).
4. **Merges both sides.** Because contracts are symmetric, role_a's §6.x for role_b and role_b's §6.y for role_a describe the same `contract_id`. The job merges them into one entry, cross-checking that Provides on one side matches Requires on the other (a mismatch raises a **reciprocity warning**, feeding the [[RECIPROCITY_AUDIT_SPEC|Reciprocity Audit]]).
5. **Binds payload schemas.** If the artifact maps to one of the eight [[SCHEMA_INDEX]] schemas (ADR, CCR, DQIR, IRD, OCM, SIRC, TTP, BIA), `payload_schema` is set to that wikilink; otherwise `payload_schema: null` and the entry is tagged `prose-only` (the residual RB-2 surface).
6. **Computes provenance.** `source_sha256` = SHA-256 of the exact §6 subsection text; `source_section` records the file and heading.

### 4.2 Cadence Classification

Cadence prose is classified into the four machine-actionable types (mirroring [[REVIEW_V2_PHASE3_AI_AGENT]] §3.2):

| Prose pattern (example) | `type` | Machine action |
|-------------------------|--------|----------------|
| "second Tuesday of Jan/Apr/Jul/Oct", "first Tuesday of November" | `CALENDAR` | schedule from `calendar_rule` |
| "within 15 business days of algorithm-specification handoff" | `SLA_FROM_EVENT` | start SLA timer on `trigger_event` |
| "within 1 business day of identifying data quality issue" | `TRIGGER` | watch `trigger_source` (Prometheus/Grafana), then apply `sla` |
| "continuous during development", "weekly integration smoke tests" | `CONTINUOUS` | recurring obligation |

`decision_tier` is assigned from the `tier_classification` table (§7), defaulting upward when ambiguous.

### 4.3 Worked Example — `FW↔DATA-001`

Source: [[FIRMWARE_ENGINEER_SKILL]] §6.8 (Data Engineer) and the mirrored Data Engineer §6 (Firmware Engineer).

```yaml
contract_id: "FW↔DATA-001"
contract_title: "Device Telemetry Schema & Schema-Change Coordination"
contract_version: "2.1.0"
status: ACTIVE
superseded_by: null

role_a:
  role_code: "FW"
  wikilink: "[[FIRMWARE_ENGINEER_SKILL]]"
role_b:
  role_code: "DATA"
  wikilink: "[[DATA_ENGINEER_SKILL]]"

provides:
  - artifact: "device-telemetry-conformant-stream"
    from_role: "FW"
    to_role: "DATA"
    payload_schema: null            # prose-only (RB-2 residual)
    description: "Telemetry conforming to the schema, correct units/sampling/timestamps, edge-buffering/backfill behavior."
  - artifact: "schema-change-proposal"
    from_role: "FW"
    to_role: "DATA"
    payload_schema: "[[CCR_SCHEMA]]" # schema changes carry a CCR-shaped payload
    description: "Schema-change proposal: changed fields, rationale, backward-compatibility assessment, impact."

requires:
  - artifact: "telemetry-schema-details"
    required_by: "FW"
    from_role: "DATA"
  - artifact: "ingestion-constraints"
    required_by: "FW"
    from_role: "DATA"

cadence:
  - name: "Schema-Change Joint Review"
    type: "SLA_FROM_EVENT"
    trigger_event: "schema-change-proposal-raised"
    sla: "5 business days"
    decision_tier: "Tier-3"          # non-breaking; breaking escalates to Tier-2 ADR
  - name: "Pipeline-Integration Checkpoints"
    type: "CONTINUOUS"
    decision_tier: "Tier-4"

open_ccrs: []
linked_adrs: []
breaking_change_policy: "Backward-incompatible change → ADR with [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] as approver (FIRMWARE_ENGINEER_SKILL §6.8 step 3)"

next_deliverable:
  artifact: null
  due: null
  obligation_status: PENDING

source:
  skill_md_paths:
    - "FIRMWARE_ENGINEER_SKILL.md"
    - "DATA_ENGINEER_SKILL.md"
  source_section: "FIRMWARE_ENGINEER_SKILL.md §6.8 + DATA_ENGINEER_SKILL.md (Firmware)"
  source_sha256: "c1a9e4...d27b"
  generated_at: "2026-06-21"

tags:
  - schema-change
  - telemetry
  - prose-only-stream
```

---

## 5. Synchronization & Drift Control

The registry must stay synchronized as contracts change. The synchronization model has one rule: **SKILL.md §6 is the source of truth; the registry is a generated mirror.**

### 5.1 Generation Triggers

The registry-build job runs:
- on every commit that touches any `*_SKILL.md` file (CI hook),
- on every CCR transition to `CLOSED` with `contract_update_required: true` (the contract text changed),
- on every ADR transition to `DECIDED` that lists `affected_contracts`,
- nightly as a backstop.

### 5.2 Drift Detection

For every entry, the job recomputes `source_sha256` from the current §6 text:
- **Match** → entry is current.
- **Mismatch** → the §6 text changed but the registry was not regenerated through the proper path. The job regenerates the entry, bumps `contract_version` (SemVer: minor for additive, major for breaking — determined by diffing the Provides/Requires sets), and records the change in the Coordination Ledger.
- **Reciprocity mismatch** (Provides on one side ≠ Requires on the other) → raises a warning to the [[RECIPROCITY_AUDIT_SPEC|Reciprocity Audit]] and tags the entry `reciprocity-warning`; agents treat such a contract as **degraded** and require human confirmation before relying on it.

### 5.3 CCR/ADR Feedback Loop

This is how the registry stays consistent with human governance (Constraint: compatible with CCR/ADR):

```
CCR RESOLVED (contract_update_required=true)
        │
        ▼
  human edits the SKILL.md §6 text
        │
        ▼
  CI detects *_SKILL.md change → registry-build job runs
        │
        ▼
  entry regenerated, contract_version bumped, open_ccrs cleared of the resolved CCR
        │
        ▼
  ledger entry appended: {event: contract-updated, contract_id, old_v, new_v, ccr_ref}
```

`open_ccrs` is **auto-populated** from the CCR registry on every build: any `CCR-NNNN` whose `contract_reference.contract_id` matches and whose `status ∈ {OPEN, IN_REVIEW}` is listed. This makes CCR validation rule V-CCR-11 (BLOCKING CCRs hold integration) directly enforceable by agents at gate time.

### 5.4 Versioning

- `schema_version` — version of *this registry schema* (1.0.0).
- `contract_version` — SemVer of each individual contract's text; bumped on any §6 change.
- The registry file itself is Git-tracked, so its full history is auditable alongside the SKILL.md history.

---

## 6. Query Interface

The registry exposes the discovery queries that the coordination lifecycle's Phase A depends on:

| Query | Returns | Backs |
|-------|---------|-------|
| `producers_of(artifact)` | role codes + contract_ids that produce the artifact | "Who produces what I require?" |
| `consumers_of(artifact)` | role codes + contract_ids that consume the artifact | "Who requires what I produce?" |
| `contracts_for(role_code)` | all contracts a role participates in | obligation enumeration |
| `contract(contract_id)` | the full entry | message composition |
| `obligations_due(role_code, by_date)` | obligations with `due ≤ by_date` and status not SATISFIED | proactive scheduling |
| `open_ccrs_for(contract_id)` | blocking/open CCRs | gate enforcement (ESC-BLOCK) |
| `tier_of(contract_id, decision_name)` | the decision tier for a coordination | authority check |
| `prose_only_contracts()` | contracts with `payload_schema: null` | tracks residual RB-2 surface |

---

## 7. Decision-Tier Classification Table

To make tier classification machine-executable ([[REVIEW_V2_PHASE3_AI_AGENT]] §4.3 / RB-3), the registry carries a top-level `tier_classification` block referenced by all cadence entries:

```yaml
tier_classification:
  - decision_category: "platform/protocol/security-baseline/OTA-strategy change"
    tier: "Tier-1"
    authority: "human only (permanent HITL gate)"
    sla: "4 business hours"
  - decision_category: "ARB-resolvable architecture decision; cross-team interface deadlock"
    tier: "Tier-2"
    authority: "agents deliberate + vote → non-binding recommendation; human ratifies"
    sla: "2 business days"
  - decision_category: "schema clarification within rubric; DQIR severity within rubric; routine contract interpretation"
    tier: "Tier-3"
    authority: "agent-autonomous (Auto-Confirm if confidence ≥ 0.70)"
    sla: "5 business days"
  - decision_category: "documentation alignment; cosmetic clarification; routine scheduling"
    tier: "Tier-4"
    authority: "agent-autonomous (Auto-Confirm default)"
    sla: "10 business days"
```

---

## 8. Validation Rules

| Rule | Condition |
|------|-----------|
| V-CR-01 | `contract_id` matches regex `^[A-Z]+↔[A-Z]+(-[A-Z0-9]+)?-\d{3}$` |
| V-CR-02 | `role_a.role_code` precedes `role_b.role_code` in the canonical ordering (§2) |
| V-CR-03 | Every `provides[].to_role` and `requires[].from_role` is one of the two parties |
| V-CR-04 | Each `cadence[].type` ∈ {CALENDAR, TRIGGER, SLA_FROM_EVENT, CONTINUOUS} |
| V-CR-05 | Each `cadence[].decision_tier` ∈ {Tier-1, Tier-2, Tier-3, Tier-4} |
| V-CR-06 | `open_ccrs[*]` each match `^CCR-\d{4}$` and exist in the CCR registry |
| V-CR-07 | `linked_adrs[*]` each match `^ADR-\d{4}$` and exist in the ADR registry |
| V-CR-08 | `source.source_sha256` equals the current SHA-256 of `source_section` (else `reciprocity-warning`/regenerate) |
| V-CR-09 | `payload_schema` is either `null` or a wikilink to a file in [[SCHEMA_INDEX]] |
| V-CR-10 | For symmetric pairs, the union of both sides' Provides equals the union of both sides' Requires (reciprocity) |
| V-CR-11 | Total base-pair entries = 91 (one per role pair); topic variants add to this count |
| V-CR-12 | If `status = SUPERSEDED`, `superseded_by` is a valid `contract_id` |

---

## 9. Machine-Actionability Notes

An agent consuming this registry should:

1. **Resolve before composing:** run `consumers_of` / `producers_of` to find the counterpart agent and contract before sending any message.
2. **Gate on CCRs:** before accepting an Integration Readiness Declaration or completing coordination, check `open_ccrs_for(contract_id)`; any BLOCKING CCR forces escalation (ESC-BLOCK).
3. **Schedule from cadence:** convert `CALENDAR` rules to dated obligations and `SLA_FROM_EVENT`/`TRIGGER` to timers/watches; surface `OVERDUE` obligations (ESC-SLA).
4. **Classify by table:** use `tier_of(...)` to set the decision tier and therefore the agent's authority; default upward on ambiguity.
5. **Never hand-edit:** treat the registry as read-only; to change a contract, edit the SKILL.md §6 and let the build regenerate (preserving the human source-of-truth invariant).
6. **Flag prose-only:** for `payload_schema: null` artifacts, fall back to human confirmation of acceptance criteria — these are the contracts not yet machine-validatable (RB-2).

---

## 10. Related Documents

- [[MULTI_AGENT_COORDINATION_PROTOCOL]] — master specification (Pillar 2 lives here)
- [[AGENT_IDENTITY_SCHEMA]] — pairs with contract discovery
- [[A2A_MESSAGE_SCHEMA]] — `contract_ref` in messages resolves against this registry
- [[CCR_SCHEMA]], [[ADR_SCHEMA]] — feed `open_ccrs` and `linked_adrs`; the sync feedback loop
- [[SCHEMA_INDEX]] — source of `payload_schema` bindings
- [[RECIPROCITY_AUDIT_SPEC]] — consumes reciprocity warnings
- [[REVIEW_V2_PHASE3_AI_AGENT]] — §3 (contract actionability), §6.1 (registry gap), RB-3 (tier table)

#multi-agent #coordination-protocol #MACP #autonomy #contract-registry
