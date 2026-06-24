"""Scoring engine public API (spec §4).

Pure-Python: no database or network dependency, so the whole engine is unit
testable with the standard library. Persistence wires these results into
``evaluation_runs`` / ``metric_scores`` elsewhere.
"""
from __future__ import annotations

from .base import (
    DeliverableSpec,
    DimensionKind,
    DimensionResult,
    RubricDimension,
    RunStatus,
    ScoreResult,
    combine_composite,
    normalise_continuous,
    weighted_subscore,
)
from .human_review import HRAggregate, ReviewerScore, aggregate_hr
from .metrics_manifest import score_auto_from_metrics
from .registry import score_submission
from .schema_validators import SCHEMA_VALIDATORS, ValidationReport

__all__ = [
    "DeliverableSpec",
    "DimensionKind",
    "DimensionResult",
    "RubricDimension",
    "RunStatus",
    "ScoreResult",
    "ReviewerScore",
    "HRAggregate",
    "ValidationReport",
    "SCHEMA_VALIDATORS",
    "aggregate_hr",
    "score_auto_from_metrics",
    "score_submission",
    "combine_composite",
    "normalise_continuous",
    "weighted_subscore",
]
