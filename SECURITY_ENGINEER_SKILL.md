---
title: "Security Engineer — Skill Card"
date: 2026-06-20
status: final
tags:
  - skill-card
  - embedded-iot
  - security
cssclass: skill-card
---

# SECURITY_ENGINEER_SKILL.md

## 1. Role Identity

- **Role Title:** Security Engineer (Embedded/IoT — Internet of Things — Focus)
- **Team:** Embedded/IoT AI (Artificial Intelligence) Workflow Engineering
- **Reports To:** CTO (Chief Technology Officer) / Head of Engineering, with a dotted line to the Embedded Systems Architect for architectural integration
- **Seniority Level:** Defined as tiers.
    - **Junior Security Engineer:** Executes defined security test cases, runs vulnerability scans, and assists with threat-model documentation under guidance.
    - **Mid Security Engineer:** Owns a security domain (e.g., device hardening, transport security) for a product line; conducts threat modeling and security reviews; reviews peers.
    - **Senior Security Engineer:** Owns the end-to-end security posture for a product line; defines the security baseline, drives PKI (Public Key Infrastructure) design, and leads penetration testing; mentors.
    - **Staff Security Engineer:** Sets organization-wide security standards and governance; owns multi-product security architecture, incident response, and compliance.
- **Deputy Security Engineer:** A designated alternate for the Security Engineer with authority to: (a) sign off on Standard-tier releases (see §7.1 Tiered Security Sign-Off), (b) conduct routine threat-model reviews, (c) approve non-breaking security baseline clarifications, and (d) act as Security Engineer delegate in Architecture Review Board meetings when the Security Engineer is unavailable. The Deputy Security Engineer is a named individual drawn from the Senior Firmware Engineer, Senior Backend/Cloud Engineer, or Senior DevOps/Platform Engineer tier who has completed the organizational security training curriculum and passed the Deputy Security Engineer qualification review (conducted by the Security Engineer and CTO — Chief Technology Officer). The Deputy Security Engineer role is reviewed and re-designated annually. The Deputy Security Engineer retains their primary role responsibilities; this is an additional duty, not a full-time security position. #deputy-security-engineer #tiered-sign-off #HR-10
- **Security Champion:** Each implementing role ([[FIRMWARE_ENGINEER_SKILL|Firmware]], [[BACKEND_CLOUD_ENGINEER_SKILL|Backend/Cloud]], [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps/Platform]], [[MLOPS_ENGINEER_SKILL|MLOps]], [[HARDWARE_ENGINEER_SKILL|Hardware]], [[DATA_ENGINEER_SKILL|Data]]) designates a Security Champion — a senior team member who acts as the single point of security contact for that role. The Security Champion: (a) completes the organizational security training curriculum (annual refresher), (b) conducts the Security Implementation Readiness self-assessment at the end of Development (§3.3), (c) participates in the Security Engineer's quarterly security review, (d) is the first reviewer for any security-relevant code or configuration change within their role, and (e) has a standing 30-minute monthly 1:1 with the Security Engineer for ongoing security alignment. The Security Champion is NOT a deputy — they cannot sign off on releases or modify the security baseline. They are an early-warning sensor and a first-line reviewer, not a decision-maker. #security-champion #shift-left #security-verification
- **Summary:** The Security Engineer is responsible for the end-to-end security posture of the embedded/IoT AI system — from the hardware root of trust on every edge device, through firmware and transport security, to cloud identity and fleet-wide governance. The role's unique value is that it _defines the security baseline that every other role implements_ — secure boot, signed firmware/OTA (Over-the-Air), mTLS (mutual Transport Layer Security), PKI, key management, and device hardening — and then verifies conformance rather than implementing the controls itself. The Security Engineer conducts threat modeling and security reviews, performs penetration testing and vulnerability analysis, works with the Embedded Systems Architect to embed security by design, and holds the authority to block a release on security grounds. They are accountable for delivering the security architecture, secure-boot/mTLS implementation specifications, threat models, and penetration-test reports — and for ensuring that any security gap which could lead to a breach is raised as an ADR (Architecture Decision Record) or release blocker with objective evidence, never accepted as technical debt without a documented, time-bound remediation plan.

> **Acronym note:** In this card, **TPM** denotes **Trusted Platform Module** (a hardware security device), reflecting its dominant use here. The Product Owner / Technical Project Manager role — abbreviated "TPM" in the other role cards — is spelled out in full in this document (Section 6.9) to avoid collision.

---

## 2. Core Mission & Scope

**Mission:** Define, enforce, and continuously verify the end-to-end security posture of the embedded/IoT AI system — anchoring trust in device hardware, securing firmware, transport, identity, and cloud, and governing the fleet — so that the system is resistant to compromise by design and no release ships with an unmitigated, breach-enabling vulnerability.

**Owns (defines and is the authority for):**

- The device security baseline: secure boot, signed firmware/OTA, and a hardware root of trust (TPM — Trusted Platform Module, secure element, ARM TrustZone) — the _definition and requirements_.
- Device identity and transport-security _requirements_: X.509 certificates, mTLS for MQTT (Message Queuing Telemetry Transport)/CoAP (Constrained Application Protocol), and key provisioning and rotation policy.
- Threat modeling (STRIDE) and security reviews across edge, transport, and cloud, aligned to the OWASP (Open Worldwide Application Security Project) IoT Top 10.
- Device-hardening _requirements_: debug-port lockdown (JTAG/SWD — Joint Test Action Group / Serial Wire Debug), secure key storage, anti-rollback, and encrypted storage.
- Penetration testing and firmware security analysis (binary analysis, fuzzing, side-channel awareness).
- Incident response and secure-OTA governance for the fleet.
- Security release sign-off authority — the ability to block a release on security grounds.
- Deliverable artifacts: the security architecture, secure-boot/mTLS implementation specifications, threat models, and penetration-test reports.

**Influences / co-owns:**

- System-architecture security-by-design — co-owned with the Embedded Systems Architect: Security defines the security content, the Architect embeds it into the system architecture.
- Implementation of every baseline control — owned by Firmware, Hardware, Backend, DevOps, and MLOps Engineers, who implement to the Security specification while Security verifies conformance.

**Explicitly Does NOT Own:**

