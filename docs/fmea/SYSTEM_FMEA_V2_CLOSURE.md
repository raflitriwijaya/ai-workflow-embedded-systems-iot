---
title: "System FMEA V2 — Critical Chain Closure Design"
date: 2026-06-24
status: draft
version: "2.0"
owner: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] + [[QA_TEST_AUTOMATION_ENGINEER_SKILL]]"
methodology: "IEC 60812 (FMEA) + IEC 61025 (FTA)"
tags:
  - fmea
  - robustness
  - reliability
  - cross-layer
  - mitigation
  - rpn-closure
  - system-safety
cssclass: fmea-worksheet
---

# System FMEA V2 — Critical Chain Closure Design

> **Owners (joint):** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] (robustness NFR + design-time mitigation authority, §2/§5.1/§8) and [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA & Test Automation Engineer]] (fault-injection verification + R4/R5 reporting, §2/§3.4).
> **Methodology:** IEC 60812 — FMEA re-scoring; IEC 61025 — FTA for top events. Same calibrated S/O/D scales as [[SYSTEM_FMEA_V1|System FMEA V1]] §3.
> **Closes:** the 17 Critical (RPN ≥ 200) "Open — mitigation MANDATORY" chains enumerated in [[SYSTEM_FMEA_V1|System FMEA V1]] §5.1.
> **Status:** `draft` — these are **buildable mitigation designs for the Development stage (§3.3)**, not yet-verified closures. **No chain is "closed" here in the gate sense.** A chain becomes closed only when its QA fault-injection scenario (§3 per-chain) passes in the cross-layer robustness regression suite ([[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]], NFR R5) and the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] signs the production gate (HG-04).
> **Referenced by:** [[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 (R1–R5)]], [[SYSTEM_FMEA_V1#7. Integration with the System Robustness Contract|FMEA V1 §7]].

---

## 1. Purpose, Scope, and Honesty Rules

### 1.1 What this document does

[[SYSTEM_FMEA_V1|System FMEA V1]] enumerated 36 cross-layer chains and surfaced **17 Critical** (RPN ≥ 200), of which **14 carry D ≥ 8** (no contracted detection control) by their §4 worksheet scores. R4 detection coverage self-reports below its ≥ 95 % gate. V1 named the *direction* of each fix in its "Recommended" column but did not design buildable controls, re-score residual RPN, or map each chain to a QA fault-injection test.

This V2 supplies, **for each of the 17 Critical chains**: (1) a concrete buildable mitigation with a single accountable role owner (per [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]]); (2) a detection control with the **specific metric that triggers the alert** (required for every D ≥ 8 chain); (3) re-scored S/O/D and RPN; (4) an automatable QA fault-injection scenario; and (5) an **honest closure verdict** — fully closed, detection-closed (the physical failure still occurs but is now visible), or partially mitigated with a named residual.

### 1.2 Scope boundary (honest)

In scope: the **17 Critical chains only** (FC-001, FC-004, FC-005, FC-006, FC-007, FC-008, FC-011, FC-012, FC-013, FC-014, FC-016, FC-017, FC-022, FC-025, FC-028, FC-031, FC-033). The **15 High chains (100–199)** are **out of scope for V2** and retain their V1 scores; 4 of them (FC-010, FC-024, FC-027, FC-029) are D ≥ 8 and become the defined next burn-down (§5.3). This document does **not** lower any S/O/D by assertion, does not mark a chain closed without a QA scenario, and does not change any ratified §6 interface contract — each mitigation is grounded in an **existing** SKILL.md `§` or named standard, and any that requires a new contracted control is routed to an ADR (§6).

### 1.3 Re-scoring methodology (so the numbers are auditable)

Per IEC 60812, mitigation acts on **Occurrence** and **Detectability**; **Severity is intrinsic to the failure *effect* and is held fixed unless the design changes the effect itself.**

- **D drops** only when a *contracted* detection control with a named trigger metric is added (detective control). A telemetered metric + alert moves a chain from D 8–9 (no contracted control) to D 2–3 (promptly detected by a contracted alert/test).
- **O drops** only when a preventive/structural control reduces the probability of the *effect* (e.g., a pool allocator structurally prevents fragmentation-driven `malloc` failure; an atomic journaled index prevents pointer corruption).
- **S drops** only when the design converts the effect to a less-severe class — almost always by a **fail-safe SUPPRESS** that turns "silent wrong output" into "known no output, recoverable" (the R1(b) containment invariant, [[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 R1]]). Where the worst-case effect is unchanged (e.g., a defeated security control still enables fleet-wide compromise), **S is held**.

Numeric thresholds below are **initial proposed values to be calibrated** during §3.3 against field/HIL data; all carry explicit units. They are not silent budget trades — any value that proves unmeetable triggers an ADR per [[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6]] and CLAUDE.md §10.1.

---

## 2. Closure Summary (before → after)

| Rank (V1) | FC | One-line | Before S·O·D = RPN | After S·O·D = RPN | Verdict |
|--:|---|---|--:|--:|---|
| 1 | **FC-001** | In-range spectral-AFE drift | 9·6·9 = **486** | 7·4·3 = **84** | Partially closed (sub-threshold residual) |
| 2 | **FC-022** | Closed-loop silent corruption (KEYSTONE) | 9·5·9 = **405** | 9·3·3 = **81** | Strongly mitigated (anchor-staleness residual) |
| 3 | **FC-007** | RTC drift → wrong event-time | 6·6·8 = **288** | 6·4·3 = **72** | Detection-closed |
| 4 | **FC-006** | Clock/temp drift → sample-rate error | 7·5·8 = **280** | 7·3·3 = **63** | Closed |
| 4 | **FC-012** | Store-and-forward drops earliest onset | 7·5·8 = **280** | 6·4·3 = **72** | Detection-closed |
| 6 | **FC-005** | Brown-out at TX → buffer-pointer corruption | 6·6·7 = **252** | 6·3·3 = **54** | Closed |
| 7 | **FC-028** | Unlocked debug port on production sub-batch | 9·3·9 = **243** | 9·2·2 = **36** | Closed (manufacturing-escape) |
| 8 | **FC-014** | Downlink limit → `DESIRED_SET` never delivered | 6·5·8 = **240** | 6·4·3 = **72** | Detection-closed (downlink physics residual) |
| 8 | **FC-017** | Cert expiry → aging cohort drops off | 8·5·6 = **240** | 8·3·2 = **48** | Closed |
| 8 | **FC-031** | OTA stall pre-`DESIRED_SET` (F1) | 6·5·8 = **240** | 6·4·2 = **48** | Closed |
| 11 | **FC-011** | Shallow liveness → "alive" but no inference | 7·4·8 = **224** | 7·3·2 = **42** | Closed |
| 11 | **FC-016** | LoRaWAN frame-counter desync | 7·4·8 = **224** | 7·2·3 = **42** | Closed |
| 13 | **FC-004** | Anti-rollback counter wear, unverified | 9·3·8 = **216** | 9·2·2 = **36** | Detection-closed (fuse-endurance residual) |
| 13 | **FC-008** | Stack→arena overlap → silent weight corruption | 8·3·9 = **216** | 5·2·2 = **20** | Closed |
| 13 | **FC-025** | Re-identification via engineered features | 9·3·8 = **216** | 9·2·3 = **54** | Closed (adversarial residual) |
| 13 | **FC-033** | Rollback model↔firmware mismatch | 8·3·9 = **216** | 6·2·2 = **24** | Closed |

**Result:** all 17 Critical chains drop below the RPN ≥ 200 threshold after mitigation; **0 remain Critical**. The highest residuals (FC-001 = 84, FC-022 = 81) are the honest "detection-closed, not prevention-closed" cluster — the physical/numerical failure can still occur sub-threshold, but it is now *visible and bounded* rather than silent. Detail and caveats per chain in §3; aggregate honesty assessment in §4.

---

## 3. Per-Chain Closure Design

> Priority order per the task brief: **FC-022, FC-001, FC-006, FC-031** first (keystones), then by descending V1 RPN. Each block cites only **existing** SKILL.md `§` controls and named standards; the trigger metric is stated for every D ≥ 8 chain.

### 3.1 FC-022 — Closed-loop silent corruption (KEYSTONE) — *strongly mitigated*

- **Mitigation:** Install an **absolute ground-truth anchor**. [[MLOPS_ENGINEER_SKILL|MLOps]] and [[EDGE_AI_ML_ENGINEER_SKILL|ML]] maintain a **frozen, externally lab-labelled golden validation set** whose labels do **not** come from the field (so they cannot co-drift). The accuracy-floor gate ([[MLOPS_ENGINEER_SKILL|MLOps]] §6.9) is re-pointed to evaluate against this frozen anchor **every retrain**, instead of against re-baselined field labels. The drift monitor ([[MLOPS_ENGINEER_SKILL|MLOps]] §4) adds a **non-self-referential** comparison against the frozen anchor distribution. FC-001's on-device self-test (§3.2) breaks the upstream sensor-drift root; [[DATA_ENGINEER_SKILL|DATA]] §6.2 DQIR carries the data-side gate; the physical root cause is classified and routed to [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Research]] (§3.7 assumption validation, B5 field-push).
- **Owner:** [[EDGE_AI_ML_ENGINEER_SKILL|ML]] / [[MLOPS_ENGINEER_SKILL|MLOps]] (lead), supporting [[DATA_ENGINEER_SKILL|DATA]], [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|RES]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] — per [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 1.
- **Buildable in §3.3:** frozen-anchor dataset is captured once and version-pinned (immutable snapshot, [[DATA_ENGINEER_SKILL|DATA]] §4.6); gate re-pointing is a config + CI change in the MLOps training pipeline.
- **Detection control + trigger metric:** `accuracy_vs_frozen_anchor_delta` computed on every retrain. **Alert when** Δaccuracy drops **> 1.0 percentage point** from the committed baseline on any single retrain, **or** any monotonic decline across **≥ 2 consecutive retrains** (erosion-shaped statistical trend alarm — the kind V3 flagged as missing from "crash-shaped" machinery). Because the anchor is frozen, this trigger cannot be fooled by re-baselining.
- **RPN:** S 9 → **9** (held: if it slips through, fleet-wide erosion is still S9); O 5 → **3** (FC-001 self-test + grouped/immutable training data reduce the corrupting input); D 9 → **3** (frozen-anchor gate + multi-cycle test = contracted, non-self-referential detection). **405 → 81.**
- **QA scenario (NEW test class — multi-retraining-cycle degradation, R5):** automate an N-cycle closed-loop simulation: inject a controlled spectral-drift signal into synthetic field telemetry, run it through ingest → retrain → re-evaluate for ≥ 5 simulated retrain cycles, and **assert** that `accuracy_vs_frozen_anchor` does not erode > 1.0 pp/cycle and that the trend alarm fires by cycle 2. This is the first of the two new R5 test classes ([[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 R5]]); it does not exist in the current six [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]] scenarios.
- **Honest verdict:** **Strongly mitigated, not fully closed.** Residual: over a 7-year field life the frozen anchor can become *unrepresentative* of evolved field reality (**anchor staleness**) — refreshing it reintroduces a slow, human-reviewed update path. This is a **new, smaller residual** the mitigation creates; logged as candidate **FC-037 (anchor-staleness)** for V2.x, governed by a Research-reviewed anchor-refresh cadence with documented provenance (never an unreviewed field-label refresh).

