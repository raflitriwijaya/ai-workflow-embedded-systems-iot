# Prompt Execution — Low-Severity Remediation (LR-7 through LR-12)

## [SYSTEM]

You are a senior organizational architect and precision editor with 25+ years of experience performing final-fit-and-finish remediation on sociotechnical system designs. You are executing the second half of the Low-severity recommendations (LR-7 through LR-12) from the organizational audit `[[REVIEW_SKILL_REPORT]]`. Each is a small, self-contained surgical edit. You work with extreme precision, following instructions exactly, and produce output that integrates seamlessly into existing documents within an Obsidian vault.

All output must be fully Obsidian-compatible:
- Every reference to another role uses `[[SKILL_FILENAME]]` wiki-link syntax.
- Every key concept is tagged with inline `#tag` notation.
- You do not add commentary or meta-remarks outside the delimited output blocks.
- You process all 6 recommendations efficiently, producing exactly what is needed for each.

---

## [TASK]

Execute **6 precision surgical additions** across 5 SKILL.md files to close Low-severity audit findings LR-7 through LR-12. Each is a small, self-contained edit: a new sentence, a new table row, a new KPI, a new template, or a new cadence note. Output exactly 6 blocks, one per LR.

---

## [CONTEXT] — The 6 Low-Severity Recommendations

| LR | Title | Target File(s) | Edit Type |
|----|-------|----------------|-----------|
| **LR-7** | Clarify OTA artifact format ownership | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` §5 | Append sentence to existing table row |
| **LR-8** | Add automated Model Rebuildability Verification Job | `[[MLOPS_ENGINEER_SKILL]]` §5 + §10 | New table row + new KPI bullet |
| **LR-9** | Designate North Star KPIs | `[[BUSINESS_CONSULTANT_SKILL]]` §10 | Insert at top of KPI section |
| **LR-10** | Add Business Impact field to ADR template + cadence note | `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` §7 + `[[BUSINESS_CONSULTANT_SKILL]]` §6.2 | New field + new cadence bullet |
| **LR-11** | Add Accessibility Audit & Remediation prompt template | `[[FRONTEND_DASHBOARD_ENGINEER_SKILL]]` §9.4 | New numbered template |
| **LR-12** | Increase BIZ↔PO cadence during Planning & Development | `[[BUSINESS_CONSULTANT_SKILL]]` §6.1 + `[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL]]` §6 | Append cadence note to both files |

### Detailed Descriptions

**LR-7** — Clarify OTA artifact format ownership in `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` §5. Append a sentence to the existing "OTA Strategy Specification" row's Description column stating that this specification includes the canonical OTA artifact format (MCUboot image format, signing envelope, metadata manifest, naming convention) and is the authoritative reference for `[[FIRMWARE_ENGINEER_SKILL|FW]]`, `[[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]]`, `[[BACKEND_CLOUD_ENGINEER_SKILL|Backend]]`, and `[[MLOPS_ENGINEER_SKILL|MLOps]]`.

**LR-8** — Add an automated Model Rebuildability Verification Job to `[[MLOPS_ENGINEER_SKILL]]` §5 (new row in Deliverables & Artifacts table) and a corresponding KPI in §10. The job randomly samples one registered model per product line weekly, rebuilds from lineage, and verifies binary-identical artifact. Failure triggers a reproducibility incident.

**LR-9** — Designate 3–5 North Star KPIs at the top of `[[BUSINESS_CONSULTANT_SKILL]]` §10, with a note that all other KPIs are diagnostic. North Star KPIs: Product Revenue Growth Rate, Product-Market Fit Score, LTV:CAC Ratio, Gross Margin, Time-to-Market Accuracy.

**LR-10** — Add a "Business Impact" field to the ADR template in `[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]` §7, and a corresponding cadence note in `[[BUSINESS_CONSULTANT_SKILL]]` §6.2 that the Business Consultant provides the Business Impact Assessment within 10 business days for ADRs tagged `#business-impact`.

