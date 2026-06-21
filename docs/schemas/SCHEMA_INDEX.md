---
title: "Schema Index — Machine-Parseable Deliverable Schemas"
version: "1.0.0"
date_created: "2026-06-21"
tags:
  - schema-index
  - machine-parseable
  - governance
  - interface-contracts
  - automation
---

# Schema Index — Machine-Parseable Deliverable Schemas

## Purpose

This index catalogues all machine-parseable YAML schemas for inter-role deliverables in the IoT Embedded System AI Workflow. Each schema replaces prose-described artifact templates with structured definitions that AI agents can validate programmatically, enabling:

- **Automated gate enforcement** — no integration phase advances with unresolved blocking artifacts
- **Signatory completeness checking** — bilateral contracts cannot close without confirmed signatures from both parties
- **Budget and arithmetic validation** — resource figures are auto-verified against their components
- **Cross-artifact linkage** — CCRs, ADRs, BIAs, and IRDs are cross-referenced and chain-validated
- **Compliance coverage dashboards** — security checklist items are aggregated across roles per sprint

**Motivation:** Review Part 2 Phase 3 (HR-B) identified that 65% of deliverable schemas were prose-described, limiting the Interface Contract Machine-Actionability score to 3.0/5. These 8 schemas target the highest-priority deliverables to raise that score.

---

## Schema Registry

| # | Schema | Producing Role(s) | Consuming Role(s) | File |
|---|--------|-------------------|-------------------|------|
| 1 | Architecture Decision Record (ADR) | Any role | All roles, ARB | [[ADR_SCHEMA]] |
| 2 | Contract Clarification Record (CCR) | Any role pair | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]], ARB | [[CCR_SCHEMA]] |
| 3 | Data Quality Issue Report (DQIR) | [[EDGE_AI_ML_ENGINEER_SKILL]] | [[DATA_ENGINEER_SKILL]], [[MLOPS_ENGINEER_SKILL]] | [[DQIR_SCHEMA]] |
| 4 | Integration Readiness Declaration (IRD) | Any role pair | [[QA_TEST_AUTOMATION_ENGINEER_SKILL]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] | [[INTEGRATION_READINESS_DECLARATION_SCHEMA]] |
| 5 | OTA Compatibility Manifest (OCM) | [[MLOPS_ENGINEER_SKILL]] | [[DEVOPS_PLATFORM_ENGINEER_SKILL]], [[FIRMWARE_ENGINEER_SKILL]], [[SECURITY_ENGINEER_SKILL]] | [[OTA_COMPATIBILITY_MANIFEST_SCHEMA]] |
| 6 | Security Implementation Readiness Checklist (SIRC) | Each role's Security Champion | [[SECURITY_ENGINEER_SKILL]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] | [[SECURITY_IMPLEMENTATION_READINESS_SCHEMA]] |
| 7 | Technology Transfer Pack (TTP) | [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]], [[SECURITY_ENGINEER_SKILL]] | [[TECHNOLOGY_TRANSFER_PACK_SCHEMA]] |
| 8 | Business Impact Assessment (BIA) | [[BUSINESS_CONSULTANT_SKILL]] | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]], ARB | [[BUSINESS_IMPACT_ASSESSMENT_SCHEMA]] |

---

## Schema Detail Cards

### 1. ADR — Architecture Decision Record
**File:** [[ADR_SCHEMA]]
**ID format:** `ADR-NNNN`
**Key structured fields:** `status` (5 values), `decision_class` (3 values), `tier` (10 values), `options_considered` (≥2), `approvers`, `affected_contracts`, `business_impact_assessment`
**Gate role:** STRATEGIC ADRs require [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] approval; BIA required for cost-material decisions
**Machine-actionability:** Agent cross-references `affected_contracts` against contract registry; detects circular supersession chains; triggers downstream role notifications on status→DECIDED
**Validation rules:** 12 rules (V-ADR-01 through V-ADR-12)
**Standards cited:** ISO/IEC/IEEE 42010:2011, NIST SP 800-160 Vol. 1

---

### 2. CCR — Contract Clarification Record
**File:** [[CCR_SCHEMA]]
**ID format:** `CCR-NNNN`
**Key structured fields:** `contract_reference` (ID + version + section), `ambiguity_class` (5 values), `severity` (BLOCKING/HIGH/MEDIUM/LOW), `proposed_clarification`, `resolution`, `signatories`
**Gate role:** BLOCKING CCRs halt integration gates until resolved; ARB chairs review IN_REVIEW CCRs
**Machine-actionability:** Agent scans open CCRs before any IRD is accepted; tracks contract update deadlines; escalates when update SLA (10 business days) is breached
**Validation rules:** 11 rules (V-CCR-01 through V-CCR-11)
**Standards cited:** IEEE 29148:2018, IEC 62443-4-1 §SR-2

