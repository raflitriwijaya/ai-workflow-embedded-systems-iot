---
title: "Organizational SKILL.md Review Report — Phase 4: AI Workflow"
date: 2026-06-19
status: superseded
tags:
  - review
  - organizational-design
  - embedded-iot
  - ai-workflow
  - skill-audit
  - phase4-workflow
cssclass: review-report
---

# Organizational SKILL.md Review Report — Phase 4: AI Workflow Review

## Prefatory Note

The workflow document (`EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md`) declares a team of **12 roles**, not the 13 stated in the Phase 4 task specification. This report uses the actual count of 12. The 14 `SKILL.md` files in the project include all 12 workflow-defined roles plus two additional roles not present in the workflow document: [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] and [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]]. The consistency matrix in §2.1 reflects the 12 workflow-defined roles only; the two extra roles are analyzed separately in §1.1.

---

## 1. Workflow Structure & Completeness

### 1.1 Role Coverage — Missing & Extra Roles

**Workflow roles (12):**

| # | Workflow Role | Corresponding SKILL.md |
|---|---|---|
| 1 | Embedded Systems Architect | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] |
| 2 | Firmware Engineer | [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] |
| 3 | Hardware Engineer | [[HARDWARE_ENGINEER_SKILL\|Hardware Engineer]] |
| 4 | Edge AI/ML Engineer | [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML Engineer]] |
| 5 | MLOps Engineer | [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] |
| 6 | Data Engineer | [[DATA_ENGINEER_SKILL\|Data Engineer]] |
| 7 | DevOps/Platform Engineer | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] |
| 8 | Backend/Cloud Engineer | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend/Cloud Engineer]] |
| 9 | Frontend/Dashboard Engineer | [[FRONTEND_DASHBOARD_ENGINEER_SKILL\|Frontend Engineer]] |
| 10 | QA & Test Automation Engineer | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA Engineer]] |
| 11 | Product Owner / Technical Project Manager | [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]] |
| 12 | Security Engineer (Embedded/IoT Focus) | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] |

**SKILL.md roles MISSING from the workflow document:** #workflow-gap

1. **[[BUSINESS_CONSULTANT_SKILL|Business Consultant]]** — The Business Consultant (IoT & Embedded Systems Specialist) defines market strategy, business cases, pricing models, GTM planning, and monetization for the IoT product portfolio. This role has 13 interface contracts defined in its `SKILL.md` — including with the Product Owner/TPM, Embedded Systems Architect, all engineering roles, and executive leadership. Its absence from the workflow means there is **no formal mechanism for market requirements, pricing constraints, or business viability assessments to flow into the engineering pipeline**. The workflow's Product Owner role partially absorbs business-facing duties but is defined as the translator of existing business/field needs, not as the originator of market strategy. This is a critical structural gap.

   **Recommendation:** Add the Business Consultant as a role in the workflow, interfacing with the Product Owner/TPM (providing market requirements and pricing constraints), the Embedded Systems Architect (providing business framing of architectural trade-offs), and executive leadership. The Business Consultant feeds the "why" (market viability, pricing, GTM timing) that the PO/TPM operationalizes into backlog priorities. #recommendation

2. **[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]]** — The IoT & Embedded Systems Researcher conducts fundamental scientific research at the intersection of embedded systems, chemistry, physics, biology, and AI/Math. This role owns the research lifecycle from hypothesis formation through peer-reviewed publication, patent filing, and technology transfer to the engineering team. Its `SKILL.md` defines 8 interface contracts including direct interfaces with the Embedded Systems Architect, Product Owner, Hardware Engineer, Firmware Engineer, Edge AI/ML Engineer, and Data Engineer. The workflow has **no research-to-engineering handoff mechanism**, meaning novel sensing principles, energy-harvesting paradigms, or bio-inspired architectures discovered in research have no defined path into the product pipeline.

   **Recommendation:** Add the IoT & Embedded Systems Researcher as a role in the workflow, with explicit technology-transfer interface contracts flowing to the Embedded Systems Architect (PoC evaluation, feasibility reports), Hardware Engineer (novel sensor/component characterization), and Edge AI/ML Engineer (novel ML-based sensing approaches). The researcher feeds the "what is newly possible" into the architecture pipeline. #recommendation

**Extra roles in workflow not in SKILL.md:** None. All 12 workflow roles have corresponding `SKILL.md` files. #strength

### 1.2 Job Description Quality

The workflow uses a consistent three-part structure per role: **(a) Job Description** (3–6 bullet points of responsibilities), **(b) Required Skills** (organized into 5 categories: Hardware/Systems, Firmware/Low-Level, Software/Middleware, AI/ML Awareness, Tools & Processes), and **(c) Collaboration Interfaces** (a paragraph naming collaborating roles and what is delivered).

**Strengths:** #strength
- Consistent, scannable format across all 12 roles.
- Skills are categorized into the same five buckets across roles, enabling cross-role comparison.
- Collaboration interfaces consistently name "works closely with" and "delivers" for each role.
- Every role's Required Skills section maps to its SKILL.md counterpart at the category level.

