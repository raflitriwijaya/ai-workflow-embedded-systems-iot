---
title: "Contract Registry Index — Machine-Parseable Interface Contracts"
date: 2026-06-23
status: draft
tags:
  - contract-registry
  - embedded-iot
  - machine-parseable
cssclass: protocol-spec
---

# REGISTRY_INDEX.md

> Index of the JSON Schema (Draft 2020-12) representations of the highest-priority interface contracts, generated for the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]] Contract Registry so agents can run automated `CONFIRM` / `REJECT` / `COUNTER` validation. Schemas live in [docs/contract-registry/schemas/](schemas/). Contract IDs follow the canonical role ordering of [[CONTRACT_REGISTRY_SCHEMA|Contract Registry Schema]] §2 (`RES < ARCH < HW < FW < ML < DATA < MLOPS < BACK < DEVOPS < FE < QA < SEC < PO < BIZ`) and the ID regex `^[A-Z]+↔[A-Z]+(-[A-Z0-9]+)?-\d{3}$`.

**Scope:** 44 of 91 contracts converted (the agent-coordination-critical surface plus the cross-layer planning/feasibility edges), across three batches. The remaining 47 are tracked as `[NOT YET CONVERTED]` and remain authoritative as §6 prose in their owning `*_SKILL.md`. Each JSON Schema carries an `x-macp` block holding `decision_tier`, `cadence`, and the `confirm_conditions` / `reject_conditions` / `counter_conditions` validation rules.

**Authoritativeness note:** For the six schema-backed multilateral contracts (IRD, SIRC, DQIR, ADR, TTP, BIA), the Markdown schema in [docs/schemas/](../schemas/) remains the authoritative source; the JSON Schema here is a faithful translation for machine validation. On any divergence, the Markdown schema and its `V-*` validation rules govern.

---

## Registry Entries

