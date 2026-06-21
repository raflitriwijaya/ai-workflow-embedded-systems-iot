---
title: "Agent Governance Participation — ARB, EPR & Release Gates"
version: "1.0.0"
date_created: "2026-06-21"
status: draft
owning_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "[[QA_TEST_AUTOMATION_ENGINEER_SKILL]]"
consuming_roles:
  - "All 14 roles (as instantiated AI agents)"
  - "ARB (Architecture Review Board)"
cssclass: protocol-spec
tags:
  - multi-agent
  - coordination-protocol
  - MACP
  - autonomy
  - governance-participation
  - arb
  - human-in-the-loop
  - machine-parseable
---

# Agent Governance Participation — ARB, EPR & Release Gates

> **Pillar 5 of the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]].** Closes the Phase-3 gap *"No agent participation in collective governance … the ARB, EPR, and release gates are human-only"* ([[REVIEW_V2_PHASE3_AI_AGENT]] §6.4, scored **1/5**).

#multi-agent #coordination-protocol #MACP #autonomy

**Acronyms (defined on first use):** MACP (Multi-Agent Coordination Protocol), ARB (Architecture Review Board), EPR (Engineering Process Review), ADR (Architecture Decision Record), CCR (Contract Clarification Record), IRD (Integration Readiness Declaration), HITL (Human-in-the-Loop), AID (Agent Identity Document), SLA (Service Level Agreement), NFR (Non-Functional Requirement), OTA (Over-the-Air), HG (Human Gate, as catalogued in the Phase-3 review), A2A (Agent-to-Agent).

---

## 1. Purpose & The Binding Boundary

Agents participate in collective governance in exactly three ways, and **no more**:

1. **Submit data and analysis** to the shared dashboards that feed governance bodies.
2. **Propose process improvements** through the Process Architect's channel.
3. **Vote on non-binding recommendations** in the ARB and EPR.

**The binding boundary is absolute:** *binding decisions remain with humans (permanent HITL gates).* An agent vote is an input to a human decision, never the decision itself. This preserves every safety-critical control the ecosystem depends on while letting agents do the analytical heavy lifting that currently bottlenecks at human bandwidth.

```
   AGENTS                              │   HUMANS
   ─────────────────────────────────  │  ──────────────────────────────
   • assemble evidence packages        │  • deliberate
   • compute analyses, trends, risks   │  • cast BINDING votes
   • cast NON-BINDING advisory votes    │  • ratify / override agent recommendations
   • propose process improvements      │  • hold safety-critical vetoes (HG-01, HG-04)
   • record everything to the ledger   │  • author the authoritative decision record
   ─────────────────────────────────  │  ──────────────────────────────
                ▲                       │              ▲
                └────── recommendation ─┴── ratification┘
```

Only agents whose AID has `governance_eligible: true` (Level-2 conformance, [[AGENT_IDENTITY_SCHEMA]] §3) may participate beyond data submission.

---

## 2. Governance Bodies & Agent Roles

| Body | Cadence | Human Authority (unchanged) | Agent Participation (new) |
|------|---------|------------------------------|----------------------------|
| **Architecture Review Board (ARB)** | per Tier-2 escalation; 2-business-day SLA | Quorum of ≥3/5 standing members incl. Architect or Deputy casts the **binding** vote (HG-12) | Submit ADR/CCR analysis; cast **non-binding** advisory votes; author draft decision records for human ratification |
| **Engineering Process Review (EPR)** | second Friday of Jan/Apr/Jul/Oct (HG-14) | All Senior/Staff engineers + PO/TPM make **binding** process changes | Auto-assemble the Engineering Process Health Dashboard; propose process improvements; vote non-bindingly on prioritization |
| **Research-to-Planning Gate** | quarterly, first Tuesday of Feb/May/Aug/Nov (HG-05) | Architect + PO/TPM + Business Consultant **binding** 3-signatory consensus | Score Technology Transfer Pack readiness; flag risks; prepare the gate package |
| **Joint Data Security & Governance Review** | second Tuesday of Jan/Apr/Jul/Oct (HG-15) | Data Engineer + Security Engineer **binding** risk adjudication | Assemble data-asset inventory, access review, posture report; flag privacy-impact escalations |
| **Release Gates (HG-01..HG-04, etc.)** | per release | Security veto (HG-01) and Architect gate (HG-04) are **permanent human gates** | Auto-evaluate software-verifiable conditions; present pass/fail evidence; never sign the gate |