### 3.2 FC-001 — In-range spectral-AFE drift — *partially closed*

- **Mitigation:** [[HARDWARE_ENGINEER_SKILL|HW]] adds an on-board **stable reflectance/optical reference path** (a known reference target measured by the same AFE). [[EDGE_AI_ML_ENGINEER_SKILL|ML]] extends the [[HARDWARE_ENGINEER_SKILL|HW]] §6.3 Sensor Data Fidelity loop from a one-time bring-up check to a **lifetime on-device reference-channel self-test** on a fixed cadence (e.g., every 24 h): measure the reference target, compare per-band against the factory-characterized golden reference stored at provisioning, compute a drift metric, and on exceedance enter **SUPPRESS** (no inference emitted) per R1(b). Grounds: [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARCH]] §5.1 R1 (detect corrupted sensor data) and §8 (IEC 60812).
- **Owner:** [[EDGE_AI_ML_ENGINEER_SKILL|ML]] (lead), supporting [[HARDWARE_ENGINEER_SKILL|HW]], [[MLOPS_ENGINEER_SKILL|MLOps]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 1.
- **Buildable in §3.3:** reference path is a bring-up hardware addition; self-test + SUPPRESS gating is firmware/ML logic against an existing golden reference.
- **Detection control + trigger metric:** `reference_channel_drift_pct` (per spectral band) telemetered. **Alert when** any band deviates **> 3 %** from the factory golden reference, **or** the drift *rate* exceeds the characterized aging curve by **> 2σ**. Detection works against in-range drift precisely because the reference target is fixed and known, so AFE drift shows up independent of the (also-drifting) field signal.
- **RPN:** S 9 → **7** (SUPPRESS converts silent fleet-wide false-neg/pos into a *flagged, recoverable* recalibration/RMA case); O 6 → **4** (periodic re-characterization + field replacement shrinks the population running impactful-but-undetected drift); D 9 → **3** (contracted on-device self-test + telemetered metric + alert). **486 → 84.**
- **QA scenario (NEW test class — accelerated-aging / temperature-conditioned parity, R5):** inject a slow in-range drift onto the reference-channel input on the HIL rig across the operating temperature range; assert the self-test trips SUPPRESS and emits `reference_channel_drift_pct` before the model's output crosses a wrong-decision boundary. Extends [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(b)]] (sensor corruption) from bit-flip to *slow plausible drift* — the second new R5 test class.
- **Honest verdict:** **Partially closed.** Residual: drift **below the 3 % alarm** that is still operationally meaningful, and co-aging of the reference path itself, remain undetected on-device — bounded by the lifetime re-characterization cadence, not eliminated. RPN 84 is honest, not 0.

### 3.3 FC-006 — Clock/temp drift → sample-rate error — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] adds **runtime timestamping of the actual sample interval** (capture-timer delta per acquisition window); if the measured rate deviates from nominal beyond tolerance, flag the feature vector and SUPPRESS/correct. [[HARDWARE_ENGINEER_SKILL|HW]] §4.7 disciplines the clock (TCXO or temperature-compensation table). [[EDGE_AI_ML_ENGINEER_SKILL|ML]] §6.3 parity vectors are re-validated across temperature, not only at lab temperature.
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead, runtime sample-rate verify), supporting [[HARDWARE_ENGINEER_SKILL|HW]], [[EDGE_AI_ML_ENGINEER_SKILL|ML]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]].
- **Detection control + trigger metric:** `sample_interval_deviation_ppm` telemetered. **Alert when** deviation **> 5,000 ppm (0.5 %)** from nominal. Plus the temperature-conditioned HIL parity test below.
- **RPN:** S 7 → **7** (held); O 5 → **3** (clock discipline reduces drift magnitude); D 8 → **3** (runtime verify + temp-conditioned parity = contracted detection). **280 → 63.**
- **QA scenario:** temperature-conditioned parity (new R5 class shared with FC-001): run the golden parity vectors on the HIL rig across the full operating-temperature range; assert effective sample rate stays within 5,000 ppm and feature-vector parity holds bit-for-bit (or within the contracted tolerance) at every temperature step.
- **Honest verdict:** **Closed.** Residual: excursions beyond the characterized temperature range (out of spec) — covered by SUPPRESS-on-deviation.

