---
title: "Obsidian Compatibility Audit Report"
date: 2026-06-20
status: final
tags:
  - audit
  - obsidian
  - vault-health
  - final
cssclass: audit-report
---

# Obsidian Compatibility Audit Report

> **Generated:** 2026-06-20
> **Scope:** All .md files in vault (21 files, excluding this report)
> **Dimensions Audited:** 6

---

## 1. Executive Summary

This audit scanned **21 Markdown files** in the vault — 14 `*_SKILL.md` role definitions, 1 workflow document ([[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM|Workflow Team doc]]), 5 review/phase documents under [docs/review_phase1/](review_phase1/), and 1 meta/prompt scratch file (`prompt_obsidian.md`). Across these files, **960 wikilink occurrences** and **1,276 tag occurrences** (157 unique tags) were inspected, along with every YAML frontmatter block, heading, and `§` cross-reference.

**The vault's link integrity and structural consistency are excellent.** Of 960 wikilink occurrences, **953 resolve to a real file** and only **1 is a genuinely broken rendered link** (an illustrative `[[wikilinks]]` placeholder in [[REVIEW_SKILL_REPORT]]). Section numbering is clean across all 15 content files (no gaps, no duplicates), there are **zero duplicate headings**, and the 14 skill files form a dense, well-connected graph (9–17 inbound links each — no fragile single-link nodes). No file is tag-less.

**However, three systematic, easily-remediated issues drag down the formal health score.** (1) **Unescaped pipes in table-cell wikilinks** — 38 wikilinks across 5 skill files use `[[Note|alias]]` inside Markdown tables where Obsidian requires `[[Note\|alias]]`; these break table rendering and, tellingly, sit alongside *correctly escaped* links in the very same tables (e.g. line 242 of [[QA_TEST_AUTOMATION_ENGINEER_SKILL]]). This is the single most user-visible defect and is **not** captured by the prescribed scoring rubric, so it is surfaced here and ranked Priority 1. (2) **16 of 21 files lack YAML frontmatter** — all 14 skill files plus the workflow doc and the prompt file — meaning no Dataview/Properties metadata. (3) **7 files are graph orphans** (zero inbound links), including the workflow hub and all 5 review documents.

**Top 3 recommended fixes:** (1) Escape all 38 table-cell wikilink pipes (`|` → `\|`) in the 5 skill files listed in §6.4. (2) Add standard frontmatter (`title`, `date`, `tags`, `status`) to the 14 skill files and the workflow doc (§5.1). (3) Create a vault index / Map-of-Content note that links the workflow doc and the 5 review files, and have [[REVIEW_SKILL_REPORT]] link its 4 phase sub-reports, eliminating all 7 orphans (§3.1).

---

## 2. Broken Wikilinks

**Methodology:** Scanned every `[[wikilink]]` in every .md file (resolving `|alias` and `\|alias` separators and `#section` anchors), verified the target basename exists in the vault, and tracked whether each link sits inside inline code or a fenced code block (Obsidian does **not** render wikilinks inside code, so those are illustrative, not active links).

### 2.1 Critical (Target File Does Not Exist)

| Source File | Line | Broken Link | Suggested Fix |
|---|---|---|---|
| docs/review_phase1/REVIEW_SKILL_REPORT.md | 614 | `[[wikilinks]]` | This is descriptive prose ("All 14 role references are `[[wikilinks]]`"), not a real link. Remove the brackets → write the word **wikilinks** in plain text or inline code: `` `wikilinks` ``. |

> **Note:** `prompt_obsidian.md` also contains the strings `[[wikilink]]` (lines 2, 50, 66, 154), `[[QA_TEST_ENGINEER_SKILL]]` (line 15), and `[[PRODUCT_OWNER_TPM_SKILL]]` (line 16), but **every one is inside inline-code backticks or a fenced code block**, so Obsidian renders them as literal text, not links. They are illustrative content of the audit prompt itself and are listed under §6.3, not counted as broken rendered links. If `prompt_obsidian.md` is a transient scratch file, consider moving it out of the vault.

### 2.2 Warning (Target Exists But Filename Mismatch — Wrong Case/Typo)

| Source File | Line | Current Link | Correct Link |
|---|---|---|---|
| *(none — no rendered wikilink in vault content points to a wrong-case or deprecated filename)* | — | — | — |

