---
title: ARB Roster — 2026-Q3
type: governance-instantiation
tags:
  - ARB
  - distributed-governance
  - architect-singularity
  - roster
status: active
created: 2026-06-24
owner: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]]"
---

# ARB Roster — 2026-Q3

> **Instantiation of a charter, not a new authority.** This roster names the seats defined by the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] §7.Z Architecture Review Board (ARB) Charter. It is subordinate to §7.Z — where this document and §7.Z disagree, §7.Z is authoritative. This roster confers no authority beyond what §7.Z grants; it only fills the named seats, the rotation, and the meeting logistics.

---

## 1. Governing Document

| Field | Value |
|---|---|
| **Governing charter** | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Embedded Systems Architect]] §7.Z (ARB Charter) |
| **Authority scope** | As defined in §7.Z ARB Decision Authority + Decision Limits — not extended here |
| **Decision record format** | ARB Decision Record (same Markdown format as ADR), tagged `#ARB`, stored `docs/arb/decisions/arb-NNNN.md` |
| **Current term** | 2026-Q3 (1 July 2026 – 30 September 2026) |
| **Annual charter review** | First ARB meeting of December (§7.Z Operations) |

This roster instantiates the membership structure in §7.Z. It is **not** a SKILL.md and does not carry the 5-field skill-card frontmatter; it follows the operations/governance-instantiation convention used by [[INCIDENT_COMMANDER|Incident Commander]].

---

## 2. Standing Members (5)

Seats name **roles**, not persons — the ecosystem is contract-defined, not an org chart. The on-duty holder of each role occupies the seat.

| Seat | Role | Charter Function |
|---|---|---|
| **Chair** | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Embedded Systems Architect]] | Convenes, facilitates, and documents ARB meetings; retains sole authority over the five reserved Decision Limit classes; has standing to halt any vote on safety-critical grounds |
| **Vice Chair** | Deputy Architect (`ARCH-DEP`) | Chairs in the Architect's absence; non-breaking ADR authority only; may convene the Urgent Meeting (§7.Z) when the Architect is unavailable |
| **Member** | Senior [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] | Firmware/on-target voice on contract MINOR/PATCH, Flash↔SRAM rebalancing, and on-device feasibility |
| **Member** | Senior [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend/Cloud Engineer]] | Cloud/fleet-scale voice on contract evolution, scalability, and OTA orchestration implications |
| **Member** | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] | Security surface assessment; signs the security/architecture impact note on non-novel technology adoption; additional standing to escalate any undisclosed-security-surface decision to the Architect within 1 business day (§7.Z Escalation); retains HG-01 release veto independent of ARB |

The Security Engineer's HG-01 release veto and the Architect's HG-04 production gate are **permanent Tier-1 gates** and are not subject to ARB majority vote.

---

## 3. Rotating Member Slot

Per §7.Z: **one additional Senior Engineer from the role most affected by the current release scope, rotating per release cycle, invited by the Chair.** The rotating member votes as a full member of the convened quorum but does **not** count toward the standing-member quorum requirement (§4).

| Rotation | Release Cycle | Most-Affected Role (rationale) | Rotating Member |
|---|---|---|---|
| **Current** | 2026-Q3 / Cycle 1 (Jul) | Edge AI/ML — model-OTA cadence dominates this cycle's scope | Senior [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML Engineer]] |
| Next +1 | 2026-Q3 / Cycle 2 (Aug) | MLOps — OTA Compatibility Manifest + drift monitoring rollout | Senior [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] |
| Next +2 | 2026-Q3 / Cycle 3 (Sep) | DevOps/Platform — staged-rollout + canary tooling hardening | Senior [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps/Platform Engineer]] |
| Next +3 | 2026-Q4 / Cycle 1 (Oct) | Data Engineering — telemetry-ingest scaling (SCALE-5) review | Senior [[DATA_ENGINEER_SKILL\|Data Engineer]] |

The Chair confirms the most-affected role at the close of each release cycle and issues the invitation before the next cycle's first ARB meeting. If the release scope shifts, the Chair may re-assign the rotating slot and records the change in the meeting minutes.

---

## 4. Quorum Verification

Per §7.Z: **Quorum = 3 of 5 standing members, including at least one of the Architect (Chair) or Deputy Architect (Vice Chair).**

A convened meeting is quorate when **all** of the following hold:

1. **Count:** ≥ 3 of the 5 standing seats (§2) are present.
2. **Leadership anchor:** at least one of {Chair, Vice Chair} is present.
3. **Rotating member excluded from count:** the rotating member (§3) may attend and vote but does **not** satisfy the 3-of-5 standing-member count.

**Worked examples:**

| Present | Quorate? | Reason |
|---|---|---|
| Chair + Sr. Firmware + Security | ✅ Yes | 3 standing, includes Chair |
| Vice Chair + Sr. Backend + Security | ✅ Yes | 3 standing, includes Vice Chair |
| Sr. Firmware + Sr. Backend + Security | ❌ No | 3 standing but neither Chair nor Vice Chair present |
| Chair + Sr. Firmware + Rotating (Edge AI/ML) | ❌ No | Only 2 standing members; rotating does not count |

A non-quorate meeting may discuss but may **not** vote. Decisions requiring a vote are deferred to the next quorate session or, for Tier 1 (CRITICAL) matters when the Architect is unavailable, handled via the §7.Z Urgent Meeting path.

---

## 5. Meeting Cadence

| Parameter | Value |
|---|---|
| **Regular meeting** | Bi-weekly, 60 minutes (per §7.Z Operations) |
| **Day/time** | Every **second Tuesday, 14:00–15:00 local team time** |
| **2026-Q3 dates** | Jul 7, Jul 21, Aug 4, Aug 18, Sep 1, Sep 15, Sep 29 |
| **Standing agenda** | Open Tier 2 decisions → escalated CCRs → ADR review queue → expanded-authority queue (contract MINOR/PATCH, non-novel tech eval, SE prioritization, agent proposals) → cross-role architecture concerns → upcoming technology-transfer assessments |
| **Urgent meeting** | Convened within 1 business day by Chair or Vice Chair for Tier 1 (CRITICAL) decisions when the Architect is unavailable (§7.Z) |
| **Chair** | Architect; Vice Chair chairs in the Architect's absence |
| **Minutes & decisions** | Recorded as ARB Decision Records (`#ARB`); expanded-authority decisions additionally tagged `#expanded-authority`; ADR-equivalent decisions cross-referenced from [[ADR_INDEX\|ADR Index]] |

---

## 6. Escalation Path

Per §7.Z Escalation, aligned with the Architect §7 escalation chain (Architect → TPM → CTO):

```
ARB decision
   │
   ├─▶ Any standing member may escalate to the Architect within 5 business days
   │     (Security Engineer: within 1 business day for undisclosed security surface)
   │
   ▼
Architect  — upholds / modifies / reverses via a superseding ADR
   │
   ▼
CTO / Engineering Lead  — final escalation for deadlocks the Architect cannot resolve
```

- **ARB → Architect:** any standing member, within 5 business days of the decision; the Security Engineer holds an additional 1-business-day fast path for any decision with an undisclosed security surface.
- **Architect → CTO:** matters the Architect cannot resolve, or where the Architect's own decision is contested, escalate to the CTO/Engineering Lead per the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] §7 escalation path.
- The five **reserved Decision Limit** classes (platform/MCU selection, protocol/topology changes, MAJOR contract changes, budget changes > ±10%, OTA-strategy changes, security-baseline modifications, production-gate sign-off, safety-critical paths, novel-technology adoption) are never resolved by ARB vote — they route directly to the Architect + ADR regardless of quorum.

---

## 7. Term & Next Actions

| Item | Value |
|---|---|
| **Current term** | 2026-Q3 (1 July – 30 September 2026) |
| **Next roster review** | First ARB meeting of 2026-Q4 (Oct), re-confirm seats + rotation |
| **Annual charter review** | First ARB meeting of December (§7.Z) — membership, authority scope, operations |
| **Roster publisher** | Architect (Chair); changes recorded in ARB minutes and reflected here |

---

## 8. Related Documents

- [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] §7.Z — ARB Charter (governing document; authoritative)
- [[ADR_INDEX]] — ARB decisions requiring an ADR are cross-referenced here
- [[INCIDENT_COMMANDER]] — IC files the incident report to the ARB within 5 business days of incident closure
- [[SECURITY_ENGINEER_SKILL]] — HG-01 release veto; Security Engineer ARB seat
- [[SCHEMA_INDEX]] — ADR / CCR schemas governing ARB decision records

---

*Tags: #ARB #distributed-governance #architect-singularity #roster*
