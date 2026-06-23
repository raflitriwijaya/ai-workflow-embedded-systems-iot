# GUIDELINE.md — Practical User Guide

> **For:** Project Owner
> **Purpose:** A friendly, practical guide on how to use this ecosystem every day.
> **Last updated:** 2026-06-22

---

## 🚀 Quick Start (5 Minutes)

You've built something impressive. Here's the fastest path to feeling at home in it:

- **Open `[[HOME|HOME.md]]`** — it's your index. Everything links from here.
- **Read `[[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM|EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md]]` §1 and §14** — the team topology and the Mermaid diagram showing how all 14 roles connect.
- **Pick one role** and open its `*_SKILL.md` — jump straight to **§2** (what it owns) and **§6** (who it talks to).
- **Check the audit verdict** in `[[REVIEW_V3_FINAL|docs/review_v3/REVIEW_V3_FINAL.md]]` — the system is a CONDITIONAL GO; 17 open Critical chains need burn-down before you can ship.
- **Remember the prime rule:** no role starts implementation without a frozen interface contract. When in doubt, write the contract first.

---

## 🧭 How to Navigate This Vault

This vault is built for [Obsidian](https://obsidian.md). Once open, you have two main ways to find things:

**Graph View** (`Ctrl+G` / `Cmd+G`)
Shows every file as a node, with links as edges. Clusters of connected nodes reveal which roles and documents are most central. Use it for orientation, not daily navigation.

**`[[HOME|HOME.md]]` — Your Index**
The single best place to start every session. It links to all 14 SKILL.md files, every schema, the audit history, and the governance docs. Treat it like a dashboard.

**Quick file map:**

| Location | What's there |
|---|---|
| Vault root | `CLAUDE.md`, `HOME.md`, `GUIDELINE.md`, `README.md`, 14 `*_SKILL.md` files |
| `docs/agent-protocol/` | MACP master spec + 5 schema files for multi-agent coordination |
| `docs/schemas/` | 8 machine-parseable schemas (ADR, CCR, IRD, OCM, SIRC, etc.) |
| `docs/fmea/` | System FMEA — 36 failure chains, 17 still Critical |
| `docs/review_v1–v3/` | Audit history (historical only — SKILL.md is always authoritative) |
| `docs/evaluation/` | Evaluation Harness — used before activating AI agents |
| `docs/security/` | Device attestation spec |
| `docs/operations/` | Incident Commander playbook |

---

## 📖 How to Read a SKILL.md

Every role has exactly one SKILL.md. All 14 follow the same 10-section structure, so once you learn one, you know them all.

**The 10 sections — and what matters most:**

| Section | What it tells you | Priority |
|---|---|---|
| **§1 Role Identity** | Title, team, seniority, 4-tier career ladder | Context |
| **§2 Core Mission & Scope** | What this role *owns*, *influences*, and explicitly does *NOT own* | **Read first** |
| **§3 Lifecycle Engagement** | What the role does in each of 6 project phases | Reference |
| **§4 Technical Competencies** | Skill proficiency table | Hiring/leveling |
| **§5 Deliverables & Artifacts** | Every artifact the role produces, with format and versioning | **Read second** |
| **§6 Interface Contracts** | Who this role works with, what it gives them, what it needs back | **Read third** |
| **§7 Decision Authority** | What this role decides alone vs. with others; ADR standing | Governance |
| **§8 Standards & Best Practices** | Domain standards (IEC, MISRA, OWASP, etc.) | Reference |
| **§9 AI Agent Execution Guide** | How to brief an AI agent playing this role | Agent use |
| **§10 Success Metrics & KPIs** | How you know the role is performing well | Measurement |

**A 2-minute tour — try it on `[[FIRMWARE_ENGINEER_SKILL|FIRMWARE_ENGINEER_SKILL.md]]`:**

1. §2 → confirms FW owns firmware build/flash/RTOS; does NOT own cloud APIs or ML training.
2. §5 → lists the firmware binary (Git-SHA + SemVer), HAL drivers, OTA packages.
3. §6 → shows FW's contract with ML (receives quantized TFLite model; provides flash budget confirmation) and with DEVOPS (receives CI pipeline; provides build artifacts).

That's enough to understand FW's place in the system in under two minutes.

---

## 🔗 How Roles Work Together

**The core idea:** every pair of roles has a formal contract describing exactly what each side gives and receives. With 14 roles, that's 91 unique contracts — all of them defined.

**The Provides / Requires / Cadence triple**

Every contract entry in a role's §6 states three things:

- **Provides:** what *this* role sends to the other
- **Requires:** what *this* role needs from the other
- **Cadence:** when they sync (e.g., "at Planning gate," "per sprint," "on model release")

**How to trace a deliverable:**

1. Identify the producing role (who makes the artifact).
2. Open that role's `*_SKILL.md` → §5 → find the artifact.
3. In §6, find the consumer role — the **Provides** line will reference the artifact.
4. Open the consumer's SKILL.md → §6 → find the producing role — the **Requires** line should mirror it.

This symmetry is enforced. If you ever find a mismatch (A says it provides X, but B's §6 doesn't require X), that's a gap worth logging as a CCR (Contract Clarification Record — see §6 below).

**To find who depends on whom:** open `[[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM|EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md]]` §14 — the Mermaid diagram maps every connection at a glance.

---

## ⚖️ How Governance Works

You don't need to memorize the full governance stack. You need to know three things:

**1. When to write an ADR (Architecture Decision Record)**

An ADR is a short document recording *why* a significant technical decision was made. Write one whenever:
- You choose a platform, protocol, or technology outside the current stack
- A contract, budget, or requirement can't be met as written
- Any security baseline changes
- A production or OTA governance rule changes

ADRs use the schema at `[[ADR_SCHEMA|docs/schemas/ADR_SCHEMA.md]]`. ID format: `ADR-NNNN`.

**2. When to write a CCR (Contract Clarification Record)**

A CCR is how you formally change or clarify a role contract. Write one whenever a §6 clause is ambiguous, has a gap, or needs to change. A **BLOCKING** CCR halts all related work until resolved. Schema: `[[CCR_SCHEMA|docs/schemas/CCR_SCHEMA.md]]`.

**3. The release gate sequence (always in this order)**

Before anything goes to production:

1. Architect robustness sign-off (no TBD values in NFR matrix)
2. Security Engineer release sign-off / veto
3. QA go/no-go
4. Product Owner release decision
5. OTA readiness review
6. Business GTM readiness check

**Decision speed tiers** — not everything needs a meeting:

| Tier | Urgency | Who decides |
|---|---|---|
| 1 — CRITICAL | 4 business hours | Human only, always |
| 2 — HIGH | 2 business days | Human ratifies AI recommendation |
| 3 — MEDIUM | 5 business days | AI decides if confidence ≥ 0.70 |
| 4 — LOW | 10 business days | AI decides autonomously |

When in doubt, classify **upward** (more conservative). Never resolve at a lower tier than justified.

---

## 🤖 How to Activate AI Agents

**The principle: Measure First, Delegate Second.**

Before any AI agent takes on a role autonomously, you need a human baseline — at least 30 human-produced examples of each deliverable, scored via the `[[EVALUATION_HARNESS_SPEC|docs/evaluation/EVALUATION_HARNESS_SPEC.md]]`.

**The Wave System — activation in order:**

| Wave | What happens | Who's involved |
|---|---|---|
| Wave 0 | Human-operated only | You |
| Wave 1 | MACP registries online | AI can read/register |
| Wave 2 | A2A messaging active | AI agents talk to each other |
| Wave 3 | Tier 3 autonomy enabled | AI decides MEDIUM/LOW tier items |
| Wave 4 | Full governance participation | AI submits data, votes (non-binding) |

**Three things that must be true before activating a role agent:**
1. Evaluation Harness baseline captured (≥ 30 human samples per deliverable)
2. MACP at Wave 1 or higher
3. No open BLOCKING CCR on that role's contracts

**Permanent human gates — these never go to AI:**
- Security Engineer release veto (HG-01)
- Architect production sign-off (HG-04)
- QA go/no-go stage transition

No agent can override, bypass, or argue against these three. If a task requires it, escalate immediately with `ESC-TIER1`.

---

## 📊 How to Read Audit Reports

The project has three audit layers, each building on the last:

| Audit | Location | Finding | Status |
|---|---|---|---|
| V1 — Org Audit | `docs/review_v1/` | 37 findings | All remediated |
| V2 — Holistic Validation | `docs/review_v2/` | Conditional yes; hollow robustness gate | Historical |
| V3 — Lifecycle Simulation | `[[REVIEW_V3_FINAL|docs/review_v3/REVIEW_V3_FINAL.md]]` | **CONDITIONAL GO** | **Current verdict** |

**What CONDITIONAL GO means in practice:**

The system is well-designed and the team is real. But there are 17 open Critical FMEA failure chains (RPN ≥ 200) that have no mitigation yet. You cannot ship to production until these are burned down.

The most important chains to watch:
- **FC-001** (spectral-AFE drift; RPN 486) — highest risk
- **FC-022** (silent corruption loop; RPN 405) — hardest to detect

**Your burn-down path:** build the 9 missing detection controls, validate against the FC-IDs in `[[SYSTEM_FMEA_V1|docs/fmea/SYSTEM_FMEA_V1.md]]`, then re-run the QA gate. Detection coverage needs to reach ≥ 95% (currently ≈ 53%).

---

## ❓ Common Questions

**Q: Where do I start if I'm new to a role?**
Open the role's `*_SKILL.md`, read §2 first (scope), then §6 (contracts), then §9 (how to use it with AI).

**Q: A role says it needs something from another role. Where's the agreement?**
In the other role's `*_SKILL.md` §6 — find the subsection for the first role. The Provides/Requires should mirror each other. If they don't, log a CCR.

**Q: Can I change a role's responsibilities?**
Not unilaterally. Changes to §6 contracts require a CCR. Changes to scope (§2) require an ADR if they cross role boundaries.

**Q: How do I know if an AI agent is ready to operate a role?**
Check: (a) Evaluation Harness baseline captured, (b) MACP Wave 1+, (c) no BLOCKING CCR open. All three must be true.

**Q: The FMEA has 17 Critical chains. Do I fix them all at once?**
No — prioritize by RPN. FC-001 (486) and FC-022 (405) first. The 9 "does not exist today" controls are the build targets. Each control closed reduces the Critical count.

**Q: What if an AI agent gives me a number without units, or says "approximately"?**
That's a violation of the conventions in `[[CLAUDE|CLAUDE.md]]` §3.10. Flag it and ask for the exact value with units. Never accept TBD in a `status: final` document.

**Q: Where do I escalate when something is blocked?**
Follow the escalation trigger table in `[[CLAUDE|CLAUDE.md]]` §7.4. For Tier 1 issues, go directly to the human decision-maker — no AI in the loop.

---

## 🗺️ Where to Go for What

| I want to... | Go to... |
|---|---|
| Get oriented quickly | `[[HOME|HOME.md]]` |
| Understand the whole project | `[[README|README.md]]` |
| Configure AI agents | `[[CLAUDE|CLAUDE.md]]` |
| Find a role's responsibilities | `*_SKILL.md` §2 |
| See what a role produces | `*_SKILL.md` §5 |
| Know who a role works with | `*_SKILL.md` §6 |
| Brief an AI agent on a role | `*_SKILL.md` §9 |
| Understand governance rules | `[[CLAUDE|CLAUDE.md]]` §6 |
| See all 14 roles at once | `[[EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM|EMBEDDED_IOT_AI_WORKFLOW_ENGINEERING_TEAM.md]]` §14 |
| Check the current audit verdict | `[[REVIEW_V3_FINAL|docs/review_v3/REVIEW_V3_FINAL.md]]` |
| Find open Critical failure chains | `[[SYSTEM_FMEA_V1|docs/fmea/SYSTEM_FMEA_V1.md]]` |
| Set up AI agent evaluation | `[[EVALUATION_HARNESS_SPEC|docs/evaluation/EVALUATION_HARNESS_SPEC.md]]` |
| Log a contract change | `[[CCR_SCHEMA|docs/schemas/CCR_SCHEMA.md]]` |
| Log an architecture decision | `[[ADR_SCHEMA|docs/schemas/ADR_SCHEMA.md]]` |
| Understand multi-agent coordination | `[[MULTI_AGENT_COORDINATION_PROTOCOL|docs/agent-protocol/MULTI_AGENT_COORDINATION_PROTOCOL.md]]` |
| Handle a production incident | `[[INCIDENT_COMMANDER|docs/operations/INCIDENT_COMMANDER.md]]` |
| Look up an acronym | `[[ACRONYM_GLOSSARY|docs/ACRONYM_GLOSSARY.md]]` |

---

## 📞 Getting Help

**Stuck on a governance question?** The answer is almost always in `[[CLAUDE|CLAUDE.md]]` — it's the master reference. Check §6 for governance, §7 for agent rules, §10 for project-specific rules.

**Stuck on what a role does?** Open the role's `*_SKILL.md` and go to §2 (scope) and §9 (execution guide). They're written to be self-contained.

**Found a gap or inconsistency?** That's a CCR. Use `[[CCR_SCHEMA|docs/schemas/CCR_SCHEMA.md]]` to log it formally. Don't work around it silently — the system is designed to surface and resolve gaps, not hide them.

**Need a second opinion?** The audit reports in `docs/review_v1–v3/` explain *why* each design decision was made. They're your historical record of what was considered and why.

You built a rigorous, well-validated system. Trust it — and when something feels wrong, the governance tools are there specifically to help you surface and fix it cleanly.
