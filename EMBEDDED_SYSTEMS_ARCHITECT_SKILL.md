---
title: "Embedded Systems Architect — Skill Card"
date: 2026-06-20
status: final
tags:
  - skill-card
  - embedded-iot
  - architecture
cssclass: skill-card
---

# EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md

## 1. Role Identity

- **Role Title:** Embedded Systems Architect
- **Team:** Embedded/IoT (Internet of Things) AI (Artificial Intelligence) Workflow Engineering
- **Reports To:** Product Owner / Technical Project Manager (TPM), with a dotted-line relationship to the CTO (Chief Technology Officer) / Engineering Lead
- **Seniority Level:** Defined as tiers; this skill card is written to the **Staff/Principal** bar.
    - **Senior Embedded Systems Architect:** Owns architecture for a single product line or subsystem; authors contracts under an existing reference architecture.
    - **Staff Embedded Systems Architect:** Owns architecture across multiple product lines; sets cross-cutting interface and platform standards.
    - **Principal Embedded Systems Architect:** Owns the organization-wide reference architecture, platform strategy, and long-horizon technology bets; final architectural authority and ADR (Architecture Decision Record) approver.
- **Deputy Architect:** A designated alternate for the Embedded Systems Architect, drawn from the Staff [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]] or Staff [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]] tier. The Deputy Architect is appointed by the Architect with the concurrence of the CTO (Chief Technology Officer) and is reviewed and re-designated annually. The Deputy retains their primary role responsibilities; this is an additional duty with an estimated 20–30% capacity allocation, not a full-time architecture position.

  **Deputy Architect Authority (exercisable when the Architect is unavailable or has delegated):**
  - Maintain existing interface contracts — clarify, interpret, and document existing contracts without changing scope, budgets, or schemas. Contract changes (scope, budget, schema) still require an ADR (Architecture Decision Record)
  - Approve non-breaking ADRs — ADRs that do not: change a platform selection, protocol choice, resource budget, security baseline, or OTA (Over-the-Air) strategy
  - Chair the Architecture Review Board (ARB) — convene, facilitate, and document ARB meetings; the ARB can make decisions within its chartered authority regardless of who chairs
  - Resolve Tier 2 (HIGH) decision requests within the SLA window defined in §7
  - Serve as the primary architecture point of contact during the Architect's planned absence (vacation, conference, training)

  **Deputy Architect Authority Limits (NOT authorized):**
  - Cannot change resource budgets (Flash, SRAM — Static Random-Access Memory, power, latency) — these require the Architect or an ARB consensus vote
  - Cannot create new interface contracts or deprecate existing contracts
  - Cannot approve Security-Relevant ADRs (those tagged #security-impact)
  - Cannot sign the production architecture release gate — this is reserved for the Architect
  - Cannot modify the security baseline or OTA strategy

  **Deputy Architect Qualification Requirements:**
  - Must hold a Staff-level tier in Firmware or Backend/Cloud engineering
  - Must have served as a Senior Engineer for ≥2 years in the organization
  - Must complete the Architecture Governance training curriculum (ADR authoring, interface contract design, trade-study methodology, NFR — Non-Functional Requirement — specification)
  - Must pass a qualification review conducted by the Architect and CTO, including: producing a shadow ADR for a real architectural decision, defending a trade study, and resolving a simulated contract dispute
  #deputy-architect #bus-factor #resilience
- **Summary:** The Embedded Systems Architect is the single technical authority for the end-to-end system spanning constrained MCU (Microcontroller Unit) edge nodes (STM32, ESP32), Linux-class MPU (Microprocessor Unit) gateways (Raspberry Pi), and cloud services. The role exists to convert product and field requirements into a coherent, resource-bounded, and parallelizable technical design: it selects compute platforms, partitions workloads between on-device inference and cloud aggregation, defines the communication topology and protocols, and freezes the interface contracts and resource budgets that gate every downstream team. Its unique value is enabling firmware, ML (Machine Learning), data, cloud, and frontend teams to build independently against stable, versioned interfaces while guaranteeing the integrated system meets its real-time, power, security, and reliability targets.

---

## 2. Core Mission & Scope

**Mission:** Define and govern an end-to-end embedded/IoT AI architecture that is technically feasible within hardware constraints, secure by design, updatable in the field, and decomposed into stable interface contracts so that all engineering disciplines can develop, integrate, and ship in parallel.

**Owns (unilateral authority, subject to the ADR process):**

- End-to-end system architecture across edge devices, gateways, and cloud, including the deployment and data-flow views.
- MCU/SoC (System on Chip) platform selection and workload partitioning between MCU-class targets (TinyML — Tiny Machine Learning — on Cortex-M) and MPU-class targets (Linux on Raspberry Pi).
- Communication topology and protocol selection (MQTT — Message Queuing Telemetry Transport — / CoAP — Constrained Application Protocol — over Wi-Fi/BLE — Bluetooth Low Energy — /LoRaWAN — Long Range Wide Area Network), including QoS (Quality of Service) levels and offline/fallback behavior.
- Hardware abstraction boundaries: HAL (Hardware Abstraction Layer) layering, RTOS (Real-Time Operating System) selection, and message/payload schemas.
- On-device ML deployment strategy: model format (TFLite Micro — TensorFlow Lite for Microcontrollers), tensor-arena sizing, and the edge-versus-cloud inference split.
- Non-functional requirements: real-time deadlines, per-node compute/memory/power budgets, OTA (Over-the-Air) update path (A/B partitioning with rollback), and the security baseline.
- **End-to-end system robustness:** The Architect is the primary guarantor of cross-layer system robustness — the property that the system behaves correctly under adverse conditions that span multiple architectural layers. This includes: (a) defining the #system-robustness-contract that specifies how each layer must respond to failures originating in other layers, (b) owning the system-level #FMEA (Failure Mode and Effects Analysis) or #FTA (Fault Tree Analysis) that traces failure chains across hardware, firmware, edge AI, communication, cloud, and data layers, (c) defining cross-layer robustness #NFR (Non-Functional Requirement) entries in the NFR Verification Matrix, (d) arbitrating robustness trade-offs between layers, and (e) signing off on end-to-end robustness at the production release gate. #quality-attribute #robustness
- **End-to-end OTA (Over-the-Air) governance:** The Architect is the single governance owner of the end-to-end OTA update path spanning all four OTA layers: (a) on-device apply and rollback (owned by [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]]), (b) delivery transport and fleet rollout mechanism (owned by [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps/Platform Engineer]]), (c) cloud desired-state control plane (owned by [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]]), and (d) model rollout strategy (owned by [[MLOPS_ENGINEER_SKILL|MLOps Engineer]]). The Architect owns the OTA Model Artifact Contract (§5) that chains through all four roles, defines the end-to-end OTA validation requirements, arbitrates OTA-related disputes between the four layers, and signs off on OTA readiness at the production release gate. The Architect does not implement any layer's OTA mechanism — each role owns its layer's implementation to the OTA Model Artifact Contract. #OTA-governance #end-to-end-ota #CR-3
- The ADR repository and architecture governance.

**Influences (advisory; does not implement):**

- Detailed firmware implementation — sets the HAL/contract; the Firmware Engineer owns the code.
- Model layer architecture and training — sets the footprint/latency envelope; the Edge AI/ML Engineer owns the model.
- PCB design — validates feasibility and constrains the platform; the Hardware Engineer owns schematics/layout.
- Cloud service implementation — defines interface contracts; the Backend/Cloud Engineer owns the services.
- CI/CD (Continuous Integration / Continuous Deployment) and fleet tooling — sets the OTA strategy; the DevOps/Platform Engineer owns the pipeline.
- Security implementation — mandates the baseline; the Security Engineer owns the controls.
- Layer-specific robustness mechanisms (watchdogs, circuit breakers, fault tolerance patterns, environmental hardening) — sets cross-layer robustness requirements; each implementing role owns its layer-specific mechanism per the #system-robustness-contract

**Explicitly Does NOT Own:**

- Writing production firmware, drivers, cloud APIs, or dashboard code.
- Training, quantizing, or selecting ML model layers.
- Schematic capture or PCB layout.
- Sprint-level task assignment, backlog prioritization, or people management (owned by the TPM / engineering management).
- Implementation of layer-specific robustness mechanisms (owned by [[HARDWARE_ENGINEER_SKILL|HW]], [[FIRMWARE_ENGINEER_SKILL|FW]], [[BACKEND_CLOUD_ENGINEER_SKILL|BACK]], [[DATA_ENGINEER_SKILL|DATA]], [[SECURITY_ENGINEER_SKILL|SEC]]).
- Robustness validation and testing execution (owned by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]] — Architect defines the cross-layer robustness NFRs and the #system-robustness-contract; QA validates them through fault-injection, stress testing, and the cross-layer robustness regression suite).

---

## 3. Lifecycle Stage Engagement

### 3.1 Research

- **Activities:** Survey candidate MCU/SoC platforms (e.g., STM32H7/U5/L4, ESP32-S3, Raspberry Pi CM4/5) against the target workload; run feasibility trade studies comparing on-device inference latency against cloud round-trip latency; evaluate protocols (MQTT vs CoAP; Wi-Fi vs BLE vs LoRaWAN) against the connectivity, range, and power profile; estimate TinyML feasibility by checking projected model footprint against available SRAM (Static Random-Access Memory)/Flash and verifying TFLite Micro operator coverage; analyze power source (battery/solar) to derive the energy envelope.
- **Deliverables:** Technology trade-study report, candidate-platform shortlist, edge/cloud feasibility memo, and draft per-node power/memory budgets.

### 3.2 Planning

- **Activities:** Author the System Architecture Document (SAD) — node topology, data-flow, and deployment views; define interface contracts and message/payload schemas (Protocol Buffers / CBOR — Concise Binary Object Representation); select the RTOS (Zephyr vs FreeRTOS vs bare-metal) and define HAL layering; specify the OTA strategy (A/B partitioning, MCUboot, rollback); co-define the security baseline (secure boot, mTLS — mutual Transport Layer Security, root of trust) with the Security Engineer; finalize per-node compute/memory/power budgets; author the foundational ADRs.
- **Deliverables:** SAD v1, interface-contract specifications, schema definitions, OTA strategy spec, security baseline spec, resource-budget tables, and the initial ADR set.

### 3.3 Development

