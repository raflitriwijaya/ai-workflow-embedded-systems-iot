---
title: "ADR Index — Architecture Decision Record Registry"
version: "1.0.0"
date_created: "2026-06-23"
status: active
tags:
  - adr-index
  - embedded-iot
  - governance
  - machine-parseable
  - architecture
cssclass: adr-index
---

# ADR Index — Architecture Decision Record Registry

> **Append-only master registry** of all Architecture Decision Records (ADRs). This index closes the CLAUDE.md §6.1 gap (`ADR storage location`, `ADR numbering convention`). It is the human-navigable companion to the machine-parseable [[ADR_SCHEMA|ADR Schema]]; every row corresponds to one `docs/adr/adr-NNNN.md` file.
> **Owner:** [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] (owns the ADR repository and architecture governance per Skill §2). **Ratified by:** [[adr-0001|ADR-0001]].

---

## 1. Storage Location & Numbering Convention

- **Storage directory:** `docs/adr/` — one ADR per Markdown file.
- **File naming:** `adr-NNNN.md` — lowercase, zero-padded, sequential (e.g., `adr-0001.md`, `adr-0002.md`, …). The next ADR takes the lowest unused sequential number.
- **Internal ID:** `ADR-NNNN` — uppercase, 4-digit, matching the [[ADR_SCHEMA|ADR Schema]] validation `V-ADR-01` regex `^ADR-\d{4}$` (e.g., `ADR-0001`). The file `adr-0001.md` carries `id: "ADR-0001"`.
- **Naming exception (stated explicitly):** ADR **instance** files use lowercase `adr-NNNN.md`, an approved exception to the CLAUDE.md §3.1 SCREAMING_SNAKE_CASE primary-doc rule, consistent with the vault's lowercase convention for non-skill working/record files. The ADR **framework** documents themselves remain SCREAMING_SNAKE_CASE: `ADR_SCHEMA.md`, `ADR_INDEX.md`, `ADR_TEMPLATE.md`.
- **Template:** Author new ADRs from [[ADR_TEMPLATE|ADR Template]]; validate against [[ADR_SCHEMA|ADR Schema]] (rules V-ADR-01 … V-ADR-12) before merge.

## 2. Append-Only Discipline

- **Rows are appended, never reordered or deleted.** A new ADR is added as a new row at the end of the registry (§4).
- **The only permitted in-place edit to an existing row** is its `Status` cell, updated to reflect a status transition that is itself recorded inside the ADR file (ADRs are append-only and immutable once `DECIDED`; see [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §7). A change of decision is made by **superseding** with a new ADR, never by rewriting an existing one.
- ARB (Architecture Review Board) Decision Records that would normally require an ADR are cross-referenced here per the [[ARB_CHARTER_INSTANTIATED|ARB Charter]] §7.

## 3. Status Values & Terminology Reconciliation

The machine-parseable `status` enum (authoritative, from [[ADR_SCHEMA|ADR Schema]]) is: `PROPOSED` → `DECIDED` → (`DEPRECATED` | `SUPERSEDED` | `REJECTED`).

**Stated inconsistency (do not silently "correct"):** the prose lifecycle in [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect Skill]] §7 (`Proposed → Accepted → Superseded | Deprecated`) and CLAUDE.md §6.1 (`Proposed → Under Review → Accepted/Rejected/Superseded`) use **"Accepted"** as a synonym for the schema's **`DECIDED`**. This index and all ADR frontmatter use the schema enum (`DECIDED`) for machine-parseability; "Accepted" is the prose synonym.

## 4. ADR Registry

| ADR | Title | Status | Date | Author | Affected Contracts |
|---|---|---|---|---|---|
| [[adr-0001\|ADR-0001]] | Adoption of ARB Charter and ADR Process | DECIDED | 2026-06-23 | [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]] | None (governance process; no interface contract changed) |

<!-- APPEND NEW ADRs BELOW THIS LINE — one row per adr-NNNN.md, lowest unused sequential number. Never reorder or delete existing rows. -->

---

## 5. Related Governance Artifacts

- [[ADR_SCHEMA|ADR Schema]] — machine-parseable field definitions and validation rules (V-ADR-01 … V-ADR-12).
- [[ADR_TEMPLATE|ADR Template]] — copy-to-author skeleton matching the §7 fields and the schema.
- [[ARB_CHARTER_INSTANTIATED|ARB Charter (Instantiated)]] — the body that ratifies non-breaking and expanded-authority decisions; ARB Decision Records cross-reference into this index.
- [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Embedded Systems Architect]] §7 — ADR process and decision authority.

#adr-index #governance #architecture