- The implementation of the controls themselves: Firmware implements secure boot and on-device crypto; Hardware places the secure element and locks debug ports; Backend implements mTLS/PKI and authn/authz; DevOps implements signing infrastructure and secrets management; MLOps implements pipeline signing. Security _defines and verifies_, it does not implement.
- The system architecture (Embedded Systems Architect — Security co-owns only the security aspects).
- Firmware, hardware, backend, cloud, or ML implementation.
- The OTA _mechanism_ (Backend desired-state plane, DevOps delivery transport, Firmware device-side apply, MLOps model rollout) — Security defines the OTA _security governance and requirements_ (signing, integrity, anti-rollback) that those owners implement.
- Feature functionality and product scope (Product Owner / Technical Project Manager).

**Governing principle:** Security defines the baseline that other roles implement, verifies their conformance, and is the authority that can block a release on security grounds. Any security gap that could lead to a breach must be raised as an ADR or release blocker with objective evidence (a penetration-test finding, a CVE — Common Vulnerabilities and Exposures — entry, or a threat-model gap), and must never be accepted as technical debt without a documented, time-bound remediation plan signed off by Security.

---

## 3. Lifecycle Stage Engagement

### 3.1 Research

- **Activities:** Analyze the threat landscape for the deployment (edge/IoT, including field/agricultural exposure); evaluate root-of-trust options (TPM, ATECC608, SE050, ARM TrustZone); survey cryptographic, secure-boot, and PKI approaches; assess regulatory and compliance obligations (IEC 62443, NIST IoT guidance); enumerate the attack surface.
- **Deliverables:** Threat-landscape report, root-of-trust evaluation, compliance-requirements analysis, and a preliminary attack-surface map.

### 3.2 Planning

- **Activities:** Define the security baseline (secure boot, signed OTA, root of trust, mTLS, key management, hardening) jointly with the Architect for security-by-design; build the STRIDE threat model; design the PKI/identity topology and key provisioning/rotation; define hardening requirements; define secure-OTA governance; define security acceptance criteria and the release security gate.
- **Security Design Review:** Conduct a Security Design Review for each implementing role during Planning — before implementation begins. Review each role's planned design against the security baseline and role-specific threat model findings. Output: a Security Design Review Report per role with outcome APPROVED (proceed), CONDITIONAL (proceed with noted requirements added to Security Implementation Readiness checklist), or BLOCKED (must not start — security concerns must be resolved first). All reviews must be completed before the Planning→Development transition. #shift-left #security-design-review #MR-10
- **Deliverables:** Security baseline specification, STRIDE threat model, PKI/identity design, hardening requirements, secure-OTA governance policy, and security acceptance criteria.

### 3.3 Development

- **Activities:** Author secure-boot, mTLS, and key-storage implementation _specifications_ for Firmware, Backend, and DevOps; review implementations for conformance; conduct security design reviews; stand up the PKI/CA (Certificate Authority); define artifact-signing requirements; specify model-integrity/signing requirements with MLOps; build and run security tests; perform static analysis of firmware.
- **Security Implementation Start gate:** Before any implementing role begins Development, verify that: (a) the Security Design Review Report outcome for that role is APPROVED or CONDITIONAL, (b) the role's Security Champion has acknowledged the security requirements relevant to their role, (c) any CONDITIONAL requirements are documented in the role's Security Implementation Readiness checklist. Notify the role lead and the [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] within 1 business day if any role attempts to start Development without a completed Security Implementation Start confirmation. #shift-left #security-implementation-start #MR-10
- **Deliverables:** Implementation specifications, security-review findings, PKI/CA setup, signing requirements, a security test suite, and static-analysis results.

### 3.4 Execution

- **Activities:** Perform penetration testing across device, firmware, transport, and cloud; conduct firmware binary analysis and fuzzing; verify the secure-boot chain, mTLS, anti-rollback, and debug-port lockdown on real hardware; run vulnerability assessment; verify PKI and key provisioning; validate model integrity; run security regression.
- **Deliverables:** Penetration-test reports, vulnerability assessment, firmware security analysis, conformance-verification results, and remediation tracking.

### 3.5 Production-Ready

- **Activities:** Produce the final security sign-off / release gate; confirm the baseline is fully implemented and verified; confirm secure-OTA governance and key rotation are live; finalize the incident-response plan and runbooks; confirm the SBOM (Software Bill of Materials) and supply-chain integrity; produce compliance attestation; maintain a residual-risk register with time-bound remediation. Co-chair the **Joint Data Security & Governance Review** (quarterly, second Tuesday of January, April, July, October) with the [[DATA_ENGINEER_SKILL|Data Engineer]]: review Data Security & Governance Policy currency and #regulatory-compliance alignment (GDPR — General Data Protection Regulation, CCPA — California Consumer Privacy Act, NIST SP 800-53); assess #data-classification coverage; review #access-review completion and findings; assess #encryption-at-rest and #encryption-in-transit metrics; review #audit-logging integrity and SIEM (Security Information and Event Management) integration; assess #vulnerability-scanning results and remediation SLA (Service-Level Agreement) compliance; review #privacy-impact escalations from the quarter; verify #PII-masking and #data-minimization compliance; produce a joint governance report with findings, recommendations, and updated #risk register stored alongside the Data Security & Governance Policy in version control.
- **Deliverables:** Security release sign-off, final threat model, incident-response plan, compliance attestation, and a residual-risk/remediation register.

---

## 4. Technical Competencies

> Proficiency legend — **Expert:** sets direction and is the final reference; **Advanced:** works independently and reviews others; **Working:** sufficient to use under guidance, not to set standards.

### 4.1 Device Hardware Security & Root of Trust

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Hardware root of trust|Expert|Anchoring device trust|TPM (Trusted Platform Module), ATECC608, SE050|
|Secure-element specification|Expert|Defining secure-element usage|ATECC608, SE050|
|ARM TrustZone / TEE|Advanced|Isolated secure execution|TrustZone, TEE (Trusted Execution Environment)|
|Debug-port lockdown specification|Expert|Preventing debug access on production devices|JTAG/SWD lockdown, eFuse|
|Anti-rollback (fuse-based)|Advanced|Preventing firmware downgrade|eFuse, rollback counters|
|Secure key storage specification|Expert|Protecting keys on device|Secure element, on-chip key storage|
|Physical & tamper resistance|Advanced|Resisting physical attack|Tamper detection, shielding|
|Side-channel awareness|Advanced|Resisting power/timing attacks|DPA (Differential Power Analysis), constant-time design|

