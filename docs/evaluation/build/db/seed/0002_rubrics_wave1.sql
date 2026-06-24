-- =============================================================================
-- Evaluation Harness — Seed: Wave-1 scoring rubrics (rubric_version = v1)
-- Spec: docs/evaluation/EVALUATION_HARNESS_SPEC.md §3.1–§3.3, §4
--
-- Calibration policy:
--   * Thresholds that the spec states numerically are encoded as AUTO_CONTINUOUS
--     (threshold + threshold_op). '>=' = higher-is-better; '<=' = lower-is-better.
--   * Pass/fail checks whose threshold the spec delegates to a role-owned SLO
--     (no number given) are AUTO_BINARY booleans — the CI tool emits the
--     pass/fail so the harness never invents an SLO number (CLAUDE.md §1, P3).
--   * HR dimensions use the 0–3 rubric (spec §4.2); pass/fail HR dims use max 1.
--
-- Idempotent: upsert on (deliverable_id, rubric_version, dimension_key).
-- =============================================================================

INSERT INTO scoring_rubrics
    (deliverable_id, rubric_version, dimension_key, dimension_label, dimension_kind,
     max_score, threshold, threshold_op, weight, tool, description) VALUES

-- ── D1-DE-1 Ingestion Pipeline (AUTO) ─────────────────────────────────────────
('D1-DE-1','v1','lint_pass','Linting pass (0 errors)','AUTO_BINARY',1.0,NULL,NULL,1.0,'ruff/flake8','flake8/ruff report 0 errors'),
('D1-DE-1','v1','dag_import','DAG import success','AUTO_BINARY',1.0,NULL,NULL,1.0,'airflow','DAG imports without error'),
('D1-DE-1','v1','unit_test_pass_rate','Unit test pass rate ≥90%','AUTO_CONTINUOUS',1.0,90,'>=',1.0,'pytest','percent of unit tests passing'),
('D1-DE-1','v1','schema_validation','Schema validation vs contract','AUTO_BINARY',1.0,NULL,NULL,1.0,'great_expectations','pass/fail against contract schema'),
('D1-DE-1','v1','p99_latency_slo_met','P99 ingestion latency within SLO','AUTO_BINARY',1.0,NULL,NULL,1.0,'custom','CI emits pass/fail vs role SLO'),

-- ── D1-DE-2 Data-Quality Report (HYB 70/30) ───────────────────────────────────
('D1-DE-2','v1','required_sections_present','All required sections present','AUTO_BINARY',1.0,NULL,NULL,1.0,'md_parser','completeness%, accuracy%, timeliness%, dedup rate, schema conformance%'),
('D1-DE-2','v1','slo_thresholds_flagged','SLO breaches flagged correctly','AUTO_BINARY',1.0,NULL,NULL,1.0,'threshold_check','values vs SLO thresholds flagged correctly'),
('D1-DE-2','v1','rca_clarity','Root-cause analysis clarity','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 clarity of RCA for any SLO breach'),
('D1-DE-2','v1','findings_actionability','Actionability of findings','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 actionability of findings'),

-- ── D1-DE-3 ETL/ELT + Feature Pipeline (AUTO) ─────────────────────────────────
('D1-DE-3','v1','dag_execution_success','DAG execution success','AUTO_BINARY',1.0,NULL,NULL,1.0,'airflow','DAG runs to success'),
('D1-DE-3','v1','output_schema_match','Output schema matches downstream contract','AUTO_BINARY',1.0,NULL,NULL,1.0,'great_expectations','schema match vs downstream contract'),
('D1-DE-3','v1','unit_test_coverage','Unit test coverage ≥80%','AUTO_CONTINUOUS',1.0,80,'>=',1.0,'pytest-cov','line coverage percent'),
('D1-DE-3','v1','no_data_loss','No data-loss events (count in==out)','AUTO_BINARY',1.0,NULL,NULL,1.0,'custom','sample count in == count out ±expected'),
('D1-DE-3','v1','feature_dist_in_bounds','Feature distribution within bounds (KS p>0.05)','AUTO_BINARY',1.0,NULL,NULL,1.0,'scipy_ks','KS test p>0.05 vs expected'),

