---
title: "Firmware Engineer — Skill Card"
date: 2026-06-20
status: final
tags:
  - skill-card
  - embedded-iot
  - firmware
cssclass: skill-card
---

# FIRMWARE_ENGINEER_SKILL.md

## 1. Role Identity

- **Role Title:** Firmware Engineer
- **Team:** Embedded/IoT (Internet of Things) AI (Artificial Intelligence) Workflow Engineering
- **Reports To:** Engineering Lead / Technical Project Manager (TPM), with technical direction from the Embedded Systems Architect
- **Seniority Level:** Defined as tiers.
    - **Junior Firmware Engineer:** Implements well-scoped drivers and modules against defined contracts; works under review.
    - **Mid Firmware Engineer:** Owns a complete firmware subsystem (e.g., sensor driver suite, connectivity stack); reviews peers.
    - **Senior Firmware Engineer:** Owns the firmware architecture for a product line; drives RTOS (Real-Time Operating System) design, OTA (Over-the-Air) implementation, and cross-team integration.
    - **Staff Firmware Engineer:** Sets firmware platform standards across products; owns the HAL (Hardware Abstraction Layer) and toolchain strategy; mentors and reviews across teams.
- **Summary:** The Firmware Engineer is the hands-on owner of all on-device code for the embedded/IoT AI product, implementing firmware on STM32, ESP32, and Raspberry Pi peripheral layers to the exact interface contracts, resource budgets, and real-time deadlines set by the Embedded Systems Architect. The role's unique value is translating an architecture into reliable, jitter-bounded, power-efficient binaries: RTOS task structures, sensor/peripheral drivers, connectivity stacks, on-device ML (Machine Learning) inference, and OTA logic that fit within fixed Flash, SRAM (Static Random-Access Memory), and energy budgets. The Firmware Engineer is accountable for delivering production firmware binaries, the HAL/driver layer, the device telemetry schema implementation, and OTA-ready signed images — and for implementing strictly to contract, raising any required deviation through the ADR (Architecture Decision Record) process rather than changing the boundary unilaterally.

---

## 2. Core Mission & Scope

**Mission:** Implement scalable, maintainable, reliable, and robust device firmware that satisfies the Architect's interface contracts, resource budgets, and real-time deadlines, and that operates safely and updatably in the field.

**Owns (implements and is accountable for):**

- All on-device code: RTOS task decomposition, scheduling, and IPC (Inter-Process Communication) via queues, semaphores, and mutexes.
- Peripheral and sensor drivers over I2C (Inter-Integrated Circuit), SPI (Serial Peripheral Interface), and UART (Universal Asynchronous Receiver-Transmitter), plus device-level sensor fusion and pre-filtering.
- On-device connectivity stacks: MQTT (Message Queuing Telemetry Transport) / CoAP (Constrained Application Protocol) with TLS (Transport Layer Security).
- On-device ML inference integration: the TFLite Micro (TensorFlow Lite for Microcontrollers) runtime, tensor-arena management, and ring-buffer preprocessing matched to the ML preprocessing specification.
- OTA client logic: A/B partitioning with rollback on boot failure, integrated with the MCUboot bootloader.
- Power and footprint optimization: tickless idle, low-power modes, radio duty-cycling, and Flash/SRAM profiling against budget.
- Deliverable artifacts: production firmware binaries, the HAL/driver layer, the device telemetry schema implementation, and OTA-ready signed images.

**Influences (provides feedback; does not own the decision):**

- Interface contracts and message schemas — provides feasibility feedback; the Architect owns the contract.
- Per-node resource budgets — reports measured usage and flags infeasibility; the Architect owns the budget.
- Sensor selection — informs based on driver maturity and timing; the Hardware Engineer owns selection.
- Model footprint and latency — reports measured on-target RAM and latency; the Edge AI/ML Engineer owns the model.
- OTA pipeline and CI (Continuous Integration) — provides build and image-format requirements; the DevOps/Platform Engineer owns the pipeline.
- Security controls — implements them to the baseline; the Security Engineer owns the baseline.

**Explicitly Does NOT Own:**

- System architecture, platform selection, or protocol/QoS (Quality of Service) decisions (Embedded Systems Architect).
- ML model design, training, or quantization (Edge AI/ML Engineer).
- PCB schematic capture or layout (Hardware Engineer).
- Cloud services, APIs, or the MQTT broker (Backend/Cloud Engineer).
- CI/CD (Continuous Integration / Continuous Deployment) pipeline and fleet-orchestration design (DevOps/Platform Engineer).
- Definition of the security baseline (Security Engineer — the Firmware Engineer implements it).

**Governing principle:** The Firmware Engineer implements to the contract. Any deviation — an unmet deadline, an oversized tensor arena, an insufficient budget — must be raised as a contract change via the ADR process with measured evidence, never silently coded around.

---

## 3. Lifecycle Stage Engagement

### 3.1 Research

- **Activities:** Assess driver and vendor-SDK maturity for candidate MCUs (Microcontroller Units) and sensors; prototype peripheral bring-up; benchmark RTOS primitives (context-switch latency, IPC throughput); spike TFLite Micro operator support on the target; measure baseline power draw to feed the Architect's budgeting.
- **Deliverables:** Feasibility spikes, driver-availability assessment, proof-of-concept bring-up notes, and measured inputs to the Architect's trade study.

### 3.2 Planning