---

### 3. DQIR — Data Quality Issue Report
**File:** [[DQIR_SCHEMA]]
**ID format:** `DQIR-NNNN`
**Key structured fields:** `dataset` (name + version + window), `affected_features` (per-feature stats), `issue_type` (8 DAMA-DMBOK2 values), `severity`, `root_cause`, `correction_status`, `training_pipeline_blocked`
**Gate role:** CRITICAL/HIGH DQIRs block MLOps training pipeline until corrected; PII_LEAKAGE triggers immediate security escalation
**Machine-actionability:** Agent blocks training scheduler if `training_pipeline_blocked = true`; validates percentage arithmetic; enforces correction SLAs (48h for CRITICAL, 5 days for HIGH)
**Validation rules:** 13 rules (V-DQIR-01 through V-DQIR-13)
**Standards cited:** ISO 8000-8:2015, NIST IR 8259A, DAMA-DMBOK2

---

### 4. IRD — Integration Readiness Declaration
**File:** [[INTEGRATION_READINESS_DECLARATION_SCHEMA]]
**ID format:** `IRD-NNNN`
**Key structured fields:** `contract` (ID + open CCRs list), `gate_result` (4 values), `test_scenarios` (per-scenario pass/fail), `waivers`, `test_environment`, `metrics`, `signatories`
**Gate role:** Gate cannot be PASS if `open_ccrs` is non-empty or any mandatory scenario fails; both producer and consumer must co-sign
**Machine-actionability:** Agent auto-populates `open_ccrs` from CCR registry; verifies evidence artifact reachability; flags expired waivers; enforces mandatory security scenario requirement per IEC 62443-4-1
**Validation rules:** 13 rules (V-IRD-01 through V-IRD-13)
**Standards cited:** IEEE 829:2008, IEC 62443-4-1 §SVV-3

---

### 5. OCM — OTA Compatibility Manifest
**File:** [[OTA_COMPATIBILITY_MANIFEST_SCHEMA]]
**ID format:** `model.id + model.version` (no separate OCM-NNNN; one manifest per model version)
**Key structured fields:** `model` (SHA-256, framework, quantization), `target_hardware` (validated HW IDs), `firmware_compatibility` (min/max version + excluded), `resource_budget` (flash + RAM with computed checks), `security` (signing key + signature), `deployment` (rollout strategy + rollback triggers)
**Gate role:** `flash_budget_check.result = FAIL` blocks OTA dispatch; `dqir_clearance` IDs must be resolved; firmware version incompatibilities block per-device dispatch
**Machine-actionability:** Agent re-computes SHA-256 of model file; validates budget arithmetic; checks capability flags against device fleet; monitors rollback thresholds post-deployment
**Validation rules:** 16 rules (V-OCM-01 through V-OCM-16)
**Standards cited:** NIST SP 800-193, IEC 62443-4-2 CR 3.4, OTA Alliance Ref Spec v2.0

---

### 6. SIRC — Security Implementation Readiness Checklist
**File:** [[SECURITY_IMPLEMENTATION_READINESS_SCHEMA]]
**ID format:** `SIRC-ROLE-Ssprint` (e.g. `SIRC-FW-S14`)
**Key structured fields:** `checklist_items` (per-control: category, control_reference, status CONFIRMED/UNCERTAIN/FAILED/NOT_APPLICABLE, evidence, risk_accepted), `summary` (coverage_pct), `security_engineer_review`, `architect_signoff`
**Gate role:** Any mandatory item FAILED blocks Security Engineer review scheduling; UNCERTAIN items with `risk_accepted = true` require Architect sign-off; coverage trends tracked per sprint
**Machine-actionability:** Agent validates evidence artifact existence; enforces Architect sign-off for risk-accepted items; auto-carries UNCERTAIN items into next sprint's SIRC template; aggregates coverage_pct for governance dashboard
**Validation rules:** 15 rules (V-SIRC-01 through V-SIRC-15)
**Standards cited:** IEC 62443-4-1, IEC 62443-4-2, NIST SP 800-53 Rev 5, OWASP ISVS v1.0

---