- **Activities:** Support teams building against the contracts; clarify and amend contracts only through versioned ADRs; review the firmware HAL implementation for contract conformance; validate tensor-arena sizing with the Edge AI/ML Engineer as real models materialize; adjudicate cross-team interface conflicts; maintain the architecture as a living, version-controlled document.
- **Continuous Integration Testing governance:** Require weekly integration smoke tests for every interface contract pair entering Development. Contract pairs: FW↔BACK (device-cloud), BACK↔FRONT (API/dashboard), DATA↔ML (data-to-training), MLO↔DEV (model-to-OTA), FW↔ML (model-to-firmware). Each pair runs at least one integration smoke test per week during Development. The Architect reviews smoke test results at the bi-weekly ARB meeting. Persistent failures (≥2 consecutive weeks) on any contract pair block the Development→Execution transition for both roles in the pair. #integration-testing #shift-left #HR-5
- **Integration Readiness exit criterion:** Before a role exits Development, all its interface contract pairs must have: (a) ≥2 consecutive weeks of passing integration smoke tests, (b) a joint Integration Readiness Declaration signed by both roles in each pair, (c) any integration defects found during smoke testing resolved or accepted via ADR (Architecture Decision Record). The Architect defines the Integration Readiness criteria in the Interface Contract Specifications (§5). #integration-testing #shift-left #HR-5
- **Deliverables:** Versioned contract amendments, updated ADRs, architecture-review notes, and per-interface conformance checklists.

### 3.4 Execution

- **Activities:** Oversee end-to-end integration (sensor → firmware → on-device inference → MQTT → cloud → dashboard); verify non-functional requirements with measurements — latency against deadline, current draw against power budget, and an OTA update-and-rollback test on real hardware; drive resolution of integration-level architecture defects; freeze interfaces ahead of production.
- **Deliverables:** Integration architecture validation report, NFR (Non-Functional Requirement) verification matrix, and OTA validation sign-off.

### 3.5 Production-Ready

- **Activities:** Execute the final architecture release gate; confirm the SBOM (Software Bill of Materials), security baseline, and OTA governance are in place; define field-scaling considerations (fleet provisioning, MQTT broker scaling) with Backend/DevOps; capture the as-built architecture and lessons-learned ADRs; define the architecture maintenance and evolution plan.
- **Architect Succession Exercise (annual):** Conduct an annual Architect Succession Exercise during the Production-Ready stage of the final release cycle of each calendar year (typically November–December). The Deputy Architect produces: (a) a shadow System Architecture Document (SAD) for a hypothetical next-generation product or a substantial feature expansion of the current product — demonstrating ability to define topology, select platforms, partition workloads, and freeze interface contracts independently, (b) a set of 3 shadow ADRs for architectural decisions that would arise from the shadow SAD — demonstrating trade-study methodology and governance discipline, and (c) a shadow resource budget table for at least two node types — demonstrating quantitative architecture reasoning. The Architect reviews the shadow artifacts against the same standards applied to production architecture artifacts. The exercise output is a Succession Readiness Assessment (Ready / Conditionally Ready / Not Ready) with specific development recommendations. This exercise verifies that the organization can sustain architectural continuity if the Architect transitions, and it identifies Deputy development needs before they become critical. Results are reviewed with the CTO and inform the Deputy Architect re-designation for the following year. Shadow artifacts are archived alongside production architecture artifacts for reference.

  **ARB (Architecture Review Board) chairmanship rotation (NEW — Long-Term Bet):** During the annual Succession Exercise, the Deputy Architect chairs the ARB for one full release cycle — or one simulated cycle during the exercise when no live release cycle aligns — while the Architect observes all meetings without holding voting rights. The Deputy must: (a) convene and facilitate all bi-weekly ARB meetings during the rotation period; (b) manage the full ARB decision queue, including the expanded-authority queue for contract MINOR/PATCH (Minor/Patch version) changes, non-novel technology evaluations, SE (Sustaining Engineering) prioritization, and agent proposals (where applicable by autonomy phase); (c) produce a complete ARB Decision Record for each meeting held during the rotation; and (d) escalate any decision that exceeds ARB authority — per the Decision Limits defined in §7.Z — to the Architect before the vote is held. This rotation tests whether the ARB can function as a collective decision-making body independent of the Architect's active chairmanship — a critical prerequisite for the distribution of decision classes established in §7.Z #expanded-authority and for Human-Governed Autonomy (Phase 3). The Architect reviews all ARB Decision Records from the rotation period and assesses whether escalation judgments, vote facilitation, and the use of expanded authority were exercised correctly. Findings from the chairmanship rotation are documented in the Succession Readiness Assessment (Ready / Conditionally Ready / Not Ready) submitted to the CTO (Chief Technology Officer) alongside findings from the shadow SAD (System Architecture Document), shadow ADRs, and shadow resource budget exercises. #succession-exercise #organizational-resilience #ARB #distributed-governance #expanded-authority
- **Deliverables:** Production architecture sign-off, as-built SAD, fleet-scaling guidance, and post-release ADRs.

### 3.6 Post-Launch/Market

**Activities:**
- **Architecture drift monitoring:** Review the deployed system quarterly against the as-built SAD (System Architecture Document) and active ADRs to detect architectural drift (undocumented topology changes, contract deviations, resource budget exceedances). If drift is detected, file an ADR for retroactive ratification or initiate a correction within 10 business days. #post-launch
- **Fleet-scale architecture review:** Review fleet growth telemetry (device count, MQTT broker load, backend throughput) quarterly against the architecture's stated scaling assumptions. If fleet metrics are trending to exceed the architecture's scaling envelope within 12 months, initiate a capacity architecture review and produce a scaling recommendation within 15 business days. #field-reliability
- **Sustaining architecture consultation:** Provide architecture-level guidance on Sustaining Engineering backlog items that have cross-layer implications (contract changes, new OTA flows, security baseline updates). Response SLA: 5 business days for architecture impact assessment. #sustaining-engineering #lifecycle-gap #CR-5
- **Incident response participation:** Respond to [[INCIDENT_COMMANDER|Incident Commander]] direction during declared cross-layer incidents within the role's defined response SLA. Provide role-specific expertise to the war room and document any temporary deviations from standard process for retroactive ADR formalization within 5 business days of incident closure. **Note: safety-critical design decisions remain under the Architect's permanent authority and cannot be overridden by the Incident Commander.** Participate in the annual cross-layer incident drill. #cross-layer-incident #incident-commander #emergency-tempo

**Deliverables:**
- Architecture Drift Report (quarterly)
- Scaling recommendation (on-demand, when fleet metrics approach envelope limits)
- Architecture impact assessments (on-demand per Sustaining Engineering backlog)

---

## 4. Technical Competencies

> Proficiency legend — **Expert:** sets direction and is the final reference; **Advanced:** works independently and reviews others; **Working:** sufficient to specify constraints and collaborate, not to implement.

### 4.1 Hardware & Systems Architecture

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|MCU/SoC platform selection|Expert|Choosing the target per workload, power, and cost|STM32 (H7/U5/L4), ESP32-S3, RP2040, RPi CM4/5|
|ARM core architecture reasoning|Expert|Matching core class to compute and latency needs|Cortex-M0+/M4/M7/M33, Cortex-A53/A76|
|Memory hierarchy budgeting|Expert|Sizing per-node Flash/SRAM/PSRAM (Pseudo-Static RAM)|Flash, SRAM, PSRAM, eMMC|
|Power-domain & energy budgeting|Advanced|Deriving field battery/solar envelopes and sleep strategy|LDO/buck regulators, RTC wake, low-power modes|
|Sensor bus topology design|Expert|Selecting and arbitrating sensor interfaces|I2C, SPI, UART, CAN, 1-Wire|
|Compute partitioning (MCU vs MPU)|Expert|Splitting workload across node classes|Cortex-M nodes vs Linux SoC gateways|
|Thermal & environmental envelope|Working|Setting operating limits for outdoor field nodes|IP rating, industrial temperature ranges|

### 4.2 Firmware & Low-Level Design

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|RTOS selection & trade-off analysis|Expert|Choosing RTOS vs bare-metal per node|Zephyr, FreeRTOS, NuttX, bare-metal|
|Bootloader & OTA architecture|Expert|Designing A/B partitions with safe rollback|MCUboot, dual-bank/A-B slots|
|HAL & driver-boundary design|Expert|Defining abstraction so teams build in parallel|CMSIS (Cortex Microcontroller Software Interface Standard), Zephyr HAL, STM32 HAL/LL|
|Interrupt/DMA-driven design|Advanced|Setting determinism and latency requirements|NVIC, DMA (Direct Memory Access), ISR (Interrupt Service Routine) budgets|
|Real-time scheduling constraints|Advanced|Defining and verifying real-time deadlines|Rate-monotonic concepts, RTOS schedulers|
|Memory isolation & protection|Working|Mandating isolation for safety/security|Memory Protection Unit, ARM TrustZone|
|Firmware image integrity|Advanced|Mandating signed images and anti-rollback|Image signing, rollback counters, MCUboot|

### 4.3 Software & Middleware Architecture

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Edge gateway architecture|Expert|Designing the Linux-class gateway role|K3s (lightweight Kubernetes), balena, Docker|
|Message schema & serialization design|Expert|Defining payload contracts and evolution rules|Protocol Buffers, CBOR, JSON Schema|
|Pub/sub & data-flow topology|Expert|Designing telemetry and command/control flow|MQTT broker topology, message routing|
|Device-cloud state modeling|Advanced|Defining device shadow/twin patterns|Device twin/shadow, AWS IoT / Azure IoT patterns|
|Time-series data-flow design|Advanced|Routing telemetry to storage and analytics|InfluxDB / TimescaleDB ingestion patterns|
|Interface/API contract design|Advanced|Defining edge–cloud boundaries|REST (Representational State Transfer), gRPC, OpenAPI|
|Offline/store-and-forward strategy|Advanced|Designing behavior under intermittent links|Local queues, store-and-forward buffering|

### 4.4 AI/ML Awareness & Edge Inference

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|TinyML deployment constraint analysis|Advanced|Setting the model footprint envelope|TFLite Micro, TinyML, Edge Impulse|
|Tensor-arena sizing|Advanced|Reserving static SRAM for inference|TFLite Micro arena, static allocation|
|Quantization impact assessment|Advanced|Trading accuracy against memory/latency|INT8 (8-bit integer) post-training quantization, QAT awareness|
|Operator-support validation|Working|Confirming model ops are runnable on target|TFLite Micro operator set, CMSIS-NN (CMSIS Neural Network)|
|Edge-vs-cloud inference partitioning|Expert|Deciding where each inference runs|Latency/power/bandwidth trade analysis|
|Inference latency/throughput estimation|Advanced|Verifying real-time feasibility on Cortex-M|Cycle estimation, on-target profiling|
|ML lifecycle awareness|Working|Coordinating model updates via OTA|Model registry, OTA model-delivery concepts|

### 4.5 Communication Protocols & Topology

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Application protocol selection|Expert|Choosing MQTT vs CoAP per use case|MQTT, CoAP|
|QoS & reliability design|Expert|Setting delivery guarantees per data class|MQTT QoS 0/1/2, CoAP CON/NON|
|Link/transport selection|Expert|Wi-Fi vs BLE vs LoRaWAN per range/power|Wi-Fi, BLE, LoRaWAN, Thread|
|Transport security design|Advanced|Mandating encrypted, authenticated channels|TLS, mTLS, DTLS, X.509 certificates|
|Network resilience & fallback|Expert|Defining reconnection and degraded-mode behavior|MQTT LWT (Last Will and Testament), exponential backoff|
|Payload & bandwidth budgeting|Advanced|Sizing payloads for constrained links|CBOR compaction, LoRaWAN duty-cycle limits|
|Identity & provisioning topology|Advanced|Fleet identity and onboarding design|X.509 device identity, MQTT client IDs|

