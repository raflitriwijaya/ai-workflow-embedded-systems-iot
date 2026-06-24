"""Statistical engine (spec §4.5, §5.3, §6.4, §7.1).

Pure standard-library implementations (math/statistics only) so the whole module
runs and tests without scipy/numpy. ``scipy.stats`` may be substituted in
production for performance, but the maths here is self-contained and verified
against known reference values in tests/test_stats.py.
"""
from __future__ import annotations

from .descriptive import (
    BaselineStats,
    compute_baseline_stats,
    linregress_slope,
    pearson,
    percentile,
)
from .irr import IRR_GATE, ICCResult, build_fleiss_matrix, fleiss_kappa, icc
from .readiness import (
    ReadinessResult,
    RoleReadiness,
    compute_deliverable_readiness,
    roll_up_role,
)
from .ttest import TTestResult, welch_ttest

__all__ = [
    "BaselineStats",
    "compute_baseline_stats",
    "percentile",
    "linregress_slope",
    "pearson",
    "fleiss_kappa",
    "build_fleiss_matrix",
    "icc",
    "ICCResult",
    "IRR_GATE",
    "welch_ttest",
    "TTestResult",
    "compute_deliverable_readiness",
    "roll_up_role",
    "ReadinessResult",
    "RoleReadiness",
]
