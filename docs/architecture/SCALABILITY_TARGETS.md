---
title: "Scalability Targets — AgriSpectra Reference Fleet"
date: 2026-06-23
status: final
tags:
  - scalability
  - embedded-iot
  - nfr
  - architecture
  - fleet-scale
cssclass: architecture-doc
---

# Scalability Targets — AgriSpectra Reference Fleet

> **Consolidated, traceable reference.** This document closes the CLAUDE.md §8.4 gap (`quantitative scalability targets: fleet size, MQTT throughput, data ingestion rate/s, OTA concurrency, cloud API p99 latency`) by consolidating the **authoritative** Scalability and Performance NFRs (Non-Functional Requirements) from [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §5.1 (Sub-NFR IDs SCALE-1…SCALE-6, S1…S5, PERF-1…PERF-3) into a single reference, and grounds the correlated-event surge thresholds in the verified [[SYSTEM_FMEA_V1|System FMEA]] chains FC-019 and FC-035.
> **Authority:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §5.1 is the single source of truth; on any conflict the §5.1 Sub-NFR ID and Target govern, and this file is corrected to match. **Owner / sign-off:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] at the production release gate; co-signed by [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]], [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud]], and [[DATA_ENGINEER_SKILL|Data]] per §5.1 S1. **Version:** 1.0.0.

---

## 1. Fleet Scale Ceiling

Reference scale (AgriSpectra): **50,000** field devices, **7-year** field lifetime, seasonal deployment windows, LoRaWAN (Long Range Wide Area Network) uplink constraints (physics-bounded downlink). MQTT = Message Queuing Telemetry Transport; REST = Representational State Transfer; API = Application Programming Interface; DB = Database; msgs/s = messages per second; req/s = requests per second; P99 = 99th percentile; PUBACK = MQTT publish acknowledgment.

| Target | Value | Canonical NFR (§5.1) | Justification |
|---|---|---|---|
| Max concurrent active devices | **50,000** devices | SCALE-1 | AgriSpectra reference fleet ceiling; all REL, PERF, and R1–R5 targets must hold at this load without architectural redesign |
| MQTT persistent connections | **50,000** connections | SCALE-2 | One persistent connection per device; PUBACK latency P99 ≤ 100 ms under full load |
| MQTT aggregate throughput | **10,000 msgs/s** sustained | SCALE-3 | 60× headroom over the **167 msgs/s** nominal baseline (50,000 devices × 1 sample ÷ 300 s = 166.7 msgs/s); covers OTA-campaign bursts + debug-mode telemetry; error rate ≤ 0.01% |
| REST API request rate — sustained | **500 req/s** | SCALE-4 (sustained) | Routine fleet telemetry-pull + 1,000 dashboard users |
| REST API request rate — burst | **2,000 req/s** (10 s window) | SCALE-4 (burst) | OTA-campaign / event-driven burst headroom; error rate ≤ 0.1% |
| Time-series DB write throughput | **50,000 writes/s** aggregate | SCALE-5 | Fleet-wide reconnect-flush burst after network partition; P99 write latency ≤ 10 ms; zero data loss |

> **Working-label note:** the source task framed these rows as `SCALE-1…SCALE-6`. To prevent collision with the differently-numbered §5.1 SCALE series (where §5.1 SCALE-5 = DB writes and §5.1 SCALE-6 = OTA download sessions), this document keys every row to the **canonical §5.1 Sub-NFR ID** above. The task working-labels map as: SCALE-1→SCALE-1, SCALE-2→SCALE-2, SCALE-3→SCALE-3, SCALE-4→SCALE-4 (sustained), SCALE-5→SCALE-4 (burst), SCALE-6→SCALE-5.

## 2. OTA Concurrency, API & Ingestion Latency (remaining §8.4 gap items)

P99 / P95 = 99th / 95th percentile; OTA = Over-the-Air; SLO = Service Level Objective.

| Target | Value | Canonical NFR (§5.1) |
|---|---|---|
| Concurrent OTA firmware download sessions | **5,000** sessions (= 10% of 50,000-device fleet) | SCALE-6 |
| Cloud REST API response latency | **≤ 200 ms P99** (API Gateway ingress → response egress) | PERF-3 / S4(2) |
| Standard telemetry end-to-end latency | **≤ 3,000 ms P99** (device publish → dashboard display) | PERF-1 / S4(3) |
| Alert/alarm telemetry latency | **≤ 500 ms P99** (device alert publish → dashboard notification) | PERF-2 |
| Data ingestion commit latency | **≤ 10 ms P95** (message received → written to time-series DB) | S4(4) |
| MQTT delivery latency (publish → PUBACK) | **≤ 100 ms P95** | S4(1) |

## 3. Correlated-Event Surge Thresholds

These thresholds size the architecture for **correlated** fleet events — the failure mode a per-device average hides. Both referenced chains are **High-severity, open** in the [[SYSTEM_FMEA_V1|System FMEA]] and require mitigation before the production release gate. FC = Failure Chain; RPN = Risk Priority Number.

