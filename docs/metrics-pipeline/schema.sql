-- Engineering Metrics Pipeline — Database Schema
-- Targets: InfluxDB (time-series) via SQL-like DDL comments + PostgreSQL (dimensional)
-- Retention: raw data 12 months, aggregated 36 months
-- Tags: #engineering-metrics-pipeline #build #process-health

-- ============================================================
-- POSTGRESQL — Dimensional / Reference Data
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- ----------------------------------------------------------------
-- Lookup / dimension tables
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS adr_tiers (
    tier_id        SMALLINT PRIMARY KEY,
    tier_name      VARCHAR(32)  NOT NULL,
    description    TEXT,
    target_hours   NUMERIC(6,1) NOT NULL,   -- SLA target in hours
    warning_factor NUMERIC(4,2) NOT NULL DEFAULT 1.5  -- yellow threshold multiplier
);

INSERT INTO adr_tiers (tier_id, tier_name, target_hours, description, warning_factor) VALUES
    (1, 'Tier 1', 4,    'Operational / hot-fix decisions', 1.5),
    (2, 'Tier 2', 48,   'Feature / sprint-scope decisions', 1.5),
    (3, 'Tier 3', 120,  'Architectural / cross-team decisions', 1.5),
    (4, 'Tier 4', 240,  'Strategic / multi-quarter decisions', 1.5)
ON CONFLICT (tier_id) DO NOTHING;