The two historically-deprecated filenames (`QA_TEST_ENGINEER_SKILL`, `PRODUCT_OWNER_TPM_SKILL`) appear **only** inside inline code in `prompt_obsidian.md` (illustrative) and once in prose in `REVIEW_PHASE3_QUALITY.md` (not a link). See §6.3 and §7.2 for those residual references and their fixes.

### 2.3 Summary

- **Total wikilinks scanned:** 960
- **Resolve to an existing file (healthy):** 953
- **Broken (no target):** 1 rendered link ([[REVIEW_SKILL_REPORT]]:614) + 6 illustrative placeholders in `prompt_obsidian.md` that are inside code and **not rendered as links**
- **Filename mismatch (rendered):** 0
- **Deprecated-name targets (all inside inline code, non-rendered):** 2 (`QA_TEST_ENGINEER_SKILL`, `PRODUCT_OWNER_TPM_SKILL`)

> A separate, higher-impact wikilink-rendering issue (38 unescaped pipes inside tables) is documented in **§6.4** — those links *resolve* to real files but break table layout.

---

## 3. Orphan Files

**Methodology:** Counted inbound `[[wikilinks]]` (from other files, excluding self-links and this report) for every .md file.

### 3.1 Files with Zero Inbound Links

| File | Notes |
|---|---|
| EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | Workflow **hub** — links out to all 14 roles but nothing links back. **Fix:** add a `[[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM\|Team Overview]]` backlink in each skill's "Role Identity" or footer, or from a vault index note. |
| docs/review_phase1/REVIEW_SKILL_REPORT.md | Final merged report. **Fix:** link it from a vault index/MOC and from each phase doc (`See [[REVIEW_SKILL_REPORT]]`). |
| docs/review_phase1/REVIEW_PHASE1_ROLES.md | Phase sub-report. **Fix:** add a link to it from [[REVIEW_SKILL_REPORT]] (e.g. a "Source Phases" section listing `[[REVIEW_PHASE1_ROLES]]`). |
| docs/review_phase1/REVIEW_PHASE2_INTERFACE.md | Phase sub-report. **Fix:** link from [[REVIEW_SKILL_REPORT]] as `[[REVIEW_PHASE2_INTERFACE]]`. |
| docs/review_phase1/REVIEW_PHASE3_QUALITY.md | Phase sub-report. **Fix:** link from [[REVIEW_SKILL_REPORT]] as `[[REVIEW_PHASE3_QUALITY]]`. |
| docs/review_phase1/REVIEW_PHASE4_WORKFLOW.md | Phase sub-report. **Fix:** link from [[REVIEW_SKILL_REPORT]] as `[[REVIEW_PHASE4_WORKFLOW]]`. |
| prompt_obsidian.md | Meta/prompt scratch file. **Fix:** move out of the vault, or link from an index and add frontmatter if it is to be retained. |

> Once **this** report (`docs/OBSIDIAN_AUDIT_REPORT.md`) is saved, it adds an inbound link to [[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM]] and [[REVIEW_SKILL_REPORT]] (referenced above), partially de-orphaning them — but the 5 review/phase docs and `prompt_obsidian.md` still need the explicit backlinks above.

### 3.2 Files with Only 1 Inbound Link (Fragile)

| File | Inbound From |
|---|---|
| *(none)* | — |

**No fragile files.** All 14 skill files have a healthy inbound-link count (minimum 9, maximum 17), confirming a robust cross-reference graph:

| Skill File | Inbound | Skill File | Inbound |
|---|---|---|---|
| IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL | 17 | FIRMWARE_ENGINEER_SKILL | 13 |
| SECURITY_ENGINEER_SKILL | 16 | MLOPS_ENGINEER_SKILL | 13 |
| BUSINESS_CONSULTANT_SKILL | 15 | BACKEND_CLOUD_ENGINEER_SKILL | 12 |
| DEVOPS_PLATFORM_ENGINEER_SKILL | 15 | FRONTEND_DASHBOARD_ENGINEER_SKILL | 10 |
| PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL | 15 | HARDWARE_ENGINEER_SKILL | 10 |
| QA_TEST_AUTOMATION_ENGINEER_SKILL | 14 | EDGE_AI_ML_ENGINEER_SKILL | 9 |
| DATA_ENGINEER_SKILL | 13 | EMBEDDED_SYSTEMS_ARCHITECT_SKILL | 13 |

---

