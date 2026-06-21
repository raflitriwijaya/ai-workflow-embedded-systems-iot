---
title: "System FMEA V1 — Cross-Layer Failure Mode and Effects Analysis"
date: 2026-06-21
status: final
version: "1.0"
owner: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
methodology: "IEC 60812"
tags:
  - fmea
  - reliability
  - robustness
  - system-safety
  - cross-layer
  - adversarial
cssclass: fmea-worksheet
---

# System FMEA V1 — Cross-Layer Failure Mode and Effects Analysis

> **Owner:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]]
> **Methodology:** IEC 60812 — Failure Mode and Effects Analysis
> **Date:** 2026-06-21
> **Version:** 1.0
> **Referenced by:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#5. Deliverables & Artifacts|System Robustness Contract]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#5.1 NFR Verification Matrix — End-to-End System Robustness Category|NFR Verification Matrix (R1–R5)]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA Cross-Layer Robustness Validation Suite]]
> **Review cadence:** Updated at each major architecture revision; reviewed at every Architecture Review Board (ARB) milestone
> **Closes:** Review Part 2 Critical Finding **C-1** (`[TBD per product class]` NFR targets) and Phase 4 Debt **DEBT-R1** (FMEA mandated-not-conducted); Review V3 Phase 1 master finding (hollow robustness gate)

---

## 1. Scope and Methodology

### 1.1 Purpose

This is the **first conducted system-level FMEA** for the embedded/IoT AI product ecosystem defined by the 14-role organizational design. It discharges the obligation in [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#8. Standards & Best Practices|Architect §8]] ("FMEA per IEC 60812 conducted at system level for all cross-layer failure chains") and replaces the `[TBD per product class]` placeholders in the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#5.1 NFR Verification Matrix — End-to-End System Robustness Category|System Robustness Contract NFRs (R1–R5)]] with quantified, FMEA-derived targets (§6).

Until this document existed, the robustness gate was structurally hollow: [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] is contracted to regression-test "100% of Critical and High-severity FMEA failure chains" (NFR R5) against a failure-chain inventory **that had never been enumerated**. 100% coverage of an empty set is coverage of nothing. This worksheet is that inventory.

### 1.2 Scope — what is in and out

- **In scope:** Every failure chain whose effect **crosses ≥2 architectural layers**. The initiating fault may be local; it qualifies only if the *effect* propagates across a layer boundary (e.g., a sensor fault that silently corrupts a fleet-wide retrained model).
- **Out of scope:** Single-layer failures with no cross-layer effect (e.g., "one sensor drifts and is replaced under RMA with no downstream propagation"). These belong to per-layer FMEAs owned by the implementing roles, not to this system FMEA.
- **Adversarial mandate:** This FMEA deliberately privileges the failures the design did **not** anticipate — silent in-range corruption, race conditions across asynchronous boundaries, closed-loop self-reinforcing degradation, and chains whose only "detection" lives *downstream* of the damage. Failures already closed cleanly by a contracted control (e.g., a signed image failing verification and being rejected) are noted but not inflated; the value of this document is the chains with **no detection mechanism at all**.

### 1.3 Architectural layers

| # | Layer | Representative owner |
|---|---|---|
| 1 | Hardware | [[HARDWARE_ENGINEER_SKILL\|HW]] |
| 2 | Firmware | [[FIRMWARE_ENGINEER_SKILL\|FW]] |
| 3 | Edge AI/ML | [[EDGE_AI_ML_ENGINEER_SKILL\|ML]] |
| 4 | Communication | [[FIRMWARE_ENGINEER_SKILL\|FW]] / [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] / [[SECURITY_ENGINEER_SKILL\|SEC]] |
| 5 | Cloud/Backend | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] |
| 6 | Data | [[DATA_ENGINEER_SKILL\|DATA]] |
| 7 | DevOps/OTA | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] / [[MLOPS_ENGINEER_SKILL\|MLO]] |
| 8 | Frontend | [[FRONTEND_DASHBOARD_ENGINEER_SKILL\|FRONT]] |
| 9 | Security (cross-cutting) | [[SECURITY_ENGINEER_SKILL\|SEC]] |

> In the worksheet **Layers** column, these short codes (HW, FW, ML, COMM, CLOUD, DATA, OTA, FRONT, SEC) denote **architectural layers**, not role cards. Role *cards* are always cited as `[[wikilinks]]` in the control columns.

### 1.4 Method

For each chain: identify Failure Mode → Effect (system-level) → Cause; map the crossed layers; score Severity (S), Occurrence (O), Detectability (D) on the calibrated 1–10 scales in §3; compute **RPN = S × O × D**; cite the **specific** design-time and detection controls that exist in the organizational design (with `§` references); recommend additional controls; and classify residual risk. Reference deployment profile for O and field-condition reasoning: a **50,000-device fleet, 7-year outdoor field life, intermittent LoRaWAN connectivity** (the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]'s reference product class), consistent with the Review V3 AgriSpectra scenario.

---

## 2. RPN Thresholds and Risk Acceptance Criteria

| RPN Range | Classification | Required Action |
|---|---|---|
| ≥200 | **Critical** | Design-time mitigation **MANDATORY** before production release. Must be verified by [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] fault-injection testing and signed off by the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] at the production release gate |
| 100–199 | **High** | Design-time mitigation strongly recommended. If accepted as-is, requires [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] and [[SECURITY_ENGINEER_SKILL\|Security Engineer]] concurrence via ADR with a time-bound remediation plan |
| 50–99 | **Medium** | Mitigation considered. Accepted with documented rationale and routine monitoring |
| <50 | **Low** | Accepted as-is. Reviewed at next FMEA update |

> **Calibration note (adversarial honesty):** A chain that is both severe and **undetectable** (high S, high D) lands at high RPN *by design of the scale* — that is precisely the combination a robustness program exists to surface. No RPN in this document has been padded downward to make a gate look safe. Where a chain has **no detection mechanism**, D is scored 9–10 and named as such in §4 and §5.2.

---

## 3. Severity, Occurrence, and Detectability Scales

### 3.1 Severity (S) — system-level impact

| S | Level | Criteria |
|---|---|---|
| 10 | Catastrophic | Physical safety harm (wrong actuator/advisory acted on in field), fleet-wide bricking, or confirmed breach of PII / cryptographic keys |
| 9 | Critical | Silent fleet-wide erosion of core product value, irreversible data loss, or a security defect enabling breach |
| 8 | Severe | Major functional loss across a large device subset; recoverable only by field intervention, RMA, or emergency OTA |
| 7 | High | Significant degradation of a core function on a device/region subset; requires an OTA hotfix |
| 6 | Moderate-High | Incorrect or unavailable output on a device/region; recoverable without field visit |
| 5 | Moderate | Degraded performance with a viable workaround |
| 4 | Low-Moderate | Minor functional issue, limited blast radius |
| 3 | Low | Minor degradation with transparent automatic recovery |
| 2 | Minor | Negligible user-visible impact |
| 1 | None | No system-level effect |

