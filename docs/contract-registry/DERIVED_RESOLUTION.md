---
title: "DERIVED Contract Resolution — RATIFY / MEDIATE Dispositions"
date: 2026-06-24
status: draft
tags:
  - contract-registry
  - embedded-iot
  - machine-parseable
cssclass: protocol-spec
---

# DERIVED_RESOLUTION.md

> Architect disposition of the 10 `DERIVED` / provisional interface contracts flagged in the [[REGISTRY_INDEX|Contract Registry Index]]. Each `DERIVED` edge has **no direct §6 contract on either role's SKILL.md** and therefore mandates a perpetual `COUNTER` (never a binding `CONFIRM`) under its `x-macp.source_status`. That behaviour is correct but leaves the edge in limbo and caps agent autonomy. This document resolves each edge to one of: **(A) RATIFY** — author a real §6 contract via a [[CCR_SCHEMA|CCR]] because direct coordination is needed; or **(B) MEDIATE** — confirm no direct contract is needed and coordination flows through existing, already-ratified paths.
>
> Authored under the Embedded Systems Architect's §2 authority over interface contracts and system/data-flow topology (see [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] §2, §6, §7). New §6 contracts (RATIFY) are a reserved Architect decision class ([[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARCH]] §7.Z Decision Limits — "MAJOR contract version changes … new contracts … require Architect + ADR"). Confirming an edge as permanently mediated is a registry-governance disposition routed to the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARB]] for ratification (see §"Governance & Next Steps").

---

## 1. Method & Decision Criteria

An edge is evaluated **RATIFY** only when **all** of the following hold; otherwise it is **MEDIATE**:

1. A recurring, direct artifact exchange exists between the two roles that is **not** already owned by a third role's ratified contract.
2. The mediation path is **lossy or latency-unacceptable** for that artifact (a multi-hop relay would degrade the deliverable).
3. Grounding exists in **both** roles' SKILL.md §2 (Owns) and §5 (Deliverables) for the proposed `Provides` / `Requires` — per the Measure-First principle, no responsibility may be invented to justify a contract.

**Governing constraints applied** (CLAUDE.md §1): contract-first (no invented coordination); measure-first (no fabricated role responsibilities); honesty over polish (§10.3 — the honest outcome is reported, not balanced for variety).

---

## 2. Disposition Summary

| # | Edge | Registry ID | Decision | Mediation path (primary) |
|---|---|---|---|---|
| 1 | FE ↔ BIZ | `FE↔BIZ-001` | **MEDIATE** | BIZ → PO → FE (requirements) + `DATA↔FE-001` (serving) |
| 2 | QA ↔ BIZ | `QA↔BIZ-001` | **MEDIATE** | QA → PO → BIZ (`QA↔PO-001` → `PO↔BIZ-001`); `DEVOPS↔BIZ-001` for SLA reliability |
| 3 | HW ↔ DATA | `HW↔DATA-001` | **MEDIATE** | HW → FW → DATA (`HW↔FW-001` → `FW↔DATA-001`); `HW↔ML-001` characterization |
| 4 | HW ↔ MLOPS | `HW↔MLOPS-001` | **MEDIATE** | ARCH → MLOPS (`ARCH↔MLOPS-001`) + FW → MLOPS (`FW↔MLOPS-001`) |
| 5 | HW ↔ BACK | `HW↔BACK-001` | **MEDIATE** | HW/BACK ↔ SEC (`HW↔SEC-001`, `BACK↔SEC-001`) + `HW↔DEVOPS-001` (ESC-SEC) |
| 6 | HW ↔ FE | `HW↔FE-001` | **MEDIATE** | HW → FW → BACK → FE (`HW↔FW-001` → `FW↔BACK-001` → `BACK↔FE-001`) |
| 7 | FW ↔ FE | `FW↔FE-001` | **MEDIATE** | FW → BACK → FE (`FW↔BACK-001` → `BACK↔FE-001`) |
| 8 | ML ↔ BACK | `ML↔BACK-001` | **MEDIATE** (conditional) | edge-first; `ARCH↔ML-001` split → `ML↔MLOPS-001` → `MLOPS↔BACK-001` |
| 9 | ML ↔ DEVOPS | `ML↔DEVOPS-001` | **MEDIATE** | ML → MLOPS → DEVOPS (`ML↔MLOPS-001` → `MLOPS↔DEVOPS-001`) |
| 10 | MLOPS ↔ FE | `MLOPS↔FE-001` | **MEDIATE** | MLOPS → BACK → FE (`MLOPS↔BACK-001` → `BACK↔FE-001`); signal schema `ML↔FE-001` |

