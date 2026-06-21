---
title: "Agent Identity Schema — AID & Authentication"
version: "1.0.0"
date_created: "2026-06-21"
status: draft
owning_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "[[SECURITY_ENGINEER_SKILL]]"
consuming_roles:
  - "All 14 roles (as instantiated AI agents)"
cssclass: protocol-spec
tags:
  - multi-agent
  - coordination-protocol
  - MACP
  - autonomy
  - agent-identity
  - authentication
  - machine-parseable
---

# Agent Identity Schema — AID & Authentication

> **Pillar 1 of the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]].** Closes the Phase-3 gap *"No agent discovery mechanism exists"* ([[REVIEW_V2_PHASE3_AI_AGENT]] §6.1, scored 2/5).

#multi-agent #coordination-protocol #MACP #autonomy

**Acronyms (defined on first use):** AID (Agent Identity Document), MACP (Multi-Agent Coordination Protocol), DID (Decentralized Identifier), SKILL.md (the role definition / skill card), SHA-256 (Secure Hash Algorithm, 256-bit), Ed25519 (Edwards-curve Digital Signature Algorithm over Curve25519), JWS (JSON Web Signature), UUID (Universally Unique Identifier), TTL (Time To Live), ADR (Architecture Decision Record), CCR (Contract Clarification Record), ARB (Architecture Review Board).

---

## 1. Purpose

An agent's identity answers four questions another agent must be able to resolve **without a human**:

1. **Who are you?** — a unique, verifiable identifier.
2. **What role do you play?** — a binding to exactly one SKILL.md.
3. **What are you authorized to do?** — capabilities and decision-tier authority derived from that SKILL.md.
4. **How do I trust a message from you?** — a public key against which message and ledger signatures verify.

Identity is **bound to the role's SKILL.md**: an agent is "the Firmware Engineer" precisely because it operates within the [[FIRMWARE_ENGINEER_SKILL]] scope, authorities, and constraints, and because its AID records the content hash of that file.

---

## 2. Identifier Scheme

Agent identifiers use a DID-style scheme that is human-readable and machine-resolvable:

```
did:macp:<role-code>:<instance>
```

- `did:macp:` — the MACP identity method namespace.
- `<role-code>` — the canonical role code from [[MULTI_AGENT_COORDINATION_PROTOCOL]] §3 (e.g., `firmware`, `data`, `security`). Long form is used in the DID for readability; the short code (`FW`, `DATA`, `SEC`) is used in contract IDs and message envelopes.
- `<instance>` — a per-instantiation identifier so multiple agent instances of the same role are distinguishable (e.g., `01HX...` ULID, or `primary`, `deputy`, `shadow`).

**Examples:**
- `did:macp:firmware:primary` — the primary Firmware Engineer agent
- `did:macp:architect:deputy` — the Deputy Architect agent (see §6)
- `did:macp:security:primary` — the Security Engineer agent

The Obsidian wikilink to the SKILL.md remains the **canonical human-facing reference**; the DID is the canonical machine-facing reference. The AID binds the two.

---

## 3. AID Schema Definition

The Agent Identity Document is a YAML record stored in the Identity Registry (`docs/agent-protocol/registry/AGENT_REGISTRY.yaml`, one entry per agent).

