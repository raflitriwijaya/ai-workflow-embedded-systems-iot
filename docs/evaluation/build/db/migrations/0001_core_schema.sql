-- =============================================================================
-- Evaluation Harness — Core Schema
-- Migration: 0001_core_schema
-- Spec: docs/evaluation/EVALUATION_HARNESS_SPEC.md  (v1.0.0, 2026-06-21)
-- Engine: PostgreSQL 15+ (TimescaleDB extension optional — see 0003)
--
-- Idempotent: every object uses IF NOT EXISTS / CREATE OR REPLACE so the
-- migration runner may re-apply on a partially-migrated database without error.
-- =============================================================================

-- pgcrypto provides gen_random_uuid() on PostgreSQL < 13; harmless on 13+.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ── Enumerated domains ───────────────────────────────────────────────────────
-- Created via DO-blocks so re-application does not raise "type already exists".

DO $$ BEGIN
    CREATE TYPE producer_type_t AS ENUM ('HUMAN', 'AGENT');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE scoring_type_t AS ENUM ('AUTO', 'HR', 'HYB');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE dimension_kind_t AS ENUM ('AUTO_BINARY', 'AUTO_CONTINUOUS', 'HR_RUBRIC', 'HR_PASS_FAIL');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE run_status_t AS ENUM ('PENDING', 'AUTO_SCORED', 'AWAITING_HR', 'ADJUDICATION', 'SCORED', 'ERROR');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE baseline_status_t AS ENUM ('DRAFT', 'TSC_ACCEPTED', 'SUPERSEDED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE readiness_t AS ENUM ('GREEN', 'YELLOW', 'RED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ── Lookup: roles ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS roles (
    role_code     TEXT PRIMARY KEY,                 -- e.g. 'DATA', 'FE', 'MLOPS'
    display_name  TEXT NOT NULL,
    skill_doc     TEXT NOT NULL,                    -- wikilink target, e.g. 'DATA_ENGINEER_SKILL'
    wave          SMALLINT NOT NULL CHECK (wave BETWEEN 1 AND 4),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Lookup: deliverables (the top-5 per role from spec §3) ────────────────────
CREATE TABLE IF NOT EXISTS deliverables (
    deliverable_id   TEXT PRIMARY KEY,              -- e.g. 'D1-DE-1'
    role_code        TEXT NOT NULL REFERENCES roles(role_code),
    name             TEXT NOT NULL,
    scoring_type     scoring_type_t NOT NULL,
    auto_weight      NUMERIC(4,3) NOT NULL DEFAULT 1.000 CHECK (auto_weight BETWEEN 0 AND 1),
    hr_weight        NUMERIC(4,3) NOT NULL DEFAULT 0.000 CHECK (hr_weight   BETWEEN 0 AND 1),
    composite_weight NUMERIC(4,3) NOT NULL CHECK (composite_weight BETWEEN 0 AND 1),  -- role-level weight (§3)
    min_sample       INTEGER NOT NULL DEFAULT 30 CHECK (min_sample > 0),
    schema_ref       TEXT,                          -- 'ADR'|'CCR'|'DQIR'|'IRD'|'OCM'|NULL
    scorer_key       TEXT NOT NULL,                 -- dispatch key into the Python scorer registry
    calibration_note TEXT,                          -- e.g. AUTO/HR split provenance (§10.1)
    active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT weights_sum_to_one CHECK (abs((auto_weight + hr_weight) - 1.000) < 0.001)
);
CREATE INDEX IF NOT EXISTS idx_deliverables_role ON deliverables(role_code);

-- ── scoring_rubrics: one row per scorable dimension per deliverable ───────────
-- Captures BOTH automated metrics (with thresholds/tools) AND human rubric
-- dimensions (0–3 scale). rubric_version lets us freeze a rubric (§10.1).
CREATE TABLE IF NOT EXISTS scoring_rubrics (
    rubric_id        BIGSERIAL PRIMARY KEY,
    deliverable_id   TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    rubric_version   TEXT NOT NULL DEFAULT 'v1',
    dimension_key    TEXT NOT NULL,                 -- stable machine key, e.g. 'lint_pass', 'rca_clarity'
    dimension_label  TEXT NOT NULL,                 -- human label from spec §3
    dimension_kind   dimension_kind_t NOT NULL,
    max_score        NUMERIC(6,2) NOT NULL DEFAULT 1.0,   -- 1.0 binary, 100 continuous, 3 rubric
    threshold        NUMERIC(12,4),                 -- SLO threshold for AUTO_CONTINUOUS (nullable)
    threshold_op     TEXT CHECK (threshold_op IN ('>=','<=','>','<','==')),  -- comparison sense
    weight           NUMERIC(6,4) NOT NULL DEFAULT 1.0,   -- weight within its (auto|hr) sub-score
    tool             TEXT,                          -- e.g. 'ruff', 'lighthouse', 'great_expectations'
    description      TEXT,
    active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (deliverable_id, rubric_version, dimension_key)
);
CREATE INDEX IF NOT EXISTS idx_rubrics_deliverable ON scoring_rubrics(deliverable_id, rubric_version);

-- ── submissions: every ingested artifact (HUMAN baseline or AGENT) ────────────
-- Producer identity is stored here but the blind_token is what scorers see,
-- enforcing blind scoring (spec §6.2).
CREATE TABLE IF NOT EXISTS submissions (
    submission_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code         TEXT NOT NULL REFERENCES roles(role_code),
    deliverable_id    TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    producer_type     producer_type_t NOT NULL,
    blind_token       UUID NOT NULL DEFAULT gen_random_uuid(),   -- shown to reviewers instead of identity
    artifact_uri      TEXT NOT NULL,                -- s3://... or file://...
    artifact_sha256   CHAR(64) NOT NULL,            -- integrity + dedup
    rubric_version    TEXT NOT NULL DEFAULT 'v1',
    -- producer-side metadata
    agent_id          TEXT,                         -- non-null when producer_type='AGENT'
    task_id           TEXT,
    human_producer_id TEXT,                         -- role-holder who produced a baseline sample
    time_spent_minutes INTEGER CHECK (time_spent_minutes IS NULL OR time_spent_minutes >= 0),
    complexity_rating SMALLINT CHECK (complexity_rating IS NULL OR complexity_rating BETWEEN 1 AND 5),
    -- agent acceptance tracking (spec §6.1)
    human_reviewer_id   TEXT,
    human_accepted      BOOLEAN,
    human_edit_required BOOLEAN,
    edit_effort_minutes INTEGER CHECK (edit_effort_minutes IS NULL OR edit_effort_minutes >= 0),
    is_baseline       BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_json     JSONB NOT NULL DEFAULT '{}'::jsonb,   -- carries tool metric outputs for AUTO scoring
    submitted_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT agent_has_id CHECK (producer_type <> 'AGENT' OR agent_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS idx_submissions_route ON submissions(role_code, deliverable_id, producer_type);
CREATE INDEX IF NOT EXISTS idx_submissions_blind ON submissions(blind_token);
CREATE UNIQUE INDEX IF NOT EXISTS uq_submissions_artifact
    ON submissions(deliverable_id, artifact_sha256);

-- ── evaluation_runs: one scoring run per submission (append-only results) ─────
CREATE TABLE IF NOT EXISTS evaluation_runs (
    run_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id   UUID NOT NULL REFERENCES submissions(submission_id) ON DELETE CASCADE,
    rubric_version  TEXT NOT NULL,
    engine_version  TEXT NOT NULL,                  -- harness SemVer that produced the scores
    status          run_status_t NOT NULL DEFAULT 'PENDING',
    auto_score      NUMERIC(6,3) CHECK (auto_score IS NULL OR auto_score BETWEEN 0 AND 100),
    hr_score        NUMERIC(6,3) CHECK (hr_score   IS NULL OR hr_score   BETWEEN 0 AND 100),
    composite_score NUMERIC(6,3) CHECK (composite_score IS NULL OR composite_score BETWEEN 0 AND 100),
    detail_json     JSONB NOT NULL DEFAULT '{}'::jsonb,   -- per-rule pass/fail + messages
    error_message   TEXT,
    scored_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_runs_submission ON evaluation_runs(submission_id);
CREATE INDEX IF NOT EXISTS idx_runs_status ON evaluation_runs(status);

-- ── metric_scores: per-dimension detail for a run (audit granularity) ─────────
CREATE TABLE IF NOT EXISTS metric_scores (
    metric_score_id BIGSERIAL PRIMARY KEY,
    run_id          UUID NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    rubric_id       BIGINT REFERENCES scoring_rubrics(rubric_id),
    dimension_key   TEXT NOT NULL,
    raw_value       NUMERIC(14,4),                  -- measured value (continuous) when applicable
    score           NUMERIC(6,3) NOT NULL,          -- normalised contribution 0..max_score
    max_score       NUMERIC(6,2) NOT NULL,
    passed          BOOLEAN,                        -- for binary dimensions
    detail          TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_metric_scores_run ON metric_scores(run_id);

-- ── human_review_scores: per-reviewer rubric scores (blind) → IRR + adjudication
CREATE TABLE IF NOT EXISTS human_review_scores (
    review_id       BIGSERIAL PRIMARY KEY,
    run_id          UUID NOT NULL REFERENCES evaluation_runs(run_id) ON DELETE CASCADE,
    reviewer_id     TEXT NOT NULL,                  -- panel member id (never the producer)
    dimension_key   TEXT NOT NULL,
    score           NUMERIC(4,2) NOT NULL CHECK (score >= 0),   -- 0–3 rubric, or 0/1 pass-fail
    is_adjudicator  BOOLEAN NOT NULL DEFAULT FALSE,
    submitted_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (run_id, reviewer_id, dimension_key)
);
CREATE INDEX IF NOT EXISTS idx_hr_scores_run ON human_review_scores(run_id);

-- ── human_baselines: one row per scored HUMAN sample (gate counts read here) ──
-- Denormalised composite for fast ≥30 counting (WG-1) and stats (HG-5).
CREATE TABLE IF NOT EXISTS human_baselines (
    baseline_id      BIGSERIAL PRIMARY KEY,
    role_code        TEXT NOT NULL REFERENCES roles(role_code),
    deliverable_id   TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    submission_id    UUID NOT NULL REFERENCES submissions(submission_id),
    run_id           UUID NOT NULL REFERENCES evaluation_runs(run_id),
    composite_score  NUMERIC(6,3) NOT NULL CHECK (composite_score BETWEEN 0 AND 100),
    time_spent_minutes INTEGER,
    complexity_rating  SMALLINT,
    rubric_version   TEXT NOT NULL,
    captured_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (submission_id)
);
CREATE INDEX IF NOT EXISTS idx_baselines_route ON human_baselines(role_code, deliverable_id, rubric_version);

-- ── agent_results: one row per scored AGENT submission ────────────────────────
CREATE TABLE IF NOT EXISTS agent_results (
    result_id        BIGSERIAL PRIMARY KEY,
    role_code        TEXT NOT NULL REFERENCES roles(role_code),
    deliverable_id   TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    submission_id    UUID NOT NULL REFERENCES submissions(submission_id),
    run_id           UUID NOT NULL REFERENCES evaluation_runs(run_id),
    agent_id         TEXT NOT NULL,
    composite_score  NUMERIC(6,3) NOT NULL CHECK (composite_score BETWEEN 0 AND 100),
    human_accepted      BOOLEAN NOT NULL DEFAULT FALSE,
    human_edit_required BOOLEAN NOT NULL DEFAULT FALSE,
    edit_effort_minutes INTEGER,
    -- draft_accepted: accepted AND not edited (spec §6.4 draft_acceptance_rate numerator)
    draft_accepted   BOOLEAN GENERATED ALWAYS AS (human_accepted AND NOT human_edit_required) STORED,
    rubric_version   TEXT NOT NULL,
    sprint           TEXT,
    captured_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (submission_id)
);
CREATE INDEX IF NOT EXISTS idx_agent_results_route ON agent_results(role_code, deliverable_id, rubric_version);
CREATE INDEX IF NOT EXISTS idx_agent_results_time ON agent_results(captured_at);

-- ── role_readiness: computed gate state per role×deliverable (statistical engine)
CREATE TABLE IF NOT EXISTS role_readiness (
    readiness_id        BIGSERIAL PRIMARY KEY,
    role_code           TEXT NOT NULL REFERENCES roles(role_code),
    deliverable_id      TEXT REFERENCES deliverables(deliverable_id),  -- NULL = role-level rollup
    rubric_version      TEXT NOT NULL,
    baseline_n          INTEGER NOT NULL DEFAULT 0,
    baseline_mean       NUMERIC(6,3),
    baseline_sd         NUMERIC(6,3),
    baseline_p25        NUMERIC(6,3),
    baseline_p75        NUMERIC(6,3),
    baseline_p95        NUMERIC(6,3),
    baseline_status     baseline_status_t NOT NULL DEFAULT 'DRAFT',
    temporal_stability_flag BOOLEAN NOT NULL DEFAULT FALSE,
    agent_n             INTEGER NOT NULL DEFAULT 0,
    agent_mean          NUMERIC(6,3),
    welch_t             NUMERIC(10,4),
    welch_p             NUMERIC(10,6),              -- one-tailed agent>=baseline
    draft_acceptance_rate NUMERIC(5,4),
    harness_alignment_r NUMERIC(5,4),              -- Pearson(harness_score, human_accepted)
    sample_threshold_met BOOLEAN NOT NULL DEFAULT FALSE,
    readiness           readiness_t NOT NULL DEFAULT 'RED',
    computed_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (role_code, deliverable_id, rubric_version, computed_at)
);
CREATE INDEX IF NOT EXISTS idx_readiness_latest ON role_readiness(role_code, deliverable_id, computed_at DESC);

-- ── incidents: agent-attributable safety/security/quality (spec §6.5 / DASH-8) ─
CREATE TABLE IF NOT EXISTS incidents (
    incident_id     BIGSERIAL PRIMARY KEY,
    incident_class  TEXT NOT NULL CHECK (incident_class IN ('SAFETY','SECURITY','QUALITY_ESCAPE')),
    role_code       TEXT REFERENCES roles(role_code),
    agent_id        TEXT,
    submission_id   UUID REFERENCES submissions(submission_id),
    description     TEXT NOT NULL,
    severity        TEXT,
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_incidents_class ON incidents(incident_class, occurred_at);
