---
title: "CLAUDE.md"
date: 2026-06-22
status: final
cssclass: claude-reference
---

# CLAUDE.md

> **Purpose:** Master reference for AI agents (Claude Code) in this project.
> **Version:** 1.0 · **Last updated:** 2026-06-22 · **Vault entry point:** [[HOME|HOME.md]].

---

## 1. Project Identity & Scope

A **document-as-code governance system** for an embedded/IoT software + hardware + ML engineering organization — **not** an application codebase. It defines how the product is built, by whom, under what contracts, and subject to what gates.

**Reference product — AgriSpectra:** agricultural IoT sensor node for pre-symptomatic crop disease detection — quantized CNN on an STM32H7 MCU, LoRaWAN uplink, solar power, 50,000-device target fleet, 7-year field lifetime, across an embedded (STM32/ESP32 + Rust/C RTOS, TFLite Micro) → gateway (Raspberry Pi, MQTT/CoAP) → cloud (InfluxDB/TimescaleDB + Parquet, REST/gRPC, React/TS dashboards, MLOps, secure fleet OTA) stack.

**Vault:** `[[wikilinks]]`, `#tags`;

**Audit status:** CONDITIONAL GO

**Five governing principles — internalize these:**
1. **Contract-first:** no role begins implementation without a frozen, versioned interface contract.
2. **Shift-left:** security reviews, QA smoke tests, and architecture gate artifacts are produced during §3.2 Planning, not discovered during §3.4 Execution.
3. **Measure-first, delegate-second:** agents never invent metrics, budgets, or requirements. A missing value triggers an escalation package, never a plausible fill-in.
4. **Never silently deviate:** any infeasibility (unmeetable budget, unimplementable contract, contradictory requirement) is raised as an ADR or CCR with measured evidence.
5. **Parallel development by contract:** all 14 roles work concurrently, possible only by freezing contracts before implementation. Do not bypass the contract-freeze gate to start early.

---

## 2. Vault Architecture

### 2.1 Directory Structure (key paths)
Root: `HOME.md` · `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md` · `CLAUDE.md` · `*_SKILL.md` ×14
`docs/`:
- `ACRONYM_GLOSSARY.md`
- `agent-protocol/` — `MULTI_AGENT_COORDINATION_PROTOCOL.md` + AGENT_IDENTITY / A2A_MESSAGE / CONTRACT_REGISTRY / COORDINATION_LEDGER / AGENT_GOVERNANCE_PARTICIPATION schemas
- `automation/RECIPROCITY_AUDIT_SPEC.md`; `evaluation/EVALUATION_HARNESS_SPEC.md`
- `fmea/SYSTEM_FMEA_V1.md`; `operations/INCIDENT_COMMANDER.md`; `metrics-pipeline/` (PIPELINE_README, deployment_guide)
- `review_v1/ v2/ v3/`; `schemas/` (SCHEMA_INDEX + 8 schemas: ADR, CCR, DQIR, IRD, OCM, SIRC, TTP, BIA); `security/DEVICE_ATTESTATION_SPEC.md`

### 2.2 File Types & Authoritativeness

| File type | `cssclass` | Tier-1 tag | Authoritative? |
|---|---|---|---|
| `*_SKILL.md` (×14) | `skill-card` | `skill-card` | **Yes** |
| `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md` | `workflow-doc` | `workflow-doc` | **Yes** |
| `MULTI_AGENT_COORDINATION_PROTOCOL.md` | `protocol-spec` | `MACP` | **Yes** (status: draft) |
| `docs/schemas/*.md` | — | `machine-parseable` | **Yes** |
| `docs/fmea/`, `operations/`, `evaluation/`, `security/` specs | — | — | **Yes** |
| `docs/review_v*/`, `OBSIDIAN_AUDIT_REPORT.md` | `review-report-*` | `review-*` | Historical only — not prescriptive |
| `prompt_*.md` (root) | — | — | **Not authoritative — never cite** |
| `HOME.md` | `moc` | `moc` | Navigation only |

**Rule:** `prompt_*.md` vault-root files are working documents — never cite them as sources of governance, convention, or specification.

### 2.3 Session Reading Order
(1) `CLAUDE.md`; (2) `HOME.md`; (3) `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md` §1 and §14; (4) the active role's `*_SKILL.md` §2 and §9.

---

## 3. Naming & Style Conventions

Evidence base for §3 and §4: 14 SKILL.md files. Conventions at ≥ 10/14 (> 70%) are **RULES**. Named inconsistencies are stated explicitly — do not hide or "correct" them.

### 3.1 File Naming
**RULE (14/14):** Primary vault documents use `SCREAMING_SNAKE_CASE` with a type suffix — skill cards `ROLE_NAME_SKILL.md`; workflow doc `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md`; schemas `ARTIFACT_NAME_SCHEMA.md`; MACP specs descriptive `SCREAMING_SNAKE_CASE`; review files `REVIEW_PHASE_N_TOPIC.md` / `REVIEW_VN_PHASE_N_TOPIC.md`. No spaces, hyphens, or lowercase in primary-doc filenames.

### 3.2 YAML Frontmatter
**RULE (14/14):** Every vault document opens with a YAML block of exactly five fields, in order: `title`, `date`, `status`, `tags`, `cssclass`. All mandatory; omitting any is a violation.
- `title:` double-quoted; skill cards `"Role Display Name — Skill Card"`. Separator is em dash `—` (U+2014), never `-` or `--`.
- `date:` `YYYY-MM-DD` (current skill cards: `2026-06-20`). `status:` `draft` | `review` | `final` (current skill cards: `final`).
- `tags:` YAML block sequence (`- item`), never inline flow (`[a, b]`). `cssclass:` skill cards `skill-card`; workflow doc `workflow-doc`.