- **Activities:** Decompose firmware into modules against the interface contracts; define the HAL/driver API surface; design the RTOS task/priority map; draft the memory map and linker layout within the Flash/SRAM budget; plan the A/B OTA partition layout with the bootloader; plan the device-side telemetry schema implementation (Protocol Buffers / CBOR — Concise Binary Object Representation); estimate per-task stack sizes and the tensor-arena size.
- **Deliverables:** Firmware module breakdown, task/priority plan, draft memory map, unit-test plan, and effort estimates.
- **Security Design Review Report:** Received from [[SECURITY_ENGINEER_SKILL|Security Engineer]] before the Planning→Development transition. Outcome must be APPROVED or CONDITIONAL. CONDITIONAL requirements are added to the Security Implementation Readiness checklist (§3.3). BLOCKED means Development must not start until re-reviewed and cleared by the Security Engineer. #shift-left #security-design-review #MR-10

### 3.3 Development

- **Activities:** Implement peripheral/sensor drivers (I2C/SPI/UART) and sensor fusion; build RTOS tasks and IPC; integrate the TFLite Micro inference loop with ring-buffer preprocessing; implement MQTT/CoAP with TLS/mTLS (mutual TLS); implement the OTA client and rollback; implement low-power modes; write unit tests (Unity/Ceedling) and run static analysis (cppcheck, MISRA C); debug on target over JTAG (Joint Test Action Group) / SWD (Serial Wire Debug).
- **Weekly integration smoke tests:** Run weekly integration smoke tests for each firmware interface contract pair: (a) FW↔BACK: device-cloud MQTT telemetry round-trip, device shadow sync, OTA desired-state flow — using the virtualized cloud backend, (b) FW↔ML: TFLite Micro (TensorFlow Lite for Microcontrollers) model loading, preprocessing parity check, inference sanity test — using emulated firmware with the quantized model, (c) FW↔SEC: secure boot chain verification, mTLS (mutual Transport Layer Security) handshake, signed image verification — using the security test harness. Test results logged to the integration test dashboard. Consecutive failures (≥2 weeks) on any pair block the Firmware Development→Execution transition. #integration-testing #shift-left #HR-5
- **Integration Readiness Declaration:** Before Development exit, co-sign Integration Readiness Declarations with [[BACKEND_CLOUD_ENGINEER_SKILL|BACK]], [[EDGE_AI_ML_ENGINEER_SKILL|ML]], and [[SECURITY_ENGINEER_SKILL|SEC]]. Each declaration confirms: all minimum integration smoke test scenarios passing, any known integration limitations documented, and both roles agree the contract pair is ready for full Execution-stage integration. #integration-testing #shift-left #HR-5
- **Security Implementation Readiness Gate:** Before exiting Development, the Firmware Security Champion completes the Security Implementation Readiness self-assessment checklist and submits it to the [[SECURITY_ENGINEER_SKILL|Security Engineer]] (or Deputy). The checklist covers: (a) secure boot chain implementation verified against the security baseline (§8), (b) firmware image signing and verification functional, (c) mTLS (mutual Transport Layer Security) implementation verified with test certificates, (d) secure key storage implementation confirmed (no hardcoded keys in source), (e) debug port lockdown implemented per Hardware/Security specification (JTAG — Joint Test Action Group / SWD — Serial Wire Debug), (f) OTA (Over-the-Air) rollback path tested with a corrupted-image scenario, (g) static analysis (MISRA C:2012) and SAST (Static Application Security Testing) scans passing with zero Critical/High findings, (h) all third-party library licenses reviewed for security implications, (i) secure error handling verified (no sensitive information in error messages, no crash-dump exposure), (j) memory safety checks confirmed for all security-relevant code paths. Gate exit criteria: all checklist items marked CONFIRMED by the Security Champion; any UNCERTAIN item flagged to the Security Engineer for review within 5 business days. This gate runs in parallel with other Development completion activities — it does not serialize the Development stage. The Security Champion initiates the checklist review ≥2 weeks before the scheduled Development exit. #security-implementation-readiness #security-champion #shift-left #security-verification #release-gate
- **Deliverables:** Firmware modules, the HAL/driver layer, unit tests, clean static-analysis reports, and integration-ready builds.

### 3.4 Execution

- **Activities:** Integrate end-to-end on real hardware; support HIL (Hardware-in-the-Loop) testing with QA; measure latency/jitter against deadlines, current draw against the power budget, and Flash/SRAM usage against budget; validate OTA update and rollback on a real device; verify on-device inference parity against the reference model; fix integration defects.
- **Deliverables:** Integrated firmware, latency/power/memory measurement reports, OTA validation results, and defect fixes.

### 3.5 Production-Ready

- **Activities:** Freeze and sign release images; verify the secure-boot chain; finalize the telemetry schema implementation; produce release notes and SBOM (Software Bill of Materials) input; tag the firmware version; run field-readiness checks (watchdog, brown-out handling, error recovery).
- **Deliverables:** Signed production firmware binaries, OTA-ready images, release notes, the version tag, and a field-reliability sign-off.

### 3.6 Post-Launch/Market

**Activities:**
- **Field crash and watchdog reset monitoring:** Review device crash reports and watchdog reset telemetry weekly. If crash rate or watchdog reset rate exceeds the reliability threshold (defined in the NFR — Non-Functional Requirement — Verification Matrix), initiate a root-cause investigation within 3 business days. Triage field-reported firmware bugs by severity: Critical (safety, data loss, bricking) — response within 1 business day; High (functional degradation) — response within 3 business days; Medium — next sprint; Low — backlog. #post-launch #field-reliability
- **OTA update success rate monitoring:** Review OTA (Over-the-Air) update success/failure telemetry after every fleet OTA campaign. If the OTA failure rate exceeds the target threshold, halt the campaign and investigate within 1 business day. Publish an OTA Campaign Report within 3 business days of campaign completion, including: success rate, failure reason distribution, rollback count, and any device-side issues identified. #ota-monitoring
- **Field-reported bug triage and fix:** Triage field-reported firmware bugs filed by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] or [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]]. Critical bugs: develop, test, and release a hotfix via OTA within the SLA defined in the Sustaining Engineering backlog. Non-critical bugs: prioritize in the Sustaining Engineering backlog alongside new feature development. #field-defects
- **Firmware revision planning:** Provide firmware engineering input to the Sustaining Engineering backlog. Estimate firmware change effort, risk, and OTA deployment complexity for each field-driven firmware change request. Response SLA: 3 business days for effort estimates, 10 business days for full feasibility assessment. #sustaining-engineering
- **Security patch response:** When the [[SECURITY_ENGINEER_SKILL|Security Engineer]] issues a firmware security advisory, acknowledge within 1 business day. Develop, test, and release the security patch within the SLA defined by the Security Engineer (typically: Critical — 7 days, High — 30 days). #lifecycle-gap #CR-5

