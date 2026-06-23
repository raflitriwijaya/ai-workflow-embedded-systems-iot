---
title: "ADR Template — Architecture Decision Record"
version: "1.0.0"
date_created: "2026-06-23"
tags:
  - adr-template
  - embedded-iot
  - governance
  - machine-parseable
  - architecture
cssclass: adr-template
---

# ADR Template — Architecture Decision Record

> **How to use:** Copy the two blocks below into a new file `docs/adr/adr-NNNN.md` (next unused sequential number; see [[ADR_INDEX|ADR Index]] §1). Fill every required field, validate against [[ADR_SCHEMA|ADR Schema]] (rules V-ADR-01 … V-ADR-12), then add a row to the [[ADR_INDEX|ADR Index]] §4 registry. This template reproduces both the machine-parseable schema frontmatter and the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §7 prose fields (Title, Status, Context, Decision, Consequences, Business Impact, Alternatives Considered, Related ADRs).

---

## Field Requirements (must pass before merge)

- `id` matches `^ADR-\d{4}$` (V-ADR-01); filename is the lowercase `adr-NNNN.md` form.
- `status` ∈ {`PROPOSED`, `DECIDED`, `DEPRECATED`, `SUPERSEDED`, `REJECTED`} (V-ADR-02). "Accepted" in §7 prose ≡ schema `DECIDED`.
- `decision_class` ∈ {`STRATEGIC`, `TACTICAL`, `LOCAL`} (V-ADR-03); `tier` is one of the 10 schema values (V-ADR-04).
- `options_considered` has **≥ 2 entries** (V-ADR-05); each has **≥ 1 pro and ≥ 1 con** (V-ADR-06).
- If `status = DECIDED`: `date_decided` is set and ≥ 1 approver has `approved: true` (V-ADR-07); `date_created ≤ date_decided` (V-ADR-11).
- If `decision_class = STRATEGIC`: at least one approver is `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` (V-ADR-09), and the decision is ratified by the [[ARB_CHARTER_INSTANTIATED|ARB]] (STRATEGIC requires ARB ratification).
- `context`, `problem_statement`, `decision`, `rationale`, `consequences` all meet minimum char counts (V-ADR-10).
- A Business Impact Assessment is required for cost-material decisions (V-ADR-12); authored by [[BUSINESS_CONSULTANT_SKILL|Business Consultant]], appended within 10 business days of Architect notification.
- Security-baseline ADRs are tagged `#security-impact` and require [[SECURITY_ENGINEER_SKILL|Security Engineer]] co-approval.

---

## Block 1 — Frontmatter (machine-parseable; copy into the new file)

```yaml
---
schema_version: "1.0.0"

id: "ADR-NNNN"                  # 4-digit, e.g. ADR-0002
title: "<imperative decision title, ≤120 chars>"
date_created: "YYYY-MM-DD"
date_decided: null             # set to ISO date when status = DECIDED
date_superseded: null          # set only when status = SUPERSEDED

status: PROPOSED               # PROPOSED | DECIDED | DEPRECATED | SUPERSEDED | REJECTED
decision_class: TACTICAL       # STRATEGIC | TACTICAL | LOCAL
tier: CROSS-CUTTING            # HARDWARE | FIRMWARE | EMBEDDED-SOFTWARE | EDGE-AI |
                               # CONNECTIVITY | CLOUD-BACKEND | DATA-PIPELINE | SECURITY |
                               # DEVOPS | CROSS-CUTTING

initiator:
  role: "[[ROLE_SKILL_FILE]]"  # Obsidian wikilink to the initiating role
  name: null                   # optional human name

approvers:                     # ≥1 with approved:true required for DECIDED
  - role: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"   # required for STRATEGIC
    name: null
    approved: false
    date: null

superseded_by: null            # ADR-NNNN when status = SUPERSEDED
supersedes: null               # ADR-NNNN when this replaces a prior ADR

# ── Content fields (machine-validated; the body in Block 2 mirrors these for humans) ──
context: >                      # ≥50 chars (V-ADR-10) — situation forcing the decision
  <…>
problem_statement: >           # ≥30 chars (V-ADR-10) — the specific question being resolved
  <…>
options_considered:            # ≥2 entries (V-ADR-05); each ≥1 pro and ≥1 con (V-ADR-06)
  - id: "A"
    description: "<≥20 chars>"
    pros: ["<…>"]
    cons: ["<…>"]
    security_implications: "<optional free text>"
  - id: "B"
    description: "<≥20 chars>"
    pros: ["<…>"]
    cons: ["<…>"]
decision: >                     # ≥50 chars (V-ADR-10) — which option is chosen and why
  <…>
rationale: >                    # ≥50 chars (V-ADR-10) — reasoning beyond the decision text
  <…>
consequences: >                 # ≥30 chars (V-ADR-10) — what changes; consumers notified
  <…>

affected_contracts: []         # list of { contract_id, impact_description }
affected_requirements: []      # e.g. REQ-SEC-042
linked_adrs: []                # related ADR IDs

business_impact_assessment: null   # populated by [[BUSINESS_CONSULTANT_SKILL]] when #business-impact

tags:
  - architecture
  - adr-proposed              # transition to adr-decided / adr-superseded with status
---
```

## Block 2 — Body (§7 prose fields; human-readable rendering of the Block 1 content fields)

> The Block 1 frontmatter is the machine-parseable source of truth for validation; this body mirrors the same `context`, `options_considered`, `decision`, `rationale`, and `consequences` for human readers (see [[adr-0001|ADR-0001]] for a worked example).

```markdown
# ADR-NNNN — <imperative decision title>

## Status
PROPOSED  <!-- DECIDED | DEPRECATED | SUPERSEDED | REJECTED; mirror the frontmatter -->

## Context
<≥50 chars: the situation forcing the decision — constraints, triggering event, scope.>

## Problem Statement
<≥30 chars: the specific question being resolved.>

## Alternatives Considered
<≥2 options. For each: description (≥20 chars), Pros (≥1), Cons (≥1),
security implications (if any), estimated effort (days, optional).>

### Option A — <name>
- **Description:** …
- **Pros:** …
- **Cons:** …

### Option B — <name>
- **Description:** …
- **Pros:** …
- **Cons:** …

## Decision
<≥50 chars: which option is chosen and why.>

## Rationale
<≥50 chars: reasoning beyond the decision text — standards, trade study, precedent.>

## Consequences
<≥30 chars: what changes as a result; which consumers must act and are notified.>

## Business Impact  <!-- include only when tagged #business-impact -->
<Cost (one-time NRE, per-unit BOM delta, annual cloud OpEx delta), Schedule (market-window shift),
Market (positioning/commitment/pricing), Recommendation (Proceed / Proceed with Mitigation / Escalate).
Authored by the Business Consultant.>

## Related ADRs / Links
<linked ADRs, superseded/superseding IDs, affected contracts, SAD references.>
```

---

## Notes

- **Append-only:** once `DECIDED`, an ADR file is immutable except for a status transition; change a decision by creating a **superseding** ADR and updating both files' status fields.
- **Registry:** every new ADR must be appended to [[ADR_INDEX|ADR Index]] §4.
- **ARB cross-reference:** decisions made by the [[ARB_CHARTER_INSTANTIATED|ARB]] under delegated authority use the ARB Decision Record format and are cross-referenced from the ADR Index when they would otherwise require an ADR.

#adr-template #governance #architecture