### 3.3 Heading Structure
**RULE (14/14):** First body line after frontmatter is an H1 mirroring the filename exactly, incl. `.md` (e.g. `# FIRMWARE_ENGINEER_SKILL.md`). Top-level `## N. Name`; subsections `### N.M Name`; sub-subsections `#### N.M.X` (rare; ARCH NFR matrix only).
**RULE (14/14):** Every SKILL.md has exactly 10 top-level sections: `1 Role Identity` / `2 Core Mission & Scope` / `3 Lifecycle Stage Engagement` / `4 Technical Competencies` / `5 Deliverables & Artifacts` / `6 Interface Contracts` / `7 Decision Authority & Governance` / `8 Standards & Best Practices` / `9 AI Agent Execution Guide` / `10 Success Metrics & KPIs`.
**Approved §3-heading deviations (do not "correct"):** RES = `3. Research Lifecycle Engagement`; BIZ = `3. Business–Product Lifecycle Stage Engagement`.

### 3.4 Wikilinks
**RULE (14/14):** In-vault cross-references use `[[FULL_SCREAMING_SNAKE_CASE_FILENAME|Human-Readable Alias]]` (target = filename without `.md`). Bare `[[FILENAME]]` (no alias) is permitted only in the `HOME.md` index; elsewhere always include an alias. Never use lowercase targets, alias-only links, or plain text where a cross-reference is intended.

### 3.5 Tags
**RULE (14/14):** Body hashtags use `#kebab-case` only — no `#CamelCase`, no `#SCREAMING_SNAKE_CASE`. Audit codes follow `#PREFIX-N` (uppercase prefix): `#MR-N`, `#CR-N`, `#HR-N`, `#B-N`, `#P4-M-N`; placed at the end of bullet items, never mid-sentence.
**RULE (14/14):** Frontmatter `tags:` is a three-tier taxonomy: Tier 1 document class (`skill-card` / `workflow-doc`); Tier 2 ecosystem (`embedded-iot`, always second); Tier 3 role domain (one kebab-case role tag — see Appendix B).

### 3.6 Tables
**RULE (14/14):** Standard `|Col|Col|` pipe format with a `|---|---|` separator. No HTML tables. Alignment decorators optional. §5 deliverables and §4 skill tables have fixed column structures (see §4).

### 3.7 Bold & Emphasis
**RULE (14/14):** Inline field labels use `**Label:**` (bold label, colon, space, value). Never plain `Label:` or a `###` substitute for an inline label. Italics `_text_` only for introduced terms or template placeholders — never as a substitute for a bold label.

### 3.8 Bullet Lists
**RULE (14/14):** `- ` (hyphen, space) for all bullets; no `*` or `+`; nested bullets use 2-space indentation.
**RULE (10/14):** §1 identity blocks for the 10 engineering roles render field labels as bullets (`- **Field:** Value`); the 4 strategic/research roles (PO, FE, RES, BIZ) use bold-heading paragraphs (`**Field:** Value`) — approved deviation.

### 3.9 Deliverable Naming & Versioning
**RULE (14/14):** Every deliverable in a `status: final` document carries a SemVer (`MAJOR.MINOR.PATCH`) in the §5 `Versioning Approach` column; binary artifacts (firmware images, TFLite models) additionally carry a Git SHA. MAJOR = breaking interface change (requires CCR + ADR); MINOR = backward-compatible addition; PATCH = backward-compatible fix. "Version TBD", "v?", or unversioned entries in `final` documents are violations.

### 3.10 Acronyms & Units
**RULE (14/14):** Every technical acronym is defined on first appearance per section: `ACRONYM (Full Expansion in Title Case)`. Canonical expansions: [[ACRONYM_GLOSSARY|Acronym Glossary]].
**RULE (14/14):** Every numerical quantity in a `status: final` document carries an explicit unit. Forbidden in final documents: `TBD`, `~N`, `approximately N`, or a bare number where a physical quantity is expected. Standard units: `KB`, `MB`; `mW`, `mWh`, `µA`; `ms`; `Hz`, `MHz`; `°C`; `%`; `dB`; `mΩ`, `pF`. Mandatory §9.2 checklist item in all 10 engineering files.

---

## 4. Output Format Conventions

### 4.1 §5 Deliverable Table
**RULE (14/14):** §5 is a single table with exactly these headers, in order: `|Artifact|Description|Consumers|Format/Standard|Versioning Approach|`. No variation. `Versioning Approach` = SemVer (documents) / Git-SHA+SemVer (binaries). All 14 conform.

### 4.2 §6 Interface Contract
**RULE (14/14):** Every §6.N subsection contains the mandatory triple — `**Provides:**`, `**Requires:**`, `**Cadence:**`. Missing any element is a violation.
**RULE (10/14):** The 10 engineering roles open §6 with a blockquote before `### 6.1`: *"For each collaborator: **Provides** (what [Role] supplies), **Requires** (what [Role] needs), **Cadence** (synchronization points)."* The 4 strategic/research roles prefix the role name in the triple (`**PO/TPM provides:**`, …) and omit the blockquote — approved deviation.