### 3.4 FC-031 — OTA stall pre-`DESIRED_SET` (F1) — *closed*

- **Mitigation:** [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] builds the **F1 chain-level OTA transaction watchdog** — a single wall-clock timer started when [[MLOPS_ENGINEER_SKILL|MLOps]] initiates a campaign (model → Production), spanning the entire MLO→ACTIVE path **including the pre-`DESIRED_SET` hops** (DevOps `DISTRIBUTING`). Extends [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] §6.2 fleet-mismatch monitoring *upstream* of `DESIRED_SET`, closing the unwatched hop named in Review V2 F1.
- **Owner:** [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] (lead), supporting [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]], [[MLOPS_ENGINEER_SKILL|MLOps]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 2.
- **Detection control + trigger metric:** `campaign_elapsed_wallclock_s` vs per-stage SLA. **Alert when** a campaign has **no `DESIRED_SET`** within its stage deadline, bounded by the OTA end-to-end timeout (**1 h hotfix / 24 h staged**); chain-level stall detection within **≤ 15 min** ([[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 R3]]). The alert names the stuck stage.
- **RPN:** S 6 → **6** (held); O 5 → **4** (a `DISTRIBUTED` handshake barrier slightly reduces stall probability); D 8 → **2** (dedicated chain-level watchdog with explicit alert). **240 → 48.**
- **QA scenario:** in the staging OTA pipeline, force a campaign to hang in `DISTRIBUTING` (never reach `DISTRIBUTED`); assert the F1 watchdog fires a "campaign stalled — stage `DISTRIBUTING`" alert within 15 min and that `desired == reported` does **not** read as healthy. Extends the OTA end-to-end validation in [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]] (OTA path) with a pre-`DESIRED_SET` stall case.
- **Honest verdict:** **Closed.** This was a pure detection gap (F1); the watchdog directly fills it.

