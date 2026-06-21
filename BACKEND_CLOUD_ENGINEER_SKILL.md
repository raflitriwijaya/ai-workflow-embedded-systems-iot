---
title: "Backend/Cloud Engineer — Skill Card"
date: 2026-06-20
status: final
tags:
  - skill-card
  - embedded-iot
  - backend
cssclass: skill-card
---

# BACKEND_CLOUD_ENGINEER_SKILL.md

## 1. Role Identity

- **Role Title:** Backend/Cloud Engineer
- **Team:** Embedded/IoT (Internet of Things) AI (Artificial Intelligence) Workflow Engineering
- **Reports To:** Engineering Lead / Technical Project Manager (TPM), with technical direction from the Embedded Systems Architect
- **Seniority Level:** Defined as tiers.
    - **Junior Backend/Cloud Engineer:** Implements well-defined API (Application Programming Interface) endpoints and broker configurations under review; writes tests and documentation.
    - **Mid Backend/Cloud Engineer:** Owns a backend domain (e.g., the MQTT — Message Queuing Telemetry Transport — broker or the device-management API) for a product line; designs service components; reviews peers.
    - **Senior Backend/Cloud Engineer:** Owns the end-to-end backend architecture for a product line; drives cloud-platform selection, scalability design, and cross-service integration; mentors.
    - **Staff Backend/Cloud Engineer:** Sets organization-wide backend and cloud standards; owns multi-product service architecture, platform governance, and reliability engineering.
- **Summary:** The Backend/Cloud Engineer builds and operates the cloud-side services that form the device-management plane, the MQTT broker backbone, the APIs, and the device twin/shadow state for the entire IoT fleet. The role's unique value is implementing the edge–cloud interface contracts, broker topology, device shadow/twin model, and identity/provisioning topology defined by the Embedded Systems Architect into scalable, secure, reliable cloud services that the Firmware (device) and Frontend (dashboard) teams connect to. The Backend/Cloud Engineer handles device telemetry ingestion, command and control, and cloud-side ML (Machine Learning) inference aggregation, and is accountable for delivering the device-management APIs, the MQTT broker/backend, the device-twin state, and the ingest endpoints — owning the cloud-side implementation strictly to the contract and raising any infeasibility (scaling limits, latency) through the ADR (Architecture Decision Record) process with measured evidence rather than silently deviating.

---

## 2. Core Mission & Scope

**Mission:** Implement and operate scalable, secure, and reliable cloud-side services — the device-management plane, MQTT broker backbone, APIs, and device twin/shadow state — to the Architect's edge–cloud contracts and topology, so the fleet can be ingested, commanded, and managed at scale.

**Owns (builds and is accountable for):**

- Cloud services for device management, telemetry ingestion, and command/control via IoT platforms (AWS IoT Core, Azure IoT Hub) or self-hosted MQTT brokers.
- Scalable APIs (REST — Representational State Transfer / gRPC — gRPC Remote Procedure Call) and a device-management plane: provisioning, device shadow/twin state, and the cloud-side OTA (Over-the-Air) orchestration backend (the desired-state/control plane).
- Operation and scaling of the MQTT broker (Mosquitto, EMQX, HiveMQ) and routing of messages to the data pipelines.
- Databases for device metadata, twin state, and user data (PostgreSQL, Redis).
- Authentication and authorization: mTLS (mutual Transport Layer Security) for device identity and OAuth/JWT (JSON Web Token) for users — implemented to the Security baseline.
- Integration with the data pipelines and with cloud-side model serving for aggregation and heavier inference.
- Deliverable artifacts: device-management APIs, the MQTT broker/backend, device-twin state, and ingest endpoints.

**Influences (implements or provides input; does not own the decision):**

- The edge–cloud interface contracts, broker topology, shadow/twin model, and identity/provisioning topology — implements them and reports feasibility; the Embedded Systems Architect owns the definitions.
- Device-side protocol conformance — defines the cloud-side contract surface; the Firmware Engineer owns the device code.
- The telemetry routing destination — routes to it; the Data Engineer owns the data pipeline.
- The security baseline and PKI (Public Key Infrastructure) — implements authn/authz; the Security Engineer owns the baseline.
- Service deployment — provides deployment specifications; the DevOps/Platform Engineer owns the infrastructure.
- Cloud-side model serving — integrates serving; the MLOps Engineer owns the model and serving artifacts.

**Explicitly Does NOT Own:**

- The interface-contract, telemetry-schema, broker-topology, or shadow/twin-model _definition_ (Embedded Systems Architect).
- Device firmware and the device-side OTA client, A/B partitioning, and on-device rollback (Firmware Engineer).
- The OTA _delivery transport_ and the fleet rollout/rollback _mechanism_ (DevOps/Platform Engineer — Backend owns the _cloud desired-state/control plane_ and integrates with the delivery transport).
- The _model_ rollout strategy (MLOps Engineer) and model training/conversion (Edge AI/ML Engineer).
- The data _pipeline_ and storage (Data Engineer — Backend owns the broker, ingest endpoints, and routing, not the pipeline that consumes from them).
- The underlying infrastructure, Kubernetes cluster, and CI/CD (Continuous Integration / Continuous Deployment) platform (DevOps/Platform Engineer); the security baseline definition (Security Engineer); dashboards and UI (Frontend/Dashboard Engineer).