### 4.3 §9.2 Pre-Delivery Checklist
**RULE (10/14):** Engineering roles: §9.2 is a numbered list (items 1–14 or 1–15); checkboxes forbidden. Mandatory final item (variant): *"All acronyms are defined on first use and all quantities carry explicit units."* Mandatory near-final item (variant): *"Any [contract/budget/requirement] infeasibility is raised as an ADR with measured evidence — never silently deviated."* The 4 strategic/research roles use `- [ ]` checkboxes — do not apply the numbered format to them.

### 4.4 §9.3 Forbidden Actions
**RULE (10/14):** Engineering roles: every §9.3 item begins with `- Do NOT [verb]…`. Approved deviations: PO uses a `"must **never**:"` preamble + bare verbs; FE uses `"The agent must NOT [verb]"`; RES and BIZ use bare imperatives (no prefix). Use `Do NOT` exclusively for new engineering files; never apply it to strategic/research roles.

### 4.5 §9.4 Prompt Templates
**RULE (10/14):** Engineering roles: each §9.4 template is a fenced code block with five labeled fields in order — `Role:` / `Goal:` / `Inputs:` / `Produce:` / `Constraints:` — labeled **Template A**–**E** (FE has A–F) as bold headers. Approved deviations: PO uses a prose template; FE uses `Task:`/`Output:`; RES and BIZ use all-caps `TASK:` / `CONTEXT:` / `REQUIRED OUTPUTS:` / `CONSTRAINTS:`.

### 4.6 §3 Lifecycle Stages
**RULE (12/14):** §3.1–§3.6 names (engineering roles + PO/FE): `3.1 Research` / `3.2 Planning` / `3.3 Development` / `3.4 Execution` / `3.5 Production-Ready` / `3.6 Post-Launch/Market`. Approved deviations: RES uses 8 research-specific subsections (Ideation & Hypothesis Formation → Experimental Design → Experimentation → Analysis → Publication → Technology Transfer → Post-Launch → Research-to-Planning Gate); BIZ uses 6 business-specific (Market Discovery → Business Feasibility → GTM Planning → Scaling → Portfolio Management → Post-Launch).
**RULE (14/14):** §3.6 in all 14 files contains `**Activities:**` (bold-named bullets with `#hashtags`) and `**Deliverables:**` blocks.
**RULE (14/14):** §3.6 in all 14 files contains the universal cross-layer incident-response text (verbatim/near-verbatim; canonical wording in any SKILL.md §3.6): respond to [[INCIDENT_COMMANDER|Incident Commander]] direction within the role's response SLA; document temporary deviations for retroactive ADR within 5 business days of incident closure; join the annual incident drill. The three hashtags `#cross-layer-incident #incident-commander #emergency-tempo` must always appear.

### 4.7 §7 Decision Authority
**RULE (12/14):** Four-part structure for the 12 conforming roles: (1) `**Decisions owned unilaterally:**` (bullets); (2) `**Decisions requiring consensus or escalation:**` (bullets); (3) `**ADR participation:**` (paragraph — Proposing Author / Consulted / Informed / Veto); (4) `**Escalation path:**` (paragraph). Approved deviations: RES and BIZ omit the ADR-participation paragraph (three-part structure).

---

## 5. Role Ecosystem

### 5.1 Complete Role Inventory
**16 roles total:** 14 primary (each with a SKILL.md) + 2 fractional functions.

| Code | Display Name | SKILL.md File |
|---|---|---|
| `ARCH` | Embedded Systems Architect | `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| `FW` | Firmware Engineer | `FIRMWARE_ENGINEER_SKILL.md` |
| `HW` | Hardware Engineer | `HARDWARE_ENGINEER_SKILL.md` |
| `ML` | Edge AI/ML Engineer | `EDGE_AI_ML_ENGINEER_SKILL.md` |
| `MLOPS` | MLOps Engineer | `MLOPS_ENGINEER_SKILL.md` |
| `DATA` | Data Engineer | `DATA_ENGINEER_SKILL.md` |
| `DEVOPS` | DevOps/Platform Engineer | `DEVOPS_PLATFORM_ENGINEER_SKILL.md` |
| `BACK` (alias `CLOUD`) | Backend/Cloud Engineer | `BACKEND_CLOUD_ENGINEER_SKILL.md` |
| `FE` | Frontend/Dashboard Engineer | `FRONTEND_DASHBOARD_ENGINEER_SKILL.md` |
| `QA` | QA & Test Automation Engineer | `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` |
| `SEC` | Security Engineer | `SECURITY_ENGINEER_SKILL.md` |
| `PO` | Product Owner / Technical Project Manager | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md` |
| `RES` | IoT & Embedded Systems Researcher | `IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md` |
| `BIZ` | Business Consultant | `BUSINESS_CONSULTANT_SKILL.md` |
| `ARCH-DEP` | Deputy Architect *(fractional; no SKILL.md, inherits parent scope)* | non-breaking ADR authority only — within `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` |
| `SEC-DEP` | Deputy Security Engineer *(fractional; no SKILL.md, inherits parent scope)* | Standard-tier sign-off only |
| Process Architect | function of QA *(fractional; no SKILL.md, inherits parent scope)* | owns the Engineering Process Review loop + Process Health Dashboard — `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` §3.7 |

**Operational coordinator:** `IC` — [[INCIDENT_COMMANDER|Incident Commander]]; coordination authority during declared cross-layer incidents; not a permanent role (weekly rotation, owner: QA/Process Architect).
**Engineering vs. strategic/research split** (governs which format conventions apply): **10 engineering (strict):** ARCH, FW, HW, ML, MLOPS, DATA, DEVOPS, BACK, QA, SEC. **4 strategic/research (approved deviators):** PO, FE, RES, BIZ. Uncertain on a new role? Default to engineering format and escalate if genuinely ambiguous.