-- ── D1-DE-4 Curated/Labeled Dataset (AUTO) ────────────────────────────────────
('D1-DE-4','v1','schema_compliance','Schema compliance (cols/types)','AUTO_BINARY',1.0,NULL,NULL,1.0,'schema_checker','all required columns present, correct types'),
('D1-DE-4','v1','completeness_rate','Completeness ≥99%','AUTO_CONTINUOUS',1.0,99,'>=',1.0,'pandas_profiling','non-null rate per required field'),
('D1-DE-4','v1','dedup_acceptable','Deduplication within contract threshold','AUTO_BINARY',1.0,NULL,NULL,1.0,'custom','duplicate records / total within dataset-contract threshold'),
('D1-DE-4','v1','label_coverage_acceptable','Label coverage within target','AUTO_BINARY',1.0,NULL,NULL,1.0,'custom','labeled / total within target'),
('D1-DE-4','v1','dvc_version_lineage','DVC version tag + lineage pointer','AUTO_BINARY',1.0,NULL,NULL,1.0,'dvc','DVC version tag present with lineage pointer'),

-- ── D1-DE-5 Data Catalog + Lineage Record (HYB 60/40) ─────────────────────────
('D1-DE-5','v1','datasets_registered_pct','Datasets registered (coverage %)','AUTO_CONTINUOUS',1.0,100,'>=',1.0,'catalog_check','% of datasets registered'),
('D1-DE-5','v1','lineage_pointer_present','Lineage pointer present per dataset','AUTO_BINARY',1.0,NULL,NULL,1.0,'catalog_check','lineage pointer present'),
('D1-DE-5','v1','schema_version_recorded','Schema version recorded','AUTO_BINARY',1.0,NULL,NULL,1.0,'catalog_check','schema version recorded'),
('D1-DE-5','v1','lineage_accuracy','Lineage accuracy (spot-check)','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 lineage accuracy on 5-record spot-check'),
('D1-DE-5','v1','discoverability','Discoverability of entries','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 discoverability'),

-- ── D1-FE-1 Fleet Monitoring Dashboard (AUTO) ─────────────────────────────────
('D1-FE-1','v1','lighthouse_perf','Lighthouse Performance ≥85','AUTO_CONTINUOUS',1.0,85,'>=',1.0,'lighthouse','performance score'),
('D1-FE-1','v1','lighthouse_a11y','Lighthouse Accessibility ≥90','AUTO_CONTINUOUS',1.0,90,'>=',1.0,'lighthouse','accessibility score'),
('D1-FE-1','v1','cwv_lcp','Core Web Vitals LCP ≤2.5 s','AUTO_CONTINUOUS',1.0,2.5,'<=',0.334,'lighthouse','largest contentful paint, seconds'),
('D1-FE-1','v1','cwv_cls','Core Web Vitals CLS ≤0.1','AUTO_CONTINUOUS',1.0,0.1,'<=',0.333,'lighthouse','cumulative layout shift'),
('D1-FE-1','v1','cwv_fid','Core Web Vitals FID ≤100 ms','AUTO_CONTINUOUS',1.0,100,'<=',0.333,'lighthouse','first input delay, ms'),
('D1-FE-1','v1','ts_build_zero_errors','TypeScript build 0 errors','AUTO_BINARY',1.0,NULL,NULL,1.0,'tsc','tsc reports 0 errors'),
('D1-FE-1','v1','jest_pass_rate','Jest unit test pass rate ≥90%','AUTO_CONTINUOUS',1.0,90,'>=',1.0,'jest','percent of unit tests passing'),

