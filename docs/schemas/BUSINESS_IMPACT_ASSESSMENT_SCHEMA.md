---
title: "Business Impact Assessment Schema"
owning_roles:
  - "[[BUSINESS_CONSULTANT_SKILL]]"
consuming_roles:
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
  - "ARB (Architecture Review Board)"
  - "All roles receiving an ADR with BIA appended"
version: "1.0.0"
tags:
  - schema
  - business-impact
  - adr
  - governance
  - machine-parseable
  - cost
---

# Business Impact Assessment Schema

## Purpose

A Business Impact Assessment (BIA) is produced by the Business Consultant and appended to an ADR when a decision has material cost, schedule, or market implications. It translates technical choices into business language for ARB deliberation. The machine-parseable schema enables automated financial risk scoring, aggregation of per-ADR cost deltas into sprint burn-down, and structured comparison of decision alternatives.

**Standards referenced:** ISO 31000:2018 (Risk Management), PMI PMBOK 7th Ed. (Schedule and Cost Management), IEC 62443-2-1 §4.2.3 (Business Risk Assessment).

---

## YAML Schema Definition

```yaml
# Business Impact Assessment Schema v1.0.0

schema_version: "1.0.0"           # (required) string

# ── Identity ──────────────────────────────────────────────────────────────────
id: string                         # (required) BIA-NNNN format, e.g. "BIA-0007"
linked_adr: string                 # (required) ADR-NNNN — the ADR this BIA is appended to
date_produced: date                # (required) ISO 8601
date_reviewed: date                # (optional) ISO 8601 — filled by Architect or ARB

# ── Produced By ───────────────────────────────────────────────────────────────
produced_by:
  role: string                     # (required) "[[BUSINESS_CONSULTANT_SKILL]]"
  name: string                     # (optional)

# ── Decision Context ──────────────────────────────────────────────────────────
decision_summary: string           # (required) ≥30 chars — brief restatement of the ADR decision for business audience
decision_options_compared:         # (required) list — mirrors ADR options_considered; at least 2 entries
  - option_id: string              # (required) matches ADR option id, e.g. "A", "B"
    option_label: string           # (required) non-technical label, e.g. "Retain current TLS"
    selected: boolean              # (required) true for the chosen option only

# ── Cost Impact ───────────────────────────────────────────────────────────────
cost_impact:
  selected_option:
    one_time_capex_usd: number     # (required) one-time capital expenditure; 0 if none
    recurring_opex_usd_per_month: number # (required) monthly operational cost delta; negative = saving
    total_12_month_cost_usd: number # (required) computed: capex + (opex × 12); agent validates
    avoided_cost_usd: number       # (optional) cost of NOT making this decision (e.g., breach, recall)
    net_cost_usd: number           # (required) total_12_month_cost_usd - avoided_cost_usd
  alternatives_cost_comparison:    # (required) cost breakdown per rejected option
    - option_id: string
      one_time_capex_usd: number
      recurring_opex_usd_per_month: number
      total_12_month_cost_usd: number
  confidence:                      # (required)
    level: string                  # enum: LOW | MEDIUM | HIGH
    basis: string                  # ≥20 chars — how the estimate was derived
  cost_assumptions: list[string]   # (required) at least 1 — assumptions underlying the numbers

# ── Schedule Impact ───────────────────────────────────────────────────────────
schedule_impact:
  delta_calendar_days: integer     # (required) positive = delay, negative = acceleration
  affected_milestones: list[string] # (required) milestone names affected (empty list if none)
  critical_path_impact: boolean    # (required) true if change is on the project critical path
  schedule_assumptions: list[string] # (required) at least 1 assumption

# ── Market Impact ─────────────────────────────────────────────────────────────
market_impact:
  revenue_impact_usd_12mo: number  # (optional) estimated revenue delta over 12 months; 0 if none
  market_segments_affected: list[string] # (optional) e.g. ["EU Industrial IoT", "APAC Smart Factory"]
  competitive_impact: string       # (required) ≥30 chars — effect on competitive position
  regulatory_impact: string        # (required) ≥20 chars — compliance or regulatory implications (cite standards)
  customer_impact: string          # (required) ≥20 chars — effect on end customers or partners
  reputational_risk: string        # (required) enum: NONE | LOW | MEDIUM | HIGH
  reputational_risk_notes: string  # (required when reputational_risk ∈ {MEDIUM, HIGH}) ≥20 chars

# ── Risk Register ─────────────────────────────────────────────────────────────
business_risks:                    # (required) list — ISO 31000 aligned; at least 1 entry
  - id: string                     # (required) e.g. "BR-001"
    description: string            # (required) ≥20 chars — risk description
    probability: string            # (required) enum: LOW | MEDIUM | HIGH
    impact: string                 # (required) enum: LOW | MEDIUM | HIGH | CRITICAL
    risk_score: string             # (required) computed label: LOW | MEDIUM | HIGH | CRITICAL
                                   # matrix: CRITICAL if impact=CRITICAL; HIGH if high×high; etc.
    mitigation: string             # (required) ≥20 chars — mitigation action
    owner: string                  # (required) Obsidian wikilink to owning role
    residual_risk: string          # (required) enum: LOW | MEDIUM | HIGH | CRITICAL — after mitigation

# ── Recommendation ────────────────────────────────────────────────────────────
recommendation:
  verdict: string                  # (required) enum: PROCEED | PROCEED_WITH_MITIGATION | REJECT | DEFER
  rationale: string                # (required) ≥50 chars — business case for the verdict
  conditions: list[string]         # (required when verdict = PROCEED_WITH_MITIGATION) list of conditions
  defer_until: date                # (required when verdict = DEFER) ISO 8601 date to revisit
  roi_estimate:                    # (optional)
    roi_percentage: number         # net benefit / cost × 100
    payback_period_months: integer # months to recoup net cost

# ── ARB Review ────────────────────────────────────────────────────────────────
arb_review:                        # (optional) — filled after ARB deliberation
  date: date
  decision: string                 # enum: ACCEPTED | ACCEPTED_WITH_CONDITIONS | REJECTED | TABLED
  conditions: list[string]
  notes: string

# ── Metadata ──────────────────────────────────────────────────────────────────
tags: list[string]
notes: string
```