### 3.2 Occurrence (O) — probability over fleet lifetime (50k devices, 7 yr)

| O | Level | Criteria |
|---|---|---|
| 10 | Inevitable | Routine across the fleet (multiple events per device per year) |
| 9 | Very high | Occurs on most devices over lifetime |
| 8 | High | Occurs on a large fraction of devices over lifetime |
| 7 | Moderately high | Expected on a meaningful device subset over lifetime |
| 6 | Moderate | Recurs somewhere in the fleet several times per year |
| 5 | Occasional | Plausible several times across the fleet over lifetime |
| 4 | Low | Possible but uncommon; needs an off-nominal condition |
| 3 | Unlikely | Rare; requires an unusual condition |
| 2 | Very unlikely | Requires a confluence of rare conditions |
| 1 | Improbable | Essentially never, given existing controls |

### 3.3 Detectability (D) — difficulty of detection (10 = worst)

| D | Level | Criteria |
|---|---|---|
| 10 | Undetectable | No mechanism detects it even after a customer report; silent and unattributable |
| 9 | **No detection mechanism exists in the system as specified**; surfaces only via external/customer report or special investigation |
| 8 | Detection theoretically possible but **no contracted control**; would require luck or a manual audit |
| 7 | Detected only late/downstream, after the effect has propagated; signal is weak or indirect |
| 6 | Detected by aggregate monitoring that **can mask the specific instance** |
| 5 | Detected by an existing control but with significant latency or ambiguity |
| 4 | Detected by an existing control with moderate latency |
| 3 | Detected promptly by a contracted control (alert/test) |
| 2 | Detected near-immediately by a dedicated control |
| 1 | Prevented or caught immediately by a hard, fail-closed gate |

---

## 4. Failure Chain Inventory

> 36 cross-layer chains, **FC-001 … FC-036**, organised by initiating layer. Every chain crosses ≥2 layers. Control columns cite the specific SKILL.md `§` that would catch or prevent the chain; where the cited control is *downstream of* or *blind to* the failure, the Detection column says so plainly.