**Weaknesses:** #workflow-gap
- **Job descriptions are generic compared to SKILL.md.** The workflow provides 3–6 bullet points per role; the corresponding SKILL.md provides a "Core Mission & Scope" with explicit Owns/Influences/Does NOT Own tripartite structure, plus a full lifecycle stage engagement table. The workflow JDs would be insufficient for an AI agent to execute the role without also reading the SKILL.md.
- **No seniority tiering.** Every SKILL.md defines Junior/Mid/Senior/Staff tiers with differentiated scope. The workflow treats all roles as monolithic. An AI agent assigned to a "Junior Firmware Engineer" vs. "Staff Firmware Engineer" would have no guidance from the workflow document alone.
- **No "Does NOT Own" boundaries.** The SKILL.md files rigorously define what each role explicitly does NOT own to prevent scope creep. The workflow lacks these negative-space definitions, which are critical for AI agents that tend to over-execute.
- **Product Owner role has no AI/ML Awareness skill category.** Every other technical role includes an "AI/ML Awareness" skills section. The PO/TPM's workflow skills section omits this entirely, yet the corresponding SKILL.md devotes an entire subsection (4.6) to AI/ML Lifecycle Awareness. This is a significant gap given the product is an AI-driven IoT system.

### 1.3 Mermaid Diagram Accuracy

The Mermaid diagram at §14 of the workflow document is a **simplified subset** of the interface contracts actually defined. It captures 22 directed edges. The full set of interface contracts described in the workflow text and SKILL.md files numbers well over 80 directed edges. #workflow-gap

**Edges present in text but MISSING from the diagram (non-exhaustive):** #workflow-gap

| Missing Edge | Source of Definition |
|---|---|
| ARCH → EDGE (memory/latency/power budgets) | Workflow §2.3, §5.3; SKILL.md §6.1 |
| ARCH → MLOPS (deployment topology, OTA constraints) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.5 |
| ARCH → DATA (telemetry schema, data-flow topology) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.6 |
| ARCH → DEVOPS (OTA strategy, gateway orchestration) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.7 |
| ARCH → QA (NFR targets, requirements traceability) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.10 |
| ARCH → SEC (security-by-design, architecture surfaces) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.11 |
| ARCH → FE (data/event contracts, stream topology) | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] §6.9 |
| EDGE → HW (sensor data requirements spec) | [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML Engineer]] §6.5 |
| EDGE → DATA (dataset/labeling requirements) | [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML Engineer]] §6.3 |
| MLOPS → FW (OTA-ready model artifacts) | [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] §6.3 |
| MLOPS → EDGE (pipeline, registry, drift telemetry) | [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] §6.1 |
| FW → BE (device-side protocol conformance) | [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] §6.7 |
| FW → DEVOPS (build entry points, toolchain requirements) | [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] §6.4 |
| FW → SEC (implementation conformance evidence) | [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] §6.6 |
| DATA → FE (query-ready data, serving views) | [[DATA_ENGINEER_SKILL\|Data Engineer]] §6.4 |
| DEVOPS → MLOPS (CI/CD platform, OTA distribution) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] §6.3 |
| DEVOPS → QA (CI/CD test stages) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] §6.6 |
| DEVOPS → HW (device provisioning/enrollment) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] §6.7 |
| DEVOPS → SEC (signing/secrets implementation) | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] §6.4 |
| QA → FW (HIL results, defect reports) | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA Engineer]] §6.1 |
| QA → EDGE (model validation results) | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA Engineer]] §6.2 |
| QA → BE (API/integration test results) | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA Engineer]] §6.3 |
| SEC → HW (secure-element requirements, debug lockdown) | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] §6.3 |
| SEC → DEVOPS (signing/key/PKI requirements) | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] §6.5 |
| SEC → MLOPS (model-signing/integrity requirements) | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] §6.6 |
| SEC → EDGE (model integrity, anti-tampering requirements) | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] §6.7 |
| HW → SEC (secure-element placement, tamper resistance) | [[HARDWARE_ENGINEER_SKILL\|Hardware Engineer]] §6.4 |
| FE → BE (API/streaming contract feedback) | [[FRONTEND_DASHBOARD_ENGINEER_SKILL\|Frontend Engineer]] §6.1 |
| PO → ALL (requirements, backlog, acceptance criteria) | Workflow §12.3; SKILL.md §6 |

**Diagram issues specific to edge labels:** #workflow-gap
- EDGE → MLOPS is labeled "Training Requirements" but the actual interface is bidirectional: MLOps provides the pipeline and registry back to EDGE.
- The diagram shows a purely left-to-right flow, but many SKILL.md interface contracts are **bidirectional** (e.g., FW ↔ EDGE, FW ↔ HW, MLOPS ↔ DEVOPS, QA ↔ all roles).
- The diagram has **no feedback loops** (e.g., QA findings → FW fixes → re-validation; field telemetry → drift detection → retraining trigger).

**Recommendation:** The Mermaid diagram should either be expanded to a full C4 Container diagram with bidirectional edges or explicitly labeled as a "simplified primary-flow diagram" with a note that it does not represent all interface contracts. The diagram should at minimum include the Architect's fan-out to all roles (the Architect defines contracts for every other role, yet the diagram only shows ARCH → HW, FW, and BE) and the bidirectional QA feedback loops. #recommendation

---

## 2. SKILL.md vs. Workflow Consistency Analysis

### 2.1 Consistency Matrix (12 × 2)

> **Legend:** ✅ = Consistent | ⚠️ = Minor differences | ❌ = Major conflict | **Every cell filled.**