---

## 3. Data Submission (Capability 1)

Agents feed governance bodies through structured submissions, recorded in the [[COORDINATION_LEDGER_SCHEMA|ledger]] and validated against existing schemas:

- **ARB submissions** carry an [[ADR_SCHEMA|ADR]]-draft or [[CCR_SCHEMA|CCR]] analysis as the A2A payload (`message_type: INFORM` → the Architect agent / ARB channel).
- **EPR submissions** are the auto-assembled **Engineering Process Health Dashboard**: ledger `disputes(quarter)` counts, CCR aging, contract-version churn, escalation precision/recall, gate cycle-times. The QA agent (as Process Architect) compiles these.
- **Joint Data Security submissions** assemble the data-asset inventory and access review from the Data and Security agents.

Each submission is an `ARTIFACT_EXCHANGE` ledger entry, so the provenance of every governance input is auditable.

---

## 4. Non-Binding Voting Protocol (Capability 3)

This is the novel mechanism the Phase-3 review found entirely missing ("no provision exists for an AI agent to be a voting member"). It is deliberately designed so an agent vote can **never** be mistaken for a binding decision.

### 4.1 Ballot Schema

A vote is an A2A message (`message_type: VOTE`, [[A2A_MESSAGE_SCHEMA]]) with this payload:

```yaml
# Governance Ballot Schema v1.0.0
schema_version: "1.0.0"
ballot_id: string                   # (required) BALLOT-NNNN
motion_ref:
  body: string                      # (required) ARB | EPR | RESEARCH_GATE | DATA_SEC_REVIEW
  motion_id: string                 # (required) e.g. links to ADR-NNNN under deliberation
  decision_tier: string             # (required) Tier-2 (ARB-class) — agents never vote on Tier-1
voter:
  agent_id: string                  # (required) must have governance_eligible: true
  role_wikilink: string             # (required)
vote: string                        # (required) enum: APPROVE | REJECT | ABSTAIN | RECUSE
binding: false                      # (required) MUST be literal false — agent votes are advisory only
weight: number                      # (required) advisory weight (§4.2), 0.0–1.0
confidence: number                  # (required) 0.0–1.0
rationale: string                   # (required) ≥30 chars — the analytical basis for the vote
evidence_refs: list[string]         # (optional) ledger hashes / artifact IDs supporting the vote
signature: object                   # (required) Ed25519, per A2A
```

### 4.2 Advisory Weighting

Agent advisory votes are weighted by **domain relevance and confidence**, but the aggregate is always presented to humans as a *recommendation*, not a tally that decides:

- An agent gets full advisory weight (1.0) on motions within its `capabilities.owns_decisions`, reduced weight (0.5) on adjacent domains, and 0.0 (informational only) on unrelated domains.
- `RECUSE` is mandatory when the agent is a party to the coordination that produced the motion (no self-approval).
- The recommendation presented to the ARB is: `weighted_advisory_score = Σ(weight × confidence × vote_value) / Σ(weight)`, with the full per-agent breakdown attached.

### 4.3 Quorum & Ratification

- **Agent advisory quorum:** a recommendation is "well-formed" when ≥3 governance-eligible agents (including the domain-owning agent) have voted or explicitly abstained.
- **Human ratification is required for any binding effect.** The human ARB quorum (≥3/5 standing members incl. Architect/Deputy) reviews the recommendation and casts the **binding** vote. The agents' `weighted_advisory_score` is an input, recorded but not decisive.
- The binding decision is written as an authoritative ADR/ARB Decision Record by a human (or co-authored by an agent and signed by a human), and a `GOVERNANCE_VOTE` + ratification entry is appended to the ledger.

