"""Descriptive baseline statistics (spec §5.3).

Per deliverable per role the Baseline Statistical Report carries: n, mean, sd,
p25/p75/p95, min/max, a trend slope (to detect learning curves), and a temporal
stability flag (sd > 15 OR |trend| > 2 points/month → review before accepting).
Percentiles use linear interpolation, matching PostgreSQL ``percentile_cont`` so
the Python and SQL paths agree.
"""
from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import datetime

# Thresholds from spec §5.3 temporal_stability_flag.
SD_FLAG_THRESHOLD = 15.0
TREND_FLAG_THRESHOLD = 2.0  # points per month


def percentile(values: Sequence[float], q: float) -> float:
    """Linear-interpolation percentile, q in [0,1]. Matches percentile_cont."""
    if not values:
        raise ValueError("percentile of empty sequence")
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0,1]")
    xs = sorted(values)
    if len(xs) == 1:
        return float(xs[0])
    rank = (len(xs) - 1) * q
    lo = int(rank)
    frac = rank - lo
    if lo + 1 >= len(xs):
        return float(xs[lo])
    return float(xs[lo] + frac * (xs[lo + 1] - xs[lo]))


def linregress_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    """Ordinary least-squares slope dy/dx. 0.0 if undefined (n<2 or no x spread)."""
    n = len(xs)
    if n < 2 or len(ys) != n:
        return 0.0
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / sxx


@dataclass
class BaselineStats:
    n: int
    mean: float
    sd: float
    p25: float
    median: float
    p75: float
    p95: float
    min: float
    max: float
    trend_slope_per_month: float
    temporal_stability_flag: bool

    def as_dict(self) -> dict:
        return asdict(self)


def compute_baseline_stats(
    scores: Sequence[float],
    times: Sequence[datetime] | None = None,
) -> BaselineStats:
    """Compute the §5.3 baseline statistics for one deliverable's human samples."""
    if not scores:
        raise ValueError("cannot compute baseline stats from zero samples")
    n = len(scores)
    mean = statistics.fmean(scores)
    sd = statistics.stdev(scores) if n >= 2 else 0.0

    trend = 0.0
    if times is not None and len(times) == n and n >= 2:
        t0 = min(times)
        # x axis in months (30.0-day months) so the slope is points/month
        xs = [(t - t0).total_seconds() / (30.0 * 86400.0) for t in times]
        trend = linregress_slope(xs, list(scores))

    flag = sd > SD_FLAG_THRESHOLD or abs(trend) > TREND_FLAG_THRESHOLD
    return BaselineStats(
        n=n,
        mean=mean,
        sd=sd,
        p25=percentile(scores, 0.25),
        median=percentile(scores, 0.50),
        p75=percentile(scores, 0.75),
        p95=percentile(scores, 0.95),
        min=float(min(scores)),
        max=float(max(scores)),
        trend_slope_per_month=trend,
        temporal_stability_flag=flag,
    )


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float | None:
    """Pearson correlation (spec §6.4 harness_alignment_correlation). None if undefined."""
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / (sxx ** 0.5 * syy ** 0.5)
