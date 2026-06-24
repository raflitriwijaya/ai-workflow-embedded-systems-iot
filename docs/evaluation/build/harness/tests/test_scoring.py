"""Scoring-engine tests: AUTO metrics, HR aggregation/adjudication, hybrid
composite, and the schema:OCM dispatch path through score_submission."""
from __future__ import annotations

import pytest

from eval_harness.scoring import (
    DeliverableSpec,
    DimensionKind,
    ReviewerScore,
    RubricDimension,
    RunStatus,
    aggregate_hr,
    score_auto_from_metrics,
    score_submission,
)
from tests.test_validators import _valid_ocm

V = "v1"


def _auto_dim(key, kind, **kw):
    return RubricDimension(deliverable_id="D", dimension_key=key, dimension_label=key, kind=kind, **kw)


# ── AUTO metrics manifest ─────────────────────────────────────────────────────
def test_auto_all_pass_is_100():
    dims = [
        _auto_dim("lint", DimensionKind.AUTO_BINARY),
        _auto_dim("cov", DimensionKind.AUTO_CONTINUOUS, threshold=80, threshold_op=">="),
    ]
    score, results = score_auto_from_metrics(dims, {"lint": True, "cov": 92})
    assert score == pytest.approx(100.0)
    assert all(r.passed for r in results)


def test_auto_missing_metric_scores_zero():
    dims = [_auto_dim("lint", DimensionKind.AUTO_BINARY)]
    score, results = score_auto_from_metrics(dims, {})
    assert score == pytest.approx(0.0)
    assert results[0].detail == "metric not reported in manifest"


def test_auto_continuous_partial_credit_below_threshold():
    dims = [_auto_dim("cov", DimensionKind.AUTO_CONTINUOUS, threshold=80, threshold_op=">=")]
    score, _ = score_auto_from_metrics(dims, {"cov": 40})
    assert score == pytest.approx(50.0)  # 40/80


def test_auto_continuous_lower_is_better():
    # latency budget 100 ms, measured 50 ms -> full credit (clamped)
    dims = [_auto_dim("lat", DimensionKind.AUTO_CONTINUOUS, threshold=100, threshold_op="<=")]
    score, _ = score_auto_from_metrics(dims, {"lat": 50})
    assert score == pytest.approx(100.0)
    score2, _ = score_auto_from_metrics(dims, {"lat": 200})
    assert score2 == pytest.approx(50.0)  # 100/200


# ── human review aggregation ──────────────────────────────────────────────────
def _hr_dim(key):
    return RubricDimension(deliverable_id="D", dimension_key=key, dimension_label=key,
                           kind=DimensionKind.HR_RUBRIC, max_score=3.0)


def test_hr_mean_of_two_reviewers():
    dims = [_hr_dim("clarity")]
    scores = {"clarity": [ReviewerScore("r1", 3), ReviewerScore("r2", 3)]}
    agg = aggregate_hr(dims, scores)
    assert agg.hr_score == pytest.approx(100.0)
    assert not agg.needs_adjudication


def test_hr_divergence_triggers_adjudication():
    dims = [_hr_dim("clarity")]
    scores = {"clarity": [ReviewerScore("r1", 1), ReviewerScore("r2", 3)]}  # diff 2 > 1
    agg = aggregate_hr(dims, scores)
    assert agg.needs_adjudication is True


def test_hr_adjudicator_resolves_with_median():
    dims = [_hr_dim("clarity")]
    scores = {"clarity": [
        ReviewerScore("r1", 1), ReviewerScore("r2", 3), ReviewerScore("r3", 2, is_adjudicator=True),
    ]}
    agg = aggregate_hr(dims, scores)
    assert not agg.needs_adjudication
    assert agg.hr_score == pytest.approx(100.0 * 2 / 3)  # median([1,3,2]) = 2 -> 2/3


# ── hybrid composite via score_submission ─────────────────────────────────────
def test_hybrid_composite_combines_auto_and_hr():
    spec = DeliverableSpec(
        deliverable_id="D1-DE-2", role_code="DATA", scoring_type="HYB",
        auto_weight=0.7, hr_weight=0.3, composite_weight=0.2, scorer_key="metrics_manifest",
    )
    dims = [
        _auto_dim("sections", DimensionKind.AUTO_BINARY),
        _hr_dim("rca_clarity"),
    ]
    res = score_submission(
        spec, dims,
        metrics={"sections": True},
        reviewer_scores={"rca_clarity": [ReviewerScore("r1", 2), ReviewerScore("r2", 2)]},
    )
    assert res.auto_score == pytest.approx(100.0)
    assert res.hr_score == pytest.approx(100.0 * 2 / 3)
    assert res.composite_score == pytest.approx(0.7 * 100.0 + 0.3 * (200.0 / 3))
    assert res.status == RunStatus.SCORED


def test_hybrid_awaiting_hr_when_no_reviews():
    spec = DeliverableSpec(
        deliverable_id="D1-DE-2", role_code="DATA", scoring_type="HYB",
        auto_weight=0.7, hr_weight=0.3, composite_weight=0.2, scorer_key="metrics_manifest",
    )
    dims = [_auto_dim("sections", DimensionKind.AUTO_BINARY), _hr_dim("rca_clarity")]
    res = score_submission(spec, dims, metrics={"sections": True})
    assert res.status == RunStatus.AWAITING_HR
    assert res.composite_score is None


# ── schema:OCM dispatch ───────────────────────────────────────────────────────
def _ocm_spec():
    return DeliverableSpec(
        deliverable_id="D1-ML-4", role_code="MLOPS", scoring_type="AUTO",
        auto_weight=1.0, hr_weight=0.0, composite_weight=0.25,
        scorer_key="schema:OCM", schema_ref="OCM",
    )


def _ocm_rule_dim():
    return RubricDimension(deliverable_id="D1-ML-4", dimension_key="ocm_v_rules",
                           dimension_label="OCM rules", kind=DimensionKind.AUTO_CONTINUOUS,
                           threshold=100, threshold_op=">=")


def test_schema_ocm_valid_scores_100():
    res = score_submission(_ocm_spec(), [_ocm_rule_dim()], artifact_data=_valid_ocm())
    assert res.auto_score == pytest.approx(100.0)
    assert res.composite_score == pytest.approx(100.0)
    assert res.hard_block is False
    assert res.status == RunStatus.SCORED
    assert res.schema_report["schema"] == "OCM"


def test_schema_ocm_budget_fail_sets_hard_block():
    res = score_submission(_ocm_spec(), [_ocm_rule_dim()], artifact_data=_valid_ocm(util_pct=97.0))
    assert res.hard_block is True
    assert res.auto_score < 100.0  # the V-OCM-14 rule fails


def test_unknown_scorer_key_yields_error_status():
    spec = DeliverableSpec(
        deliverable_id="D?", role_code="DATA", scoring_type="AUTO",
        auto_weight=1.0, hr_weight=0.0, composite_weight=1.0, scorer_key="bogus",
    )
    res = score_submission(spec, [])
    assert res.status == RunStatus.ERROR