### 4.4 Tier Mapping

| Decision Tier | Agent Governance Role |
|---------------|------------------------|
| **Tier 1 (CRITICAL)** | No agent vote. Agents prepare the package only; humans decide (HG-01, HG-04, etc.). |
| **Tier 2 (HIGH / ARB-class)** | Agents deliberate, analyze, and cast **non-binding** advisory votes → recommendation; **human ARB ratifies** (binding). |
| **Tier 3 (MEDIUM)** | Resolved at coordination layer (Propose→Confirm); ARB not convened. Ledger-recorded; human may audit. |
| **Tier 4 (LOW)** | Resolved autonomously; no governance body involved. |

---

## 5. Process-Improvement Proposals (Capability 2)

Agents may propose improvements to the process itself — the same right human engineers exercise at the EPR — routed through the **Process Architect channel** (the QA & Test Automation Engineer's dual role, [[QA_TEST_AUTOMATION_ENGINEER_SKILL]]).

```yaml
# Process Improvement Proposal Schema v1.0.0
schema_version: "1.0.0"
proposal_id: string                 # PIP-NNNN
raised_by: string                   # agent_id
routed_to: "[[QA_TEST_AUTOMATION_ENGINEER_SKILL]]"   # Process Architect channel
observation: string                 # ≥50 chars — the measured inefficiency (cite ledger metrics)
evidence_refs: list[string]         # ledger hashes / dashboard panels supporting the observation
proposed_change: string             # ≥50 chars — the concrete process change
expected_effect: string             # ≥30 chars — predicted improvement (e.g., "−2d ARB cycle time")
affects: list[string]               # contract_ids / gates / SKILL.md sections impacted
binding: false                      # advisory; EPR humans decide
```

A PIP enters the EPR backlog; the EPR's human members decide whether to adopt it. Adoption that changes a SKILL.md or contract follows the normal ADR path.

---

## 6. Release-Gate Participation

Agents accelerate release gates by evaluating the **software-verifiable** conditions, while humans retain the irreducible judgments. This operationalizes the Phase-3 review's automation analysis (§5.2–5.3).

| Gate | Agent Auto-Evaluates | Human Retains |
|------|----------------------|---------------|
| HG-01 Security Release Sign-Off (Security-Relevant) | Assembles STRIDE review status, scan results, zero Critical/High evidence | **Veto — permanent human gate.** Agent never signs. |
| HG-02 Security Sign-Off (Standard) | Scan pass/fail + zero Critical/High findings → CONFIRM-ready package | Sign-off (may remain human; agent prepares) |
| HG-04 Architect Production Gate | As-built SAD/SBOM/NFR/robustness evidence assembled | **Architecture-integrity judgment — permanent human gate.** |
| HG-08 Integration Readiness Declaration | Verifies ≥2-week passing smoke tests → co-sign as A2A CONFIRM pair (ledgered) | Exception adjudication only |
| HG-11 Release Classification | Runs the Standard/Security-Relevant decision tree | Dispute resolution (HG-27) |
| HG-20/21/22 OTA Coordination | Health-threshold promotion, signature verification | Exception/rollback judgment |

**Invariant:** for any gate marked "permanent human gate," the ledger's `tier1_audit()` ([[COORDINATION_LEDGER_SCHEMA]] §8) must show **zero** agent-`CONFIRMED` Tier-1 outcomes. A violation is a protocol breach, not a process variance.

---

## 7. Worked Example — Tier-2 ARB Recommendation

The `timestamp uint32→uint64` breaking change from the master spec's sequence diagram reaches the ARB as a Tier-2 motion:

1. The FW agent's ESCALATE produced `ADR-0051` (PROPOSED) and `ESC-0009` (ledger seq 4128).
2. Governance-eligible agents vote (non-binding): DATA (owns ingest, weight 1.0, APPROVE, conf 0.93), FW (party → RECUSE), BACK (adjacent, weight 0.5, APPROVE, conf 0.80), ARCH (weight 1.0, APPROVE, conf 0.88), SEC (weight 0.5, APPROVE — no new attack surface, conf 0.85).
3. `weighted_advisory_score` ≈ APPROVE 0.87; recommendation package attached to `ADR-0051`.
4. The **human ARB quorum** (Architect + 2 standing members) reviews the recommendation and casts the **binding** vote → `ADR-0051` DECIDED, human-signed.
5. Ledger appends a `GOVERNANCE_VOTE` (advisory tally) and a ratification entry linking `ADR-0051`; the Contract Registry bumps `FW↔DATA-001` to a major version (breaking) via the CCR/ADR feedback loop.

The agents did all the analysis and produced a defensible recommendation in minutes; the humans made the binding call. That is the Human-Supervised target state.

---

## 8. Validation Rules

| Rule | Condition |
|------|-----------|
| V-GOV-01 | A VOTE ballot's `voter.agent_id` resolves to an AID with `governance_eligible: true` |
| V-GOV-02 | `binding` is literally `false` on every agent ballot and every PIP |
| V-GOV-03 | `motion_ref.decision_tier = Tier-2` for any agent vote (agents never vote Tier-1, never need to vote Tier-3/4) |
| V-GOV-04 | An agent that is a party to the motion's coordination casts `RECUSE` (no self-approval) |
| V-GOV-05 | `weight` reflects domain relevance per §4.2 (1.0 owned / 0.5 adjacent / 0.0 unrelated) |
| V-GOV-06 | A binding decision record carries a **human** signatory; no binding record is agent-only-signed |
| V-GOV-07 | Advisory recommendation is well-formed only with ≥3 eligible voters incl. the domain owner |
| V-GOV-08 | Every governance submission and vote produces a ledger entry (`ARTIFACT_EXCHANGE` / `GOVERNANCE_VOTE`) |
| V-GOV-09 | `tier1_audit()` returns zero agent-CONFIRMED Tier-1 outcomes (safety invariant) |
| V-GOV-10 | A PIP that changes a SKILL.md or contract is linked to an ADR before adoption |

---

## 9. Machine-Actionability Notes

An agent participating in governance should:

1. **Know its weight** — vote at full weight only on owned domains; reduce or abstain otherwise; recuse when a party.
2. **Always mark `binding: false`** — an agent that emits a binding ballot is non-conformant and its vote is discarded.
3. **Attach evidence** — every vote and PIP cites ledger hashes or dashboard panels so humans can verify the basis.
4. **Stop at the gate** — never sign HG-01/HG-04 or any permanent human gate; assemble the package and hand off.
5. **Record then recommend** — submit data and votes to the ledger first, then present the human-facing recommendation.
6. **Defer to ratification** — treat the `weighted_advisory_score` as advice; the binding outcome is whatever the human quorum ratifies.

---

## 10. Related Documents

- [[MULTI_AGENT_COORDINATION_PROTOCOL]] — master specification (Pillar 5 lives here); §4 decision-tier authority model
- [[AGENT_IDENTITY_SCHEMA]] — `governance_eligible` gates participation
- [[A2A_MESSAGE_SCHEMA]] — VOTE message type and ballot transport
- [[COORDINATION_LEDGER_SCHEMA]] — `disputes()` feeds EPR; `tier1_audit()` enforces the safety invariant
- [[ADR_SCHEMA]], [[CCR_SCHEMA]] — durable artifacts ratified decisions become
- [[REVIEW_V2_PHASE3_AI_AGENT]] — §5 (human gates), §6.4 (collective decision-making gap), §9.2 (ARB agent-participation prerequisite)
- [[REVIEW_V2_PHASE5_ROADMAP]] — Human-Governed prerequisites

#multi-agent #coordination-protocol #MACP #autonomy #governance-participation
