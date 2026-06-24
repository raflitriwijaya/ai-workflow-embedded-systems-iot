"""AUTO scorer for code/config/pipeline deliverables (spec §4.1).

In CI the deterministic tools (ruff, pytest, lighthouse, tsc, …) run and emit a
*metrics manifest* — a flat mapping of ``dimension_key -> measured value``. This
scorer compares each value to its rubric threshold and produces a 0–100 auto
sub-score. The harness never re-runs the tools; it scores their reported output
(spec §4.1: "Automated checks run in the Evaluation Harness CI — not re-run
manually").

A metric that the rubric expects but the manifest omits scores 0 with a clear
message — silence is not a pass.
"""
from __future__ import annotations

import logging
from typing import Any

from .base import (
    DimensionKind,
    DimensionResult,
    RubricDimension,
    clamp,
    normalise_continuous,
    weighted_subscore,
)

LOG = logging.getLogger("harness.scoring.metrics")

_EPS = 1e-9


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value >= 1
    if isinstance(value, str):
        return value.strip().lower() in ("true", "pass", "passed", "ok", "yes", "1")
    if isinstance(value, dict) and "passed" in value:
        return bool(value["passed"])
    return False


def score_auto_from_metrics(
    auto_dims: list[RubricDimension], metrics: dict[str, Any]
) -> tuple[float | None, list[DimensionResult]]:
    """Return (auto_score 0–100, per-dimension results)."""
    results: list[DimensionResult] = []
    metrics = metrics or {}

    for d in auto_dims:
        if d.dimension_key not in metrics:
            results.append(
                DimensionResult(
                    dimension_key=d.dimension_key, kind=d.kind, score=0.0,
                    max_score=d.max_score, norm=0.0, weight=d.weight, passed=False,
                    detail="metric not reported in manifest",
                )
            )
            continue

        value = metrics[d.dimension_key]
        if d.kind == DimensionKind.AUTO_BINARY:
            passed = _coerce_bool(value)
            norm = 1.0 if passed else 0.0
            results.append(
                DimensionResult(
                    dimension_key=d.dimension_key, kind=d.kind, score=norm * d.max_score,
                    max_score=d.max_score, norm=norm, weight=d.weight, passed=passed,
                    detail="" if passed else "binary check failed",
                )
            )
        elif d.kind == DimensionKind.AUTO_CONTINUOUS:
            try:
                v = float(value)
            except (TypeError, ValueError):
                results.append(
                    DimensionResult(
                        dimension_key=d.dimension_key, kind=d.kind, score=0.0,
                        max_score=d.max_score, norm=0.0, weight=d.weight, passed=False,
                        detail=f"non-numeric value {value!r}",
                    )
                )
                continue
            norm = normalise_continuous(v, d.threshold, d.threshold_op or ">=")
            passed = norm >= 1.0 - _EPS
            results.append(
                DimensionResult(
                    dimension_key=d.dimension_key, kind=d.kind, score=norm * d.max_score,
                    max_score=d.max_score, norm=clamp(norm), weight=d.weight, passed=passed,
                    raw_value=v,
                    detail=f"{v} {d.threshold_op} {d.threshold}",
                )
            )
        else:  # defensive: an HR dim was mis-routed here
            LOG.warning("non-auto dimension %s routed to metrics scorer", d.dimension_key)

    return weighted_subscore(results), results