-- ── D1-FE-2 Real-Time Data Client Module (AUTO) ───────────────────────────────
('D1-FE-2','v1','ts_strict_zero_errors','TypeScript strict-mode 0 errors','AUTO_BINARY',1.0,NULL,NULL,1.0,'tsc','tsc --strict 0 errors'),
('D1-FE-2','v1','unit_test_coverage','Unit test coverage ≥85%','AUTO_CONTINUOUS',1.0,85,'>=',1.0,'jest-coverage','line coverage percent'),
('D1-FE-2','v1','e2e_reconnect_pass','E2E reconnection test passes','AUTO_BINARY',1.0,NULL,NULL,1.0,'playwright','drop → reconnect within 5 s'),
('D1-FE-2','v1','msg_roundtrip_parity','Message-parsing round-trip parity','AUTO_CONTINUOUS',1.0,100,'>=',1.0,'custom','% schema parity on round-trip'),
('D1-FE-2','v1','eslint_zero_errors','ESLint 0 errors','AUTO_BINARY',1.0,NULL,NULL,1.0,'eslint','eslint reports 0 errors'),

-- ── D1-FE-3 Frontend Test Suite (HYB 70/30) ───────────────────────────────────
('D1-FE-3','v1','all_tests_pass','All tests pass (0 failures)','AUTO_BINARY',1.0,NULL,NULL,1.0,'jest','0 failures'),
('D1-FE-3','v1','line_coverage','Line coverage ≥80%','AUTO_CONTINUOUS',1.0,80,'>=',1.0,'jest-coverage','line coverage percent'),
('D1-FE-3','v1','e2e_scenario_coverage','E2E scenario coverage (%)','AUTO_CONTINUOUS',1.0,100,'>=',1.0,'playwright','% of acceptance-criteria flows covered'),
('D1-FE-3','v1','test_quality','Test quality (edge cases)','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 are edge cases meaningfully covered'),
('D1-FE-3','v1','test_maintainability','Test maintainability','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 clear structure, no brittle selectors'),

-- ── D1-FE-4 Component Library / Design System (AUTO) ──────────────────────────
('D1-FE-4','v1','storybook_build','Storybook build success','AUTO_BINARY',1.0,NULL,NULL,1.0,'storybook','0 build errors'),
('D1-FE-4','v1','each_component_has_story','Each exported component has ≥1 story','AUTO_BINARY',1.0,NULL,NULL,1.0,'storybook','≥1 story per exported component'),
('D1-FE-4','v1','axe_zero_critical','axe-core 0 critical/serious','AUTO_BINARY',1.0,NULL,NULL,1.0,'axe-storybook','0 critical/serious a11y violations'),
('D1-FE-4','v1','ts_types_no_any','TS types exported, 0 any in public API','AUTO_BINARY',1.0,NULL,NULL,1.0,'tsc','no any in public API'),
('D1-FE-4','v1','npm_publish_ok','npm package publishes without error','AUTO_BINARY',1.0,NULL,NULL,1.0,'npm','publish dry-run succeeds'),

-- ── D1-FE-5 API/Streaming Contract Requirement Spec (HR) ──────────────────────
('D1-FE-5','v1','endpoint_coverage','All required endpoints described','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 completeness vs API surface (incl. update-freq, latency, breaking-change process)'),
('D1-FE-5','v1','payload_specificity','Payload shapes fully specified','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 specificity of payload shapes (no TBD)'),
('D1-FE-5','v1','counterpart_acceptance','Accepted by Backend/Cloud Engineer','HR_PASS_FAIL',1.0,NULL,NULL,1.0,NULL,'pass/fail acceptance by counterpart'),

-- ── D1-ML-1 Automated Training/Deployment Pipeline (AUTO) ─────────────────────
('D1-ML-1','v1','e2e_no_manual','Executes end-to-end, no manual step','AUTO_BINARY',1.0,NULL,NULL,1.0,'ci','pipeline runs without manual intervention'),
('D1-ML-1','v1','all_stage_tests_pass','All stage tests pass','AUTO_BINARY',1.0,NULL,NULL,1.0,'ci','0 failures across stages'),
('D1-ML-1','v1','artifact_signing_present','Artifact signing step present + passes','AUTO_BINARY',1.0,NULL,NULL,1.0,'signing_verifier','signing step present and passes'),
('D1-ML-1','v1','pipeline_lint','Pipeline lint (YAML schema)','AUTO_BINARY',1.0,NULL,NULL,1.0,'yaml-lint','0 lint errors'),
('D1-ML-1','v1','rollback_trigger_test','Rollback invoked on injected failure','AUTO_BINARY',1.0,NULL,NULL,1.0,'ci','rollback triggers correctly'),

