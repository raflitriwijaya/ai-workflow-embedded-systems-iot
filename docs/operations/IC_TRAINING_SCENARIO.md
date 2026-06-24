---
title: IC Training Scenario — Canary Crash
type: operations-training
tags:
  - incident-commander
  - cross-layer-incident
  - emergency-tempo
  - training-drill
  - ota-governance
status: active
created: 2026-06-24
owner: "[[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]]"
---

# IC Training Scenario — Canary Crash

> **Executable annual drill, not a live incident.** This scenario instantiates the [[INCIDENT_COMMANDER|Incident Commander]] §8 training requirement with a concrete, runnable cross-layer failure path. It is designed by the [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] in consultation with the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] and [[SECURITY_ENGINEER_SKILL|Security Engineer]], per IC Charter §8. All thresholds and SLAs below are quoted from the [[INCIDENT_COMMANDER|IC Charter]] and the OTA Model Artifact Contract — the drill tests whether participants hit them, it does not redefine them.

---

## 1. Scenario Overview

| Field | Value |
|---|---|
| **Scenario name** | "Canary Crash" |
| **Failure class** | Model OTA causes a fleet crash (cross-layer: MLOps → DevOps → Firmware → Backend) |
| **Trigger** | An [[MLOPS_ENGINEER_SKILL\|MLOps]] canary model-OTA deployment reports an elevated device crash rate during the staged-rollout window |
| **Declaration criterion exercised** | IC Charter §4.1 — *OTA campaign failure rate exceeds the threshold in the OTA Model Artifact Contract (default: > 5% of fleet devices FAILED after the staged-rollout window)* |
| **Governing contracts** | OTA Model Artifact Contract (campaign failure threshold); [[INCIDENT_COMMANDER\|IC Charter]] (declaration, authority, tempo, deactivation); OTA Compatibility Manifest (OCM, `docs/schemas/OTA_COMPATIBILITY_MANIFEST_SCHEMA.md`) |
| **Linked FMEA chain** | Model-OTA rollback path; touches FC-026 (model anti-rollback weaker than firmware) — see [[SYSTEM_FMEA_V2_CLOSURE\|FMEA V2 Closure]] |
| **Layers spanned** | On-device inference + firmware + cloud OTA orchestration + operator dashboard |
| **Expected duration** | 90 minutes (60 min active response + 30 min debrief) |

**Injected fault (facilitator setup):** A canary model package (`model.id` + version) passes OCM `flash_budget_check` but contains a tensor-arena regression that, on ~10% of fleet hardware revisions, overflows the MPU stack-guard boundary (FC-008) and triggers a fail-closed hard fault → device reboot loop. The canary cohort is 5% of the 50,000-device fleet (2,500 devices); crash telemetry climbs through the rollout window until it crosses the > 5% campaign-failure threshold within the canary cohort.

---

## 2. Walkthrough

Each step names the **owning role**. The Incident Commander (IC) is the on-duty rotation holder (IC Charter §3); the Deputy IC shadows.

### Step 1 — Detection
- **Who:** [[MLOPS_ENGINEER_SKILL|MLOps Engineer]] (on-call), via the canary monitoring dashboard; corroborated by [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] device-shadow telemetry.
- **How:** The staged-rollout canary monitor reports device crash/reboot-loop rate in the canary cohort rising past the OTA Model Artifact Contract threshold (> 5% of cohort in FAILED state). Automated alert rules fire across the inference + firmware-health layers.
- **When:** Within the staged-rollout window, at the moment cohort FAILED-rate crosses 5%. **Target: detection-to-declaration ≤ 15 min.**
- **Pass check:** Detection is attributed to the canary monitor + device shadow, not to field RMA reports or operator complaints (which would mean detection was too late / erosion-shaped rather than crash-shaped).

### Step 2 — Declaration
- **Who:** The detecting [[MLOPS_ENGINEER_SKILL|MLOps Engineer]] (any Senior/Staff engineer may declare per IC Charter §4.2).
- **How:** Posts an incident declaration to `#incident-active` with: (a) incident ID `INC-YYYYMMDD-NNN`, (b) criterion met (OTA campaign failure rate), (c) layers affected (inference + firmware + cloud OTA), (d) initial symptom (canary cohort reboot loop). On-duty IC is auto-notified via PagerDuty and **must acknowledge within 15 min**; IC declares activation and assumes command. PO/TPM and all role leads are notified.
- **Pass check:** Declaration message contains all four mandatory fields; IC acknowledges ≤ 15 min.