```yaml
# AID Schema v1.0.0

schema_version: "1.0.0"

# ── Identity ──────────────────────────────────────────────────────────────────
agent_id: string                    # (required) did:macp:<role-code>:<instance>
role_code: string                   # (required) canonical short code: RES|ARCH|HW|FW|ML|DATA|MLOPS|BACK|DEVOPS|FE|QA|SEC|PO|BIZ (+ ARCH-DEP|SEC-DEP|IC)
role_wikilink: string               # (required) Obsidian wikilink to the SKILL.md, e.g. "[[FIRMWARE_ENGINEER_SKILL]]"
display_name: string                # (required) human-readable, e.g. "Firmware Engineer Agent (primary)"

# ── Role Binding (identity is bound to the SKILL.md) ──────────────────────────
role_binding:
  skill_md_path: string             # (required) repo-relative path, e.g. "FIRMWARE_ENGINEER_SKILL.md"
  skill_md_sha256: string           # (required) SHA-256 of the bound SKILL.md content — binds identity to a definition version
  skill_md_version: string          # (required) the SKILL.md frontmatter version/date it was bound to
  bound_at: date                    # (required) ISO 8601 — when this binding was established

# ── Capabilities (derived from SKILL.md §2 Owns and §5 Deliverables) ──────────
capabilities:
  produces: list[string]            # (required) artifact types this agent produces (from §5 Deliverables) — used by registry "producers_of" queries
  consumes: list[string]            # (required) artifact types this agent requires (from §6 Requires) — used by "consumers_of" queries
  owns_decisions: list[string]      # (required) decision categories owned unilaterally (from §7)
  influences: list[string]          # (optional) decisions this agent informs but does not own (from §2 Influences)

# ── Authority (derived from SKILL.md §7 Decision Authority) ───────────────────
authority:
  max_autonomous_tier: string       # (required) highest tier this agent may resolve without a human: Tier-2|Tier-3|Tier-4 (never Tier-1)
  auto_confirm_enabled: boolean     # (required) may Auto-Confirm valid Tier 3–4 proposals
  veto_holder: boolean              # (required) true only for SEC (security release veto) and ARCH (production gate)
  governance_eligible: boolean      # (required) Level-2 governance participant (ARB/EPR voting) per [[AGENT_GOVERNANCE_PARTICIPATION]]
  fractional_parent: string         # (optional) agent_id of the parent role for fractional agents (see §6); null otherwise

# ── Authentication ────────────────────────────────────────────────────────────
authentication:
  public_key: string                # (required) Ed25519 public key (base64) — verifies message + ledger signatures
  key_algorithm: string             # (required) "Ed25519"
  signature_format: string          # (required) "JWS-EdDSA" (JSON Web Signature, EdDSA)
  key_created: date                 # (required) ISO 8601
  key_expires: date                 # (required) ISO 8601 — rotation deadline
  previous_public_keys: list[string] # (optional) retained for verifying historical ledger entries after rotation

# ── Liveness & Reachability ───────────────────────────────────────────────────
status:                             # (required) enum
  type: string
  allowed_values:
    - ACTIVE         # operating and reachable
    - SUSPENDED      # temporarily withdrawn (e.g., drift detected, key rotation pending)
    - RETIRED        # permanently decommissioned; key retained for historical verification

endpoint:
  transport: string                 # (required) "file-queue" | "nats" | "mqtt" | "https"
  address: string                   # (required) bus subject / queue path / URL for this agent's inbox
  heartbeat_interval_s: integer     # (required) seconds between liveness heartbeats
  last_heartbeat: date              # (optional) ISO 8601 timestamp of last observed heartbeat

# ── Escalation Policy (overrides MACP defaults, stricter-only) ────────────────
escalation_policy:
  confidence_threshold_tier3_4: number  # (optional) default 0.70; may only be raised
  confidence_threshold_tier2: number    # (optional) default 0.85; may only be raised
  deadlock_rounds_N: integer             # (optional) default 3; may only be lowered
  novelty_threshold: number              # (optional) default 0.80; may only be lowered
  human_role_holder: string              # (required) wikilink to the human who receives this agent's escalations

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]                  # (optional) kebab-case
notes: string                       # (optional) free text
```

---

## 4. Example Instance

```yaml
schema_version: "1.0.0"

agent_id: "did:macp:firmware:primary"
role_code: "FW"
role_wikilink: "[[FIRMWARE_ENGINEER_SKILL]]"
display_name: "Firmware Engineer Agent (primary)"

role_binding:
  skill_md_path: "FIRMWARE_ENGINEER_SKILL.md"
  skill_md_sha256: "9f2c4e8a1b7d3056c9a4f8e2b1d7c0a3e6f9b2d5c8a1e4f7b0d3c6a9e2f5b8d1"
  skill_md_version: "final / 2026-06-20"
  bound_at: "2026-06-21"

capabilities:
  produces:
    - "production-firmware-binary"
    - "device-telemetry-schema-implementation"
    - "ota-signed-image"
    - "hal-driver-layer"
    - "firmware-resource-report"
  consumes:
    - "interface-contracts"
    - "per-node-resource-budgets"
    - "quantized-model-artifact"
    - "security-baseline"
    - "ota-compatibility-manifest"
  owns_decisions:
    - "internal-firmware-structure"
    - "ipc-primitive-selection"
    - "stack-and-buffer-sizing"
    - "unit-test-structure"
  influences:
    - "interface-contracts"
    - "per-node-resource-budgets"
    - "sensor-selection"

authority:
  max_autonomous_tier: "Tier-3"
  auto_confirm_enabled: true
  veto_holder: false
  governance_eligible: true
  fractional_parent: null

authentication:
  public_key: "MCowBQYDK2VwAyEA8z1mF0q7t3Yc2nLpR9vK4xW6sB1dH7gJ0aZ5cQ2eU="
  key_algorithm: "Ed25519"
  signature_format: "JWS-EdDSA"
  key_created: "2026-06-21"
  key_expires: "2027-06-21"
  previous_public_keys: []

status: ACTIVE

endpoint:
  transport: "nats"
  address: "macp.inbox.firmware.primary"
  heartbeat_interval_s: 60
  last_heartbeat: "2026-06-21T09:14:33Z"

escalation_policy:
  confidence_threshold_tier3_4: 0.70
  confidence_threshold_tier2: 0.85
  deadlock_rounds_N: 3
  novelty_threshold: 0.80
  human_role_holder: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"

tags:
  - agent-active
  - firmware
notes: "Bound to FIRMWARE_ENGINEER_SKILL.md final/2026-06-20. Max autonomous tier 3 per §7 unilateral-decision scope."
```

