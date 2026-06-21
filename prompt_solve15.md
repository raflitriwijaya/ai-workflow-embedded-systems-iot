# [SYSTEM]

You are a senior embedded security architect and device attestation specialist with 20+ years of experience designing hardware-rooted attestation systems for IoT fleets. You have built attestation frameworks for automotive ECUs, smart grid meters, industrial sensors, and medical devices. You understand that the integrity of an IoT fleet depends on a fundamental question: "Can we trust what this device reports?" — and that without cryptographic attestation, the answer is always "we assume so." Review Part 2 Phase 4 identified Hidden Assumption HA-A3: "Field devices report truthfully." A compromised device that lies about its state, its firmware version, its model version, or its sensor data corrupts every downstream system that trusts that data — fleet monitoring, OTA targeting, drift detection, and incident response. You are now designing the Device Attestation Specification that closes this assumption. Output is fully Obsidian-compatible.

# [TASK]

Design the **Device Attestation Specification** — a cryptographic attestation framework that enables the fleet management plane to verify, not merely trust, the integrity and authenticity of device-reported state. This specification defines what is attested, how attestation works, how it integrates with the existing secure boot chain and hardware root of trust, and what changes are needed in the implementing roles. Save to `docs/security/DEVICE_ATTESTATION_SPEC.md`.

# [CONTEXT]

The [[REVIEW_V2_PHASE4_EMERGENT|Phase 4]] Stress Scenario 4 (Fleet-Scale Incident) revealed that the fleet-management plane reconciles the device twin against what devices *report*. A compromised device that *lies* corrupts fleet-wide state silently. The detection mechanism for this — cross-source reconciliation — was recommended as P4-M5.

The ecosystem already has foundational security infrastructure that enables attestation:

- **Secure Boot Chain:** [[SECURITY_ENGINEER_SKILL|Security Engineer]] defines it; [[FIRMWARE_ENGINEER_SKILL|Firmware Engineer]] implements it (MCUboot, image signing, signature verification)
- **Hardware Root of Trust:** Secure element (ATECC608, SE050) or ARM TrustZone, integrated by [[HARDWARE_ENGINEER_SKILL|Hardware Engineer]]
- **Device Identity:** X.509 certificates, mTLS for MQTT/CoAP, key provisioning and rotation — defined by Security, implemented by Firmware and [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]]
- **OTA Integrity:** A/B partitioning with rollback, signed firmware and model artifacts, compatibility manifests, flash-budget checks — governed by the OTA Model Artifact Contract
- **Device Twin:** Desired/reported state managed by Backend, reconciled against device-reported status

Attestation extends this foundation by making device-reported state *verifiable*. Rather than a device simply reporting "I am running firmware v2.3.1, model v4.2.0," the device provides cryptographic proof — a signed attestation token — that can be verified by the Backend without trusting the device.

**What is attested (minimum):**

1. **Firmware identity and integrity:** The device is running an authentic, untampered firmware image. The attestation token includes a hash of the active firmware image, signed by the secure element.
2. **Model identity and integrity:** The on-device ML model is the authentic, signed model artifact. The attestation token includes the model version and hash.
3. **Secure boot state:** The device booted through the full secure boot chain with no verification failures. The attestation token includes the boot state from the secure element.
4. **Device configuration integrity:** Critical configuration (security settings, debug port state, OTA partition state) has not been tampered with.
5. **Sensor pipeline integrity (stretch goal):** The path from sensor to telemetry emission is untampered — sensor data has not been injected, replayed, or modified by compromised middleware.

**Attestation protocol:**

- **Challenge-Response:** The Backend (or DevOps fleet management) sends an attestation challenge (random nonce) to the device. The device's secure element generates an attestation token binding the challenge to the device's measured state, signed with the device's private key (rooted in the hardware root of trust). The Backend verifies the token using the device's public key.
- **Periodic Attestation:** Devices generate and report attestation tokens periodically (e.g., once per day, on every reboot, on every OTA apply). These tokens are stored alongside device telemetry for audit.
- **Event-Triggered Attestation:** Attestation is triggered on: (a) device reboot, (b) OTA apply (firmware or model), (c) detection of anomalous device behavior (by fleet monitoring), (d) Backend on-demand challenge.

**Integration with existing infrastructure:**

- **Device Twin:** The attestation state (last attested firmware version, last attested model version, last attested boot state, last attestation timestamp) is added to the device twin as reported properties.
- **Fleet Monitoring:** [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] monitors attestation failures across the fleet. A device that fails attestation is quarantined (removed from active fleet, OTA paused, alerts fired).
- **Incident Response:** Attestation failure is a security incident. The [[SECURITY_ENGINEER_SKILL|Security Engineer]] and Incident Commander are notified within 5 minutes.

# [OUTPUT FORMAT]

Generate `docs/security/DEVICE_ATTESTATION_SPEC.md` with this structure:

```yaml
---
title: "Device Attestation Specification"
date: 2026-06-21
status: draft
version: "1.0"
owner: "[[SECURITY_ENGINEER_SKILL]]"
contributors:
  - "[[FIRMWARE_ENGINEER_SKILL]]"
  - "[[HARDWARE_ENGINEER_SKILL]]"
  - "[[BACKEND_CLOUD_ENGINEER_SKILL]]"
  - "[[DEVOPS_PLATFORM_ENGINEER_SKILL]]"
tags:
  - attestation
  - security
  - device-integrity
  - hardware-root-of-trust
cssclass: security-spec
---
```

````markdown
# Device Attestation Specification

> **Owner:** [[SECURITY_ENGINEER_SKILL|Security Engineer]]
> **Status:** Draft — Long-Term Bet
> **Closes:** HA-A3 ("Field devices report truthfully") from [[REVIEW_V2_PHASE4_EMERGENT|Phase 4]]
> **References:** [[SECURITY_ENGINEER_SKILL|Security Baseline]], System Robustness Contract, OTA Model Artifact Contract

---

## 1. Purpose and Scope

[Why attestation matters: it closes the "trust what devices report" assumption. What is in scope: firmware integrity, model integrity, boot state, configuration integrity. What is out of scope for V1: sensor pipeline integrity (future).]

## 2. Attestation Architecture

[High-level architecture with a Mermaid sequence diagram showing: Backend challenges device → Device secure element generates attestation token → Device reports token to Backend → Backend verifies token → Backend updates device twin → Fleet monitoring detects attestation failure → Security incident triggered.]

## 3. Attested Properties

[For each of the 5 attested properties, define: what is measured, how it is measured, what the measurement is compared against (reference value), and what constitutes a pass/fail.]

## 4. Attestation Token Format

[Define the exact structure of the attestation token: header (version, device ID, timestamp), challenge (nonce from Backend), measurements (firmware hash, model hash, boot state, config hash), metadata (secure element identity, signing algorithm), and signature. Specify encoding (CBOR or ASN.1 DER). Reference existing standards: IETF RATS (Remote ATtestation ProcedureS), TCG DICE (Device Identifier Composition Engine).]

## 5. Attestation Protocol

### 5.1 Challenge-Response Protocol

[Step-by-step protocol: Backend generates nonce → sends challenge to device → device secure element performs measurements → generates token → signs → device returns token to Backend → Backend verifies signature → Backend verifies measurements against reference values → Backend records result.]

### 5.2 Periodic Attestation

[Default interval, how it co-exists with normal telemetry, how tokens are stored.]

### 5.3 Event-Triggered Attestation

[Triggers: reboot, OTA apply, anomaly detection, on-demand. Priority escalation for event-triggered attestation.]

## 6. Integration with Existing Infrastructure

[How attestation integrates with: secure boot chain (MCUboot), hardware root of trust (ATECC608/SE050/TrustZone), device identity (X.509 certificates), device twin (new reported properties), fleet monitoring (new alerts and dashboards), OTA pipeline (attestation before and after OTA apply), incident response (attestation failure = security incident).]

## 7. Role-Specific Requirements

[A table mapping each affected role to its attestation responsibilities. [[HARDWARE_ENGINEER_SKILL|Hardware]]: secure element provisioning and integration. [[FIRMWARE_ENGINEER_SKILL|Firmware]]: attestation token generation, secure element API, boot measurement. [[SECURITY_ENGINEER_SKILL|Security]]: attestation policy, reference values, key management. [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]]: challenge generation, token verification, device twin attestation state. [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]]: fleet attestation monitoring, quarantining, alerting.]

## 8. Threat Model

[What threats does attestation address? What threats does it NOT address? Attestation prevents: firmware tampering, unauthorized OTA, model substitution, configuration tampering. Attestation does NOT prevent: physical attacks on the secure element itself, side-channel attacks, compromised sensors at the analog level, supply chain attacks before the root of trust is provisioned.]

## 9. Implementation Phases

[Phase 1: Firmware attestation only (boot state + firmware hash). Phase 2: Add model attestation. Phase 3: Add configuration attestation. Phase 4 (stretch): Sensor pipeline attestation.]

## 10. References

[IETF RATS RFC 9334, TCG DICE, NIST SP 800-155 (BIOS Integrity Measurement), GlobalPlatform TEE, PSA Certified, CSA IoT Security Controls.]
````

# [CONSTRAINTS]

- ALL role references MUST use correct Obsidian `[[wikilinks]]`
- ALL tags in kebab-case: #attestation #device-integrity #hardware-root-of-trust #long-term-bet #HA-A3
- The Mermaid sequence diagram must be syntactically valid
- The attestation token format must reference existing standards (IETF RATS, TCG DICE) — do not invent a proprietary format
- The spec must be implementable on the target hardware classes: MCU-class (STM32/ESP32 with ATECC608 or SE050) and MPU-class (Raspberry Pi with TPM or TrustZone)
- Role-specific requirements must be concrete — what each role must do, not "coordinate with other roles"
- Threat model must honestly state what attestation does NOT protect against
- The implementation phases must be achievable within the existing ecosystem — Phase 1 must not require hardware changes
- DEFINE every acronym on first use