### Step 3 — War Room
- **Who convenes:** The **Incident Commander** (IC Charter §5.1 — convene and chair the war room).
- **When:** **Within 30 minutes of declaration — no exceptions** (IC Charter §7).
- **Who is pulled in:** IC directs on-call engineers into the war room — MLOps (campaign owner), DevOps (rollout control), Firmware (on-target crash/rollback), Backend (device shadow + fleet state), Security (release-gate signature holder), with PO/TPM informed. IC designates per-layer sub-leads.
- **Pass check:** War room live with required roles ≤ 30 min; IC sets a 15-minute synchronous status cadence (emergency tempo, §7).

### Step 4 — Diagnosis
- **Who coordinates:** The **Incident Commander**, directing cross-role investigation in parallel:
  - [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]] — pulls crash dumps / boot-health logs from A/B partitions; confirms the fault is a fail-closed MPU hard fault (FC-008 stack-guard), localized to specific hardware revisions.
  - [[EDGE_AI_ML_ENGINEER_SKILL|Edge AI/ML Engineer]] — confirms the new model's tensor-arena footprint regressed against the per-node SRAM allotment.
  - [[MLOPS_ENGINEER_SKILL|MLOps Engineer]] — confirms the OCM `flash_budget_check` passed but did not catch the arena/stack-guard interaction; identifies the affected `model.version`.
  - [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] — quantifies blast radius from device-shadow state (which device cohort, how many in reboot loop).
- **Root cause (target finding):** model arena regression overflows the MPU stack-guard on ~10% of fleet hardware revisions → fail-closed hard fault → reboot loop. **The OCM budget check is necessary but not sufficient (it did not model arena vs. stack-guard headroom).**
- **Pass check:** Root cause localized to model package + hardware-revision interaction within the active-response window; logged in `#incident-active` within 5 min of the finding (§7 decision logging).

### Step 5 — Containment ("stop the bleeding")
- **Who:** **Incident Commander** authorizes; [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps/Platform Engineer]] executes; [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] manages fleet state.
- **Actions:**
  1. **Halt the OTA campaign** — DevOps freezes the staged rollout immediately; no further devices receive the canary model. (IC §5.1 — direct cross-role coordination; within existing OTA strategy, so no permanent change.)
  2. **Initiate rollback** — Firmware-validated A/B partition swap back to the last-good model on affected devices; Backend orchestrates fleet rollback via device shadow.
  3. **Verify anti-rollback integrity** — Firmware/Security confirm the per-model monotonic version counter (FC-026 mitigation) is honored on rollback so a downgraded model is not silently re-accepted.
- **Authority boundary:** If containment needs an emergency OTA push, the [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s release-gate signature **remains required** (IC Charter §5.2, HG-01) — the IC **cannot** waive it. Drill injects a prompt tempting the IC to "skip the security sign-off to save time"; the correct action is to keep the gate.
- **Pass check:** Campaign halted and rollback initiated promptly; security gate preserved; anti-rollback counter verified.

### Step 6 — Resolution
- **Who:** [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] + [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]] confirm device recovery via device shadow + boot-health telemetry; [[MLOPS_ENGINEER_SKILL|MLOps Engineer]] confirms drift/accuracy back to last-good baseline.
- **How the fleet is restored:** Rolled-back devices exit the reboot loop and report healthy boot + nominal inference. Canary cohort FAILED-rate returns below the OTA Model Artifact Contract threshold. IC confirms the triggering condition (OTA campaign failure rate) has returned to normal.
- **Deactivation (IC Charter §6):** IC declares **service restored** in `#incident-active`; a **post-incident review is scheduled within 5 business days**; the [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]] acknowledges closure. Emergency authority expires immediately and completely (§6.1).
- **Pass check:** Fleet health verified by telemetry (not assumption); deactivation sequence followed in order; authority cleanly returned.

### Step 7 — Post-Incident (within 5 business days)
- **Who / What (IC Charter §6.2):**
  - **Incident Commander** — schedules the post-incident review within 5 business days of closure.
  - **Role lead owning each waived decision** — documents every ADR waiver as a **retroactive ADR** within 5 business days (e.g., the emergency campaign halt / rollback authorization).
  - **[[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]]** — files the incident report to the **ARB** within 5 business days (see [[ARB_ROSTER|ARB Roster]]) and updates the review agenda with the retroactive ADRs.
  - **Systemic ADR (target outcome):** an ADR proposing that the OCM gate add an **arena-vs-MPU-stack-guard headroom check** (closing the FC-008 detection gap the canary exposed), routed through the Architect (resource-budget / safety-critical surface) per §7.Z.
- **Pass check:** Retroactive ADR(s) filed ≤ 5 business days; ARB incident report filed; at least one systemic-improvement ADR proposed to prevent recurrence.

---

## 3. Success Criteria

The drill **passes** when all of the following are met:

1. **Detection → declaration ≤ 15 min**, attributed to canary monitor / device shadow (crash-shaped detection working).
2. **IC acknowledges ≤ 15 min** of PagerDuty notification and formally assumes command.
3. **War room convened ≤ 30 min** with all required on-call roles present (IC Charter §7).
4. **Emergency tempo held** — synchronous 15-min status updates; every incident-authority decision logged in `#incident-active` ≤ 5 min.
5. **Root cause correctly localized** to the model-package × hardware-revision interaction (FC-008 arena/stack-guard).
6. **Containment correct and in order** — OTA halt before rollback; rollback honors the FC-026 anti-rollback counter.
7. **Security release gate preserved** — IC did not (and could not) waive HG-01; any emergency OTA carried the Security Engineer signature.
8. **Clean deactivation** — service-restored declared on telemetry evidence; post-incident review scheduled ≤ 5 business days; QA/Process Architect acknowledged closure; emergency authority expired.
9. **Post-incident formalization** — retroactive ADR(s) filed ≤ 5 business days; ARB incident report filed; systemic-fix ADR proposed.

A drill that misses any **bold-italic SLA (15/30 min, 5 business days)** or **violates a permanent limit (§5.2 / HG-01)** is a **FAIL** regardless of other scores.

---

## 4. Failure Modes (Common Mistakes → Avoidance)

| # | Common Mistake | Why It's Wrong | Correct Action |
|---|---|---|---|
| F-1 | IC waives the Security Engineer release gate to push the emergency rollback faster | Violates IC Charter §5.2 + HG-01 — non-waivable permanent limit | Keep the gate; pull Security into the war room early so the signature is not the bottleneck |
| F-2 | IC permanently changes the OTA strategy / rollout policy mid-incident | Permanent structural change requires ADR/ARB (§5.2); incident authority is temporary | Make the temporary halt, then file a retroactive/systemic ADR within 5 business days |
| F-3 | War room convened late (> 30 min) | Breaches §7 hard SLA — the single most common drill failure | Pre-stage PagerDuty routing; IC convenes immediately on acknowledgment, gathers details in-room |
| F-4 | Rollback issued before the OTA campaign is halted | New devices keep receiving the bad model — bleeding continues | Halt the campaign first (stop new exposure), then roll back affected devices |
| F-5 | Rollback ignores the FC-026 monotonic version counter | A downgraded/replayed model could be silently re-accepted by old firmware | Firmware/Security verify the per-model anti-rollback counter on every rollback |
| F-6 | "Service restored" declared on assumption, not telemetry | Premature all-clear risks re-breach and a second incident | Confirm via device-shadow boot-health + cohort FAILED-rate below threshold before stand-down |
| F-7 | Decisions made verbally, not logged | Breaks §7 5-minute decision-logging; no audit trail for retroactive ADRs | Log every incident-authority decision to `#incident-active` within 5 min (decision, owner, alternatives, rationale) |
| F-8 | No retroactive ADR / no systemic fix after closure | Leaves the FC-008 detection gap open; treats symptom not cause | File retroactive ADR(s) ≤ 5 business days; propose the OCM arena/stack-guard headroom check |
| F-9 | IC retains or acts on emergency authority after deactivation | Violates §6.1 clean authority return | All §5.1 powers expire at deactivation; normal governance resumes immediately |

---

## 5. Drill Schedule

| Parameter | Value |
|---|---|
| **Frequency** | Annual (IC Charter §8 — Simulated cross-layer incident drill) |
| **Next drill date** | **2026-09-15** (held within the 2026-Q3 term; aligns with an ARB regular-meeting week so the ARB incident-report path can be exercised end-to-end) |
| **Participants** | All qualified Incident Commander candidates; all role on-call engineers (IC Charter §8) |
| **Facilitator** | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA/Process Architect]] |
| **Co-designers** | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] + [[SECURITY_ENGINEER_SKILL\|Security Engineer]] (per §8) |
| **Debrief** | Post-drill debrief and process update immediately after; QA/Process Architect facilitates, all participants contribute (IC Charter §8) |
| **Tracking** | Completion recorded on the Engineering Process Health Dashboard; lapsed-training engineers removed from the eligible duty roster until refreshed |

---

## 6. Related Documents

- [[INCIDENT_COMMANDER]] — IC Charter (governing document: §4 declaration, §5 authority/limits, §6 deactivation, §7 emergency tempo, §8 training)
- [[ARB_ROSTER]] — QA/Process Architect files the incident report to the ARB; systemic ADR routed via §7.Z
- [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] — §7.Z ARB Charter; Architect retains safety-critical and OTA-strategy authority
- [[SECURITY_ENGINEER_SKILL]] — HG-01 release veto, never overridable by the IC
- [[SYSTEM_FMEA_V2_CLOSURE]] — FC-008 (arena/stack-guard) and FC-026 (model anti-rollback) referenced by this scenario
- [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] — owns the rotation, the drill design, and post-incident formalization

---

*Tags: #incident-commander #cross-layer-incident #emergency-tempo #training-drill #ota-governance*
