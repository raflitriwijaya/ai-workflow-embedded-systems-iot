-- =============================================================================
-- Evaluation Harness — Reporting Views & Helper Functions
-- Migration: 0002_views_and_functions
-- These views back the Grafana dashboard (spec §8.1 DASH-1..10) and the
-- Wave Activation Gates (spec §7.2 WG-1..3). All are read-only projections.
-- =============================================================================

-- Optional: convert the two high-churn score tables to TimescaleDB hypertables
-- for efficient time-series trend queries (spec §2.2). Guarded so the migration
-- succeeds on a vanilla PostgreSQL instance without the extension.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'timescaledb') THEN
        CREATE EXTENSION IF NOT EXISTS timescaledb;
        -- create_hypertable is idempotent with if_not_exists => TRUE
        PERFORM create_hypertable('agent_results', 'captured_at',
                                  if_not_exists => TRUE, migrate_data => TRUE);
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'TimescaleDB not enabled (%): continuing on vanilla PostgreSQL', SQLERRM;
END $$;

-- ── DASH-2 / WG-1: baseline sample progress toward the ≥30 threshold ──────────
CREATE OR REPLACE VIEW v_sample_progress AS
SELECT
    d.role_code,
    d.deliverable_id,
    d.name                         AS deliverable_name,
    d.min_sample,
    COALESCE(b.n, 0)               AS baseline_n,
    (COALESCE(b.n, 0) >= d.min_sample) AS threshold_met
FROM deliverables d
LEFT JOIN (
    SELECT role_code, deliverable_id, COUNT(*) AS n
    FROM human_baselines
    GROUP BY role_code, deliverable_id
) b USING (role_code, deliverable_id)
WHERE d.active;

-- ── DASH-3 / HG-5: human baseline statistics (mean, sd, percentiles) ──────────
CREATE OR REPLACE VIEW v_baseline_stats AS
SELECT
    role_code,
    deliverable_id,
    rubric_version,
    COUNT(*)                                              AS n,
    ROUND(AVG(composite_score)::numeric, 3)               AS mean,
    ROUND(COALESCE(STDDEV_SAMP(composite_score), 0)::numeric, 3) AS sd,
    ROUND(percentile_cont(0.25) WITHIN GROUP (ORDER BY composite_score)::numeric, 3) AS p25,
    ROUND(percentile_cont(0.50) WITHIN GROUP (ORDER BY composite_score)::numeric, 3) AS median,
    ROUND(percentile_cont(0.75) WITHIN GROUP (ORDER BY composite_score)::numeric, 3) AS p75,
    ROUND(percentile_cont(0.95) WITHIN GROUP (ORDER BY composite_score)::numeric, 3) AS p95,
    ROUND(MIN(composite_score)::numeric, 3)               AS min_score,
    ROUND(MAX(composite_score)::numeric, 3)               AS max_score
FROM human_baselines
GROUP BY role_code, deliverable_id, rubric_version;

-- ── DASH-5 / G2 / G3: draft-acceptance rate (rolling 90 days) ─────────────────
CREATE OR REPLACE VIEW v_draft_acceptance_role AS
SELECT
    role_code,
    COUNT(*)                                                          AS submissions_90d,
    SUM(CASE WHEN draft_accepted THEN 1 ELSE 0 END)                   AS draft_accepted_90d,
    ROUND( SUM(CASE WHEN draft_accepted THEN 1 ELSE 0 END)::numeric
           / NULLIF(COUNT(*), 0), 4)                                  AS draft_acceptance_rate
FROM agent_results
WHERE captured_at >= now() - INTERVAL '90 days'
GROUP BY role_code;

CREATE OR REPLACE VIEW v_draft_acceptance_org AS
SELECT
    COUNT(*)                                                          AS submissions_90d,
    ROUND( SUM(CASE WHEN draft_accepted THEN 1 ELSE 0 END)::numeric
           / NULLIF(COUNT(*), 0), 4)                                  AS org_draft_acceptance_rate
FROM agent_results
WHERE captured_at >= now() - INTERVAL '90 days';

