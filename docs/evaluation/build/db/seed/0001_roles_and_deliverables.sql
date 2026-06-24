-- =============================================================================
-- Evaluation Harness — Seed: roles + Wave-1 deliverables
-- Spec: docs/evaluation/EVALUATION_HARNESS_SPEC.md §3.1–§3.3, Appendix A
--
-- All 14 primary roles are seeded (the harness is wave-extensible), but only
-- Wave-1 deliverables (DATA, FE, MLOPS) are seeded for the initial build, per
-- the task constraint. Adding a later wave = adding rows here + rubrics in
-- 0002_rubrics_wave1.sql; no code change required.
--
-- Idempotent: upsert semantics via ON CONFLICT.
-- =============================================================================

INSERT INTO roles (role_code, display_name, skill_doc, wave) VALUES
    ('DATA',  'Data Engineer',                         'DATA_ENGINEER_SKILL',                       1),
    ('FE',    'Frontend/Dashboard Engineer',           'FRONTEND_DASHBOARD_ENGINEER_SKILL',         1),
    ('MLOPS', 'MLOps Engineer',                         'MLOPS_ENGINEER_SKILL',                      1),
    ('FW',    'Firmware Engineer',                      'FIRMWARE_ENGINEER_SKILL',                   2),
    ('BACK',  'Backend/Cloud Engineer',                 'BACKEND_CLOUD_ENGINEER_SKILL',              2),
    ('DEVOPS','DevOps/Platform Engineer',               'DEVOPS_PLATFORM_ENGINEER_SKILL',            2),
    ('HW',    'Hardware Engineer',                      'HARDWARE_ENGINEER_SKILL',                   3),
    ('ML',    'Edge AI/ML Engineer',                    'EDGE_AI_ML_ENGINEER_SKILL',                 3),
    ('QA',    'QA & Test Automation Engineer',          'QA_TEST_AUTOMATION_ENGINEER_SKILL',         3),
    ('RES',   'IoT & Embedded Systems Researcher',      'IOT_EMBEDDED_SYSTEMS_RESEARCHER_SKILL',     4),
    ('SEC',   'Security Engineer',                      'SECURITY_ENGINEER_SKILL',                   4),
    ('ARCH',  'Embedded Systems Architect',             'EMBEDDED_SYSTEMS_ARCHITECT_SKILL',          4),
    ('BIZ',   'Business Consultant',                    'BUSINESS_CONSULTANT_SKILL',                 4),
    ('PO',    'Product Owner / Technical Project Manager','PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL', 4)
ON CONFLICT (role_code) DO UPDATE
    SET display_name = EXCLUDED.display_name,
        skill_doc    = EXCLUDED.skill_doc,
        wave         = EXCLUDED.wave;

-- ── Wave 1 deliverables ───────────────────────────────────────────────────────
-- composite_weight = role-level weight from the spec's "Composite score formula".
-- auto_weight/hr_weight: AUTO=1/0, HR=0/1. For HYB, the spec §3.1–§3.3 enumerates
-- AUTO and HR sub-metrics but does not state a numeric split; the splits below are
-- build-time calibrated defaults flagged for TSC ratification per spec §10.1
-- (recorded in calibration_note). They can be changed by UPDATE without code change.