| Scenario | Threshold | FMEA Reference | Required control (per FMEA "Recommended") |
|---|---|---|---|
| Telemetry storm (regional outbreak) | **≥ 10× nominal rate sustained for > 5 min** | [[SYSTEM_FMEA_V1\|FC-019]] (RPN 140, High) | Fleet-scale surge test (≥ 10× nominal) + **priority lane for anomaly-positive messages** so alerts are not delayed past the actionable window under the very load that matters most |
| Post-outage thundering herd | **≥ 50,000 devices reconnecting within 30 min** | [[SYSTEM_FMEA_V1\|FC-035]] (RPN 120, High) | Admission control / broker rate-limit + surge headroom so recovery does not starve legitimate telemetry ingest |
| Jittered reconnect/poll backoff | **Mandatory exponential backoff (1–120 s) with random jitter** | [[SYSTEM_FMEA_V1\|FC-035]] (RPN 120, High) | De-synchronize fleet reconnection/desired-state polling so 50,000 devices do not poll simultaneously when an outage clears |

> **Honesty note (CLAUDE.md §10.3):** FC-019 and FC-035 are at residual status **"High → mitigate"** — the surge controls above do **not** exist as contracted detection/mitigation today; they are design requirements to be built during §3.3 Development and validated by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]]. These targets state what the architecture must withstand, not what is currently proven.

## 4. Scalability Verification

Each target is verified by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] and signed off by the Architect at the production release gate, using the §5.1 measurement methods (device simulators, `emqtt-bench`, `k6`, sustained soak). The Gate column reproduces the source task; the mapping column gives the authoritative reference.

| Test | Method | Gate | Authoritative NFR / FMEA mapping |
|---|---|---|---|
| Fleet-scale load test | Simulate 50,000 devices at 2× nominal telemetry rate | SCALE-1 | SCALE-1 + S1 (load simulation at 2× the 12-month target; all SCALE-series targets must hold; ≤ 70% per-layer utilization) |
| Burst load test | 10× telemetry surge for 15 min | SCALE-2 | **SCALE-3** throughput under surge + **FC-019** fault-injection scenario (≥ 10× nominal); priority-lane assertion |
| Reconnect storm test | 50,000 devices reconnect within 30 min | SCALE-5 | **FC-035** thundering-herd scenario + **SCALE-2** (connection re-establishment) + **SCALE-5** (reconnect-flush DB write burst); jittered-backoff assertion |

> **Mapping note:** the surge and reconnect tests are the FC-019 and FC-035 fault-injection / robustness-regression scenarios respectively; the canonical NFR mapping is provided so the gate traces to the §5.1 Sub-NFR IDs and the FMEA chain IDs rather than to local labels.

## 5. Horizontal Scaling & Capacity Triggers (§5.1 S1–S5 summary)

HPA = Horizontal Pod Autoscaler. Per §5.1 S1–S5, the architecture must scale **horizontally** with these capacity-management rules across all four service layers (MQTT broker, Backend API, Data ingestion, OTA distribution):

- **Growth headroom (S1):** every per-service scaling limit is sized to the 3-year fleet ceiling **× 1.3** (≥ 30% headroom); per-service utilization at the 12-month device count must not exceed **70%** of any per-layer limit.
- **Autoscaling trigger (S5):** HPA activates at **70% of a per-layer limit sustained ≥ 15 min**.
- **Alert threshold (S5):** oncall alerted at **80% of a per-layer limit**, within ≤ 5 min of breach.
- **Provisioning SLA (S5):** new capacity available within **≤ 10 min** of HPA trigger, for all four layers.
- **Sustained-load SLO (S4):** all five SLOs (§2) hold concurrently for **≥ 24 continuous hours** at the 12-month fleet target, including during autoscaling events.
- **Per-device budgets (S3):** telemetry payload ≤ **256 bytes** (CBOR — Concise Binary Object Representation — encoded), OTA firmware image ≤ **2 MB**, OTA model package ≤ **512 KB**, MQTT keepalive ≥ **30 s**; any breach without a closed ADR blocks Development exit and production release.

## 6. Authority, Traceability & Governance Notes

- **Source of truth:** all numeric targets are transcribed from [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §5.1 (status `final`, zero `[TBD]` values). This document adds no new numbers; it consolidates and cross-references them and binds the surge thresholds to the FMEA chains.
- **Change control:** changes to fleet-scale targets > 2× require a major SemVer bump and an ADR ([[ADR_INDEX|ADR Index]]); per §5.1 S1 such changes are co-signed by DevOps, Backend, and Data at ARB sign-off ([[ARB_CHARTER_INSTANTIATED|ARB Charter]]).
- **Validation against reference scale:** any agent-generated architecture/infrastructure design must be validated against these targets before delivery (CLAUDE.md §8.4).
- **Drift monitoring:** the Architect reviews fleet-growth telemetry quarterly against this envelope ([[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §3.6); trending to exceed within 12 months triggers a capacity architecture review.

#scalability #nfr #fleet-scale #architecture