-- ── DASH-6: human edit-required breakdown per role ────────────────────────────
CREATE OR REPLACE VIEW v_edit_breakdown AS
SELECT
    role_code,
    SUM(CASE WHEN human_accepted AND NOT human_edit_required THEN 1 ELSE 0 END) AS accepted_as_is,
    SUM(CASE WHEN human_accepted AND human_edit_required THEN 1 ELSE 0 END)     AS accepted_with_edit,
    SUM(CASE WHEN NOT human_accepted THEN 1 ELSE 0 END)                         AS rejected,
    COUNT(*)                                                                    AS total
FROM agent_results
WHERE captured_at >= now() - INTERVAL '90 days'
GROUP BY role_code;

-- ── DASH-1 / WG-1 / WG-2: wave activation gate status ─────────────────────────
-- A wave is sample-ready when every active deliverable for every role in the
-- wave has ≥ min_sample baselines (WG-1) AND the baseline report is accepted (WG-2).
CREATE OR REPLACE VIEW v_wave_gate_status AS
WITH per_deliverable AS (
    SELECT
        r.wave,
        sp.role_code,
        sp.deliverable_id,
        sp.threshold_met,
        COALESCE(rr.baseline_status = 'TSC_ACCEPTED', FALSE) AS report_accepted
    FROM v_sample_progress sp
    JOIN roles r ON r.role_code = sp.role_code
    LEFT JOIN LATERAL (
        SELECT baseline_status
        FROM role_readiness
        WHERE role_readiness.role_code = sp.role_code
          AND role_readiness.deliverable_id = sp.deliverable_id
        ORDER BY computed_at DESC
        LIMIT 1
    ) rr ON TRUE
)
SELECT
    wave,
    bool_and(threshold_met)                       AS wg1_all_samples_met,
    bool_and(report_accepted)                     AS wg2_all_reports_accepted,
    COUNT(*)                                       AS deliverables_in_wave,
    SUM(CASE WHEN threshold_met THEN 1 ELSE 0 END) AS deliverables_at_threshold
FROM per_deliverable
GROUP BY wave;

-- ── DASH-4 / G1: latest agent-vs-baseline readiness per role×deliverable ──────
CREATE OR REPLACE VIEW v_role_readiness_latest AS
SELECT DISTINCT ON (role_code, deliverable_id, rubric_version)
    role_code, deliverable_id, rubric_version,
    baseline_n, baseline_mean, baseline_sd, baseline_p25, baseline_p75, baseline_p95,
    baseline_status, temporal_stability_flag,
    agent_n, agent_mean, welch_t, welch_p,
    draft_acceptance_rate, harness_alignment_r,
    sample_threshold_met, readiness, computed_at
FROM role_readiness
ORDER BY role_code, deliverable_id, rubric_version, computed_at DESC;

-- ── DASH-8: agent-attributable safety/security incident counters ──────────────
CREATE OR REPLACE VIEW v_incident_counts AS
SELECT
    incident_class,
    COUNT(*) AS total,
    SUM(CASE WHEN occurred_at >= now() - INTERVAL '90 days' THEN 1 ELSE 0 END) AS last_90d
FROM incidents
GROUP BY incident_class;

-- ── Helper: assert a deliverable's rubric weights are internally consistent ────
-- Returns rows for any deliverable whose AUTO/HR rubric dimension weights do not
-- sum to a positive number (used by the smoke test, spec §9.1 "smoke-tested").
CREATE OR REPLACE FUNCTION fn_rubric_integrity_issues()
RETURNS TABLE (deliverable_id TEXT, issue TEXT) AS $$
    SELECT d.deliverable_id, 'no active AUTO dimensions for AUTO/HYB deliverable'
    FROM deliverables d
    WHERE d.active AND d.scoring_type IN ('AUTO','HYB')
      AND NOT EXISTS (
        SELECT 1 FROM scoring_rubrics sr
        WHERE sr.deliverable_id = d.deliverable_id AND sr.active
          AND sr.dimension_kind IN ('AUTO_BINARY','AUTO_CONTINUOUS'))
    UNION ALL
    SELECT d.deliverable_id, 'no active HR dimensions for HR/HYB deliverable'
    FROM deliverables d
    WHERE d.active AND d.scoring_type IN ('HR','HYB')
      AND NOT EXISTS (
        SELECT 1 FROM scoring_rubrics sr
        WHERE sr.deliverable_id = d.deliverable_id AND sr.active
          AND sr.dimension_kind IN ('HR_RUBRIC','HR_PASS_FAIL'));
$$ LANGUAGE sql STABLE;