## 4. Tag Audit

**Methodology:** Extracted all `#tags` from all files (excluding tags inside fenced code blocks and YAML frontmatter list items), counted occurrences, and flagged single-use tags, case/concept collisions, and tag-less files.

- **Total tag occurrences:** 1,276
- **Unique tags:** 157
- **Single-use tags:** 49

### 4.1 Tags Used Only Once (Possible Typos or Orphans)

Most of these are **intentional, domain-specific** tags (e.g. `#WCAG`, `#STRIDE`, `#FMEA`-adjacent), not defects. The ones that are genuine hygiene problems (case/concept duplicates) are called out in §4.2 and are the only single-use tags penalized in §9.

| Tag | File | Line |
|---|---|---|
| `#ADR-appendix` | BUSINESS_CONSULTANT_SKILL.md | 280 |
| `#ARB` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 363 |
| `#ARB-decision` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 360 |
| `#Architecture-Review-Board` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 363 |
| `#Deputy-Architect` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 33 |
| `#Deputy-Security-Engineer` | SECURITY_ENGINEER_SKILL.md | 13 |
| `#ML-feasibility` | EDGE_AI_ML_ENGINEER_SKILL.md | 279 |
| `#ML-research-transfer` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 464 |
| `#MR-4` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 213 |
| `#MR-5` | BUSINESS_CONSULTANT_SKILL.md | 46 |
| `#MR-8` | EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | 623 |
| `#North-Star-KPI` | BUSINESS_CONSULTANT_SKILL.md | 747 |
| `#OTA-artifact-format` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 195 |
| `#OTA-governance` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 51 |
| `#OTA-validation` | QA_TEST_AUTOMATION_ENGINEER_SKILL.md | 79 |
| `#Research-to-Planning-Gate` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 213 |
| `#SLA` | BUSINESS_CONSULTANT_SKILL.md | 280 |
| `#STRIDE` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 141 |
| `#WCAG` | FRONTEND_DASHBOARD_ENGINEER_SKILL.md | 439 |
| `#accessibility` | FRONTEND_DASHBOARD_ENGINEER_SKILL.md | 439 |
| `#bus-factor` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 33 |
| `#business-metrics` | BUSINESS_CONSULTANT_SKILL.md | 747 |
| `#continuous-security` | DEVOPS_PLATFORM_ENGINEER_SKILL.md | 70 |
| `#cross-layer-failure` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 374 |
| `#data-archival` | DATA_ENGINEER_SKILL.md | 319 |
| `#distributed-governance` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 363 |
| `#final-verdict` | docs/review_phase1/REVIEW_SKILL_REPORT.md | 916 |
| `#firmware-feasibility` | FIRMWARE_ENGINEER_SKILL.md | 322 |
| `#frontend-kpi` | FRONTEND_DASHBOARD_ENGINEER_SKILL.md | 448 |
| `#gate-governance` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 213 |
| `#hardware-feasibility` | HARDWARE_ENGINEER_SKILL.md | 300 |
| `#interface-consolidation` | BUSINESS_CONSULTANT_SKILL.md | 46 |
| `#organizational-resilience` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 102 |
| `#product-alignment` | PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md | 327 |
| `#prompt-template` | FRONTEND_DASHBOARD_ENGINEER_SKILL.md | 439 |
| `#reconnection-metric` | FRONTEND_DASHBOARD_ENGINEER_SKILL.md | 448 |
| `#regulatory-compliance` | SECURITY_ENGINEER_SKILL.md | 79 |
| `#research-alignment` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 393 |
| `#research-data` | IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | 487 |
| `#resilience` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 33 |
| `#security-business` | BUSINESS_CONSULTANT_SKILL.md | 376 |
| `#security-impact` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 24 |
| `#security-implementation-start` | SECURITY_ENGINEER_SKILL.md | 69 |
| `#security-review` | SECURITY_ENGINEER_SKILL.md | 291 |
| `#single-source-of-truth` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 195 |
| `#succession-exercise` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 102 |
| `#tag` | prompt_obsidian.md | 2 |
| `#technology-transfer` | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 294 |
| `#workflow-diagram` | EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | 623 |

> `#tag` (prompt_obsidian.md:2) is a false tag — it is the literal word "`#tag`" inside inline code in the audit prompt. It will be cleaned up when `prompt_obsidian.md` is removed or its backticks are recognized; no action needed in vault content.