### 4.1 Hardware-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-001** | Spectral/analog-front-end **gradual drift** over 7-yr outdoor life produces values **in-range but wrong**; FW reads valid I²C frames; INT8 CNN infers on corrupted spectra and emits normal-looking probabilities at normal confidence | Silent fleet-wide false negatives/positives; core product value erodes undetected | AFE aging, temperature/humidity cycling, sensor element degradation without hard failure | HW→FW→ML(→CLOUD) | 9 | 6 | **9** | **486** | [[HARDWARE_ENGINEER_SKILL\|HW]] §6.3 Sensor Data Fidelity loop (one-time, at bring-up); [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] §5.1 R1 (assumes "detect corrupted sensor data within 100 ms") | **None for in-range drift.** R1 fault-injection covers stuck/out-of-range, not slow plausible drift; Fidelity loop is one-time not lifetime. **D=9: undetectable on-device as specified** | Periodic on-device **reference-channel self-test** vs a known reflectance target; absolute ground-truth re-validation (see FC-022); lifetime re-characterisation cadence | **Open — mitigation MANDATORY** |
| **FC-002** | Voltage brown-out **during the MCUboot A/B swap/trailer write** tears the boot-confirmation flag, leaving both slots in an indeterminate state | Device boots a stale or unconfirmed image, or fails to confirm a valid update → field intervention / RMA | Marginal solar/Li-ion supply at cold temperature during the narrow flash-commit window | HW→FW→OTA | 8 | 3 | 4 | 96 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.6 MCUboot A/B + watchdog-driven revert; brown-out detection | Boot failure → rollback path usually catches it (D moderate); torn-trailer edge can defeat revert | Power-fail-safe swap (scratch/move) with atomic trailer write; brown-out threshold set above flash-write minimum Vcc | Mitigated |
| **FC-003** | I²C clock-stretch / bus hang during a sensor read → ISR timeout → FW **reuses last-good preprocessing window**; inference runs on **stale input reported as fresh** (DMA-vs-inference-task race) | Inference/telemetry on stale data presented as current; wrong field decision | Sensor bus contention, EMI, marginal pull-ups; non-deterministic ISR/DMA timing | HW→FW→ML→CLOUD | 7 | 4 | 7 | 196 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §3.3 ring-buffer preprocessing; §4.2 WDT/stack | ACTIVE-model + telemetry heartbeat ([[FIRMWARE_ENGINEER_SKILL\|FW]] §6.7) prove the model is live, **not that this inference's input was fresh** | **End-to-end input-freshness timestamp** carried sample→inference→telemetry; reject window if age > deadline | Mitigated (after control) |
| **FC-004** | Secure-element / on-chip **anti-rollback counter write wears out or fails silently** (write-endurance / fuse limit over 7 yr) → counter not incremented | Device accepts a rolled-back (older, vulnerable) firmware/model; anti-rollback defeated fleet-wide on aged units | Flash/fuse endurance, SE intermittent fault, write not verified | HW→FW→SEC→OTA | 9 | 3 | 8 | 216 | [[SECURITY_ENGINEER_SKILL\|SEC]] §4.1/§4.2 anti-rollback (fuse/counter); [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.6 image integrity | Counter-write success **not read-back-verified or reported**; no fleet telemetry on rollback-counter health → **D=8** | Read-back-verify every counter increment; report counter value in heartbeat; alert on non-monotonic regression | **Open — mitigation MANDATORY** |
| **FC-005** | Brown-out **during LoRaWAN TX peak current** resets device mid-transmit; **store-and-forward buffer pointer corrupts** (non-atomic update across reset) | Silent loss of the in-flight record and/or duplicate replay on reboot; earliest-onset telemetry lost | Cold-temp battery sag at TX peak; non-atomic buffer index | HW→FW→COMM→DATA | 6 | 6 | 7 | 252 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.4 store-and-forward; [[DATA_ENGINEER_SKILL\|DATA]] §4.5 dedup/idempotency | Dedup catches **duplicates**, not the **silent loss** of the in-flight record; ingest-health is aggregate → **D=7** | Atomic (journaled) buffer index across reset; emit a **per-device data-gap marker** on recovery | **Open — mitigation MANDATORY** |
| **FC-006** | MCU **clock drift over temperature** (RC osc / crystal pull) shifts the effective sensor sampling rate → FFT bin alignment / windowing drifts → feature vector subtly wrong | Model accuracy silently degrades on hot/cold devices; region-correlated error | Wide operating-temperature range; clock not disciplined | HW→FW→ML | 7 | 5 | 8 | 280 | [[HARDWARE_ENGINEER_SKILL\|HW]] §4.7 thermal/derating; [[EDGE_AI_ML_ENGINEER_SKILL\|ML]] §6.3 preprocessing golden reference + test vectors | Parity vectors validated at **lab temperature**, not across the temp range; **no runtime sample-rate verification** → **D=8** | Runtime timestamping of actual sample interval; temperature-conditioned parity test in HIL ([[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] §3.4) | **Open — mitigation MANDATORY** |
| **FC-007** | Cheap MCU **RTC drift** over years (no GPS/NTP discipline) → wrong event timestamps | [[DATA_ENGINEER_SKILL\|DATA]] event-time/watermark logic places disease alerts in the **wrong time window** or drops them as "too late"; mis-ordered fleet history | Uncompensated RTC, no time sync on LoRaWAN | HW→FW→COMM→DATA | 6 | 6 | 8 | 288 | [[DATA_ENGINEER_SKILL\|DATA]] §4.5 watermarks/event-time; §6 late-data handling | Watermark logic **trusts device timestamps** (HA-A3); no cross-check of device clock vs ingest arrival → **D=8** | Cross-check device clock vs broker receipt time at ingest; periodic time-sync downlink; flag skew > threshold | **Open — mitigation MANDATORY** |

### 4.2 Firmware-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-008** | Under a rare deep ISR-nesting path, **stack high-water grows into the statically-allocated tensor arena** region → inference reads corrupted weights/activations | Wrong inference output with **no crash, no fault**; silent on affected devices | Worst-case nesting not covered by stack sizing; arena placed adjacent to stack | FW→ML | 8 | 3 | 9 | 216 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.2 stack sizing + high-water watermark; MISRA static analysis | High-water **sampling** can miss the rare path; arena/stack overlap not guarded at runtime → **D=9** | MPU guard region between stack and arena (hard fault on touch); worst-case stack analysis in CI | **Open — mitigation MANDATORY** |
| **FC-009** | A **toolchain/compiler-flag change** (e.g., FP contraction, fixed-point rounding mode) makes FW preprocessing diverge bit-level from the ML golden reference | Train/serve skew; inference on subtly different features fleet-wide after a routine build change | New toolchain version; `-ffast-math`/rounding default change; no parity gate on toolchain bump | FW→ML→OTA | 7 | 4 | 7 | 196 | [[EDGE_AI_ML_ENGINEER_SKILL\|ML]] §6.3 golden reference + test vectors; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] §4.6 pinned reproducible toolchain | Parity validated **once at integration**, not re-run on every toolchain change; CI may not gate on parity vectors → **D=7** | Gate every build on the ML parity vectors in CI; fail closed on any bit-mismatch | Mitigated (after control) |
| **FC-010** | FW changes telemetry field semantics (e.g., units, scaling) but **does not bump the schema-version field** (developer error) | [[DATA_ENGINEER_SKILL\|DATA]] validates against the old version and **silently accepts misinterpreted values**; training/dashboards corrupted | Human omission; version field is a manual increment | FW→COMM→DATA | 8 | 3 | 8 | 192 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §6.8 Schema-Change Coordination (FW increments version; DATA validates at ingest) | Relies on the developer remembering to bump; **no automated schema-hash check** → **D=8** | Auto-derive a schema **content hash** at build; ingest rejects unknown hash; CI diffs schema vs registry | High → mitigate |
| **FC-011** | **Watchdog masking / shallow liveness:** WDT is serviced from a high-priority timer ISR that keeps running while the inference/telemetry task is deadlocked → WDT never fires | Device looks alive (ISR heartbeat) but produces **no inference**; "dark" device counted as healthy | Anti-pattern: WDT kicked independent of the supervised work | FW→COMM→CLOUD→FRONT | 7 | 4 | 8 | 224 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.2 WDT; [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §6.2 twin heartbeat | Heartbeat/WDT prove **the ISR runs**, not that the inference task is alive → **D=8** | True liveness: inference-task must "check in" to feed the WDT; heartbeat carries last-inference timestamp | **Open — mitigation MANDATORY** |
| **FC-012** | During a multi-day LoRaWAN outage the store-and-forward buffer fills; FW **drops oldest (FIFO)** to make room → earliest disease-onset telemetry discarded | [[DATA_ENGINEER_SKILL\|DATA]] never sees onset; model/alerts miss the most valuable signal | Bounded buffer + extended connectivity gap; drop-oldest policy | FW→COMM→DATA→ML | 7 | 5 | 8 | 280 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §4.4 store-and-forward; [[DATA_ENGINEER_SKILL\|DATA]] §3.6 ingest-health (aggregate) | Ingest-health is **aggregate**; a device dropping its oldest records is below the noise floor → **D=8** | Emit an explicit **buffer-overflow / data-gap event** with the dropped time-range; prioritise retention of anomalous records | **Open — mitigation MANDATORY** |
| **FC-013** | **Heap fragmentation** in the long-running TLS/connectivity stack (mbedTLS session allocs) over months of uptime → `malloc` fails during a TLS re-handshake | Device silently stops reconnecting; telemetry ceases while the device still "exists" | Dynamic allocation in a never-restarted process; fragmentation accumulates | FW→COMM→CLOUD | 6 | 5 | 7 | 210 | [[FIRMWARE_ENGINEER_SKILL\|FW]] §9 (discourages dynamic alloc in hot paths); §4 reliability | TLS libs use heap; long-uptime fragmentation not exercised unless HIL soak ≈ field uptime → **D=7** | Static/pool allocator for TLS; periodic supervised reconnect; soak test at field-representative uptime | **Open — mitigation MANDATORY** |

### 4.3 Communication-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-014** | **LoRaWAN downlink duty-cycle limits** delay or drop the desired-model-version command from the network server → device never receives `DESIRED_SET` | Twin shows `desired == reported` (old) → **no mismatch** → campaign silently never reaches that device; new disease pattern undeployed | Constrained downlink bandwidth; gateway/network-server contention | COMM→CLOUD→FW | 6 | 5 | 8 | 240 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §6.2 twin-sync monitor; [[MLOPS_ENGINEER_SKILL\|MLO]] §6.9 "stuck non-ACTIVE >1 h"; [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] OTA end-to-end timeout | Both monitors live **downstream of `DESIRED_SET`**; the downlink-delivery hop is unwatched (Review V2 **F1**) → **D=8** | Assign the **F1 chain-level OTA watchdog**: alert if any device fails to ACK desired-state within N× the downlink SLA | **Open — mitigation MANDATORY** |
| **FC-015** | **QoS-1 redelivery after broker failover** duplicates a command/control message on a path lacking an idempotency key → double actuation/command | Repeated command executed twice (e.g., duplicate advisory or actuator pulse) | At-least-once delivery + broker failover redelivery; missing idempotency on the command path | COMM→CLOUD→FW | 8 | 3 | 6 | 144 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §4.1 idempotency keys (APIs); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] §3.4 cloud-degradation scenario | Idempotency contracted for **APIs**, not explicitly for the device **command** path → **D=6** | Mandate idempotency keys on every device command in the OTA/command contract; device dedups by key | High → mitigate |
| **FC-016** | **LoRaWAN frame-counter desync** after a device reset that loses counter state (or 32-bit rollover over 7 yr) → network server rejects frames as replay | That device's telemetry **silently dropped at the network-server layer**, before it reaches the broker | Reset loses non-volatile counter; replay-protection window | COMM→SEC→CLOUD→DATA | 7 | 4 | 8 | 224 | [[SECURITY_ENGINEER_SKILL\|SEC]] §4.3 LoRaWAN session/replay protection | Loss occurs **at the network server**, invisible to [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] ingest-health and twin → **D=8** | Persist/restore frame counter atomically; rejoin (OTAA) on desync; surface NS reject counts into observability | **Open — mitigation MANDATORY** |
| **FC-017** | **Device X.509 certificate expiry** mid-lifetime; if the device is offline near expiry (or RTC wrong, see FC-007) it cannot rotate → mTLS handshake fails permanently | A cohort of aging devices **silently drops off the network** as certs expire; looks like normal churn | Cert validity < device life; rotation requires connectivity; clock dependency | COMM→SEC→CLOUD | 8 | 5 | 6 | 240 | [[SECURITY_ENGINEER_SKILL\|SEC]] §4.4 X.509 lifecycle, key rotation; [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §4.4 cert handling | Backend sees devices drop but may attribute to churn; **no expiry-horizon alerting** → **D=6** | Rotate ≥30 days before expiry with offline-grace; fleet **cert-expiry-horizon** dashboard + proactive renewal campaign | High → mitigate |

### 4.4 Cloud/Backend-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-018** | **Twin reconciliation race:** Backend sets `desired` while a device is mid-OTA; a stale cached `reported` overwrites the device's true `ACTIVE(new)` (last-write-wins) | Twin shows the device on the old version → redundant OTA re-push to an already-updated device → needless flash wear / re-apply | Non-CAS twin update; cache vs device-report ordering | CLOUD→FW→OTA | 5 | 4 | 7 | 140 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §4.3/§6.2 twin reconciliation | Race not contracted with versioned/compare-and-set semantics; symptom (re-push) looks benign → **D=7** | Versioned (CAS) twin writes keyed on report monotonic counter; reject stale `reported` overwrites | High → mitigate |
| **FC-019** | **Telemetry storm** during a regional outbreak → ingest backpressure → DLQ → disease alerts **delayed past the actionable window** exactly when they matter most | Operators act late or not at all during the highest-value event | Correlated fleet event; ingest not sized for surge ([[DATA_ENGINEER_SKILL\|DATA]]) | CLOUD→DATA→FRONT | 7 | 4 | 5 | 140 | [[DATA_ENGINEER_SKILL\|DATA]] §3.6 pipeline-latency SLO (>5 min → investigate) | Latency alert **degrades under the very load it must survive**; not correlated to "outbreak in progress" → **D=5** | `System Scalability Contract` + fleet-scale surge test (≥10× nominal); priority lane for anomaly-positive messages | High → mitigate |
| **FC-020** | OTA status events arrive **out of order** (`DESIRED_SET` acted on before `DISTRIBUTED` confirmed) → device attempts to download an artifact not yet at the edge endpoint | Repeated download failures; device stuck `DOWNLOADING`; cohort rollout stalls | Event-ordering bug; no transactional barrier between DevOps `DISTRIBUTED` and Backend `desired` | CLOUD→OTA→FW | 6 | 3 | 5 | 90 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §6.2 ("set desired only after DevOps confirms DISTRIBUTED"); OTA status codes | Relies on status ordering; download-failure retries are visible → **D=5** | Transactional barrier / handshake before `DESIRED_SET`; bounded retry with explicit `DOWNLOAD_FAILED` escalation | Medium — accept w/ monitoring |
| **FC-021** | **Broker ACL drift** after a config change → a device subscribes to the wrong topic prefix and receives **another cohort's** desired-state/command | Wrong model/command delivered to the wrong device class (e.g., crop-A model to crop-B node) | Manual ACL change not gated by the OTA contract; topic-prefix templating error | CLOUD→COMM→FW | 8 | 2 | 7 | 112 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §4.2 topic ACLs; [[SECURITY_ENGINEER_SKILL\|SEC]] review; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] cohort-targeting validation (at release) | Cohort targeting validated **at release**, not on config drift → **D=7** | ACL-as-code with CI policy test; per-message cohort assertion on device (reject mismatched target ID) | High → mitigate |

### 4.5 Data-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-022 (KEYSTONE)** | **Closed-loop silent corruption:** FC-001 sensor drift → field telemetry → becomes **retraining data** → model learns the drift as signal → OTA'd fleet-wide. Evidently drift monitor compares each cycle to a **re-baselined** distribution → gradual drift never trips (boiling-frog) | Core product value erodes **fleet-wide and silently**; spans every layer; **also masks B5** (physical root cause never routed to [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL\|Research]]) | Self-referential monitoring baseline; field labels co-drift with the corruption | HW→FW→COMM→CLOUD→DATA→ML→OTA→fleet | 9 | 5 | **9** | **405** | [[MLOPS_ENGINEER_SKILL\|MLO]] §6.9 accuracy-floor gate; §4 drift monitoring; [[DATA_ENGINEER_SKILL\|DATA]] §6.2 DQIR; [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL\|RES]] §3.7 assumption validation (quarterly) | **Every control is self-referential or lagging:** accuracy floor measured against drifting field labels; drift-vs-(re-baselined) monitors against its own corruption; DQIR catches only what ML *notices*. **No absolute ground-truth anchor → D=9** | **Absolute ground-truth anchor**: a frozen, externally-labelled golden validation set re-run every retrain; closed-loop multi-cycle degradation test; **field-push** B5 classify-and-route to Research | **Open — mitigation MANDATORY** |
| **FC-023** | **Train/test leakage at field scale:** temporally/spatially adjacent samples (same device/field, hours apart) split across train and validation → inflated validation accuracy | A weak model **passes the accuracy-floor gate** and underperforms in the field | Random split ignores device/field grouping at fleet scale | DATA→ML→OTA | 7 | 4 | 6 | 168 | [[DATA_ENGINEER_SKILL\|DATA]] §6.2 "split definitions to avoid leakage" | Split integrity named but **device/field-level grouping not explicitly contracted**; golden ref covers preprocessing, not split integrity → **D=6** | Mandate grouped (device/field/time-block) splits; leakage audit in the pipeline + [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] validation | High → mitigate |
| **FC-024** | **Backfill mutates a partition already consumed by a training run** → two runs on "the same" dataset version yield different models; lineage hash still matches its own snapshot | Silent non-determinism in what a dataset "version" means; reproducibility passes yet semantics shifted | Late/backfilled data written into a labelled partition rather than a new immutable snapshot | DATA→ML→OTA | 6 | 4 | 8 | 192 | [[DATA_ENGINEER_SKILL\|DATA]] §4.6 versioning/lineage, immutable snapshots; [[MLOPS_ENGINEER_SKILL\|MLO]] §5 Rebuildability job | Rebuildability verifies binary-identity **to its own lineage**, not that the partition wasn't mutated post-consumption → **D=8** | Enforce immutable training snapshots; backfill only into new versions; record consumed-snapshot hash in the model lineage | **Open — mitigation MANDATORY** |
| **FC-025** | **Re-identification via engineered features:** a derived feature (precise geo + timestamp combination) re-identifies a farm/operator despite raw-PII masking → Confidential data enters training sets and model-card examples | Privacy breach (GDPR/CCPA exposure) propagated through ML artifacts | Quasi-identifier combination not caught by field-level masking | DATA→ML→SEC | 9 | 3 | 8 | 216 | [[DATA_ENGINEER_SKILL\|DATA]] §6.9 Data Security & Governance Policy (k-anonymity k≥5 for quasi-identifiers, PII masking); quarterly Joint Review | Field-level masking misses **quasi-identifier combinations** in engineered features; **no automated re-identification test** → **D=8** | Automated re-identification / k-anonymity test on engineered feature sets in the pipeline; privacy review gate on new features | **Open — mitigation MANDATORY** |

### 4.6 Security-Initiated Failure Chains

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-026** | **Model signing-scheme downgrade / replay:** an old-firmware device accepts a downgraded or previously-valid (replayed) **model** artifact because model anti-rollback is weaker than firmware anti-rollback | Tampered/stale model deployed to the fleet's core ML asset (tampering + elevation) | Asymmetry between firmware and model anti-rollback strength; replay window | SEC→OTA→FW→ML | 9 | 3 | 7 | 189 | [[SECURITY_ENGINEER_SKILL\|SEC]] secure-OTA governance; [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] OTA Model Artifact Contract signing chain (MLO signs → DEV co-signs → FW verifies) | FW verifies the signature chain (catches *unsigned*), but **model monotonic anti-rollback not specified at firmware strength** → **D=7** | Per-model monotonic version counter enforced on device; reject any model version ≤ current; pen-test the model path each release | High → mitigate (was the Review V3 S5 Security veto) |
| **FC-027** | **Provisioning key non-uniqueness:** a provisioning bug issues a batch of devices a duplicate/shared identity key (or an intermediate CA key leaks) | Fleet-wide identity spoofing / impersonation; blast radius = whole batch | Provisioning automation defect; no per-batch uniqueness audit | SEC→CLOUD→COMM | 10 | 2 | 8 | 160 | [[SECURITY_ENGINEER_SKILL\|SEC]] §4.4 PKI (unique per-device X.509); [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] §6.7 provisioning; [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §6.5 | No **fleet-wide key-uniqueness audit** contracted; duplicates invisible until exploited → **D=8** | Automated key-uniqueness assertion at provisioning + periodic fleet identity-collision scan; HSM-issued keys only | High → mitigate |
| **FC-028** | **Debug port left unlocked on a manufacturing sub-batch:** DFT/test fixture leaves JTAG/SWD enabled on a fraction of units | Physical attacker extracts keys/firmware/model IP; clones or backdoors devices | Per-design lockdown verified, but **per-unit/per-batch** production verification absent | SEC→HW→FW | 9 | 3 | 9 | 243 | [[SECURITY_ENGINEER_SKILL\|SEC]] §6.3 debug-lockdown; [[HARDWARE_ENGINEER_SKILL\|HW]] §6.4; [[FIRMWARE_ENGINEER_SKILL\|FW]] §3.3 Security Implementation Readiness (item e) | Checklist is **per-design**, not per-batch; **no field detection** of an unlocked port until exploited → **D=9** | Per-unit lockdown verification in the production test fixture (pass/fail gate); attestation that fuses are blown | **Open — mitigation MANDATORY** |
| **FC-029** | **Compromised/"lying" device feeds false telemetry:** a tampered device reports fabricated healthy/disease values while presenting valid mTLS identity and plausible twin state | Corrupts fleet aggregate, retraining data, and the incident picture; silently poisons FC-022's loop | Device tamper; mTLS authenticates identity, **not the truth of the data** | SEC→CLOUD→DATA→ML | 8 | 2 | 9 | 144 | [[SECURITY_ENGINEER_SKILL\|SEC]] mTLS device identity; secure boot | Identity is authenticated; **values are trusted** (HA-A3). No attestation or cross-source reconciliation → **D=9** | Remote attestation; cross-source/neighbour-consistency reconciliation; anomaly-bound on per-device value distributions | **Open — accept w/ monitoring → mitigation** |
| **FC-030** | **Secret baked into an OTA artifact/model:** a debug API key or test credential committed during dev is bundled into a firmware image or model blob and distributed fleet-wide | Credential exposure across the entire fleet | Secret embedded in a binary/weights blob, not source | SEC→OTA→FW | 8 | 2 | 4 | 64 | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] §3.3 secret detection in CI (blocks merge); [[FIRMWARE_ENGINEER_SKILL\|FW]] §9 no hardcoded secrets | CI secret-scan covers source; may **miss secrets inside a compiled blob/weights** → D moderate | Scan built artifacts (binaries, model blobs) for secrets pre-signing; entropy/credential heuristics on weights | Medium — accept w/ monitoring |

### 4.7 OTA-Initiated Failure Chains (cross-cutting MLO→DEV→BACK→FW loop)

| ID | Failure Mode | Effect | Cause | Layers | S | O | D | RPN | Design Controls | Detection Controls | Recommended | Residual |
|---|---|---|---|---|--:|--:|--:|--:|---|---|---|---|
| **FC-031** | **OTA campaign stalls in DevOps `DISTRIBUTING`**; Backend sets `desired` only after `DISTRIBUTED`, so `desired` is never set → twin `desired == reported` (old) → no mismatch → **campaign silently dead, no alert** | New disease pattern never reaches the fleet; nobody is told the campaign died | Distribution-pipeline fault before `DISTRIBUTED`; no pre-`DESIRED_SET` watchdog | OTA(DEV)→CLOUD→FW | 6 | 5 | 8 | 240 | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] post-launch twin-sync monitor; [[MLOPS_ENGINEER_SKILL\|MLO]] §6.9 "stuck non-ACTIVE >1 h" | **Both monitors are downstream of `DESIRED_SET`**; the OTA end-to-end timeout (24 h staged / 1 h hotfix) has **no owner on the pre-`DESIRED_SET` hops** (Review V2 **F1**) → **D=8** | Assign the **chain-level OTA transaction watchdog** to [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] (extend fleet-mismatch monitoring to the whole MLO→ACTIVE wall-clock) | **Open — mitigation MANDATORY** |
| **FC-032** | **Stuck partial rollout:** staged rollout pauses at an ambiguous canary health gate and is never resumed (promotion notification lost / owner unaware) → fleet permanently split across model versions | Two cohorts give inconsistent disease calls in the same region → operator confusion, inconsistent field decisions | No max-dwell-time on a paused stage; promotion is a notification, not a deadline | OTA→CLOUD→FW→FRONT | 6 | 4 | 6 | 144 | [[MLOPS_ENGINEER_SKILL\|MLO]] §6.9 staged rollout; [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] §6.2/§6.7 promotion notification | "Paused" is not distinguished from "in progress"; no alert on a stage exceeding max dwell → **D=6** | Max-dwell timer per stage with auto-escalation; "rollout stalled" alert distinct from "in progress" | High → mitigate |
| **FC-033** | **Rollback compatibility race:** FW sanity-check fails → `ROLLED_BACK` to the previous model in slot B, but firmware has advanced since → the rolled-back **model + current firmware** mismatch (arena size / preprocessing) → device runs but inference silently wrong | Self-inflicted silent corruption created by the safety mechanism itself | Rollback target not re-checked against *current* firmware version at rollback time | OTA→FW→ML | 8 | 3 | 9 | 216 | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] OTA Model Artifact Contract compatibility manifest (model↔firmware range); [[FIRMWARE_ENGINEER_SKILL\|FW]] §6.4 sanity check before ACTIVE | Compatibility checked at **apply**, not re-validated at **rollback**; sanity check can pass on plausible-but-wrong output → **D=9** | Re-validate rollback-target ↔ current-firmware compatibility before reverting; if incompatible, fail to a known-safe SUPPRESS state, not to an incompatible model | **Open — mitigation MANDATORY** |
| **FC-034** | **Reproducibility rot found under pressure:** the MLOps weekly rebuildability job samples one model per product line; a never-sampled model's lineage has silently rotted (a pinned dependency moved/yanked) — discovered only when an emergency retrain is needed during an outbreak | Cannot rebuild the trusted model; emergency disease-response stalls at the worst time | Sampling ≠ full coverage; upstream package mutability | OTA(MLO)→DATA | 7 | 3 | 7 | 147 | [[MLOPS_ENGINEER_SKILL\|MLO]] §5 Model Rebuildability Verification Job (samples one/product-line/week) | A rarely-touched model's rot surfaces only on demand → **D=7** | Risk-weighted full-coverage rebuild over a bounded window; vendored/immutable dependency mirror; pre-outbreak "break-glass" rebuild drill | High → mitigate |
| **FC-035** | **OTA thundering herd:** after a mass connectivity outage clears, ~50k devices simultaneously poll for desired-state / attempt download → DevOps + Backend overwhelmed → **legitimate telemetry ingest starved** → cascading degradation | Fleet-wide ingest brown-out triggered by recovery itself, during the post-outage window when data matters | Synchronised reconnection; no jittered backoff for desired-state polling at fleet scale | OTA→CLOUD→DATA | 6 | 4 | 5 | 120 | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] staged rollout/cohorts; [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] autoscaling | Reconnection storm ≠ staged rollout; no jittered-backoff contract; Scalability Contract pending → **D=5** | Mandated jittered exponential backoff for reconnect/poll; admission control / rate-limit at the broker; surge headroom in `System Scalability Contract` | High → mitigate |
| **FC-036** | **Flash-budget check defeated by a mis-tagged hardware revision:** the model flash-budget check passes against the declared hardware-ID profile, but a HW rev with a smaller flash part is mis-tagged → model write **overflows into a reserved region** → next-boot config corrupted | Bricked/degraded units on the mis-tagged revision after an otherwise-valid model OTA | Hardware-ID/profile mismatch; budget check trusts the declared profile | OTA→FW→HW | 8 | 2 | 6 | 96 | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] OTA Model Artifact Contract flash-budget check field; [[FIRMWARE_ENGINEER_SKILL\|FW]] §6.4 on-device flash-budget verify | On-device verify catches a *correctly-tagged* overflow, but a **mis-tagged HW-ID defeats the check** → **D=6** | Device reports *measured* free flash (not declared profile); reconcile HW-ID against a provisioning registry before `DESIRED_SET` | Medium — mitigate |