### 4.6 Tools, Processes & Governance

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Architecture modeling|Expert|Documenting context/container/component views|C4 model, SysML (Systems Modeling Language), PlantUML, Mermaid|
|ADR authoring & governance|Expert|Recording and versioning every key decision|ADRs in Markdown, Git|
|Trade-study methodology|Expert|Structuring platform/protocol decisions|Weighted decision matrices, Pugh matrix|
|Requirements traceability|Advanced|Linking requirement → architecture → test|Traceability matrix, Jira, DOORS|
|Doc-as-code & version control|Advanced|Keeping all architecture artifacts in VCS|Git, Markdown, Mermaid|
|Standards compliance governance|Advanced|Enforcing quality/safety/security baselines|ISO/IEC 25010, MISRA C:2012, OWASP IoT Top 10|
|Risk & dependency analysis|Advanced|Surfacing interface and critical-path risk|Risk register, dependency mapping|

---

## 5. Deliverables & Artifacts

|Artifact|Description|Consumers|Format/Standard|Versioning Approach|
|---|---|---|---|---|
|System Architecture Document (SAD)|Authoritative topology, data-flow, and deployment views with rationale|All engineering roles|Markdown + C4/Mermaid diagrams|Semantic version in Git; major bump on topology change|
|Interface Contract Specifications|Stable boundaries between firmware, edge, cloud, and frontend. Each interface contract specification now includes an Integration Readiness Criteria appendix defining: (a) the minimum integration smoke test scenarios for that contract (at least 3: happy path, degraded path, and failure/recovery path), (b) the test environment required (virtualized, emulated, or HIL — Hardware-in-the-Loop), (c) the pass/fail criteria for each scenario, and (d) the Integration Readiness Declaration template to be signed by both consumer and producer roles before Development exit. #integration-testing #shift-left #HR-5|Firmware, Backend, Edge AI/ML, Frontend, QA|Markdown + schema files|SemVer per contract; breaking change → major + ADR|
|Message/Payload Schemas|Canonical wire formats for telemetry and commands|Firmware, Backend, Data, Frontend|Protocol Buffers (.proto) / CBOR + JSON Schema|Schema registry; additive-only minor, breaking → major|
|Protocol & Topology Specification|Chosen protocols, QoS, transports, and fallback behavior|Firmware, Backend, DevOps, Security|Markdown + sequence diagrams|Versioned with SAD|
|Per-Node Resource Budgets|Compute, Flash/SRAM/PSRAM, power, and latency targets per node|Firmware, Hardware, Edge AI/ML, QA|Markdown tables (explicit units)|Versioned; re-baselined at each integration milestone|
|HAL & RTOS Selection Spec|Abstraction layering and RTOS choice with rationale|Firmware, QA|Markdown + ADR reference|Versioned with SAD|
|OTA Strategy Specification|A/B partitioning, signing, and rollback policy. The OTA Strategy Specification also defines the canonical OTA artifact format, which is the single authoritative reference for all roles in the OTA pipeline: (a) image format — MCUboot-compatible binary layout with manifest header, (b) signing envelope — algorithm identifier, key reference, and signature block structure, (c) metadata manifest — firmware or model version, target hardware ID (Hardware Identifier), compatibility matrix, flash-budget check fields, and A/B slot designation, and (d) artifact naming and versioning convention — SemVer (Semantic Versioning) with build metadata. [[FIRMWARE_ENGINEER_SKILL\|Firmware]] produces artifacts to this format; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] packages and distributes artifacts in this format; [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]] references this format in the desired-state control plane; [[MLOPS_ENGINEER_SKILL\|MLOps]] ensures model artifacts conform to this format. Any change to the artifact format requires an ADR (Architecture Decision Record) with all four consuming roles as consulted parties. #ota-artifact-format #single-source-of-truth|Firmware, DevOps, Security|Markdown|SemVer; major bump on partition/scheme change|
|Security Baseline Specification|Secure boot, mTLS, identity, and root-of-trust requirements (co-owned with Security Engineer)|Firmware, Backend, Hardware, DevOps|Markdown|Versioned jointly with Security Engineer|
|Architecture Decision Records (ADRs)|Immutable record of each significant decision|All roles|Markdown (one file per ADR)|Append-only; status transitions, never edited in place|
|NFR Verification Matrix|Mapping of each non-functional requirement to its measured result|QA, TPM, Security|Markdown table|Updated each validation cycle|
|Trade-Study Reports|Structured comparison behind platform/protocol choices|TPM, Hardware, Edge AI/ML|Markdown + decision matrix|Snapshot per decision; linked from ADR|
|As-Built Architecture|Final, production-accurate architecture at release gate|All roles, future maintainers|Markdown + diagrams|Tagged to the release version|
| System Robustness Contract | Authoritative cross-layer robustness specification defining: (a) failure domains and their boundaries (hardware, firmware, edge AI, communication, cloud, data), (b) required robustness behavior per layer when a failure originates in another layer (e.g., "FW must enter fail-safe state within 100ms of detecting corrupted sensor data regardless of corruption source"), (c) cross-layer failure chain taxonomy with severity classification (Critical / High / Medium / Low) based on system-level impact analysis using #FMEA (Failure Mode and Effects Analysis) methodology, (d) robustness #NFR entries with quantified targets per failure scenario, (e) shared robustness design patterns (#graceful-degradation paths, #failure-containment boundaries, fallback modes), and (f) robustness sign-off criteria for production release. Co-signed by [[HARDWARE_ENGINEER_SKILL\|HW]], [[FIRMWARE_ENGINEER_SKILL\|FW]], [[SECURITY_ENGINEER_SKILL\|SEC]], [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]], [[DATA_ENGINEER_SKILL\|DATA]], with [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] as designated validator | [[HARDWARE_ENGINEER_SKILL\|HW]], [[FIRMWARE_ENGINEER_SKILL\|FW]], [[SECURITY_ENGINEER_SKILL\|SEC]], [[BACKEND_CLOUD_ENGINEER_SKILL\|BACK]], [[DATA_ENGINEER_SKILL\|DATA]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]], [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]] | Markdown document in Git; references IEC 60812 (FMEA), IEC 61025 (FTA), and ISO/IEC 25010 (Reliability and Recoverability characteristics) | Semantic versioning (SemVer); major bump on failure domain addition or robustness NFR change; minor bump on pattern addition; reviewed at each Architecture Review Board milestone |
| OTA Model Artifact Contract | Authoritative end-to-end specification for model artifact flow through the OTA pipeline. Defines: (a) Artifact format at each hop: MLOps packaging format → DevOps distribution bundle → Firmware MCUboot-compatible image, with format conversion requirements at each boundary, (b) Signing chain: signing authority per stage (MLOps signs the model artifact, DevOps co-signs the distribution bundle, Firmware verifies the final image against the hardware root of trust), (c) Compatibility manifest: mandatory fields (model version, target hardware ID, firmware compatibility range, tensor arena size requirement, flash-budget check result), validated at each hop before forwarding, (d) Deployment-status reporting: required status codes at each hop (MLOps: REGISTERED → DevOps: DISTRIBUTING/DISTRIBUTED → Backend: DESIRED_SET → Firmware: DOWNLOADING/VERIFIED/APPLYING/ACTIVE/ROLLED_BACK/FAILED) with maximum latency per status transition, (e) Rollback coordination: sequence of events when any hop triggers a rollback (Backend sets desired state to previous version → DevOps halts distribution → Firmware applies rollback → MLOps updates model registry with rollback status), (f) End-to-end timeout: maximum time from MLOps registration to Firmware ACTIVE status (default: 24 hours for staged rollout, 1 hour for urgent hotfix). #ota-model-artifact-contract #model-ota #CR-3 | [[MLOPS_ENGINEER_SKILL\|MLOps]], [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]], [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]], [[FIRMWARE_ENGINEER_SKILL\|Firmware]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | Markdown document in Git; references the OTA Strategy Specification for artifact format details and the OTA artifact format defined in LR-7 | Semantic versioning (SemVer); major bump on protocol change, signing chain change, or new required manifest field; reviewed at each Architecture Review Board milestone; change requires ADR with all four OTA roles as consulted parties |
| System Scalability Contract | Authoritative cross-layer scalability specification defining: (a) Fleet-scale targets — initial deployment size ([N_initial] devices at launch), 12-month growth target ([N_12mo] devices), and 3-year ceiling ([N_3yr] devices) — the authoritative reference all per-service scaling limits must accommodate with ≥ 30% headroom; (b) Per-service scaling limits for each architectural layer — MQTT (Message Queuing Telemetry Transport) broker cluster (max concurrent connections, aggregate messages/sec throughput), Backend REST (Representational State Transfer) API (Application Programming Interface) services (requests/sec sustained, requests/sec burst, P95 latency under full fleet load), Data ingestion pipeline (write transactions/sec, commit latency P95), OTA (Over-the-Air) distribution pipeline (concurrent device download sessions, campaign deployment bandwidth); (c) Per-device resource budgets that enable fleet scaling without per-service limit renegotiation — maximum telemetry payload size per message (CBOR — Concise Binary Object Representation — encoded, bytes), maximum OTA firmware image size (MB), maximum OTA model update package size (KB), minimum MQTT connection keepalive interval (seconds, bounding per-broker keep-alive processing overhead at fleet scale); (d) Scalability NFRs (Non-Functional Requirements) S1–S5 with quantified targets and validation methods, referencing the NFR Verification Matrix; (e) Scaling triggers and capacity planning thresholds — for each per-service layer: utilization alert threshold at which oncall is notified (80% of limit), autoscaling trigger at which HPA (Horizontal Pod Autoscaler) activates (70% of limit sustained for ≥ 15 minutes), and the capacity provisioning SLA (≤ 10 minutes from trigger to capacity available); (f) Per-device budget ADR escalation rule — any per-device design decision that would breach a budget defined in (c) requires an ADR (Architecture Decision Record) with fleet-scale capacity impact analysis before shipment; (g) Scalability sign-off criteria for the production release gate. Co-signed by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]], [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]], [[DATA_ENGINEER_SKILL\|Data]], [[FIRMWARE_ENGINEER_SKILL\|Firmware]], [[MLOPS_ENGINEER_SKILL\|MLOps]], with [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] as designated validator. #system-scalability-contract #scalability #NFR #quality-attribute | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]], [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]], [[DATA_ENGINEER_SKILL\|Data]], [[FIRMWARE_ENGINEER_SKILL\|Firmware]], [[MLOPS_ENGINEER_SKILL\|MLOps]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]], [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]], [[BUSINESS_CONSULTANT_SKILL\|Business Consultant]] | Markdown document in Git; fleet-scale targets expressed with explicit units (device count, messages/sec, GB/day); per-service limits expressed with explicit units and ≥ 30% headroom requirement; references the OTA Model Artifact Contract for OTA-layer scaling limits and the NFR Verification Matrix (S1–S5) for scalability NFRs; references ISO/IEC 25010 Performance Efficiency and Scalability characteristics | Semantic versioning (SemVer); major bump on fleet-scale target change > 2× or a new scaling dimension added (new service layer or new per-device budget dimension); minor bump on limit revision within the existing fleet-scale envelope; reviewed at each Architecture Review Board (ARB) milestone and within 10 business days after any fleet-scale incident; change to fleet-scale ceiling requires ADR with all co-signing roles as consulted parties |

