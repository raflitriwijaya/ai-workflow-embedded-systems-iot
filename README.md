# AgriSpectra IoT AI Workflow — Embedded/IoT AI Engineering Ecosystem

> **A complete, validated, AI-augmented organizational design for building embedded/IoT AI products — from research to market.**

[![Status](https://img.shields.io/badge/status-CONDITIONAL%20GO-brightgreen)]()
[![Audit](https://img.shields.io/badge/audit-V3%20PASSED-blue)]()
[![Roles](https://img.shields.io/badge/roles-14%20%2B%202%20fractional-orange)]()
[![Contracts](https://img.shields.io/badge/contracts-91%20symmetric-purple)]()
[![FMEA](https://img.shields.io/badge/FMEA-36%20chains%20IEC%2060812-red)]()

---

## 📖 What This Is

This vault is a **document-as-code governance system** for an embedded/IoT software, hardware, and ML engineering organization. It is not an application codebase — it defines *how* a product is built, *by whom*, under *what contracts*, and subject to *what quality gates*.

The reference product is **AgriSpectra**: an agricultural IoT sensor node for pre-symptomatic crop disease detection, running a quantized CNN on an STM32H7 MCU with LoRaWAN uplink, solar power, targeting a 50,000-device fleet over a 7-year field lifetime. Every process, contract, and quality framework in this vault was designed and stress-tested against that product.

The ecosystem is engineered for **gradual AI augmentation**: human-operated today, human-supervised in 12–18 months, human-governed autonomy at 24+ months. Full autonomy is explicitly not the target — permanent human gates remain for safety, security, and ethics.

---

## 🏗️ Architecture

### Roles (14 Primary + 2 Fractional)

| Code | Role | SKILL.md |
|------|------|----------|
| `ARCH` | Embedded Systems Architect | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| `FW` | Firmware Engineer | `FIRMWARE_ENGINEER_SKILL.md` |
| `HW` | Hardware Engineer | `HARDWARE_ENGINEER_SKILL.md` |
| `ML` | Edge AI/ML Engineer | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| `MLOPS` | MLOps Engineer | `MLOPS_ENGINEER_SKILL.md` |
| `DATA` | Data Engineer | `DATA_ENGINEER_SKILL.md` |
| `DEVOPS` | DevOps/Platform Engineer | `DEVOPS_PLATFORM_ENGINEER_SKILL.md` |
| `BACK` | Backend/Cloud Engineer | `BACKEND_CLOUD_ENGINEER_SKILL.md` |
| `FE` | Frontend/Dashboard Engineer | `FRONTEND_DASHBOARD_ENGINEER_SKILL.md` |
| `QA` | QA & Test Automation Engineer | `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` |
| `SEC` | Security Engineer | `SECURITY_ENGINEER_SKILL.md` |
| `PO` | Product Owner / Technical Project Manager | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` |
| `RES` | IoT & Embedded Systems Researcher | `IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md` |
| `BIZ` | Business Consultant | `BUSINESS_CONSULTANT_SKILL.md` |
| — | ARCH-DEP (Deputy Architect) | Fractional — within ARCH scope |
| — | Process Architect | Fractional — within QA scope |

All 14 roles work **concurrently**, enabled by 91 symmetric interface contracts (one per role pair, both directions) frozen before implementation begins.

### Directory Structure

```
/
├── *_SKILL.md (×14)                          # Role definitions — authoritative
├── EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md  # Team topology + Mermaid diagram
├── HOME.md                                    # Vault index
├── CLAUDE.md                                  # AI agent master reference
└── docs/
    ├── ACRONYM_GLOSSARY.md
    ├── agent-protocol/                        # Multi-Agent Coordination Protocol (MACP)
    ├── automation/                            # Reciprocity audit spec (91-contract checker)
    ├── evaluation/                            # AI agent evaluation harness (70 scored types)
    ├── fmea/                                  # System FMEA — 36 chains (IEC 60812)
    ├── metrics-pipeline/                      # Engineering metrics pipeline spec
    ├── operations/                            # Incident Commander specification
    ├── schemas/                               # 8 machine-parseable deliverable schemas
    ├── security/                              # Device attestation spec (RATS + EAT + DICE)
    ├── review_v1/                             # Part 1 audit — 37 findings
    ├── review_v2/                             # Part 2 holistic validation
    └── review_v3/                             # V3 definitive simulation verdict
```

---

## 🚀 Getting Started

### Prerequisites

- [Obsidian](https://obsidian.md/) (recommended) or any Markdown editor
- Git (for version control and change governance)
- Claude Code or a compatible AI agent (for AI-augmented operation)

### First Steps

1. **Clone** this repository
2. **Open** the folder as an Obsidian vault
3. **Read** `CLAUDE.md` — the AI agent master reference (supersedes all default behavior)
4. **Navigate** `HOME.md` — the vault index linking every role and document
5. **Explore** the role `*_SKILL.md` files; each contains interface contracts, deliverables, and an AI execution guide
6. **Review** `docs/review_v3/REVIEW_V3_FINAL.md` for the definitive audit verdict and open gates

### Five Governing Principles

1. **Contract-first** — no implementation begins without a frozen, versioned interface contract
2. **Shift-left** — security reviews and QA gates happen during Planning (§3.2), not Execution (§3.4)
3. **Measure-first, delegate-second** — missing values trigger escalation packages, never plausible fill-ins
4. **Never silently deviate** — any infeasibility is raised as an ADR or CCR with measured evidence
5. **Parallel development by contract** — all 14 roles work concurrently, enabled by frozen contracts

---

## 📊 The Audit Journey

| Phase | Document | Description | Verdict |
|-------|----------|-------------|---------|
| **Part 1** | `docs/review_v1/` | Organizational audit — 37 findings identified | All resolved |
| **Part 2** | `docs/review_v2/` | 5-phase holistic validation | CONDITIONAL YES |
| **V3** | `docs/review_v3/REVIEW_V3_FINAL.md` | Full lifecycle simulation against AgriSpectra | **CONDITIONAL GO** |

The V3 simulation traced a single research finding through all 6 lifecycle stages, all 14 roles, every handoff, and every governance gate — then stress-tested security, OTA governance, quality attributes, and three adversarial scenarios. The verdict is CONDITIONAL GO: the ecosystem is structurally sound and end-to-end traversable, with 12 hard gates remaining before a production fleet release.

---

## 🔑 Key Documents

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | AI agent master reference — read this first |
| `HOME.md` | Vault index — navigate the entire project |
| `*_SKILL.md` (×14) | Role definitions with contracts, deliverables, and agent guides |
| `docs/review_v3/REVIEW_V3_FINAL.md` | Definitive audit verdict with 12 hard gates |
| `docs/fmea/SYSTEM_FMEA_V1.md` | System FMEA — 36 cross-layer failure chains (IEC 60812) |
| `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` | Agent-to-agent coordination spec (MACP) |
| `docs/schemas/` | 8 machine-parseable deliverable schemas (ADR, CCR, IRD, OCM, SIRC, DQIR, TTP, BIA) |
| `docs/security/DEVICE_ATTESTATION_SPEC.md` | Device attestation: RATS + EAT + DICE |

---

## 🎯 Quality Framework

| Quality Attribute | Current State | Gate Mechanism |
|-------------------|--------------|----------------|
| **Scalable** | Specified, not yet verified at fleet scale | System Scalability Contract; load testing gate |
| **Maintainable** | Guaranteed | Contract-first discipline; SemVer on all artifacts |
| **Reliable** | Conditional | A/B OTA rollback; NFR matrix (23 sub-NFRs instantiated) |
| **Robust** | Honest gap: ≈ 53% detection coverage vs. ≥ 95% gate | System FMEA — 17 Critical chains open; burn-down mandatory |
| **Secure** | Conditional (baseline defined) | HG-01 Security veto; SIRC gate; device attestation |
| **High Standards** | Guaranteed | IEC 60812/61025, MISRA C:2012, IEC 62443, ISO/IEC 27001, OWASP IoT Top 10, NIST SP 800-53 |

---

## 🤖 AI Agent Readiness Roadmap

| Wave | Timeline | Scope | Gate |
|------|----------|-------|------|
| **Wave 0** | Now | All 14 roles — human-operated, agents may draft for review | No evaluation harness baseline yet |
| **Wave 1** | Month 1–2 | MACP registries live; DATA, FE, MLOPS agents assist | ≥ 30 human samples per deliverable |
| **Wave 2** | Month 2–3 | A2A messaging; FW, BACK, DEVOPS execute routine tasks autonomously | MACP at L1+ Participant |
| **Wave 3** | Month 3–4 | Tier 3 autonomy; HW, ML, QA agents handle schema/code tasks | No open BLOCKING CCR |
| **Wave 4** | Month 5–6 | Governance participation; RES, SEC, ARCH, BIZ, PO — Tier 1 human gates permanent | Evaluation harness baseline per role |

> **Permanent human gates (non-negotiable):** HG-01 Security Engineer release veto · HG-04 Architect production gate · QA go/no-go stage transitions

---

## 📜 License

To be determined. Contact the project maintainer.

---

## 🙏 Acknowledgments

This ecosystem is the product of a rigorous three-part audit journey spanning organizational design (Part 1 — 37 findings), holistic validation (Part 2 — 5-phase synthesis), and definitive lifecycle simulation (V3 — CONDITIONAL GO). The project's most important property is epistemic honesty: it writes the unflattering truth into its own target cells. The ≈ 53% detection coverage figure exists in the system's documentation not as a failure, but as the foundation for a disciplined burn-down. That honesty is what the CONDITIONAL GO verdict exists to protect.