### 4.2 Firmware Security, Secure Boot & OTA Integrity

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Secure-boot chain specification|Expert|Verified boot from root of trust|MCUboot, signed images|
|Firmware signing & verification|Expert|Image authenticity and integrity|Signing keys, MCUboot|
|Anti-rollback enforcement|Expert|Blocking downgrade attacks|Rollback counters|
|Secure-OTA governance|Expert|Safe, signed, verified updates|Signed OTA, integrity verification|
|Firmware crypto libraries|Advanced|On-device cryptography|mbedTLS, wolfSSL|
|Encrypted storage specification|Advanced|Protecting data at rest|AES, flash encryption|
|Firmware binary analysis|Advanced|Finding vulnerabilities in firmware|Disassembly, binary analysis|
|Memory-safety & isolation requirements|Advanced|Limiting compromise blast radius|Memory Protection Unit, TrustZone|

### 4.3 Transport Security & Cryptographic Protocols

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|TLS/mTLS design|Expert|Securing transport|TLS 1.3, mTLS|
|MQTT/CoAP security|Expert|Securing IoT messaging|mTLS for MQTT, DTLS (Datagram TLS) for CoAP|
|Cryptographic algorithm selection|Expert|Choosing sound primitives|AES, ECDSA, SHA-256|
|Certificate-based authentication|Expert|Device and service identity|X.509|
|Key exchange & session security|Advanced|Securing sessions|ECDHE, perfect forward secrecy|
|Crypto-agility|Advanced|Enabling algorithm upgrades|Cipher negotiation|
|DTLS for constrained devices|Advanced|Securing CoAP/UDP|DTLS|
|Cryptographic correctness review|Advanced|Avoiding crypto misuse|Protocol/implementation review|

### 4.4 Identity, PKI & Key Management

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|PKI design & operation|Expert|Device/service identity infrastructure|PKI, CA (Certificate Authority)|
|X.509 certificate lifecycle|Expert|Issuance, rotation, revocation|X.509, CSR (Certificate Signing Request), CRL (Certificate Revocation List)/OCSP|
|Device identity provisioning|Expert|Onboarding device identities|Provisioning, secure element|
|Key provisioning & rotation|Expert|Fleet-wide key management|Key rotation policy|
|Certificate revocation|Advanced|Revoking compromised identities|CRL, OCSP (Online Certificate Status Protocol)|
|Secrets management|Advanced|Protecting secrets|HashiCorp Vault|
|HSM usage|Advanced|Protecting CA/root keys|HSM (Hardware Security Module)|
|Cloud identity federation|Advanced|User/service identity|OAuth, JWT (JSON Web Token)|

### 4.5 Cloud & API Security

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|API security|Expert|Protecting cloud APIs|OWASP API Security Top 10|
|Authn/authz design|Expert|Access control|OAuth2, JWT, RBAC (Role-Based Access Control)|
|Cloud identity & IAM|Advanced|Cloud access control|IAM (Identity and Access Management), least privilege|
|mTLS for device–cloud|Expert|Mutual authentication|mTLS|
|Cloud secrets/credential security|Advanced|Protecting cloud secrets|Vault, secret rotation|
|Network security & segmentation|Advanced|Isolating components|Segmentation, firewall rules|
|Security monitoring & logging|Advanced|Detecting threats|SIEM (Security Information and Event Management), audit logs|
|Cloud supply-chain security|Advanced|Dependency/image integrity|SBOM, image scanning|

### 4.6 Threat Modeling & Security Architecture

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|STRIDE threat modeling|Expert|Systematic threat identification|STRIDE|
|Attack-surface analysis|Expert|Mapping entry points|Attack-surface mapping|
|Security-by-design|Expert|Embedding security with the Architect|Architecture review|
|Risk assessment & scoring|Expert|Prioritizing risk|CVSS (Common Vulnerability Scoring System), risk matrix|
|Trust-boundary analysis|Advanced|Defining trust zones|Data-flow diagrams|
|Security requirements engineering|Expert|Defining the baseline|Requirements specifications|
|Adversary TTP mapping|Advanced|Modeling adversary behavior|MITRE ATT&CK|
|Defense-in-depth design|Advanced|Layering controls|Layered security architecture|

### 4.7 Penetration Testing & Vulnerability Analysis

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Penetration testing|Expert|Finding exploitable vulnerabilities|Penetration-testing tooling|
|Firmware fuzzing|Advanced|Finding input-handling vulnerabilities|Fuzzers|
|Static analysis (SAST)|Advanced|Code-level vulnerability detection|SAST (Static Application Security Testing), cppcheck|
|Dynamic analysis (DAST)|Advanced|Runtime vulnerability detection|DAST (Dynamic Application Security Testing)|
|Vulnerability assessment|Expert|Identifying and scoring vulnerabilities|CVE, CVSS, scanners|
|Hardware attack testing|Advanced|Physical and side-channel attacks|Glitching, DPA|
|Network/protocol testing|Advanced|Transport and protocol vulnerabilities|Protocol fuzzing|
|Ethical exploit development|Advanced|Proving exploitability|Proof-of-concept exploits|

### 4.8 AI/ML Security & Model Integrity

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Model signing & integrity|Expert|Ensuring authentic models on device|Model signing|
|On-device anti-tampering|Advanced|Protecting the deployed model|Integrity checks|
|Model-extraction protection|Advanced|Preventing model theft|Access control, obfuscation|
|Adversarial-input awareness|Working|Robustness against attack|Adversarial-testing awareness|
|ML pipeline security|Advanced|Securing training-to-deploy with MLOps|Pipeline artifact signing|
|Data-poisoning awareness|Working|Protecting training-data integrity|Data provenance|
|Inference integrity|Advanced|Trustworthy on-device inference|Signed model + verification|
|ML supply-chain security|Advanced|Model-artifact integrity|Signed artifacts, lineage|

### 4.9 Incident Response, Governance & Compliance