---

## Example Instance

```yaml
schema_version: "1.0.0"

id: "BIA-0007"
linked_adr: "ADR-0007"
date_produced: "2026-04-15"
date_reviewed: "2026-04-18"

produced_by:
  role: "[[BUSINESS_CONSULTANT_SKILL]]"
  name: "Maya Putri"

decision_summary: >
  Upgrading the device-to-cloud authentication from TLS 1.2 server-only to TLS 1.3 mutual
  X.509 certificate authentication. This eliminates a confirmed device impersonation attack
  vector at the cost of a 14-day schedule delay and $18,500 one-time infrastructure investment.

decision_options_compared:
  - option_id: "A"
    option_label: "Retain TLS 1.2 with stronger ciphers (minimal change)"
    selected: false
  - option_id: "B"
    option_label: "Upgrade to TLS 1.3 mutual authentication with X.509 PKI"
    selected: true
  - option_id: "C"
    option_label: "Use pre-shared keys with TLS 1.3"
    selected: false

cost_impact:
  selected_option:
    one_time_capex_usd: 15000.0
    recurring_opex_usd_per_month: 292.0
    total_12_month_cost_usd: 18504.0
    avoided_cost_usd: 2100000.0
    net_cost_usd: -2081496.0
  alternatives_cost_comparison:
    - option_id: "A"
      one_time_capex_usd: 500.0
      recurring_opex_usd_per_month: 0.0
      total_12_month_cost_usd: 500.0
    - option_id: "C"
      one_time_capex_usd: 8000.0
      recurring_opex_usd_per_month: 150.0
      total_12_month_cost_usd: 9800.0
  confidence:
    level: MEDIUM
    basis: "PKI infra capex from vendor quotes (3 quotes obtained). Breach avoided cost from Ponemon Institute 2025 IoT breach cost study ($2.1M average for device impersonation incident in industrial IoT at 50K-device scale)."
  cost_assumptions:
    - "PKI infrastructure deployed on existing cloud provider (no new vendor)"
    - "Certificate provisioning automated; no manual per-device cost beyond first 90 days"
    - "Breach cost estimate uses Ponemon 2025 study lower quartile; actual could be higher"
    - "Firmware engineering effort costed at internal day rate"

schedule_impact:
  delta_calendar_days: 14
  affected_milestones:
    - "M3 — Integration Testing Start"
    - "M4 — Security Audit"
  critical_path_impact: true
  schedule_assumptions:
    - "PKI provisioning pipeline can be built in parallel with firmware changes"
    - "No additional hardware procurement delay; PKI is software-only"

market_impact:
  revenue_impact_usd_12mo: 450000.0
  market_segments_affected:
    - "EU Industrial IoT (IEC 62443 compliance is procurement requirement)"
    - "Healthcare IoT (medical device security certification)"
  competitive_impact: >
    IEC 62443-4-2 CL2 compliance unlocks EU industrial IoT procurement tenders estimated
    at $450K ARR. Two identified competitors already hold this certification; non-compliance
    would cost us these bids.
  regulatory_impact: >
    EU Cyber Resilience Act (CRA) effective 2027 mandates mutual authentication for
    internet-connected devices. Early adoption eliminates a future compliance sprint.
    References: EU CRA Article 13, IEC 62443-4-2 CR 1.1.
  customer_impact: >
    Enterprise customers with IEC 62443 requirements can now procure without additional
    security assessment overhead. Consumer segment unaffected.
  reputational_risk: MEDIUM
  reputational_risk_notes: >
    If Option A is chosen and a device impersonation incident occurs at scale, media coverage
    of a 50K-device compromise would materially damage brand trust in the industrial segment.

business_risks:
  - id: "BR-001"
    description: "PKI provisioning pipeline overruns 14-day schedule estimate, delaying M3"
    probability: LOW
    impact: HIGH
    risk_score: MEDIUM
    mitigation: "Begin PKI vendor engagement immediately; use existing cloud certificate manager to prototype. Weekly milestone check with DevOps."
    owner: "[[DEVOPS_PLATFORM_ENGINEER_SKILL]]"
    residual_risk: LOW

  - id: "BR-002"
    description: "Certificate revocation at fleet scale (50K devices) is operationally complex and may cause device lockout"
    probability: MEDIUM
    impact: HIGH
    risk_score: HIGH
    mitigation: "Design OCSP stapling with fallback grace period. Staged rollout via canary deployment (ADR-0007 deployment policy). Revocation runbook mandated before M4."
    owner: "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
    residual_risk: MEDIUM

  - id: "BR-003"
    description: "Vendor dependency on cloud PKI service creates single point of failure for device onboarding"
    probability: LOW
    impact: CRITICAL
    risk_score: CRITICAL
    mitigation: "Multi-region PKI deployment with active-active failover. SLA contract with cloud provider for 99.99% availability."
    owner: "[[DEVOPS_PLATFORM_ENGINEER_SKILL]]"
    residual_risk: MEDIUM

recommendation:
  verdict: PROCEED_WITH_MITIGATION
  rationale: >
    The net 12-month economic value of Option B is strongly positive (-$2.08M net cost, i.e.
    net saving of $2.08M after avoided breach cost). The 14-day schedule impact is on the
    critical path but is manageable with parallel workstreams. The IEC 62443 compliance benefit
    opens $450K ARR of identified revenue. Proceeding with BR-002 and BR-003 mitigations
    as mandatory conditions.
  conditions:
    - "BR-002 mitigation: OCSP stapling with grace period must be designed and reviewed before M3"
    - "BR-003 mitigation: Multi-region PKI architecture must be confirmed with cloud vendor before contract sign"
    - "Firmware flash budget re-validation (for mbedTLS upgrade) must pass before Sprint-13 ends"
  defer_until: null
  roi_estimate:
    roi_percentage: 11251.3
    payback_period_months: 1

arb_review:
  date: "2026-04-18"
  decision: ACCEPTED_WITH_CONDITIONS
  conditions:
    - "BR-003 risk must be downgraded to LOW before M4 sign-off"
  notes: "ARB accepted BIA-0007 unanimously. ADR-0007 status updated to DECIDED."

tags:
  - bia
  - adr-0007
  - security
  - tls
  - pki
  - proceed-with-mitigation

notes: "Ponemon 2025 IoT breach cost study referenced at docs/research/ponemon-2025-iot-breach.pdf"
```