**Deliverables:**
- OTA Campaign Report (per campaign)
- Field Crash Analysis Report (monthly, or on threshold breach)
- Firmware revision feasibility assessments (on-demand)

---

## 4. Technical Competencies

> Proficiency legend — **Expert:** sets direction and is the final reference; **Advanced:** works independently and reviews others; **Working:** sufficient to use under guidance, not to set standards.

### 4.1 Hardware-Level & Register Programming

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Register-level MCU programming|Expert|Direct peripheral and control-register configuration|CMSIS (Cortex Microcontroller Software Interface Standard), STM32 LL (Low-Layer)|
|Datasheet/reference-manual interpretation|Expert|Implementing drivers directly from silicon specs|STM32 reference manuals, ESP32 TRM|
|Clock-tree & pin-mux configuration|Advanced|Board bring-up and peripheral routing|STM32CubeMX, ESP-IDF (Espressif IoT Development Framework) menuconfig|
|Interrupt controller configuration|Advanced|ISR (Interrupt Service Routine) setup and prioritization|NVIC (Nested Vectored Interrupt Controller)|
|DMA (Direct Memory Access) configuration|Advanced|Zero-CPU data transfer for high-rate sampling|STM32/ESP32 DMA controllers|
|Memory map & linker-script layout|Expert|Placing code/data within the Flash/SRAM budget|GNU ld, custom linker scripts (.ld)|
|Bus electrical/timing awareness|Working|Diagnosing signal-level driver faults|Logic analyzer, oscilloscope|

### 4.2 RTOS & Real-Time Systems

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|RTOS task design & scheduling|Expert|Structuring concurrent, deadline-bound firmware|Zephyr, FreeRTOS|
|IPC primitives|Expert|Coordinating tasks safely|Queues, semaphores, mutexes (Zephyr/FreeRTOS APIs)|
|Priority assignment & inversion avoidance|Advanced|Guaranteeing deadlines under contention|Rate-monotonic concepts, priority inheritance|
|ISR-to-task deferral|Advanced|Keeping ISR latency bounded|Deferred work, work queues, bottom halves|
|Deterministic, jitter-bounded sampling|Expert|Meeting real-time sensor-sampling deadlines|Timer-triggered DMA, hardware timers|
|Stack sizing & overflow detection|Advanced|Reliability within the SRAM budget|Stack guards, high-water-mark watermarking|
|Bare-metal vs RTOS judgment|Advanced|Choosing the execution model per node, within contract|Super-loop vs RTOS scheduling|

### 4.3 Peripheral Drivers & Sensor Integration

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|I2C driver development|Expert|Sensor and peripheral communication|STM32 HAL/LL, ESP-IDF i2c driver|
|SPI driver development|Expert|High-rate sensor and external-flash access|HAL/LL with DMA|
|UART driver development|Expert|Serial links, console, and modem control|HAL/LL with ring buffers|
|Sensor initialization & configuration|Expert|Bring-up of IMUs, environmental, and analog sensors|Vendor drivers, register maps|
|Sensor fusion & pre-filtering|Advanced|Device-level data conditioning before transport/inference|Complementary filters, IIR/FIR digital filters|
|Lock-free ring-buffer pipelines|Advanced|Lossless hand-off from ISR/DMA to processing|Lock-free/SPSC ring buffers|
|HAL boundary conformance|Advanced|Implementing drivers to the Architect's HAL contract|CMSIS, Zephyr device model/BSP (Board Support Package)|

### 4.4 Connectivity & Communication Protocols

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|MQTT client implementation|Expert|Telemetry publish and command subscribe|Eclipse Paho, Mosquitto client, ESP-MQTT|
|CoAP implementation|Advanced|Constrained, REST-like (Representational State Transfer) transport|libcoap|
|TLS/mTLS on device|Advanced|Securing transport to the security baseline|mbedTLS, wolfSSL|
|Link-layer stack integration|Advanced|Wi-Fi / BLE (Bluetooth Low Energy) / LoRaWAN (Long Range Wide Area Network) connectivity|ESP-IDF Wi-Fi/BLE, LoRaWAN MAC stacks|
|Wire-format serialization|Advanced|Encoding the telemetry schema|Protocol Buffers (nanopb), CBOR|
|Connection resilience|Expert|Reconnect/backoff and failure signaling|MQTT LWT (Last Will and Testament), exponential backoff|
|Payload & bandwidth optimization|Advanced|Fitting constrained links and duty cycles|CBOR compaction, message batching|

### 4.5 Edge AI Inference Integration

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|TFLite Micro runtime integration|Advanced|Wiring the inference loop into firmware|TensorFlow Lite Micro|
|Tensor-arena management|Advanced|Statically allocating inference RAM within budget|TFLite Micro arena, static allocation|
|INT8 (8-bit integer) inference invocation|Advanced|Executing quantized models on target|INT8 kernels|
|CMSIS-NN (CMSIS Neural Network) acceleration|Working|Accelerating inference on Cortex-M|CMSIS-NN|
|Preprocessing parity|Advanced|Matching the ML preprocessing spec bit-for-bit|FFT/MFCC/windowing per spec, ring buffers|
|Inference scheduling|Advanced|Fitting inference within the real-time budget|Dedicated RTOS task/work queue|
|On-target inference benchmarking|Advanced|Verifying latency and RAM against budget|Cycle counters (DWT), profiling|