**LR-11** — Add a dedicated "Accessibility Audit & Remediation" prompt template (Template 6 or next available) to `[[FRONTEND_DASHBOARD_ENGINEER_SKILL]]` §9.4, covering WCAG 2.1 AA automated and manual testing for real-time dashboards.

**LR-12** — Increase cadence between `[[BUSINESS_CONSULTANT_SKILL]]` and `[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL]]` during Planning and early Development stages. Append to both BIZ §6.1 and PO §6 (BIZ interface) a note that the Business Consultant co-locates (virtual or physical) with the PO/TPM during Planning and the first 2 weeks of Development for daily stand-ups and ad hoc consultation within 2 hours.

---

## [OUTPUT FORMAT]

Output exactly six blocks, each delimited with `### BLOCK N: LR-N [title]` headers. Each block contains **ONLY** the Markdown content to be directly inserted into the target Obsidian note. Output nothing else — no preamble, no closing remarks, no meta-commentary.

---

### BLOCK 1: LR-7 — OTA Artifact Format Ownership in [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] §5

**Instruction:** Output the sentence to append to the **Description** column of the existing "OTA Strategy Specification" row in the Architect's §5 Deliverables & Artifacts table. Do not create a new row; provide only the text to add to the existing cell.

**Content to append to the OTA Strategy Specification Description:**

> The OTA Strategy Specification also defines the canonical OTA artifact format, which is the single authoritative reference for all roles in the OTA pipeline: (a) image format (MCUboot-compatible binary layout with manifest header), (b) signing envelope (algorithm identifier, key reference, signature block structure), (c) metadata manifest (firmware/model version, target hardware ID, compatibility matrix, flash-budget check fields, A/B slot designation), and (d) artifact naming and versioning convention (SemVer — Semantic Versioning — with build metadata). [[FIRMWARE_ENGINEER_SKILL|Firmware]] produces artifacts to this format; [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] packages and distributes artifacts in this format; [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] references this format in the desired-state control plane; [[MLOPS_ENGINEER_SKILL|MLOps]] ensures model artifacts conform to this format. Any change to the artifact format requires an ADR (Architecture Decision Record) with all four consuming roles as consulted parties. #OTA-artifact-format #single-source-of-truth

---

### BLOCK 2: LR-8 — Model Rebuildability Verification Job for [[MLOPS_ENGINEER_SKILL]] §5 and §10

**Instruction:** Two insertions — (a) a new row in the §5 Deliverables & Artifacts table, and (b) a new bullet in the §10 Technical metrics list.

**(a) New row for the §5 Deliverables & Artifacts table:**

| Artifact | Description | Consumers | Format | Versioning |
|----------|-------------|-----------|--------|------------|
| Model Rebuildability Verification Job | Automated CI job executing weekly. Selects a random registered model version from the MLflow Model Registry (1 per product line per week). Attempts a clean rebuild from recorded lineage: dataset version (DVC — Data Version Control — reference) → training code version (Git commit SHA) → training config (pinned hyperparameters) → conversion script (fixed version). Rebuild succeeds if the reproduced model artifact is binary-identical (SHA-256 hash match) to the registered artifact. Rebuild failure triggers a #reproducibility-incident: root-cause analysis within 2 business days, remediation within 5 business days. Results published to the MLOps observability dashboard. Consecutive weekly failures for the same model block the next model release until root cause is resolved. | [[EDGE_AI_ML_ENGINEER_SKILL|Edge AI/ML]], [[DATA_ENGINEER_SKILL|Data]], [[QA_TEST_ENGINEER_SKILL|QA]] | Automated CI job (Python/pytest) + weekly Markdown report | Versioned with the MLOps pipeline repository; report generated weekly and archived |

**(b) New bullet for §10 Technical metrics:**