### 3.5 FC-007 — RTC drift → wrong event-time — *detection-closed*

- **Mitigation:** [[DATA_ENGINEER_SKILL|DATA]] cross-checks **device timestamp vs broker-receipt time** at ingest (an independent, trusted clock), computes skew, and corrects/flags event-time when skew exceeds tolerance (extends [[DATA_ENGINEER_SKILL|DATA]] §4.5 watermarks/event-time and §6 late-data handling). [[FIRMWARE_ENGINEER_SKILL|FW]] adds a periodic **time-sync downlink** to discipline the RTC.
- **Owner:** [[DATA_ENGINEER_SKILL|DATA]] (lead), supporting [[FIRMWARE_ENGINEER_SKILL|FW]], [[SECURITY_ENGINEER_SKILL|SEC]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 5.
- **Detection control + trigger metric:** `device_vs_broker_clock_skew_s` per device. **Alert when** skew **> 60 s** (calibrate to the watermark window). Surfaces the previously-trusted device clock against an independent reference.
- **RPN:** S 6 → **6**; O 6 → **4** (periodic sync caps drift accumulation); D 8 → **3** (contracted ingest skew cross-check). **288 → 72.**
- **QA scenario:** replay telemetry with deliberately skewed device timestamps (±minutes/hours) through the ingest pipeline; assert skew is detected, event-time is corrected into the right window, and the skew alert fires above 60 s. Maps to [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(d/f)]] (connectivity-loss backfill / late-data merge).
- **Honest verdict:** **Detection-closed.** The RTC still drifts (physical); we now detect and correct it. Devices offline long enough to miss time-sync (couples FC-017) retain bounded skew — visible, not silent.

### 3.6 FC-012 — Store-and-forward drops earliest onset — *detection-closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §4.4 emits an explicit **buffer-overflow / data-gap event** carrying the dropped time-range when FIFO eviction occurs, and switches from pure FIFO to **priority retention** (anomalous / disease-positive records retained over routine ones). [[DATA_ENGINEER_SKILL|DATA]] §3.6 reconciles gap markers.
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[DATA_ENGINEER_SKILL|DATA]], [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 4.
- **Detection control + trigger metric:** per-device `data_gap_event{dropped_range}`. **Alert when** any gap marker is received (DATA-side), converting below-noise-floor silent loss into an explicit signal. Supports the R2 ≥ 72 h buffer requirement.
- **RPN:** S 7 → **6** (anomalous-record prioritization preserves the highest-value onset signal); O 5 → **4** (≥ 72 h buffer reduces overflow frequency); D 8 → **3** (explicit per-device gap marker). **280 → 72.**
- **QA scenario:** simulate a multi-day connectivity outage that overflows the buffer; assert a data-gap event with the correct dropped range is emitted on reconnection and that anomaly-flagged records survive eviction. Maps to [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(d)]] (MQTT connectivity loss).
- **Honest verdict:** **Detection-closed.** An outage longer than the buffer still loses data — but now *visibly* (gap marker) and *selectively* (onset retained).

### 3.7 FC-005 — Brown-out at TX → buffer-pointer corruption — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §4.4 makes the store-and-forward index **atomic/journaled** across reset (write-ahead or double-buffered index with CRC); emits a data-gap marker on recovery ([[DATA_ENGINEER_SKILL|DATA]] §4.5 dedup/idempotency handles duplicates). [[HARDWARE_ENGINEER_SKILL|HW]] sets the brown-out threshold above the flash/buffer-write minimum Vcc. Satisfies R1(a) (power-fail-safe writes).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[DATA_ENGINEER_SKILL|DATA]], [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]], [[HARDWARE_ENGINEER_SKILL|HW]].
- **Detection control + trigger metric:** per-device `data_gap_event` on reboot recovery (same family as FC-012); DATA reconciles loss vs duplicate.
- **RPN:** S 6 → **6**; O 6 → **3** (atomic journaled index + brown-out threshold prevent most corruption); D 7 → **3** (gap marker). **252 → 54.**
- **QA scenario ([[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(a)]] — voltage brown-out):** inject a supply sag during a LoRaWAN TX peak on the HIL rig; assert the buffer index survives (no corruption), no in-flight record is silently lost, and a gap marker is emitted if a record was dropped.
- **Honest verdict:** **Closed** — structural (atomic index) + detective (gap marker).

### 3.8 FC-028 — Unlocked debug port on production sub-batch — *closed (manufacturing-escape)*