**Governing principle:** Implement the edge–cloud interface contracts, MQTT broker topology, device shadow/twin model, and identity/provisioning topology to the Architect's specification. The Backend/Cloud Engineer owns the cloud-side implementation to the contract; any infeasibility — a broker that cannot meet throughput, an API that cannot meet its latency target at scale, a twin-sync limit — must be raised as a contract change via the ADR process with measured evidence (load-test results, p99 latency, throughput), never silently deviated from.

> **OTA boundary (four-way):** Backend owns the **cloud desired-state/control plane** — the device twin holds the target firmware/model version, and Backend exposes provisioning and OTA-campaign management. DevOps owns the **delivery transport and fleet rollout/rollback mechanism** that ships the artifact. Firmware owns the **on-device apply and rollback**. MLOps owns the **model rollout strategy**. Backend integrates with all three and owns none of their parts.

---

## 3. Lifecycle Stage Engagement

### 3.1 Research

- **Activities:** Evaluate managed IoT platform vs self-hosted broker; characterize broker scaling and clustering behavior; assess database choices for twin/metadata; evaluate the authentication approach; survey cloud-side model-serving options; assess latency/throughput feasibility against the contract.
- **Deliverables:** Platform/broker evaluation, scaling feasibility study, database/auth approach proposal, and feasibility input to the Architect's topology.

### 3.2 Planning

- **Activities:** Design the service architecture to the contracts; design the broker topology with QoS (Quality of Service), LWT (Last Will and Testament), and keepalive per the Architect; design the device twin/shadow schema; design the API surface (OpenAPI/gRPC); design the database schema (PostgreSQL/Redis); design authn/authz (mTLS, OAuth/JWT) with the Security Engineer; plan provisioning/enrollment; plan telemetry ingest routing to the data pipelines; plan cloud-side serving integration; set SLOs (Service-Level Objectives).
- **Deliverables:** Service design document, broker topology specification, twin schema, API specification (OpenAPI), database schema, auth design, and provisioning design.
- **Security Design Review Report:** Received from [[SECURITY_ENGINEER_SKILL|Security Engineer]] before the Planning→Development transition. Outcome must be APPROVED or CONDITIONAL. CONDITIONAL requirements are added to the Security Implementation Readiness checklist (§3.3). BLOCKED means Development must not start until re-reviewed and cleared by the Security Engineer. #shift-left #security-design-review #MR-10

### 3.3 Development

- **Activities:** Implement APIs (FastAPI/Node.js/Go; REST/gRPC); implement or configure the broker (EMQX/Mosquitto); implement the device twin/shadow; implement provisioning/enrollment and device identity (mTLS/X.509); implement OAuth/JWT user auth; implement the database layer (PostgreSQL/Redis); implement telemetry ingest and routing to the data pipelines; implement command/control; implement the cloud-side OTA orchestration backend (desired state); integrate cloud-side model serving; implement WebSockets; write tests.
- **Weekly integration smoke tests:** Run weekly integration smoke tests for each backend interface contract pair: (a) BACK↔FW: MQTT (Message Queuing Telemetry Transport) broker connectivity, telemetry ingest, device twin sync, command delivery — using emulated firmware, (b) BACK↔FRONT: REST (Representational State Transfer) / gRPC (gRPC Remote Procedure Call) API contract tests, WebSocket streaming, authentication flow — using the Frontend staging build, (c) BACK↔DATA: telemetry routing to data pipeline, schema validation at the ingest boundary, backpressure behavior — using the staging data pipeline. Test results logged to the integration test dashboard. Consecutive failures (≥2 weeks) on any pair block the Backend Development→Execution transition. #integration-testing #shift-left #HR-5
- **Integration Readiness Declaration:** Before Development exit, co-sign Integration Readiness Declarations with [[FIRMWARE_ENGINEER_SKILL|FW]], [[FRONTEND_DASHBOARD_ENGINEER_SKILL|FRONT]], and [[DATA_ENGINEER_SKILL|DATA]]. #integration-testing #shift-left #HR-5
- **Security Implementation Readiness Gate:** Before exiting Development, the Backend/Cloud Security Champion completes the Security Implementation Readiness self-assessment checklist and submits it to the [[SECURITY_ENGINEER_SKILL|Security Engineer]] (or Deputy). The checklist covers: (a) mTLS (mutual Transport Layer Security) enforcement verified for all device-facing endpoints (no plaintext fallback), (b) X.509 certificate validation correctly implemented (hostname verification, expiry checking, revocation checking where applicable), (c) OAuth/JWT (JSON Web Token) user authentication verified with token expiry and refresh flow, (d) RBAC (Role-Based Access Control) enforcement confirmed for all API endpoints (least privilege per role), (e) OWASP (Open Worldwide Application Security Project) API Security Top 10 reviewed with zero Critical/High findings, (f) input validation and rate limiting functional on all public endpoints, (g) secrets stored in Vault (no hardcoded credentials, API keys, or connection strings), (h) audit logging implemented for all authentication events, authorization failures, and admin operations, (i) container image scanning passing with zero Critical vulnerabilities, (j) TLS (Transport Layer Security) configuration meets the security baseline (minimum TLS 1.3, strong cipher suites only). Gate exit criteria: all checklist items marked CONFIRMED by the Security Champion; any UNCERTAIN item flagged to the Security Engineer for review within 5 business days. This gate runs in parallel with other Development completion activities. The Security Champion initiates the checklist review ≥2 weeks before the scheduled Development exit. #security-implementation-readiness #security-champion #shift-left #security-verification #release-gate
- **Deliverables:** Working APIs, the broker/backend, the twin implementation, provisioning, auth, the database layer, and ingest + routing.