| # | Role | Job Description Match | Skill Requirements Match | Interface Contracts Match | Overall |
|---|---|---|---|---|---|
| 1 | Embedded Systems Architect | ✅ | ✅ | ⚠️ | ⚠️ |
| 2 | Firmware Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 3 | Hardware Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 4 | Edge AI/ML Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 5 | MLOps Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 6 | Data Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 7 | DevOps/Platform Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 8 | Backend/Cloud Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 9 | Frontend/Dashboard Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 10 | QA & Test Automation Engineer | ✅ | ✅ | ⚠️ | ⚠️ |
| 11 | Product Owner / TPM | ⚠️ | ❌ | ⚠️ | ❌ |
| 12 | Security Engineer | ✅ | ✅ | ⚠️ | ⚠️ |

**Summary:** 10 of 12 roles score `⚠️` overall (minor interface contract differences). 1 role (Product Owner/TPM) scores `❌` (major skill requirement conflict). 0 roles score `✅` overall. This indicates the workflow document is **directionally aligned** with the SKILL.md files but **systematically less detailed** — particularly in interface contracts, which are significantly more elaborated in every SKILL.md than in the workflow.

### 2.2 Responsibility Mismatches

**None found at the "Owns" level.** The workflow's job descriptions for all 12 roles align with the "Owns" sections of the corresponding SKILL.md files. No role in the workflow claims ownership of a responsibility that its SKILL.md explicitly disclaims. #strength

**Minor misalignment in scope articulation:** #consistency-issue

- **[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]** explicitly lists 7 items under "Owns (unilateral authority, subject to the ADR process)" plus 6 items under "Influences (advisory; does not implement)" plus 5 items under "Explicitly Does NOT Own." The workflow document (§2.1) covers 6 bullet points of JD that map to the "Owns" items but omits the "Influences" and "Does NOT Own" distinctions entirely. This matters because an AI agent reading only the workflow might attempt to write firmware or design ML models — actions the SKILL.md explicitly forbids.

- **[[SECURITY_ENGINEER_SKILL|Security Engineer]]** defines the role as one that "*defines and verifies, it does not implement*" — Security sets the baseline that Firmware, Hardware, Backend, DevOps, and MLOps implement. The workflow document's JD (§13.1) uses active verbs like "Defines and implements," "Implements device identity," "Conducts threat modeling," "Hardens devices," and "Performs penetration testing." The word "implements" applied to controls is a **meaningful ambiguity** — the SKILL.md clarifies that Security *defines the specification* and *verifies conformance*, while the implementing roles build the controls. The workflow's phrasing could lead an AI agent to implement controls directly. #consistency-issue

- **[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]]** explicitly states the PO/TPM "does NOT own: Technical architecture or design decisions." The workflow document does not include this explicit exclusion, though it also does not positively assert architecture ownership.

### 2.3 Skill Requirement Mismatches

**[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] — Major conflict.** #consistency-issue

The workflow document's "Required Skills" section for the PO/TPM (§12.2) lists 5 categories:
1. **Process:** Agile/Scrum/Kanban; roadmap and backlog management; risk management; OKRs.
2. **Technical Literacy:** Working understanding of embedded/IoT constraints.
3. **Software / Middleware Awareness:** System architecture comprehension; protocol and data-flow basics; ML lifecycle awareness.
4. **Domain:** Agricultural automation field-operations realities.
5. **Tools & Processes:** Jira/Linear; Confluence; roadmap tooling; requirements traceability; stakeholder communication.

The corresponding SKILL.md defines **8 skill categories** with **55 individually profiled skills**, including:
- Product Strategy & Roadmapping (7 skills)
- Agile & Lean Project Management (8 skills)
- Backlog Management & Requirements Engineering (7 skills)
- Cross-Functional Dependency & Risk Management (7 skills)
- Embedded/IoT Technical Literacy (7 skills)
- **AI/ML Lifecycle Awareness (6 skills)** — completely absent from the workflow
- Stakeholder Communication & Reporting (6 skills)
- Release Management & Field Deployment (7 skills)

The workflow entirely omits the AI/ML Lifecycle Awareness category, which the SKILL.md defines with 6 skills including model readiness gate definition, data pipeline dependency awareness, model drift/monitoring awareness, edge inference deployment constraints, and ML experiment/iteration cadence understanding. For a Product Owner managing an **AI-driven** IoT system, this omission is a ❌ **major conflict** — the PO cannot effectively prioritize backlog items, define acceptance criteria for ML features, or manage cross-functional dependencies without basic AI/ML lifecycle literacy. #consistency-issue

### 2.4 Interface Contract Mismatches

**Systematic pattern: Workflow defines fewer interfaces than SKILL.md for every role.** #consistency-issue

Every SKILL.md file contains a dedicated "Interface Contracts" section (§6) enumerating what the role **Provides**, **Requires**, and the **Cadence** for each collaborating role. The workflow document's "Collaboration Interfaces" subsection (§X.3) for each role is a single paragraph naming primary collaborators and deliverables.

Quantitative comparison:

| Role | Collaborators Named in Workflow | Collaborators Defined in SKILL.md §6 | Missing from Workflow |
|---|---|---|---|
| Embedded Systems Architect | 4 (PO, HW, EDGE, SEC) | 11 (PO, HW, FW, EDGE, MLOps, DATA, DEVOPS, BE, FE, QA, SEC) | 7 |
| Firmware Engineer | 5 (HW, EDGE, ARCH, DEVOPS, QA) | 8 (ARCH, HW, EDGE, DEVOPS, QA, SEC, BE, DATA) | 3 |
| Hardware Engineer | 4 (ARCH, FW, EDGE, SEC) | 7 (ARCH, FW, EDGE, SEC, QA, DEVOPS, PO) | 3 |
| Edge AI/ML Engineer | 4 (DATA, FW, ARCH, MLOPS) | 7 (ARCH, FW, DATA, MLOPS, HW, QA, PO) | 3 |
| MLOps Engineer | 4 (EDGE, DATA, DEVOPS, FW) | 8 (EDGE, DEVOPS, FW, DATA, ARCH, QA, SEC, PO) | 4 |
| Data Engineer | 4 (BE, EDGE, MLOPS, FE) | 8 (BE, EDGE, MLOPS, FE, ARCH, DEVOPS, QA, PO) | 4 |
| DevOps/Platform Engineer | 4 (FW, BE, MLOPS, SEC) | 8 (FW, BE, MLOPS, SEC, ARCH, QA, HW, PO) | 4 |
| Backend/Cloud Engineer | 6 (ARCH, FW, FE, DATA, SEC, DEVOPS) | 9 (ARCH, FW, FE, DATA, SEC, DEVOPS, MLOPS, QA, PO) | 3 |
| Frontend/Dashboard Engineer | 4 (BE, DATA, PO, EDGE) | 7 (BE, DATA, PO, EDGE, QA, DEVOPS, SEC) | 3 |
| QA & Test Automation Engineer | 5 (FW, EDGE, BE, DEVOPS, ARCH) | 8 (FW, EDGE, BE, DEVOPS, ARCH, HW, FE, PO) | 3 |
| Product Owner / TPM | 4 (ARCH, team leads, FE, stakeholders) | 12 (ARCH, HW, FW, EDGE, MLOPS, DATA, DEVOPS, BE, FE, QA, SEC, stakeholders) | 8 |
| Security Engineer | 5 (ARCH, FW, HW, BE, DEVOPS) | 9 (ARCH, FW, HW, BE, DEVOPS, MLOPS, EDGE, QA, PO) | 4 |

**Average: 4.4 collaborators named in workflow vs. 8.5 in SKILL.md.** The workflow names approximately **52%** of the interface contracts that the SKILL.md files define.

### 2.5 Workflow Adds / SKILL.md Adds

**What the workflow adds that SKILL.md does not:** #strength
- The workflow provides a **single-document overview** of the entire team — no SKILL.md does this. A reader can scan the 12 role summaries in ~10 minutes and understand the full team topology.
- The workflow's consistent five-category skill structure (Hardware/Systems, Firmware/Low-Level, Software/Middleware, AI/ML Awareness, Tools & Processes) creates a **cross-role comparability** that is harder to extract from individual SKILL.md files.
- The Mermaid diagram, though simplified, provides a **visual entry point** to the architecture that no individual SKILL.md offers.

**What SKILL.md adds that the workflow does not:** #consistency-issue
- **Owns/Influences/Does NOT Own** tripartite scope definition — critical for AI agent boundary enforcement.
- **Lifecycle stage engagement** (Research → Planning → Development → Execution → Production-Ready) with stage-specific activities and deliverables for every role.
- **Deliverables & Artifacts table** with consumers, format/standard, and versioning approach for every role.
- **Full bidirectional interface contracts** with Provides/Requires/Cadence for every collaborator.
- **Decision Authority & Governance** with unilateral vs. consensus decisions and escalation paths.
- **AI Agent Execution Guide** (§9 in every SKILL.md) — persona, mandatory pre-delivery checklist, forbidden actions, and prompt templates.
- **Standards & Best Practices** with specific standards bodies (ISO, IEC, IEEE, OWASP, IPC, ISTQB, COPE).
- **Seniority tiering** (Junior/Mid/Senior/Staff) with differentiated scope for each tier.
- **Success Metrics & KPIs** with both technical and process metrics for every role.

**Recommendation:** The workflow document should either (a) be expanded to incorporate the SKILL.md detail, or (b) be explicitly positioned as a "Team Overview & Quick Reference" that delegates to individual SKILL.md files as the authoritative source per role. Currently, no such delegation statement exists, and the workflow presents itself as complete. #recommendation

---

## 3. AI-Specific Readiness

### 3.1 AI Agent Execution Clarity per Role

Every SKILL.md contains a §9 "AI Agent Execution Guide" with persona/tone, mandatory pre-delivery checklist, forbidden actions, and prompt templates. The **workflow document contains zero AI-specific execution guidance.** This section assesses the workflow document alone for AI execution clarity; SKILL.md AI guidance is treated as the benchmark.

| Role | Workflow AI Clarity | Evidence | SKILL.md §9 Coverage |
|---|---|---|---|
| Embedded Systems Architect | ❌ Not AI-ready | No persona, checklist, forbidden actions, or prompts | ✅ Full — 4 templates, 12-item checklist, 9 forbidden actions |
| Firmware Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 14-item checklist, 10 forbidden actions |
| Hardware Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 15-item checklist, 11 forbidden actions |
| Edge AI/ML Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 14-item checklist, 10 forbidden actions |
| MLOps Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 15-item checklist, 11 forbidden actions |
| Data Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 15-item checklist, 11 forbidden actions |
| DevOps/Platform Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 15-item checklist, 11 forbidden actions |
| Backend/Cloud Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 15-item checklist, 11 forbidden actions |
| Frontend/Dashboard Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 9-item checklist, 7 forbidden actions |
| QA & Test Automation Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 14-item checklist, 10 forbidden actions |
| Product Owner / TPM | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 9-item checklist, 8 forbidden actions |
| Security Engineer | ❌ Not AI-ready | No AI execution guidance | ✅ Full — 5 templates, 14-item checklist, 10 forbidden actions |