### 4.2 Tag Inconsistencies (Same Concept, Different Tags)

| Tag 1 | Tag 2 (and 3) | Suggested Canonical Tag |
|---|---|---|
| `#technology-transfer` (ARCH:294) | `#Technology-Transfer` (used 3×) | **`#technology-transfer`** — these are a **case-insensitive collision**: Obsidian treats them as the same tag in search/graph but displays both spellings, causing visible inconsistency. Pick lowercase and rewrite the 3 PascalCase occurrences. |
| `#ARB` (ARCH:363) | `#ARB-decision` (ARCH:360), `#Architecture-Review-Board` (ARCH:363) | **`#ARB`** — three single-use tags for the one "Architecture Review Board" concept. Consolidate to `#ARB` (keep `#ARB-decision` only if a distinct "decision" facet is genuinely needed). |
| `#WCAG` (FRONTEND:439) | `#accessibility` (FRONTEND:439) | Keep both, but they co-occur on one line; treat `#accessibility` as the umbrella and `#WCAG` as the specific standard. No rename required — listed for awareness. |
| `#OTA-governance`, `#OTA-validation`, `#OTA-artifact-format`, `#OTA-Model-Artifact-Contract`, `#model-OTA`, `#end-to-end-OTA`, `#OTA-monitoring` | — | OTA tag family with **mixed casing** (`OTA-` PascalCase prefix vs lowercase facets). Standardize the prefix casing (e.g. `#ota-governance`, `#ota-validation`, …) for consistent filtering. These denote distinct facets, so do **not** merge — only normalize case. |

**Casing convention (vault-wide):** 52 of 157 tags contain uppercase. Acronym tags (`#FMEA`, `#FTA`, `#NFR`, `#RPN`, `#STRIDE`, `#WCAG`, `#SLA`, `#DQIR`, `#PII-masking`) and ID tags (`#HR-1`, `#MR-1`, `#CR-3`, …) are acceptable, but multi-word PascalCase tags (`#Deputy-Architect`, `#Architecture-Review-Board`, `#Process-Architect`, `#Security-Champion`, `#System-Robustness-Contract`, `#Research-to-Planning-Gate`, `#North-Star-KPI`) break the otherwise-dominant kebab-case convention. **Fix:** adopt lowercase-kebab-case for multi-word concept tags; reserve uppercase for established acronyms only.

### 4.3 Most Used Tags (Top 20)

| Tag | Count | Tag | Count |
|---|---|---|---|
| `#recommendation` | 226 | `#research-interface` | 17 |
| `#risk` | 126 | `#HR-1` | 17 |
| `#strength` | 120 | `#single-point-of-failure` | 15 |
| `#gap` | 71 | `#lifecycle-gap` | 14 |
| `#cadence` | 34 | `#FMEA` | 13 |
| `#interface-contract` | 28 | `#integration-testing` | 11 |
| `#shift-left` | 25 | `#HR-5` | 11 |
| `#systemic-risk` | 22 | `#Process-Architect` | 11 |
| `#synchronization` | 21 | `#MR-1` | 11 |
| `#quality-attribute` | 19 | `#workflow-gap` | 11 |

> The top four tags (`#recommendation`, `#risk`, `#strength`, `#gap`) originate overwhelmingly from the review/phase documents and reflect a deliberate review-annotation taxonomy — healthy, not anomalous.

### 4.4 Files With No Tags

**None.** All 21 files contain at least one tag.

---

## 5. Frontmatter Audit

**Methodology:** Checked every .md file for a YAML block delimited by `---` on the very first line.

### 5.1 Files Missing Frontmatter

| File | Recommendation |
|---|---|
| EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | Add `title`, `date`, `status`, `tags`, `cssclass: skill-card` (or similar). |
| FIRMWARE_ENGINEER_SKILL.md | Same standard skill-card frontmatter. |
| HARDWARE_ENGINEER_SKILL.md | Same. |
| EDGE_AI_ML_ENGINEER_SKILL.md | Same. |
| MLOPS_ENGINEER_SKILL.md | Same. |
| DATA_ENGINEER_SKILL.md | Same. |
| DEVOPS_PLATFORM_ENGINEER_SKILL.md | Same. |
| BACKEND_CLOUD_ENGINEER_SKILL.md | Same. |
| FRONTEND_DASHBOARD_ENGINEER_SKILL.md | Same. |
| QA_TEST_AUTOMATION_ENGINEER_SKILL.md | Same. |
| SECURITY_ENGINEER_SKILL.md | Same. |
| PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL.md | Same. |
| BUSINESS_CONSULTANT_SKILL.md | Same. (Note: line 2 has a `---` horizontal rule **after** the H1 — this is *not* frontmatter; frontmatter must be the first line.) |
| IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL.md | Same. |
| EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | Add `title`, `date`, `tags`, `cssclass: workflow-doc`. |
| prompt_obsidian.md | Add frontmatter **or** move out of the vault (it is a meta/prompt scratch file). |