**Result: 0 RATIFY, 10 MEDIATE.** This is the correct measure-first outcome, not an evasion — see §4 ("Why zero RATIFY") for the explicit justification.

---

## 3. Per-Contract Dispositions

### 3.1 FE↔BIZ-001 — Frontend ↔ Business Consultant — **MEDIATE**

- **Scope reconstructed:** BIZ supplies market/business KPIs to surface (operator / executive / customer / investor views); FE returns dashboard UX feasibility + query SLO.
- **Rationale:** Business KPIs are **product requirements**, and requirement ownership belongs to the Product Owner/TPM, not to a direct BIZ→FE channel. [[BUSINESS_CONSULTANT_SKILL|BIZ]] feeds business-value priorities to PO via `PO↔BIZ-001`; PO translates them into user-facing requirements + acceptance criteria for [[FRONTEND_DASHBOARD_ENGINEER_SKILL|FE]] via `FE↔PO-001`. The data to populate the views is served via `DATA↔FE-001` (query-ready views, p95 ≤ 2 s / p99 ≤ 5 s) and `BACK↔FE-001`. A direct FE↔BIZ contract would duplicate PO's requirement-ownership role — the "noise" this analysis is required to avoid.
- **Mediation path:** `PO↔BIZ-001` (business-value ranking) → `FE↔PO-001` (requirements + acceptance criteria) → `DATA↔FE-001` / `BACK↔FE-001` (serving).
- **DERIVED status:** **Permanent.** No §6 FE↔BIZ contract required.

### 3.2 QA↔BIZ-001 — QA ↔ Business Consultant — **MEDIATE**

- **Scope reconstructed:** QA supplies quality/reliability metrics (defect-escape, field MTBF, OTA success rate, RPN burn-down) for business cases and SLA/warranty commitments; BIZ supplies market-driven quality requirements.
- **Rationale:** QA's release-readiness and quality evidence already flow to PO via `QA↔PO-001` (go/no-go + coverage/defects), and PO carries GTM readiness to [[BUSINESS_CONSULTANT_SKILL|BIZ]] via `PO↔BIZ-001`. Field-reliability/uptime figures that bind customer SLAs are already covered by the grounded `DEVOPS↔BIZ-001` edge. There is no quality artifact [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] hands BIZ that is not already routed through PO or DevOps; a direct line would duplicate the PO release-decision channel.
- **Mediation path:** `QA↔PO-001` (release-readiness + coverage/defects) → `PO↔BIZ-001` (GTM readiness); `DEVOPS↔BIZ-001` for reliability/uptime SLA inputs.
- **DERIVED status:** **Permanent.** No §6 QA↔BIZ contract required.

### 3.3 HW↔DATA-001 — Hardware ↔ Data Engineer — **MEDIATE**

- **Scope reconstructed:** Hardware-generated data formats ↔ sensor-data-pipeline ingestion requirements.
- **Rationale:** Hardware does not emit data to the pipeline — **Firmware does**. Raw sensor signals are formatted into telemetry by [[FIRMWARE_ENGINEER_SKILL|FW]] (`HW↔FW-001` sensor specs / pin-mux) and validated against the [[DATA_ENGINEER_SKILL|DATA]]-owned schema registry via `FW↔DATA-001`. Sensor characterization for modelling flows through `HW↔ML-001`. The authoritative per-field telemetry schema is DATA-owned and resolved by `schema_version` — defining it on a direct HW↔DATA edge would violate schema ownership.
- **Mediation path:** `HW↔FW-001` → `FW↔DATA-001` (telemetry → DATA registry); `HW↔ML-001` (characterization for modelling).
- **DERIVED status:** **Permanent.** No §6 HW↔DATA contract required.