| CONTRACT_ID | Producer | Consumer | Schema File | Key Deliverables | Cadence | Tier |
|---|---|---|---|---|---|---|
| `FW↔BACK-001` | FW | BACK | [FW↔BACK-001.json](schemas/FW↔BACK-001.json) | Telemetry envelope; OTA model status (DOWNLOADING→ACTIVE/ROLLED_BACK); desired-state command | CONTINUOUS + SLA_FROM_EVENT | Tier-1 |
| `FW↔ML-001` | ML | FW | [FW↔ML-001.json](schemas/FW↔ML-001.json) | TFLite Micro model artifact; preprocessing spec + golden reference; on-target latency/RAM | TRIGGER | Tier-2 |
| `MLOPS↔DEVOPS-001` | MLOPS | DEVOPS | [MLOPS↔DEVOPS-001.json](schemas/MLOPS↔DEVOPS-001.json) | OTA-ready artifact + OCM; rollout strategy; per-cohort distribution status | TRIGGER + SLA_FROM_EVENT | Tier-1 |
| `FW↔DEVOPS-001` | DEVOPS | FW | [FW↔DEVOPS-001.json](schemas/FW↔DEVOPS-001.json) | Signed OTA bundle (MCUboot); signature chain; on-device verification report | TRIGGER + SLA_FROM_EVENT | Tier-1 |
| `MLOPS↔BACK-001` | MLOPS | BACK | [MLOPS↔BACK-001.json](schemas/MLOPS↔BACK-001.json) | Rollout params; fleet model-version distribution; stage-promotion / rollback | SLA_FROM_EVENT | Tier-1 |
| `ML↔DATA-001` | DATA | ML | [ML↔DATA-001.json](schemas/ML↔DATA-001.json) | Versioned dataset; feature spec (with units); leakage-safe splits; calibration set | TRIGGER + CONTINUOUS | Tier-3 |
| `BACK↔FE-001` | BACK | FE | [BACK↔FE-001.json](schemas/BACK↔FE-001.json) | REST/gRPC endpoints; WebSocket streams; OAuth/JWT auth; PERF-3 latency | TRIGGER | Tier-3 |
| `HW↔FW-001` | HW | FW | [HW↔FW-001.json](schemas/HW↔FW-001.json) | Pin-mux; sensor specs (I2C/ADC/1-Wire); errata; joint Bring-Up DoD | TRIGGER | Tier-3 |
| `QA↔ALL-IRD-001` | Any pair | QA | [QA↔ALL-IRD-001.json](schemas/QA↔ALL-IRD-001.json) | Integration Readiness Declaration (bilateral signed gate) | TRIGGER | Tier-2 |
| `SEC↔ALL-SIRC-001` | Security champions | SEC | [SEC↔ALL-SIRC-001.json](schemas/SEC↔ALL-SIRC-001.json) | Security Implementation Readiness Checklist (shift-left gate) | TRIGGER | Tier-1 |
| `ML↔DATA-DQIR-002` | ML | DATA | [ML↔DATA-DQIR-002.json](schemas/ML↔DATA-DQIR-002.json) | Data Quality Issue Report (blocks training on CRITICAL/HIGH) | SLA_FROM_EVENT | Tier-3 |
| `ARCH↔ALL-ADR-001` | Any role | ARCH | [ARCH↔ALL-ADR-001.json](schemas/ARCH↔ALL-ADR-001.json) | Architecture Decision Record submission + approval | TRIGGER (SLA per tier) | Tier-1 |
| `RES↔ARCH-TTP-001` | RES | ARCH | [RES↔ARCH-TTP-001.json](schemas/RES↔ARCH-TTP-001.json) | Technology Transfer Pack (TRL ≥ 5 gate) | CALENDAR (quarterly TTR) | Tier-2 |
| `ARCH↔BIZ-BIA-001` | BIZ | ARCH | [ARCH↔BIZ-BIA-001.json](schemas/ARCH↔BIZ-BIA-001.json) | Business Impact Assessment (appended to cost-material ADR) | TRIGGER | Tier-2 |
| `PO↔ALL-RELEASE-001` | PO | ALL | [PO↔ALL-RELEASE-001.json](schemas/PO↔ALL-RELEASE-001.json) | OTA release calendar; ordered 6-step Release Gate Sequence status | TRIGGER + SLA_FROM_EVENT | Tier-1 |
| `DATA↔BACK-INGEST-001` | BACK | DATA | [DATA↔BACK-INGEST-001.json](schemas/DATA↔BACK-INGEST-001.json) | Telemetry ingest routing; schema validation at boundary; Segment-A SLO | TRIGGER + CONTINUOUS | Tier-3 |
| `DATA↔BACK-HEALTH-002` | DATA | BACK | [DATA↔BACK-HEALTH-002.json](schemas/DATA↔BACK-HEALTH-002.json) | Pipeline health; Segment-B + end-to-end SLO; query performance | CONTINUOUS + SLA_FROM_EVENT | Tier-3 |
| `DATA↔DEVOPS-001` | DATA | DEVOPS | [DATA↔DEVOPS-001.json](schemas/DATA↔DEVOPS-001.json) | Data-infra compute/storage/platform requirements; observability hooks | TRIGGER + CONTINUOUS | Tier-3 |
| `BACK↔DEVOPS-001` | DEVOPS | BACK | [BACK↔DEVOPS-001.json](schemas/BACK↔DEVOPS-001.json) | Service deployment; container spec; scaling policy; health checks | TRIGGER | Tier-3 |
| `DEVOPS↔SEC-001` | SEC | DEVOPS | [DEVOPS↔SEC-001.json](schemas/DEVOPS↔SEC-001.json) | Artifact signing; secrets (Vault); RBAC; image/dependency scanning | TRIGGER | Tier-1 |
| `FW↔QA-001` | FW | QA | [FW↔QA-001.json](schemas/FW↔QA-001.json) | Testable HIL builds; defect reports (traceable); defect fixes + root cause | CONTINUOUS + TRIGGER | Tier-3 |
| `BACK↔QA-001` | BACK | QA | [BACK↔QA-001.json](schemas/BACK↔QA-001.json) | API test environments; API/load/integration results; quality gates | TRIGGER | Tier-3 |
| `ML↔QA-001` | ML | QA | [ML↔QA-001.json](schemas/ML↔QA-001.json) | Model + parity vectors + acceptance criteria; on-device validation results | TRIGGER | Tier-2 |
| `FW↔SEC-001` | SEC | FW | [FW↔SEC-001.json](schemas/FW↔SEC-001.json) | Secure-boot / mTLS / anti-rollback specs; firmware conformance evidence | TRIGGER | Tier-1 |
| `HW↔ML-001` | ML | HW | [HW↔ML-001.json](schemas/HW↔ML-001.json) | ML sensor data spec; sensor characterization data; conformance verdict | TRIGGER + SLA_FROM_EVENT | Tier-2 |
| `ML↔SEC-001` | SEC | ML | [ML↔SEC-001.json](schemas/ML↔SEC-001.json) | Model-integrity / anti-extraction / anti-tampering reqs; threat assessment | TRIGGER | Tier-2 |
| `RES↔DATA-001` | RES | DATA | [RES↔DATA-001.json](schemas/RES↔DATA-001.json) | FAIR dataset archival; datasheet; research-to-training flag; Ingestion Report | TRIGGER + SLA_FROM_EVENT | Tier-3 |
| `RES↔SEC-001` | RES | SEC | [RES↔SEC-001.json](schemas/RES↔SEC-001.json) | Pre-Transfer Security Review briefing; STRIDE threat assessment | TRIGGER + SLA_FROM_EVENT | Tier-2 |
| `ARCH↔PO-001` | PO | ARCH | [ARCH↔PO-001.json](schemas/ARCH↔PO-001.json) | Prioritized feature requests; feasibility verdict + trade-off options | TRIGGER | Tier-2 |
| `ARCH↔HW-001` | ARCH | HW | [ARCH↔HW-001.json](schemas/ARCH↔HW-001.json) | Platform constraints (MCU, per-node budgets, bus topology); board feasibility verdict + errata | TRIGGER | Tier-2 |
| `ARCH↔ML-001` | ARCH | ML | [ARCH↔ML-001.json](schemas/ARCH↔ML-001.json) | Tensor-arena + flash + latency budget; measured footprint/latency + budget conformance | TRIGGER | Tier-2 |
| `ARCH↔DATA-001` | ARCH | DATA | [ARCH↔DATA-001.json](schemas/ARCH↔DATA-001.json) | Telemetry schema + data-flow topology + payload budget; ingestion feasibility | TRIGGER | Tier-3 |
| `ARCH↔QA-001` | ARCH | QA | [ARCH↔QA-001.json](schemas/ARCH↔QA-001.json) | NFR targets (value+unit, no TBD); verification results + contract-violation reports | TRIGGER | Tier-2 |
| `FW↔PO-001` | PO | FW | [FW↔PO-001.json](schemas/FW↔PO-001.json) | Feature reqs + acceptance criteria + OTA release train; milestone status + effort estimate | TRIGGER | Tier-3 |
| `ML↔PO-001` | PO | ML | [ML↔PO-001.json](schemas/ML↔PO-001.json) | ML features as acceptance criteria; model-readiness gate + deployment constraints | TRIGGER | Tier-2 |
| `PO↔BIZ-001` | PO | BIZ | [PO↔BIZ-001.json](schemas/PO↔BIZ-001.json) | Product roadmap/forecast; business-value ranking + market-window + GTM readiness | TRIGGER | Tier-3 |
| `FE↔BIZ-001` | BIZ | FE | [FE↔BIZ-001.json](schemas/FE↔BIZ-001.json) | Market KPIs to surface; dashboard UX feasibility + query SLO **(DERIVED / provisional — no direct §6)** | TRIGGER | Tier-3 |
| `DATA↔BIZ-001` | BIZ | DATA | [DATA↔BIZ-001.json](schemas/DATA↔BIZ-001.json) | Monetization data-product reqs + tiers; cost/device/month + pipeline cost profiles | TRIGGER | Tier-3 |
| `RES↔PO-001` | RES | PO | [RES↔PO-001.json](schemas/RES↔PO-001.json) | Research roadmap (TRL, transfer confidence); product vision + market-driven research questions | TRIGGER | Tier-3 |
| `RES↔HW-001` | RES | HW | [RES↔HW-001.json](schemas/RES↔HW-001.json) | PoC HW design + characterization; HW feasibility (BOM cost, availability, showstoppers) | TRIGGER | Tier-3 |
| `RES↔ML-001` | RES | ML | [RES↔ML-001.json](schemas/RES↔ML-001.json) | Novel ML findings + operators; TFLite Micro feasibility (arena, latency, verdict) | TRIGGER | Tier-2 |
| `HW↔SEC-001` | SEC | HW | [HW↔SEC-001.json](schemas/HW↔SEC-001.json) | Secure-element/RoT spec + debug-lockdown policy; placement + lockdown conformance | TRIGGER | Tier-1 |
| `FW↔DATA-001` | FW | DATA | [FW↔DATA-001.json](schemas/FW↔DATA-001.json) | Schema-conformant telemetry; joint schema-change process (ADR if breaking) | TRIGGER | Tier-3 |
| `BACK↔SEC-001` | SEC | BACK | [BACK↔SEC-001.json](schemas/BACK↔SEC-001.json) | PKI/identity + mTLS/X.509 reqs; device-identity conformance evidence | TRIGGER | Tier-1 |

