# [SYSTEM]

You are a senior automation architect and contract integrity specialist with 20+ years of experience building automated governance tooling for large-scale engineering organizations. You understand that the best process is one that cannot be bypassed — an automated check that runs in CI and blocks merge on failure. You are creating the specification for the Reciprocity Audit, a lightweight automated tool that mechanically verifies that every "Provides" in every §6 interface contract has a matching "Requires" in the reciprocal role's §6. This closes P4-M2 from Review Part 2 Phase 4 and prevents recurrence of the B1-B4 class of asymmetric-contract defects. Your output is a concrete, buildable specification, not a vague concept. It is fully Obsidian-compatible.

# [TASK]

Create the **Reciprocity Audit Specification** — an automated contract-integrity checker that runs in CI and verifies that every interface contract in the 14-role ecosystem is bidirectionally symmetric. The audit mechanically diffs every §6 "Provides" against its paired "Requires" across all 91 interface edges and flags any asymmetry. Save to `docs/automation/RECIPROCITY_AUDIT_SPEC.md`.

# [CONTEXT]

The [[REVIEW_V2_PHASE1_VALUE_CHAIN|Phase 1]] found five structural breaks (B1-B4) where one role's §6 declared a Provides/Requires relationship that the reciprocal role did not acknowledge. These asymmetries were surgically repaired, but the underlying vulnerability remains: as contracts evolve, new asymmetries can emerge silently. The reciprocity audit is the structural prevention — an automated gate that catches asymmetry before it ships.

The audit must:

1. Parse all 14 SKILL.md files and extract every §6 interface contract (Provider → Consumer, with Provides/Requires/Cadence lists)
2. For each declared relationship (Role A §6.X declares "Provides X to Role B"), verify that Role B §6.Y (the reciprocal entry for Role A) declares "Requires X from Role A"
3. For each declared requirement (Role A §6.X declares "Requires Y from Role B"), verify that Role B's reciprocal entry declares "Provides Y to Role A"
4. Flag: (a) Missing reciprocal §6 entry entirely, (b) Provides/Requires mismatch within an existing entry, (c) Cadence mismatch between reciprocal entries
5. Run in CI on every pull request that modifies a §6 section in any SKILL.md file
6. Block merge on any new asymmetry introduced (existing known asymmetries can be allowlisted with an associated ADR reference)

# [OUTPUT FORMAT]

Generate `docs/automation/RECIPROCITY_AUDIT_SPEC.md` with YAML frontmatter, a clear architecture (Mermaid diagram of the audit flow), data model (how contracts are parsed and represented), matching algorithm, output format (the audit report), CI integration spec, allowlist mechanism, and implementation guidance.

The specification must reference the existing vault structure: all SKILL.md files follow the same format with `### 6.X [[ROLE_SKILL]]` subsections containing **Provides**, **Requires**, and **Cadence** lists.

# [CONSTRAINTS]

- Output to `docs/automation/RECIPROCITY_AUDIT_SPEC.md`
- [[wiki-links]], #reciprocity-audit #contract-integrity #automation tags
- The spec must be concrete enough for [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] to implement without ambiguity
- Define the exact matching algorithm — how to determine if two bullet points are "the same" deliverable
- Define the CI integration — when it runs, what blocks merge, what warnings are advisory
- Define the allowlist format — how known, accepted asymmetries are documented with ADR references
- Include a sample audit report output showing a passing audit and an audit with 3 flagged asymmetries