---

## 5. RPN Distribution and Analysis

### 5.1 Distribution by classification

| Classification | RPN range | Count | Chains |
|---|---|--:|---|
| **Critical** | ≥200 | **17** | FC-001, FC-004, FC-005, FC-006, FC-007, FC-008, FC-011, FC-012, FC-013, FC-014, FC-016, FC-017, FC-022, FC-025, FC-028, FC-031, FC-033 |
| **High** | 100–199 | **15** | FC-003, FC-009, FC-010, FC-015, FC-018, FC-019, FC-021, FC-023, FC-024, FC-026, FC-027, FC-029, FC-032, FC-034, FC-035 |
| **Medium** | 50–99 | **4** | FC-002, FC-020, FC-030, FC-036 |
| **Low** | <50 | **0** | — (see note) |
| **Total** | — | **36** | — |

> **Why zero Low chains:** this is an *adversarial cross-layer* FMEA, deliberately hunting severe, silent, multi-boundary chains. Low-RPN single-layer failures are out of scope by §1.2 and belong to per-layer FMEAs. The absence of Low chains is a property of the hunting strategy, not an inflated scoreboard.

### 5.2 Brutal-detectability call-out — chains with NO detection mechanism (D ≥ 8)

These **15** chains are detectable late, only by luck, or **not at all** in the system as specified. They are the core of this FMEA. Stated plainly:

- **D = 9 (no detection mechanism exists):** **FC-001** (in-range sensor drift — undetectable on-device), **FC-008** (stack→arena overlap — silent weight corruption), **FC-022 KEYSTONE** (drift monitor re-baselines against its own corruption — invisible to every cited control), **FC-028** (unlocked debug port — no field detection until exploited), **FC-029** (lying device — values trusted, not attested), **FC-033** (rollback model↔firmware mismatch — sanity check passes on plausible-but-wrong output).
- **D = 8 (no contracted detection control):** **FC-004** (anti-rollback counter wear, unverified), **FC-005** (silent loss of in-flight record below aggregate noise floor), **FC-006** (clock-drift sample-rate error, parity tested only at lab temp), **FC-007** (RTC drift, device timestamps trusted), **FC-010** (schema version not bumped, no content-hash check), **FC-011** (shallow liveness — heartbeat proves the ISR, not the task), **FC-012** (drop-oldest data loss below noise floor), **FC-014** / **FC-031** (OTA stall upstream of `DESIRED_SET` — F1, unwatched), **FC-016** (frame-counter desync — loss at the network server, invisible to ingest-health), **FC-024** (backfill mutation — rebuildability blind to it), **FC-025** (re-identification — no automated test), **FC-027** (key non-uniqueness — no uniqueness audit).

