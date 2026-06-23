---
title: "Architecture Review Board (ARB) — Instantiated Charter"
date: 2026-06-23
status: final
tags:
  - arb
  - embedded-iot
  - distributed-governance
  - architect-singularity
  - expanded-authority
cssclass: governance-doc
---

# Architecture Review Board (ARB) — Instantiated Charter

> **Subordinate, non-superseding instantiation.** This document operationalizes the ARB (Architecture Review Board) charter defined normatively in [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] §7.Z. The skill-card §7.Z is **authoritative**; where this document and §7.Z conflict, §7.Z governs and this file is corrected to match. Nothing here grants the ARB authority beyond the §7.Z Decision Limits.
> **Owner:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] (Chair) · **Version:** 1.0.0 · **Ratified by:** [[adr-0001|ADR-0001]].

---

## 1. Purpose & Authority Source

The ARB is a standing governance body that distributes architectural decision-making capacity, reducing the Architect as a single point of failure and accelerating resolution of routine architectural questions. It was established during CR-1 (Critical Remediation 1) with limited caretaker authority and expanded under a Phase 5 Long-Term Bet (LTB) into a collective governance institution — the primary structural mitigation for EN-1 (Emergent Property 1: Architect Singularity) identified in [[REVIEW_V2_SKILL_REPORT|Review Part 2]].

This instantiation closes the CLAUDE.md §6.2 gap (`ARB quorum composition, member list, meeting cadence`) by surfacing the §7.Z provisions in operational form. It introduces **no new decision authority**; it adds only operational mechanics (seat-distinctness, quorum worked examples, tie-breaking, scheduling, and the ARB Decision Record template) that §7.Z leaves to the Chair.

**Governing principle:** The Architect remains Chair and retains sole authority over the nine reserved Decision Limits in §6 below. The ARB never decides a reserved class regardless of quorum, vote margin, or autonomy phase. #distributed-governance #architect-singularity

---

## 2. ARB Membership

**Standing Members (5 seats):**

| Seat | Role | ARB Function | Appointment Mechanism |
|---|---|---|---|
| S1 | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] | **Chair** | Ex officio (the Architect) |
| S2 | Deputy Architect — see [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §1 | **Vice Chair** | Appointed by the Architect with CTO (Chief Technology Officer) concurrence; re-designated annually |
| S3 | Senior [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]] | Standing voting member | Designated by the Architect from the Firmware Staff/Senior tier |
| S4 | Senior [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] | Standing voting member | Designated by the Architect from the Backend/Cloud Staff/Senior tier |
| S5 | [[SECURITY_ENGINEER_SKILL|Security Engineer]] | Standing voting member; holds the §7.Z security-escalation standing | Ex officio (the Security Engineer) |

**Rotating Member (1 seat):**

| Seat | Role | ARB Function | Appointment Mechanism |
|---|---|---|---|
| R1 | One additional Senior Engineer from the role **most affected by the current release scope** | Rotating voting member | Invited by the Chair; rotates per release cycle (see §5) |

**Operational instantiation rules (mechanics §7.Z leaves to the Chair):**
- **Distinct seat-holders.** Each of the five standing seats must be held by a **distinct individual** so that quorum reflects five independent voices. Because the Deputy Architect (S2) is drawn from the Staff Firmware or Staff Backend/Cloud tier, the person serving as Deputy must **not** simultaneously occupy S3 or S4; a different Senior engineer fills the affected discipline seat. This preserves the §7.Z bus-factor intent. #bus-factor
- **Named appointments.** The individuals occupying S2–S5 and R1 are recorded in the ARB roster maintained by the Architect and CTO; appointment of specific humans is a management action and is **not** performed by any AI agent. This charter defines the **seats**, not the persons.
- **Agent participation.** MACP (Multi-Agent Coordination Protocol) L2 (Governance Participant) agents may submit data and cast **non-binding advisory votes** only; they hold no seat and are not counted toward quorum. Binding authority is human-only (CLAUDE.md §6.2, §7.3).

---

## 3. Quorum Rule

**Quorum = 3 of the 5 standing members, and the 3 must include at least one of the Architect (S1) or Deputy Architect (S2).** (Verbatim from §7.Z.) The rotating member (R1) may participate and vote but does **not** count toward the standing-member quorum minimum.