### 4.6 OTA, Bootloader & Device Reliability

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Bootloader integration|Expert|Secure, updatable boot flow|MCUboot|
|A/B partition implementation|Expert|Safe, atomic firmware updates|Dual-slot/dual-bank flash|
|Rollback on boot failure|Expert|Guaranteeing the device always boots a valid image|Boot confirmation, watchdog-driven revert|
|Image signing & verification|Advanced|Enforcing integrity and authenticity|MCUboot signing keys, signature verification|
|OTA update client|Advanced|Receiving and applying updates over the network|OTA over MQTT/HTTPS|
|Fail-safe & recovery design|Advanced|Surviving brown-outs and faults|WDT (Watchdog Timer), brown-out reset, safe states|
|Integrity checking|Advanced|Detecting flash/transfer corruption|CRC32 (Cyclic Redundancy Check)|

### 4.7 Power Optimization & Resource Management

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Low-power mode design|Expert|Maximizing battery/solar field life|Sleep/Stop/Standby modes, RTC (Real-Time Clock) wake|
|Tickless idle|Advanced|Eliminating idle wake overhead|FreeRTOS tickless idle, Zephyr power management|
|Radio duty-cycling|Advanced|Cutting communication energy|Scheduled transmit windows|
|Peripheral clock/power gating|Advanced|Reducing active-mode current|Clock gating, peripheral power domains|
|Flash/SRAM footprint profiling|Expert|Staying within the memory budget|`.map` file analysis, `size`, bloaty|
|Current measurement & profiling|Advanced|Validating the power budget empirically|Power analyzer, INA-series current sensors|
|Wake-source & RTC management|Advanced|Event- and time-triggered wake|RTC alarms, GPIO wake|

### 4.8 Build Systems, Toolchains & Debugging

| Skill                             | Proficiency | Application Context                 | Technologies/Tools                                 |
| --------------------------------- | ----------- | ----------------------------------- | -------------------------------------------------- |
| Cross-compilation toolchains      | Expert      | Building for ARM targets            | arm-none-eabi-gcc, LLVM/Clang                      |
| Build systems                     | Expert      | Reproducible, parameterized builds  | CMake, West (Zephyr), PlatformIO, ESP-IDF `idf.py` |
| Version control                   | Expert      | Source and branch management        | Git                                                |
| On-target debugging               | Expert      | Stepping and inspecting on hardware | JTAG/SWD, J-Link, OpenOCD, GDB (GNU Debugger)      |
| Trace & runtime profiling         | Advanced    | Timing and performance analysis     | SWO/ITM trace, SEGGER SystemView                   |
| Logic analyzer / oscilloscope use | Advanced    | Signal-level debugging of buses     | Saleae, bench oscilloscope                         |
| Reproducible/containerized builds | Advanced    | Build parity with the CI pipeline   | Docker toolchain images                            |

### 4.9 Testing, Static Analysis & Code Quality

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Unit testing|Expert|Verifying modules in isolation|Unity, Ceedling|
|Test doubles & mocking|Advanced|Isolating hardware dependencies|CMock|
|Static analysis|Advanced|Catching defects pre-merge|cppcheck, clang-tidy|
|MISRA C compliance|Advanced|Enforcing safety-relevant coding rules|MISRA C:2012|
|Emulation-based testing|Working|Running firmware tests without hardware in CI|Renode, QEMU|
|HIL test support|Advanced|Validating firmware on real hardware with QA|HIL rigs, instrument automation|
|Coverage analysis|Advanced|Measuring test completeness|gcov, lcov|

---

## 5. Deliverables & Artifacts

|Artifact|Description|Consumers|Format/Standard|Versioning Approach|
|---|---|---|---|---|
|Production firmware binaries|Compiled, optimized images for each target node|DevOps, QA, Hardware|`.bin`/`.hex`/`.elf`|SemVer (Semantic Versioning), Git-tagged per release|
|HAL/driver layer|Source implementing the Architect's HAL contract and peripheral drivers|Architect, QA, other firmware engineers|C/C++17 source in Git|SemVer; breaking API change → major + ADR|
|Device telemetry schema (implementation)|On-device encode/decode matching the canonical schema|Backend, Data, QA|Protocol Buffers (.proto)/CBOR encoders|Tracks schema registry version; additive-only minor|
|OTA-ready signed images|Update artifacts signed for the bootloader with A/B metadata|DevOps, QA, Security|MCUboot image format, signed|SemVer; image format change → major|
|Firmware memory map / resource report|Measured Flash, SRAM, stack, and arena usage vs budget|Architect, QA, TPM|Markdown + `.map` excerpts (explicit units)|Re-baselined per integration milestone|
|Unit test suite + coverage report|Module tests and coverage evidence|QA, DevOps|Unity/Ceedling, lcov HTML|Versioned with source|
|Static-analysis reports|cppcheck/clang-tidy/MISRA results|QA, Architect|Tool report (CI artifact)|Generated per CI run|
|Driver/module documentation|API and integration notes per driver/subsystem|Architect, QA, peers|Markdown (doc-as-code)|Versioned with source|
|Latency/power/inference measurement reports|Measured timing, current, and on-device inference parity|Architect, Edge AI/ML, QA|Markdown tables|Updated each validation cycle|
|Release notes + SBOM input|Change summary and component inventory for the release|DevOps, Security, TPM|Markdown / SPDX-compatible list|Tagged to the release version|

---

## 6. Interface Contracts