No RPN above was reduced to make the gate appear safe. **FC-001 (486)** and **FC-022 (405)** top the 1000-point scale *because* they are simultaneously severe and undetectable — exactly the combination the robustness program exists to find, and exactly what the unconducted FMEA was silently presuming away.

### 5.3 Top 12 highest-RPN chains

| Rank | ID | RPN | One-line |
|--:|---|--:|---|
| 1 | FC-001 | 486 | In-range sensor drift → silent corrupt inference |
| 2 | FC-022 | 405 | Closed-loop drift → re-baselined monitor → fleet-wide silent erosion (KEYSTONE) |
| 3 | FC-007 | 288 | RTC drift → wrong event-time → mis-windowed/dropped alerts |
| 4 | FC-006 | 280 | Clock/temp drift → sample-rate → wrong features |
| 4 | FC-012 | 280 | Store-and-forward drops earliest onset telemetry |
| 6 | FC-005 | 252 | Brown-out at TX → buffer-pointer corruption → silent loss |
| 7 | FC-028 | 243 | Unlocked debug port on a production sub-batch |
| 8 | FC-014 | 240 | Downlink limit → `DESIRED_SET` never delivered, no mismatch |
| 8 | FC-017 | 240 | Cert expiry → aging cohort silently drops off |
| 8 | FC-031 | 240 | OTA stall pre-`DESIRED_SET` → silent dead campaign (F1) |
| 11 | FC-011 | 224 | Shallow liveness → "alive" device produces no inference |
| 11 | FC-016 | 224 | LoRaWAN frame-counter desync → NS silently drops uplinks |