### 3.4 HW↔MLOPS-001 — Hardware ↔ MLOps Engineer — **MEDIATE**

- **Scope reconstructed:** Hardware platform profile ↔ model-target packaging constraints.
- **Rationale:** The only hardware fact that matters to model packaging is the **model flash/RAM budget**, and that is the **Architect's** to set via `ARCH↔MLOPS-001` (deployment topology + model flash budget). The on-device hardware-ID match and flash-budget fit are enforced through `FW↔MLOPS-001` (OTA chain). [[MLOPS_ENGINEER_SKILL|MLOps]] never needs a direct line to [[HARDWARE_ENGINEER_SKILL|HW]]; a packaging constraint that conflicts with the budget is routed as a trade through `ARCH↔MLOPS-001` (ADR on exceedance), never settled bilaterally.
- **Mediation path:** `ARCH↔MLOPS-001` (Architect-owned flash budget) + `FW↔MLOPS-001` (on-device hardware-ID / flash-fit); `HW↔ML-001` (characterization).
- **DERIVED status:** **Permanent.** No §6 HW↔MLOPS contract required.

### 3.5 HW↔BACK-001 — Hardware ↔ Backend/Cloud Engineer — **MEDIATE** (security-governed)

- **Scope reconstructed:** Hardware identity anchors (root of trust, secure element, device-ID source) ↔ backend provisioning / enrollment requirements.
- **Rationale:** This edge is **security baseline** territory. The hardware root of trust / secure element is governed by `HW↔SEC-001`; the cloud PKI / X.509 device identity by `BACK↔SEC-001`; production provisioning/enrollment by `HW↔DEVOPS-001`. Cryptographic device identity must **not** be defined on a direct HW↔BACK edge — doing so would create a security-baseline surface outside [[SECURITY_ENGINEER_SKILL|SEC]] ownership, firing `ESC-SEC` and violating HG-01. MEDIATE is not merely sufficient here; it is **required** by the security baseline.
- **Mediation path:** `HW↔SEC-001` + `BACK↔SEC-001` (device-identity baseline, SEC-owned) + `HW↔DEVOPS-001` (provisioning/enrollment). Any device-identity touchpoint → `ESC-SEC`.
- **DERIVED status:** **Permanent.** No §6 HW↔BACK contract required; a direct contract would be a security anti-pattern.

### 3.6 HW↔FE-001 — Hardware ↔ Frontend Engineer — **MEDIATE**

- **Scope reconstructed:** Hardware health signals (battery V, solar current, board temperature, sensor health) ↔ device-health dashboard requirements.
- **Rationale:** Physical topology forbids a direct edge — hardware health is read by firmware, emitted as telemetry, and only then reaches a dashboard. Signals travel HW → FW (`HW↔FW-001`) → cloud (`FW↔BACK-001`) → dashboard (`BACK↔FE-001`), with serving views via `DATA↔FE-001`. [[FRONTEND_DASHBOARD_ENGINEER_SKILL|FE]]'s device-health view requirements flow back along the same chain.
- **Mediation path:** `HW↔FW-001` → `FW↔BACK-001` → `BACK↔FE-001` (+ `DATA↔FE-001` serving).
- **DERIVED status:** **Permanent.** No §6 HW↔FE contract required.

### 3.7 FW↔FE-001 — Firmware ↔ Frontend Engineer — **MEDIATE**