---

## Validation Rules

| Rule | Condition |
|------|-----------|
| V-BIA-01 | `id` matches regex `^BIA-\d{4}$` |
| V-BIA-02 | `linked_adr` matches `^ADR-\d{4}$` and exists in ADR registry |
| V-BIA-03 | `decision_options_compared` has ≥ 2 entries |
| V-BIA-04 | Exactly one entry in `decision_options_compared` has `selected = true` |
| V-BIA-05 | `cost_impact.selected_option.total_12_month_cost_usd` = `one_time_capex_usd` + (`recurring_opex_usd_per_month` × 12) (±$1 rounding) |
| V-BIA-06 | `cost_impact.selected_option.net_cost_usd` = `total_12_month_cost_usd` − `avoided_cost_usd` |
| V-BIA-07 | `cost_impact.confidence.level` ∈ {LOW, MEDIUM, HIGH} |
| V-BIA-08 | `cost_assumptions` has ≥ 1 entry |
| V-BIA-09 | `business_risks` has ≥ 1 entry |
| V-BIA-10 | `business_risks[*].risk_score` is consistent with the probability × impact matrix |
| V-BIA-11 | `recommendation.verdict` ∈ {PROCEED, PROCEED_WITH_MITIGATION, REJECT, DEFER} |
| V-BIA-12 | If `verdict = PROCEED_WITH_MITIGATION`, `conditions` list must be non-empty |
| V-BIA-13 | If `verdict = DEFER`, `defer_until` must be non-null |
| V-BIA-14 | If `reputational_risk ∈ {MEDIUM, HIGH}`, `reputational_risk_notes` must be non-null |
| V-BIA-15 | `roi_estimate.roi_percentage` = (`avoided_cost_usd` − `total_12_month_cost_usd`) / `total_12_month_cost_usd` × 100 (when present) |

