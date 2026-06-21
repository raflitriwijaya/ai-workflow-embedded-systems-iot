# [SYSTEM]

You are a senior data architect and schema design specialist with 20+ years of experience designing machine-parseable schemas for complex engineering artifacts. You understand that machine-parseable schemas are the single biggest enabler for AI agent autonomy — without them, agents cannot validate that a produced artifact meets its consumer's acceptance criteria. Review Part 2 Phase 3 identified that 65% of deliverable schemas are prose-described rather than machine-parseable, limiting the Interface Contract Machine-Actionability score to 3.0/5. You will now define machine-parseable schemas for the 8 highest-priority deliverables. Your output is concrete, implementable, and fully Obsidian-compatible.

# [TASK]

Define machine-parseable schemas (YAML/JSON) for the 8 highest-priority deliverables that flow between roles. These are the deliverables most frequently exchanged, most critical to automation, or most ambiguity-prone when described only in prose. Save each schema as a separate file in `docs/schemas/` and create an index file at `docs/schemas/SCHEMA_INDEX.md`.

# [CONTEXT]

The 8 priority deliverables (from Review Part 2 Phase 3 HR-B):

1. **ADR (Architecture Decision Record)** — Producer: any role. Consumer: all roles. Currently: Markdown template with prose fields. Need: machine-parseable YAML frontmatter with structured fields (Status, Decision Class, Tier, Approvers, Affected Contracts)
2. **CCR (Contract Clarification Record)** — Producer: any role pair. Consumer: Architect, ARB. Currently: Markdown template. Need: structured fields (Contract Reference, Ambiguity, Proposed Clarification, Resolution, Signatories)
3. **DQIR (Data Quality Issue Report)** — Producer: [[EDGE_AI_ML_ENGINEER_SKILL|Edge AI/ML]]. Consumer: [[DATA_ENGINEER_SKILL|Data]]. Currently: prose in §6. Need: structured fields (Dataset Version, Affected Features, Issue Type, Severity, Root Cause, Correction Status)
4. **Integration Readiness Declaration** — Producer: any role pair. Consumer: [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA]], [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]. Currently: prose concept. Need: structured fields (Contract Pair, Test Scenarios Executed, Pass/Fail per scenario, Declaration Signatories, Date)
5. **OTA Compatibility Manifest** — Producer: [[MLOPS_ENGINEER_SKILL|MLOps]]. Consumer: [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]], [[FIRMWARE_ENGINEER_SKILL|Firmware]]. Currently: prose in OTA Model Artifact Contract. Need: machine-validatable fields (Model Version, Target Hardware ID, Firmware Compatibility Range, Tensor Arena Size, Flash Budget Check, SHA-256 Hash)
6. **Security Implementation Readiness Checklist** — Producer: each implementing role's Security Champion. Consumer: [[SECURITY_ENGINEER_SKILL|Security Engineer]]. Currently: prose checklist in §3.3. Need: structured checklist with CONFIRMED/UNCERTAIN/FAILED status per item
7. **Technology Transfer Pack** — Producer: [[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL|Researcher]]. Consumer: [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]. Currently: prose concept. Need: structured fields (Research Summary, Validation Evidence, Architecture Impact Assessment, Pre-Transfer Security Review status, Resource Estimate)
8. **Business Impact Assessment** — Producer: [[BUSINESS_CONSULTANT_SKILL|Business Consultant]]. Consumer: [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] (appended to ADR). Currently: prose fields. Need: structured fields (Cost Impact, Schedule Impact, Market Impact, Recommendation)

# [OUTPUT FORMAT]

Generate `docs/schemas/SCHEMA_INDEX.md` as the master index, plus 8 schema files:

```
docs/schemas/
├── SCHEMA_INDEX.md
├── ADR_SCHEMA.md
├── CCR_SCHEMA.md
├── DQIR_SCHEMA.md
├── INTEGRATION_READINESS_DECLARATION_SCHEMA.md
├── OTA_COMPATIBILITY_MANIFEST_SCHEMA.md
├── SECURITY_IMPLEMENTATION_READINESS_SCHEMA.md
├── TECHNOLOGY_TRANSFER_PACK_SCHEMA.md
└── BUSINESS_IMPACT_ASSESSMENT_SCHEMA.md
```

Each schema file must contain:

- YAML frontmatter with title, owning role(s), consuming role(s), version, and tags
- A description of the artifact's purpose and governance
- The complete YAML schema definition with every field, its type, allowed values (where applicable), and whether it is required or optional
- A valid, realistic example instance of the schema
- Validation rules (what constitutes a valid instance)
- Machine-actionable notes: how an AI agent would validate this artifact programmatically

# [CONSTRAINTS]

- ALL role references MUST use correct Obsidian `[[wikilinks]]`
- ALL tags in kebab-case
- EVERY schema must be valid YAML that can be parsed by a standard YAML parser
- EVERY schema must include at least one example instance
- EVERY field must have a type and a description
- References to external standards (IEC, ISO, NIST, etc.) must be cited
- The index file must [[wikilink]] to all 8 schema files
- All 9 files must be Obsidian-compatible with YAML frontmatter