- **Scope reconstructed:** Firmware-status semantics (OTA state, boot health, firmware version) ↔ device-management UI requirements.
- **Rationale:** Firmware status reaches the dashboard via the cloud, not directly: `FW↔BACK-001` (telemetry + OTA state + desired-state command) → `BACK↔FE-001` (served to UI). Critically, **binding device-management actions** (reboot, re-flash, re-key) must route through the Backend desired-state contract `FW↔BACK-001` with the security review attached — a UI control wired directly to firmware would bypass the desired-state and security-baseline path. The OTA state machine itself is owned by `FW↔BACK-001` / `FW↔DEVOPS-001`; FE consumes its enum, it does not define it.
- **Mediation path:** `FW↔BACK-001` (telemetry / OTA state / desired-state) → `BACK↔FE-001` (UI).
- **DERIVED status:** **Permanent.** No §6 FW↔FE contract required.

### 3.8 ML↔BACK-001 — Edge AI/ML ↔ Backend/Cloud Engineer — **MEDIATE** (conditional)

- **Scope reconstructed:** Cloud inference output schema ↔ backend serving requirements.
- **Rationale:** AgriSpectra inference is **edge-first** — the model runs on the STM32H7, so there is presently no cloud-served inference for the Backend to host. The edge-vs-cloud inference split is owned by the Architect via `ARCH↔ML-001`. Any cloud-side inference would be packaged by MLOps (`ML↔MLOPS-001`) and served via `MLOPS↔BACK-001`, not handed directly from [[EDGE_AI_ML_ENGINEER_SKILL|ML]] to [[BACKEND_CLOUD_ENGINEER_SKILL|BACK]].
- **Mediation path:** `ARCH↔ML-001` (inference split) → `ML↔MLOPS-001` (packaging) → `MLOPS↔BACK-001` (serving).
- **DERIVED status:** **Permanent under the current edge-first architecture.** **Conditional re-evaluation:** if a future `ARCH↔ML-001` ADR changes `inference_location` to `CLOUD` / `HYBRID`, this edge is re-opened and a §6 ML↔BACK contract is then ratified via CCR + ADR. That trigger is recorded here so the disposition is not silently stale.

### 3.9 ML↔DEVOPS-001 — Edge AI/ML ↔ DevOps/Platform Engineer — **MEDIATE**

- **Scope reconstructed:** ML build/compute requirements ↔ ML build/CI infrastructure.
- **Rationale:** The ML training/conversion CI pipeline and model registry are owned by **MLOps** (`ML↔MLOPS-001`), and the underlying platform/cluster/IaC by `MLOPS↔DEVOPS-001`. [[EDGE_AI_ML_ENGINEER_SKILL|ML]] expresses build needs to MLOps, who provisions through [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]]. A direct ML↔DevOps contract would bypass the MLOps-owned pipeline. Specialized research compute (e.g., novel-operator experiments) routes via `RES↔DEVOPS-001` with SEC + PO approval, not this edge.
- **Mediation path:** `ML↔MLOPS-001` (CI pipeline / registry) → `MLOPS↔DEVOPS-001` (platform / cluster / IaC).
- **DERIVED status:** **Permanent.** No §6 ML↔DEVOPS contract required.

### 3.10 MLOPS↔FE-001 — MLOps ↔ Frontend Engineer — **MEDIATE**

- **Scope reconstructed:** Model deployment-status + drift dashboard data ↔ frontend monitoring requirements.
- **Rationale:** MLOps fleet/deployment data reaches dashboards through the Backend (`MLOPS↔BACK-001` → `BACK↔FE-001`), and the **operator-facing inference confidence/drift signal schema is already a ratified bilateral contract**, `ML↔FE-001` — FE sources drift semantics there, not from a redefined MLOPS↔FE schema. This matters for governance: the **FC-022** erosion-shaped drift detection chain (keystone open Critical chain, RPN 405, D = 9; see [[SYSTEM_FMEA_V1|System FMEA V1]]) is contractually covered by the existing `ML↔MLOPS-001` + `ML↔FE-001` + `MLOPS↔BACK-001` edges — a direct MLOPS↔FE contract would add no detection coverage, only redundancy. Drift values must be surfaced at their computed magnitude (Honesty Over Polish §10.3) — never softened to suppress a dashboard alert.
- **Mediation path:** `MLOPS↔BACK-001` → `BACK↔FE-001` (deployment-status / drift series); `ML↔FE-001` (confidence/drift signal schema).
- **DERIVED status:** **Permanent.** No §6 MLOPS↔FE contract required.