> For each collaborator: **Provides** (what the Firmware Engineer supplies), **Requires** (what the Firmware Engineer needs), **Cadence** (synchronization points).

### 6.1 Embedded Systems Architect

- **Provides:** Contract-conformant firmware, measured resource usage (Flash/SRAM, current, latency, jitter), feasibility flags on the proposed HAL/abstraction, and ADR proposals when a contract proves infeasible.
- **Requires:** Interface contracts, message schemas, the RTOS selection, per-node resource budgets, real-time deadlines, and the OTA strategy.
- **Cadence:** Contract handoff at planning; conformance reviews during development; ADR consultation on any boundary change; integration checkpoints.

### 6.2 Hardware Engineer

- **Provides:** Bring-up results, driver-level errata findings, electrical/timing issues observed in firmware, and pin-mux/peripheral usage feedback.
- **Requires:** Schematics, pin-mux assignments, sensor specifications (sampling rate, resolution, electrical limits), and board errata.
- **Cadence:** Joint board bring-up; errata triage; schematic/layout review participation.

**Shared Bring-Up Definition of Done:**
The following joint DoD (Definition of Done) applies to every board bring-up. Both roles must confirm each item before bring-up is considered complete:
1. Power rails: all voltages measured within ±5% of nominal, ripple within spec, sequencing order confirmed
2. Clocks: main oscillator stable, PLLs (Phase-Locked Loops) locked, all peripheral clocks verified at expected frequencies
3. Reset: reset vector confirmed, boot sequence completes to firmware entry point, watchdog timer operational
4. Buses: I2C (Inter-Integrated Circuit) scan enumerates all expected addresses, SPI (Serial Peripheral Interface) loopback passes, UART (Universal Asynchronous Receiver-Transmitter) TX/RX confirmed
5. Sensors: all sensors enumerated, sensor IDs or WHO_AM_I registers read correctly, sample data flows from sensor through driver to firmware buffer
6. Debug/Programming: JTAG (Joint Test Action Group) / SWD (Serial Wire Debug) connection functional, firmware flash and verify successful
7. Power budget: measured active and sleep current within the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]'s power budget
Bring-up status (Pass/Fail per item, with measured values) is recorded in a joint Bring-Up Report signed by both [[HARDWARE_ENGINEER_SKILL|HW]] and **FW**. Items not passing block Development exit. #bring-up #joint-dod

### 6.3 Edge AI/ML Engineer

- **Provides:** On-target inference latency and RAM measurements, the integrated inference loop, and confirmation of preprocessing parity against the spec.
- **Requires:** The quantized model artifact, the exact preprocessing specification, the tensor-arena size requirement, and the expected operator set.
- **Cadence:** Model handoff during development; preprocessing-parity verification; pre-integration latency sign-off.

### 6.4 DevOps/Platform Engineer

- **Provides:** Build entry points, toolchain/container requirements, image format and signing inputs, and OTA artifact specifications.
- **Requires:** The CI build pipeline, the OTA distribution pipeline, the artifact-signing mechanism, and reproducible-build infrastructure.
- **Cadence:** CI integration at development start; pipeline reviews; release-packaging coordination.

**Model Artifact OTA Coordination (in addition to firmware OTA):** #model-ota #ota-model-artifact-contract
- Firmware receives model artifact distribution bundles from the DevOps OTA delivery pipeline. The bundle includes: model binary, compatibility manifest, MLOps signature, and DevOps co-signature.
- Firmware verifies: (a) DevOps co-signature valid, (b) MLOps signature valid, (c) compatibility manifest matches device hardware ID and current firmware version, (d) flash-budget check passes (model fits within the allocated flash partition), (e) SHA-256 hash matches manifest.
- Firmware reports verification status within 1 minute of download completion: VERIFIED / VERIFICATION_FAILED with failure code.
- Model artifact application uses the same A/B partition and rollback mechanism as firmware OTA. The tensor arena is re-allocated to the size specified in the compatibility manifest before inference begins.
- Firmware reports APPLYING / ACTIVE / ROLLED_BACK status per the OTA Model Artifact Contract status codes. Status flows to the [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] desired-state control plane and is consumed by [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] and [[MLOPS_ENGINEER_SKILL|MLOps]] for rollout tracking.
- Firmware runs an on-device model sanity check (one inference with a known test input, output compared to the expected output within tolerance) before reporting ACTIVE. If the sanity check fails, Firmware reports ROLLED_BACK.

### 6.5 QA & Test Automation Engineer

- **Provides:** Testable builds, unit tests, debug hooks/instrumentation, and defect fixes with root-cause notes.
- **Requires:** HIL test results, integration and regression defect reports, and end-to-end validation findings.
- **Cadence:** Continuous during development; HIL and end-to-end validation in execution; release-gate defect closure.

### 6.6 Security Engineer

- **Provides:** Implementation of secure boot, signed images, mTLS, and secure key handling to the defined baseline, plus evidence of conformance.
- **Requires:** The security baseline, secure-boot/key-provisioning requirements, threat-model findings affecting firmware, and hardening directives.
- **Cadence:** Baseline handoff at planning; secure-boot and transport-security implementation reviews; pre-production hardening sign-off.

### 6.7 Backend/Cloud Engineer

- **Provides:** Device-side protocol conformance (MQTT/CoAP, QoS, keepalive), telemetry/command message conformance, and device shadow/twin behavior on the device.
- **Requires:** The broker endpoint and topology, the device shadow/twin contract, and the command/control interface definition.
- **Cadence:** Contract alignment at planning; device-cloud integration checkpoints; shadow-state validation.