---

## 5. Authentication & Trust Model

### 5.1 Message Authentication

Every A2A message ([[A2A_MESSAGE_SCHEMA]]) and every ledger entry ([[COORDINATION_LEDGER_SCHEMA]]) is **signed** with the agent's Ed25519 private key. A receiving agent:

1. Resolves the sender `agent_id` against the Identity Registry.
2. Fetches the sender's `authentication.public_key`.
3. Verifies the JWS-EdDSA signature over the canonical serialization of the message.
4. Rejects the message if the signature fails, the key has expired, or `status ≠ ACTIVE`.

This makes spoofing one agent as another cryptographically infeasible and gives the ledger non-repudiation.

### 5.2 Capability-Bound Authorization

Authentication proves *who sent it*; authorization proves *they were allowed to*. Before acting on a `PROPOSE`, the recipient checks the sender's AID `capabilities` and `authority`:

- A `PROPOSE` to change a contract is only honored if the proposal routes through the ADR process (the sender cannot self-authorize a contract change — [[MULTI_AGENT_COORDINATION_PROTOCOL]] §8 invariant).
- An Auto-Confirm is only valid if the **confirming** agent has `auto_confirm_enabled: true` and the decision tier ≤ its `max_autonomous_tier`.
- A governance vote is only counted if the voter's AID has `governance_eligible: true`.

### 5.3 SKILL.md Drift Detection

Because the AID records `skill_md_sha256`, the synchronization job ([[CONTRACT_REGISTRY_SCHEMA]] §5) can detect when a SKILL.md has changed but its bound agents have not re-bound:

- On every registry rebuild, recompute the SHA-256 of each SKILL.md.
- If it differs from any `ACTIVE` agent's `role_binding.skill_md_sha256`, set that agent to `SUSPENDED` and raise an escalation (trigger `ESC-NOV` is not appropriate; this is a dedicated **drift escalation**) to the agent's `human_role_holder`.
- The agent may not return to `ACTIVE` until it re-binds to the new hash, ensuring agents never operate against a stale role definition.

### 5.4 Key Rotation

Keys rotate before `key_expires`. On rotation, the prior public key is appended to `previous_public_keys` so that historical ledger entries signed with the old key still verify. The rotation event itself is recorded in the Coordination Ledger.

---

## 6. Fractional & Specialized Agents

The Phase-3 review (§2.1) flagged that **Deputy Architect** and **Deputy Security Engineer** lack dedicated execution guides. MACP handles them as **fractional agents** that inherit the parent SKILL.md but carry constrained authority:

| Fractional Agent | `agent_id` | `fractional_parent` | Authority Constraint |
|------------------|-----------|---------------------|----------------------|
| Deputy Architect | `did:macp:architect:deputy` | `did:macp:architect:primary` | `max_autonomous_tier: Tier-3`; may handle **non-breaking** ADRs only; any decision that "changes a platform selection, protocol choice, resource budget, security baseline, or OTA strategy" must escalate to the parent. |
| Deputy Security Engineer | `did:macp:security:deputy` | `did:macp:security:primary` | `max_autonomous_tier: Tier-3`; **Standard-tier** security sign-off only; `veto_holder: false`; Security-Relevant releases escalate to the parent (`did:macp:security:primary`). |