---

## 4. Why Zero RATIFY (Honesty Note)

A 10/10 MEDIATE outcome is the **measured** result, not a default. Every one of these edges fails the RATIFY criteria of §1 for a concrete, structural reason — grouped into three families:

- **Physical topology forbids a direct edge (4):** `HW↔DATA`, `HW↔FE`, `FW↔FE`, `MLOPS↔FE`. The edge endpoint (a sensor, a board signal, firmware state, fleet status) physically cannot reach the consumer except through the firmware → cloud → dashboard relay. The "mediation" is the actual data path, not a workaround.
- **A third role already owns the artifact (4):** `HW↔MLOPS` (ARCH owns the flash budget), `ML↔BACK` (ARCH owns the inference split; MLOps owns serving), `ML↔DEVOPS` (MLOps owns the CI pipeline), and the two BIZ edges `FE↔BIZ` / `QA↔BIZ` (PO owns requirements and the release decision). Ratifying would duplicate an owner and create conflicting authority.
- **Security baseline requires mediation (1):** `HW↔BACK` — device identity is SEC-owned; a direct contract would be a security anti-pattern (`ESC-SEC`, HG-01).

Per CLAUDE.md §1 (contract-first; measure-first) and §10.3 (honesty over polish), inventing a RATIFY for variety would itself be the violation this exercise exists to prevent.

---

## 5. Governance & Next Steps

1. **Registry reclassification (recommended action).** The 10 schemas in [docs/contract-registry/schemas/](schemas/) currently carry `x-macp.source_status = DERIVED` mandating a perpetual `COUNTER` for *ratification*. With ratification now formally declined, the limbo should be retired: each `source_status` should be updated from *"DERIVED — mandates COUNTER for §6 ratification"* to **`MEDIATED-PERMANENT`** with a `redirect_to` list naming the mediating contracts above. The agent behaviour changes from an unresolvable "always COUNTER to ratify" loop to a definitive **"REDIRECT — coordinate on the named mediating contract(s), do not negotiate this edge directly."** This *increases* autonomy (the original goal) by removing a dead-end negotiation, while preserving the invariant that no binding `CONFIRM` ever occurs on a non-existent contract.
2. **Ratification route.** This disposition is a contract-registry governance decision, not a new §6 contract, so it does not require a STRATEGIC ADR. It is routed to the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARB]] for ratification (registry-metadata disposition; bilateral, low-novelty — within ARB scope per §7.Z) and recorded as an ARB Decision Record cross-referenced from the [[ADR_INDEX|ADR Index]]. The `ML↔BACK-001` conditional re-evaluation trigger (§3.8) is logged with it.
3. **Standing exception — `ML↔BACK-001`.** Re-open and ratify a §6 ML↔BACK contract (CCR + ADR) **only if** a future `ARCH↔ML-001` ADR moves `inference_location` to `CLOUD` / `HYBRID`. Until then it remains `MEDIATED-PERMANENT`.
4. **Security standing — `HW↔BACK-001`.** The permanent-mediated status does **not** relax `ESC-SEC`: any coordination touching cryptographic device identity continues to escalate to [[SECURITY_ENGINEER_SKILL|SEC]] under `HW↔SEC-001` / `BACK↔SEC-001`.

> No interface contract, resource budget, security baseline, or OTA strategy is changed by this document. It records an architecture topology disposition and a recommended registry-metadata update; binding effect follows ARB ratification per the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]] invariant.