- **Mitigation:** [[SECURITY_ENGINEER_SKILL|SEC]] §6.3 + [[HARDWARE_ENGINEER_SKILL|HW]] §6.4 add **per-unit debug-lockdown verification** in the production test fixture (read fuse state; pass/fail gate; a unit cannot ship without a fuses-blown attestation). Field attestation per [[DEVICE_ATTESTATION_SPEC|Device Attestation Spec]] (RATS/DICE, IETF RFC 9334) reports lockdown state in the heartbeat. Grounds also [[FIRMWARE_ENGINEER_SKILL|FW]] §3.3 SIRC item (e).
- **Owner:** [[SECURITY_ENGINEER_SKILL|SEC]] (lead), supporting [[HARDWARE_ENGINEER_SKILL|HW]], [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 6. Touches the security baseline → `ESC-SEC`; SEC owns the binding decision (HG-01).
- **Detection control + trigger metric:** manufacturing gate `debug_lockdown_verified` (per unit, pass/fail) + field `attestation.debug_locked`. **Alert when** any device reports `debug_locked = false`.
- **RPN:** S 9 → **9** (held: physical key/IP extraction is still catastrophic); O 3 → **2** (per-unit gate prevents shipping unlocked units); D 9 → **2** (per-unit production gate + field attestation). **243 → 36.**
- **QA scenario:** on the production fixture, present a unit with JTAG/SWD deliberately left enabled; assert the gate fails the unit (cannot ship). On a field rig, assert attestation reports `debug_locked` and the backend alerts on a spoofed `false`.
- **Honest verdict:** **Closed** for the *manufacturing-escape* chain. Residual (out of scope): a sophisticated physical attack against a *correctly-locked* port — a different threat class, not this chain.

### 3.9 FC-014 — Downlink limit → `DESIRED_SET` never delivered — *detection-closed*

- **Mitigation:** Same F1 chain-level OTA watchdog as FC-031, extended to require a **device ACK of desired-state** within N× the downlink SLA; on no-ACK, alert and schedule a downlink retry / proactive re-push at the next uplink window. Grounds: [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] §6.2, [[MLOPS_ENGINEER_SKILL|MLOps]] §6.9, [[SECURITY_ENGINEER_SKILL|SEC]] §4.3 (LoRaWAN), ARCH OTA end-to-end timeout.
- **Owner:** [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] (lead), supporting [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]], [[MLOPS_ENGINEER_SKILL|MLOps]], [[FIRMWARE_ENGINEER_SKILL|FW]] (ACK).
- **Detection control + trigger metric:** `devices_without_desired_ack` per campaign. **Alert when** a device has no desired-state ACK after **N = 3** downlink windows.
- **RPN:** S 6 → **6**; O 5 → **4**; D 8 → **3** (watchdog at the downlink hop — kept at 3 not 2 because LoRaWAN downlink physics lengthen detection latency). **240 → 72.**
- **QA scenario:** in the staging pipeline, drop downlink delivery of `DESIRED_SET` to a cohort; assert the no-ACK alert fires within N windows and a retry/re-push is scheduled (the twin does not read healthy).
- **Honest verdict:** **Detection-closed.** LoRaWAN downlink is physics-bounded — delivery cannot be guaranteed, only detected and retried. The chain is detection-closed; the underlying delivery constraint persists by design.

### 3.10 FC-017 — Cert expiry → aging cohort drops off — *closed*

- **Mitigation:** [[SECURITY_ENGINEER_SKILL|SEC]] §4.4 + [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] §4.4 rotate certs **≥ 30 days before expiry** with offline-grace, and build a fleet **cert-expiry-horizon dashboard** + proactive renewal campaign (R3 cert-expiry-lockout prevention).
- **Owner:** [[SECURITY_ENGINEER_SKILL|SEC]] (lead), supporting [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]]. `ESC-SEC` applies; SEC owns the binding decision.
- **Detection control + trigger metric:** `days_to_cert_expiry` distribution across the fleet. **Alert when** any cohort has **> N devices within 30 days** of expiry and not yet rotated.
- **RPN:** S 8 → **8** (held); O 5 → **3** (proactive rotation + offline-grace prevents most lockouts); D 6 → **2** (expiry-horizon dashboard with proactive alert). **240 → 48.**
- **QA scenario:** fast-forward device clocks toward cert expiry in staging; assert the horizon dashboard alerts ≥ 30 days out and that rotation completes with offline-grace before mTLS fails.
- **Honest verdict:** **Closed.** Residual: a device continuously offline past expiry + grace still locks out (couples FC-007 clock) — but is now flagged pre-emptively.

### 3.11 FC-011 — Shallow liveness → "alive" device produces no inference — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §4.2 implements **true liveness** — the inference/telemetry task must "check in" to a software watchdog supervisor for the WDT to be serviced; the WDT kick is **gated on the supervised work**, not an independent timer ISR. The heartbeat carries `seconds_since_last_inference` ([[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] §6.2 twin heartbeat). Satisfies R2 (suppress/flag when not producing).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 3.
- **Detection control + trigger metric:** `seconds_since_last_inference` in heartbeat. **Alert when** > **3× the nominal inference interval** while the heartbeat continues (device "dark" but alive).
- **RPN:** S 7 → **7**; O 4 → **3** (task-gated WDT removes the masking anti-pattern → a deadlock now triggers reset); D 8 → **2** (last-inference timestamp = direct contracted detection). **224 → 42.**
- **QA scenario ([[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(c)]] — inference timeout):** stall the inference task while the timer ISR keeps running; assert the WDT fires (no longer masked) and that the backend alert on stale `seconds_since_last_inference` triggers.
- **Honest verdict:** **Closed** — anti-pattern fix + direct detection.

### 3.12 FC-016 — LoRaWAN frame-counter desync — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] persists/restores the frame counter **atomically across reset** (non-volatile, journaled); on desync, trigger an **OTAA rejoin**. [[SECURITY_ENGINEER_SKILL|SEC]] §4.3 governs session/replay protection; [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]]/[[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] surface **network-server frame-reject counts** into observability (the loss is otherwise invisible at the NS layer).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (counter persistence) + [[SECURITY_ENGINEER_SKILL|SEC]] (session/replay) + [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] (NS telemetry). `ESC-SEC` applies.
- **Detection control + trigger metric:** `ns_frame_reject_count` per device, exported from the network server. **Alert when** ≥ **5 consecutive rejects** (= desync), independent of ingest-health.
- **RPN:** S 7 → **7**; O 4 → **2** (atomic persistence + rejoin largely prevents desync; rollover handled by rejoin); D 8 → **3** (NS reject counts surfaced + alert). **224 → 42.**
- **QA scenario:** force a device reset that loses counter state (and simulate 32-bit rollover) in the LoRaWAN test harness; assert atomic restore or OTAA rejoin recovers the link and that NS reject counts surface an alert if desync occurs.
- **Honest verdict:** **Closed.** Dependency: requires the network server to expose reject metrics (integration item) — flagged for the FW↔BACK/SEC observability contract.