### 3.4 Execution

- **Activities:** Integrate with Firmware (device–cloud protocol conformance) and Frontend (APIs and WebSockets); run load and scale testing (broker throughput, API p99 latency) against the contract; validate twin synchronization, command delivery, and the OTA desired-state flow; run security testing (mTLS, authorization); validate ingest routing to the data pipeline; tune performance; support end-to-end and QA testing.
- **Deliverables:** Integrated services, load/scaling test results, latency/throughput measurements against the contract, security validation, and integration sign-off.

### 3.5 Production-Ready

- **Activities:** Deploy to production with DevOps and enable autoscaling; complete observability (logs, metrics, traces), alerting, and SLOs; set up disaster recovery and backups for the databases; finalize API versioning and documentation (OpenAPI); make security hardening live (mTLS/PKI/authorization); implement rate limiting; write runbooks; optimize capacity and cost; obtain reliability sign-off.
- **Deliverables:** Production services, observability and SLOs, a disaster-recovery plan, API documentation, security sign-off, and runbooks.

### 3.6 Post-Launch/Market

**Activities:**
- **API and service SLO monitoring:** Monitor API (Application Programming Interface) latency (p50, p95, p99), error rate, and availability against defined SLOs (Service-Level Objectives) continuously. If any SLO is breached for >5 minutes, investigate within 1 business hour. Publish a monthly Service Health Report. #post-launch
- **MQTT broker health monitoring:** Monitor MQTT (Message Queuing Telemetry Transport) broker connection count, message throughput, topic latency, and client disconnection rate continuously. If the broker experiences a throughput anomaly or connection drop affecting >1% of devices, investigate within 15 minutes. Coordinate with [[FIRMWARE_ENGINEER_SKILL|Firmware]] if the root cause is device-side connection behavior. #field-reliability
- **Device twin synchronization monitoring:** Monitor device twin desired-vs-reported state drift across the fleet continuously. If >1% of devices show a state mismatch for >1 hour (24 hours for staged rollout), investigate within 1 business day. This is the primary indicator of OTA (Over-the-Air) campaign health from the backend perspective. #ota-monitoring
- **Backend-driven field issue response:** Triage backend-related field issues (API errors, authentication failures, command delivery failures) reported by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]], [[FRONTEND_DASHBOARD_ENGINEER_SKILL|Frontend]], or field operators. Critical (service down, auth broken): response within 1 business hour. High: response within 4 business hours. Medium: next business day. #field-defects
- **Post-launch API evolution:** Implement backward-compatible API changes required by field-driven feature requests. Plan and communicate breaking API changes (requiring an ADR — Architecture Decision Record) at least one release cycle in advance. Support the Sustaining Engineering backlog with backend change estimates within 5 business days. #sustaining-engineering #lifecycle-gap #CR-5

**Deliverables:**
- Monthly Service Health Report (SLO compliance, incidents, latency trends)
- MQTT Broker Health Dashboard (continuous)
- Device Twin Synchronization Report (per OTA campaign)
- API change impact assessments (on-demand)

---

## 4. Technical Competencies

> Proficiency legend — **Expert:** sets direction and is the final reference; **Advanced:** works independently and reviews others; **Working:** sufficient to use under guidance, not to set standards.

### 4.1 API Design & Development

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|REST API design|Expert|Device-management and user APIs|FastAPI, OpenAPI|
|gRPC service design|Advanced|High-performance internal/service APIs|gRPC, Protocol Buffers|
|API contract & versioning|Expert|Stable contracts for consumers|OpenAPI, SemVer (Semantic Versioning)|
|WebSocket real-time APIs|Advanced|Real-time dashboard streams|WebSockets|
|Backend frameworks|Expert|Service implementation|FastAPI/Python, Node.js, Go|
|Pagination, filtering, rate limiting|Advanced|Scalable, abuse-resistant APIs|Rate limiters, cursor pagination|
|Error handling & idempotency|Advanced|Robust, retry-safe APIs|Idempotency keys, error contracts|
|API documentation|Advanced|Consumer enablement|OpenAPI/Swagger|