> **Batch 1** = rows 1–15 (`FW↔BACK-001` … `PO↔ALL-RELEASE-001`); **Batch 2** = rows 16–29 (`DATA↔BACK-INGEST-001` … `ARCH↔PO-001`); **Batch 3** = rows 30–44 (`ARCH↔HW-001` … `BACK↔SEC-001`). 44 of 91 contracts converted.

---

## Validation-Rule Convention (CONFIRM / REJECT / COUNTER)

Each schema's `x-macp` object defines, for the MACP Negotiate phase:

- **`confirm_conditions`** — all must hold for an agent to emit `CONFIRM` on a proposed artifact.
- **`reject_conditions`** — any one holding forces `REJECT` (and, where flagged, an escalation trigger such as `ESC-SEC` / `ESC-TIER1`).
- **`counter_conditions`** — situations that are not outright invalid but need clarification before acceptance → emit `COUNTER` (Propose→Confirm, max 3 rounds; `> 3` rounds fires `ESC-DEAD`).

**Invariant (MACP §7.3):** a `CONFIRM` on any of these schemas records a proposal only — it never by itself changes a contract, schema, resource budget, security baseline, or OTA strategy. Binding changes still require the ADR/CCR process with the correct human approver. The Tier-1 contracts above (`FW↔BACK-001`, `MLOPS↔DEVOPS-001`, `FW↔DEVOPS-001`, `MLOPS↔BACK-001`, `SEC↔ALL-SIRC-001`, `ARCH↔ALL-ADR-001`, `PO↔ALL-RELEASE-001`, `DEVOPS↔SEC-001`, `FW↔SEC-001`, `HW↔SEC-001`, `BACK↔SEC-001`) sit behind permanent HITL gates (HG-01, HG-04, QA go/no-go) and admit zero autonomous resolution. The `SEC`-side contracts (`DEVOPS↔SEC-001`, `FW↔SEC-001`, `ML↔SEC-001`, `RES↔SEC-001`, `HW↔SEC-001`, `BACK↔SEC-001`) additionally carry `ESC-SEC`: agents may only propose; the Security Engineer owns all binding decisions.