-- ── D1-ML-2 Model Registry Entry (AUTO) ───────────────────────────────────────
('D1-ML-2','v1','required_metadata_complete','Required metadata fields populated','AUTO_BINARY',1.0,NULL,NULL,1.0,'mlflow','version, data version, commit SHA, hyperparams, metrics, date'),
('D1-ML-2','v1','lineage_chain_complete','Lineage chain complete','AUTO_BINARY',1.0,NULL,NULL,1.0,'lineage_validator','data DVC ref → code Git ref → artifact'),
('D1-ML-2','v1','stage_tag_correct','Stage tag set correctly','AUTO_BINARY',1.0,NULL,NULL,1.0,'mlflow','Staging/Production tag set'),
('D1-ML-2','v1','artifact_uri_valid','Artifact URI valid + present','AUTO_BINARY',1.0,NULL,NULL,1.0,'mlflow','artifact resolves and present'),
('D1-ML-2','v1','drift_spec_linked','Drift-monitoring spec linked','AUTO_BINARY',1.0,NULL,NULL,1.0,'mlflow','drift spec linked'),

-- ── D1-ML-3 Drift-Monitoring Dashboard + Alerting Config (HYB 75/25) ──────────
('D1-ML-3','v1','grafana_json_valid','Grafana config valid JSON','AUTO_BINARY',1.0,NULL,NULL,1.0,'grafana-validator','0 parse errors'),
('D1-ML-3','v1','required_panels_present','All required panels present','AUTO_BINARY',1.0,NULL,NULL,1.0,'grafana-validator','feature/label/prediction drift + model latency'),
('D1-ML-3','v1','alert_rules_syntax_valid','Alert rules syntax valid','AUTO_BINARY',1.0,NULL,NULL,1.0,'alertmanager','config check passes'),
('D1-ML-3','v1','alert_fires_injected','Alert fires on injected drift signal','AUTO_BINARY',1.0,NULL,NULL,1.0,'integration_test','alert fires on injected drift'),
('D1-ML-3','v1','alert_threshold_appropriateness','Alert threshold appropriateness','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 threshold appropriateness'),

-- ── D1-ML-4 OTA-Ready Model Artifact (AUTO, schema:OCM) ───────────────────────
-- Scored by the full OCM validator; raw_value = % of V-OCM-01..16 rules passed.
('D1-ML-4','v1','ocm_v_rules','OCM schema validation (V-OCM-01..16)','AUTO_CONTINUOUS',1.0,100,'>=',1.0,'ocm_validator','percent of OCM validation rules passing; FAIL flash/ram budget = hard block'),

-- ── D1-ML-5 Reproducibility/Audit (Lineage) Report (HYB 70/30) ────────────────
('D1-ML-5','v1','binary_identical_rebuild','Binary-identical rebuild (SHA-256 match)','AUTO_BINARY',1.0,NULL,NULL,1.0,'reproducibility_ci','clean rebuild SHA-256 match'),
('D1-ML-5','v1','lineage_fields_present','All required lineage fields present','AUTO_BINARY',1.0,NULL,NULL,1.0,'section_parser','data version, code version, hyperparams, env hash'),
('D1-ML-5','v1','generated_within_24h','Report generated within 24 h of registration','AUTO_BINARY',1.0,NULL,NULL,1.0,'custom','generated within 24 h'),
('D1-ML-5','v1','audit_trail_clarity','Audit trail clarity for third party','HR_RUBRIC',3.0,NULL,NULL,1.0,NULL,'0–3 clarity of audit trail for a third party')

ON CONFLICT (deliverable_id, rubric_version, dimension_key) DO UPDATE
    SET dimension_label = EXCLUDED.dimension_label,
        dimension_kind  = EXCLUDED.dimension_kind,
        max_score       = EXCLUDED.max_score,
        threshold       = EXCLUDED.threshold,
        threshold_op    = EXCLUDED.threshold_op,
        weight          = EXCLUDED.weight,
        tool            = EXCLUDED.tool,
        description     = EXCLUDED.description,
        active          = TRUE;
