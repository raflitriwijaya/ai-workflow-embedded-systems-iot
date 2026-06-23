---
title: "Acronym Glossary — Embedded/IoT AI Workflow Ecosystem"
date: 2026-06-22
status: final
tags:
  - reference
  - embedded-iot
  - glossary
cssclass: reference
---

# ACRONYM_GLOSSARY.md

> Authoritative acronym glossary for the Embedded/IoT AI Workflow Engineering ecosystem. Moved here from `CLAUDE.md` Appendix C to keep the master reference under its size budget. Every technical acronym must be defined on first use in each section (see `CLAUDE.md` §3.10); this table records the canonical expansion and the document where each is first defined.

| Acronym | Expansion | First defined in |
|---|---|---|
| A2A | Agent-to-Agent | `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` |
| ADR | Architecture Decision Record | Any SKILL.md §7; schema: `docs/schemas/ADR_SCHEMA.md` |
| AID | Agent Identity Document | `docs/agent-protocol/AGENT_IDENTITY_SCHEMA.md` |
| ARB | Architecture Review Board | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §7.Z |
| BIA | Business Impact Assessment | `docs/schemas/BUSINESS_IMPACT_ASSESSMENT_SCHEMA.md` |
| BLE | Bluetooth Low Energy | `HARDWARE_ENGINEER_SKILL.md`, `FIRMWARE_ENGINEER_SKILL.md` |
| CBOR | Concise Binary Object Representation | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| CCR | Contract Clarification Record | `docs/schemas/CCR_SCHEMA.md` |
| CI/CD | Continuous Integration / Continuous Delivery | `DEVOPS_PLATFORM_ENGINEER_SKILL.md` |
| CMSIS-NN | Cortex Microcontroller Software Interface Standard — Neural Network | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| CoAP | Constrained Application Protocol | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| CVSS | Common Vulnerability Scoring System | `SECURITY_ENGINEER_SKILL.md` |
| CVE | Common Vulnerabilities and Exposures | `SECURITY_ENGINEER_SKILL.md` |
| CWE | Common Weakness Enumeration | `SECURITY_ENGINEER_SKILL.md` |
| DICE | Device Identifier Composition Engine | `docs/security/DEVICE_ATTESTATION_SPEC.md` |
| DID | Decentralized Identifier | `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` |
| DQIR | Data Quality Issue Report | `docs/schemas/DQIR_SCHEMA.md` |
| DVC | Data Version Control | `MLOPS_ENGINEER_SKILL.md` |
| EAT | Entity Attestation Token | `docs/security/DEVICE_ATTESTATION_SPEC.md` |
| EMC | Electromagnetic Compatibility | `HARDWARE_ENGINEER_SKILL.md` |
| EPR | Engineering Process Review | `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` §3.7 |
| ESP-IDF | Espressif IoT Development Framework | `FIRMWARE_ENGINEER_SKILL.md` |
| FC | Failure Chain | `docs/fmea/SYSTEM_FMEA_V1.md` |
| FFT | Fast Fourier Transform | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| FMEA | Failure Modes and Effects Analysis (IEC 60812) | `docs/fmea/SYSTEM_FMEA_V1.md` |
| FTA | Fault Tree Analysis (IEC 61025) | `docs/fmea/SYSTEM_FMEA_V1.md` |
| GTM | Go-to-Market | `BUSINESS_CONSULTANT_SKILL.md` |
| HAL | Hardware Abstraction Layer | `FIRMWARE_ENGINEER_SKILL.md` |
| HIL | Hardware-in-the-Loop | `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` |
| HITL | Human-in-the-Loop | `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` |
| HG | Human Gate (e.g., HG-01 Security veto, HG-04 Architect gate) | `docs/review_v2/REVIEW_V2_PHASE3_AI_AGENT.md` |
| IC | Incident Commander | `docs/operations/INCIDENT_COMMANDER.md` |
| INT8 | 8-bit integer quantization | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| IP | Intellectual Property | `IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md` |
| IRD | Integration Readiness Declaration | `docs/schemas/INTEGRATION_READINESS_DECLARATION_SCHEMA.md` |
| IPC | Inter-Process Communication (also: Institute for Printed Circuits, context-dependent) | `FIRMWARE_ENGINEER_SKILL.md` |
| KPI | Key Performance Indicator | All SKILL.md §10 |
| LoRaWAN | Long Range Wide Area Network | `HARDWARE_ENGINEER_SKILL.md`, `FIRMWARE_ENGINEER_SKILL.md` |
| LWT | Last Will and Testament (MQTT connection parameter) | `BACKEND_CLOUD_ENGINEER_SKILL.md` |
| MACP | Multi-Agent Coordination Protocol | `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` |
| MCU | Microcontroller Unit | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| MFCC | Mel-Frequency Cepstral Coefficient | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| MQTT | Message Queuing Telemetry Transport | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| mTLS | Mutual TLS (Transport Layer Security) | `BACKEND_CLOUD_ENGINEER_SKILL.md`, `SECURITY_ENGINEER_SKILL.md` |
| NFR | Non-Functional Requirement | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §5 |
| NIST | National Institute of Standards and Technology | Multiple §8 sections |
| OKR | Objectives and Key Results | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` |
| ONNX | Open Neural Network Exchange | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| OTA | Over-the-Air (firmware/model update) | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| OCM | OTA Compatibility Manifest | `docs/schemas/OTA_COMPATIBILITY_MANIFEST_SCHEMA.md` |
| OWASP | Open Web Application Security Project | `SECURITY_ENGINEER_SKILL.md` |
| PCB | Printed Circuit Board | `HARDWARE_ENGINEER_SKILL.md` |
| PKI | Public Key Infrastructure | `SECURITY_ENGINEER_SKILL.md` |
| PO | Product Owner (also TPM: Technical Project Manager) | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` |
| PSRAM | Pseudo-Static RAM | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| RATS | Remote Attestation Procedures (IETF RFC 9334) | `docs/security/DEVICE_ATTESTATION_SPEC.md` |
| RPN | Risk Priority Number (FMEA: Severity × Occurrence × Detectability) | `docs/fmea/SYSTEM_FMEA_V1.md` |
| RTOS | Real-Time Operating System | `FIRMWARE_ENGINEER_SKILL.md` |
| SemVer | Semantic Versioning | §5 of all SKILL.md files |
| SHA-256 | Secure Hash Algorithm, 256-bit | `docs/agent-protocol/COORDINATION_LEDGER_SCHEMA.md` |
| SIRC | Security Implementation Readiness Checklist | `docs/schemas/SECURITY_IMPLEMENTATION_READINESS_SCHEMA.md` |
| SLA | Service Level Agreement | `BACKEND_CLOUD_ENGINEER_SKILL.md`, MACP |
| SNR | Signal-to-Noise Ratio | `HARDWARE_ENGINEER_SKILL.md` |
| SoC | System-on-Chip | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| SRAM | Static Random-Access Memory | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| STRIDE | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege | `SECURITY_ENGINEER_SKILL.md` |
| TFLite Micro | TensorFlow Lite for Microcontrollers | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| TinyML | Machine learning on ultra-constrained microcontrollers | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| TPM | Trusted Platform Module (note: in `SECURITY_ENGINEER_SKILL.md`, this means hardware security module, NOT Technical Project Manager) | `SECURITY_ENGINEER_SKILL.md` §1 (explicit disambiguation note) |
| TPM (disambiguation) | Technical Project Manager — in `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` §1 |
| TRL | Technology Readiness Level | `IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md`, TTP schema |
| TSC | Technical Steering Committee | Project memory / phase governance |
| TTP | Technology Transfer Pack | `docs/schemas/TECHNOLOGY_TRANSFER_PACK_SCHEMA.md` |
| TTL | Time To Live | `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` |
| UUID | Universally Unique Identifier | `docs/agent-protocol/AGENT_IDENTITY_SCHEMA.md` |
| YAML | YAML Ain't Markup Language | Frontmatter in all vault documents |
