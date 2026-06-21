---
title: Runtime Incident Commander
type: operations-function
tags:
  - incident-commander
  - cross-layer-incident
  - emergency-tempo
  - resilience
status: active
created: 2026-06-21
owner: "[[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]]"
---

# Runtime Incident Commander

> **This is a rotating duty, not a role.** The Incident Commander function activates during declared cross-layer incidents and deactivates upon resolution. It does not add headcount and does not change the permanent authority structure of any role.

---

## 1. Purpose

The Runtime Incident Commander function exists to close [[REVIEW_V2_PHASE4_EMERGENT|Phase 4]] gap EN-6: "No runtime cross-layer incident owner." When a live incident spans multiple architectural layers — device hardware, firmware, on-device inference, cloud services, operator dashboard — no single role under the normal governance cadence can coordinate response fast enough. The Incident Commander holds temporary, scoped authority to direct cross-role coordination and make time-critical decisions until the incident is resolved.

---

## 2. Qualification

To be eligible for Incident Commander duty, an engineer must:

1. Hold **Senior or Staff engineer** level within any of the 14 defined roles in this ecosystem.
2. Have completed the **annual incident command training**, including one simulated cross-layer incident drill (see §8).
3. Have **shadowed at least one live incident** as Deputy Incident Commander before serving as primary.

Eligibility is tracked by the [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] and maintained on the Engineering Process Health Dashboard.

---

## 3. Rotation Schedule

| Parameter | Definition |
|---|---|
| **Cadence** | Weekly rotation (resets every Monday 00:00 local team time) |
| **Publisher** | [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] |
| **Visibility** | Engineering Process Health Dashboard; published at least 4 weeks in advance |
| **Designations** | Each rotation week names one primary Incident Commander and one Deputy Incident Commander |
| **Swap policy** | Swaps are permitted with ≥48 hours notice; the [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] must update the dashboard before the swap takes effect |

The Deputy assumes command if the primary is unavailable, unreachable within 10 minutes of a declaration, or needs relief during a prolonged incident (>4 hours active response).

---

## 4. Activation

### 4.1 Declaration Criteria

An incident **must** be declared when any one of the following conditions is confirmed:

| Trigger | Threshold |
|---|---|
| **SLO breach spanning ≥2 architectural layers** | Any SLO breach simultaneously affecting two or more of: device hardware/firmware, on-device inference, cloud backend, data pipeline, operator dashboard |
| **Confirmed security incident** | Any confirmed or high-confidence compromise of device, firmware, cloud credentials, PKI, or data |
| **OTA campaign failure rate** | Campaign failure rate exceeds the threshold defined in the OTA Model Artifact Contract (default: >5% of fleet devices in FAILED state after the staged rollout window) |
| **Field device failure rate** | Fleet-wide device failure rate exceeds 2× the steady-state RMA rate for any 24-hour window |

Any engineer observing an automated alert that meets a declaration criterion may and should declare an incident. Automated monitoring may also auto-declare when configured alert rules are breached across multiple layers simultaneously.

### 4.2 Declaration Process

1. **Any Senior/Staff engineer** (or automated monitoring system) posts an incident declaration in the designated incident channel: `#incident-active` (or equivalent).
2. Declaration message **must include**: (a) incident ID (auto-assigned or `INC-YYYYMMDD-NNN`), (b) declaration criterion met, (c) layers affected, (d) initial symptom description.
3. The designated on-duty Incident Commander is **automatically notified** via PagerDuty (or equivalent on-call routing) and must **acknowledge within 15 minutes**.
4. The Incident Commander **declares activation** in the incident channel, confirming they have assumed command.
5. All role leads and the [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] receive immediate notification upon declaration.

---

## 5. Authority During Active Incident (Temporary and Incident-Scoped)

The following authorities are **granted only while an incident is declared active** and **expire immediately upon deactivation** (§6). They do not persist, do not establish precedent, and do not modify any role's permanent authority.

### 5.1 What the Incident Commander CAN do