**Decision rule:** Within the chartered authority, ARB decisions pass by **majority vote of the quorum present**. With the minimum quorum of 3, a majority is 2. A tie is broken by the Chair (or, in the Chair's absence, the acting Chair / Vice Chair); if the tie-breaker is conflicted on the matter, the decision escalates to the Architect rather than passing on a tie.

**Quorum worked examples:**

| Members present | Quorum valid? | Reason |
|---|---|---|
| Architect + Senior Firmware + Security | ✅ Valid | 3 standing members, includes the Architect |
| Deputy + Senior Firmware + Senior Backend/Cloud | ✅ Valid | 3 standing members, includes the Deputy |
| Deputy + Senior Backend/Cloud + Security + Rotating | ✅ Valid | 3 standing members (R1 not counted), includes the Deputy |
| Senior Firmware + Senior Backend/Cloud + Security | ❌ Invalid | 3 standing members but neither Architect nor Deputy present — **no vote may be held**; reschedule or co-opt S1/S2 |
| Architect + Security only | ❌ Invalid | Only 2 standing members — below quorum |

**Security-relevant matters:** Any decision touching the security baseline requires the [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s co-approval and remains a reserved Decision Limit (§6) — it is **not** resolvable by majority vote even at quorum. #security-impact

---

## 4. Meeting Cadence & Operations

- **Regular meeting:** **Bi-weekly, 60 minutes** (verbatim from §7.Z). The specific recurring slot is set by the Chair and published on the engineering team calendar; quorum (§3) is confirmed at least 1 business day in advance. If quorum cannot be reached, the Chair reschedules within 3 business days, or routes Tier 3–4 items to asynchronous Propose→Confirm per MACP.
- **Urgent meeting:** Convened within **1 business day** by the Chair or Vice Chair for Tier 1 (CRITICAL) decisions when the Architect is unavailable (§7.Z). Tier 1 outcomes remain human-decided permanent HITL (Human-in-the-Loop) gates per CLAUDE.md §6.3 / §6.6.
- **Standing agenda** (per §7.Z): (1) open Tier 2 (HIGH) decisions from the Decision SLA queue; (2) escalated CCRs (Contract Clarification Records); (3) ADR (Architecture Decision Record) review queue; (4) expanded-authority decision queue — contract MINOR/PATCH changes, non-novel technology evaluations, SE (Sustaining Engineering) prioritization, agent proposals; (5) cross-role architecture concerns; (6) upcoming technology-transfer assessments from the [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]]; (7) weekly integration smoke-test results review per [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §3.3.
- **Decision records:** Every ARB decision is recorded per §7 below.

---

## 5. Rotating Member Policy

- **One additional Senior Engineer** joins the ARB per **release cycle**, selected from the role **most affected by the current release scope** (e.g., [[DATA_ENGINEER_SKILL|Data]] for a telemetry-schema release; [[MLOPS_ENGINEER_SKILL|MLOps]] for a model-rollout release; [[HARDWARE_ENGINEER_SKILL|Hardware]] for a board-revision release).
- **Invited by the Chair** at the first ARB meeting of each release cycle; the invitation and its rationale are minuted.
- The rotating member holds a **full advisory and voting voice** on agenda items within ARB authority but is **not counted toward the standing-member quorum minimum** (§3).
- Purpose: bring directly-affected discipline expertise into routine architectural decisions and widen architectural fluency across the engineering org over time, reinforcing the EN-1 mitigation. #distributed-governance

---

## 6. ARB Decision Authority & Reserved Limits (cross-reference)

This is an operational summary; the **normative list lives in §7.Z**. The ARB decides the following **by majority vote of quorum**:

**Original authority (CR-1):** Tier 2 (HIGH) architecture decisions; non-breaking ADRs; escalated CCRs unresolved within 3 business days; routine budget rebalancing within tolerance bands; architecture implications of non-novel technology transfer; architecture exploration spikes.

**Expanded authority (Phase 5 LTB, tag #expanded-authority):** (1) contract **MINOR/PATCH** SemVer (Semantic Versioning) changes; (2) Flash↔SRAM (Static Random-Access Memory) resource rebalancing **1×–2×** tolerance band (≤ ±10%) with verified ≥ 15% post-trade headroom; (3) non-novel technology evaluation/adoption; (4) SE backlog prioritization meeting all four eligibility conditions; (5) agent-proposed optimizations in Human-Supervised / Human-Governed phases only.

**Reserved Decision Limits — NOT delegated; Architect + ADR required (verbatim scope from §7.Z):**
1. Platform / MCU (Microcontroller Unit) / SoC (System on Chip) selection and deprecation.
2. Protocol or communication-topology changes.
3. **MAJOR** contract version changes (breaking changes, new contracts, deprecations).
4. Resource budget creation/deletion/rebalancing **beyond 2×** tolerance (> ±10%).
5. OTA (Over-the-Air) strategy changes.
6. Security-baseline modifications (require Security Engineer co-approval + ADR tagged #security-impact).
7. Production release-gate architecture sign-off (non-delegable).
8. Any decision affecting a safety-critical path (Architect may halt any ARB vote on safety-critical grounds).
9. Novel-technology adoption (novelty determination is the Architect's discretion when disputed).

---

## 7. ARB Decision Record Template

Per §7.Z, ARB decisions are recorded **in the same Markdown format as ADRs**, tagged `#ARB`. ARB decisions that would normally require an ADR are **cross-referenced from the ADR repository** ([[ADR_INDEX|ADR Index]]); decisions made under expanded authority are additionally tagged `#expanded-authority`.

- **ID convention:** `arb-NNNN` (zero-padded, sequential; e.g., `arb-0001`) — parallel to the `adr-NNNN` convention in [[ADR_INDEX|ADR Index]].
- **Storage:** `docs/arb/decisions/arb-NNNN.md` (append-only; records are immutable once `DECIDED`, superseded by a new record).
- **Tagging:** `#ARB` (the §7.Z-canonical record tag) **and** `#arb-decision` (kebab-case navigational tag, per the CLAUDE.md §3.5 body-tag convention and this instantiation's directive). See §9.

```yaml
---
title: "ARB-NNNN — <imperative decision title>"
id: "ARB-NNNN"
date: "YYYY-MM-DD"
status: "DECIDED"            # PROPOSED | DECIDED | DEPRECATED | SUPERSEDED | REJECTED
authority_basis: "ORIGINAL"  # ORIGINAL (CR-1) | EXPANDED (Phase 5 LTB)
decision_class: "TACTICAL"   # STRATEGIC | TACTICAL | LOCAL (per ADR_SCHEMA)
tier: "CROSS-CUTTING"        # one of the 10 ADR_SCHEMA tier values
reserved_limit_check: "CLEAR"  # CLEAR = no §6 reserved limit touched; else ESCALATE-TO-ARCHITECT
quorum_present:               # ≥3 standing, incl. Architect or Deputy
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "[[FIRMWARE_ENGINEER_SKILL]]"
  - "[[SECURITY_ENGINEER_SKILL]]"
vote_tally: { for: 3, against: 0, abstain: 0 }
affected_contracts:          # contract IDs touched (MINOR/PATCH only under expanded authority)
  - contract_id: "ROLE-A↔ROLE-B-NNN"
    impact_description: "<additive field / clarification>"
cross_referenced_adr: null   # ADR-NNNN when the decision would normally require an ADR
tags:
  - ARB
  - arb-decision
  - expanded-authority      # include only for expanded-authority decisions
---

# ARB-NNNN — <imperative decision title>

## Context
<situation forcing the decision; ≥50 chars>

## Decision
<what the ARB decided and why; ≥50 chars>

## Authority & Reserved-Limit Check
<state ORIGINAL or EXPANDED authority; confirm no §6 reserved limit is touched —
if any reserved limit applies, the item is escalated to the Architect and NOT decided here>

## Consequences
<what changes as a result; affected consumers notified>

## Escalation Window
Any standing member may escalate this decision to the Architect within 5 business days
(Security Engineer: within 1 business day for an undisclosed security surface). The Architect
may uphold, modify, or reverse via a superseding ADR.
```

---

## 8. Escalation & Annual Review

- **Escalation:** Any standing member may escalate any ARB decision to the Architect within **5 business days**; the Architect may uphold, modify, or reverse it via a superseding ADR. The [[SECURITY_ENGINEER_SKILL|Security Engineer]] has additional standing to escalate any decision with an undisclosed security surface within **1 business day** (§7.Z).
- **Annual review:** This charter and §7.Z are reviewed at the **first ARB meeting of December**. Membership, authority scope, and operations are updated as the org matures; expanded-authority items are evaluated for permanence or rollback based on decision-quality and audit-trail evidence.

---

## 9. Alignment & Governance Notes

- **§7.Z is authoritative.** This file is a subordinate instantiation. Any future edit to §7.Z that changes membership, quorum, cadence, authority, or limits must be mirrored here within the Architect's drift-monitoring cadence ([[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §3.6).
- **Tag reconciliation.** §7.Z mandates `#ARB` on ARB Decision Records; this instantiation's directive requested `#ARB-decision`. To satisfy both while honoring the CLAUDE.md §3.5 kebab-case body-tag rule, records carry **both** `#ARB` (charter-canonical) and `#arb-decision` (kebab-case navigation). No invented semantics — both denote an ARB Decision Record.
- **No invented facts.** Named human seat-holders, meeting day/time, and release-cycle boundaries are management/operational data maintained by the Architect/CTO and are intentionally not fabricated here (CLAUDE.md §1 measure-first principle).
- **Bootstrap ratification.** Adoption of this charter instantiation is recorded in [[adr-0001|ADR-0001 — Adoption of ARB Charter and ADR Process]].

#ARB #distributed-governance #expanded-authority #architect-singularity #bus-factor