INSERT INTO deliverables
    (deliverable_id, role_code, name, scoring_type, auto_weight, hr_weight,
     composite_weight, min_sample, schema_ref, scorer_key, calibration_note) VALUES
    -- Data Engineer (DATA) — composite D1=20 D2=20 D3=25 D4=25 D5=10
    ('D1-DE-1','DATA','Ingestion Pipeline',                'AUTO',1.00,0.00,0.20,30,NULL,'metrics_manifest',NULL),
    ('D1-DE-2','DATA','Data-Quality Report',               'HYB', 0.70,0.30,0.20,30,NULL,'metrics_manifest','AUTO/HR split 70/30 = build-time default, pending TSC ratification (spec §10.1).'),
    ('D1-DE-3','DATA','ETL/ELT + Feature Pipeline',        'AUTO',1.00,0.00,0.25,30,NULL,'metrics_manifest',NULL),
    ('D1-DE-4','DATA','Curated/Labeled Dataset',           'AUTO',1.00,0.00,0.25,30,NULL,'metrics_manifest',NULL),
    ('D1-DE-5','DATA','Data Catalog + Lineage Record',     'HYB', 0.60,0.40,0.10,30,NULL,'metrics_manifest','AUTO/HR split 60/40 = build-time default, pending TSC ratification (spec §10.1).'),
    -- Frontend/Dashboard Engineer (FE) — composite D1=25 D2=20 D3=20 D4=20 D5=15
    ('D1-FE-1','FE','Fleet Monitoring Dashboard',          'AUTO',1.00,0.00,0.25,30,NULL,'metrics_manifest',NULL),
    ('D1-FE-2','FE','Real-Time Data Client Module',        'AUTO',1.00,0.00,0.20,30,NULL,'metrics_manifest',NULL),
    ('D1-FE-3','FE','Frontend Test Suite',                 'HYB', 0.70,0.30,0.20,30,NULL,'metrics_manifest','AUTO/HR split 70/30 = build-time default, pending TSC ratification (spec §10.1).'),
    ('D1-FE-4','FE','Component Library / Design System',   'AUTO',1.00,0.00,0.20,30,NULL,'metrics_manifest',NULL),
    ('D1-FE-5','FE','API/Streaming Contract Requirement Spec','HR',0.00,1.00,0.15,30,NULL,'human_review_only',NULL),
    -- MLOps Engineer (MLOPS) — composite D1=25 D2=20 D3=20 D4=25 D5=10
    ('D1-ML-1','MLOPS','Automated Training/Deployment Pipeline','AUTO',1.00,0.00,0.25,30,NULL,'metrics_manifest',NULL),
    ('D1-ML-2','MLOPS','Model Registry Entry',             'AUTO',1.00,0.00,0.20,30,NULL,'metrics_manifest',NULL),
    ('D1-ML-3','MLOPS','Drift-Monitoring Dashboard + Alerting Config','HYB',0.75,0.25,0.20,30,NULL,'metrics_manifest','AUTO/HR split 75/25 = build-time default, pending TSC ratification (spec §10.1).'),
    ('D1-ML-4','MLOPS','OTA-Ready Model Artifact',         'AUTO',1.00,0.00,0.25,30,'OCM','schema:OCM','Scored by the full OCM validator (V-OCM-01..16), a superset of the 5 metrics in spec §3.3.'),
    ('D1-ML-5','MLOPS','Reproducibility/Audit (Lineage) Report','HYB',0.70,0.30,0.10,30,NULL,'metrics_manifest','AUTO/HR split 70/30 = build-time default, pending TSC ratification (spec §10.1).')
ON CONFLICT (deliverable_id) DO UPDATE
    SET role_code        = EXCLUDED.role_code,
        name             = EXCLUDED.name,
        scoring_type     = EXCLUDED.scoring_type,
        auto_weight      = EXCLUDED.auto_weight,
        hr_weight        = EXCLUDED.hr_weight,
        composite_weight = EXCLUDED.composite_weight,
        min_sample       = EXCLUDED.min_sample,
        schema_ref       = EXCLUDED.schema_ref,
        scorer_key       = EXCLUDED.scorer_key,
        calibration_note = EXCLUDED.calibration_note,
        active           = TRUE;

-- Composite-weight sanity check: each Wave-1 role's deliverable weights sum to 1.0.
DO $$
DECLARE r RECORD;
BEGIN
    FOR r IN
        SELECT role_code, ROUND(SUM(composite_weight),3) AS s
        FROM deliverables WHERE role_code IN ('DATA','FE','MLOPS')
        GROUP BY role_code
    LOOP
        IF abs(r.s - 1.000) > 0.001 THEN
            RAISE EXCEPTION 'Composite weights for role % sum to % (expected 1.000)', r.role_code, r.s;
        END IF;
    END LOOP;
END $$;