> - **Model rebuildability:** 100% of weekly sampled models rebuild successfully from lineage (binary-identical artifact). Any rebuild failure is a #reproducibility-incident. Remediation: root cause identified within 2 business days, resolved within 5 business days. Consecutive failures for the same model block the next model release. Measured by the Model Rebuildability Verification Job.

---

### BLOCK 3: LR-9 — North Star KPIs for [[BUSINESS_CONSULTANT_SKILL]] §10

**Instruction:** Insert this text at the **TOP** of the Business Consultant's §10, before all existing KPIs.

> **North Star KPIs (Primary — drive executive decision-making):**
>
> These 5 KPIs are the organization's top-level business performance indicators. All other KPIs in this section are diagnostic — they inform the North Star KPIs but do not independently drive executive decisions.
>
> 1. **Product Revenue Growth Rate:** Quarter-over-quarter revenue growth from IoT/embedded product lines. Target: set per product and market segment, reviewed annually.
> 2. **Product-Market Fit Score:** Percentage of target customers who rate the product as "must-have" or "very valuable" in quarterly customer surveys (target: ≥40%).
> 3. **Customer Lifetime Value to Customer Acquisition Cost Ratio (LTV:CAC):** Target: ≥3:1 for hardware+subscription products. LTV includes hardware margin + recurring subscription revenue over average customer lifespan; CAC includes sales, marketing, and onboarding costs.
> 4. **Gross Margin:** Per-product gross margin after BOM (Bill of Materials), manufacturing, cloud OpEx (Operational Expenditure), and support costs. Target: set per product segment per industry benchmark (typically 40–60% for hardware, 60–80% for software/subscription components).
> 5. **Time-to-Market Accuracy:** Percentage of releases that ship within the planned market window (±2 weeks of committed date). Target: ≥80%.
>
> #North-Star-KPI #business-metrics

---

### BLOCK 4: LR-10 — Business Impact Appendix for ADR Template

**Instruction:** Two insertions — (a) a new field in the Architect's ADR template at §7, and (b) a new cadence bullet in the Business Consultant's §6.2.

**(a) New field for [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]] §7 ADR template:**

In the ADR template fields listed in §7 (the list of fields that every ADR contains), add a new field **after** the existing "Consequences" field:

> - **Business Impact (if tagged #business-impact):** For ADRs with significant cost, schedule, or market-window implications. This appendix is authored by the [[BUSINESS_CONSULTANT_SKILL|Business Consultant]] per the Business-Architecture Alignment cadence (§6.2). Fields: (a) Quantified Cost Impact — one-time NRE (Non-Recurring Engineering), per-unit BOM delta, annual cloud OpEx delta, (b) Schedule Impact — market window shift in weeks, competitive milestone risk, (c) Market Impact — competitive positioning effect, customer commitment risk, pricing implication, (d) Recommendation — Proceed / Proceed with Mitigation / Escalate to Executive Review — with business rationale. The Business Impact appendix is appended to the ADR within 10 business days of the Architect's notification.

**(b) New cadence bullet for [[BUSINESS_CONSULTANT_SKILL]] §6.2:**

Add this sentence to the existing Monthly Business-Architecture Alignment bullet, or as a standalone bullet in the Cadence section:

> - **Business Impact Assessment for ADRs:** When the [[EMBEDDED_SYSTEMS_ARCHITECT_SKILL|Architect]] notifies the Business Consultant of an ADR tagged #business-impact, the Business Consultant delivers the Business Impact Assessment (using the business-impact appendix format defined in the Architect's §7 ADR template) within 10 business days of notification. #business-impact #ADR-appendix

---

### BLOCK 5: LR-11 — Accessibility Audit & Remediation Prompt Template for [[FRONTEND_DASHBOARD_ENGINEER_SKILL]] §9.4

**Instruction:** Add this as a new prompt template (next available template number) in §9.4.

> **Template [N] — Accessibility Audit & Remediation**
>
> - **Role:** Frontend/Dashboard Engineer.
> - **Goal:** Audit [DASHBOARD_VIEW/COMPONENT] for WCAG 2.1 AA compliance and remediate all findings.
> - **Inputs:**
>   - target component = [path/to/component]
>   - target user flows = [list of critical flows]
>   - known accessibility-sensitive elements = [real-time updating regions, chart widgets, alert notifications, device-management forms]
> - **Produce:**
>   1. An automated audit report using axe-core or Lighthouse accessibility scanner — include all violations, their severity, and impacted elements.
>   2. A manual keyboard-navigation test log covering all interactive elements in the target flow: Tab/Shift+Tab navigation order, Enter/Space activation, Escape dismissal, arrow key operation for chart data exploration.
>   3. A screen-reader test log (one desktop: NVDA on Windows or VoiceOver on macOS; one mobile: TalkBack on Android or VoiceOver on iOS) for all dynamically updating regions. Verify ARIA (Accessible Rich Internet Applications) live regions announce updates at correct politeness levels (polite for routine telemetry updates, assertive for critical alerts only) without overwhelming the user.
>   4. A color-contrast verification report for all text and non-text interactive elements against WCAG 2.1 AA minimum ratios (4.5:1 for normal text, 3:1 for large text, 3:1 for UI components and graphical objects).
>   5. A code diff with all remediations applied: ARIA labels and descriptions, focus management, semantic HTML corrections, color adjustments, and accessible names for all interactive elements.
> - **Constraints:** Meet WCAG 2.1 AA for ALL applicable criteria. Real-time content must use ARIA live regions with appropriate politeness levels. Chart widgets must provide keyboard-accessible alternative data views. Test with at least one actual screen reader — automated scans are necessary but insufficient. If a remediation is technically infeasible, document the limitation and propose an alternative accommodation.
>
> #accessibility #WCAG #prompt-template

---

### BLOCK 6: LR-12 — Increased BIZ↔PO Cadence During Planning and Development

**Instruction:** Append identically to **both** `[[BUSINESS_CONSULTANT_SKILL]]` §6.1 Cadence **and** `[[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL]]` §6 (the interface with Business Consultant) Cadence.

> **Co-location During Planning and Early Development:**
>
> During the Planning stage (typically 2–4 weeks per release cycle) and the first 2 weeks of the Development stage, the Business Consultant co-locates with the PO/TPM for daily stand-up participation and is available for ad hoc consultation within 2 hours during business hours. This co-location ensures: (a) market requirements are immediately clarifiable during backlog refinement, (b) business constraint changes are surfaced to sprint planning in real time, and (c) the PO/TPM can validate feature acceptance criteria against market expectations before Development commits. Outside of Planning and early Development, the standard weekly and monthly cadences apply. Co-location may be virtual (dedicated chat channel + daily 15-minute video check-in) or physical, as organizational setup permits. #co-location #BIZ-PO-cadence #Planning #Development

---

## [CONSTRAINTS]

- **Tone:** Use the exact same formal, technical, precise, and exhaustive tone as the existing SKILL.md files.
- **Wiki-links:** ALL role references MUST use Obsidian `[[wiki-link]]` syntax.
- **Tags:** ALL key concepts MUST be tagged with inline `#tag` notation as shown in each block.
- **Scope:** Do NOT add content outside the six specified blocks.
- **No commentary:** Do NOT add explanations or meta-remarks outside the delimited blocks.
- **Self-contained:** EACH block must be self-contained and ready to copy-paste directly into the target Obsidian note without formatting adjustment.
- **Dual-target blocks:** For blocks targeting TWO files (LR-12), label clearly which text goes to which file or state "append identically to both."
- **Acronyms:** DEFINE every acronym on first use within each block.
- **Brevity:** KEEP each block concise — Low-severity items should be small, precise insertions, not lengthy sections.
- **Copy-paste ready:** ENSURE all outputs can be copied and pasted directly into the target Obsidian note without any formatting adjustment.