### 5.1 NFR Verification Matrix — All System Quality Categories

> **Status:** Fully instantiated — zero `[TBD]` values. Closes Critical Finding C-1 (Phase 2) and DEBT-R1 (Phase 4) from [[docs/review_v2/REVIEW_V2_SKILL_REPORT\|Review Part 2]]. A placeholder in any Target cell is a Planning-stage exit gate blocker. #NFR #nfr-instantiated

---

**NFR Category: Reliability** #NFR #reliability

| Sub-NFR ID | Requirement | Measurement Method | Target | Validation Owner | Sign-off Authority |
|---|---|---|---|---|---|
| **REL-1 — MTBF MCU-class** | Mean Time Between Failures for MCU-class field devices (STM32/ESP32-S3, battery/solar, outdoor) — hardware MTBF only; software failures addressed by REL-3 | Telcordia SR-332 Issue 3 Parts Count FIT summation at BOM freeze; IPC-SM-785 solder-joint thermal-cycling projection (-20 °C to +60 °C, ≈2 cycles/day); reviewed by [[HARDWARE_ENGINEER_SKILL\|Hardware]] before Development exit | ≥ **100,000 hours** (hardware MTBF; excludes battery consumable) | [[HARDWARE_ENGINEER_SKILL\|Hardware]] (FIT analysis); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (gate sign-off) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-2 — MTBF MPU-class** | Mean Time Between Failures for MPU-class gateways (RPi CM4/CM5, mains/solar, protected outdoor enclosure) — hardware MTBF only; software failures addressed by REL-4 | Telcordia SR-332 Issue 3 Parts Count FIT for carrier board (~100+ components); JEDEC JESD218A eMMC endurance analysis; fleet hardware-replacement rate from [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] telemetry | ≥ **70,000 hours** (hardware MTBF) | [[HARDWARE_ENGINEER_SKILL\|Hardware]] (FIT analysis); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (gate sign-off); [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (fleet telemetry) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-3 — Firmware uptime SLO MCU-class** | MCU firmware operational availability per device per month, excluding planned deep-sleep modes and OTA reboots ≤ 60 s | Fleet telemetry: expected vs. received reporting intervals per device-month; unplanned watchdog reset counter; verified by 30-day HIL soak on ≥ 10 representative devices | ≥ **99.5% per device-month** (≤ 3.6 h unplanned downtime) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (fleet observability); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (soak validation) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-4 — Firmware uptime SLO MPU-class** | MPU gateway system availability per device per month, excluding planned maintenance windows ≤ 4 h/quarter announced ≥ 72 h in advance | Fleet heartbeat monitoring at ≤ 60 s intervals; systemd/supervisor restart rate; unplanned kernel-panic reboot count; verified by 30-day soak on production-equivalent gateway hardware | ≥ **99.9% per device-month** (≤ 44 min unplanned downtime) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (gateway heartbeat monitoring); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (soak validation) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-5 — OTA update success rate** | Fleet-wide OTA firmware update success rate per update campaign | OTA pipeline telemetry: DOWNLOADING → ACTIVE completions vs. total attempts per campaign; rollback-triggered completions excluded from denominator | ≥ **99%** of update attempts fleet-wide | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-6 — OTA rollback success rate** | A/B slot OTA rollback must succeed on all hardware SKUs — a failed rollback bricks the field device | HIL fault injection: corrupt candidate firmware image slot on all supported hardware SKUs; verify device boots prior known-good slot; executed in every release OTA qualification gate | **100%** — zero exceptions permitted | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **REL-7 — Data ingestion integrity** | Joint Telemetry-Integrity SLO: telemetry samples must reach the time-series database without loss or bit-level corruption | End-to-end pipeline test: inject N timestamped samples at device MQTT publish → confirm DB writes → hash-based corruption check; measured by [[DATA_ENGINEER_SKILL\|Data]] pipeline monitoring and [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] soak | ≥ **99.9%** of expected samples per device-month | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; [[DATA_ENGINEER_SKILL\|Data]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |

---

**NFR Category: End-to-End System Robustness** #NFR #robustness

| Sub-NFR ID | Requirement | Measurement Method | Target | Validation Owner | Sign-off Authority |
|---|---|---|---|---|---|
| **R1 — Cross-Layer Failure Containment** | Any failure originating in one architectural layer (hardware, firmware, edge AI, communication, cloud, data) must not cause irreversible failure in any other layer. #failure-containment boundaries are defined in the #system-robustness-contract | Fault-injection at each layer boundary; measure (b) local containment latency via hardware timer; measure (c) cloud-detection latency via timestamped MQTT LWT delivery and backend alert; verify (d) adjacent-layer persistent-storage integrity post-injection; verify (e) all non-failing layers return to operational state without manual intervention | **(a)** Zero irreversible cross-layer failure propagation in all Critical/High #FMEA fault-injection runs; **(b)** local containment (watchdog/circuit-breaker activation) within ≤ **30 s** of fault onset; **(c)** cloud-layer fault detection (MQTT LWT + backend alert) within ≤ **90 s** of fault onset (1.5× MQTT keepalive interval of 30 s); **(d)** zero adjacent-layer persistent-storage corruption events in all test runs; **(e)** 100% of non-failing layers return to operational state without manual intervention | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **R2 — Graceful Degradation Under Partial Failure** | The system must continue to perform its 8 mandatory safety-critical and essential functions (enumerated in the Target) when any single architectural layer is operating in degraded mode | #graceful-degradation activation test: degrade each layer individually (hardware peripheral loss, firmware watchdog trip, edge AI inference timeout, MQTT connectivity loss, cloud service degradation, data pipeline backpressure) and verify all 8 function categories remain operational; 6 scenarios × 8 functions = 48 pass/fail assertions minimum | **100% of these 8 mandatory function categories operational under any single-layer degradation:** F1 — HW watchdog reset executes within ≤ 30 s of firmware deadlock (bootloader-enforced, application-independent); F2 — raw sensor sampling continues independently of edge-AI inference status (separate RTOS tasks); F3 — store-and-forward local buffering sustains ≥ 24 h of telemetry during cloud-connectivity loss; F4 — OTA A/B rollback executable from bootloader even if application firmware is unbootable; F5 — secure-boot firmware signature verification remains functional regardless of application failure; F6 — actuator assumes defined safe state within ≤ 100 ms of command-source failure (applies to products with actuators); F7 — device certificate and identity available and valid during partial software failure; F8 — device emits minimum "device degraded" status telemetry within ≤ 5 min of entering degraded mode; degraded-mode behavior for all 8 functions documented and tested | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **R3 — Cross-Layer Recovery Time** | After transient failure affecting ≥ 2 layers, the system must recover to full operational capability (all 8 R2 functions active + telemetry flowing end-to-end) within defined time bounds | End-to-end recovery time measurement: inject transient multi-layer fault → start timer on fault clearance → stop timer when all 8 R2 functions confirmed operational AND telemetry flows sensor-to-cloud-DB; measured via [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] observability stack (timestamped firmware reboot log to first post-recovery DB record); validated per FMEA failure chain | **By product class:** safety-critical products ≤ **30 s**; non-safety-critical products ≤ **300 s** (5 min). **By FMEA failure-chain class (more restrictive ceiling governs):** Critical chains ≤ **60 s**; High chains ≤ **300 s**; Medium chains ≤ **900 s** (15 min). For safety-critical products with Critical chains, the 30 s product-class ceiling governs. All Critical chains regardless of product class must recover within 60 s | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; measured via [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] observability stack | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **R4 — Failure Chain Detection Coverage** | ≥ 95% of failure chains identified in the system #FMEA must be detectable by the operational monitoring system within the recovery time window | Monitoring coverage audit: map each FMEA failure chain to an observability alert or detection rule; measure detection latency for each chain under fault injection | ≥ **95%** coverage of all FMEA failure chains; detection latency ≤ recovery time window for each chain | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (detection rules); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (coverage validation) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **R5 — Robustness Regression Coverage** | 100% of Critical and High-severity failure chains from the #FMEA must have automated regression tests in the QA test suite, executed per release | Automated test suite coverage audit: verify each Critical/High failure chain has at least one automated #fault-injection test case; validate pass/fail status per release | **100%** coverage of Critical and High-severity failure chains; any regression failure blocks the release | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] (production release gate sign-off) |

---

**NFR Category: Scalability** #NFR #scalability

| Sub-NFR ID | Requirement | Measurement Method | Target | Validation Owner | Sign-off Authority |
|---|---|---|---|---|---|
| **SCALE-1 — Fleet scale ceiling** | Architecture must support up to 50,000 concurrent active devices without topology redesign; all REL, PERF, and R1–R5 targets must hold under full load | End-to-end fleet load test in staging: simulate 50,000 concurrent MQTT connections with representative telemetry cadence (1 sample/5 min/device + 1 sample/s burst for 5% of fleet); orchestrated by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] using device simulators; verify all other NFR targets hold | ≥ **50,000** concurrent active devices without architectural redesign | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (load-test orchestration) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **SCALE-2 — MQTT broker concurrent connections** | MQTT broker cluster must sustain 50,000 concurrent persistent connections at production fleet ceiling | Broker load test: establish 50,000 concurrent MQTT connections (keep-alive 60 s, QoS-1) using emqtt-bench; sustain ≥ 30 min; measure PUBACK latency P99 and broker CPU/RSS | ≥ **50,000** concurrent persistent connections per broker cluster; PUBACK latency P99 ≤ 100 ms under full load | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **SCALE-3 — MQTT broker throughput** | MQTT broker must sustain aggregate message throughput covering OTA-campaign bursts and debug-mode telemetry across the full fleet | Sustained broker load test at 10,000 msgs/s for ≥ 30 min; measure per-message latency P99 and error rate; repeat during simulated OTA-campaign burst | ≥ **10,000 messages/second** aggregate sustained throughput; error rate ≤ 0.01% | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **SCALE-4 — Cloud REST API request rate** | Backend REST API must sustain routine fleet + dashboard load and absorb OTA/event-driven bursts | API load test (k6): 500 req/s sustained for 10 min then 2,000 req/s burst for 10 s; verify PERF-3 latency and error rate ≤ 0.1% throughout both phases | ≥ **500 req/s** sustained; ≥ **2,000 req/s** burst capacity (10 s window); P99 latency ≤ 200 ms (PERF-3) | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **SCALE-5 — Time-series DB write throughput** | Time-series database must sustain aggregate write rate including fleet-wide reconnect-flush burst after network partition | DB load test: sustain 50,000 writes/s for ≥ 10 min; verify P99 write latency and zero data loss; repeat with 24 h reconnect-flush burst scenario | ≥ **50,000 write transactions/second** aggregate; P99 write latency ≤ 10 ms; zero data loss | [[DATA_ENGINEER_SKILL\|Data]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **SCALE-6 — Concurrent OTA download sessions** | OTA distribution infrastructure must support 10% of fleet concurrently downloading firmware without degrading device telemetry | Simulated OTA campaign: trigger staged rollout to 5,000 devices simultaneously; measure CDN egress, per-device download completion time P99, and device telemetry continuity (must remain within REL-3/REL-4 uptime SLO during campaign) | ≥ **5,000** concurrent OTA firmware download sessions (= 10% of 50,000-device fleet) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |

---

**NFR Category: End-to-End System Scalability** #NFR #scalability #system-scalability-contract

| Sub-NFR ID | Requirement | Measurement Method | Target | Validation Owner | Sign-off Authority |
|---|---|---|---|---|---|
| **S1 — Fleet Scale Target** | The system architecture must be designed to support [N_initial] devices at launch, [N_12mo] devices within 12 months, and [N_3yr] devices as the 3-year fleet ceiling without architectural redesign. Every per-service scaling limit in the #system-scalability-contract must accommodate [N_3yr] with ≥ 30% headroom (i.e., limits are sized to [N_3yr] × 1.3). Fleet-scale targets are the authoritative planning inputs for all per-layer capacity decisions and are co-signed by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]], [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]], and [[DATA_ENGINEER_SKILL\|Data]] at Architecture Review Board (ARB) sign-off. Changes to fleet-scale targets > 2× require a major SemVer (Semantic Versioning) bump and an ADR (Architecture Decision Record) | Fleet-scale load simulation: simulate [N_12mo] × 2 concurrent devices using distributed device simulators orchestrated by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]]; verify all SCALE-series NFR targets are met under the simulated fleet load. Architecture ceiling review: confirm in the System Scalability Contract that per-service resource utilization at [N_12mo] device count does not exceed 70% of any per-layer scaling limit, preserving ≥ 30% headroom for growth to [N_3yr]; headroom verified from load-simulation observability metrics | All SCALE-series NFR targets pass at 2 × [N_12mo] simulated fleet size; per-service utilization at [N_12mo] does not exceed **70% of any per-layer scaling limit**; Architect confirms in writing that no architectural redesign is required to reach [N_3yr] | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (fleet-scale load simulation execution and SCALE-series NFR pass/fail); [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (simulator orchestration and per-service utilization reporting) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **S2 — Per-Layer Horizontal Scaling** | Every cloud service layer must scale horizontally by adding Kubernetes pod instances without manual operator intervention. Kubernetes HPA (Horizontal Pod Autoscaler) policies must be defined, deployed, and verified for all four service layers: (1) MQTT (Message Queuing Telemetry Transport) broker cluster, (2) Backend REST API services, (3) Data ingestion pipeline, (4) OTA (Over-the-Air) distribution pipeline. No single-instance bottleneck may exist in any layer at the fleet-scale ceiling | Progressive load test to 150% of each per-layer limit (75,000 concurrent MQTT connections, 750 req/s API load, 75,000 DB — Database — writes/s, 7,500 concurrent OTA sessions) using k6 and emqtt-bench; verify HPA autoscaling activates before the 100% limit is reached for each layer; verify all S4 SLOs are maintained throughout the scaling event (no SLO breach during a scale-out); measure trigger-to-capacity-available latency for each of the four layers | (1) MQTT broker cluster: autoscales to ≥ **50,000** concurrent persistent connections; PUBACK latency P99 ≤ **100 ms** maintained throughout scaling event; (2) Backend API services: autoscales to ≥ **500 req/s** sustained and ≥ **2,000 req/s** burst (10 s window); P99 latency ≤ **200 ms** maintained throughout; (3) Data ingestion pipeline: autoscales to ≥ **50,000** write transactions/sec; P99 write latency ≤ **10 ms**; zero message loss during scaling; (4) OTA pipeline: autoscales to ≥ **5,000** concurrent device download sessions; all four layers: trigger-to-capacity-available latency ≤ **10 minutes** | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (HPA configuration, trigger verification, and autoscaling latency measurement); [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]] (per-service scaling verification); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (progressive load test execution and SLO continuity certification) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **S3 — Per-Device Resource Budget for Fleet Scale** | Every per-device design decision that affects fleet-scale infrastructure capacity, broker connection overhead, or per-service load must have an explicit budget enforced at Development stage. The aggregate effect of per-device budgets × [N_3yr] fleet ceiling must not breach any per-service scaling limit defined in S2. Any per-device design decision that would breach a budget requires an ADR with fleet-scale capacity impact analysis before the feature ships — there are no silent budget exceedances | Budget conformance verified per device at every Development release build: [[FIRMWARE_ENGINEER_SKILL\|Firmware]] measures telemetry payload size at nominal reporting interval using wire-capture on HIL (Hardware-in-the-Loop) rig; OTA image size recorded from the CI (Continuous Integration) build artifact at every release build; MQTT keepalive interval confirmed from firmware MQTT connection configuration. Fleet-scale cost and capacity impact calculated by [[BUSINESS_CONSULTANT_SKILL\|Business Consultant]] at Planning stage using actual per-device budgets × [N_3yr] ceiling | Telemetry payload size: ≤ **256 bytes** per message at nominal reporting interval (CBOR — Concise Binary Object Representation — encoded); OTA firmware update image: ≤ **2 MB** per package (MCUboot — Microcontroller Bootloader — compatible binary, compressed); OTA model update package: ≤ **512 KB**; MQTT connection keepalive interval: ≥ **30 seconds** minimum (bounding per-broker keep-alive processing overhead at fleet scale); any budget exceedance without a closed ADR blocks Development exit and production release | [[FIRMWARE_ENGINEER_SKILL\|Firmware]] (per-device budget measurement at every release build); [[BUSINESS_CONSULTANT_SKILL\|Business Consultant]] (fleet-scale cost and capacity impact analysis at Planning); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (budget conformance gate — block shipment on any unclosed budget ADR) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **S4 — Scalability SLOs Under Fleet Load** | At 100% of the 12-month fleet-scale target ([N_12mo] devices), the system must maintain all five SLOs (Service Level Objectives) concurrently for ≥ 24 continuous hours without degradation, including during autoscaling events triggered under S2. SLO degradation under fleet load — even transient — constitutes a scalability failure and blocks the production release. The load profile must include steady-state telemetry (nominal reporting intervals for all [N_12mo] devices), a burst scenario (5% of fleet in high-frequency debug mode, 1-hour windows), and a concurrent OTA campaign (10% of fleet simultaneously downloading firmware per SCALE-6) | Sustained load test at 100% of [N_12mo] fleet-scale target for ≥ 24 continuous hours; all five SLO metrics measured via the [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] observability stack (Grafana/Prometheus) at 1-minute resolution; any SLO breach reported regardless of duration; test covers steady-state, burst, and concurrent OTA campaign load profiles; executed and certified by [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] against the System Scalability Contract | (1) MQTT message delivery latency (device PUBLISH → broker PUBACK): **P95 ≤ 100 ms**; (2) Backend REST API response latency: **P95 ≤ 200 ms** (API Gateway ingress to response egress, excluding client network transit); (3) End-to-end telemetry latency (device PUBLISH → dashboard display): **P95 ≤ 3,000 ms**; (4) Data ingestion commit latency (message received by pipeline → written to time-series DB): **P95 ≤ 10 ms**; (5) OTA campaign completion rate: **≥ 99%** of update attempts fleet-wide within the 24-hour end-to-end timeout; all five SLOs must hold concurrently throughout the full 24-hour window, including during any S2 autoscaling events | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (24-hour sustained load test execution and all five SLO measurements); [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (observability stack instrumentation for all five SLO metrics at 1-minute resolution) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **S5 — Capacity Planning and Scaling Trigger** | For every per-service scaling limit in S2, three properties must be defined, deployed as live monitoring rules, and verified by a capacity exhaustion drill before production release: (a) an alert threshold (80% of limit) at which oncall is notified, (b) an autoscaling trigger (70% of limit sustained ≥ 15 minutes) at which HPA activates, and (c) a capacity provisioning SLA (≤ 10 minutes from HPA trigger to new capacity available). Capacity planning must ensure that the time from trigger to limit — at the projected fleet growth rate — always exceeds the provisioning SLA. Applies to all four S2 service layers | Capacity exhaustion drill for each of the four S2 service layers (MQTT broker, Backend API, Data ingestion, OTA pipeline): ramp load to 80% of per-layer limit → verify alert fires within ≤ 5 minutes → continue ramp to 70% sustained for 15 minutes → verify HPA activates → continue ramp → verify new capacity is available before the 100% limit is reached; measure trigger-to-capacity-available latency; executed by [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; alert rules and HPA policies owned and pre-validated by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] | (1) Alert threshold: monitoring alert fires when any S2 layer reaches **80% of its per-layer scaling limit**; alert notification latency ≤ **5 minutes** of threshold breach; (2) Autoscaling trigger: HPA activates when utilization exceeds **70% of per-layer limit** for ≥ **15 consecutive minutes**; (3) Provisioning SLA: new capacity available within ≤ **10 minutes** of HPA trigger for all four S2 layers; (4) Zero capacity exhaustion events in all drills: no layer reaches 100% of its per-layer scaling limit without prior alert and HPA activation; **100% coverage of all four S2 layers** required for production release gate | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (alert rule and HPA policy configuration and pre-validation); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (capacity exhaustion drill execution and certification for all four layers) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |

---

**NFR Category: Performance** #NFR #performance

| Sub-NFR ID | Requirement | Measurement Method | Target | Validation Owner | Sign-off Authority |
|---|---|---|---|---|---|
| **PERF-1 — Standard telemetry end-to-end latency** | Standard telemetry must flow from device MQTT publish to cloud database write to dashboard display within the monitoring refresh budget | End-to-end latency probe: device publishes timestamped sample → measure Δ to dashboard-served data; P99 over 30-day window under nominal and 50% load; instrumented by [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] observability | ≤ **3,000 ms P99** (device publish → dashboard display) | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] (observability instrumentation) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **PERF-2 — Alert/alarm telemetry latency** | Alert-class telemetry must reach dashboard notification within operator-response time budget | Same instrumentation as PERF-1 scoped to alert-class MQTT topics (QoS-2, dedicated alert topic); ≥ 1,000 synthetic alert injections/day during 30-day soak | ≤ **500 ms P99** (device alert publish → dashboard notification) | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **PERF-3 — Cloud REST API response latency** | Backend REST API must respond within interactive UI latency budget at sustained load | API latency test (k6): measure P50/P95/P99 from API Gateway ingress to response egress under 500 req/s sustained; all primary endpoints individually | ≤ **200 ms P99** (API Gateway ingress to response egress, excluding client network transit) | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend]]; [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **PERF-4 — MCU-class on-device inference latency** | MCU firmware must complete one TinyML inference cycle within the RTOS scheduling budget to leave ≥ 50% CPU for comms and sensing | On-target measurement: [[FIRMWARE_ENGINEER_SKILL\|Firmware]] instruments inference start/end with DWT cycle counter on production MCU at rated clock under peak thermal load; P99 over ≥ 1,000 cycles; re-verified on model change > 10% parameter delta | ≤ **100 ms** per inference cycle (wall-clock, input tensor populated → output tensor available) | [[FIRMWARE_ENGINEER_SKILL\|Firmware]] (on-target measurement); [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML]] (model compliance); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (gate sign-off) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| **PERF-5 — MPU-class gateway inference latency** | Gateway must complete one ONNX Runtime inference cycle at nominal CPU load within the edge-processing pipeline budget | On-target benchmark: [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML]] runs ONNX Runtime inference on production RPi CM4 at 50% aggregate CPU load; P99 over ≥ 1,000 cycles; re-verified on model change | ≤ **50 ms** per inference cycle (wall-clock, Python/ONNX Runtime, input prepared → output available) | [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML]] (benchmark); [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]] (gate sign-off) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |

---

**Validation method (summary — all four categories):** Reliability: Telcordia SR-332 FIT analysis at BOM freeze (REL-1/2); 30-day HIL soak for uptime SLOs (REL-3/4); OTA campaign telemetry and HIL fault-injection for OTA targets (REL-5/6); end-to-end pipeline hash-check for ingestion integrity (REL-7). Robustness: #FMEA worksheet with measured #RPN values; fault-injection test results per failure chain with R1 containment-latency measurements (local ≤ 30 s, cloud ≤ 90 s); R2 degraded-mode matrix (6 scenarios × 8 functions); R3 recovery-time measurements per failure class and product class; monitoring coverage audit (R4); regression suite pass/fail (R5). Scalability: device-simulator fleet load tests at 50,000 concurrent connections for SCALE-1/2/3; k6/Locust API load tests for SCALE-4; DB write-load tests for SCALE-5; staged OTA simulation for SCALE-6. End-to-End System Scalability: fleet-scale load simulation at 2× the 12-month target with per-service utilization verification for S1; progressive per-layer load tests to 150% of S2 limits with HPA trigger and SLO continuity verification for S2; per-device budget conformance audit at every release build for S3; 24-hour sustained load test at 100% 12-month fleet target measuring all five SLOs concurrently for S4; capacity exhaustion drills for all four S2 service layers verifying alert, trigger, and provisioning SLA for S5. Performance: 30-day end-to-end latency probes for PERF-1/2; API latency tests for PERF-3; on-target DWT cycle-counter measurements for PERF-4/5. All categories validated by [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA]]; signed off by **Architect** at the production release gate. Zero `[TBD]` values are permitted in this matrix at any lifecycle stage past Planning.