### 5.4 Distribution by initiating layer

| Initiating layer | Chains | Critical | Median RPN |
|---|--:|--:|--:|
| Hardware | 7 | 5 | 252 |
| Firmware | 6 | 4 | 217 |
| Communication | 4 | 3 | 232 |
| Cloud/Backend | 4 | 0 | 126 |
| Data | 4 | 2 | 204 |
| Security | 5 | 1 | 160 |
| OTA (cross-cutting) | 6 | 2 | 145.5 |

> Hardware-, Firmware-, and Data-initiated chains carry the highest median risk — they are where **silent physical/numerical corruption** originates and propagates upward into the ML and fleet layers before any cloud-side control can see it.

### 5.5 Recurring failure-cause patterns (the meta-findings)

1. **Silent in-range corruption** — values stay within valid bounds but are wrong; no control detects "plausible but incorrect": FC-001, FC-006, FC-022, FC-029.
2. **Trusting device-reported state / shallow liveness** (HA-A3) — the system believes what devices say: FC-007, FC-011, FC-029, FC-018.
3. **Detection located downstream of the failure point** — the monitor lives after the damage: FC-014/FC-031 (after `DESIRED_SET`), FC-005/FC-012 (aggregate ingest-health misses single-device/earliest-event loss), FC-016 (loss at the network server).
4. **One-time/lab validation vs lifetime/field conditions** — validated once, then trusted forever: FC-001 (bring-up fidelity), FC-006/FC-009 (parity at lab temp / at integration), FC-013 (soak < field uptime), FC-028 (per-design not per-batch).
5. **Race conditions across asynchronous boundaries** — FC-003 (DMA vs inference), FC-008 (stack vs arena), FC-018 (desired vs reported), FC-020 (status ordering), FC-033 (rollback vs firmware version).
6. **Closed-loop self-reference** — the instrument monitors against its own corruption: FC-022 (drift baseline), FC-024 (lineage references a mutated partition).

### 5.6 Coverage gaps in current controls (no contracted detection anywhere in the design)

In-range drift detection · device-clock truthfulness · pre-`DESIRED_SET` OTA hop watchdog (F1) · per-device "went dark" liveness (vs aggregate) · end-to-end input-freshness timestamping · closed-loop multi-retraining-cycle degradation testing · per-batch production security verification (debug lockdown, key uniqueness) · automated re-identification testing · schema content-hash check · rollback-target compatibility re-validation.

---

## 6. Populated NFR Targets

The following replaces the `[TBD per product class]` placeholders in the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#5.1 NFR Verification Matrix — End-to-End System Robustness Category|System Robustness Contract NFRs (R1–R5)]]. Two product classes are defined: **Class A — Safety-Critical** (any actuation acted on physically in the field) and **Class B — Advisory/Monitoring** (operator-in-the-loop, e.g., AgriSpectra disease advisory). Targets are derived from the worst-case recovery and detection paths in §4.

| NFR | Previous Placeholder | Populated Target | Basis (FMEA Reference) |
|---|---|---|---|
| **R1 — Cross-Layer Failure Containment** | "containment validated by fault injection" (unquantified) | **Zero irreversible cross-layer propagation for all Critical (RPN ≥ 200) and High chains.** Containment invariants: **(a)** power-fail during any flash or buffer write must never render a device unbootable or silently lose the in-flight record (FC-002, FC-005); **(b)** a corrupted, stale, or in-range-wrong sensor/model output must fail to a **SUPPRESS** state — never emit a command/advisory derived from unverified input, and never fall back to an incompatible model (FC-001, FC-003, FC-033); **(c)** a single compromised/faulty device must not corrupt fleet aggregate or retraining state (FC-029, FC-022). Verified by [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] fault injection per Critical chain | FC-001, FC-002, FC-003, FC-005, FC-008, FC-022, FC-029, FC-033 |
| **R2 — Graceful Degradation Under Partial Failure** | "safety-critical functions preserved" (unquantified) | **100% of essential functions preserved under any single-layer degradation.** Essential functions defined as: device boots a valid image; device **suppresses** (does not emit) inference when input freshness/validity is unverified (FC-003, FC-011); device buffers **≥ 72 h** of telemetry on connectivity loss and emits an explicit **data-gap marker** on reconnection (FC-012, FC-005); the dashboard never shows a stale "all-clear" without a last-updated/freshness indicator (B3) | FC-003, FC-011, FC-012, FC-013, FC-019 |
| **R3 — Cross-Layer Recovery Time** | `[TBD per product class]` | **On-device fault recovery (watchdog/rollback to known-good): Class A ≤ 30 s, Class B ≤ 120 s** (FC-002, FC-011, FC-033). **Connectivity-loss recovery: re-establish telemetry ≤ 5 min after link restoration**, with a data-gap marker emitted (FC-012, FC-013). **Multi-layer transient recovery: Class A ≤ 5 min, Class B ≤ 30 min** (FC-019, FC-035). **OTA chain-level stall detection ≤ 15 min** (F1 watchdog), bounded by the end-to-end timeout **1 h hotfix / 24 h staged** (FC-014, FC-031). **Certificate-expiry lockout prevented** by rotating **≥ 30 days** before expiry (FC-017) | FC-002, FC-011, FC-012, FC-014, FC-017, FC-019, FC-031, FC-033, FC-035 |
| **R4 — Failure Chain Detection Coverage** | ≥95% | **≥95%** of Critical/High chains must have a **contracted detection control** with detection latency ≤ the R3 recovery window. **HONEST CURRENT STATE: NOT YET MET.** Of 32 Critical/High chains, **15 are D ≥ 8 (no/near-no detection)** → current coverage ≈ **53%**. The ≥95% target is confirmed **achievable only after** implementing the Recommended Additional Controls in §4 (absolute ground-truth anchor, in-range self-test, F1 OTA watchdog, per-device liveness, end-to-end input-freshness timestamp, device-clock cross-check, attestation). Until then, [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] reports actual coverage at each release gate | §5.2 detectability call-out; FC-001, FC-022, FC-031, FC-005, FC-012, FC-007 |
| **R5 — Robustness Regression Coverage** | 100% Critical/High | **100% of Critical and High chains (32 of 36) must have an automated [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] fault-injection regression test**, traced to its FC-ID, executed per release; any failure blocks the release. **Confirmed achievable as a contracted target**, with one expansion required: the current six [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]] scenarios cover single/multi-layer point faults but **not closed-loop (FC-022) or lifetime-drift (FC-001, FC-006) classes** — these need two new test classes (**multi-retraining-cycle degradation** and **accelerated-aging/temperature-conditioned parity**) | All 32 Critical/High FC-IDs; gap noted for FC-001, FC-006, FC-022 |