### 3.13 FC-004 — Anti-rollback counter wear, unverified — *detection-closed*

- **Mitigation:** [[SECURITY_ENGINEER_SKILL|SEC]] §4.1/§4.2 + [[FIRMWARE_ENGINEER_SKILL|FW]] §4.6 **read-back-verify every anti-rollback counter increment**, report the counter value in the heartbeat, and alert on write-verify failure or non-monotonic regression. Aligns with NIST SP 800-193 (firmware resilience/anti-rollback). `ESC-SEC` applies (HG-01).
- **Owner:** [[SECURITY_ENGINEER_SKILL|SEC]] (lead), supporting [[FIRMWARE_ENGINEER_SKILL|FW]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 7.
- **Detection control + trigger metric:** `antirollback_counter_value` in heartbeat + write-verify flag. **Alert when** any read-back-verify fails **or** the counter regresses (non-monotonic).
- **RPN:** S 9 → **9** (held: a defeated counter still enables fleet-wide rollback vulnerability); O 3 → **2** (read-back-verify converts silent write-failure into a caught event); D 8 → **2** (telemetered counter + verify). **216 → 36.**
- **QA scenario:** force a counter-write failure (or fuse-exhaustion emulation) on the HIL rig; assert the read-back-verify catches it, the device flags it, and a rolled-back image is **rejected** (fail-closed). Maps to the OTA validation path in [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]].
- **Honest verdict:** **Detection-closed, not prevention-closed.** Fuse/SE write-endurance is a *physical limit* — read-back-verify **detects** exhaustion but cannot prevent it; an exhausted-counter device must be retired/RMA'd. Now visible at write-time instead of silently defeated.

### 3.14 FC-008 — Stack→arena overlap → silent weight corruption — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §4.2 places an **MPU guard region** between the stack and the tensor arena → any overrun raises a **hard fault (fail-closed)** instead of silently corrupting weights; **worst-case stack-depth analysis in CI** (MISRA C:2012 / CERT C static analysis, [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARCH]] §8).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[EDGE_AI_ML_ENGINEER_SKILL|ML]] (arena placement), [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] (CI stack analysis).
- **Detection control + trigger metric:** MPU fault → WDT reset + `fault_event{mpu_guard}` telemetry; CI gate `worst_case_stack_margin`. **Alert/fail when** the MPU guard faults in field, or CI margin **< 25 %**.
- **RPN:** S 8 → **5** (converts silent wrong-inference into a clean fault + reset + recovery to known-good — degraded-with-recovery, not silent); O 3 → **2** (worst-case analysis sizes the stack; guard catches the residual); D 9 → **2** (hard fault = immediate fail-closed + static CI). **216 → 20.**
- **QA scenario:** drive the deep ISR-nesting path on the HIL/emulator (Renode/QEMU) to push stack into the guard region; assert a hard fault + recovery occurs (no silent corruption), and that the CI worst-case-stack job fails a build below 25 % margin.
- **Honest verdict:** **Closed** — one of the cleanest closures (D 9 → 2 via a hard fail-closed control).

### 3.15 FC-025 — Re-identification via engineered features — *closed*