---

## 6. Interface Contracts

> For each collaborator: **Provides** (what the Architect supplies), **Requires** (what the Architect needs back), **Cadence** (synchronization points).

### 6.1 Product Owner / TPM

- **Provides:** Technical feasibility assessments, resource/time-cost implications of requirements, risk and dependency surfacing, and release-gate architecture readiness.
- **Requires:** Prioritized product and field requirements, target deployment context (environment, scale, connectivity), and constraints (budget, certification, timeline).
- **Cadence:** Requirement-intake sessions; sprint planning; release-gate reviews; ad hoc trade-off escalations.

### 6.2 Hardware Engineer

- **Provides:** Platform selection rationale, per-node resource and power budgets, sensor-bus topology, and debug/security-element requirements (e.g., debug-port lockdown).
- **Requires:** Board feasibility confirmation, electrical constraints, sensor specifications (sampling rate, resolution), and bring-up findings/errata.
- **Cadence:** Platform-selection trade study; schematic review; board bring-up; errata triage.

### 6.3 Firmware Engineer

- **Provides:** HAL boundary definition, RTOS selection, interface contracts, message schemas, OTA strategy, and real-time/power budgets.
- **Requires:** Contract-conformance feedback, measured resource usage (Flash/SRAM, current), timing measurements, and feasibility flags on the proposed abstraction.
- **Cadence:** Contract handoff at planning; conformance reviews during development; integration checkpoints; ADR consultation on contract changes.

### 6.4 Edge AI/ML Engineer

- **Provides:** Tensor-arena and footprint budget, latency/throughput deadline, target operator-support constraints, and the edge-vs-cloud inference split.
- **Requires:** Actual model footprint and on-target latency, operator-coverage gaps, and accuracy-vs-resource trade-offs.
- **Cadence:** Budget definition at planning; arena-sizing validation as models mature; pre-integration latency sign-off.

### 6.5 MLOps Engineer

- **Provides:** OTA constraints for model artifacts, model-delivery/versioning expectations, and the edge target profile for packaging.
- **Requires:** Model artifact format and size, deployment/rollback mechanism feasibility, and drift-monitoring telemetry needs.
- **Cadence:** OTA strategy alignment at planning; model-delivery integration during development; release-gate review.

### 6.6 Data Engineer

- **Provides:** Telemetry schema, data-flow topology, sampling/payload budgets, and edge-buffering behavior.
- **Requires:** Ingestion feasibility, schema-evolution constraints, and storage/throughput limits that may feed back into payload design.
- **Cadence:** Schema definition at planning; pipeline-integration checkpoints; schema-change ADR reviews.

### 6.7 DevOps/Platform Engineer

- **Provides:** OTA strategy (A/B, signing, rollback), gateway-orchestration approach (K3s/balena), and build/toolchain constraints.
- **Requires:** Pipeline and fleet-management feasibility, artifact-signing mechanism, and observability hooks.
- **Cadence:** OTA and fleet-strategy alignment at planning; CI/CD integration during development; production-scaling review.

### 6.8 Backend/Cloud Engineer

- **Provides:** Edge–cloud interface contracts, MQTT broker topology and QoS, device shadow/twin model, and identity/provisioning topology.
- **Requires:** API/broker feasibility, scaling limits, and device-management constraints that may reshape the contract.
- **Cadence:** Contract handoff at planning; integration checkpoints; fleet-scaling review at production-ready.

### 6.9 Frontend/Dashboard Engineer

- **Provides:** Data/event contracts for visualization, real-time stream topology (e.g., MQTT-over-WebSockets), and the semantics of inference outputs to be displayed.
- **Requires:** UX-driven data needs and feedback on contract gaps for monitoring/alerting.
- **Cadence:** Contract definition at planning; integration checkpoints; alert-semantics review.

### 6.10 QA & Test Automation Engineer

- **Provides:** NFR targets (latency, power, OTA reliability), interface contracts as the basis for conformance tests, and the requirements-traceability map.
- **Requires:** Measured verification results, contract-violation reports, and integration-defect analysis.
- **Cadence:** NFR matrix handoff at planning; HIL (Hardware-in-the-Loop) and end-to-end validation during execution; release-gate sign-off.

### 6.11 Security Engineer

- **Provides:** Architecture surfaces for threat modeling and the requirement to embed secure boot, mTLS, and a root of trust.
- **Requires:** Security baseline definition, threat-model findings, hardening requirements, and PKI (Public Key Infrastructure)/identity design — co-owned.
- **Cadence:** Joint security-baseline authoring at planning; security architecture reviews; pre-production hardening sign-off.

### 6.12 [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|IoT & Embedded Systems Researcher]]

- **Provides:** Long-term architecture roadmap — platform evolution direction, planned protocol/technology shifts, and the technology-horizon challenges and architectural constraints that seed and shape research direction (presented annually, first Tuesday of March); engineering feasibility feedback on research findings — whether a discovery can be productized within current or planned architecture, including identified gaps and required architecture changes, raised during PoC (Proof-of-Concept) review; system-level constraints for experimental design — resource budgets (power, form factor, communication bandwidth, latency, cost target) and target hardware profiles the Researcher should design experiments against for eventual technology transfer; ADR (Architecture Decision Record) notifications with research implications within 5 business days of acceptance; and facilitation of the quarterly Technology Transfer Review (chairing, ensuring all relevant engineering roles are represented and feasibility assessments are delivered ≥1 week before the meeting).
- **Requires:** Technology Transfer Packs — complete research-finding documentation (scientific rationale, experimental validation, known limitations, preliminary architecture-impact assessment) submitted ≥3 weeks before the quarterly Technology Transfer Review; Feasibility Assessment Reports for novel sensing, communication, or computation paradigms assessing whether a candidate technology can meet system-level constraints; PoC demonstrations with characterized performance metrics sufficient to assess integration complexity and architecture compatibility; and on-demand scientific consultation on novel material or physics choices that affect architecture decisions (response within 5 business days).
- **Cadence:** Scheduled Technology Transfer Review — quarterly, first Tuesday of February, May, August, November; Researcher submits the Technology Transfer Pack ≥3 weeks before, Architect provides written feasibility assessment ≥1 week before, 60-minute review meeting. Interim Technology Transfer — for time-sensitive findings (market window <3 months or patent filing deadline), Architect acknowledges within 3 business days and schedules within 10 business days, limited to 2 interim reviews per quarter. Long-term Architecture Roadmap Briefing — Architect presents annually, first Tuesday of March; Researcher provides research-direction feedback within 2 weeks. System-level constraint update — Architect notifies the Researcher within 5 business days of ADR acceptance; Researcher provides impact assessment on active research within 15 business days. Ad hoc scientific consultation — 5 business days' notice, limited to 4 hours/month; urgent (production incident requiring scientific expertise) within 1 business day. #research-interface #technology-transfer #HR-1

### 6.13 [[BUSINESS_CONSULTANT_SKILL|Business Consultant]]