**Finding:** The workflow document is **not AI-ready** as a standalone execution guide for any role. It serves as a human-readable team topology document. The SKILL.md files, by contrast, are AI-ready — each contains explicit agent persona, mandatory checklists, forbidden actions, and parameterized prompt templates. This is not a defect of the workflow document per se; it is a **separation of concerns** — the workflow defines *what* the team is, and the SKILL.md files define *how* each role is executed. However, this separation is **not documented anywhere**, creating ambiguity about which document an AI agent should follow. #ai-readiness

**Recommendation:** Add a statement to the workflow document's preamble: "This document defines the team topology, role summaries, and primary collaboration interfaces. For detailed role scope, lifecycle engagement, AI agent execution guidance, and prompt templates, see the corresponding `SKILL.md` file for each role." #recommendation

### 3.2 Human-AI Ambiguity

The following phrases in the workflow document are clear to human readers but **ambiguous for AI agents**: #ai-readiness #gap

| Location | Ambiguous Phrase | Why It Fails for AI |
|---|---|---|
| §2.3 | "Works closely with the Product Owner/TPM" | An AI agent needs specific cadence, format, and trigger conditions — not "works closely." |
| §3.3 | "Honors interface and memory contracts" | No specification of what constitutes a violation or what evidence is required to flag one. |
| §4.3 | "Leads board bring-up jointly with firmware" | "Jointly" is undefined — who initiates? What is the handoff sequence? |
| §6.3 | "Automates model-to-edge conversion" | An AI agent needs the exact pipeline stages, tool versions, and artifact format. |
| §7.3 | "Ensures data quality" | "Ensures" is a vague verb for an AI. The SKILL.md specifies: schema validation, deduplication, out-of-order handling, completeness/accuracy/timeliness metrics. |
| §8.3 | "Manages edge-fleet orchestration" | No specification of the orchestration tool, deployment group model, or rollout policy. |
| §11.3 | "Validates end-to-end flows" | An AI needs the specific flow catalog, the expected state at each hop, and the pass/fail criteria. |
| §12.1 | "Manages dependencies and the critical path" | An AI agent needs the dependency map format, the critical-path algorithm, and the escalation threshold. |
| §13.3 | "Hardens devices" | An AI agent needs the specific hardening checklist (which debug ports, which key storage mechanism, which anti-rollback scheme). |
| §14 (Diagram) | All edge labels | Labels like "Requirements & Roadmap" and "System Architecture Doc" name artifacts but don't specify formats, versions, or delivery cadences. |

**Pattern:** The workflow uses **human-collaboration verbs** (coordinate, manage, ensure, work closely, lead, partner) that are appropriate for a human team document but insufficient for AI agent instruction. The SKILL.md files consistently replace these with **machine-actionable verbs** (implement, validate, measure, report, raise ADR, fail closed, block release).

### 3.3 Human Review Feedback Loops

**Feedback loops defined:** #ai-readiness

The SKILL.md files define several explicit human-in-the-loop mechanisms that the workflow document **does not surface**:

1. **ADR Process** — Every SKILL.md requires that any contract/budget/specification deviation be raised as a formal ADR with measured evidence. ADRs are reviewed via pull request with required approvers. This is the **primary human review mechanism** embedded in the architecture, referenced in all 12 technical SKILL.md files but only mentioned implicitly in the workflow (§2.1: "records decisions as version-controlled ADRs").

2. **Security Release Gate** — [[SECURITY_ENGINEER_SKILL|Security Engineer]] grants the Security Engineer **veto authority** to block a release on security grounds. This is a mandatory human-in-the-loop checkpoint. The workflow document mentions security review in the Threat Model context but does not explicitly state the Security Engineer's release-blocking authority.

3. **QA Go/No-Go Recommendation** — [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA Engineer]] states QA produces a release-readiness assessment and recommendation; the final go/no-go decision is shared with the TPM and Architect. The workflow mentions QA's test reports but not the release-gate authority.

4. **PO Feasibility-vs-Priority Conflict Escalation** — [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] defines a formal escalation process when business priority and technical feasibility conflict: the PO/TPM **must not resolve this conflict alone** but must surface it to executive stakeholders with documented options from the Architect. The workflow has no mention of this conflict-resolution mechanism.

5. **Model Validation Gate (MLOps)** — [[MLOPS_ENGINEER_SKILL|MLOps Engineer]] specifies that a model failing validation must never be auto-promoted and may require a human approval gate for production. The workflow does not mention this gate.

**Missing feedback loops:** #ai-readiness #risk

1. **No field-feedback-to-backlog loop.** Post-deployment field data (device performance, user satisfaction, defect reports) has no defined path back into the backlog. The Product Owner SKILL.md §3.5 mentions "field feedback loops" but no specific mechanism.

2. **No model-performance-to-retraining loop in the workflow.** The MLOps SKILL.md defines drift monitoring → retraining trigger → automated redeployment, but this cycle is invisible in the workflow diagram and text.

3. **No architecture-review cadence.** The Architect SKILL.md defines architecture reviews at each lifecycle stage, but the workflow does not mention when architecture is reviewed or by whom.