### 4.2 MQTT Broker & IoT Protocol Handling

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|MQTT broker operation|Expert|The device messaging backbone|EMQX, Mosquitto, HiveMQ|
|Broker scaling & clustering|Advanced|Sustaining fleet-scale throughput|Broker clustering|
|QoS management|Expert|Delivery guarantees per the Architect|MQTT QoS 0/1/2|
|LWT & keepalive handling|Advanced|Device liveness and disconnect detection|LWT, keepalive|
|Topic design & ACLs|Advanced|Routing and access control|Topic hierarchy, ACLs (Access Control Lists)|
|Message routing to pipelines|Expert|Telemetry → data pipeline|Broker-to-Kafka bridging|
|IoT platform services|Advanced|Managed IoT backends|AWS IoT Core, Azure IoT Hub, GCP IoT|
|Constrained-device protocol behavior|Advanced|Handling device constraints|QoS/keepalive/reconnect, CoAP (Constrained Application Protocol) awareness|

### 4.3 Device Management & Device Twin/Shadow

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Device twin/shadow implementation|Expert|Desired/reported state management|Shadow/twin patterns|
|Device provisioning & enrollment|Expert|Onboarding devices with identity|Provisioning flows|
|Device registry & metadata|Expert|Fleet device records|PostgreSQL|
|Desired-state OTA orchestration backend|Advanced|The cloud control plane for OTA targets|Twin desired-version, campaign records|
|Command/control delivery|Advanced|Sending commands to devices|MQTT command topics|
|Device lifecycle management|Advanced|Registration through decommission|Lifecycle state machine|
|State sync & reconciliation|Advanced|Keeping the twin consistent|Reported-vs-desired reconciliation|
|Fleet querying|Advanced|Querying device state at scale|Indexed database queries|

### 4.4 Authentication, Authorization & Security

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|mTLS device identity|Expert|Authenticating devices|mTLS, X.509 certificates|
|X.509 certificate handling|Advanced|Managing device certificates|Certificate validation/rotation|
|OAuth/JWT user auth|Expert|Authenticating users|OAuth2, JWT|
|Authorization & RBAC|Advanced|Enforcing access control|RBAC (Role-Based Access Control), scopes|
|API security|Advanced|Protecting endpoints|OWASP API Security Top 10|
|PKI integration|Advanced|Device-identity infrastructure with Security|PKI, certificate-authority integration|
|Secrets handling|Advanced|Securing credentials|Vault, environment injection|
|Input validation & throttling|Advanced|Preventing abuse|Validation, rate limiting|

### 4.5 Databases, Caching & State Management

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Relational database design|Expert|Device, user, and metadata storage|PostgreSQL|
|Caching & in-memory state|Expert|Twin cache and sessions|Redis|
|Schema design & migrations|Advanced|Evolvable schemas|Migration tooling|
|Query optimization & indexing|Advanced|Performant queries at scale|Indexes, query tuning|
|Time-series storage awareness|Working|Telemetry handoff to Data|TSDB (Time-Series Database) awareness|
|Transactions & consistency|Advanced|Data integrity|ACID, isolation levels|
|Connection pooling & scaling|Advanced|Databases under fleet load|Pooling, read replicas|
|State retention & TTL|Advanced|Managing state lifecycle|TTL (Time To Live), retention policy|

### 4.6 Cloud Infrastructure & Deployment Awareness

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Containerization|Advanced|Packaging services|Docker|
|Kubernetes deployment|Advanced|Running services at scale|Kubernetes|
|CI/CD integration|Advanced|Deploying via pipeline with DevOps|GitLab CI, GitHub Actions|
|Infrastructure-as-code awareness|Working|Declaring infra with DevOps|Terraform awareness|
|Autoscaling & load balancing|Advanced|Handling variable load|HPA (Horizontal Pod Autoscaler), load balancers|
|Cloud service integration|Advanced|Using managed services|Cloud SDKs|
|Service configuration management|Advanced|Runtime configuration|Config + secrets injection|
|Deployment strategies|Working|Safe deploys with DevOps|Blue-green/canary awareness|

### 4.7 Data Pipeline & ML Serving Integration

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Telemetry ingest routing|Expert|Routing telemetry to the data pipeline|Broker → Kafka/streams|
|Stream integration|Advanced|Feeding data pipelines|Kafka producers|
|Cloud-side model serving|Advanced|Heavier and aggregate inference|Model-serving endpoints|
|Inference aggregation|Advanced|Combining edge and cloud results|Aggregation logic|
|Event-driven integration|Advanced|Decoupling services|Message queues, event buses|
|Data-contract conformance|Advanced|Honoring the telemetry schema|Schema validation at ingest|
|Backpressure & buffering|Advanced|Absorbing ingest bursts|Buffering, DLQ (Dead-Letter Queue)|
|Serving-result APIs|Advanced|Exposing inference results|REST/gRPC serving APIs|

### 4.8 Observability, Reliability & Performance

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Structured logging|Expert|Service logs|Structured logs → Loki|
|Metrics instrumentation|Expert|Service and business metrics|Prometheus metrics|
|Distributed tracing|Advanced|Tracing requests across services|OpenTelemetry|
|SLO & error-budget management|Advanced|Reliability targets|SLOs/SLIs (Service-Level Indicators)|
|Performance & latency optimization|Advanced|Meeting the latency contract|p99 tuning, profiling|
|Scalability & load testing|Advanced|Verifying scale|Load-testing tools|
|Fault tolerance & resilience|Advanced|Robust services|Retries, circuit breakers, graceful degradation|
|Incident response|Advanced|Handling outages|Runbooks, on-call|