- **Mitigation:** [[DATA_ENGINEER_SKILL|DATA]] §6.9 adds an **automated re-identification / k-anonymity test (k ≥ 5)** over **engineered feature sets** (not just raw fields) in the pipeline, plus a privacy-review gate on any new feature touching geo/time quasi-identifiers. [[SECURITY_ENGINEER_SKILL|SEC]] concurrence; quarterly Joint Review.
- **Owner:** [[DATA_ENGINEER_SKILL|DATA]] (lead), supporting [[SECURITY_ENGINEER_SKILL|SEC]], [[MLOPS_ENGINEER_SKILL|MLOps]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 8. PII/breach surface → `ESC-SEC`.
- **Detection control + trigger metric:** `k_anonymity_min` over quasi-identifier combinations in the engineered feature table. **Block (CRITICAL [[DQIR_SCHEMA|DQIR]]) when** k **< 5**.
- **RPN:** S 9 → **9** (held: a breach is a breach); O 3 → **2**; D 8 → **3** (automated, gating pipeline test). **216 → 54.**
- **QA scenario:** seed the feature pipeline with a known re-identifiable quasi-identifier combination (precise geo + timestamp); assert the k-anonymity test computes k < 5 and **blocks** promotion with a CRITICAL DQIR.
- **Honest verdict:** **Closed** against known quasi-identifier patterns. Residual (named honestly): privacy is **adversarial** — a *novel* quasi-identifier combination not in the test battery could still re-identify. Detection is strong but not provably exhaustive; the privacy-review gate on new features is the human backstop.

### 3.16 FC-033 — Rollback model↔firmware mismatch — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §6.4 **re-validates the rollback-target ↔ current-firmware compatibility manifest at rollback time** (not only at apply time); if incompatible, **fail to a known-safe SUPPRESS state** rather than activating an incompatible model. Grounds: ARCH OTA Model Artifact Contract compatibility manifest (model↔firmware range). Satisfies R1(b).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[EDGE_AI_ML_ENGINEER_SKILL|ML]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|ARCH]] — [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row 7.
- **Detection control + trigger metric:** `rollback_compat_check_result` telemetered. **Alert when** a device enters SUPPRESS-on-rollback (incompatible target detected).
- **RPN:** S 8 → **6** (fail-to-SUPPRESS converts silent-wrong-inference into a known no-inference state, recoverable via re-push); O 3 → **2**; D 9 → **2** (deterministic compatibility re-check at rollback). **216 → 24.**
- **QA scenario:** advance firmware past a model's compatibility range, then force a model sanity-check failure to trigger rollback; assert the device re-checks compatibility, refuses the incompatible model, and enters SUPPRESS (never runs the mismatched model). Extends the OTA rollback validation in [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]].
- **Honest verdict:** **Closed** — fail-closed SUPPRESS changes the effect from silent corruption to a visible, recoverable safe state.

### 3.17 FC-013 — Heap fragmentation in TLS stack — *closed*

- **Mitigation:** [[FIRMWARE_ENGINEER_SKILL|FW]] §9 replaces dynamic allocation in the TLS/connectivity path with a **static/pool allocator** (fixed-size session pool), adds **periodic supervised reconnect**, and [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] runs a **soak test at field-representative uptime** (§4 reliability).
- **Owner:** [[FIRMWARE_ENGINEER_SKILL|FW]] (lead), supporting [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] (soak).
- **Detection control + trigger metric:** `heap_largest_free_block_bytes` / `fragmentation_ratio` + `consecutive_reconnect_failures`. **Alert when** the fragmentation ratio trends up beyond threshold **or** reconnect failures ≥ **3**.
- **RPN:** S 6 → **6**; O 5 → **2** (pool allocator **structurally** prevents fragmentation-driven `malloc` failure); D 7 → **3** (heap-health + reconnect-fail metrics). **210 → 36.**
- **QA scenario ([[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4(d)]] extended — soak):** run a months-equivalent accelerated soak with repeated TLS re-handshakes; assert no allocation failure occurs with the pool allocator and that heap-health telemetry stays flat.
- **Honest verdict:** **Closed** — structural prevention is the strong control; detection is the backstop.

---

## 4. Honest Closure Assessment

Three honesty grades, applied per the §1.3 methodology:

- **Fully closed (10)** — structural/preventive control **plus** a contracted detective control; residual is minor or out-of-scope: **FC-005, FC-006, FC-008, FC-011, FC-013, FC-016, FC-017, FC-028, FC-031, FC-033.** These are the cleanest — most pair a fail-closed mechanism (MPU guard, atomic index, task-gated WDT, SUPPRESS-on-incompatible) with a named alert.
- **Detection-closed, not prevention-closed (4)** — the underlying **physical/physics failure still occurs**; the win is that it is now *visible and bounded* instead of silent. Stated plainly: **FC-001** (sub-threshold AFE drift below the 3 % alarm persists), **FC-004** (fuse/SE endurance is a hard physical limit — detected, not prevented), **FC-007** (RTC still drifts; we cross-check and correct), **FC-012/FC-014** (buffer overflow and downlink non-delivery still happen; now marked/retried). FC-014's downlink constraint is physics-bounded by LoRaWAN duty cycle and cannot be engineered away.
- **Strongly mitigated, residual named (2)** — **FC-022** (frozen-anchor detection is robust, but **anchor staleness** is a *new, smaller* slow-blind-spot the fix introduces — logged as candidate **FC-037**) and **FC-025** (k-anonymity gate is strong but privacy is adversarial; a novel quasi-identifier could evade the test battery).

**No chain is claimed fully eliminated.** Every "after" RPN above 50 (FC-001 84, FC-022 81, FC-007/FC-012/FC-014 72, FC-005/FC-025 54) is an *honest residual* in the Medium band, retained with monitoring per [[SYSTEM_FMEA_V1#2. RPN Thresholds and Risk Acceptance Criteria|FMEA V1 §2]] — not rounded to zero to make the gate look clean (CLAUDE.md §10.3).

---

## 5. R4 Detection Coverage — Recompute and Honest Baseline

### 5.1 A V1 accounting discrepancy, surfaced not hidden

While re-deriving coverage I found an internal inconsistency in [[SYSTEM_FMEA_V1|System FMEA V1]] that I am obligated to flag rather than silently adopt (CLAUDE.md §10.3, §10.7):

- V1 §6 R4 states **15** chains are D ≥ 8 → coverage **≈ 53 %** (17 of 32 Critical/High with contracted detection).
- But counting **D ≥ 8 directly from the §4 worksheet scores** (the RPN-consistent source of truth) yields **18** chains, not 15 — and V1 §5.2 prose lists **FC-005 as D = 8** while its §4.1 worksheet row scores it **D = 7** (RPN 252 = 6·6·**7**). The worksheet, which computes the published RPNs, is authoritative.
- Worksheet-derived baseline: **14 of 32** Critical/High chains have a contracted detection control (D ≤ 7) → **≈ 44 %**, not 53 %.

**Recommendation:** reconcile V1 §5.2 / §6 R4 to the worksheet (an honest *downward* correction from 53 % to ≈ 44 %). I do not overwrite V1 here (it is `final`); I record the discrepancy and track progress against **both** figures below so no reader is misled.

The 18 baseline D ≥ 8 chains (worksheet): **Critical (14)** FC-001, FC-004, FC-006, FC-007, FC-008, FC-011, FC-012, FC-014, FC-016, FC-022, FC-025, FC-028, FC-031, FC-033; **High (4)** FC-010, FC-024, FC-027, FC-029.

### 5.2 Post-V2 coverage

After the 17 Critical-chain mitigations land, **all 14 Critical D ≥ 8 chains move to D ≤ 3** (contracted detection with latency within the R3 window). The 3 already-covered Critical chains (FC-005 D7, FC-013 D7, FC-017 D6) improve further. The 15 High chains are unchanged (out of V2 scope).

| Milestone | Chains with contracted detection (D ≤ 7) | Coverage |
|---|--:|--:|
| V1 baseline (as stated in V1 §6) | 17 / 32 | ≈ 53 % |
| V1 baseline (honest worksheet recount) | 14 / 32 | ≈ 44 % |
| **After V2 (17 Critical mitigated)** | **28 / 32** | **≈ 87.5 %** |
| Target | ≥ 31 / 32 | **≥ 95 %** |

**Post-V2 ≈ 87.5 %** — a large, honest gain, but **still below the ≥ 95 % gate**. R4 is reported as **NOT YET MET** at the release gate until the remaining gap closes.

### 5.3 What remains to reach ≥ 95 % (the next burn-down)

Four **High** chains remain D ≥ 8 and are the defined next scope (a V2.x High-chain closure): **FC-010** (schema version not bumped — auto schema content-hash check), **FC-024** (backfill mutation — immutable-snapshot enforcement), **FC-027** (provisioning key non-uniqueness — fleet uniqueness audit), **FC-029** (lying device — remote attestation + cross-source reconciliation; security-keystone, couples FC-022). Closing **any 3 of these 4** reaches **31/32 ≈ 96.9 % ≥ 95 %**. Until then, [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] reports actual coverage at each release gate per [[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 R4]].

---

## 6. R5 Regression Mapping and Governance

### 6.1 R5 — every closed chain has an automated fault-injection test

Per [[QA_TEST_AUTOMATION_ENGINEER_SKILL#3.4 Execution|QA §3.4]] (robustness regression, NFR R5), each §3 QA scenario maps into the cross-layer robustness regression suite, traced to its FC-ID, executed per release; any failure blocks the release. The existing six §3.4 scenarios (a–f) cover most point-fault chains. **Two new test classes are required** (confirmed in [[SYSTEM_FMEA_V1#6. Populated NFR Targets|FMEA V1 §6 R5]]) and are introduced here:

1. **Multi-retraining-cycle degradation** (closes the verification gap for **FC-022**): the N-cycle closed-loop simulation in §3.1.
2. **Accelerated-aging / temperature-conditioned parity** (closes **FC-001, FC-006**): the slow-drift + across-temperature HIL parity tests in §3.2–§3.3.

| QA §3.4 scenario family | Chains verified |
|---|---|
| (a) Hardware brown-out | FC-005 |
| (b) Sensor corruption → **+ slow in-range drift (new class 2)** | FC-001, FC-006 |
| (c) Inference timeout / liveness | FC-011 |
| (d) MQTT connectivity loss / soak | FC-012, FC-013 |
| (e) Cloud degradation | (High: FC-019) |
| (f) Data backpressure / late-data | FC-007 |
| OTA end-to-end validation (incl. stall, rollback) | FC-014, FC-031, FC-033, FC-016, FC-004 |
| **Multi-retraining-cycle degradation (new class 1)** | FC-022 |
| Security production-gate / attestation | FC-028, FC-025 |
| MPU-guard / worst-case-stack CI | FC-008 |

### 6.2 Governance — how these designs become binding

- **ADR per mitigation theme.** Each [[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]] row is filed as an ADR by the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]], with [[SECURITY_ENGINEER_SKILL|Security]] concurrence on the security-relevant rows (FC-004, FC-016, FC-017, FC-025, FC-028 — all `ESC-SEC`, HG-01). Mitigations that introduce a *new contracted control* (F1 OTA watchdog, end-to-end input-freshness/liveness, frozen-anchor drift gate, per-batch production verification, immutable-snapshot enforcement, rollback-compat re-check) require the corresponding §6 contract change via CCR + version bump — none are applied silently (CLAUDE.md §7.6, §10.2).
- **Release-gate consequence.** Per [[QA_TEST_AUTOMATION_ENGINEER_SKILL#7. Decision Authority & Governance|QA §7]] and HG-04, any Critical chain **without a passing fault-injection regression test** remains a validation gap forcing **NO-GO**. This V2 supplies the *designs and test scenarios*; closure is asserted only when QA's scenario passes and the Architect signs HG-04. R4 ≈ 87.5 % is below the ≥ 95 % gate, so an **unconditional** production sign-off is not yet available — consistent with the project's CONDITIONAL GO posture and CLAUDE.md §10.1 (never ship around open Critical chains).
- **Wave/autonomy note.** These mitigations are human-authored design artifacts; agent participation stays advisory (non-binding) until the per-role Evaluation Harness baseline exists ([[EVALUATION_HARNESS_SPEC|Evaluation Harness Spec]]) and no BLOCKING CCR is open on the affected contracts.

---

## 7. Maintenance and Next Steps

1. **File 8 mitigation-theme ADRs** ([[SYSTEM_FMEA_V1#7.2 Cross-role ownership of mitigations|FMEA V1 §7.2]]), Architect-authored, SEC-concurred where flagged; track to closure before the production gate.
2. **Build the two new QA R5 test classes** (multi-retraining-cycle degradation; accelerated-aging/temperature parity) during §3.3; without them FC-001, FC-006, FC-022 cannot be marked verified.
3. **Reconcile V1 R4 accounting** (§5.1) — correct V1 §5.2/§6 from "15 D ≥ 8 / ≈ 53 %" to the worksheet-honest "18 D ≥ 8 / ≈ 44 %".
4. **Open the High-chain burn-down (V2.x)** for FC-010, FC-024, FC-027, FC-029 to lift R4 from ≈ 87.5 % to ≥ 95 %.
5. **Log new residual FC-037 (anchor staleness)** from the FC-022 fix, with a Research-governed anchor-refresh cadence, for inclusion at the next FMEA revision.
6. **Re-run coverage at each release gate** ([[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] owns R4/R5 reporting); update this document when a chain's QA scenario first passes (status `draft` → per-chain `verified`).

> **Owner:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] (robustness + ADRs) and [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] (fault-injection + R4/R5). **Validator:** [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]]. **Review cadence:** every ARB milestone, re-baselined with the System Robustness Contract. This is **v2.0-draft** — a closure *design*; it does not by itself close any chain or change any ratified contract, budget, security baseline, or OTA strategy (MACP invariant).
