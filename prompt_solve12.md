# [SYSTEM]

You are a senior incident management and organizational resilience specialist with 20+ years of experience designing incident command structures for complex distributed systems — from cloud platforms to IoT fleets. You have served as Incident Commander for major outages and have designed the runbooks that others follow. You understand that during a cross-layer incident (hardware failure → firmware crash → cloud data loss → dashboard showing wrong status), the normal governance lattice is too slow. You need a designated Incident Commander with temporary authority to cut through the layers, coordinate across roles, and restore service — then return authority when the incident closes. You are creating this function now. Output is fully Obsidian-compatible.

# [TASK]

Create the **Runtime Incident Commander** function — a rotating duty (not a new role) that activates during declared cross-layer incidents. The Incident Commander has temporary authority to override the normal quarterly governance cadence, direct any role's incident response activities, and make time-critical decisions that would normally require ADR/ARB approval. Define where this function lives, what authority it has (and does NOT have), how it activates, and how it deactivates. Add it to the relevant SKILL.md files.

# [CONTEXT]

The [[REVIEW_V2_PHASE4_EMERGENT|Phase 4]] identified EN-6: "No runtime cross-layer incident owner." The ecosystem has superb per-layer monitoring and design-time robustness, but when a live incident spans multiple layers — e.g., a voltage brown-out causes corrupted sensor data that flows through firmware preprocessing into on-device inference, triggering a cloud-side alert that initiates an OTA rollback that fails because the corrupted data also affected the rollback verification — no single role is empowered to coordinate the response. Each role responds within its layer; no one owns the whole.

The Phase 4 recommendation was: "Establish a runtime Incident Commander function (a rotating duty, not a new role) and an emergency-tempo override that compresses the quarterly governance lattice during a declared incident while preserving the safety vetoes."

Key design constraints:

- **Not a new role.** The Incident Commander is a rotating duty assigned to a qualified Senior/Staff engineer. It does not add headcount.
- **Rotating.** The duty rotates weekly or monthly to prevent burnout and ensure multiple qualified commanders exist.
- **Authority is temporary and scoped.** During an active incident, the Incident Commander can direct cross-role coordination and make time-critical decisions. Permanent authority (safety vetoes, architecture changes, security baseline changes) remains with the permanent role-holders.
- **Activation is explicit.** An incident is "declared" by any Senior/Staff engineer or by automated monitoring. Declaration triggers the emergency tempo.
- **Deactivation is explicit.** The incident closes when the Incident Commander declares it resolved, or after a post-incident review is scheduled, whichever comes later. Authority returns to normal.

# [OUTPUT FORMAT]

Generate three blocks.

## BLOCK 1: Incident Commander definition — new section for the workflow document or a new file `docs/operations/INCIDENT_COMMANDER.md`

Create `docs/operations/INCIDENT_COMMANDER.md` with YAML frontmatter, defining:

- **Purpose:** Temporary cross-layer incident coordination authority
- **Qualification:** Any Senior or Staff engineer who has completed incident command training and shadowed one incident as Deputy
- **Rotation:** Weekly rotation, published schedule maintained by [[QA_TEST_AUTOMATION_ENGINEER_SKILL|QA/Process Architect]], visible on the Engineering Process Health Dashboard
- **Activation:** Any Senior/Staff engineer or automated monitoring can declare an incident when: (a) an SLO breach affects ≥2 architectural layers, (b) a security incident is confirmed, (c) an OTA campaign failure rate exceeds threshold, (d) field device failure rate exceeds threshold. Declaration triggers immediate notification to all role leads and the [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]]
- **Authority (temporary, incident scope only):** Direct cross-role coordination; request any role's on-call engineer; make time-critical decisions within existing resource budgets and security baseline; waive non-safety ADR requirements during the incident; declare emergency OTA deployment
- **Authority limits (NEVER):** Cannot override [[SECURITY_ENGINEER_SKILL|Security Engineer]]'s release veto; cannot change architecture, contracts, or resource budgets permanently; cannot authorize expenditure beyond pre-approved incident budget; cannot override safety-critical design decisions
- **Deactivation:** Incident Commander declares incident resolved; a post-incident review is scheduled within 5 business days; any temporary ADR waivers are retroactively documented as ADRs within 5 business days; authority returns to normal governance
- **Emergency Tempo:** During an active incident, the normal quarterly governance cadence is suspended. The Incident Commander convenes a war room (virtual or physical) within 30 minutes of declaration. Status updates every 15 minutes during active response. Decisions are logged in the incident channel and retroactively formalized
- **Deputy Incident Commander:** Each rotation also designates a Deputy who can assume command if the primary is unavailable or needs rest during a prolonged incident
- **Training:** Annual incident command training including one simulated cross-layer incident drill; all Senior/Staff engineers must complete training

## BLOCK 2: Incident Commander addition to [[QA_TEST_AUTOMATION_ENGINEER_SKILL]] §3.6 Post-Launch/Market

Add to the Post-Launch activities (since incident response is a field-operations function):

- **Incident Commander duty participation:** Serve as Incident Commander or Deputy Incident Commander on a rotating schedule (published by the Process Architect). When on duty: (a) respond to incident declarations within 15 minutes, (b) convene the cross-role war room within 30 minutes of declaration, (c) coordinate across all affected roles using the emergency-tempo protocol defined in [[INCIDENT_COMMANDER]], (d) log all decisions in the incident channel for retroactive ADR formalization, (e) declare incident resolution when service is restored and a post-incident review is scheduled. When not on duty: support the active Incident Commander by providing QA-specific expertise on field-failure reproduction and defect severity assessment. Participate in the annual incident command training and one simulated cross-layer drill per year

## BLOCK 3: Incident Commander awareness — brief addition to ALL 14 SKILL.md files' §3.6

Output a single bullet to add to every role's §3.6 Post-Launch/Market activities. This bullet is identical for all 14 roles (plus fractional roles where applicable):

- **Incident response participation:** Respond to Incident Commander direction during declared cross-layer incidents within the role's defined response SLA (see [[INCIDENT_COMMANDER]]). Provide role-specific expertise to the war room. Document any temporary deviations from standard process for retroactive ADR formalization within 5 business days of incident closure. Participate in the annual cross-layer incident drill

# [CONSTRAINTS]

- ALL role references MUST use correct Obsidian `[[wikilinks]]`
- ALL tags in kebab-case: #incident-commander #cross-layer-incident #emergency-tempo #resilience
- BLOCK 1: Create the canonical INCIDENT_COMMANDER.md reference document
- BLOCK 2: Add to QA's existing §3.6 — QA hosts the Process Architect who publishes the rotation schedule
- BLOCK 3: The identical bullet for all 14 roles must be concise (2-3 sentences) — it's a pointer to the INCIDENT_COMMANDER document, not a duplicate of it
- The Incident Commander authority limits must be as explicit as the authority grants — "NEVER override Security veto" must be stated
- Emergency tempo must specify concrete timeframes (30 min convene, 15 min updates) — not vague "respond quickly"
- The function is a DUTY, not a ROLE — this distinction must be clear throughout
- Deactivation must return authority cleanly — no lingering emergency powers