**Recommendation:** Add a "Human Review Gates" section to the workflow document enumerating: (a) ADR review/approval, (b) Security release gate (veto), (c) QA release-readiness sign-off, (d) PO feasibility-conflict escalation, (e) Model validation gate, and (f) Architecture review cadence. Each gate should specify: who decides, what evidence is required, and what happens if the gate fails. #recommendation

### 3.4 Overall AI-Assisted Maturity Assessment

**Rating: `Ready with Human-in-the-Loop`** #ai-readiness

**Evidence for the rating:**

- **The SKILL.md ecosystem is AI-ready.** Every one of the 14 SKILL.md files contains a complete AI Agent Execution Guide with persona, mandatory pre-delivery checklist, forbidden actions, and parameterized prompt templates. An AI agent assigned to any role can execute autonomously within that role's defined scope, subject to the checklist and forbidden-actions constraints. The prompt templates are specific enough to be copy-pasted into an AI session.

- **The workflow document is NOT AI-ready as a standalone.** It lacks execution guidance and would need to be supplemented by the SKILL.md files for any AI agent to function.

- **Human-in-the-loop is required because:** (a) The ADR process requires human review and approval for any contract/budget deviation, (b) The Security release gate requires human sign-off, (c) The QA go/no-go recommendation feeds a human decision, (d) The PO feasibility-conflict escalation requires executive human judgment, and (e) Physical hardware validation steps (board bring-up, EMC testing, environmental testing) require human-operated lab equipment and cannot be fully automated.

- **The system is NOT ready for `Fully Autonomous`** because of these mandatory human gates and because two roles critical to the product lifecycle (Business Consultant, IoT Researcher) are defined in SKILL.md but not integrated into the workflow.

**Recommendation:** To advance to `Fully Autonomous` for software/firmware/cloud-only changes (excluding physical hardware), the workflow needs: (1) full integration of the Business Consultant and Researcher roles, (2) automated gating of all human review checkpoints where the evidence is purely digital (test results, metrics, schema conformance), and (3) a machine-readable interface contract registry that AI agents can validate against without human interpretation. #recommendation

---

## 4. Workflow Gaps & Risks

### 4.1 Lifecycle Coverage Gaps

Cross-referencing the lifecycle stages from Phase 2 (**Research → Planning → Development → Execution → Production-Ready → Post-Launch/Market**) against the workflow document: #workflow-gap #risk

| Lifecycle Stage | Covered in Workflow? | Evidence |
|---|---|---|
| **Research** | ❌ Not covered | The workflow has no research-stage activities. All 12 roles are engineering roles. The [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL\|Researcher]] covers this stage, but it is not in the workflow. |
| **Planning** | ⚠️ Implicit | The workflow mentions "Delivers to all engineering roles the System Architecture Document... that gate downstream development" (§2.3), implying a planning stage, but no planning-stage activities or deliverables are defined for any role. |
| **Development** | ✅ Covered | Each role's JD describes implementation activities. |
| **Execution** | ⚠️ Implicit | The workflow mentions "Delivers" artifacts, implying execution outputs, but does not describe integration, testing, or validation activities. |
| **Production-Ready** | ❌ Not covered | No role in the workflow describes production-readiness activities (final sign-off, hardening, runbooks, disaster recovery). Every SKILL.md §3.5 covers this stage in detail. |
| **Post-Launch/Market** | ❌ Not covered | No role describes post-launch activities (field monitoring, customer feedback, OTA update governance, incident response, product-market fit assessment). The [[BUSINESS_CONSULTANT_SKILL\|Business Consultant]] covers post-launch in §3.4–3.5, but is not in the workflow. |

**Finding:** The workflow document covers only the **Development** stage explicitly. Planning and Execution are implicit. Research, Production-Ready, and Post-Launch/Market are **entirely absent**. This is a critical gap — the workflow describes a team that builds things but does not describe how the team researches what to build, validates readiness for production, or operates and improves after launch. #workflow-gap #risk

**Recommendation:** Add lifecycle stage sections to the workflow document, even if brief, showing each role's primary activities in Research, Planning, Development, Execution, Production-Ready, and Post-Launch/Market. Alternatively, add a lifecycle cross-reference table linking each stage to the relevant SKILL.md §3 sections. #recommendation

### 4.2 Missing Interface Contracts

The following **critical** interface contracts are defined in SKILL.md files but **absent from both the workflow text and the Mermaid diagram**: #workflow-gap #risk

1. **ARCH → ALL downstream roles (budgets/contracts fan-out).** The workflow diagram shows the Architect delivering to only HW, FW, and BE. In reality, the Architect defines contracts for all 11 other roles. An AI agent for MLOps, Data, QA, FE, or DEVOPS would not know from the workflow that the Architect is their contract authority.

2. **EDGE → HW (sensor data requirements).** The Edge AI/ML Engineer specifies sensor sampling rate, resolution, dynamic range, and SNR targets that the Hardware Engineer selects sensors to satisfy. This is absent from the workflow diagram, which shows only HW → EDGE (Sensor Specs) but not the reverse dependency: EDGE defines the sensor data spec that HW must meet.

3. **SEC → ALL implementing roles (security baseline).** The Security Engineer defines the baseline that Firmware, Hardware, Backend, DevOps, and MLOps implement. The workflow diagram shows SEC → FW and SEC → BE only. Missing: SEC → HW (secure-element requirements, debug lockdown), SEC → DEVOPS (signing infrastructure), SEC → MLOPS (model signing/integrity), SEC → EDGE (model integrity).