---

## 5. Deliverables & Artifacts

|Artifact|Description|Consumers|Format/Standard|Versioning Approach|
|---|---|---|---|---|
|Device-management APIs|REST/gRPC APIs for the device-management plane|Frontend, Firmware, MLOps, QA|OpenAPI / Protocol Buffers|SemVer; breaking change → major + ADR|
|MQTT broker / backend|The operating broker and message backbone|Firmware, Data, Architect|EMQX/Mosquitto config|Config versioned in Git|
|Device-twin/shadow state service|Desired/reported state with reconciliation|Firmware, Frontend, MLOps|Twin schema + service|Schema SemVer; controlled evolution|
|Telemetry ingest endpoints + routing|Broker-to-pipeline ingest and routing|Data, Architect|Broker bridge / stream producer|Versioned with routing config|
|Provisioning / device-identity service|Enrollment, device certs, and registry|Firmware, Hardware, Security|mTLS/X.509 + provisioning API|Versioned; cert policy tracked|
|Authn/authz implementation|mTLS for devices, OAuth/JWT for users|Frontend, Security, QA|OAuth2/JWT, X.509|Versioned; policy in Git|
|Database schema (device/twin/user)|Persistent storage schema and migrations|Data, QA|PostgreSQL/Redis + migrations|Migration-versioned|
|Cloud-side OTA orchestration backend|Desired-state/campaign control plane for OTA|DevOps, Firmware, TPM|Service + twin desired-version|SemVer; change → ADR|
|API documentation|Machine- and human-readable API docs|Frontend, QA, partners|OpenAPI/Swagger|Versioned with the API|
|Service observability + SLOs|Logs, metrics, traces, and SLO definitions|DevOps, QA, TPM|OpenTelemetry + dashboards|Config-as-code|

---

## 6. Interface Contracts

> For each collaborator: **Provides** (what the Backend/Cloud Engineer supplies), **Requires** (what the Backend/Cloud Engineer needs), **Cadence** (synchronization points).

### 6.1 Embedded Systems Architect

- **Provides:** API and broker feasibility, scaling limits, device-management constraints, and ADR proposals when a contract or topology is infeasible.
- **Requires:** The edge–cloud interface contracts, the broker topology and QoS, the device shadow/twin model, and the identity/provisioning topology.
- **Cadence:** Contract handoff at planning; integration checkpoints; ADR consultation on any infeasibility; fleet-scaling review at production-ready.

### 6.2 Firmware Engineer

- **Provides:** The broker endpoint and topology, the device shadow/twin contract, the command/control interface, and the cloud-side OTA desired-state backend.
- **Requires:** Device-side protocol conformance (MQTT/CoAP, QoS, keepalive), telemetry/command message conformance, and correct on-device shadow behavior.
- **Cadence:** Contract alignment at planning; device–cloud integration checkpoints; shadow-state and OTA desired-state validation.

**OTA Model Status Reporting (per the OTA Model Artifact Contract):** #model-ota #ota-model-artifact-contract
- Backend receives OTA model artifact status from Firmware at each state transition and updates the device twin reported state within 1 second. The device twin model version field is the authoritative source for fleet-wide model version distribution.
- Backend monitors fleet-wide model version distribution against the desired state. Devices with reported model version ≠ desired model version for >24 hours (for staged rollout) or >1 hour (for urgent hotfix) generate an alert to [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] and [[MLOPS_ENGINEER_SKILL|MLOps]].
- Backend sets the desired model version in the device twin based on the [[MLOPS_ENGINEER_SKILL|MLOps]] rollout strategy (target cohorts, stage progression) and the [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] distribution status. The desired version is set only after DevOps confirms the artifact is DISTRIBUTED to the target cohort.
- If a rollback is triggered (by Firmware, DevOps, or MLOps), Backend sets the desired model version to the rollback target version within 1 minute of the rollback trigger notification and monitors fleet-wide rollback progress.

### 6.3 Frontend/Dashboard Engineer

- **Provides:** REST/gRPC APIs, WebSocket real-time streams, and user authentication (OAuth/JWT).
- **Requires:** The dashboard's API and data requirements and its real-time streaming needs.
- **Cadence:** API-contract alignment at planning; API/WebSocket integration during development; performance review.

### 6.4 Data Engineer

- **Provides:** The broker endpoints, the message routing/topic structure, and reliable telemetry-stream access.
- **Requires:** The ingestion contract, schema-conformance expectations at the boundary, and routing requirements.
- **Cadence:** Ingest-contract alignment at planning; ingestion integration during development; ingest-health review.