**Suggested skill-card frontmatter template** (apply to all 14 skill files):

```yaml
---
title: "Embedded Systems Architect — Skill Card"
role: Embedded Systems Architect
date: 2026-06-20
status: final
tags:
  - skill-card
  - embedded-iot
  - architecture
cssclass: skill-card
---
```

### 5.2 Files With Frontmatter But Missing Key Fields (title, date, tags)

| File | Missing Fields |
|---|---|
| *(none)* | — |

All 5 review/phase documents have complete frontmatter (`title`, `date`, `status`, `tags`, `cssclass`).

### 5.3 Frontmatter Consistency Issues

- **Stale `status` on superseded phase docs:** The 4 phase documents ([[REVIEW_PHASE1_ROLES]], [[REVIEW_PHASE2_INTERFACE]], [[REVIEW_PHASE3_QUALITY]], [[REVIEW_PHASE4_WORKFLOW]]) carry `status: draft`, while the merged [[REVIEW_SKILL_REPORT]] is `status: final`. Since the merged report supersedes them, set the phase docs to `status: superseded` (or `final`) to avoid implying unfinished work. **Fix:** update the `status` field in the 4 phase docs.
- **Otherwise consistent:** The 5 review docs use an identical field set and ordering (`title` → `date` → `status` → `tags` → `cssclass`) and a shared `cssclass: review-report`. Adopt this same ordering for the new skill-card frontmatter so the whole vault is uniform.

---

## 6. Wikilink Best Practices

### 6.1 Wikilinks Without Display Aliases (Where Recommended)

710 of 960 wikilink occurrences are bare (`[[FILENAME]]` with no `|alias`). Bare links are valid Obsidian, but in rendered prose they display the full `SCREAMING_SNAKE_CASE` filename, which is hard to read. The skill files already follow good practice (aliases like `[[FIRMWARE_ENGINEER_SKILL|FW]]`); the **review/phase documents** are where bare links cluster.

| File | Line | Wikilink | Suggestion to add `|alias` |
|---|---|---|---|
| docs/review_phase1/REVIEW_SKILL_REPORT.md | 843 | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]]` |
| docs/review_phase1/REVIEW_SKILL_REPORT.md | 844 | `[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL]]` | `[[IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL\|Researcher]]` |
| docs/review_phase1/REVIEW_SKILL_REPORT.md | 847 | `[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL]]` | `[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL\|PO/TPM]]` |
| docs/review_phase1/REVIEW_PHASE3_QUALITY.md | 150 | `[[BUSINESS_CONSULTANT_SKILL]]` | `[[BUSINESS_CONSULTANT_SKILL\|Business Consultant]]` |

> Representative sample only — the same bare-link pattern recurs throughout the 5 review documents. **Severity: Low** (cosmetic, not broken). **Bulk fix:** in the review docs, replace bare role links with aliased forms (and remember to **escape the pipe** when the link is inside a table cell — see §6.4).

### 6.2 Self-Referencing Wikilinks

A file that wikilinks to itself is valid but redundant (it does not aid navigation and creates a self-loop in the graph). 12 occurrences found, all from a role being listed among co-signers/owners and the author linking *every* role including its own:

| File | Line | Wikilink |
|---|---|---|
| EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 210, 211, 212, 213, 214 | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]]` (NFR table "Sign-off Authority" column) |
| EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 216, 300 | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]]` |
| FIRMWARE_ENGINEER_SKILL.md | 256, 310 | `[[FIRMWARE_ENGINEER_SKILL\|FW]]` |
| HARDWARE_ENGINEER_SKILL.md | 255, 264 | `[[HARDWARE_ENGINEER_SKILL\|HW]]` |
| DATA_ENGINEER_SKILL.md | 253 | `[[DATA_ENGINEER_SKILL\|DATA]]` |

**Fix:** replace each self-link with **bold plain text** of the alias (e.g. `**Architect**` instead of `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]`) when the role is referring to itself. This keeps the visual emphasis without a useless self-loop.

### 6.3 Wikilinks With Deprecated Filenames

| File | Line | Deprecated Link | Current Filename |
|---|---|---|---|
| prompt_obsidian.md | 15 | `[[QA_TEST_ENGINEER_SKILL]]` *(inside inline code — illustrative)* | `QA_TEST_AUTOMATION_ENGINEER_SKILL` |
| prompt_obsidian.md | 16 | `[[PRODUCT_OWNER_TPM_SKILL]]` *(inside inline code — illustrative)* | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL` |
| docs/review_phase1/REVIEW_PHASE3_QUALITY.md | 150 | `PRODUCT_OWNER_TPM_SKILL` *(plain prose, not a link)* | `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL` |