4. **QA → ALL roles (validation feedback).** The workflow diagram shows QA → ARCH only. In reality, QA provides HIL results to FW, model validation to EDGE, API test results to BE, and receives test infrastructure from DEVOPS and test fixtures from HW. These bidirectional feedback loops are critical for defect remediation and are entirely absent from the diagram.

5. **DEVOPS → HW (device provisioning/enrollment).** The DevOps Engineer provides the provisioning infrastructure that the Hardware Engineer's production-programming interface feeds. This interface is critical for manufacturing and fleet onboarding but is absent.

6. **Business viability flow (Business Consultant → PO → ARCH).** Since [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] is not in the workflow, the entire market-requirements-to-engineering-constraints translation chain is missing. The PO/TPM SKILL.md defines this interface with the Business Consultant, but the workflow has no Business Consultant role for the PO to interface with.

7. **Research-to-engineering transfer (Researcher → ARCH → HW/FW/EDGE).** Since [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]] is not in the workflow, there is no defined path for novel research findings to enter the product pipeline.

**Recommendation:** Add the missing interface contracts to the Mermaid diagram as a minimum. For the Business Consultant and Researcher, either integrate them into the workflow or explicitly state that they are external roles with defined SKILL.md interfaces that feed into the workflow at specific touchpoints (Business Consultant → PO/TPM; Researcher → Architect). #recommendation

### 4.3 Top 5 Workflow-Specific Risks

**Risk 1: AI Agent Scope Creep Due to Missing "Does NOT Own" Boundaries** #risk #recommendation

- **Role pairs affected:** All 12 roles × all other roles.
- **Description:** The workflow document defines what each role *does* but never what each role *does NOT do*. Every SKILL.md has an explicit "Explicitly Does NOT Own" section. An AI agent executing a role from the workflow alone lacks negative constraints and may attempt actions owned by other roles — e.g., a Backend/Cloud Engineer AI could change the telemetry schema (owned by the Architect), or a Firmware Engineer AI could modify the ML model architecture (owned by Edge AI/ML).
- **Product impact:** Cross-role contamination, silent contract violations, integration failures discovered late, and architecture drift. In an embedded/IoT system, a firmware change that silently exceeds the flash budget or an ML model change that increases tensor-arena size can cause devices to fail OTA updates or crash in the field.
- **Mitigation:** Add an explicit "Does NOT Own" subsection to each role in the workflow, extracted from the corresponding SKILL.md. Alternatively, add a preamble statement: "For authoritative scope boundaries including explicit exclusions, see §2 (Core Mission & Scope) of each role's SKILL.md."

**Risk 2: Unintegrated Product-Market Feedback Loop** #risk #recommendation

- **Role pairs affected:** Business Consultant → Product Owner/TPM → Embedded Systems Architect → all engineering roles.
- **Description:** The Business Consultant role (which owns market viability, pricing, GTM strategy, and post-launch product-market fit assessment) is absent from the workflow. Without it, there is no defined mechanism for: (a) market requirements and pricing constraints to enter the engineering pipeline, (b) competitive intelligence to inform architecture trade-offs, (c) post-launch field data (revenue, churn, NPS) to feed back into the backlog.
- **Product impact:** The engineering team builds to the PO's backlog without market-validated prioritization. Features may be technically sound but commercially non-viable. Pricing may not cover BOM + cloud OpEx. GTM timing may miss seasonal deployment windows (critical for agricultural IoT). Post-launch, there is no defined owner for monitoring product-market fit or recommending pivots.
- **Mitigation:** Integrate the Business Consultant into the workflow as a strategic input role feeding the Product Owner/TPM, with a defined cadence (weekly backlog alignment, quarterly roadmap prioritization, per-release GTM readiness review) per [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] §6.1.

**Risk 3: Research-to-Production Gap with No Technology Transfer Mechanism** #risk #recommendation

- **Role pairs affected:** IoT & Embedded Systems Researcher → Embedded Systems Architect → Hardware Engineer, Firmware Engineer, Edge AI/ML Engineer.
- **Description:** The Researcher role (which discovers novel sensing principles, energy-harvesting paradigms, and bio-inspired architectures) is absent from the workflow. Without a technology transfer mechanism, research outputs — PoC prototypes, characterized datasets, feasibility assessments — have no defined path into the engineering pipeline. The Researcher's SKILL.md §3.6 defines a complete Technology Transfer Pack and joint feasibility assessment process with the Architect and PO, but this is invisible to the workflow.
- **Product impact:** Research findings remain in the lab. The product roadmap is limited to commercially available technologies. Competitive differentiation from novel IP is lost. Conversely, if research findings are transferred ad hoc without the defined feasibility gate, engineering teams may attempt to productize immature technologies, causing schedule delays and reliability failures.
- **Mitigation:** Add the Researcher to the workflow with a "Technology Transfer" interface flowing to the Embedded Systems Architect, triggered by a Feasibility Assessment Report. Define the transfer gate: TRL assessment, engineering gap analysis, and joint go/no-go with the Architect and PO.

**Risk 4: Single Point of Failure at the Embedded Systems Architect** #risk #recommendation