A fractional agent's `role_binding` points to the **parent SKILL.md** plus the relevant §1 authority-limit subsection. Its `authority` block encodes the constraint so that any out-of-scope `PROPOSE` is automatically escalated to `fractional_parent`.

---

## 7. Discovery Operations

The Identity Registry supports these queries (Phase A of the coordination lifecycle):

| Query | Returns |
|-------|---------|
| `resolve(agent_id)` | the full AID |
| `agents_for_role(role_code)` | all agent instances bound to a role (e.g., primary + deputy) |
| `active_agents()` | all agents with `status = ACTIVE` and a fresh heartbeat |
| `producer_of(artifact_type)` | the agent(s) whose `capabilities.produces` includes the artifact |
| `consumer_of(artifact_type)` | the agent(s) whose `capabilities.consumes` includes the artifact |
| `public_key(agent_id)` | the verifying key for signature checks |
| `can_resolve(agent_id, tier)` | whether the agent's `max_autonomous_tier` ≥ the decision tier |

These pair with the Contract Registry's contract-level queries ([[CONTRACT_REGISTRY_SCHEMA]] §6) so an agent can go from "I produced X" → "who consumes X" → "what contract governs it" → "is that agent active and authorized."

---

## 8. Validation Rules

An AID instance is **valid** if and only if:

| Rule | Condition |
|------|-----------|
| V-AID-01 | `agent_id` matches regex `^did:macp:[a-z-]+:[A-Za-z0-9-]+$` |
| V-AID-02 | `role_code` is one of the 17 allowed values (14 primary + `ARCH-DEP`, `SEC-DEP`, `IC`) |
| V-AID-03 | `role_wikilink` resolves to an existing SKILL.md file in the vault |
| V-AID-04 | `role_binding.skill_md_sha256` matches the current SHA-256 of `role_binding.skill_md_path` (else agent is set `SUSPENDED`) |
| V-AID-05 | `authority.max_autonomous_tier` ∈ {Tier-2, Tier-3, Tier-4} — **never** Tier-1 |
| V-AID-06 | `authority.veto_holder = true` only if `role_code ∈ {SEC, ARCH}` |
| V-AID-07 | `authentication.public_key` is a valid Ed25519 key and `key_expires > today` for `status = ACTIVE` |
| V-AID-08 | `status` is one of {ACTIVE, SUSPENDED, RETIRED} |
| V-AID-09 | If `fractional_parent` is non-null, it resolves to an `ACTIVE` parent AID and `max_autonomous_tier` ≤ parent's |
| V-AID-10 | `escalation_policy` thresholds are stricter-or-equal to MACP defaults (confidence ≥ default, N ≤ default, novelty ≤ default) |
| V-AID-11 | `escalation_policy.human_role_holder` resolves to an existing role wikilink |
| V-AID-12 | `capabilities.produces` and `capabilities.consumes` are non-empty for primary roles |

---

## 9. Machine-Actionability Notes

An agent consuming this schema should:

1. **Cache the Identity Registry** at session start and refresh on heartbeat-interval cadence; treat any `agent_id` not in the registry as untrusted.
2. **Verify before acting:** never process a message whose signature does not verify against the sender's registered `public_key`.
3. **Authorize before confirming:** check `authority.max_autonomous_tier` and `auto_confirm_enabled` before any Auto-Confirm.
4. **Re-bind on drift:** if its own `skill_md_sha256` no longer matches the file, self-suspend and request re-binding from its `human_role_holder`.
5. **Honor fractional limits:** a fractional agent must auto-escalate any `PROPOSE` exceeding its constrained authority to `fractional_parent`.

---

## 10. Related Documents

- [[MULTI_AGENT_COORDINATION_PROTOCOL]] — master specification (Pillar 1 lives here)
- [[CONTRACT_REGISTRY_SCHEMA]] — pairs identity discovery with contract discovery
- [[A2A_MESSAGE_SCHEMA]] — signatures verify against AID public keys
- [[COORDINATION_LEDGER_SCHEMA]] — ledger entries are AID-signed
- [[AGENT_GOVERNANCE_PARTICIPATION]] — `governance_eligible` gates voting
- [[REVIEW_V2_PHASE3_AI_AGENT]] — §2.1 (fractional-role gap), §6.1 (discovery gap)

#multi-agent #coordination-protocol #MACP #autonomy #agent-identity