| Authority | Scope |
|---|---|
| **Direct cross-role coordination** | Request any role's on-call engineer to join the war room, assign tasks, and set response priorities across all 14 roles |
| **Request role resources** | Pull any on-call engineer into the war room within the existing on-call roster and pre-approved incident response budget — no new headcount or expenditure authorization required |
| **Make time-critical technical decisions** | Authorize decisions that would normally require ADR or ARB approval, provided they remain within the existing resource budgets and security baseline |
| **Waive non-safety ADR requirements** | Suspend the requirement for pre-decision ADR documentation for the duration of the incident; all waived decisions are retroactively documented (§6) |
| **Declare emergency OTA deployment** | Authorize an emergency OTA campaign outside the scheduled release calendar, subject to the [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s release gate signature (which remains required — see §5.2) |
| **Convene and chair the war room** | Set agenda, control information flow, and designate sub-leads for specific layers within the war room |
| **Set emergency-tempo communication cadence** | Override the normal asynchronous communication cadence and require synchronous status updates on the emergency-tempo schedule (§7) |
| **Declare incident resolved** | Trigger the deactivation sequence (§6) |

### 5.2 What the Incident Commander CANNOT do — Permanent Limits

These limits **cannot be waived by the Incident Commander, the war room, or any combination of role leads**. They require the permanent authority-holder and normal governance process regardless of incident status.

| Prohibited Action | Why |
|---|---|
| **Override the [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s release veto** | Security baseline integrity is a non-negotiable safety property; the Security Engineer's release gate remains in full effect during incidents, including emergency OTA |
| **Change architecture, inter-role contracts, or resource budgets permanently** | Permanent structural changes require ADR/ARB; incident-scope decisions are temporary by definition |
| **Authorize expenditure beyond the pre-approved incident response budget** | Financial authority requires the normal approval chain; the Incident Commander manages within pre-authorized budgets only |
| **Override safety-critical design decisions** | Any decision touching device safety margins, physical safety constraints, or fail-safe behaviors requires the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] and [[SECURITY_ENGINEER_SKILL|Security Engineer]] using the normal safety-review process |
| **Modify the security baseline** | Cryptographic parameters, authentication requirements, key management, and access control policies remain under the [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s exclusive authority |
| **Retain any authority after deactivation** | Emergency powers expire at deactivation; no emergency authority carries forward into normal operations |

---

## 6. Deactivation

The incident is **closed** when all of the following are true:

1. The Incident Commander declares **service restored** in the incident channel, with confirmation that the triggering SLO breach, security incident, OTA failure, or device failure rate has returned to normal operating thresholds.
2. A **post-incident review** is scheduled within 5 business days of declaration (it does not need to have occurred — only scheduled).
3. The [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] acknowledges the closure in the incident channel, confirming the post-incident review is on the calendar.

### 6.1 Clean Authority Return

Upon deactivation, authority returns to the normal governance structure **immediately and completely**:

- The Incident Commander's temporary authorities (§5.1) expire.
- All role leads resume normal governance cadence.
- No emergency-tempo overrides remain in effect.
- No decision made under incident authority persists as a policy without formal ADR.

### 6.2 Mandatory Post-Closure Formalization (within 5 business days)

| Obligation | Owner | Deadline |
|---|---|---|
| Schedule post-incident review | Incident Commander | Within 5 business days of closure |
| Document every ADR waiver as a retroactive ADR | Role lead who owns the waived decision | Within 5 business days of closure |
| File incident report to the ARB | [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] | Within 5 business days of closure |
| Update the post-incident review agenda with retroactive ADRs | [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] | Before the post-incident review |

---

## 7. Emergency Tempo Protocol

While an incident is declared active, the following communication and decision tempo replaces the normal quarterly governance cadence:

| Protocol Element | Specification |
|---|---|
| **War room convene time** | Within **30 minutes** of incident declaration — no exceptions |
| **Status update cadence** | Every **15 minutes** during active response, in the incident channel |
| **Decision logging** | Every decision made under incident authority is logged in the incident channel within **5 minutes** of the decision, with: the decision made, who made it, the alternatives considered, and the rationale |
| **Escalation path** | If the Incident Commander cannot reach a required role within 15 minutes, the [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] is notified and may escalate to CTO within 30 minutes |
| **All-clear / stand-down** | When the triggering condition is resolved, the Incident Commander posts a stand-down message and transitions to deactivation (§6) |
| **Prolonged incident shift change** | If the incident exceeds 4 hours, the Deputy assumes command to allow the primary to rest; handoff is documented in the incident channel with a current-state briefing |

---

## 8. Training Requirements

| Requirement | Frequency | Participants |
|---|---|---|
| **Incident command training** (classroom/async module) | Annual | All Senior/Staff engineers across all 14 roles |
| **Simulated cross-layer incident drill** | Annual | All qualified Incident Commander candidates; all role on-call engineers |
| **Deputy shadowing** | Once before first primary duty | Each new Incident Commander candidate |
| **Post-drill debrief and process update** | After each drill | [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] facilitates; all participants contribute |

The annual drill scenario is designed by the [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] in consultation with the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] and [[SECURITY_ENGINEER_SKILL|Security Engineer]] to cover a realistic cross-layer failure path (e.g., hardware voltage anomaly → firmware crash → corrupted telemetry → cloud alert → OTA rollback failure).

Training completion is tracked on the Engineering Process Health Dashboard. An engineer whose training has lapsed is removed from the eligible duty roster until training is refreshed.

---

## 9. Relationship to Normal Governance

| Dimension | Normal Operations | Active Incident |
|---|---|---|
| **Decision authority** | ADR/ARB process, role-level authority | Incident Commander + permanent safety limits |
| **Communication cadence** | Asynchronous, quarterly reviews | Synchronous, 15-minute updates |
| **OTA authorization** | Scheduled release calendar, ADR | Emergency OTA (Incident Commander + Security Engineer gate) |
| **Cross-role coordination** | Voluntary, contract-driven | Directed by Incident Commander |
| **Documentation** | Pre-decision ADR | Post-decision retroactive ADR (within 5 business days) |

The Incident Commander function is **not a shadow ARB**. It does not review, approve, or modify architectural decisions outside the incident scope. It is a time-limited coordination authority that compresses the governance tempo only for the duration of the declared incident.

---

## 10. Related Documents

- [[REVIEW_V2_PHASE4_EMERGENT]] — Phase 4 gap EN-6 that this function addresses
- [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] — QA/Process Architect owns the rotation schedule and post-incident formalization
- [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] — Architect retains permanent authority over safety-critical design decisions
- [[SECURITY_ENGINEER_SKILL]] — Security Engineer's release veto is never overridable by the Incident Commander
- [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL]] — PO/TPM receives immediate declaration notification and escalation path

---

*Tags: #incident-commander #cross-layer-incident #emergency-tempo #resilience*