CREATE TABLE IF NOT EXISTS decision_classes (
    class_id    SERIAL PRIMARY KEY,
    class_name  VARCHAR(64) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS defect_stages (
    stage_id   SERIAL PRIMARY KEY,
    stage_name VARCHAR(32) UNIQUE NOT NULL,
    stage_order SMALLINT NOT NULL,   -- 1=Development, 2=Execution, 3=Production
    target_pct  NUMERIC(5,2)         -- null = no explicit target for this stage
);

INSERT INTO defect_stages (stage_name, stage_order, target_pct) VALUES
    ('Development', 1, 60.00),
    ('Execution',   2, NULL),
    ('Production',  3, 10.00)
ON CONFLICT (stage_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS security_finding_stages (
    stage_id    SERIAL PRIMARY KEY,
    stage_name  VARCHAR(48) UNIQUE NOT NULL,
    stage_order SMALLINT NOT NULL,
    target_pct  NUMERIC(5,2)
);

INSERT INTO security_finding_stages (stage_name, stage_order, target_pct) VALUES
    ('Design Review',        1, NULL),
    ('Implementation Review',2, NULL),
    ('Release Gate',         3, NULL),
    ('Post-Release',         4, 5.00)
ON CONFLICT (stage_name) DO NOTHING;

-- ----------------------------------------------------------------
-- ADR / CCR records (source-of-truth mirror, updated by ingest_adr.py)
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS adr_records (
    adr_id           UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    adr_ref          VARCHAR(32)  UNIQUE NOT NULL,  -- e.g. ADR-0042
    title            TEXT         NOT NULL,
    tier_id          SMALLINT     REFERENCES adr_tiers(tier_id),
    class_id         INTEGER      REFERENCES decision_classes(class_id),
    status           VARCHAR(16)  NOT NULL DEFAULT 'proposed',
    -- Timestamps (all UTC)
    created_at       TIMESTAMPTZ  NOT NULL,
    submitted_at     TIMESTAMPTZ,
    first_reviewed_at TIMESTAMPTZ,
    resolved_at      TIMESTAMPTZ,
    -- Computed durations (hours)
    turnaround_hours NUMERIC(8,2) GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (resolved_at - submitted_at)) / 3600.0
    ) STORED,
    sla_met          BOOLEAN,      -- updated by transform_metrics.py
    repo_path        TEXT,
    git_sha          VARCHAR(64),
    ingested_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_adr_tier         ON adr_records(tier_id);
CREATE INDEX IF NOT EXISTS idx_adr_status       ON adr_records(status);
CREATE INDEX IF NOT EXISTS idx_adr_created_at   ON adr_records(created_at);
CREATE INDEX IF NOT EXISTS idx_adr_resolved_at  ON adr_records(resolved_at);

CREATE TABLE IF NOT EXISTS ccr_records (
    ccr_id           UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    ccr_ref          VARCHAR(32)  UNIQUE NOT NULL,  -- e.g. CCR-0017
    title            TEXT         NOT NULL,
    status           VARCHAR(16)  NOT NULL DEFAULT 'open',
    escalated_to_adr VARCHAR(32)  REFERENCES adr_records(adr_ref) ON UPDATE CASCADE,
    created_at       TIMESTAMPTZ  NOT NULL,
    resolved_at      TIMESTAMPTZ,
    repo_path        TEXT,
    git_sha          VARCHAR(64),
    ingested_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ccr_escalated ON ccr_records(escalated_to_adr);
CREATE INDEX IF NOT EXISTS idx_ccr_created   ON ccr_records(created_at);

-- ----------------------------------------------------------------
-- Defect / security finding records
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS defect_records (
    defect_id        UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    jira_key         VARCHAR(32)  UNIQUE NOT NULL,
    summary          TEXT,
    discovery_stage  INTEGER      REFERENCES defect_stages(stage_id),
    severity         VARCHAR(16),
    project_key      VARCHAR(32),
    created_at       TIMESTAMPTZ  NOT NULL,
    resolved_at      TIMESTAMPTZ,
    ingested_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS security_findings (
    finding_id       UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    finding_ref      VARCHAR(64)  UNIQUE NOT NULL,
    summary          TEXT,
    discovery_stage  INTEGER      REFERENCES security_finding_stages(stage_id),
    severity         VARCHAR(16),
    source_tool      VARCHAR(64),   -- e.g. 'sonarqube', 'snyk', 'trivy'
    created_at       TIMESTAMPTZ  NOT NULL,
    resolved_at      TIMESTAMPTZ,
    ingested_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ----------------------------------------------------------------
-- Process improvement initiatives
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS process_initiatives (
    initiative_id   UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title           TEXT        NOT NULL,
    owner_role      VARCHAR(64),
    target_date     DATE,
    completed_at    TIMESTAMPTZ,
    status          VARCHAR(16) NOT NULL DEFAULT 'in_progress',  -- in_progress | completed | cancelled
    source_adr_ref  VARCHAR(32) REFERENCES adr_records(adr_ref),
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ----------------------------------------------------------------
-- Aggregated daily metric snapshots (36-month retention)
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS daily_metric_snapshots (
    snapshot_id         UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    snapshot_date       DATE        NOT NULL,
    metric_name         VARCHAR(128) NOT NULL,
    metric_value        NUMERIC(12,4),
    dimension_key       VARCHAR(64),   -- e.g. tier, stage, project
    dimension_value     VARCHAR(128),
    computed_at         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    UNIQUE (snapshot_date, metric_name, dimension_key, dimension_value)
);

CREATE INDEX IF NOT EXISTS idx_dms_date   ON daily_metric_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_dms_metric ON daily_metric_snapshots(metric_name);

-- ----------------------------------------------------------------
-- Row-level expiry (raw mirrors: 12 months)
-- ----------------------------------------------------------------

CREATE OR REPLACE VIEW adr_records_active AS
    SELECT * FROM adr_records
    WHERE ingested_at >= NOW() - INTERVAL '12 months';

CREATE OR REPLACE VIEW ccr_records_active AS
    SELECT * FROM ccr_records
    WHERE ingested_at >= NOW() - INTERVAL '12 months';

CREATE OR REPLACE VIEW defect_records_active AS
    SELECT * FROM defect_records
    WHERE ingested_at >= NOW() - INTERVAL '12 months';

CREATE OR REPLACE VIEW security_findings_active AS
    SELECT * FROM security_findings
    WHERE ingested_at >= NOW() - INTERVAL '12 months';

-- PostgreSQL background job to delete old raw rows (run via pg_cron or Airflow cleanup DAG)
-- DELETE FROM adr_records     WHERE ingested_at < NOW() - INTERVAL '12 months';
-- DELETE FROM ccr_records     WHERE ingested_at < NOW() - INTERVAL '12 months';
-- DELETE FROM defect_records  WHERE ingested_at < NOW() - INTERVAL '12 months';
-- DELETE FROM security_findings WHERE ingested_at < NOW() - INTERVAL '12 months';
-- Aggregated snapshots: 36 months
-- DELETE FROM daily_metric_snapshots WHERE snapshot_date < NOW() - INTERVAL '36 months';

-- ============================================================
-- INFLUXDB — Time-Series Measurements (DDL as comments for reference)
-- InfluxDB uses Tags (indexed) and Fields (values).
-- Retention policies are set via InfluxDB CLI / Terraform.
-- ============================================================

-- BUCKET: engineering_metrics_raw   (retention: 365d)
-- BUCKET: engineering_metrics_agg   (retention: 1095d  = 36 months)

-- Measurement: git_metrics
--   Tags:    repo, branch, author_team
--   Fields:  commit_count (int), pr_count (int), pr_cycle_time_hours (float),
--            review_turnaround_hours (float), pr_size_lines (int)
--   Time:    UTC timestamp of aggregation window start

-- Measurement: jira_metrics
--   Tags:    project_key, team, sprint_name
--   Fields:  velocity_points (float), cycle_time_hours (float),
--            blocked_time_hours (float), defect_count (int)
--   Time:    UTC timestamp of sprint end (or daily snapshot)

-- Measurement: cicd_metrics
--   Tags:    pipeline_name, environment, repo
--   Fields:  build_success_rate (float), test_pass_rate (float),
--            deploy_frequency_per_day (float), pipeline_duration_seconds (float),
--            smoke_test_pass_rate (float)
--   Time:    UTC timestamp of pipeline run

-- Measurement: adr_metrics
--   Tags:    tier, decision_class, status
--   Fields:  turnaround_hours (float), sla_met (int 0/1),
--            adr_count (int), ccr_escalation_rate (float)
--   Time:    UTC timestamp of ADR resolution

-- Measurement: process_health_kpis   (derived, written by transform_metrics.py)
--   Tags:    metric_category
--   Fields:  shift_left_ratio (float), contract_clarity_index (float),
--            security_shift_left_ratio (float), initiative_completion_rate (float),
--            adr_sla_compliance_pct (float)
--   Time:    UTC timestamp of computation

-- ============================================================
-- GRANTS (adjust role names to your IAM setup)
-- ============================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'metrics_writer') THEN
        CREATE ROLE metrics_writer LOGIN PASSWORD 'CHANGE_ME_VIA_VAULT';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'metrics_reader') THEN
        CREATE ROLE metrics_reader LOGIN PASSWORD 'CHANGE_ME_VIA_VAULT';
    END IF;
END$$;

GRANT INSERT, UPDATE, SELECT ON ALL TABLES IN SCHEMA public TO metrics_writer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO metrics_writer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO metrics_reader;