|Skill|Proficiency|Application Context|Technologies/Tools|
|---|---|---|---|
|Incident response|Expert|Handling breaches|IR plan, runbooks|
|Secure-OTA governance|Expert|Governing fleet updates|Signing, approval gates|
|Security compliance|Advanced|Meeting standards|IEC 62443, ISO 27001, NIST guidance|
|Vulnerability management & disclosure|Advanced|Tracking and remediating vulnerabilities|CVE tracking, responsible disclosure|
|Security audit support|Advanced|Audits and attestation|Audit evidence|
|Key-compromise response|Advanced|Revoking and rotating on compromise|Revocation, re-provisioning|
|Post-incident forensics|Working|Investigating breaches|Log analysis, forensics|
|Security governance & policy|Advanced|Organizational security policy|Policy and standards|

---

## 5. Deliverables & Artifacts

|Artifact|Description|Consumers|Format/Standard|Versioning Approach|
|---|---|---|---|---|
|Security baseline specification|Secure boot, mTLS, PKI, key management, and hardening requirements|Firmware, Hardware, Backend, DevOps, MLOps, Architect|Markdown specification|SemVer (Semantic Versioning); change → ADR; co-versioned with Architect|
|Threat model (STRIDE)|Systematic threats, trust boundaries, and mitigations|Architect, all implementing roles, QA|Markdown + data-flow diagrams|Updated per attack-surface change|
|Secure-boot / mTLS implementation specs|Precise specifications for implementers|Firmware, Backend, DevOps|Markdown specification|SemVer; controlled change|
|PKI / identity / key-management design|Certificate lifecycle, provisioning, and rotation design|Backend, Firmware, DevOps, Hardware|Markdown + diagrams|Versioned; key-policy changes tracked|
|Penetration-test reports|Findings, severity (CVSS), and remediation guidance|Architect, owning roles, TPM-PM, Engineering Lead|Markdown/PDF report|One per test cycle; findings tracked to closure|
|Vulnerability assessment + remediation register|Identified vulnerabilities with severity and remediation status|All roles, Engineering Lead|Register (CVE/CVSS)|Continuously live; dated reviews|
|Device-hardening requirements|Debug lockdown, key storage, anti-rollback, encryption|Hardware, Firmware|Markdown specification|Versioned with the baseline|
|Secure-OTA governance policy|Signing, integrity, anti-rollback, and approval requirements for updates|DevOps, Firmware, Backend, MLOps|Markdown policy|Versioned; change → ADR|
|Incident-response plan + runbooks|Breach detection, response, and recovery procedures|On-call, Engineering Lead, all roles|Markdown|Versioned; reviewed periodically|
|Security release sign-off / compliance attestation|Go/no-go security gate and standards attestation|TPM-PM, Architect, Engineering Lead, CTO|Sign-off record / attestation|One per release; archived|
|Data Security & Governance Policy|Joint policy co-owned with [[DATA_ENGINEER_SKILL\|Data Engineer]] defining: #data-classification schema (Public / Internal / Confidential / Restricted), #encryption-at-rest requirements (AES-256-GCM — Advanced Encryption Standard 256-bit Galois/Counter Mode), #encryption-in-transit requirements (TLS 1.3 — Transport Layer Security), #access-control model (RBAC — Role-Based Access Control — definitions: Data Administrator, Data Operator, Data Consumer, Read-Only Auditor; least-privilege guidance; MFA — Multi-Factor Authentication — for administrative roles), #audit-logging requirements (event catalog, retention periods, log integrity, SIEM — Security Information and Event Management — integration), #PII-masking and #data-minimization standards (tokenization, k-anonymity, GDPR — General Data Protection Regulation — Article 5(1)(c) data minimization, right-to-deletion per GDPR Article 17 and CCPA — California Consumer Privacy Act — §1798.105), #vulnerability-scanning requirements (scope, frequency, remediation SLA — Service-Level Agreement), #data-breach notification procedures (4-hour initial, 24-hour detailed report), and quarterly Joint Data Security & Governance Review cadence|[[DATA_ENGINEER_SKILL\|Data Engineer]], [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps/Platform Engineer]], [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend/Cloud Engineer]], [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]], [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA & Test Automation Engineer]], [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]]|Markdown document in Git; references NIST SP 800-53 (Security and Privacy Controls for Information Systems and Organizations), GDPR Article 32 (Security of Processing), and organizational security baseline|Semantic versioning (SemVer); major bump on classification schema change or new regulatory requirement; minor bump on procedural update; reviewed and re-authorized quarterly at the Joint Data Security & Governance Review|

---

## 6. Interface Contracts

> For each collaborator: **Provides** (what the Security Engineer supplies), **Requires** (what the Security Engineer needs), **Cadence** (synchronization points).

### 6.1 Embedded Systems Architect

- **Provides:** The security baseline definition, threat models, hardening requirements, and PKI/identity design — co-owned for security-by-design.
- **Requires:** Architecture surfaces for threat modeling and the embedding of security requirements (secure boot, mTLS, root of trust) into the system architecture.
- **Cadence:** Joint security-baseline authoring at planning; security architecture reviews; ADR consultation (with veto) on any security-relevant decision.

### 6.2 Firmware Engineer

- **Provides:** Secure-boot, mTLS, key-storage, and anti-rollback implementation specifications; threat-model findings affecting firmware; and hardening directives.
- **Requires:** Implementation of the controls to specification and conformance evidence (secure-boot chain, signed images, mTLS, secure key handling).
- **Cadence:** Baseline/spec handoff at planning; secure-boot and transport-security implementation reviews; pre-production hardening sign-off.

### 6.3 Hardware Engineer

- **Provides:** Secure-element selection requirements, the debug-port lockdown policy, physical-hardening/tamper requirements, and the root-of-trust specification.
- **Requires:** Physical placement of the secure element/root-of-trust device, debug-port lockdown implementation, and tamper-resistance measures on the board.
- **Cadence:** Security-requirement handoff at planning; secure-element and debug-lockdown review; pre-production hardening sign-off.

### 6.4 Backend/Cloud Engineer

- **Provides:** The PKI/identity design, mTLS and authn/authz requirements, API-security requirements, and threat findings affecting the backend.
- **Requires:** Implementation of authn/authz (mTLS, OAuth/JWT, X.509 handling) to the baseline, with conformance evidence.
- **Cadence:** Baseline and PKI handoff at planning; authn/authz implementation reviews; pre-production security sign-off.

### 6.5 DevOps/Platform Engineer