### 5.2 SKILL.md Section Contents
Section names: §3.3; format per section: §3–§4. Unique required contents — §1: 5-field identity block (Role Title, Team, Reports To, Seniority, Summary) + 4-tier ladder; §2: **Owns** / **Influences** / **Explicitly Does NOT Own** + **Governing principle**; §3: 6 subsections, each **Activities** + **Deliverables** (§3.6 = universal incident text); §4: proficiency-legend blockquote + 4-column skill tables; §10: **Technical metrics** + **Process & team metrics** (custom for PO, RES, BIZ).

### 5.3 Interface Contract Model (91 Symmetric Edges)
C(14,2) = 91 unique role-pair relationships; every pair has a contract from both sides. Authoritative visual: Mermaid diagram in `EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md` §14. Find a contract: target role's `*_SKILL.md` → §6 → the `### 6.N` subsection for the collaborator. Symmetry is enforced by `docs/automation/RECIPROCITY_AUDIT_SPEC.md` (what A provides to B = what B requires from A). Contract IDs (MACP): `ROLE-A↔ROLE-B-NNN` (e.g. `FW↔DATA-001`). Changing a ratified contract requires a CCR (`docs/schemas/CCR_SCHEMA.md`, `CCR-NNNN`); a `BLOCKING` CCR halts the associated IRD gate until resolved.

### 5.4 Role Activation Sequence (Wave Model)
Five-wave activation: Wave 0 Human-operated → Wave 1 MACP Registries → Wave 2 A2A Messaging → Wave 3 Tier 3 Autonomy → Wave 4 Governance; see [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]].
Per-role AI activation requires: (a) Evaluation Harness baseline (≥ 30 human samples per deliverable); (b) MACP at Wave 1+; (c) no open BLOCKING CCR on that role's contracts.

---

## 6. Governance & Decision Making

### 6.1 ADR Process
ADR (Architecture Decision Record): one significant technical decision + context, alternatives, consequences. Schema `docs/schemas/ADR_SCHEMA.md`; ID `ADR-NNNN`. Lifecycle: `Proposed` → `Under Review` → `Accepted` / `Rejected` / `Superseded`.
**Mandatory when** (Never-Silently-Deviate, universal): any platform/protocol/technology choice outside the approved stack, security-baseline change (even one that "only affects a test device"), or production/OTA governance change; any contract/budget/standard/requirement unmeetable as written, or any breaking interface contract change (must precede the CCR and version bump); any temporary deviation during an incident (retroactive ADR within 5 business days of closure).
**Standing:** Proposing Author — any role. Veto / final approver for STRATEGIC ADRs — ARCH + SEC (security-baseline). Consulted — DATA, DEVOPS, FW (schema/contract), ML (model deployment). Informed — FE, BIZ (architectural ADRs affecting their interfaces).
**Key `ADR_SCHEMA.md` validations:** ≥ 2 alternatives (V-ADR-03); valid status transitions only (V-ADR-07); `affected_contracts` resolve against the registry (V-ADR-09); BIA required for cost-material ADRs (V-ADR-12).

**ADR storage:** `docs/adr/` — one ADR per file. File naming `adr-NNNN.md` (lowercase, zero-padded, sequential); internal ID `ADR-NNNN` (4-digit, per `ADR_SCHEMA.md` V-ADR-01). Master registry: [[ADR_INDEX|ADR Index]] (append-only). Author new ADRs from [[ADR_TEMPLATE|ADR Template]]. The directory, numbering convention, index, and template were established by ADR-0001 (see [[ADR_INDEX|ADR Index]]).
[NOT YET AVAILABLE — fill in manually: the approved technology stack that defines "outside the stack" for ADR trigger purposes.]

### 6.2 Architecture Review Board (ARB)
Governs platform/protocol/interface/NFR decisions crossing ≥ 2 role boundaries. Charter: `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §7.Z. Architect chairs; STRATEGIC ADRs require ARB ratification. MACP L2 agents may submit data + cast non-binding advisory votes; humans retain all binding authority. Tier 2 (HIGH) decisions: agent Propose→Confirm + non-binding vote, then a human ARB member ratifies. Agents never short-circuit ARB authority.

**ARB membership / quorum / cadence:** instantiated in [[ARB_CHARTER_INSTANTIATED|ARB Charter (Instantiated)]] — subordinate to `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §7.Z, which remains authoritative. **Decision records:** ARB Decision Record format (same as ADR), tagged `#ARB` / `#arb-decision`, stored `docs/arb/decisions/arb-NNNN.md`; cross-referenced from [[ADR_INDEX|ADR Index]] when an ADR would otherwise be required.

### 6.3 Decision SLA Tiers (MACP §4)

| Tier | Class | SLA | Agent Authority | Human Role |
|---|---|---|---|---|
| **1** | CRITICAL | 4 business hours | Escalation package only; zero autonomous resolution | Decides. Permanent HITL gate |
| **2** | HIGH | 2 business days | Coordinate + non-binding vote → recommendation | Ratifies the binding decision |
| **3** | MEDIUM | 5 business days | Decide autonomously when confidence ≥ 0.70 and novelty ≤ 0.80 | Audits / may override |
| **4** | LOW | 10 business days | Decide autonomously; Auto-Confirm by default | Audits / may override |