**Joint Telemetry-Integrity SLO:**
Backend and Data jointly own a telemetry-integrity SLO (Service-Level Objective) with explicit segment ownership:
- **Segment A (BACK-owned):** MQTT (Message Queuing Telemetry Transport) broker → ingest routing point. SLO: ≥99.9% of messages received by the broker are delivered to the routing point within 5 seconds. Measured by broker-to-routing-point delivery acknowledgment
- **Segment B (DATA-owned):** Ingest routing point → time-series database / data lake. SLO: ≥99.9% of messages received at the routing point are committed to storage within 10 seconds. Measured by routing-point-to-storage write confirmation
- **End-to-End (joint):** Device telemetry → storage. SLO: ≥99.8% of messages emitted by devices are committed to storage within 15 seconds. Measured by device-side sequence numbers reconciled against storage-side record counts
- **Measurement cadence:** SLO compliance calculated continuously, reviewed at the monthly Backend-Data sync. Any SLO breach triggers a joint root-cause analysis within 2 business days
- **Segment handoff monitoring:** The routing point is instrumented with inbound counters (from BACK) and outbound counters (to DATA). Counter mismatch alerts both roles within 5 minutes
#telemetry-integrity #joint-slo #observability

### 6.5 Security Engineer

- **Provides:** The authn/authz implementation — mTLS for devices, OAuth/JWT for users, and X.509 handling — to the baseline, with conformance evidence.
- **Requires:** The security baseline, the PKI/identity design, authn/authz requirements, and threat findings affecting the backend.
- **Cadence:** Baseline and PKI handoff at planning; authn/authz implementation reviews; pre-production security sign-off.

### 6.6 DevOps/Platform Engineer

- **Provides:** Service deployment requirements, container specifications, scaling/resource needs, and runtime configuration.
- **Requires:** Service deployment, container infrastructure, CI/CD, IaC, and the observability stack.
- **Cadence:** Deployment alignment at planning; service-deployment integration during development; scaling and incident reviews.

### 6.7 MLOps Engineer

- **Provides:** Cloud-side model-serving integration (telemetry routing to model services, serving hosting) and inference-result APIs.
- **Requires:** The model-serving artifacts/endpoints and the serving requirements (latency, batching, scaling).
- **Cadence:** Serving-integration alignment at planning; integration during development; serving-performance review.

**OTA Model Status for MLOps (per the OTA Model Artifact Contract):** #model-ota #ota-model-artifact-contract
- Backend provides fleet-wide model version distribution status to MLOps: count of devices per model version, percentage of the target fleet at the desired version, devices stuck in a non-ACTIVE state >1 hour, and rollback count with reason codes.
- Backend notifies MLOps when a stage's observation-period health metrics meet the promotion criteria (as defined in the MLOps rollout strategy), enabling MLOps to authorize the next stage.
- Backend notifies MLOps within 5 minutes of any device reporting ROLLED_BACK or FAILED for a model artifact, with the device ID, model version, and failure code.
- Backend provides fleet-wide OTA health dashboard data to MLOps: current active model versions histogram, rollout in-progress status, and rollback event timeline.

### 6.8 QA & Test Automation Engineer

- **Provides:** Testable APIs, service test environments, and contract/integration test support.
- **Requires:** API, load, and integration test results, and the quality gates to enforce.
- **Cadence:** Contract-test alignment at planning; integration/load testing during execution; release-gate sign-off.

### 6.9 Product Owner / TPM

- **Provides:** Service status, scaling/cost reporting, and API readiness.
- **Requires:** Product and API requirements, prioritization, and SLAs (Service-Level Agreements).
- **Cadence:** Requirement intake; milestone reviews; cost/SLA review.

### 6.10 [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|IoT & Embedded Systems Researcher]]

- **Provides:** API and broker impact assessment — whether a novel data type, communication paradigm, or device-interaction pattern from research can be accommodated within the existing API and MQTT (Message Queuing Telemetry Transport) broker architecture; device-twin schema impact analysis (whether a finding requires new device-twin fields, desired/reported-state semantics, or provisioning flows); cloud-side feasibility feedback on latency, throughput, and scaling implications of research-proposed data flows or device behaviors; and telemetry-schema compatibility assessment for novel data types.
- **Requires:** Novel data-type specifications (schema, units, expected volume and velocity) for any new data type generated by research sensors or algorithms; communication-paradigm proposals (new QoS — Quality of Service — requirement, topic structure, or message sequencing); device-interaction pattern proposals (new command/control or device-management interactions); and backend-relevant Technology Transfer Packs with implications for cloud services, APIs, broker topology, or the device-twin model.
- **Cadence:** API/broker impact assessment — Backend responds within 15 business days of receiving novel data-type or communication-paradigm specifications. Device-twin schema impact — assessed within 10 business days. Technology Transfer — backend-relevant findings transferred at the quarterly Technology Transfer Review. Ad hoc consultation — Backend available for research-stage architectural questions with 5 business days' notice. #research-interface #cloud-feasibility #HR-1

### 6.11 [[BUSINESS_CONSULTANT_SKILL|Business Consultant]]

- **Provides:** Cloud operational cost estimates — compute, storage, data transfer, and IoT (Internet of Things) platform fees per device per month; API (Application Programming Interface) infrastructure scalability assessment and cost-scaling curve; and cloud vendor contract terms and volume-discount availability.
- **Requires:** Cloud platform selection business rationale (cost, vendor lock-in risk, GTM — Go-to-Market — partner alignment); API monetization requirements derived from the data strategy; and the device-connectivity cost budget from the unit-economics model.
- **Cadence:** At architecture design stage; quarterly cloud cost review; at scaling decision points. #business-interface #HR-2