---

## 7. Integration with the System Robustness Contract

### 7.1 What each chain becomes

- **Becomes a robustness NFR design requirement (Critical, RPN ≥ 200, MANDATORY before production):** FC-001, FC-004, FC-005, FC-006, FC-007, FC-008, FC-011, FC-012, FC-013, FC-014, FC-016, FC-017, FC-022, FC-025, FC-028, FC-031, FC-033. Each requires a documented design-time mitigation in the System Robustness Contract and a [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] fault-injection scenario before the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] may sign the production release gate.
- **Becomes a [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] fault-injection regression scenario (all Critical + High, R5):** the 32 Critical/High chains map 1:1 to the cross-layer robustness regression suite. Two new test classes are required (see R5).
- **Requires a design change (new contracted control that does not exist today):** the F1 chain-level OTA watchdog (FC-014, FC-031); end-to-end input-freshness timestamp (FC-003, FC-011); absolute ground-truth drift anchor + B5 field-push classify-and-route (FC-022); per-device liveness/data-gap marker (FC-005, FC-012); device-clock cross-check (FC-007); per-batch production security verification (FC-028, FC-027); immutable-snapshot enforcement (FC-024); automated re-identification test (FC-025); rollback-target compatibility re-check (FC-033).
- **Accepted with monitoring (Medium, documented rationale):** FC-002, FC-020, FC-030, FC-036 — accepted with the routine monitoring noted, re-reviewed at the next FMEA update.

### 7.2 Cross-role ownership of mitigations

| Mitigation theme | Lead role | Supporting |
|---|---|---|
| In-range drift self-test + absolute ground-truth anchor (FC-001, FC-022, FC-006) | [[EDGE_AI_ML_ENGINEER_SKILL\|ML]] | [[HARDWARE_ENGINEER_SKILL\|HW]], [[MLOPS_ENGINEER_SKILL\|MLO]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] |
| F1 chain-level OTA watchdog (FC-014, FC-031) | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]], [[MLOPS_ENGINEER_SKILL\|MLO]] |
| End-to-end input freshness + true liveness (FC-003, FC-011) | [[FIRMWARE_ENGINEER_SKILL\|FW]] | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] |
| Per-device liveness / data-gap marker (FC-005, FC-012) | [[FIRMWARE_ENGINEER_SKILL\|FW]] | [[DATA_ENGINEER_SKILL\|DATA]], [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]] |
| Device-clock cross-check / time sync (FC-007, FC-017) | [[DATA_ENGINEER_SKILL\|DATA]] | [[FIRMWARE_ENGINEER_SKILL\|FW]], [[SECURITY_ENGINEER_SKILL\|SEC]] |
| Per-batch production security verification (FC-028, FC-027) | [[SECURITY_ENGINEER_SKILL\|SEC]] | [[HARDWARE_ENGINEER_SKILL\|HW]], [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] |
| Model anti-rollback / rollback compatibility (FC-026, FC-033) | [[SECURITY_ENGINEER_SKILL\|SEC]] | [[FIRMWARE_ENGINEER_SKILL\|FW]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|ARCH]] |
| Immutable snapshots + re-identification test (FC-024, FC-025) | [[DATA_ENGINEER_SKILL\|DATA]] | [[MLOPS_ENGINEER_SKILL\|MLO]], [[SECURITY_ENGINEER_SKILL\|SEC]] |
| Fleet-scale surge + jittered backoff (FC-019, FC-035) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DEV]] | [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]], [[DATA_ENGINEER_SKILL\|DATA]] |

> Each row above should be filed as an ADR by the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] (Critical/High chains, with [[SECURITY_ENGINEER_SKILL\|Security]] concurrence where security-relevant) and tracked to closure before the production release gate.

### 7.3 Release-gate consequence

Per [[QA_TEST_AUTOMATION_ENGINEER_SKILL#7. Decision Authority & Governance|QA §7]], any Critical chain without a passing fault-injection regression test, or any remaining `[TBD]` NFR target, is a **validation gap** that forces a **NO-GO** with a validation-gap ADR. This FMEA removes the `[TBD]` targets (§6); the remaining gate condition is implementing and verifying the §7.1 design-change mitigations. **R4 is honestly below target today (≈53%)** and must reach ≥95% (with the new detection controls) before an unconditional production sign-off.

---

## 8. FMEA Maintenance

- **Owner:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] (single accountable owner of system robustness).
- **Validator:** [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA & Test Automation Engineer]] (maps each chain to a fault-injection scenario; reports R4 coverage and R5 pass/fail per release).
- **Update triggers:** (a) any major architecture revision; (b) any new layer, protocol, platform, or external interface; (c) **any production incident that reveals a failure chain not in this inventory** (mandatory same-cycle addition); (d) a new product class (re-derive R3 numbers).
- **Review cadence:** reviewed at every **Architecture Review Board (ARB)** milestone; re-baselined with the System Robustness Contract version.
- **Versioning:** SemVer. This is **v1.0** — the first conducted FMEA, deliberately adversarial and biased toward silent cross-layer chains. v1.x adds chains from incidents and reviews; a major bump follows a failure-domain or product-class change.
- **Stored alongside:** the System Robustness Contract and its FMEA/FTA worksheets in version control, per [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL#8. Standards & Best Practices|Architect §8]].

---

> **Next Update:** At the next major architecture revision, or after the first production incident that reveals a failure chain not in this inventory — whichever comes first. The standing expectation, per §5.2, is that the field will first reveal one of the **D ≥ 8 silent chains** above; when it does, the corresponding mitigation in §7.1 must already be in flight, not discovered in the incident.