---

## Machine-Actionability Notes

An AI agent validating or processing this artifact should:

1. **Arithmetic validation**: independently compute `total_12_month_cost_usd`, `net_cost_usd`, and `roi_percentage` from component fields; flag any discrepancy > $1 (rounding).
2. **ADR linkage**: verify `linked_adr` exists in the ADR registry and that this BIA ID appears in the ADR's `business_impact_assessment` block.
3. **Option selection consistency**: verify exactly one `decision_options_compared` entry has `selected = true` and that this option's `option_id` matches the ADR's chosen option.
4. **Risk matrix validation**: for each business risk, validate `risk_score` against the standard probability × impact matrix:
   - CRITICAL impact → CRITICAL score regardless of probability
   - HIGH probability + HIGH impact → HIGH
   - LOW probability + LOW impact → LOW
   - All other combinations → MEDIUM
5. **Recommendation alignment**: if `verdict = REJECT`, verify `linked_adr.status ≠ DECIDED`; an approved ADR should not have a REJECT BIA without ARB override.
6. **ARB decision propagation**: when `arb_review.decision = ACCEPTED`, automatically update the linked ADR's `status` to `DECIDED` if not already set.
7. **Aggregation**: sum all `cost_impact.selected_option.one_time_capex_usd` across all `DECIDED` ADRs in a sprint for the sprint financial burn-down report.