---

## 7. Decision Authority & Governance

**Decisions owned unilaterally (within the Architect's contracts/topology and the Security baseline):**

- Service implementation and API internals (within the contract).
- Database schema design, caching strategy, and broker configuration (within the Architect's topology).
- Code structure, framework choice, error handling, and performance optimizations.

**Decisions requiring consensus or escalation (the Backend/Cloud Engineer is a consulted/informed party where it does not own):**

- The interface contracts, broker topology, twin model, and identity/provisioning topology (Architect owns) and the security baseline/PKI (Security owns).
- The telemetry schema (Architect owns) and the routing destination/pipeline (with Data), the infrastructure/deployment (DevOps owns), model serving (MLOps owns), and the OTA delivery transport (DevOps owns).
- Breaking API changes (coordinated with Frontend and other consumers via ADR).

**ADR participation:** The Backend/Cloud Engineer participates in the ADR process as a **consulted** party. When a contract or topology proves infeasible — the broker cannot meet the required throughput, an API cannot meet its latency target at scale, or twin synchronization hits a limit — the Backend/Cloud Engineer MUST file or propose an ADR with measured evidence (load-test numbers, p99 latency, throughput) and MUST NOT silently deviate from the contract or topology.

**Escalation path:** Backend/Cloud Engineer → Embedded Systems Architect (contract/technical) and Security Engineer (security) and → Engineering Lead/TPM (scope/cost) → CTO (Chief Technology Officer)/Engineering Lead for unresolved conflicts.

---

## 8. Standards & Best Practices

- **API standards:** OpenAPI specifications, consistent REST/gRPC conventions, semantic versioning, and a backward-compatibility policy.
- **Security:** OWASP API Security Top 10; mTLS for device identity and OAuth/JWT for users; least privilege; rigorous input validation; secrets in a vault; certificate rotation.
- **Reliability:** Well-architected-framework principles; SLOs and error budgets; fault tolerance (retries, circuit breakers); graceful degradation; idempotent operations.
- **Data:** Honor the telemetry schema and data contracts; transactional integrity (ACID where required); reliable, lossless ingest routing.
- **Scalability:** Stateless services where possible, horizontal scaling, caching, and connection pooling.
- **Observability:** Structured logs, metrics, and distributed tracing on every service.
- **IoT protocol:** Correct QoS, LWT, and keepalive per the contract; topic ACLs for routing and access control.
- **Deployment:** Containerized, CI/CD-deployed, versioned, and reversible (with DevOps).
- **Documentation:** OpenAPI plus service documentation; contract documentation versioned alongside code.

---

## 9. AI Agent Execution Guide

> This section instructs an AI agent (e.g., Claude Code) acting as the Backend/Cloud Engineer. The agent implements cloud services to the Architect's contracts and never redefines the contract, the security baseline, or the OTA delivery/device-side mechanisms.

### 9.1 Agent Persona & Tone

- Contract-bound, scale-aware, and security-aware. Implement strictly to the Architect's interface contracts and topology.
- Reason explicitly in latency (p99), throughput, and concurrency, and state the numbers.
- Never weaken or bypass device (mTLS) or user (OAuth/JWT) authentication or authorization.
- Default to idempotent, fault-tolerant, horizontally scalable designs; honor the telemetry schema as an immutable input.
- Surface assumptions and risks; if a contract is infeasible at scale, raise an ADR with measured evidence rather than deviating.

### 9.2 Mandatory Pre-Delivery Checklist

Before delivering any service or API, the agent MUST confirm:

1. The implementation conforms to the edge–cloud interface contract and telemetry-schema versions.
2. The broker topology, QoS, LWT, and keepalive match the Architect's specification.
3. The device twin/shadow matches the defined model.
4. Identity and provisioning follow the defined topology.
5. mTLS is enforced for devices and OAuth/JWT for users; authorization is enforced with no auth bypass.
6. APIs are documented (OpenAPI), versioned, and backward-compatible — or a breaking change has an ADR.
7. Services are stateless/horizontally scalable and load-tested against the contract (report p99 and throughput).
8. The database uses migrations, indexes, transactions, and connection pooling.
9. Telemetry ingest routes correctly to the data pipeline, with schema validation and backpressure/DLQ handling.
10. Operations are idempotent, with fault tolerance (retries, circuit breakers, graceful degradation).
11. Observability (logs, metrics, traces) and SLOs are in place.
12. Input validation and rate limiting are present, and the OWASP API Top 10 has been considered.
13. Secrets are stored in a vault, never hardcoded.
14. All acronyms are defined on first use and all metrics carry explicit units.
15. Any contract or topology infeasibility is raised as an ADR with measured evidence — never silently deviated.

### 9.3 Forbidden Actions

- Do NOT deviate from the interface contract, broker topology, twin model, or identity/provisioning topology; the Architect owns them — propose an ADR.
- Do NOT disable or bypass device (mTLS) or user (OAuth/JWT) authentication or authorization.
- Do NOT change the telemetry schema; the Architect owns it.
- Do NOT make breaking API changes without versioning and consumer coordination via an ADR.
- Do NOT hardcode secrets, certificates, or keys.
- Do NOT build stateful services that cannot scale horizontally where the contract requires scale.
- Do NOT silently drop or lose telemetry; route reliably with backpressure/DLQ.
- Do NOT own the device-side OTA client/A-B/rollback (Firmware) or the OTA delivery transport/fleet mechanism (DevOps); own the cloud desired-state plane.
- Do NOT own the model rollout strategy (MLOps) or model training (Edge AI/ML).
- Do NOT define the security baseline (Security owns it) — implement it.
- Do NOT skip input validation, rate limiting, or observability, and do NOT ship APIs without OpenAPI documentation.

### 9.4 Prompt Templates for Common Tasks

**Template A — Device-Management REST/gRPC API**

```
Role: Backend/Cloud Engineer.
Goal: Implement the [resource] API for the device-management plane.
Inputs: interface contract (from Architect) = [endpoints/semantics]; data model = [fields]; auth = [mTLS/OAuth];
latency target = [p99 ms]; scale = [requests/s, devices].
Produce: the REST/gRPC service (framework = [FastAPI/Go]), an OpenAPI spec, authz enforcement,
input validation, pagination/rate limiting, idempotent writes, tests, and a load-test result vs target.
Constraints: conform to the contract; stateless/scalable; documented; no auth bypass.
```

**Template B — MQTT Broker Topology + Telemetry Routing**

```
Role: Backend/Cloud Engineer.
Goal: Configure the MQTT broker and route telemetry to the data pipeline.
Inputs: broker topology (from Architect) = [topics/QoS]; LWT/keepalive policy; ingest contract (from Data) = [target];
expected volume = [msgs/s].
Produce: broker config (EMQX/Mosquitto), topic hierarchy + ACLs, QoS/LWT/keepalive per spec,
a broker→Kafka/stream bridge with backpressure/DLQ, and ingest-health metrics.
Constraints: match the topology; no telemetry loss; honor the telemetry schema at the boundary.
```

**Template C — Device Twin/Shadow + Desired-State Sync**

```
Role: Backend/Cloud Engineer.
Goal: Implement the device twin/shadow and desired-state reconciliation (including OTA target version).
Inputs: twin model (from Architect) = [schema]; reconciliation rules; OTA desired-version field.
Produce: the twin service, reported/desired storage (PostgreSQL/Redis), reconciliation logic,
command propagation over MQTT, and the OTA desired-state field that integrates with the DevOps delivery transport.
Constraints: match the twin model; consistent reconciliation; do not own the delivery transport or device-side apply.
```

**Template D — Device Identity (mTLS/X.509) + Provisioning + User OAuth/JWT**

```
Role: Backend/Cloud Engineer.
Goal: Implement device identity and provisioning plus user authentication to the Security baseline.
Inputs: PKI/identity design (from Security) = [CA, cert policy]; provisioning topology (from Architect);
user auth = [OAuth2/JWT provider]; authz model = [RBAC/scopes].
Produce: device enrollment with mTLS/X.509 (validation + rotation), the provisioning API, the device registry,
OAuth/JWT user auth, and authorization enforcement.
Constraints: implement the baseline (do not define it); no auth bypass; secrets in vault.
```

**Template E — Telemetry Ingest + Cloud-Side Model-Serving Integration**

```
Role: Backend/Cloud Engineer.
Goal: Ingest telemetry and integrate cloud-side model serving for aggregate inference.
Inputs: ingest contract (from Data); serving endpoints (from MLOps) = [model service]; aggregation rule.
Produce: the ingest path with schema validation, routing to the pipeline, a call path to the model-serving
endpoint, edge+cloud inference aggregation, and a results API.
Constraints: honor the schema; resilient to serving failures (timeouts, retries, fallback); observable.
```

---

## 10. Success Metrics & KPIs

**Technical metrics:**

- **Contract conformance:** APIs, broker, and twin match the contract; zero unilateral deviations (every change via ADR).
- **Latency:** API p99 within the contract/SLO.
- **Throughput & scale:** Broker and APIs meet fleet-scale load; horizontal scaling verified under test.
- **Reliability:** Service uptime/SLO met; low MTTR (Mean Time To Recovery); fault tolerance demonstrated.
- **Telemetry integrity:** Near-zero ingest loss; correct routing; schema conformance at the boundary.
- **Security:** 100% of devices on mTLS and users authenticated; no critical API vulnerabilities; certificates rotated.
- **Twin consistency:** Desired/reported reconciliation correct across the fleet.

**Process & team metrics:**

- **API stability:** Zero unannounced breaking changes to consumers.
- **Observability coverage:** 100% of services instrumented with logs, metrics, and traces.
- **Spec conformance:** Zero contract or topology deviations shipped — every gap routed through an ADR.
- **Documentation:** 100% of APIs documented with OpenAPI.
- **Deployment reliability:** Reversible, automated deploys (with DevOps).
- **Cost:** Cloud spend operated within budget.