**Fixes:** The two `prompt_obsidian.md` entries are illustrative examples *of* the deprecation inside the audit prompt — leave them if the file documents the prompt, or remove the file. The [[REVIEW_PHASE3_QUALITY]]:150 occurrence is a genuine **residual stale reference** in prose ("PRODUCT_OWNER_TPM_SKILL does not list…") — rewrite it to the current name `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL`.

### 6.4 Unescaped Pipes in Table-Cell Wikilinks ⚠️ (Highest-Impact Rendering Defect)

**This is the most user-visible Obsidian-compatibility problem in the vault.** Inside a Markdown table cell, the alias pipe of a wikilink **must** be escaped as `\|`, otherwise Obsidian's table parser reads the `|` as a column separator, splitting the cell and misaligning the row. The vault is **internally inconsistent**: some table-cell links are correctly escaped (`[[Note\|alias]]`) while others on the *same rows/tables* are not (`[[Note|alias]]`). **38 unescaped occurrences** were found:

| File | Line(s) | # Links | Fix |
|---|---|---|---|
| EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 195, 201 | 17 | Change each `[[…\|alias]]` → `[[…\\\|alias]]` (escape the pipe). |
| DATA_ENGINEER_SKILL.md | 221, 222 | 10 | Escape pipes in all table-cell wikilinks. |
| SECURITY_ENGINEER_SKILL.md | 221 | 7 | Escape pipes in all table-cell wikilinks. |
| MLOPS_ENGINEER_SKILL.md | 205 | 3 | Escape pipes in all table-cell wikilinks. |
| QA_TEST_AUTOMATION_ENGINEER_SKILL.md | 242 | 1 | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL\|Architect]]` in the description cell is unescaped while the 7 sign-off links on the same line are correctly escaped — escape this one too. |

> **Smoking gun:** [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] line 242 contains **both** an unescaped link (`[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]]`, description cell) **and** seven correctly-escaped links (`[[…\|…]]`, sign-off cell) in a single table row — proving the escaping was applied inconsistently rather than intentionally omitted. **Fix action:** run a find/replace within table regions: `\]\]` aliases using `|` → `\|`. Verify in Obsidian Reading view that each affected table renders with aligned columns.

---

## 7. Cross-File Consistency Checks

### 7.1 § Section Numbering Gaps or Duplicates

**None.** Every content file uses clean, sequential numbering:

- All 14 skill files: `## 1.`, `## 2.`, … with consistent `### N.M` subsections; no missing or duplicate numbers detected.
- [[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM]]: sections `## 1.`–`## 14.`, each with `.1 Job Description` / `.2 Required Skills` / `.3 Collaboration Interfaces` — fully sequential.
- The 5 review documents: numbering is internally sequential.

### 7.2 Files Referencing Old Subsection Numbers After Renumbering

**No broken internal `§` cross-references in vault content.** Notes on apparent matches:

- **CCPA/CPRA legal citations are false positives:** `§1798.105` and `§1798.140` in [[DATA_ENGINEER_SKILL]] (lines 221, 309, 311) and [[SECURITY_ENGINEER_SKILL]] (lines 221, 295, 297) are references to **California Civil Code** sections, not internal document sections. No fix needed.
- **Review-doc `§6.x` references are forward-looking, not broken:** In [[REVIEW_SKILL_REPORT]] (lines 844–887) entries like "Add §6.9 entry in RES SKILL.md" are *recommended new subsections* to be created in the target skill files — action items, not links to existing headings. They correctly refer to each skill's "Interface Contracts" (§6) section. No fix needed.
- **One genuine residual:** [[REVIEW_PHASE3_QUALITY]]:150 refers to "`PRODUCT_OWNER_TPM_SKILL` §6.1" using the **deprecated filename**. **Fix:** rename to `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL` (also tracked in §6.3).

