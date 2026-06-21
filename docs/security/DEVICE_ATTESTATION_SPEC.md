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
  - long-term-bet
  - HA-A3
cssclass: security-spec
---

# Device Attestation Specification

> **Owner:** [[SECURITY_ENGINEER_SKILL|Security Engineer]]
> **Status:** Draft — Long-Term Bet
> **Closes:** HA-A3 ("Field devices report truthfully") from [[REVIEW_V2_PHASE4_EMERGENT|Phase 4]]
> **References:** [[SECURITY_ENGINEER_SKILL|Security Baseline]], System Robustness Contract, OTA Model Artifact Contract, [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OTA Compatibility Manifest Schema]]

#attestation #device-integrity #hardware-root-of-trust #long-term-bet #HA-A3

---

## 1. Purpose and Scope

### 1.1 The assumption being closed

The [[REVIEW_V2_PHASE4_EMERGENT|Phase 4 emergent review]] named **HA-A3 — "Devices report truthfully"** as one of three high-impact, *low-detectability* hidden assumptions. The fleet-management plane reconciles the [[BACKEND_CLOUD_ENGINEER_SKILL|device twin]] against what each device **says** its state is. The [[REVIEW_V2_PHASE4_EMERGENT#7.4 Scenario 4 — Fleet-Scale Incident|Fleet-Scale Incident]] scenario showed the consequence: a compromised device that *lies* about its firmware version, model version, boot state, or configuration corrupts fleet-wide reconciliation **silently** — falsified state looks normal, so the incident-response picture is assembled on top of a false premise. Recommendation **P4-M5** ("treat device-reported state as untrusted at fleet scale — attestation, cross-source reconciliation") is the remediation this specification delivers.

Device attestation converts *trust* into *verification*. Today a device asserts "I am running firmware v2.3.1, model v4.2.0"; with attestation the device presents a **cryptographic proof** — a signed attestation token, rooted in the hardware Root of Trust (RoT) — that the fleet plane can verify **without trusting the device's own narration**.

> **Internet of Things (IoT):** the networked fleet of edge devices this ecosystem manages.
> **Hidden Assumption (HA):** a premise the design relies on but does not test; if false, the system is not told.
> **Root of Trust (RoT):** the hardware element (secure element or Trusted Execution Environment) whose integrity is assumed axiomatically and from which all other trust is derived.

### 1.2 In scope (V1)

1. **Firmware identity and integrity** — the device runs an authentic, untampered firmware image.
2. **Model identity and integrity** — the on-device Machine Learning (ML) model is the authentic, signed artifact named in the [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OTA Compatibility Manifest]].
3. **Secure boot state** — the device booted through the full secure boot chain with no verification failures.
4. **Device configuration integrity** — critical configuration (security settings, debug-port state, Over-the-Air partition state) is untampered.

### 1.3 Out of scope for V1 (deferred to a later phase)

5. **Sensor pipeline integrity** — proof that the path from physical sensor to telemetry emission has not injected, replayed, or modified data. This is the stretch goal in [[#9 Implementation Phases|§9, Phase 4]]; it is explicitly *not* part of V1 because it depends on instrumentation that does not yet exist on the target hardware.

Out of scope **entirely** (see [[#8 Threat Model|§8]]): physical de-capping/glitching of the secure element, analog sensor spoofing, and supply-chain compromise that occurs **before** the RoT is provisioned. Attestation makes device reports *verifiable*; it does not make the physical world *honest*.

---

## 2. Attestation Architecture

Attestation follows the **IETF RATS (Remote ATtestation procedureS) architecture, RFC 9334**, using its **background-check model**: the device (the *Attester*) produces *Evidence*; the [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] Attestation Verification Service (the *Verifier*) appraises that Evidence against *Reference Values* supplied by [[SECURITY_ENGINEER_SKILL|Security]]; the appraisal produces *Attestation Results*, which are written to the [[BACKEND_CLOUD_ENGINEER_SKILL|device twin]] and consumed by *Relying Parties* — fleet monitoring, Over-the-Air (OTA) targeting, and incident response.

> **RATS:** IETF working group and architecture (RFC 9334) standardising remote attestation roles and message flows.
> **Attester / Verifier / Relying Party:** RATS roles — the device proving its state, the service appraising the proof, and the consumer acting on the appraisal.
> **Evidence / Reference Values / Attestation Results:** the claims a device asserts, the known-good values they are compared against, and the verdict of that comparison.

The signing key never leaves the RoT, and the Verifier is a cloud-side service that the device cannot influence — so the chain of custody from *measurement* to *verdict* contains no link the device controls except the production of Evidence itself.

```mermaid
sequenceDiagram
    autonumber
    participant FM as Fleet Mgmt (DevOps)
    participant BE as Backend Verifier
    participant FW as Device Firmware
    participant SE as Secure Element (RoT)
    participant TW as Device Twin
    participant SEC as Security / Incident Cmd

    Note over FM,SEC: Challenge–response (background-check model)
    BE->>FW: 1. Attestation challenge (random nonce)
    FW->>SE: 2. Request token (nonce + measurement set)
    SE->>SE: 3. Read measured-boot regs; hash FW, model, config
    SE-->>FW: 4. Signed EAT (COSE_Sign1, key in RoT)
    FW-->>BE: 5. Attestation token (CBOR / EAT)
    BE->>BE: 6. Verify signature with device AK public key
    BE->>BE: 7. Appraise claims vs reference values

    alt Attestation PASS
        BE->>TW: 8a. Update reported attestation state (+ timestamp)
        TW-->>FM: 9a. Device remains trusted in fleet view
    else Attestation FAIL or stale/missing
        BE->>TW: 8b. Set attestation_status = FAILED
        BE->>FM: 9b. Quarantine device, pause OTA, fire alert
        FM->>SEC: 10b. Security incident raised (notify ≤ 5 min)
    end
```

---

## 3. Attested Properties

Each property defines **what is measured**, **how**, the **reference value** it is appraised against, and the **pass/fail** rule. All hashes are **SHA-256 (Secure Hash Algorithm, 256-bit)** to match the digest already used by the [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OTA Compatibility Manifest]] and MCUboot image format.

| # | Property | What is measured | How measured | Reference value (source) | Pass / Fail |
|---|----------|------------------|--------------|--------------------------|-------------|
| **P1** | **Firmware identity & integrity** | SHA-256 of the active firmware image (the booted A/B slot) + firmware SemVer | MCUboot computes the image hash during verified boot; the value is latched into a measurement register read by the secure element | Golden firmware hash per version from the Continuous Integration build attestation, held in [[SECURITY_ENGINEER_SKILL\|Security]]'s reference-value store | **Pass:** measured hash ∈ allowed-version set. **Fail:** unknown/mismatched hash, or a version not on the approved manifest |
| **P2** | **Model identity & integrity** | SHA-256 of the on-device model artifact + model SemVer | Firmware hashes the model partition contents after load and submits the digest to the secure element as a sub-measurement | `sha256_hash` + `version` from the [[OTA_COMPATIBILITY_MANIFEST_SCHEMA\|OTA Compatibility Manifest]] for the model the twin expects | **Pass:** digest == manifest `sha256_hash`. **Fail:** mismatch, or model not the twin's desired version |
| **P3** | **Secure boot state** | Boot-chain verdict + debug status + boot counter | Read directly from the secure element / Trusted Execution Environment boot-state registers (each stage records its verify result) | Expected: every stage `VERIFIED`, secure boot `ENABLED`, debug `DISABLED` | **Pass:** all stages verified, no fallback/recovery boot, debug disabled. **Fail:** any verification failure, debug enabled, or recovery boot |
| **P4** | **Configuration integrity** | SHA-256 over the critical-config blob: security settings, debug-port lock state, active OTA slot + rollback flags | Firmware canonicalises the critical-config region and hashes it; digest submitted to the secure element | Golden config hash for the device class at the current policy version (Security-owned) | **Pass:** digest == approved value for the device's class/policy. **Fail:** mismatch or unknown policy version |
| **P5** | **Sensor pipeline integrity** *(stretch — out of V1)* | Hash of the sensor-driver + middleware code path and a freshness/replay counter on the sensor→telemetry channel | Measured boot of the driver/middleware layer + a monotonic emission counter signed end-to-end | Golden driver/middleware hash; counter monotonicity check | **Pass:** path hash matches and counter strictly increases. **Fail:** path tampered or counter regression (replay) — *deferred, see [[#9 Implementation Phases\|§9]]* |

A device **fails attestation** if **any** in-scope property fails, if the token signature is invalid, or if the token is **stale** (older than the freshness window) or **missing** when challenged.

---

## 4. Attestation Token Format

The attestation token is an **Entity Attestation Token (EAT)** as defined by **IETF RFC 9711**, carried as a **CWT (CBOR Web Token, RFC 8392)** and signed with **COSE_Sign1 (CBOR Object Signing and Encryption, RFC 9052)**. The serialization is **CBOR (Concise Binary Object Representation, RFC 8949)** — compact enough for Microcontroller-class (MCU-class) devices and natively supported by the secure-element and Trusted Execution Environment (TEE) attestation APIs. **No proprietary token format is introduced.** This is the same family of token used by **PSA Certified (Platform Security Architecture)** attestation, so the on-MCU path can reuse a certified implementation.

> **EAT:** an IETF standard token (RFC 9711) carrying device-state *claims* in a signed CWT.
> **CWT / COSE / CBOR:** the CBOR-encoded JWT analogue, its signature wrapper, and the underlying binary encoding.
> **CoSWID:** Concise Software Identification tags (RFC 9393) — the standard way to carry software/model identity inside EAT measurements.

### 4.1 Token structure (annotated)

```
COSE_Sign1 (
  protected:   { alg: ES256 }                  ; ECDSA w/ SHA-256, key in RoT
  payload: EAT-claims = {
    ; ── Header / identity ──────────────────────────────────────────────
    / iss  /  1: "<device-id>",                 ; CWT issuer = device identity (LDevID CN)
    / iat  /  6: 1718966400,                    ; issued-at (UTC epoch seconds)
    / ueid / 256: h'02<16-byte device UEID>',   ; EAT Universal Entity ID (stable per device)
    / oemid/ 258: h'<oem-id>',                  ; manufacturer ID
    / hwmodel / 259: "GW-ESP32S3-Rev-C",        ; hardware model (matches OCM hardware_id)
    / hwversion / 260: "C",                     ; hardware revision

    ; ── Freshness (anti-replay) ────────────────────────────────────────
    / nonce / 10: h'<challenge nonce>',         ; echoes Backend challenge (§5.1)
    / bootcount / 267: 412,                     ; monotonic boot counter from RoT

    ; ── Boot state (P3) ────────────────────────────────────────────────
    / dbgstat / 263: 1,                         ; 1 = "disabled" (debug locked)
    / secure-boot / 262: true,                  ; secure boot enabled & enforced
    / boot-verdict (profile-private): "VERIFIED",

    ; ── Measurements: firmware (P1), config (P4) ──────────────────────
    / measurements / 273: [                     ; array of CoSWID-tagged digests
      { swname: "fw-image",  swversion: "2.3.1",
        digest: [ -16 /sha-256/, h'<32-byte fw hash>' ] },
      { swname: "crit-config", swversion: "policy-7",
        digest: [ -16 /sha-256/, h'<32-byte config hash>' ] }
    ],

    ; ── Sub-module: on-device model (P2) ──────────────────────────────
    / submods / 266: {
      "ml-model": {
        swname: "vibration-anomaly", swversion: "4.2.0",
        digest: [ -16 /sha-256/, h'<32-byte model hash>' ]   ; == OCM sha256_hash
      }
      ; "sensor-path": { ... }  ; reserved for P5 (Phase 4, out of V1)
    },

    / eat_profile / 265: "urn:fleet:attest:v1"  ; pins claim semantics & policy
  }
  signature:  <ECDSA-P256 signature, computed inside the RoT>
)
```

### 4.2 Key hierarchy and standards mapping

- The **Attestation Key (AK)** — an ECDSA P-256 (Elliptic Curve Digital Signature Algorithm) key whose private half is **generated in and never leaves** the secure element (ATECC608 / SE050) or TEE (TrustZone). Signing happens *inside* the RoT.
- The AK is **distinct from but certified by** the device's **X.509** identity. On MCU-class devices the key hierarchy follows **TCG DICE (Device Identifier Composition Engine)**: the immutable boot ROM derives a Compound Device Identifier (CDI), from which a stable **DeviceID** certifies a per-firmware **Alias key** used as the AK. This binds the signing key to the *exact firmware measured at boot* — so a tampered image cannot produce a valid signature under the legitimate key.
- The X.509 chain roots in the manufacturer Certificate Authority (CA) provisioned at the factory (the same Public Key Infrastructure (PKI) that issues the mTLS / LDevID identities), so the Verifier already holds the trust anchor needed to validate the AK.

> **DICE:** TCG layered measured-boot scheme that derives the device key hierarchy *from the firmware measurement itself* — ideal for MCUs that lack a full Trusted Platform Module.
> **AK / LDevID / IDevID:** the attestation signing key and the device's locally/initially provisioned X.509 identities (IEEE 802.1AR).

---

## 5. Attestation Protocol

### 5.1 Challenge–Response Protocol (authoritative, freshest)

1. **Challenge.** The [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] Verifier (or [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] fleet management on its behalf) generates a cryptographically random **nonce** (≥ 128 bits), records it with a short time-to-live (TTL), and sends it to the device over the existing mTLS (mutual Transport Layer Security) MQTT (Message Queuing Telemetry Transport) / CoAP (Constrained Application Protocol) channel.
2. **Measure.** Firmware requests a token, passing the nonce and the in-scope measurement set. The secure element reads boot-state registers (P3), and Firmware supplies the firmware (P1), model (P2), and config (P4) digests.
3. **Bind & sign.** The secure element assembles the EAT claims, embeds the **nonce** and the **boot counter**, and signs `COSE_Sign1` with the AK — *inside the RoT*.
4. **Return.** Firmware returns the CBOR token to the Backend.
5. **Verify signature.** The Backend validates the COSE signature using the device's AK public key (resolved from the device's X.509 chain).
6. **Appraise.** The Backend checks: nonce matches the outstanding challenge and is unused (anti-replay); `iat`/bootcount within the freshness window; each claim against its reference value ([[#3 Attested Properties|§3]]).
7. **Record.** The Backend writes the verdict (PASS/FAIL + measured values + timestamp) to the device twin and to the immutable attestation audit log.

The nonce makes replay infeasible: a captured token is bound to a challenge that will never be reissued.

### 5.2 Periodic Attestation

- **Default interval: once per 24 hours**, jittered across the fleet to avoid a verification thundering-herd.
- Periodic tokens piggyback on the normal telemetry channel as a dedicated `attestation` message; they do **not** displace sensor telemetry.
- Because there is no live challenge for every periodic token, freshness is bounded by **`iat` + monotonic boot counter**; the Verifier rejects any periodic token whose `iat` is older than `2 ×` the interval or whose boot counter regresses (a regression implies rollback or clone). On-demand challenge–response (§5.1) remains the authoritative check for any device whose periodic token is suspicious.
- Every token (challenge-driven or periodic) is **stored alongside device telemetry** for audit and for the [[#6 Integration with Existing Infrastructure|cross-source reconciliation]] that P4-M5 requires.

### 5.3 Event-Triggered Attestation

Attestation is forced — out of the periodic schedule — on:

| Trigger | Who initiates | Priority |
|---------|---------------|----------|
| **Device reboot** | Device (self-attests on first connect after boot) | Normal — establishes post-boot trust |
| **OTA apply** (firmware or model) | Device after apply **+** Backend post-apply challenge | **High** — confirms the new image/model is what was shipped before the twin is marked updated |
| **Anomaly detection** (fleet monitoring flags abnormal behaviour) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps]] / Backend on-demand challenge | **High** — escalates to immediate challenge–response |
| **Backend on-demand** (audit, spot check, incident) | Backend / [[SECURITY_ENGINEER_SKILL\|Security]] | Variable — incident-driven challenges run **Critical** |

Event-triggered attestation **escalates priority**: an OTA-apply or anomaly-triggered token that fails is treated as a candidate security incident immediately, not at the next periodic cycle.

---

## 6. Integration with Existing Infrastructure

- **Secure boot chain (MCUboot).** Attestation **consumes** the verified-boot result MCUboot already produces — the image hash and per-stage verdict are latched at boot and read by the secure element. No change to the boot flow; attestation reads what secure boot already measures. (Owner: [[SECURITY_ENGINEER_SKILL|Security]] defines; [[FIRMWARE_ENGINEER_SKILL|Firmware]] implements.)
- **Hardware Root of Trust (ATECC608 / SE050 / TPM / TrustZone).** The AK lives in the RoT and signing happens inside it. On MCU-class the DICE hierarchy binds the key to the measured firmware; on Microprocessor-class (MPU-class, e.g. Raspberry Pi CM4) a Trusted Platform Module (TPM) quote or a TrustZone-backed key serves the same role behind the same EAT interface. (Owner: [[HARDWARE_ENGINEER_SKILL|Hardware]] provisions.)
- **Device identity (X.509).** The AK is certified under the existing Public Key Infrastructure; the Verifier reuses the trust anchor already used for mTLS. No new CA.
- **Device twin.** Four new **reported** properties: `attested_firmware_version`, `attested_model_version`, `attested_boot_state`, `last_attestation_timestamp`, plus a Verifier-written `attestation_status` (`PASS` / `FAIL` / `STALE`). **Cross-source reconciliation (P4-M5):** the twin's *desired* firmware/model versions, the *self-reported* OTA status, and the *attested* versions are reconciled three ways — disagreement between self-report and attestation is the signal HA-A3 was missing. This extends Backend's existing desired-vs-reported drift monitor (the >1%/1h rule) with a third, *cryptographically verified* source.
- **OTA pipeline.** Attestation runs **before** an OTA apply (confirm the device is in a known-good state to receive it) and **after** apply (confirm the device is running exactly the shipped artifact, model digest == manifest `sha256_hash`). A post-apply attestation failure feeds the existing rollback path. This respects the four-way OTA boundary — Backend (desired state), [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] (delivery/rollback), [[FIRMWARE_ENGINEER_SKILL|Firmware]] (on-device apply), [[MLOPS_ENGINEER_SKILL|MLOps]] (model rollout).
- **Fleet monitoring.** [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] adds a fleet attestation dashboard and alerts on attestation-failure rate. A device that fails attestation is **quarantined**: removed from the active fleet view, OTA paused, alerts fired.
- **Incident response.** An attestation failure (especially OTA-apply- or anomaly-triggered) is a **security incident**. The [[SECURITY_ENGINEER_SKILL|Security Engineer]] and the (rotating) Incident Commander — the function recommended as P4-H2 to close the [[REVIEW_V2_PHASE4_EMERGENT#7.4 Scenario 4 — Fleet-Scale Incident|Scenario 4]] command gap — are notified **within 5 minutes**, per the existing incident-response plan.

---

## 7. Role-Specific Requirements

| Role | Concrete attestation responsibilities |
|------|----------------------------------------|
| [[HARDWARE_ENGINEER_SKILL\|Hardware Engineer]] | Provision the AK inside the secure element at production programming (key generated on-chip, non-extractable); place and route the ATECC608/SE050 (MCU-class) or expose the TPM/TrustZone (MPU-class); enforce debug-port lockdown so P3/P4 cannot be subverted physically; extend the provisioning interface and board identifiers so each unit's AK is bound to its `hwmodel`/`hwversion` and X.509 identity at the factory. |
| [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] | Implement the on-device EAT generation against the secure-element / TEE attestation API; read MCUboot measured-boot results and the boot counter; compute the firmware (P1), model (P2), and config (P4) SHA-256 digests and submit them to the RoT for signing; implement the challenge handler, the periodic scheduler (24h, jittered), and the reboot/OTA-apply event triggers; emit the CBOR token on the existing mTLS channel. **No secret leaves the RoT.** |
| [[SECURITY_ENGINEER_SKILL\|Security Engineer]] | **Own** this spec, the attestation policy, and the EAT profile (`urn:fleet:attest:v1`); define and maintain the reference-value store (golden firmware hashes, golden config hashes per class/policy); define freshness windows and the quarantine policy; manage AK lifecycle and the trust anchor; verify (not implement) conformance; classify attestation failure severity and own the incident-response runbook entry. |
| [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend/Cloud Engineer]] | Implement the Verifier service: nonce generation + TTL tracking, COSE signature verification, claim appraisal against reference values, anti-replay/freshness checks; add the new device-twin reported properties and `attestation_status`; implement three-way cross-source reconciliation (desired ↔ self-reported ↔ attested); persist every token to the immutable audit log; expose the post-OTA-apply challenge hook. |
| [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps/Platform Engineer]] | Build the fleet attestation dashboard and failure-rate alerts; implement automated **quarantine** (drop from active fleet, pause OTA) on failure; wire anomaly-detection signals to trigger on-demand challenges; route attestation-failure incidents to Security + Incident Commander within the 5-minute Service-Level Agreement (SLA); operate the reference-value store distribution. |
| [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] *(supporting)* | Ensure every published model artifact's [[OTA_COMPATIBILITY_MANIFEST_SCHEMA\|OTA Compatibility Manifest]] `sha256_hash` is the authoritative reference value for P2, so attested model digest can be appraised without a separate source of truth. |

---

## 8. Threat Model

Attestation is a **remote-integrity** control. It raises the bar from "trust the device's word" to "verify a proof rooted in tamper-resistant hardware." It is not a universal defence, and honesty about its limits is a requirement of this spec.

### 8.1 Threats attestation addresses

| Threat | How attestation defeats it |
|--------|----------------------------|
| **Firmware tampering** (modified/unauthorised image) | Measured firmware hash (P1) will not match an approved reference value; on DICE devices the AK derived from a tampered image cannot even produce a valid signature. |
| **Unauthorised / spoofed OTA** | Post-apply attestation (P1/P2) proves the running artifact is exactly what was shipped; a substituted image fails appraisal and triggers rollback. |
| **Model substitution** | Model digest (P2) is compared to the manifest `sha256_hash`; a swapped or poisoned model is detected. |
| **Configuration tampering** | Critical-config hash (P4) detects altered security settings, an unlocked debug port, or manipulated OTA slot/rollback flags. |
| **Lying device twin** (the HA-A3 core threat) | Self-reported state is reconciled against *attested* state; a device that reports a clean version while running a tampered one is caught by the three-way mismatch. |
| **Replay of an old "good" token** | The challenge nonce and monotonic boot counter make a captured token unusable out of context. |

### 8.2 Threats attestation does **NOT** address (honest limits)

- **Physical attacks on the secure element itself** — de-capping, fault injection / voltage-clock glitching, microprobing to extract or coerce the AK. Attestation *assumes* the RoT is sound; if the RoT is physically broken, its signatures are worthless. Mitigation lives in hardware tamper-resistance and device-class selection, not here.
- **Side-channel attacks** (power, timing, electromagnetic) against the signing operation. Out of scope; mitigated by certified secure-element selection.
- **Analog / physical sensor spoofing** — feeding the sensor a false but physically real stimulus (e.g. heating the probe). The pipeline is untampered, so it attests clean; the *world* is lying, not the device. Even P5 (Phase 4) only covers the *digital* path from driver to emission, not the analog front-end.
- **Supply-chain compromise before RoT provisioning** — if the AK or trust anchor is subverted at or before the factory, every downstream proof is validly signed by an attacker-controlled key. Mitigation is provisioning-process security and Software Bill of Materials (SBOM) / supply-chain integrity, owned in the [[SECURITY_ENGINEER_SKILL|security baseline]], not by runtime attestation.
- **A device that is genuinely running approved firmware but is malicious by design** — attestation proves *what* is running, not that what is running is *benign*. Trusted code that misbehaves attests as PASS.
- **Compromise of the Verifier or reference-value store** — these become high-value targets; their integrity is assumed and must be protected by cloud-side controls and access review.

> **Net:** attestation closes HA-A3 for the *digital integrity* of device-reported state. It does **not** close the gap between "the device reports honestly" and "the physical measurement is true." That residual belongs on the risk register with a time-bound note.

---

## 9. Implementation Phases

Phasing is ordered so that **Phase 1 requires no hardware change** — it reuses the secure element, MCUboot measured boot, and X.509 PKI already shipping on every production device.

| Phase | Scope | Properties | Hardware change? | Notes |
|-------|-------|------------|------------------|-------|
| **Phase 1** | **Firmware attestation** — boot state + firmware hash; challenge–response, periodic (24h), reboot/OTA-apply triggers; Verifier + twin properties + quarantine | P1, P3 | **None** — uses existing RoT, MCUboot, PKI | The minimum that makes a lying device detectable; deliverable within the current ecosystem. |
| **Phase 2** | **Model attestation** — appraise on-device model digest against the OTA Compatibility Manifest | + P2 | None | Depends only on MLOps publishing authoritative `sha256_hash` (already in the manifest schema). |
| **Phase 3** | **Configuration attestation** — golden critical-config hashes per class/policy; debug-port and OTA-slot state | + P4 | None | Requires Security to define the canonical config blob and golden values. |
| **Phase 4** *(stretch)* | **Sensor pipeline attestation** — measured boot of driver/middleware + replay counter on the sensor→telemetry channel | + P5 | Likely firmware/driver instrumentation; possibly new hardware for some classes | Out of V1; addresses the *digital* path only (not analog spoofing). |

---

## 10. References

- **IETF RFC 9334** — *Remote ATtestation procedureS (RATS) Architecture* (roles, Evidence/Reference Values/Attestation Results, background-check model).
- **IETF RFC 9711** — *The Entity Attestation Token (EAT)* (token claims, profiles, measurements, submods).
- **IETF RFC 8392** — *CBOR Web Token (CWT)*.
- **IETF RFC 9052** — *CBOR Object Signing and Encryption (COSE): Structures and Process* (COSE_Sign1).
- **IETF RFC 8949** — *Concise Binary Object Representation (CBOR)*.
- **IETF RFC 9393** — *Concise Software Identification Tags (CoSWID)*.
- **TCG DICE** — *Device Identifier Composition Engine* (Layering Architecture & Attestation Architecture) — TCG, for MCU-class key hierarchy rooted in measured boot.
- **NIST SP 800-155** — *BIOS Integrity Measurement Guidelines* (measured-boot evidence principles).
- **NIST SP 800-193** — *Platform Firmware Resiliency Guidelines* (also referenced by the [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OTA Compatibility Manifest]]).
- **GlobalPlatform TEE** — Trusted Execution Environment specifications (MPU-class / TrustZone attestation path).
- **PSA Certified (Platform Security Architecture)** — Attestation API and the PSA attestation token (an EAT profile) for the MCU-class implementation.
- **CSA (Cloud Security Alliance) IoT Security Controls Framework** — fleet-level control mapping for device integrity and quarantine.
- **IEC 62443-4-2** — component security requirements (Software/Information Integrity), cited in the OTA Compatibility Manifest.

---

> **Closes HA-A3.** Cross-references: [[REVIEW_V2_PHASE4_EMERGENT|Phase 4 Emergent Review]] (HA-A3, P4-M5, P4-H2, Scenario 4) · [[OTA_COMPATIBILITY_MANIFEST_SCHEMA|OTA Compatibility Manifest Schema]] · [[SECURITY_ENGINEER_SKILL|Security Baseline]].