- **Role pairs affected:** Embedded Systems Architect → all 11 other roles.
- **Description:** The workflow positions the Architect as the sole source of interface contracts, resource budgets, protocol specifications, OTA strategy, and security baseline co-ownership. The Mermaid diagram reinforces this by showing the Architect as the root node from which all primary flows originate (directly or indirectly). If the Architect role is not staffed, is staffed late, or produces incomplete/ambiguous contracts, **every downstream role is blocked**. The workflow has no mechanism for contract delegation, provisional contracts, or contract dispute resolution beyond the ADR process (which itself depends on the Architect as ADR approver).
- **Product impact:** A delayed or incomplete System Architecture Document blocks hardware component procurement, firmware development, ML model sizing, cloud API design, and frontend dashboard development — effectively the entire team. In an AI-assisted workflow, if the Architect AI agent hallucinates a budget or misses a constraint, the error propagates to every downstream role undetected until integration testing.
- **Mitigation:** (a) Define a "minimum viable architecture" — the subset of contracts needed to unblock each role — so that hardware, firmware, and ML can begin in parallel with partial contracts, (b) Add the Senior/Staff Architect tier distinction from [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] §1 to clarify that architecture is a capability, not a single person, (c) Define an architecture review board (Architect + affected leads + TPM) for contract dispute resolution when the Architect is unavailable or contested.

**Risk 5: Mermaid Diagram as Authoritative Reference — Misleading Simplification** #risk #recommendation

- **Role pairs affected:** All roles that consume the diagram as an interface map.
- **Description:** The Mermaid diagram (§14) is the only visual representation of inter-role workflow in the document. It is positioned as the capstone of the workflow definition. However, it captures only 22 of the 80+ interface contracts defined across the text and SKILL.md files. It omits **all bidirectional feedback loops** (QA → FW, QA → EDGE, FE → BE, FW → ARCH), **all security-baseline fan-out** (SEC → HW, SEC → DEVOPS, SEC → MLOPS, SEC → EDGE), **all Architect fan-out** (ARCH → EDGE, ARCH → MLOPS, ARCH → DATA, ARCH → DEVOPS, ARCH → QA, ARCH → FE), and **all reverse-direction edges** (EDGE → HW for sensor data spec, MLOPS → FW for OTA artifacts, DEVOPS → MLOPS for pipeline platform).
- **Product impact:** An AI agent that uses the Mermaid diagram as its interface map will miss the majority of its actual interface contracts. A QA AI agent, for example, would only know to report to the Architect — it would not know to receive test builds from Firmware, model artifacts from Edge AI/ML, or test infrastructure from DevOps. A Security AI agent would only know to interface with Firmware and Backend — missing Hardware, DevOps, MLOps, and Edge AI/ML. The resulting integration gaps would surface late as defects, not early as contract misalignments.
- **Mitigation:** Either: (a) Expand the diagram to a full C4 Container diagram with all bidirectional edges and all role pairs, (b) Split into per-role diagrams (one diagram showing each role's full set of inbound and outbound interfaces), or (c) Add an explicit caveat: "This diagram shows the primary artifact flow only. For the complete interface contract per role, see the Interface Contracts section (§6) of the corresponding SKILL.md."

---

## Appendix A: File Inventory

| # | SKILL.md File | In Workflow? | Workflow Section |
|---|---|---|---|
| 1 | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] | ✅ | §2 |
| 2 | [[FIRMWARE_ENGINEER_SKILL\|Firmware Engineer]] | ✅ | §3 |
| 3 | [[HARDWARE_ENGINEER_SKILL\|Hardware Engineer]] | ✅ | §4 |
| 4 | [[EDGE_AI_ML_ENGINEER_SKILL\|Edge AI/ML Engineer]] | ✅ | §5 |
| 5 | [[MLOPS_ENGINEER_SKILL\|MLOps Engineer]] | ✅ | §6 |
| 6 | [[DATA_ENGINEER_SKILL\|Data Engineer]] | ✅ | §7 |
| 7 | [[DEVOPS_PLATFORM_ENGINEER_SKILL\|DevOps Engineer]] | ✅ | §8 |
| 8 | [[BACKEND_CLOUD_ENGINEER_SKILL\|Backend/Cloud Engineer]] | ✅ | §9 |
| 9 | [[FRONTEND_DASHBOARD_ENGINEER_SKILL\|Frontend Engineer]] | ✅ | §10 |
| 10 | [[QA_TEST_AUTOMATION_ENGINEER_SKILL\|QA Engineer]] | ✅ | §11 |
| 11 | [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]] | ✅ | §12 |
| 12 | [[SECURITY_ENGINEER_SKILL\|Security Engineer]] | ✅ | §13 |
| 13 | [[BUSINESS_CONSULTANT_SKILL\|Business Consultant]] | ❌ | — |
| 14 | [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL\|Researcher]] | ❌ | — |

## Appendix B: Tag Index

| Tag | Count | Primary Sections |
|---|---|---|
| `#workflow-gap` | 18 | §1.1, §1.2, §1.3, §4.1, §4.2 |
| `#consistency-issue` | 8 | §2.2, §2.3, §2.4, §2.5 |
| `#ai-readiness` | 10 | §3.1, §3.2, §3.3, §3.4 |
| `#risk` | 12 | §3.3, §4.1, §4.2, §4.3 |
| `#recommendation` | 14 | All sections |
| `#strength` | 4 | §1.1, §1.2, §2.2, §2.5 |

---

> **Report generated:** 2026-06-19 | **Reviewer:** Principal Systems Architect & AI Workflow Design Expert | **Phase:** 4 of 4 | **Status:** Complete