### 7.3 Duplicate Headings Within Same File

| File | Heading Text | Lines |
|---|---|---|
| *(none)* | — | — |

**No duplicate headings** were found in any of the 21 files — every heading within each file is unique, so Obsidian heading-anchor links (`[[File#Heading]]`) are unambiguous.

---

## 8. Prioritized Fix List

| Priority | File | Line | Issue Type | Description | Fix Action |
|---|---|---|---|---|---|
| **1 (Critical)** | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 195, 201 | Table render break | 17 unescaped pipes in table-cell wikilinks | Escape `|` → `\|` in all table-cell `[[…\|alias]]` links |
| **1 (Critical)** | DATA_ENGINEER_SKILL.md | 221, 222 | Table render break | 10 unescaped pipes in table-cell wikilinks | Escape `|` → `\|` |
| **1 (Critical)** | SECURITY_ENGINEER_SKILL.md | 221 | Table render break | 7 unescaped pipes in table-cell wikilinks | Escape `|` → `\|` |
| **1 (Critical)** | MLOPS_ENGINEER_SKILL.md | 205 | Table render break | 3 unescaped pipes in table-cell wikilinks | Escape `|` → `\|` |
| **1 (Critical)** | QA_TEST_AUTOMATION_ENGINEER_SKILL.md | 242 | Table render break | 1 unescaped pipe mixed with 7 escaped on same row | Escape the lone `|` in the description-cell link |
| **2 (High)** | docs/review_phase1/REVIEW_SKILL_REPORT.md | 614 | Broken wikilink | `[[wikilinks]]` resolves to nothing (descriptive prose) | Remove brackets → plain/inline-code "wikilinks" |
| **2 (High)** | EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | frontmatter | Missing frontmatter | Workflow hub has no YAML metadata | Add `title`/`date`/`tags`/`cssclass` |
| **2 (High)** | *14 skill files* | frontmatter | Missing frontmatter | No YAML metadata on any skill card | Apply skill-card frontmatter template (§5.1) |
| **3 (Medium)** | EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md | — | Orphan file | Zero inbound links (graph hub) | Add backlinks from each skill / a vault index |
| **3 (Medium)** | docs/review_phase1/REVIEW_PHASE{1–4}_*.md | — | Orphan files (×4) | Zero inbound links | Link each from [[REVIEW_SKILL_REPORT]] "Source Phases" |
| **3 (Medium)** | docs/review_phase1/REVIEW_SKILL_REPORT.md | — | Orphan file | Zero inbound links | Link from a vault index / MOC |
| **3 (Medium)** | docs/review_phase1/REVIEW_PHASE3_QUALITY.md | 150 | Deprecated name | Prose ref to `PRODUCT_OWNER_TPM_SKILL` | Rename to `PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL` |
| **3 (Medium)** | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 294 + 3 others | Tag case collision | `#technology-transfer` vs `#Technology-Transfer` | Normalize to lowercase `#technology-transfer` |
| **4 (Low)** | EMBEDDED_SYSTEMS_ARCHITECT_SKILL.md | 360, 363 | Tag redundancy | `#ARB` / `#ARB-decision` / `#Architecture-Review-Board` | Consolidate to `#ARB` |
| **4 (Low)** | ARCH/FW/HW/DATA skill files | §6.2 lines | Self-referencing links | 12 self-loops in graph | Replace self-links with bold plain text |
| **4 (Low)** | docs/review_phase1/*.md | many | Bare wikilinks | Bare role links display raw filenames | Add `\|alias` display names |
| **4 (Low)** | prompt_obsidian.md | — | Orphan + no frontmatter | Meta/prompt scratch file | Move out of vault or add frontmatter |
| **4 (Low)** | review phase docs ×4 | frontmatter | Stale `status: draft` | Superseded by merged report | Set `status: superseded` |

---

## 9. Vault Health Score

### 9.1 Scoring Methodology

Per the prescribed rubric (start at 100):

| Category | Penalty | Honest Count | Deduction |
|---|---|---|---|
| Broken wikilinks (rendered, no target) | −5 each | 1 ([[REVIEW_SKILL_REPORT]]:614) | −5 |
| Filename mismatches | −2 each | 1 (deprecated prose ref, REVIEW_PHASE3:150) | −2 |
| Orphan files (zero inbound) | −3 each | 7 | −21 |
| Missing frontmatter | −2 each | 16 | −32 |
| Single-use tags | −1 each | 3 *(see note)* | −3 |
| **Total deductions** | | | **−63** |

**Counting notes (for honesty and transparency):**
- **Broken wikilinks:** Only the 1 *rendered* unresolved link is counted. The 6 `prompt_obsidian.md` placeholders sit inside inline code / code fences and are **not** rendered as links by Obsidian, so they are not penalized.
- **Single-use tags:** The rubric heading is "Possible **Typos or Orphans**." Of the 49 single-use tags, the overwhelming majority are intentional, meaningful domain tags (`#WCAG`, `#STRIDE`, `#FMEA`-adjacent, etc.) and are **not** defects. Only the 3 that are genuine case/concept duplicates (`#Technology-Transfer` collision + the 2 redundant `#ARB-decision`/`#Architecture-Review-Board` members) are penalized.
- **Literal-formula alternative (for transparency):** if all 49 single-use tags were penalized at −1, total deductions would be −109 → a clamped **0/100**. That figure is a rubric artifact (it treats every specific tag as a defect) and would *deflate* the true health of a vault with near-perfect link integrity. The calibrated figure below is the honest assessment.
- **Not in the rubric but material:** the 38 unescaped table-cell pipes (§6.4) carry **no** rubric penalty, yet they are the highest-priority practical fix. The numeric score therefore *understates* the importance of that one issue — see the assessment.

### 9.2 Score

- **Vault Health Score: 37/100**
- **Grade: F** (scale: A ≥ 90, B 80–89, C 70–79, D 60–69, F < 60)
- **Assessment:** Excellent link integrity and structure (953/960 links resolve, 0 duplicate headings, clean numbering, dense skill graph), but the formal score is dominated by two systematic, trivially-fixable hygiene gaps — **absent frontmatter on the 16 metadata-less files (−32)** and **7 un-backlinked hub/report files (−21)**. Remediating frontmatter, de-orphaning via an index, fixing the single broken link, the deprecated prose name, and the tag collisions would raise the score to **≈ 98/100 (A)** — and escaping the 38 table pipes (§6.4) would make the vault fully Obsidian-clean. **The low grade reflects metadata completeness, not structural dysfunction.**

---

## 10. Recommendations for Ongoing Maintenance

1. **Adopt a frontmatter standard and enforce it.** Add the §5.1 skill-card template to every new role/content file (`title`, `date`, `status`, `tags`, `cssclass`). Consider the *Templater* or *QuickAdd* community plugin so new notes start with valid YAML, and use *Dataview* to list any file missing required fields.

2. **Always escape pipes inside table-cell wikilinks (`[[Note\|alias]]`).** This is the recurring rendering bug in this vault. Add a pre-commit `grep` check that fails on the pattern `\|[^\|]*\]\]` appearing within table rows (lines starting with `|`) but not preceded by `\`. Re-verify affected tables in Obsidian **Reading view**, not just the editor.

3. **Maintain a vault index / Map-of-Content (MOC).** Create a `HOME.md` (or `INDEX.md`) that wikilinks the workflow doc, all 14 skill cards, and the review set. This eliminates orphans permanently and gives Obsidian's graph a hub. Have [[REVIEW_SKILL_REPORT]] explicitly link its 4 phase sub-reports.

4. **Keep tag casing consistent (lowercase-kebab-case; uppercase only for acronyms).** Periodically open the Obsidian **Tags** pane to spot case-collisions (like `#technology-transfer` vs `#Technology-Transfer`) and single-use tags that should fold into an existing tag. Treat the tag list as a controlled vocabulary.

5. **Run this audit after every rename or renumbering.** When a file is renamed, use Obsidian's automatic link-update, then grep the vault for the old basename in **prose and inline code** (which Obsidian does *not* auto-update) — that is exactly how `PRODUCT_OWNER_TPM_SKILL` survived in [[REVIEW_PHASE3_QUALITY]]. Re-generate this report periodically and track the health score over time.