---

## Open Items

- 47 of 91 contracts `[NOT YET CONVERTED]` — convert as agent-coordination demand warrants; preserve canonical role ordering and 3-digit sequence numbers.
- **Batch 3 notes (rows 30–44):** (a) **`FE↔BIZ-001` is DERIVED / provisional** — there is **no direct §6 contract on either the Frontend or Business Consultant side** (FE §6 lists no BIZ; BIZ §6 lists no FE). It is composed from BIZ §6.1 (market-KPI deliverables) + FE §6.3 (UX feasibility) + DATA §6.12 (dashboard query SLO p95 ≤ 2 s / p99 ≤ 5 s). Its `x-macp.source_status` mandates a `COUNTER` (request §6 ratification via a CCR) rather than a binding `CONFIRM` until a formal FE↔BIZ §6 contract exists. No KPI numeric thresholds were invented. (b) `PO↔BIZ-001` is grounded in PO §6.15 — note the PO skill card lists the Business Consultant **twice** (§6.13 and §6.15); the duplication is a source inconsistency, left un-"corrected" per §10.4, and §6.15 (HR-2-tagged) was used as the fuller version. (c) `DATA↔BIZ-001` uses the **source unit — cost per device per month at fleet scale** — as primary; the task's "per TB" framing is captured as an optional secondary field, not fabricated. (d) `FW↔DATA-001` is grounded from the **FW side only** (FW §6.8); DATA §6 has no Firmware subsection — the edge is asymmetrically documented but reciprocity holds via the shared Schema-Change Coordination Process. (e) For `ARCH↔HW-001` / `ARCH↔ML-001`, budget exceedances are encoded as ADR triggers (not silent trades); the ± tolerance bands remain `[NOT YET AVAILABLE]` per CLAUDE.md §6.5, so no margin was invented.
- **Batch 2 canonicalization notes:** (a) The requested "BACK↔DATA" and "DATA↔BACK" are the same canonical pair (DATA precedes BACK), so they were split into two topic-scoped contracts — `DATA↔BACK-INGEST-001` (ingest routing + schema validation) and `DATA↔BACK-HEALTH-002` (pipeline health + query performance). (b) The requested "HW↔FW: Pin-mux assignments + bring-up validation" was **already delivered in Batch 1 as `HW↔FW-001`** (pin-mux + sensor specs + joint Bring-Up DoD); it was not duplicated. Net new schemas in Batch 2: 14.
- The `FW↔BACK-001` sensor `payload` field set is intentionally left as an open object: AgriSpectra is a spectral crop-disease product, so the authoritative per-field telemetry schema (field names, units, ranges) is owned by [[DATA_ENGINEER_SKILL|Data Engineer]] via the Git-based schema registry and is resolved by `schema_version`, not duplicated here. `[NOT YET AVAILABLE — fill in: link the DATA telemetry field schema once registered.]`
- Filenames contain the `↔` (U+2194) glyph per the MACP contract-ID convention; confirm the artifact store / CI tooling preserves UTF-8 filenames on all platforms.
