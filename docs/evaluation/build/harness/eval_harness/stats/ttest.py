"""Welch's t-test for the agent-vs-baseline phase-gate metric (spec §4.5, §7.1).

An agent "matches or exceeds the human baseline" when its composite-score mean
is ≥ the baseline mean AND a one-tailed Welch's t-test (agent ≥ baseline) gives
p < 0.05. Welch's (unequal-variance) test is used because agent and human sample
sizes and variances differ.
"""
from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass

from .special import student_t_sf

ALPHA = 0.05


@dataclass
class TTestResult:
    t: float
    df: float
    p_one_tailed: float       # P(T > t): evidence that agent mean > baseline mean
    mean_agent: float
    mean_baseline: float
    significant: bool         # p < ALPHA AND agent mean ≥ baseline mean

    def as_dict(self) -> dict:
        return {
            "t": self.t,
            "df": self.df,
            "p_one_tailed": self.p_one_tailed,
            "mean_agent": self.mean_agent,
            "mean_baseline": self.mean_baseline,
            "significant": self.significant,
        }


def welch_ttest(agent: Sequence[float], baseline: Sequence[float]) -> TTestResult:
    """One-tailed Welch's t-test of H1: mean(agent) > mean(baseline)."""
    n1, n2 = len(agent), len(baseline)
    if n1 < 2 or n2 < 2:
        raise ValueError("Welch's t-test requires ≥2 samples per group")
    m1, m2 = statistics.fmean(agent), statistics.fmean(baseline)
    v1, v2 = statistics.variance(agent), statistics.variance(baseline)
    se2 = v1 / n1 + v2 / n2

    if se2 == 0:
        # Degenerate: both groups have zero variance.
        t = float("inf") if m1 > m2 else (float("-inf") if m1 < m2 else 0.0)
        p = 0.0 if m1 > m2 else (1.0 if m1 < m2 else 0.5)
        return TTestResult(t, float("inf"), p, m1, m2, p < ALPHA and m1 >= m2)

    t = (m1 - m2) / (se2 ** 0.5)
    df = (se2 ** 2) / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    p = student_t_sf(t, df)
    return TTestResult(
        t=t, df=df, p_one_tailed=p, mean_agent=m1, mean_baseline=m2,
        significant=(p < ALPHA and m1 >= m2),
    )