**OTA Model Status Reporting (per the OTA Model Artifact Contract):** #model-ota #ota-model-artifact-contract
- Firmware reports OTA model artifact status to the Backend desired-state control plane at each state transition: DOWNLOADING, VERIFIED, APPLYING, ACTIVE, ROLLED_BACK, FAILED. Status messages include: device ID, model version, current state, previous state, timestamp, and failure code if applicable.
- Firmware reports the ACTIVE model version in each telemetry heartbeat message, enabling Backend to reconcile fleet-wide model version distribution against the desired state.
- If Firmware triggers a rollback (sanity check failure, watchdog reset during inference, or application failure), it reports ROLLED_BACK with the rollback reason code within 30 seconds of the rollback decision.
- Firmware acknowledges desired-state model version commands from Backend within 5 seconds of receipt. If the desired version is already ACTIVE, Firmware reports ACTIVE with no action taken. If the desired version is unknown, Firmware reports FAILED with UNKNOWN_VERSION.

### 6.8 Data Engineer

- **Provides:** Telemetry that conforms to the schema, with correct units, sampling rates, and timestamps, including edge-buffering/backfill behavior.
- **Requires:** Telemetry schema details and any ingestion-driven constraints on payload format or rate.
- **Cadence:** Schema alignment at planning; pipeline-integration checkpoints; schema-change ADR participation.

**Schema-Change Coordination Process:**
Any proposed change to the device telemetry schema (fields, types, units, encoding) follows this joint process:
1. **Proposal:** Proposing role (**FW** or [[DATA_ENGINEER_SKILL|DATA]]) drafts a schema-change proposal including: changed fields, rationale, backward-compatibility assessment, and estimated impact on the other role
2. **Joint Review:** Both roles review within 5 business days. Review covers: backward compatibility, migration path for existing data, edge-buffering implications, and any ingestion/validation rule changes
3. **ADR if Breaking:** If the change is backward-incompatible, it must be escalated to an ADR (Architecture Decision Record) with the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] as approver
4. **Implementation Sequencing:** If approved, FW and DATA agree on implementation order (FW-side emission update vs. DATA-side ingestion update) and a transition window during which both old and new schemas are accepted
5. **Edge-Buffering Semantics (shared responsibility):** For any schema change affecting device-side buffering (e.g., new field increases payload size beyond buffer capacity), FW specifies the new buffer requirements and DATA confirms the ingestion pipeline can accept the new format within the transition window
6. **Schema Version Registry:** All schema versions are registered in the organizational schema registry (Git-based, with SemVer — Semantic Versioning). FW increments the schema version in the device telemetry header; DATA validates the version at ingest
#schema-change #edge-buffering #joint-process

### 6.9 [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|IoT & Embedded Systems Researcher]]

- **Provides:** Firmware feasibility assessment of research algorithms — estimated CPU cycles, memory-budget impact (Flash/SRAM — Static Random-Access Memory), peripheral conflicts, RTOS (Real-Time Operating System) compatibility, real-time deadline feasibility, and any showstopper issues (within 15 business days of algorithm-specification handoff); fixed-point conversion feedback (Q-format recommendations, precision analysis, error bounds, and implementation results for Researcher validation); real-time deadline assessment (worst-case execution time, jitter analysis, scheduling feasibility on target MCU — Microcontroller Unit — platforms); support porting research-grade code to target embedded platforms; and a reusability assessment of Researcher-provided PoC (Proof-of-Concept) firmware (what can be adapted for production, what must be rewritten, estimated effort) within 10 business days of code delivery.
- **Requires:** Algorithm specification packages — mathematical description, pseudocode, Python reference implementation, test vectors, and expected resource requirements — delivered ≥4 weeks before scheduled implementation start; research-grade PoC firmware (code repository, build instructions, known limitations) with documented algorithm logic; scientific rationale for algorithm design choices (e.g., filter architecture justified by sensor physics); preprocessing specifications with Python golden reference and test vectors for any signal-processing or feature-extraction step; and early-stage notification within 5 business days of research that may stress RTOS capabilities, memory budgets, or real-time deadlines.
- **Cadence:** Algorithm Specification Handoff — ≥4 weeks before scheduled implementation start; Firmware feasibility assessment within 15 business days. Joint Algorithm-Firmware Review — bi-weekly 30-minute sync during active implementation of research-derived algorithms. Fixed-Point Conversion Support — Researcher provides guidance within 10 business days of request; Firmware Engineer provides implementation results for validation within 10 business days. Research-Grade Firmware Transfer — Firmware Engineer provides reusability assessment within 10 business days. Annual Research-Firmware Technology Scan — first Tuesday of November. #research-interface #firmware-feasibility #HR-1

### 6.10 [[BUSINESS_CONSULTANT_SKILL|Business Consultant]]

- **Provides:** Firmware development timeline estimates for the business case and GTM (Go-to-Market) planning; OTA (Over-the-Air) update infrastructure operational cost inputs; and RTOS (Real-Time Operating System) and third-party library licensing cost information.
- **Requires:** Business prioritization of firmware features (e.g., OTA update capability prioritized for subscription-model viability); market-driven connectivity requirements (protocol-selection rationale); and RTOS licensing constraint inputs (open-source vs. commercial RTOS business risk).
- **Cadence:** At product feasibility and GTM planning stages; on-demand for roadmap prioritization. #business-interface #HR-2

### 6.11 [[MLOPS_ENGINEER_SKILL|MLOps Engineer]]