### 7. TTP — Technology Transfer Pack
**File:** [[TECHNOLOGY_TRANSFER_PACK_SCHEMA]]
**ID format:** `TTP-NNNN`
**Key structured fields:** `technology` (type, TRL, license_risk), `research_summary` (findings ≥3, limitations ≥1), `validation_evidence` (per-metric pass/fail against threshold), `architecture_impact` (layers, migration complexity, ADR trigger), `security_review` (supply chain, CVEs, verdict), `resource_estimate`, `transfer_gate`
**Gate role:** TRL ≥ 5 required for transfer approval; security review must be COMPLETED with non-REJECTED verdict; HIGH license risk triggers legal review
**Machine-actionability:** Agent enforces TRL gate; validates benchmark `passed` flags against raw values; escalates HIGH license risk; triggers ADR scaffold when `adr_required = true` and transfer is APPROVED; cross-references CVE IDs with NVD API
**Validation rules:** 15 rules (V-TTP-01 through V-TTP-15)
**Standards cited:** ISO/IEC 16085:2006, NIST SP 800-161, IEC 62443-4-1 §SR-3

---

### 8. BIA — Business Impact Assessment
**File:** [[BUSINESS_IMPACT_ASSESSMENT_SCHEMA]]
**ID format:** `BIA-NNNN`
**Key structured fields:** `cost_impact` (capex + opex + avoided cost + net, per option), `schedule_impact` (delta days + critical path flag), `market_impact` (revenue, regulatory, reputational risk), `business_risks` (ISO 31000 aligned with probability × impact matrix), `recommendation` (PROCEED / PROCEED_WITH_MITIGATION / REJECT / DEFER)
**Gate role:** Appended to ADRs with material cost/schedule/market impact; STRATEGIC ADRs with BIA recommendation=REJECT cannot be DECIDED without ARB override
**Machine-actionability:** Agent validates all cost arithmetic; enforces exactly-one-selected-option; validates risk_score against probability × impact matrix; propagates ARB ACCEPTED decision to linked ADR; aggregates capex across sprint for financial burn-down
**Validation rules:** 15 rules (V-BIA-01 through V-BIA-15)
**Standards cited:** ISO 31000:2018, PMI PMBOK 7th Ed., IEC 62443-2-1 §4.2.3

---

## Cross-Schema Dependency Map

```
TTP ──triggers──► ADR ──appends──► BIA
                   │
                   └──references──► CCR (unresolved ambiguities block ADR decision)

IRD ──requires──► CCR (open CCRs must be empty for PASS gate)
    ──validates──► Contract (contract_id must exist in registry)

DQIR ──blocks──► OCM (dqir_clearance must list resolved DQIRs)
     ──blocks──► Training pipeline (when training_pipeline_blocked = true)

SIRC ──gates──► Security Engineer review
     ──requires──► Architect sign-off (when risk_accepted = true)

OCM ──requires──► DQIR clearance
    ──validates──► firmware_compatibility against device fleet
```

---

## Schema Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-06-21 | Initial release — 8 schemas covering all HR-B priority deliverables |

---

## Implementation Notes for AI Agents

### Validation Toolchain
Schemas are expressed as YAML field definitions annotated with type and enum constraints. Agents should:
1. Parse the YAML block in each artifact file using a standard YAML 1.2 parser (e.g., PyYAML, `js-yaml`, `gopkg.in/yaml.v3`)
2. Validate against the schema definition using `pykwalify`, `jsonschema` (after YAML→JSON conversion), or equivalent
3. Cross-reference foreign keys (contract IDs, ADR IDs, DQIR IDs) against their respective registries before accepting an artifact as valid

### ID Namespaces
| Prefix | Schema | Registry Location |
|--------|--------|-------------------|
| `ADR-NNNN` | ADR | `docs/decisions/ADR_REGISTRY.md` |
| `CCR-NNNN` | CCR | `docs/contracts/CCR_REGISTRY.md` |
| `DQIR-NNNN` | DQIR | `docs/data/DQIR_REGISTRY.md` |
| `IRD-NNNN` | IRD | `docs/integration/IRD_REGISTRY.md` |
| `TTP-NNNN` | TTP | `docs/research/TTP_REGISTRY.md` |
| `BIA-NNNN` | BIA | `docs/business/BIA_REGISTRY.md` |
| `SIRC-ROLE-SNNNN` | SIRC | `docs/security/SIRC_REGISTRY.md` |
| `model.id + version` | OCM | MLOps artifact store |

### Governance Integration
These schemas feed directly into the [[EVALUATION_HARNESS_SPEC]] scoring dimensions:
- **Deliverable Completeness** — schema validation pass/fail determines completeness score
- **Interface Machine-Actionability** — automated cross-reference checks count toward the 5.0/5 target
- **Security Compliance Coverage** — SIRC `coverage_pct` trends feed the security gate dashboard
