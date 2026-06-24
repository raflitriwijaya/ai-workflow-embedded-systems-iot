"""Statistics tests — verified against published reference values where possible."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from eval_harness.stats import (
    build_fleiss_matrix,
    compute_baseline_stats,
    compute_deliverable_readiness,
    fleiss_kappa,
    icc,
    pearson,
    percentile,
    welch_ttest,
)
from eval_harness.stats.special import f_sf, student_t_sf


# ── special functions vs standard statistical tables ─────────────────────────
def test_student_t_sf_known_critical_values():
    # One-tailed t critical values for df=10: t_0.05=1.8125, t_0.025=2.2281.
    assert abs(student_t_sf(0.0, 10) - 0.5) < 1e-9
    assert abs(student_t_sf(1.8125, 10) - 0.05) < 1e-3
    assert abs(student_t_sf(2.2281, 10) - 0.025) < 1e-3
    # Large df approaches the normal: z_0.05 = 1.6449.
    assert abs(student_t_sf(1.6449, 10_000_000) - 0.05) < 1e-3


def test_f_sf_known_critical_value():
    # F_0.05(3, 10) = 3.708 -> survival ~ 0.05.
    assert abs(f_sf(3.708, 3, 10) - 0.05) < 2e-3
    assert f_sf(0.0, 3, 10) == 1.0


# ── percentiles (must match PostgreSQL percentile_cont / numpy 'linear') ──────
def test_percentile_linear_interpolation():
    assert percentile([1, 2, 3, 4], 0.5) == 2.5
    assert percentile([10, 20, 30, 40, 50], 0.95) == pytest.approx(48.0)
    assert percentile([5], 0.25) == 5.0
    assert percentile([1, 2, 3, 4, 5], 0.25) == 2.0


# ── Welch's t-test ────────────────────────────────────────────────────────────
def test_welch_identical_groups_not_significant():
    a = [80, 82, 78, 81, 79]
    res = welch_ttest(a, list(a))
    assert res.t == pytest.approx(0.0, abs=1e-9)
    assert res.p_one_tailed == pytest.approx(0.5, abs=1e-6)
    assert res.significant is False


def test_welch_agent_clearly_higher_is_significant():
    baseline = [70, 72, 71, 69, 73, 70, 71, 72, 70, 71]
    agent = [85, 86, 84, 87, 85, 86, 84, 85, 86, 85]
    res = welch_ttest(agent, baseline)
    assert res.mean_agent > res.mean_baseline
    assert res.p_one_tailed < 0.05
    assert res.significant is True


def test_welch_agent_lower_not_significant():
    baseline = [85, 86, 84, 87, 85]
    agent = [70, 72, 71, 69, 73]
    res = welch_ttest(agent, baseline)
    assert res.significant is False


# ── Fleiss' kappa ─────────────────────────────────────────────────────────────
def test_fleiss_perfect_and_total_disagreement():
    cats = [0, 1, 2, 3]
    perfect = build_fleiss_matrix([[3, 3], [1, 1], [2, 2]], cats)
    assert fleiss_kappa(perfect) == pytest.approx(1.0)

    disagree = build_fleiss_matrix([[0, 3], [3, 0]], cats)
    assert fleiss_kappa(disagree) == pytest.approx(-1.0)


def test_fleiss_rejects_unequal_raters():
    with pytest.raises(ValueError):
        build_fleiss_matrix([[1, 2], [3]], [1, 2, 3])


# ── ICC ───────────────────────────────────────────────────────────────────────
def test_icc_perfect_agreement_is_one():
    data = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
    res = icc(data)
    assert res.icc_single > 0.99
    assert res.icc_average > 0.99


def test_icc_no_between_subject_signal_is_low():
    # All subjects identical -> no true variance between subjects -> ICC ~ 0/neg.
    data = [[3, 4], [3, 4], [3, 4], [3, 4]]
    res = icc(data)
    assert res.icc_single < 0.2


# ── baseline stats + temporal stability flag ─────────────────────────────────
def test_baseline_stats_flags_high_variance():
    stable = [80] * 30
    s = compute_baseline_stats(stable)
    assert s.n == 30 and s.mean == 80 and s.sd == 0
    assert s.temporal_stability_flag is False

    noisy = [50, 90] * 15  # sd well above 15
    s2 = compute_baseline_stats(noisy)
    assert s2.temporal_stability_flag is True


def test_baseline_stats_flags_learning_trend():
    t0 = datetime(2026, 1, 1)
    # +5 points/month over 3 months -> trend slope > 2 -> flag
    scores, times = [], []
    for month in range(3):
        for _ in range(10):
            scores.append(60 + 5 * month)
            times.append(t0 + timedelta(days=30 * month))
    s = compute_baseline_stats(scores, times)
    assert s.trend_slope_per_month > 2.0
    assert s.temporal_stability_flag is True


def test_pearson_basic():
    assert pearson([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert pearson([1, 2, 3], [3, 2, 1]) == pytest.approx(-1.0)


# ── readiness classification ──────────────────────────────────────────────────
def test_readiness_red_when_baseline_incomplete():
    res = compute_deliverable_readiness([80] * 10, [85] * 5, min_sample=30)
    assert res.readiness == "RED"
    assert res.sample_threshold_met is False


def test_readiness_green_when_agent_beats_baseline():
    baseline = [70 + (i % 5) for i in range(30)]
    agent = [85 + (i % 3) for i in range(12)]
    res = compute_deliverable_readiness(baseline, agent, min_sample=30, draft_acceptance_rate=0.82)
    assert res.readiness == "GREEN"
    assert res.welch is not None and res.welch.significant


def test_readiness_red_when_agent_below_baseline():
    baseline = [85 + (i % 4) for i in range(30)]
    agent = [70 + (i % 3) for i in range(10)]
    res = compute_deliverable_readiness(baseline, agent, min_sample=30, draft_acceptance_rate=0.40)
    assert res.readiness == "RED"


def test_readiness_yellow_when_baseline_ready_no_agent_samples():
    res = compute_deliverable_readiness([80 + (i % 5) for i in range(30)], [], min_sample=30)
    assert res.readiness == "YELLOW"
