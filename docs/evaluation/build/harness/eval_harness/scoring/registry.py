"""Scorer dispatch and the top-level :func:`score_submission` orchestrator.

``scorer_key`` semantics (from the ``deliverables`` table):
    'metrics_manifest'   -> AUTO sub-score from the CI metrics manifest
    'human_review_only'  -> no AUTO sub-score; HR only
    'schema:<NAME>'      -> AUTO sub-score = % of <NAME> validation rules passed
                            (NAME in ADR|CCR|DQIR|IRD|OCM)

The orchestrator is pure: give it the deliverable spec, its rubric dimensions,
and the available inputs (CI metrics, parsed artifact, reviewer scores) and it
returns a fully-populated :class:`ScoreResult`. Persistence is the caller's job.
"""
from __future__ import annotations

import logging
from typing import Any

from .base import (
    DeliverableSpec,
    DimensionResult,
    RubricDimension,
    RunStatus,
    ScoreResult,
    clamp,
    combine_composite,
    weighted_subscore,
)
from .human_review import ReviewerScore, aggregate_hr
from .metrics_manifest import score_auto_from_metrics
from .schema_validators import SCHEMA_VALIDATORS

LOG = logging.getLogger("harness.scoring.registry")


def _score_schema(
    schema: str,
    auto_dims: list[RubricDimension],
    artifact_data: dict[str, Any],
    ctx: dict[str, Any] | None,
) -> tuple[float, list[DimensionResult], bool, dict]:
    """Run a schema validator; map pass% onto the deliverable's single auto dim."""
    validator = SCHEMA_VALIDATORS[schema]
    report = validator(artifact_data or {}, **(ctx or {}))
    pass_pct = report.pass_pct

    # The seed gives schema deliverables one AUTO_CONTINUOUS dim (threshold 100).
    if auto_dims:
        d = auto_dims[0]
        norm = clamp(pass_pct / (d.threshold or 100.0))
        dim = DimensionResult(
            dimension_key=d.dimension_key, kind=d.kind, score=norm * d.max_score,
            max_score=d.max_score, norm=norm, weight=d.weight, raw_value=pass_pct,
            passed=report.total > 0 and report.passed == report.total,
            detail=f"{report.passed}/{report.total} {schema} rules passed",
        )
        auto_score = weighted_subscore([dim]) or 0.0
        return auto_score, [dim], report.hard_block, report.to_dict()

    # No explicit rubric dim: auto_score == pass_pct.
    return pass_pct, [], report.hard_block, report.to_dict()


def score_submission(
    spec: DeliverableSpec,
    rubric_dims: list[RubricDimension],
    *,
    metrics: dict[str, Any] | None = None,
    artifact_data: dict[str, Any] | None = None,
    reviewer_scores: dict[str, list[ReviewerScore]] | None = None,
    validator_ctx: dict[str, Any] | None = None,
) -> ScoreResult:
    auto_dims = [d for d in rubric_dims if d.is_auto]
    hr_dims = [d for d in rubric_dims if d.is_hr]
    result = ScoreResult(deliverable_id=spec.deliverable_id, status=RunStatus.PENDING)

    # ── AUTO sub-score ────────────────────────────────────────────────────────
    if spec.scoring_type in ("AUTO", "HYB"):
        try:
            if spec.scorer_key.startswith("schema:"):
                schema = spec.scorer_key.split(":", 1)[1]
                if schema not in SCHEMA_VALIDATORS:
                    raise KeyError(f"unknown schema validator {schema!r}")
                auto_score, dims, hard_block, report = _score_schema(
                    schema, auto_dims, artifact_data or {}, validator_ctx
                )
                result.auto_score = auto_score
                result.dimensions.extend(dims)
                result.hard_block = result.hard_block or hard_block
                result.schema_report = report
                if hard_block:
                    result.messages.append(f"{schema} hard block: artifact valid but dispatch halted")
            elif spec.scorer_key == "metrics_manifest":
                auto_score, dims = score_auto_from_metrics(auto_dims, metrics or {})
                result.auto_score = auto_score
                result.dimensions.extend(dims)
            elif spec.scorer_key == "human_review_only":
                pass  # no auto component
            else:
                raise KeyError(f"unknown scorer_key {spec.scorer_key!r}")
        except Exception as exc:  # pragma: no cover - defensive
            LOG.exception("auto scoring failed for %s", spec.deliverable_id)
            result.status = RunStatus.ERROR
            result.messages.append(f"auto scoring error: {exc}")
            return result

    # ── HR sub-score ──────────────────────────────────────────────────────────
    hr_complete = True
    if spec.scoring_type in ("HR", "HYB"):
        if reviewer_scores:
            agg = aggregate_hr(hr_dims, reviewer_scores)
            result.hr_score = agg.hr_score
            result.dimensions.extend(agg.dimensions)
            if agg.needs_adjudication:
                result.status = RunStatus.ADJUDICATION
                result.messages.append("HR divergence > 1 point — third-reviewer adjudication required")
                hr_complete = False
            if agg.insufficient_reviews or agg.hr_score is None:
                hr_complete = False
        else:
            hr_complete = False

    # ── compose + status ───────────────────────────────────────────────────────
    result.composite_score = combine_composite(
        spec.scoring_type, float(spec.auto_weight), float(spec.hr_weight),
        result.auto_score, result.hr_score,
    )

    if result.status == RunStatus.ADJUDICATION:
        return result
    if spec.scoring_type == "AUTO":
        result.status = RunStatus.SCORED if result.auto_score is not None else RunStatus.ERROR
    elif not hr_complete:
        result.status = RunStatus.AWAITING_HR
    else:
        result.status = RunStatus.SCORED
    return result
