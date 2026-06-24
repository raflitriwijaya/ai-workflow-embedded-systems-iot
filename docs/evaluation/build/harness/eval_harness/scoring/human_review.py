"""Human-reviewed scoring aggregation (spec §4.2).

Two reviewers independently score each 0–3 rubric dimension, blind to producer
identity. Per dimension the final score is the mean of the two; if the two
diverge by more than 1 point a third reviewer adjudicates and the median of the
three is used. The dimension sub-scores are normalised and weight-averaged to a
0–100 HR sub-score.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass

from .base import DimensionResult, RubricDimension, clamp, weighted_subscore

DIVERGENCE_THRESHOLD = 1.0  # spec §4.2: |score_A − score_B| > 1 → adjudication


@dataclass(frozen=True)
class ReviewerScore:
    reviewer_id: str
    score: float
    is_adjudicator: bool = False


@dataclass
class HRAggregate:
    hr_score: float | None
    dimensions: list[DimensionResult]
    needs_adjudication: bool      # ≥1 dimension diverged and has no adjudicator yet
    insufficient_reviews: bool    # ≥1 dimension has < 2 primary reviewers


def _resolve_dimension(primary: list[float], adjudicator: float | None) -> tuple[float | None, bool]:
    """Return (final_score, needs_adjudication)."""
    if len(primary) < 2:
        # not enough reviewers yet; use the single score provisionally if present
        return (primary[0] if primary else None), False
    a, b = primary[0], primary[1]
    if abs(a - b) > DIVERGENCE_THRESHOLD:
        if adjudicator is not None:
            return statistics.median([a, b, adjudicator]), False
        return statistics.mean([a, b]), True  # provisional pending adjudication
    return statistics.mean([a, b]), False


def aggregate_hr(
    hr_dims: list[RubricDimension],
    reviewer_scores: dict[str, list[ReviewerScore]],
) -> HRAggregate:
    """``reviewer_scores`` maps dimension_key -> list of ReviewerScore."""
    results: list[DimensionResult] = []
    needs_adj = False
    insufficient = False

    for d in hr_dims:
        entries = reviewer_scores.get(d.dimension_key, [])
        primary = [e.score for e in entries if not e.is_adjudicator]
        adj = next((e.score for e in entries if e.is_adjudicator), None)

        final, dim_needs_adj = _resolve_dimension(primary, adj)
        needs_adj = needs_adj or dim_needs_adj
        if len(primary) < 2:
            insufficient = True

        if final is None:
            results.append(
                DimensionResult(
                    dimension_key=d.dimension_key, kind=d.kind, score=0.0,
                    max_score=d.max_score, norm=0.0, weight=0.0,  # weight 0 → excluded until scored
                    detail="awaiting reviewer scores",
                )
            )
            continue

        norm = clamp(final / d.max_score) if d.max_score else 0.0
        detail = f"final={final:.2f}/{d.max_score:g} from {len(primary)} reviewer(s)"
        if dim_needs_adj:
            detail += " — DIVERGENT, adjudication pending"
        results.append(
            DimensionResult(
                dimension_key=d.dimension_key, kind=d.kind, score=norm * d.max_score,
                max_score=d.max_score, norm=norm, weight=d.weight, raw_value=final, detail=detail,
            )
        )

    scored = [r for r in results if r.weight > 0]
    hr_score = weighted_subscore(scored) if scored else None
    return HRAggregate(
        hr_score=hr_score,
        dimensions=results,
        needs_adjudication=needs_adj,
        insufficient_reviews=insufficient,
    )