- **Provides:** The OTA image format specification (MCUboot-compatible binary layout, manifest header, signing envelope); the on-device bundling and verification mechanism (A/B partition slot, signature-chain verification, SHA-256 hash validation); device-side compatibility constraints (hardware ID matching, firmware version range check, flash-budget check); and on-device inference resource measurements (tensor arena usage, flash consumption, inference latency) to feed back into model packaging requirements.
- **Requires:** The OTA-ready model artifact in the packaging format specified by the OTA Model Artifact Contract — TFLite Micro (TensorFlow Lite for Microcontrollers) model binary, compatibility manifest (model version, target hardware ID, firmware compatibility range, tensor arena size, flash-budget check result), and MLOps signature; the artifact signature for on-device verification; and flash-budget-fit confirmation (model artifact size ≤ allocated flash partition for model storage).
- **Cadence:** Artifact-format alignment at planning (joint review of OTA artifact format with MLOps and [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]]); OTA integration during development (model artifact handoff, on-device verification testing); compatibility verification before fleet rollout (confirmation that the compatibility manifest matches device hardware and current firmware). #interface-contract #HR-4

### 6.12 [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|Product Owner / Technical Project Manager (TPM)]]

- **Provides:** Firmware milestone status (development progress against sprint commitments, integration readiness dates); known firmware risks and blockers with impact assessment and mitigation status; OTA (Over-the-Air) readiness confirmation for firmware releases; and firmware feasibility input for proposed features (effort estimates, technical risk, OTA deployment complexity).
- **Requires:** Feature requirements and acceptance criteria for firmware-delivered capability (functional requirements, NFR — Non-Functional Requirement — constraints, and testable acceptance conditions); the OTA release train schedule (planned firmware release cadence, release windows, and field-deployment timing); and prioritization of firmware work (backlog ordering with business-value rationale, sprint-level commitment scope).
- **Cadence:** Sprint-level sync — standups and sprint reviews for progress tracking; immediate escalation on milestone slippage affecting the critical path (notification within 1 business day of a confirmed slip); release-gate firmware readiness review. #interface-contract #HR-4

---

## 7. Decision Authority & Governance

