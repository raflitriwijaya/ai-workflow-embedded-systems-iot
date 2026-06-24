"""Readiness computation — turns score distributions into gate states.

Per deliverable (spec §7.1 G1, §7.2 WG-1, §6.4 G3):
  * sample_threshold_met  — ≥ min_sample human baselines captured (WG-1)
  * phase gate (G1)       — agent mean ≥ baseline mean AND Welch p < 0.05
  * draft acceptance (G3) — rolling draft-acceptance ≥ 0.70 per role

Classification:
  RED    — baseline incomplete, OR agent clearly below baseline / acceptance < 0.50
  YELLOW — baseline ready but agent evidence insufficient or not yet significant
  GREEN  — baseline ready AND agent statistically ≥ baseline AND acceptance ≥ 0.70
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from .descriptive import compute_baseline_stats
from .ttest import TTestResult, welch_ttest

DRAFT_ACCEPT_GREEN = 0.70   # spec §6.4 per-role exit threshold
DRAFT_ACCEPT_RED = 0.50
MIN_AGENT_SAMPLES = 2       # need ≥2 to run a t-test


@dataclass
class ReadinessResult:
    readiness: str               # GREEN | YELLOW | RED
    reason: str
    sample_threshold_met: bool
    baseline_n: int
    baseline_mean: float | None = None
    baseline_sd: float | None = None
    baseline_p25: float | None = None
    baseline_p75: float | None = None
    baseline_p95: float | None = None
    temporal_stability_flag: bool = False
    agent_n: int = 0
    agent_mean: float | None = None
    welch: TTestResult | None = None
    draft_acceptance_rate: float | None = None

    def as_dict(self) -> dict:
        d = {
            "readiness": self.readiness,
            "reason": self.reason,
            "sample_threshold_met": self.sample_threshold_met,
            "baseline_n": self.baseline_n,
            "baseline_mean": self.baseline_mean,
            "baseline_sd": self.baseline_sd,
            "baseline_p25": self.baseline_p25,
            "baseline_p75": self.baseline_p75,
            "baseline_p95": self.baseline_p95,
            "temporal_stability_flag": self.temporal_stability_flag,
            "agent_n": self.agent_n,
            "agent_mean": self.agent_mean,
            "draft_acceptance_rate": self.draft_acceptance_rate,
        }
        d["welch"] = self.welch.as_dict() if self.welch else None
        return d


def compute_deliverable_readiness(
    baseline_scores: Sequence[float],
    agent_scores: Sequence[float],
    min_sample: int = 30,
    draft_acceptance_rate: float | None = None,
) -> ReadinessResult:
    baseline_n = len(baseline_scores)
    sample_met = baseline_n >= min_sample

    base_stats = compute_baseline_stats(baseline_scores) if baseline_n else None
    res = ReadinessResult(
        readiness="RED",
        reason="",
        sample_threshold_met=sample_met,
        baseline_n=baseline_n,
        baseline_mean=base_stats.mean if base_stats else None,
        baseline_sd=base_stats.sd if base_stats else None,
        baseline_p25=base_stats.p25 if base_stats else None,
        baseline_p75=base_stats.p75 if base_stats else None,
        baseline_p95=base_stats.p95 if base_stats else None,
        temporal_stability_flag=base_stats.temporal_stability_flag if base_stats else False,
        agent_n=len(agent_scores),
        draft_acceptance_rate=draft_acceptance_rate,
    )

    if not sample_met:
        res.readiness = "RED"
        res.reason = f"baseline incomplete: {baseline_n}/{min_sample} samples (WG-1 not met)"
        return res

    if len(agent_scores) < MIN_AGENT_SAMPLES:
        res.readiness = "YELLOW"
        res.reason = "baseline ready; insufficient agent samples to evaluate (need ≥2)"
        return res

    welch = welch_ttest(agent_scores, baseline_scores)
    res.welch = welch
    res.agent_mean = welch.mean_agent

    accept_ok = draft_acceptance_rate is None or draft_acceptance_rate >= DRAFT_ACCEPT_GREEN
    accept_red = draft_acceptance_rate is not None and draft_acceptance_rate < DRAFT_ACCEPT_RED

    if welch.significant and accept_ok:
        res.readiness = "GREEN"
        res.reason = (
            f"agent mean {welch.mean_agent:.1f} ≥ baseline {welch.mean_baseline:.1f}, "
            f"Welch p={welch.p_one_tailed:.4f} (<0.05)"
        )
        if draft_acceptance_rate is not None:
            res.reason += f", draft-accept {draft_acceptance_rate:.0%}"
    elif accept_red or welch.mean_agent < welch.mean_baseline:
        res.readiness = "RED"
        res.reason = (
            f"agent mean {welch.mean_agent:.1f} vs baseline {welch.mean_baseline:.1f}, "
            f"p={welch.p_one_tailed:.4f}"
            + (f"; draft-accept {draft_acceptance_rate:.0%} < 50%" if accept_red else "")
        )
    else:
        res.readiness = "YELLOW"
        res.reason = (
            f"agent mean {welch.mean_agent:.1f} ≥ baseline {welch.mean_baseline:.1f} "
            f"but not yet significant (p={welch.p_one_tailed:.4f})"
        )
    return res


@dataclass
class RoleReadiness:
    role_code: str
    readiness: str
    composite_agent_mean: float | None
    composite_baseline_mean: float | None
    draft_acceptance_rate: float | None
    deliverables: dict[str, ReadinessResult] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "role_code": self.role_code,
            "readiness": self.readiness,
            "composite_agent_mean": self.composite_agent_mean,
            "composite_baseline_mean": self.composite_baseline_mean,
            "draft_acceptance_rate": self.draft_acceptance_rate,
            "deliverables": {k: v.as_dict() for k, v in self.deliverables.items()},
        }


def roll_up_role(
    role_code: str,
    per_deliverable: dict[str, ReadinessResult],
    weights: dict[str, float],
    draft_acceptance_rate: float | None = None,
) -> RoleReadiness:
    """Aggregate per-deliverable readiness into a role-level gate (worst-case)."""
    states = {r.readiness for r in per_deliverable.values()}
    if not per_deliverable:
        role_state = "RED"
    elif "RED" in states:
        role_state = "RED"
    elif "YELLOW" in states:
        role_state = "YELLOW"
    else:
        role_state = "GREEN"

    def weighted(attr: str) -> float | None:
        total_w, acc = 0.0, 0.0
        for did, r in per_deliverable.items():
            val = getattr(r, attr)
            w = weights.get(did, 0.0)
            if val is not None and w > 0:
                acc += val * w
                total_w += w
        return acc / total_w if total_w > 0 else None

    return RoleReadiness(
        role_code=role_code,
        readiness=role_state,
        composite_agent_mean=weighted("agent_mean"),
        composite_baseline_mean=weighted("baseline_mean"),
        draft_acceptance_rate=draft_acceptance_rate,
        deliverables=per_deliverable,
    )