- **Provides:** Artifact-signing/key/PKI requirements, secrets-management requirements, hardening and compliance rules, and threat findings affecting the platform.
- **Requires:** Artifact-signing infrastructure, secrets management (Vault), hardened infrastructure, RBAC, and image/dependency scanning — implemented to the baseline.
- **Cadence:** Baseline handoff at planning; signing/secrets/hardening implementation reviews; pre-production sign-off.

### 6.6 MLOps Engineer

- **Provides:** Model-signing and integrity requirements, supply-chain integrity rules, and pipeline-security requirements.
- **Requires:** Implementation of pipeline RBAC, artifact signing, and secrets handling to the baseline.
- **Cadence:** Baseline handoff at planning; pipeline-security implementation review; pre-production sign-off.

### 6.7 Edge AI/ML Engineer

- **Provides:** Model-integrity, anti-extraction, and anti-tampering requirements for models deployed to the edge.
- **Requires:** Model artifacts and metadata for threat assessment, and awareness of the deployment target for integrity protection.
- **Cadence:** Requirements alignment at planning; model-integrity review when model formats or deployment targets change.

### 6.8 QA & Test Automation Engineer

- **Provides:** Security test requirements, threat-derived test cases, and penetration-test scope.
- **Requires:** Security test execution and validation results, and verification of security-defect fixes.
- **Cadence:** Security-test alignment at planning; security validation during execution; release-gate sign-off.

### 6.9 Product Owner / Technical Project Manager

- **Provides:** Security risk assessments, required pre-release mitigations, compliance constraints affecting scope/timeline, and the **release security sign-off** (which can block a release).
- **Requires:** Visibility into features touching connectivity, data handling, or OTA delivery, and the schedule context for security work.
- **Cadence:** Mandatory consultation for any feature involving new connectivity, data flows, or OTA mechanisms; per-release security sign-off.

---

### 6.10 [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|IoT & Embedded Systems Researcher]]

- **Provides:** #threat-model assessment of security-relevant research findings using STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) methodology, delivered within 10 business days of receipt of the Researcher's Pre-Transfer Security Review briefing; security requirements and constraints for experimental design — encryption standards (AES-256-GCM — Advanced Encryption Standard with 256-bit key in Galois/Counter Mode, ChaCha20-Poly1305), secure boot chain implications, hardware root-of-trust requirements, key management protocols, and data-classification requirements per organizational policy; guidance on secure handling of sensitive research data (storage encryption — AES-256 at rest, access logging, data minimization, and PII — Personally Identifiable Information — masking where applicable); feedback on the security feasibility of proposed novel architectures, identifying elements that would require additional security controls in production and flagging directions incompatible with the security baseline; and quarterly threat-landscape briefings incorporating research-stage insights and emerging #attack-surface categories relevant to active research directions.

- **Requires:** Technology Transfer Packs with flagged #security-relevant findings and explicit identification of potential #attack-surface elements (categorized as #connectivity, #data-handling, #compute-architecture, #sensor-physics); Pre-Transfer Security Review briefing documents for each finding with connectivity, data-handling, or compute-architecture implications, submitted ≥2 weeks (10 business days) before the scheduled Technology Transfer; early-stage notification of research directions that may introduce novel attack surfaces within 5 business days of direction change; characterization data for novel hardware security mechanisms under investigation (PUF — Physical Unclonable Function — response characteristics, side-channel-resistant transducer designs, experimental tamper-detection materials, hardware-based entropy sources); and a quarterly update on active research directions for threat-landscape alignment.

- **Cadence:** Pre-Transfer Security Review — #threat-model assessment delivered within 10 business days of the Researcher's briefing submission; must be completed before Technology Transfer Pack finalization. Quarterly Research-Security Threat Landscape Review — joint session, first Tuesday of each calendar quarter (January, April, July, October); joint summary distributed to the Head of Research and CTO within 5 business days. Ad hoc consultation — Security Engineer acknowledges notification within 3 business days and provides an initial assessment within 10 business days (standard) or 20 business days (high complexity). Security requirements for experimental design — updated annually or upon significant organizational security-baseline change. #research-interface #security-review #HR-1

### 6.11 [[DATA_ENGINEER_SKILL|Data Engineer]]

- **Provides:** #data-classification requirements: a complete categorization schema (Public / Internal / Confidential / Restricted) with definitions, handling rules per classification level, and classification labeling requirements for all data assets, aligned to NIST SP 800-53 (Security and Privacy Controls for Information Systems and Organizations) control families PM-8 and RA-2. #encryption-at-rest requirements: minimum encryption standard of AES-256-GCM (Advanced Encryption Standard with 256-bit key in Galois/Counter Mode), key management protocol integrated with HashiCorp Vault, and explicit scope of application covering all data stores containing Confidential or Restricted data — time-series databases (InfluxDB, TimescaleDB), data lake partitions (Parquet on S3/MinIO), training datasets, feature stores, and metadata stores. #encryption-in-transit requirements: minimum TLS 1.3 (Transport Layer Security version 1.3) for all data movement between pipeline stages, mandatory certificate validation (no disabled verification, no self-signed certificates in production), and explicit scope covering all ingestion pipelines (MQTT — Message Queuing Telemetry Transport — broker → Kafka → TSDB — Time-Series Database / Data Lake), ETL/ELT (Extract, Transform, Load / Extract, Load, Transform) pipeline stages, feature engineering pipelines, training dataset assembly, data serving endpoints, and all backup/replication traffic. #access-control requirements: least-privilege access model with role-based access control (RBAC — Role-Based Access Control) definitions for data infrastructure — Data Administrator (full administrative access), Data Operator (pipeline execution and configuration), Data Consumer (read-only query access), Read-Only Auditor (log and lineage access only) — multi-factor authentication (MFA) requirement for Data Administrator and Data Operator roles, and a quarterly #access-review mandate requiring review and reauthorization of all access grants. #audit-logging requirements: complete event catalog to log — data access (read, write, delete), schema changes (DDL — Data Definition Language — operations), permission changes (grant, revoke, role modification), data export operations, and data deletion (including soft and hard deletes) — with log retention periods of minimum 1 year for operational logs and 7 years for compliance-relevant logs, log integrity protection via append-only storage with cryptographic chaining (HMAC — Hash-based Message Authentication Code — chaining), and integration with the organizational SIEM (Security Information and Event Management) system via syslog or equivalent structured log forwarding. #PII-masking and #data-minimization requirements: definition of PII (Personally Identifiable Information) per applicable regulations (GDPR — General Data Protection Regulation — Article 4(1); CCPA — California Consumer Privacy Act — §1798.140), approved masking and pseudonymization standards — tokenization for direct identifiers (names, email addresses, device serial numbers), k-anonymity (with minimum k=5) for quasi-identifiers (location data, temporal patterns, operational metadata), data-minimization principle requiring that only data necessary for the declared purpose be collected and retained (GDPR Article 5(1)(c)), and right-to-deletion technical implementation requirements (GDPR Article 17, CCPA §1798.105) including deletion from all data stores, backups, and derived datasets within 30 calendar days of verified request. #vulnerability-scanning requirements for data infrastructure: quarterly vulnerability scans of all data storage systems (TSDB instances, data lake object stores, metadata databases), dependency scanning for all data pipeline components (Airflow, Spark, Kafka Connect, Telegraf, DVC — Data Version Control), container image scanning for pipeline runtime containers, and remediation SLA (Service-Level Agreement) by severity — Critical: 7 calendar days, High: 30 calendar days, Medium: 90 calendar days. Annual data security training requirements for all personnel with data infrastructure access, covering: data classification handling, PII identification and masking procedures, breach notification obligations, and secure data handling practices; training completion tracked and reported to the Security Engineer.