- **Provides:** ADRs (Architecture Decision Records) with quantified cost and timeline implications; BOM (Bill of Materials) cost estimates and NRE (Non-Recurring Engineering) cost estimates per architecture option; assessment of the technical feasibility of market-driven feature requests; and lead-time estimates for hardware development milestones.
- **Requires:** Market requirements translated into system-level constraints (target BOM cost range, connectivity-protocol business rationale, certification requirements); business framing of architectural trade-off options (cost/risk/time analysis, e.g., edge vs. cloud compute); and the investment case for architectural decisions requiring significant NRE.
- **Cadence:** Monthly Business-Architecture Alignment — second Tuesday of each month, 60 minutes #cadence #business-architecture #interface-contract; the **Architect** presents architecture decisions with significant cost/timeline implications, platform-selection trade-offs relevant to business strategy, and technical-feasibility findings affecting market commitments, while the [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] presents updated BOM cost constraints, market-window shifts, competitive technical intelligence, and business-driven feature-prioritization changes. Business Impact Assessment of ADRs — when the Architect files an ADR tagged #business-impact, the Architect notifies the Business Consultant within 3 business days of ADR acceptance #synchronization, and the Business Consultant returns the Business Impact Assessment (quantified cost impact, market-window risk, competitive-positioning impact) within 10 business days, appended to the ADR via the business-impact appendix defined in §7. Business Constraint Change Notification — on a confirmed business-constraint change (BOM ceiling revision >10%, market-window acceleration >1 month, certification-path regulatory change, or new competitive threat requiring an architecture response), the Business Consultant notifies the Architect within 2 business days and the Architect returns a technical impact assessment within 10 business days #synchronization. Pre-Planning Business Input — the Architect receives the business-constraints package (BOM ceiling per product, target price point, market-window dates, volume forecasts) ≥2 weeks before the start of each Planning stage for a new product or major revision. Quarterly Technology-Business Strategy Session — first Thursday of January, April, July, October, 90 minutes. Annual Architecture Investment Review — first Tuesday of December, half-day. #business-interface #HR-2

---

## 7. Decision Authority & Governance

**Decisions owned unilaterally (recorded as ADRs):**

- MCU/SoC platform selection and node-class workload partitioning.
- Application protocol, QoS, and transport selection.
- Interface contracts, HAL boundaries, and message/payload schemas.
- RTOS selection and per-node resource budgets.
- OTA update strategy (A/B partitioning, signing policy, rollback).

**Decisions requiring consensus:**

- Security baseline and PKI/identity design — with the Security Engineer.
- Model footprint/latency budget — with the Edge AI/ML Engineer.
- Board feasibility and platform viability — with the Hardware Engineer.
- Cloud interface and broker-scaling limits — with the Backend/Cloud Engineer.
- Production release gate — with the TPM and QA & Test Automation Engineer.

**Escalation path:** Architect → TPM → CTO/Engineering Lead. Cross-team interface deadlocks that cannot be resolved by ADR are escalated to an Architecture Review Board (Architect + affected leads + TPM).

**ADR process:**

- **Trigger:** Any decision affecting platform, protocol, interface, resource budget, OTA, or security baseline.
- **Template fields:** Title; Status; Context; Decision; Consequences; Business Impact (if tagged #business-impact); Alternatives Considered; Related ADRs.
- **Business Impact (if tagged #business-impact):** For ADRs (Architecture Decision Records) with significant cost, schedule, or market-window implications. This appendix is authored by the [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] per the Business-Architecture Alignment cadence (§6.2). Fields: (a) Quantified Cost Impact — one-time NRE (Non-Recurring Engineering), per-unit BOM (Bill of Materials) delta, annual cloud OpEx (Operational Expenditure) delta, (b) Schedule Impact — market window shift in weeks, competitive milestone risk, (c) Market Impact — competitive positioning effect, customer commitment risk, pricing implication, (d) Recommendation — Proceed / Proceed with Mitigation / Escalate to Executive Review — with business rationale. The Business Impact appendix is appended to the ADR within 10 business days of the Architect's notification.
- **Status lifecycle:** Proposed → Accepted → (Superseded | Deprecated). ADRs are append-only and immutable once Accepted; changes are made by superseding with a new ADR.
- **Review/merge:** Authored as Markdown, reviewed via pull request, and merged only after the required approvers (per decision class above) sign off. Each ADR is linked from the SAD and from any contract it governs.

### 7.Z Architecture Review Board (ARB) Charter

The Architecture Review Board (ARB) is a standing governance body that provides distributed architectural decision-making capacity, reducing the Architect as a single point of failure and enabling faster resolution of routine architectural questions. The ARB was established during CR-1 (Critical Remediation 1) with limited caretaker authority. This charter has been expanded under a Phase 5 Long-Term Bet (LTB) to distribute additional decision classes — transforming the ARB from a caretaker body into a genuine collective governance institution and providing the primary structural mitigation for EN-1 (Emergent Property 1: Architect Singularity) identified in [[docs/review_v2/REVIEW_V2_SKILL_REPORT|Review Part 2]]. The Architect remains the Chair and retains sole authority over the five reserved decision classes listed in the Decision Limits section. #architect-singularity #distributed-governance

**ARB Membership:**
- **Standing Members:** Embedded Systems Architect (Chair), Deputy Architect (Vice Chair), Senior [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]], Senior [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud Engineer]], [[SECURITY_ENGINEER_SKILL|Security Engineer]]
- **Rotating Members:** One additional Senior Engineer from the role most affected by the current release scope, rotating per release cycle. Invited by the Chair
- **Quorum:** 3 of 5 standing members, including at least one of the Architect or Deputy Architect

**ARB Decision Authority (majority vote of quorum):**

*Original authority — established CR-1:*
- Resolve Tier 2 (HIGH) architecture decisions escalated from the Decision SLA (Service Level Agreement) queue
- Approve non-breaking ADRs (Architecture Decision Records) — ADRs that do not change a platform selection, protocol choice, resource budget, security baseline, or OTA (Over-the-Air) strategy (same criteria as Deputy Architect authority)
- Resolve CCRs (Contract Clarification Records) escalated from consumer/producer pairs when consensus is not reached within 3 business days
- Approve routine budget rebalancing within defined tolerance bands (see §2 Budget Trade Tolerance Bands) when the implementing role requests ARB validation
- Review and approve architecture implications of technology transfer from [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]] when the finding does not introduce novel platform, protocol, or security surface requirements
- Authorize architecture exploration spikes and technology evaluations

*Expanded authority — Phase 5 Long-Term Bet:* #expanded-authority #long-term-bet

1. **Contract evolution — MINOR and PATCH version changes (NEW — Long-Term Bet):** The ARB may approve MINOR and PATCH version changes to interface contracts under SemVer (Semantic Versioning) without Architect approval. MINOR changes are defined as additive-only field additions that do not break existing consumers. PATCH changes are defined as schema clarifications, tolerance tightening within existing budgets, and documentation corrections. The ARB votes by quorum majority and issues an ARB Decision Record (ADR) cross-referenced from the affected contract's ADR. MAJOR version changes — breaking changes, new contracts, and deprecated contracts — are not delegated and continue to require Architect approval plus a new or superseding ADR with all affected consumer roles as consulted parties. This is the highest-volume architectural decision class and the primary operational relief mechanism for EN-1. #expanded-authority #contract-evolution

2. **Resource budget rebalancing up to 2× tolerance band (NEW — Long-Term Bet):** The ARB may approve Flash↔SRAM (Flash memory to Static Random-Access Memory) trades between 1× and 2× the pre-authorized tolerance band — nominally between ±5% and ±10% of the baseline budget — with a quorum majority vote. Before the vote is held, the requesting role must provide a verified post-rebalancing headroom calculation demonstrating ≥15% remaining Flash and SRAM margin. The ARB issues an ARB Decision Record stating the justification, the delta, and the verified headroom margin. Trades within 1× tolerance (≤±5%) remain pre-authorized and require no ARB vote. Trades beyond 2× tolerance (>±10%) are not delegated and require Architect approval plus an ADR with full resource-budget impact analysis. #expanded-authority #resource-budget

3. **Non-novel technology evaluation and adoption (NEW — Long-Term Bet):** The ARB may authorize the evaluation and adoption of non-novel technologies without Architect approval. Non-novel technologies are explicitly defined as: a new version of an already-approved library or dependency; a new CI/CD (Continuous Integration / Continuous Deployment) tool that does not modify the OTA pipeline, the signing chain, or the artifact format; new monitoring or observability dashboard tooling with no protocol or security surface change; and minor dependency upgrades that meet the same security baseline requirements as the dependency being replaced. The ARB issues an ARB Decision Record specifying the technology change, the rationale, and the security and architecture impact assessment signed by the [[SECURITY_ENGINEER_SKILL|Security Engineer]] standing member. Novel technologies — defined as a new communication protocol, a new architectural pattern not previously approved, a new platform component, or any technology that introduces a new security surface — are not delegated and continue to require Architect approval plus an ADR. #expanded-authority #technology-evaluation

4. **Sustaining Engineering backlog prioritization (NEW — Long-Term Bet):** The ARB may prioritize SE (Sustaining Engineering) backlog items — field fixes, minor reliability enhancements, and incremental operational improvements — without Architect approval. SE items are eligible for ARB prioritization only when all four of the following conditions are met: (a) no interface contract schema is changed, (b) the OTA strategy is not modified, (c) the security baseline is not touched, and (d) the item is scoped within existing resource budgets. The ARB issues a prioritization record per SE cycle. New feature development, product roadmap changes, and any SE item that fails any of the four eligibility conditions are not delegated and continue to require PO/TPM (Product Owner / Technical Project Manager) and Architect alignment before backlog entry. #expanded-authority #sustaining-engineering

5. **Agent-proposed optimizations — Human-Supervised and Human-Governed phases only (NEW — Long-Term Bet):** In the Human-Supervised Autonomy and Human-Governed Autonomy phases of the Phase 3 AI agent transformation roadmap, AI agents may submit optimization proposals to the ARB as formal ARB Agenda Items. The ARB may approve agent-proposed optimizations without Architect approval when all of the following scoping conditions are met: (a) contract optimizations that constitute MINOR or PATCH version changes (governed by item 1 above), (b) resource budget adjustments within 2× tolerance bands (governed by item 2 above), and (c) process improvements to ARB operations, engineering tooling, or Sustaining Engineering workflows (governed by item 4 above). Agent proposals are advisory and non-binding; the ARB retains full discretion to reject, modify, or escalate any proposal regardless of agent confidence. Agent-proposed changes that involve any security baseline modification, OTA strategy change, platform architecture change, or MAJOR contract change are not delegated and must be escalated to the Architect regardless of autonomy phase. This authority is explicitly scoped to Human-Supervised and Human-Governed phases and does not apply in Human-in-the-Loop or Fully Autonomous phases. #expanded-authority #agent-governance #human-governed-autonomy

**ARB Decision Limits (NOT authorized — requires Architect approval; ADR required where noted):**

The following decision classes are reserved for the Architect and are explicitly NOT delegated by the expanded ARB authority established in this Phase 5 charter. These limits hold regardless of quorum, vote margin, or autonomy phase:

- **Platform/MCU (Microcontroller Unit)/SoC (System on Chip) selection and deprecation** — requires Architect + ADR; affects every downstream layer and cannot be reversed without major rework
- **Protocol or communication topology changes** — requires Architect + ADR; any protocol or topology change has cross-layer security, OTA, and scalability consequences that exceed ARB scope
- **MAJOR contract version changes** (breaking changes, new contracts, deprecated contracts) — requires Architect + ADR with all affected consumer roles as consulted parties; breaking changes impose coordinated migration cost across all consumers
- **Resource budget creation, deletion, or rebalancing beyond 2× the pre-authorized tolerance band** (>±10%) — requires Architect + ADR with full resource-budget impact analysis; changes of this magnitude may invalidate NFR (Non-Functional Requirement) targets
- **OTA (Over-the-Air) strategy changes** — requires Architect + ADR; OTA strategy is a cross-layer governance artifact owned by the Architect per §2 and §5
- **Security baseline modifications** — requires Architect + [[SECURITY_ENGINEER_SKILL|Security Engineer]] co-approval + ADR tagged #security-impact; security baseline is co-owned and cannot be weakened by majority vote
- **Production release gate architecture sign-off** — reserved for Architect; non-delegable regardless of Deputy availability or ARB quorum
- **Any decision affecting a safety-critical path** — requires Architect review before any ARB vote proceeds, regardless of the apparent decision class; the Architect has standing to halt an ARB vote on safety-critical grounds at any time
- **Novel technology adoption** (new protocol, new platform component, new architectural pattern, any technology introducing a new security surface) — requires Architect + ADR; novelty determination is at the Architect's discretion when disputed

**ARB Operations:**
- **Regular Meeting:** Bi-weekly, 60 minutes. Standing agenda: open Tier 2 decisions; escalated CCRs; ADR review queue; expanded-authority decision queue (contract MINOR/PATCH changes, non-novel technology evaluations, SE prioritization, agent proposals); cross-role architecture concerns; upcoming technology transfer assessments
- **Urgent Meeting:** Convened within 1 business day by the Chair or Vice Chair for Tier 1 (CRITICAL) decisions when the Architect is unavailable
- **Decision Record:** All ARB decisions are documented as ARB Decision Records in the same Markdown format as ADRs, tagged #ARB. ARB decisions that would normally require an ADR are cross-referenced from the ADR repository. Decisions made under expanded authority are additionally tagged #expanded-authority to provide a clear audit trail for Phase 5 governance review
- **Escalation:** Any standing member may escalate any ARB decision to the Architect for review within 5 business days of the decision. The Architect may uphold, modify, or reverse the ARB decision via a superseding ADR. The [[SECURITY_ENGINEER_SKILL|Security Engineer]] standing member has additional standing to escalate any decision with an undisclosed security surface to the Architect within 1 business day
- **Annual Review:** The ARB charter is reviewed annually at the first ARB meeting of December. Membership, authority scope, and operations are updated as the organization matures and as the Phase 5 Long-Term Bets are assessed. Expanded authority items are evaluated for permanence or rollback based on decision quality and audit trail evidence
#ARB #distributed-governance #expanded-authority #long-term-bet #architect-singularity

---

## 8. Standards & Best Practices

- **Architecture documentation:** C4 model and SysML for views; doc-as-code in Git; one ADR per significant decision; every interface captured as a versioned contract.
- **Software product quality:** ISO/IEC 25010 quality characteristics (reliability, performance efficiency, maintainability, security, portability) used as the architecture-evaluation framework.
- **Firmware coding standards (enforced via contract, not implementation):** MISRA C:2012 and CERT C as mandated baselines for safety-relevant firmware.
- **Security:** OWASP IoT Top 10 as the threat checklist; mandatory secure boot, signed firmware, mTLS for device transport, and a hardware root of trust; align with NIST IoT device guidance where applicable.
- **Reliability & safety:** A/B OTA with guaranteed rollback; hardware/software watchdogs; fail-safe default states; awareness of IEC 61508 functional-safety concepts where the deployment demands it.
- **System-level robustness modeling:** #FMEA (Failure Mode and Effects Analysis) per IEC 60812 conducted at system level for all cross-layer failure chains. Minimum scope: all failure chains crossing ≥2 architectural layers (e.g., hardware → firmware, firmware → cloud, cloud → data, data → ML). Each failure chain assessed for severity (system-level impact), occurrence (probability given field conditions), and detectability (by existing monitoring). Failure chains with #RPN (Risk Priority Number, calculated as Severity × Occurrence × Detectability) above the organizational threshold require documented design-time mitigation in the #system-robustness-contract. #FTA (Fault Tree Analysis) per IEC 61025 used for top-level undesirable events (e.g., "device unresponsive in field," "incorrect actuator command executed"). FMEA/FTA updated at each major architecture revision and reviewed at the Architecture Review Board. Methodology, worksheets, and results stored alongside the System Robustness Contract in version control. #robustness #cross-layer-failure
- **Interface evolution:** Semantic versioning of all contracts and schemas; additive-only changes for minor versions; breaking changes require a major bump, an ADR, and explicit consumer notification.
- **Resource discipline:** Every budget expressed in explicit units (KB, ms, mW); a minimum headroom margin maintained on Flash/SRAM at release.

---

## 9. AI Agent Execution Guide

> This section instructs an AI agent (e.g., Claude Code) acting as the Embedded Systems Architect. The agent specifies constraints and contracts; it does not write code owned by other roles.

### 9.1 Agent Persona & Tone

- Formal, precise, and evidence-based. Reason explicitly from constraints (memory, power, latency, bandwidth, security) and state the numbers.
- Decide from trade studies, not preference; justify every architectural choice and record it as an ADR.
- Defer all implementation detail to the owning role; deliver the contract or constraint, never the line-level solution.
- Produce machine-parseable artifacts: explicit tables, versioned schemas, and renderable diagrams (Mermaid/C4).
- Surface assumptions and risks rather than silently resolving ambiguity; if a budget or requirement is missing, request it before designing.

### 9.2 Mandatory Pre-Delivery Checklist

Before emitting any architecture artifact, the agent MUST confirm all of the following:

1. Target platform(s) are explicitly named (MCU/SoC plus gateway class).
2. Resource budgets are quantified with units — Flash/SRAM/PSRAM (KB/MB), power (mW/mWh), and the latency deadline (ms). No vague terms.
3. Protocol, QoS level, transport, and offline/fallback behavior are all specified.
4. Each interface contract is versioned, and its schema is defined (Protocol Buffers / CBOR).
5. If the artifact affects firmware, the OTA path (A/B + rollback) is addressed.
6. The security baseline (secure boot, mTLS, device identity) is referenced and not weakened.
7. Every significant decision has a corresponding ADR (existing or newly drafted).
8. Consumers (downstream roles) are identified for each deliverable.
9. No implementation detail owned by another role is being dictated — only the contract/constraint.
10. All acronyms are defined on first use and all quantities carry explicit units.
11. Requirement-to-architecture traceability is stated (which requirement this choice satisfies).
12. Any diagram renders correctly and matches the textual description.

### 9.3 Forbidden Actions

- Do NOT introduce a platform, protocol, or technology outside the approved stack without a trade study and an ADR.
- Do NOT emit line-level firmware, driver, cloud-API, or dashboard code (owned by Firmware/Backend/Frontend).
- Do NOT design, train, or choose layers for ML models; set only the footprint/latency envelope (owned by Edge AI/ML).
- Do NOT produce schematics or PCB layout (owned by Hardware).
- Do NOT output any budget, deadline, or requirement as "TBD" or otherwise unquantified.
- Do NOT alter an Accepted interface contract without a superseding ADR, a version bump, and consumer notification.
- Do NOT omit or weaken the security baseline, or assume an unencrypted/unauthenticated channel is acceptable.
- Do NOT assume unlimited memory, power, or bandwidth.
- Do NOT deliver an architecture without identifying consumers and synchronization points.

### 9.4 Prompt Templates for Common Tasks

**Template A — Platform Selection Trade Study**

```
Role: Embedded Systems Architect.
Goal: Select the MCU/SoC for [node name] running [workload, incl. any on-device inference].
Constraints: power budget = [mW/mWh]; latency deadline = [ms]; connectivity = [Wi-Fi/BLE/LoRaWAN];
unit cost ceiling = [value]; required peripherals = [list].
Produce: a weighted decision matrix over candidates [list, e.g., STM32U5, ESP32-S3, RPi CM4],
scoring compute, memory headroom, power, ecosystem, and cost. State the recommendation,
the rejected alternatives with reasons, and draft the corresponding ADR.
```

**Template B — Interface Contract Definition**

```
Role: Embedded Systems Architect.
Goal: Define the contract between [Producer role] and [Consumer role] for [data/command].
Specify: transport + protocol + QoS; message schema (Protocol Buffers/CBOR) with field types and units;
versioning rule; error/timeout/retry behavior; offline/fallback behavior.
Output: the schema, the contract spec, the version, the list of consumers, and a sequence diagram.
```

**Template C — ADR Authoring**

```
Role: Embedded Systems Architect.
Decision: [one-line statement].
Produce an ADR with: Context (forces and constraints, with numbers); Decision; Consequences
(positive and negative); Alternatives Considered (with rejection rationale); Status = Proposed;
Related ADRs/contracts. Output as a standalone Markdown file.
```

**Template D — Per-Node Resource Budget Table**

```
Role: Embedded Systems Architect.
Goal: Define the resource budget for [node].
Output a table with explicit units for: Flash (used/total), SRAM (used/total incl. tensor arena),
PSRAM (if any), active/sleep power, peak/average current, and the latency deadline.
State the required minimum headroom margin at release and the requirement each line traces to.
```

**Template E — Protocol & Topology Specification**

```
Role: Embedded Systems Architect.
Goal: Specify the communication topology from [edge node] to [cloud].
Decide and justify: application protocol (MQTT/CoAP), QoS, transport (Wi-Fi/BLE/LoRaWAN),
security (mTLS/DTLS, X.509 identity), and behavior under intermittent connectivity
(LWT, backoff, store-and-forward). Output a topology diagram and the spec, and link the ADR.
```

---

## 10. Success Metrics & KPIs

**Technical metrics:**

- **Power-budget conformance:** ≥95% of nodes operate within their defined power envelope at release.
- **Latency conformance:** 100% of critical real-time paths meet their stated deadline under measurement.
- **Memory headroom:** ≥15% Flash and SRAM margin maintained per node at the production gate.
- **OTA reliability:** ≥99% successful updates across the fleet with 100% safe rollback on failed boot.
- **Interface stability:** Zero unplanned breaking contract changes after the development freeze (every breaking change preceded by an ADR and version bump).
- **Security baseline coverage:** 100% of production nodes ship with secure boot and mTLS enabled.

**Process & team metrics:**

- **Parallel-development enablement:** Zero teams blocked on missing or ambiguous contracts after the planning stage.
- **ADR coverage:** 100% of platform/protocol/interface/OTA/security decisions captured as ADRs.
- **Architecture review turnaround:** Reviews resolved within the agreed service-level window.
- **Architecture-attributable defects:** Downward trend in integration defects traced to interface or specification ambiguity.
- **Traceability completeness:** 100% of requirements mapped through architecture to verification in the NFR matrix.
- **Late-change rework:** Downward trend in rework caused by architecture changes introduced after the development stage.