**Classification rule:** classify via the `tier_classification` block in the Contract Registry (`docs/agent-protocol/CONTRACT_REGISTRY_SCHEMA.md` §7). If ambiguous, default **upward** (more conservative). Never resolve at a lower tier than the true classification. **Tier 1 covers:** Security release veto, Architect production gate, any platform/protocol/security-baseline change, anything safety-critical.

### 6.4 Contract Clarification Record (CCR)
Formal process to clarify or change a ratified interface contract. Schema `docs/schemas/CCR_SCHEMA.md`; ID `CCR-NN`. Required whenever a role finds an ambiguity, gap, or necessary change in a §6 clause. Severity `BLOCKING` / `HIGH` / `MEDIUM` / `LOW`; a `BLOCKING` CCR halts all associated IRD gates until `RESOLVED`. Agents scan all open CCRs before accepting any IRD — an `OPEN`/`IN_REVIEW` + `BLOCKING` CCR fires `ESC-BLOCK`. Propose→Confirm is the machine-speed CCR for Tier 3–4 ambiguities; > 3 Reject/Counter rounds (`ESC-DEAD`) files a formal human CCR; CCRs unresolved within 10 business days escalate to an ADR with ARB review.

### 6.5 Budget Trade Tolerance Bands
[NOT YET AVAILABLE — fill in manually from `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §5 NFR matrix and per-node resource budget tables: the allowed ± margin on Flash/SRAM (KB), power (mW/mWh), and latency (ms) before a budget exceedance triggers an ADR rather than a silent trade.]

### 6.6 Human-in-the-Loop Gates (Permanent Tier 1)
Non-negotiable, non-overridable by any agent or role (incl. ARCH, PO, TSC):
- **HG-01 — Security Engineer Release Veto:** production-release veto over any artifact/architecture change that weakens the security baseline; not overridable by ARCH, PO, or CTO without SEC's explicit clearance.
- **HG-04 — Architect Production Gate:** no system enters §3.5 Production-Ready without explicit Architect sign-off (contract conformance, budget compliance, OTA path integrity, NFR matrix with no `[TBD]` values). Safety-critical design decisions remain under Architect authority even under IC direction.
- **QA Go/No-Go Gate:** QA owns stage transitions §3.3→§3.4 and §3.5→§3.6; a `BLOCKED` from QA halts the lifecycle for the affected component. (V3: QA correctly returned NO-GO on 17 open Critical FMEA chains, RPN ≥ 200 — the gate working as designed.)
- **Agent corollary:** no agent may produce output that bypasses, works around, or argues against these three gates; a task implicitly requiring it must escalate with `ESC-TIER1`.

### 6.7 Release Gate Sequence (§3.5 — do not reverse or skip)
1. Architect robustness sign-off (NFR matrix green, no TBD). 2. Security Engineer release sign-off / veto. 3. QA go/no-go (cross-layer robustness regression suite, IRDs, open CCRs). 4. PO/TPM release decision. 5. OTA readiness review (OCM per model; A/B rollback verified). 6. Business GTM readiness (BIA appended to release ADR).

---

## 7. AI Agent Operation

### 7.1 How to Read a SKILL.md
Read in order: **§2** (owns / does NOT own + Governing principle) → **§5** (the only artifacts this role may generate) → **§6** (every interface contract, both directions) → **§7** (decision authority + ADR standing) → **§9** (operational instruction set). Then confirm every §9.2 checklist item before emitting any output.

### 7.2 §9 Execution Guide Structure
- **§9.1 Persona & Tone:** cognitive posture to hold (engineering roles: bullet characteristics; strategic/research: **Identity:** / **Tone:** / **Scope:** sub-labels). Determines how the agent handles ambiguity, infeasibility, escalation.
- **§9.2 Pre-Delivery Checklist:** all items confirmed before output. Universal items: budget quantities have units; acronyms defined on first use; referenced contracts current and versioned; any infeasibility escalated (not worked around); every deliverable's consumers identified.
- **§9.3 Forbidden Actions:** hard boundaries from §2 "Explicitly Does NOT Own." A violation is grounds to halt and escalate.
- **§9.4 Prompt Templates:** fenced templates A–E (A–F for FE) for common task types.

### 7.3 Multi-Agent Coordination Protocol (MACP)
Master: `docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md` (status: `draft`, v1.0.0).

**5 pillars** (spec files in `docs/agent-protocol/`):

| # | Pillar | Spec file | Key detail |
|---|---|---|---|
| 1 | Identity & Discovery | `AGENT_IDENTITY_SCHEMA.md` | — |
| 2 | Contract Registry | `CONTRACT_REGISTRY_SCHEMA.md` | 91 contracts queryable by role-pair + tier classification |
| 3 | A2A + Propose→Confirm | `A2A_MESSAGE_SCHEMA.md` | schema-validated messages, two-phase negotiation |
| 4 | Coordination Ledger | `COORDINATION_LEDGER_SCHEMA.md` | append-only, SHA-256-chained |
| 5 | Governance Participation | `AGENT_GOVERNANCE_PARTICIPATION.md` | non-binding ARB/EPR votes + data submission |

**Conformance levels:** L0 Observer (read-only) · L1 Participant (full A2A + Tier 3–4 Auto-Confirm + ledger write) · L2 Governance Participant (L1 + ARB/EPR data + non-binding voting; requires `governance_eligible: true` in AID).
**MACP invariant:** no A2A message can change a contract, schema, resource budget, security baseline, or OTA strategy by itself. MACP carries and records proposals; binding changes require the ADR/CCR process with the correct human approver.

### 7.4 Escalation Triggers (MUST escalate, never proceed)

| Trigger | Condition |
|---|---|
| `ESC-CONF` | Confidence < 0.70 (Tier 3/4) or < 0.85 (Tier 2) |
| `ESC-DEAD` | > 3 Reject/Counter rounds on the same `correlation_id` |
| `ESC-NOV` | Novelty score > 0.80 (outside contracted/precedented surface) |
| `ESC-TIER1` | Decision classifies as Tier 1 (CRITICAL) — always |
| `ESC-BLOCK` | A BLOCKING CCR is `OPEN`/`IN_REVIEW` for the contract under coordination |
| `ESC-SLA` | Contract obligation has breached its cadence SLA with no Confirm |
| `ESC-SEC` | Coordination touches security baseline, threat model, or security-relevant release |

Every escalation carries a complete package (MACP §7.2): `escalation_id`, `trigger`, `raised_by`, `routed_to`, `correlation_id`, `contract_ref`, `intent`, `positions`, `impasse`, `recommendation`, `ledger_refs`, `decision_tier`, `sla_deadline`.

### 7.5 Evaluation Harness (Measure First)
Before delegating significant role work, ≥ 30 human-produced samples of each deliverable must be captured and scored via `docs/evaluation/EVALUATION_HARNESS_SPEC.md` (14 roles × 5 deliverables = 70 scored types). An agent without a captured baseline is in Wave 0 — it may only draft artifacts for human review, never act autonomously.

### 7.6 Forbidden Actions (Universal — All Roles)
Regardless of role or task framing:
1. **Do NOT** produce or modify source code in a domain listed under the active role's §2 "Explicitly Does NOT Own" — even to "just sketch it out" or "show an example."
2. **Do NOT** alter a ratified interface contract without a CCR and version bump — even a "minor clarification."
3. **Do NOT** emit any quantity as `TBD`, `~N`, `approximately`, or without units in a `status: final` document.
4. **Do NOT** make a platform, protocol, security-baseline, or OTA governance decision crossing role boundaries without a corresponding ADR.
5. **Do NOT** bypass or argue against HG-01 (Security veto), HG-04 (Architect production gate), or the QA go/no-go.
6. **Do NOT** claim a deliverable is complete without confirming all §9.2 checklist items.
7. **Do NOT** resolve an infeasibility silently — always raise an ADR or CCR and notify consumers.
8. **Do NOT** act on data from a `prompt_*.md` vault-root file — not authoritative.
9. **Do NOT** apply engineering-role formatting templates (numbered §9.2, `Do NOT` §9.3, proficiency-legend blockquote) to PO, FE, RES, or BIZ skill cards.
10. **Do NOT** produce output that requires an `ESC-TIER1` escalation trigger to be valid.

### 7.7 Working with the Vault
- **Reading:** always read the active role's SKILL.md first; re-read its §2 and §9 at session start (do not rely on prior-session memory).
- **Writing:** confirm valid 5-field frontmatter, correct H1 (exact filename incl. `.md`), correct conventions for the doc type, no `TBD` in `final` content, acronyms defined on first use, units on every quantity.
- **Linking:** use `[[FILENAME|alias]]`; never invent a wikilink to a non-existent file — mark as `[NOT YET AVAILABLE — fill in manually: …]`.
- **Git:** do not commit without user approval;

---

## 8. Cross-Cutting Processes

### 8.1 OTA Governance
Closed-loop chain **MLOPS→DEVOPS→FW→BACK→MLOPS:** MLOps produces a quantized TFLite Micro model + OTA Compatibility Manifest (OCM, `docs/schemas/OTA_COMPATIBILITY_MANIFEST_SCHEMA.md`, ID `model.id + version`) → DevOps runs staged rollout (Mender/balena) with canary thresholds, verifying OCM budget arithmetic + firmware compatibility → Firmware validates model signature, A/B partition swap, monitors boot health + accuracy delta, rolls back on boot failure → Backend manages OTA orchestration, device shadow state, fleet rollback → MLOps monitors post-deployment drift vs. baseline (loop closes).
Gating OCM fields: `flash_budget_check.result` must be `PASS`; all `dqir_clearance` IDs resolved; `firmware_compatibility.excluded_versions` blocked at dispatch. SEC veto can block any OTA release weakening anti-rollback or model signing.
**Residual risk (FC-026, V3):** model anti-rollback weaker than firmware anti-rollback — a downgraded/replayed model could be accepted by an old-firmware device. Mitigation: per-model monotonic version counter on-device. Open FMEA item.

### 8.2 Security Across the Lifecycle
**Shift-left gate (§3.2 Planning; applies to BACK, DATA, DEVOPS, HW, FW, MLOPS):** SEC delivers a Security Design Review Report (SIRC, `docs/schemas/SECURITY_IMPLEMENTATION_READINESS_SCHEMA.md`, ID `SIRC-ROLE-SNNNN`) before Planning → Development. Outcomes: `APPROVED` (proceed); `CONDITIONAL` (conditions logged to §3.3 checklist, then proceed); `BLOCKED` (do not start; re-review after remediation). Markers: `#shift-left #security-design-review #MR-10`.
**Device attestation:** `docs/security/DEVICE_ATTESTATION_SPEC.md` — RATS (IETF RFC 9334) + EAT + DICE. Phase 1 needs no new hardware (uses the secure-boot chain); closes hardware audit gap HA-A3, delivers Phase 4 Milestone P4-M5.
**Security baseline (mandatory, all production devices):** secure boot, signed OTA images, mTLS with X.509 device certificates, hardware root of trust, debug-port lockdown, firmware anti-rollback via monotonic counter.
**`ESC-SEC`:** any coordination touching the security baseline, threat model, or a security-relevant release must escalate — agents may only propose; SEC owns all binding decisions here.

### 8.3 Robustness & FMEA
**System FMEA:** `docs/fmea/SYSTEM_FMEA_V1.md` — 36 cross-layer failure chains under IEC 60812 (FMEA) + IEC 61025 (FTA).
**Current state (V3):** 17 Critical chains (RPN ≥ 200) `Open — mitigation MANDATORY`; 15 chains at Detectability D ≥ 8 (no contracted detection control); 9 controls "do not exist today" (build during §3.3). Keystone chains: **FC-022** (closed-loop silent corruption: sensor drift → telemetry → retraining → re-baselined drift monitor → fleet-wide silent erosion; RPN 405, D = 9), **FC-001** (in-range spectral-AFE drift; RPN 486, D = 9). End-to-end detection coverage ≈ 53% vs. a ≥ 95% gate.
**NFR Robustness R1–R5:** FMEA-derived; zero `[TBD]` values (enabled S2 PASS in V3). [NOT YET AVAILABLE — fill in the 5 robustness NFRs with quantitative thresholds from `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §5 NFR matrix.]
**Agents and FMEA:** when a task touches a firmware/hardware/ML design decision, check whether it maps to one of the 36 FC-IDs; flag explicitly if it would close a "does-not-exist-today" control (burn-down progress).

### 8.4 Scalability
Reference scale (AgriSpectra): 50,000 field devices, 7-year field lifetime, seasonal deployment windows, LoRaWAN uplink constraints (physics-bounded downlink). Any agent-generated architecture/infrastructure design must be validated against these targets before delivery.
**Quantitative scalability targets:** consolidated in [[SCALABILITY_TARGETS|Scalability Targets]] — traceable to `EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §5.1 (SCALE-1…6 / S1…5 / PERF-1…3), which is authoritative. Key ceilings: 50,000 concurrent devices (SCALE-1); 50,000 MQTT connections (SCALE-2); 10,000 msgs/s MQTT throughput (SCALE-3); 500 req/s sustained + 2,000 req/s burst REST API (SCALE-4); 50,000 writes/s time-series DB (SCALE-5); 5,000 concurrent OTA downloads = 10% of fleet (SCALE-6); cloud API ≤ 200 ms P99 (PERF-3). Correlated-event surge thresholds bind FMEA FC-019 (telemetry storm ≥ 10× nominal for > 5 min) and FC-035 (post-outage thundering herd ≥ 50,000 devices within 30 min; mandatory jittered exponential backoff 1–120 s).

### 8.5 Incident Command
IC defined in `docs/operations/INCIDENT_COMMANDER.md`; not a permanent role (weekly rotation, owned by QA/Process Architect). **All 14 roles** must respond to IC direction within their §3.6 response SLA during a declared cross-layer incident (not optional). **Emergency tempo:** MACP permits temporary deviation from standard Propose→Confirm cadence with IC-tagged bus priority; any such deviation is documented retroactively as an ADR within **5 business days** of incident closure. All roles join the annual cross-layer incident drill (coordinated by QA/Process Architect). **Crash- vs. erosion-shaped (V3):** current machinery is "crash-shaped" (discrete failures), weaker on slow erosion (e.g. FC-022 drift). On incident/monitoring tasks, ask: crash-shaped or erosion-shaped detection? Erosion needs statistical drift alarms, longitudinal baselines, anomaly-detection sliding windows.

---

## 9. Quality & Standards

### 9.1 NFR Verification Matrix & Process Health
Architect owns the NFR Verification Matrix (`EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md` §5):

| Category | Key NFRs | Owner | Verification |
|---|---|---|---|
| Reliability | R1–R5: uptime, MTTF, MTTR, field lifetime, OTA reliability | ARCH | HIL soak testing, fleet telemetry |
| Robustness | FMEA-derived: detection coverage ≥ 95%, no unmonitored Tier-1 chain | ARCH + QA | Cross-layer robustness regression suite, FC-ID traceability |
| Scalability | Fleet size, throughput, API latency, OTA concurrency | ARCH + DEVOPS | Load testing, fleet simulation |
| Performance | Inference latency (ms), sampling frequency (Hz), OTA deployment time | FW + ML + QA | On-target benchmarking, HIL profiling |

Status: all targets instantiated, no `[TBD]` (post-V3). Detection coverage self-reports honestly at ≈ 53% vs. ≥ 95% — the primary remaining burn-down.
**Engineering Process Health Dashboard** (Process Architect/QA): defined in `QA_TEST_AUTOMATION_ENGINEER_SKILL.md` §3.7; aggregates SIRC `coverage_pct` trend per sprint, open FMEA chain burn-down (17 Critical → 0), contract reciprocity audit results (91 contracts), IRD gate pass/fail per pair, Tier-1 escalation frequency (→ 0), autonomous Tier 3–4 success rate (target ≥ 80%).
[NOT YET AVAILABLE — fill in manually: dashboard location (Grafana? Obsidian query? Prometheus?), metric definitions, and sprint cadence from `DEVOPS_PLATFORM_ENGINEER_SKILL.md` §8 or the metrics-pipeline docs.]

### 9.2 Referenced Standards
Authoritative per-domain standards lists live in each `*_SKILL.md` §8 and the relevant `docs/schemas/*.md`; consult those rather than duplicating here. Recurring cross-cutting standards: IEC 60812/61025, MISRA C:2012, CERT C, ARM CMSIS-NN, IEC 62443, ISO/IEC 27001, OWASP IoT Top 10, NIST SP 800-53/-160/-193/-161, IETF RFC 9334 (RATS), STRIDE, CWE/CVE/CVSS, ISO/IEC 25010, IEEE 829/29148/42010, SemVer, ISO 8000-8, ISO 31000.

### 9.3 Machine-Parseable Schema Registry
8 schemas in `docs/schemas/` (indexed by `SCHEMA_INDEX.md`). When an agent produces any of these, validate against the schema (required fields, allowed enums, cross-reference integrity).

Schemas (ID format → producer → key gate rule):
- **ADR** `ADR-NN`, any role — STRATEGIC ADRs need ARCH approval; BIA required for cost-material decisions.
- **CCR** `CCR-NN`, any pair — BLOCKING CCRs halt IRD gate until resolved.
- **DQIR** `DQIR-NN`, ML → DATA — CRITICAL/HIGH blocks MLOps training pipeline; 48h correction SLA for CRITICAL.
- **IRD** `IRD-NN`, any pair — PASS requires open CCRs = 0, all mandatory scenarios PASS, producer + consumer signatures.
- **OCM** `model.id + model.version`, MLOPS — `flash_budget_check.result = FAIL` blocks OTA dispatch.
- **SIRC** `SIRC-ROLE-SNN`, each security champion — any mandatory item FAILED blocks SEC review scheduling.
- **TTP** `TTP-NN`, RES — TRL ≥ 5 required for transfer; HIGH license risk → legal review.
- **BIA** `BIA-NN`, BIZ — STRATEGIC ADR with BIA recommendation=REJECT cannot be DECIDED without ARB override.

**Dependency chain:** see [[SCHEMA_INDEX|Schema Index]] (TTP → ADR → BIA; open CCRs block ADR decision; IRD requires empty CCRs + Contract Registry validation; DQIR blocks OCM and the training pipeline; SIRC gates SEC review, Architect sign-off when `risk_accepted = true`).

---

## 10. Project-Specific Rules

Rules emerging from the system as a whole; internalize before reading a role card.

- **10.1 Prime Directive — Never Ship Against Open Critical Chains** (§1 principle 4): never produce a rationale, recommendation, or deliverable arguing to ship around open Critical FMEA chains (RPN ≥ 200) with no mitigation — the correct response to "how do we get to production?" with 17 open Critical chains is to burn down the 9 missing detection controls, validate against the FC-IDs, and re-run the QA gate.
- **10.2 Contract-First Discipline** (§1 principle 1): no implementation work (code, firmware, model architecture, API design, IaC) until the interface contract is defined in the producing role's §6 and accepted (`final` or `Accepted` ADR) — if no contract authorizes the output, the first deliverable is the contract spec.
- **10.3 Honesty Over Polish.** Write the honest number even when it fails the gate (e.g. "≈ 53%" vs. a ≥ 95% gate is a correct, valuable artifact; "coverage meets target" when it does not is dangerous). Never round up, soften, or hedge unfavorable findings; name the gap and link the burn-down path.
- **10.4 Strategic-Role Exception.** PO, FE, RES, BIZ have approved deviations: §1 bold-heading paragraphs (not bullets), §4 no proficiency-legend blockquote, §6 no opening blockquote, §9 no section-opening blockquote, §9.2 checkboxes (not numbered), §9.3 no `Do NOT` prefix, §9.4 no Role/Goal/Inputs/Produce/Constraints template, §10 custom KPI categories. Do not "correct" these; audit each against its own internal consistency.
- **10.5 Audit Code Semantics.** Do not invent or misread codes: `#MR-N` = Milestone Reference (`#MR-10` = Security Design Review milestone, §3.2 shift-left gate); `#P4-M-N` = Phase 4 Milestone N (Phase 5 Transformation Roadmap). `#CR-N` [NOT YET AVAILABLE — confirm whether Contract Reference, Change Request, or other]; `#HR-N` [NOT YET AVAILABLE — confirm namespace; seen as `#HR-5` in DevOps]; `#B-N` [NOT YET AVAILABLE — confirm whether Backlog item reference]. Need a new cross-reference? Request a canonical code from PO; never invent one.
- **10.6 Process Architect.** QA serves two functions: primary QA + Process Architect (`QA_TEST_AUTOMATION_ENGINEER_SKILL.md` §3.7) — runs cross-role EPRs, maintains the Process Health Dashboard, coordinates the annual incident drill, captures org learning, owns the IC weekly rotation. Fractional function, not a separate hire: use QA authority + EPR coordination only, never ARCH or SEC authority.
- **10.7 Review History — Use With Care.** `docs/review_v1/` (Part 1 Org Audit; 37 findings, all remediated); `docs/review_v2/` (Part 2 Holistic Validation; conditional yes; hollow robustness gate); `docs/review_v3/REVIEW_V3_FINAL.md` (Part 3 Lifecycle Simulation; CONDITIONAL GO; 17 open Critical chains). Historical/analytical — they do not override SKILL.md. On conflict, the SKILL.md is authoritative — unless the review tagged the finding "to be incorporated" and the SKILL.md is not yet updated, in which case flag the discrepancy. `docs/OBSIDIAN_AUDIT_REPORT.md` is a point-in-time snapshot, not a live check.

---

## Appendix A: Quick Reference (top items — full lists in §7.6 and §10)

See §7.6