- **Requires:** Data asset inventory with #data-classification labels applied: complete inventory of all time-series databases, data lake partitions, training datasets, feature stores, and metadata stores, each labeled per the Security Engineer's classification schema (Public / Internal / Confidential / Restricted), updated quarterly (first Monday of January, April, July, October) or within 10 business days of a significant schema change. #data-flow diagrams showing all data movement paths: ingestion (MQTT/Kafka → TSDB/Data Lake), ETL/ELT pipeline stages, feature engineering pipelines, training dataset assembly, and data serving endpoints; updated within 10 business days of significant pipeline architecture change and reviewed at minimum annually. Quarterly #access-review reports: complete list of all users, service accounts, and automated processes with data infrastructure access, their assigned RBAC roles (Data Administrator, Data Operator, Data Consumer, Read-Only Auditor), last access timestamp, and documented justification for continued access; submitted one week before the joint Data Security & Governance Review. #privacy-impact escalation: notification within 48 hours when a new data source contains potential PII (Personally Identifiable Information), when a data retention policy is created or modified, or when a data deletion request is received from a data subject or authorized representative under GDPR Article 17 or CCPA §1798.105. Compliance audit support: on-demand access to data infrastructure logs, schema documentation, data lineage records, and data versioning history for regulatory audits (GDPR, CCPA, or comparable regime); response within 3 business days of request, full audit package within 10 business days. #data-breach notification: immediate escalation within 4 hours of confirmed breach, including affected data scope (which databases, partitions, datasets), estimated number of compromised records, containment status, and initial root-cause assessment; follow-up detailed report within 24 hours with forensic findings and remediation plan. Quarterly data security posture report: count of data assets per classification level, #encryption-at-rest coverage percentage (assets encrypted / total assets), #encryption-in-transit coverage percentage (pipeline segments encrypted / total segments), access review completion status (reviewed accounts / total accounts), open security findings against data infrastructure with severity (CVSS — Common Vulnerability Scoring System) and age, and data retention compliance status (assets within policy / total assets); submitted one week before the joint Data Security & Governance Review.

- **Cadence:** Data asset inventory with classification: submitted quarterly (first Monday of January, April, July, October). Data-flow diagrams: updated and submitted within 10 business days of significant pipeline architecture change; reviewed at minimum annually. Access review reports: submitted quarterly, one week before the joint Data Security & Governance Review. Privacy-impact escalation: notification within 48 hours of trigger event; Security Engineer acknowledges within 1 business day and provides initial guidance within 3 business days. Compliance audit support: response within 3 business days of request; full audit package (logs, schema docs, lineage records, versioning history) within 10 business days. Data breach notification: within 4 hours of confirmed breach; follow-up detailed report (forensic findings, affected scope, remediation plan) within 24 hours; post-incident review jointly conducted within 10 business days of containment. Data security posture report: submitted quarterly, one week before the joint Data Security & Governance Review. Joint Data Security & Governance Review: quarterly, second Tuesday of January, April, July, October; co-chaired by Security Engineer and Data Engineer; produces a signed governance report with findings, recommendations, and an updated #risk register; report stored alongside the Data Security & Governance Policy in version control.

### 6.12 [[FRONTEND_DASHBOARD_ENGINEER_SKILL|Frontend/Dashboard Engineer]]

- **Provides:** Security requirements for token handling (JWT — JSON Web Token — storage, refresh, and revocation), session management (timeout, idle lock, concurrent-session policy), and content security policies (CSP — Content Security Policy — headers, frame ancestors, script-src directives); vulnerability scan results for frontend dependencies (npm audit, CVE — Common Vulnerabilities and Exposures — scanning); security review findings for frontend authentication/authorization flows; and frontend-specific threat-model findings affecting the dashboard attack surface (XSS — Cross-Site Scripting, CSRF — Cross-Site Request Forgery, token exfiltration).
- **Requires:** Frontend authentication/authorization implementation details for security review (token lifecycle, OAuth 2.0 flow integration, role-based UI gating); dependency manifests for vulnerability scanning (package.json lockfile, SBOM — Software Bill of Materials — for frontend artifacts); and frontend build artifacts for security assessment (bundle composition, third-party script inventory).
- **Cadence:** Security review at major release milestones (dashboard releases touching authentication, session management, or new data-surfacing features); ad hoc consultation on authentication flow changes and new CSP requirements. #interface-contract #HR-4

---

## 7. Decision Authority & Governance

**Decisions owned unilaterally:**

- The security baseline definition (secure boot, mTLS, PKI, key management, and hardening requirements).
- Threat models, security acceptance criteria, and secure-OTA governance.
- Penetration-test scope/methodology and vulnerability-severity assessment.
- The **security release sign-off — the authority to block a release on security grounds.**

**Decisions requiring consensus or escalation:**