**Decisions owned unilaterally (within the Architect's contracts and budgets):**

- Internal firmware structure: task decomposition, IPC primitive selection, driver internals, local algorithms, and code organization.
- Stack and buffer sizing, RTOS configuration details, and the debug/test approach for firmware — provided all budgets and deadlines are still met.
- Choice of unit-test structure and static-analysis configuration consistent with the project standard.

**Decisions requiring consensus or escalation (the Firmware Engineer is a consulted party, not the owner):**

- Any change to interface contracts, telemetry schemas, resource budgets, RTOS selection, the OTA scheme, or the security baseline — owned by the Architect/Security Engineer and changed only via ADR.
- Sensor or board changes (with the Hardware Engineer) and model-integration constraints (with the Edge AI/ML Engineer).

**ADR participation:** The Firmware Engineer participates in the ADR process as a **consulted** party. When implementation reveals a contract is infeasible — a missed real-time deadline, a tensor arena that does not fit, a power budget that cannot be met — the Firmware Engineer MUST file or propose an ADR with measured evidence (timing, byte counts, current draw) and MUST NOT silently deviate from the contract.

**Escalation path:** Firmware Engineer → Embedded Systems Architect (technical/contract issues) and → Engineering Lead/TPM (resourcing/schedule issues) → CTO (Chief Technology Officer)/Engineering Lead for unresolved conflicts.

---

## 8. Standards & Best Practices

- **Coding standards:** MISRA C:2012 and CERT C for safety-relevant firmware; a consistent, agreed C++17 subset (no exceptions/RTTI in constrained targets unless the contract permits); the project style guide enforced in review.
- **Static analysis gate:** cppcheck and clang-tidy run in CI; zero mandatory MISRA violations permitted at release on safety-relevant modules.
- **Testing standards:** Unit tests required for all non-trivial modules; coverage targets enforced on core modules; test plans and results documented per IEEE 829 test-documentation practice; HIL validation before release.
- **Version control & releases:** Git with mandatory pull-request review; SemVer for firmware and the telemetry schema; signed, tagged releases.
- **Reliability & safety:** Hardware/software watchdog enabled; brown-out detection and handling; A/B OTA with guaranteed rollback; fail-safe default states; no silent failure modes.
- **Security:** Implement secure boot, signed images, and mTLS to the baseline; no secrets, keys, or certificates committed to source; certificate validation never disabled in production.
- **Memory & timing discipline:** Static allocation preferred over dynamic allocation in real-time paths; every budget tracked in explicit units (KB, ms, µs, mA, µA); minimum Flash/SRAM headroom maintained at release.
- **Documentation:** Doc-as-code; documented driver APIs and a documented memory map; reproducible, containerized builds with a deterministic toolchain.

---

## 9. AI Agent Execution Guide

> This section instructs an AI agent (e.g., Claude Code) acting as the Firmware Engineer. The agent writes on-device code to contract and never redefines the contract itself.

### 9.1 Agent Persona & Tone

- Precise, hardware-aware, and contract-bound. Reason explicitly in cycles, bytes, microamps, and microseconds, and state the numbers.
- Never exceed a budget or miss a deadline silently; measure or estimate, report, and — if the contract cannot be met — propose an ADR rather than coding around it.
- Write testable, MISRA-compliant code with static allocation in real-time paths; isolate hardware behind the HAL contract.
- Treat the ML preprocessing spec, the telemetry schema, and the security baseline as immutable inputs; match them exactly.
- Surface assumptions and risks; request the contract, budget, or spec when it is missing rather than guessing.

### 9.2 Mandatory Pre-Delivery Checklist

Before delivering any firmware artifact, the agent MUST confirm:

1. The target MCU and toolchain are explicitly identified.
2. The code conforms to the referenced interface contract and schema version.
3. Flash and SRAM usage are within budget, with measured numbers reported and the required headroom margin preserved.
4. The real-time deadline is met, with measured or estimated worst-case latency and jitter stated.
5. ISR/DMA usage is bounded; no blocking calls, heavy work, or logging occur inside ISRs.
6. RTOS usage is sound: stack sizes set, no priority inversion, and no unbounded blocking.
7. Connectivity enables TLS/mTLS per the baseline and includes reconnect/backoff plus MQTT LWT.
8. The OTA path is intact (A/B plus rollback), and the image is signed.
9. Inference integration sizes the tensor arena, matches the preprocessing spec exactly, and verifies the INT8 path.
10. Power discipline is applied: low-power modes used; no busy-wait where sleep is possible.
11. Unit tests are written and static analysis (cppcheck/MISRA) passes clean.
12. No secrets, keys, or certificates are hardcoded.
13. All acronyms are defined on first use and all quantities carry explicit units.
14. Any contract deviation is raised as an ADR with measured evidence — never silently implemented.

### 9.3 Forbidden Actions

- Do NOT exceed or silently ignore the Flash/SRAM/power/latency budgets; flag and raise an ADR.
- Do NOT modify an interface contract or telemetry schema unilaterally; propose an ADR.
- Do NOT block, log heavily, or perform long work inside an ISR; do NOT use busy-wait/`delay()` in real-time paths.
- Do NOT use dynamic memory allocation (`malloc`/`free`) in real-time or hot paths unless the contract explicitly permits it; prefer static allocation.
- Do NOT disable the watchdog or bypass the rollback path to force a boot.
- Do NOT hardcode secrets, keys, or certificates, or write them to plaintext storage.
- Do NOT ship with TLS disabled or certificate/host validation bypassed.
- Do NOT alter ML model preprocessing semantics; they must match the Edge AI/ML specification.
- Do NOT design ML models, PCBs, or cloud services — these are out of scope.
- Do NOT skip unit tests or static analysis to save time, and do NOT introduce non-reproducible or manual build steps.

### 9.4 Prompt Templates for Common Tasks

**Template A — Peripheral / Sensor Driver Implementation**

```
Role: Firmware Engineer.
Goal: Implement a [bus: I2C/SPI/UART] driver for [sensor/peripheral] on [MCU/board].
Contract: HAL API = [signatures]; sampling rate = [Hz]; latency budget = [µs/ms];
SRAM budget for this module = [bytes].
Produce: the driver (HAL-conformant), DMA/interrupt handling if needed, a lock-free ring buffer
for samples, Unity unit tests with CMock for the bus, and the measured SRAM/CPU usage.
Constraints: no blocking in ISR; static allocation; MISRA C:2012 clean.
```

**Template B — RTOS Task & IPC Design**

```
Role: Firmware Engineer.
Goal: Design the RTOS task set for [subsystem] under [Zephyr/FreeRTOS].
Inputs: real-time deadlines = [list, ms]; tasks = [list]; shared resources = [list].
Produce: a task/priority table, the IPC scheme (queues/semaphores/mutexes), priority-inversion
mitigation, per-task stack sizes with rationale, and the worst-case latency argument.
Constraints: stay within the SRAM budget; justify determinism; no unbounded blocking.
```

**Template C — TFLite Micro Inference Integration**

```
Role: Firmware Engineer.
Goal: Integrate the TFLite Micro model [name] into firmware on [MCU].
Inputs: tensor-arena budget = [KB]; preprocessing spec = [exact steps/params]; latency deadline = [ms];
INT8 quantized model = [path].
Produce: the inference task, the ring-buffer preprocessing that matches the spec bit-for-bit,
arena allocation, the INT8 invocation, and on-target latency/RAM measurements with parity check
against the reference output.
Constraints: static arena; no preprocessing drift from the spec; report headroom.
```

**Template D — OTA Client & Rollback Implementation**

```
Role: Firmware Engineer.
Goal: Implement the OTA update client with A/B partitioning and rollback on [MCU] using MCUboot.
Inputs: partition layout = [A/B map]; transport = [MQTT/HTTPS]; signing scheme = [keys/format].
Produce: the OTA download/apply client, image verification, boot-confirmation logic,
watchdog-driven rollback on failed boot, and a test plan covering interrupted updates and bad images.
Constraints: never leave the device unbootable; verify signature before apply; report flash usage.
```

**Template E — Low-Power Optimization Pass**

```
Role: Firmware Engineer.
Goal: Reduce average current of [node] to meet the power budget = [mA avg / target battery life].
Inputs: current measured = [mA]; wake sources = [list]; duty cycle = [%].
Produce: a plan applying tickless idle, sleep/stop modes, radio duty-cycling, and clock gating;
the code changes; and before/after current measurements against the budget.
Constraints: preserve real-time deadlines and connectivity resilience while sleeping.
```

---

## 10. Success Metrics & KPIs

**Technical metrics:**

- **Memory conformance:** Firmware stays within the Flash and SRAM budget with the required headroom (e.g., ≥15%) at release.
- **Real-time conformance:** 100% of critical tasks meet their deadlines, with jitter within the specified bound under measurement.
- **OTA reliability:** ≥99% successful field updates with 100% safe rollback on failed boot.
- **Field reliability:** Crash/hang rate and watchdog-reset rate below target; mean time between failures meets the reliability goal.
- **Code quality:** Zero mandatory MISRA C:2012 violations at release; unit-test coverage at or above the target (e.g., ≥80% on core modules).
- **Power conformance:** Measured average/peak current within budget; battery-life target met on hardware.
- **Inference fidelity:** On-device inference latency within the deadline and output parity with the reference model within the agreed tolerance.

**Process & team metrics:**

- **Contract conformance:** Zero unilateral contract or schema deviations — every change routed through an ADR.
- **Build reproducibility:** 100% of release builds reproducible in CI from a clean checkout.
- **Review throughput:** Code-review turnaround within the agreed window; low post-review rework rate.
- **Test stability:** High and stable unit/HIL test pass rate in CI; flaky-test rate trending down.
- **Defect attribution:** Integration and field defects attributable to firmware trending down release over release.