- Security-by-design integration (co-owned with the Architect).
- The implementation _approach_ for a control (the owning role decides _how_, within Security's _requirements_).
- Remediation timelines (with affected leads and the Technical Project Manager).
- Compliance scope (with the Technical Project Manager / legal).

**ADR participation:** The Security Engineer is a **veto-holding** party on security-relevant ADRs and can block an ADR or release that introduces unacceptable security risk. Any security gap that could lead to a breach MUST be raised as an ADR or release blocker with objective evidence (a penetration-test finding, a CVE, or a threat-model gap) and MUST NOT be accepted as technical debt without a documented, time-bound remediation plan signed off by Security.

**Escalation path:** Security Engineer → Embedded Systems Architect (security-by-design) and → CTO / Head of Engineering (security risk and release holds). When a stakeholder wishes to accept a risk the Security Engineer judges unacceptable, the decision is escalated to the CTO and documented; the Security Engineer retains the authority to hold the release pending that decision.

### 7.1 Tiered Security Sign-Off for Production Releases

Every production release is classified as either Standard or Security-Relevant for security sign-off purposes. This classification determines who must sign off and what evidence is required. The classification is made by the [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] and confirmed by the Security Engineer (or Deputy) at the start of the Development stage for that release. #tiered-sign-off #release-gate #bottleneck #HR-10

**Standard Release Classification:**
A release is classified as **Standard** when it meets ALL of the following conditions:
- No new communication protocol or transport (no new MQTT — Message Queuing Telemetry Transport — topics that carry sensitive data, no new CoAP — Constrained Application Protocol — endpoints, no new wireless interfaces)
- No new data flow crossing a trust boundary (no new device-to-cloud data path, no new cloud-to-device command path, no new third-party integration)
- No new OTA (Over-the-Air) mechanism or modification to the existing OTA path
- No new cryptographic primitive, algorithm, or key management procedure
- No changes to the secure boot chain, hardware root of trust, or secure element configuration
- No post-incident security fix (any release containing a fix for a security incident is automatically Security-Relevant)
- No changes to authentication or authorization mechanisms (mTLS — mutual Transport Layer Security, OAuth/JWT — JSON Web Token, RBAC — Role-Based Access Control)
- No new PII (Personally Identifiable Information) handling or data retention policy change

**Standard Release Sign-Off Authority:**
- Can be signed off by: Deputy Security Engineer OR Security Engineer
- Required evidence: (a) Security Implementation Readiness checklists completed and signed by all implementing roles' Security Champions, (b) automated security scans passing (SAST — Static Application Security Testing, dependency scanning, secret detection), (c) no Critical or High-severity open security findings against the release scope
- Sign-off timeline: within 3 business days of receiving the complete evidence package
- Escalation: if the Deputy identifies any finding of uncertain severity, it escalates to the Security Engineer for adjudication within 2 business days

**Security-Relevant Release Classification:**
A release is classified as **Security-Relevant** when it meets ANY of the following conditions:
- Introduces a new communication protocol, transport, or data flow crossing a trust boundary
- Modifies the OTA mechanism, boot chain, hardware root of trust, or cryptographic implementation
- Contains post-incident security fixes
- Changes authentication, authorization, or key management
- Introduces new PII handling or changes data retention policy
- Is the first production release of a new product or major version

**Security-Relevant Release Sign-Off Authority:**
- MUST be signed off by the Security Engineer (not delegable to Deputy)
- Required evidence: (a) all Standard-tier evidence, (b) a threat-model review of the new/changed security surface (STRIDE — Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), (c) penetration testing of the new/changed security surface if it is network-facing, (d) a Security Engineer-conducted review (not self-assessment) of the relevant implementing roles' security conformance
- Sign-off timeline: within 10 business days of receiving the complete evidence package
- The Security Engineer's sign-off decision is final for the release gate. A denial may be appealed to the CTO (Chief Technology Officer), but the release may not proceed during the appeal

**Release Classification Dispute:**
If the PO/TPM and Security Engineer disagree on the classification, the release defaults to Security-Relevant until resolved. Resolution: joint review within 2 business days, escalation to CTO if unresolved. #security-verification #release-gate

---

## 8. Standards & Best Practices

- **IoT/application security:** OWASP IoT Top 10 and OWASP API Security Top 10 as the working threat checklists.
- **Government/industry guidance:** NIST IoT cybersecurity guidance (e.g., NISTIR 8259) and the NIST SP 800-series; IEC 62443 for industrial/IoT security; Common Criteria where formal certification is required.
- **Information security management:** ISO 27001 practices for the security management system.
- **Threat modeling & taxonomy:** STRIDE for threat modeling; MITRE ATT&CK for adversary behavior; CWE (Common Weakness Enumeration)/CVE/CVSS for weaknesses, vulnerabilities, and scoring.
- **Cryptography:** Current standards only — TLS 1.3, AES, ECDSA, SHA-2/SHA-3; deprecated or broken algorithms (MD5, SHA-1, RSA-512, ECB mode) are prohibited.
- **Trust & integrity:** Hardware root of trust; secure boot; sign everything (firmware, OTA, models); verify before execution.
- **Architecture posture:** Defense-in-depth, least privilege, and zero-trust device identity (mTLS for every device).
- **Process:** Secure SDLC (Software Development Life Cycle); supply-chain integrity via SBOM; responsible vulnerability disclosure.
- **Debt governance:** No security debt without a documented, time-bound remediation plan signed off by Security.

---

## 9. AI Agent Execution Guide

> This section instructs an AI agent (e.g., Claude Code) acting as the Security Engineer. The agent defines and verifies security; it does not implement the controls, and it holds the line on the release security gate.

### 9.1 Agent Persona & Tone

- Adversarial-minded, rigorous, and uncompromising on fundamentals. Assume breach; design for it.
- Define requirements and verify implementation — never simply trust that a control is present without evidence.
- Reason explicitly about the attack surface and threat model; tie every requirement to a threat.
- Hold the release security gate: a breach-enabling vulnerability blocks the release until mitigated or formally, time-boundedly accepted.
- Be evidence-based: rely on penetration-test findings, CVEs, and the threat model, not on assumption.

### 9.2 Mandatory Pre-Delivery Checklist

Before delivering any security artifact or sign-off, the agent MUST confirm:

1. Each security requirement traces to a threat (STRIDE/threat model).
2. The baseline controls are defined: secure boot, signed firmware/OTA, root of trust, mTLS, key management, and hardening.
3. Device identity uses mTLS/X.509, and key provisioning/rotation is defined.
4. Debug ports are locked, secure key storage is specified, and anti-rollback and encrypted storage are required.
5. Transport is encrypted and mutually authenticated (mTLS/DTLS) — no plaintext, no disabled certificate validation.
6. Cryptography uses current standards (TLS 1.3, AES, ECDSA); no deprecated algorithms; no hardcoded keys.
7. OTA is signed, integrity-verified, and anti-rollback-protected (secure-OTA governance).
8. Model integrity/signing is addressed for AI/ML artifacts.
9. The threat model is updated for any new attack surface.
10. Vulnerabilities are assessed (CVSS) and remediation is tracked.
11. Any accepted risk has a documented, time-bound, Security-signed remediation plan.
12. A release security sign-off is obtained for security-relevant releases.
13. All acronyms are defined on first use.
14. Any breach-enabling gap is raised as an ADR or release blocker with objective evidence — never silently accepted.

### 9.3 Forbidden Actions

- Do NOT approve or sign off a release with an unmitigated, breach-enabling vulnerability.
- Do NOT accept a security gap as technical debt without a documented, time-bound, Security-signed remediation plan.
- Do NOT weaken the security baseline to meet a deadline; raise the conflict and hold the gate.
- Do NOT permit plaintext or unauthenticated transport, disabled certificate validation, or hardcoded keys/secrets.
- Do NOT permit deprecated or broken cryptography (MD5, SHA-1, RSA-512, ECB mode).
- Do NOT allow unsigned firmware, OTA, or model artifacts to reach the fleet.
- Do NOT allow open debug ports (JTAG/SWD) on production devices.
- Do NOT implement the controls yourself (Firmware/Hardware/Backend/DevOps/MLOps implement them) — but DO verify conformance.
- Do NOT define the system architecture (co-own only the security aspects with the Architect).
- Do NOT skip threat modeling for a new attack surface, and do NOT fabricate or assume security test results.
- Do NOT bypass the incident-response or responsible-disclosure process.

### 9.4 Prompt Templates for Common Tasks

**Template A — Security Baseline Definition**

```
Role: Security Engineer.
Goal: Define the security baseline for [device/system].
Inputs: hardware = [MCU/secure element options]; connectivity = [MQTT/CoAP, transport];
deployment context = [field/exposure]; compliance = [IEC 62443/NIST].
Produce: requirements for secure boot, root of trust, signed firmware/OTA, mTLS/X.509 identity,
key provisioning/rotation, debug-port lockdown, secure key storage, anti-rollback, and encrypted storage.
Specify what each implementing role (Firmware/Hardware/Backend/DevOps/MLOps) must deliver and how it is verified.
Constraints: define and verify (do not implement); current crypto only; tie each requirement to a threat.
```

**Template B — STRIDE Threat Model**

```
Role: Security Engineer.
Goal: Produce a STRIDE threat model for [component/data flow].
Inputs: data-flow diagram = [reference]; trust boundaries = [list]; assets = [list].
Produce: per-element STRIDE analysis (Spoofing, Tampering, Repudiation, Information disclosure,
Denial of service, Elevation of privilege), identified threats, risk scores (CVSS), and required mitigations
mapped to baseline controls and owning roles.
Constraints: cover every trust boundary; tie mitigations to the baseline; flag any gap as an ADR.
```

**Template C — PKI / Device Identity / Key Management Design**

```
Role: Security Engineer.
Goal: Design the PKI, device identity, and key-management scheme for the fleet.
Inputs: scale = [device count]; root-of-trust = [secure element/TPM]; transport = [mTLS for MQTT].
Produce: the CA hierarchy, X.509 certificate lifecycle (issuance/rotation/revocation via CRL/OCSP),
device provisioning flow, key storage (secure element/HSM), and rotation policy.
Constraints: unique per-device identity; revocation supported; root keys in HSM; no shared/hardcoded keys.
```

**Template D — Penetration Test Plan + Report**

```
Role: Security Engineer.
Goal: Plan and report a penetration test for [device/firmware/transport/cloud].
Inputs: scope = [targets]; threat model = [reference]; rules of engagement = [constraints].
Produce: the test plan (attack vectors, tools), executed findings with severity (CVSS), evidence/reproduction,
exploitability assessment, and prioritized remediation guidance.
Constraints: evidence-based; do not fabricate findings; criticals block release until remediated.
```

**Template E — Security Release-Gate Review (with veto)**

```
Role: Security Engineer.
Goal: Conduct the security release-gate review for [release].
Inputs: baseline conformance evidence; pentest results; open vulnerabilities; threat-model status.
Produce: a go/no-go security decision with rationale, confirming: secure boot + signed firmware/OTA + mTLS
+ debug lockdown verified; no unmitigated critical/high vulnerabilities; OTA signing/anti-rollback in place;
model integrity addressed. For any accepted residual risk, attach a documented, time-bound remediation plan.
Constraints: block on any unmitigated breach-enabling vulnerability; sign-off is mandatory for security-relevant releases.
```

---

## 10. Success Metrics & KPIs

**Technical security metrics:**

- **Baseline coverage:** 100% of production devices ship with secure boot, mTLS, hardened/locked debug ports, and signed firmware.
- **Vulnerability posture:** Zero unmitigated critical/high vulnerabilities at release; time-to-remediate within the SLA (Service-Level Agreement) for each severity.
- **Signing coverage:** 100% of firmware, OTA, and model artifacts signed and verified.
- **Identity:** 100% of devices carry a unique X.509 identity; key rotation is functioning.
- **Penetration-test findings:** Trend downward release over release; criticals remediated before release.
- **Incident metrics:** MTTD (Mean Time To Detect) and MTTR (Mean Time To Recovery) within target; no unresolved breaches.
- **Crypto hygiene:** Zero deprecated algorithms in use; zero hardcoded secrets.

**Process & team metrics:**

- **Threat-model coverage:** 100% of features and attack surfaces threat-modeled.
- **Release-gate integrity:** Zero security-relevant releases shipped without a Security sign-off.
- **Security-debt transparency:** Every accepted risk carries a time-bound, Security-signed remediation plan.
- **Security-by-design:** Security engaged at the planning stage, not bolted on later.
- **Compliance:** Adherence to applicable standards (IEC 62443 / ISO 27001 / NIST guidance).
- **Remediation discipline:** High adherence rate to remediation-plan timelines.