"""Core scoring data types and normalisation math (spec §4).

All sub-scores are normalised to 0–100 before comparison (spec §4.5). The unit
of normalisation is the *dimension*: every rubric dimension contributes a value
in [0, 1] (``norm``); the sub-score is ``100 * weighted_mean(norm)``.

* AUTO_BINARY      -> norm = 1.0 if passed else 0.0
* AUTO_CONTINUOUS  -> norm = clamp(value/threshold) for higher-is-better ('>=','>')
                              clamp(threshold/value) for lower-is-better ('<=','<')
                              1.0 if equal within tol for '=='
* HR_RUBRIC (0–3)  -> norm = score / 3
* HR_PASS_FAIL     -> norm = score (0 or 1)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class DimensionKind(StrEnum):
    AUTO_BINARY = "AUTO_BINARY"
    AUTO_CONTINUOUS = "AUTO_CONTINUOUS"
    HR_RUBRIC = "HR_RUBRIC"
    HR_PASS_FAIL = "HR_PASS_FAIL"


class RunStatus(StrEnum):
    PENDING = "PENDING"
    AUTO_SCORED = "AUTO_SCORED"
    AWAITING_HR = "AWAITING_HR"
    ADJUDICATION = "ADJUDICATION"
    SCORED = "SCORED"
    ERROR = "ERROR"


@dataclass(frozen=True)
class RubricDimension:
    """A single scorable dimension, mirroring a ``scoring_rubrics`` row."""

    deliverable_id: str
    dimension_key: str
    dimension_label: str
    kind: DimensionKind
    max_score: float = 1.0
    threshold: float | None = None
    threshold_op: str | None = None
    weight: float = 1.0
    tool: str | None = None

    @property
    def is_auto(self) -> bool:
        return self.kind in (DimensionKind.AUTO_BINARY, DimensionKind.AUTO_CONTINUOUS)

    @property
    def is_hr(self) -> bool:
        return self.kind in (DimensionKind.HR_RUBRIC, DimensionKind.HR_PASS_FAIL)


@dataclass
class DimensionResult:
    dimension_key: str
    kind: DimensionKind
    score: float          # contribution in [0, max_score]
    max_score: float
    norm: float           # normalised contribution in [0, 1]
    weight: float
    passed: bool | None = None
    raw_value: float | None = None
    detail: str = ""


@dataclass(frozen=True)
class DeliverableSpec:
    """Subset of a ``deliverables`` row needed to drive scoring."""

    deliverable_id: str
    role_code: str
    scoring_type: str          # 'AUTO' | 'HR' | 'HYB'
    auto_weight: float
    hr_weight: float
    composite_weight: float
    scorer_key: str            # 'metrics_manifest' | 'human_review_only' | 'schema:OCM' ...
    schema_ref: str | None = None
    min_sample: int = 30


@dataclass
class ScoreResult:
    deliverable_id: str
    status: RunStatus
    auto_score: float | None = None       # 0–100
    hr_score: float | None = None          # 0–100
    composite_score: float | None = None   # 0–100
    dimensions: list[DimensionResult] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    hard_block: bool = False                  # e.g. OCM flash/ram budget FAIL (V-OCM-14)
    schema_report: dict | None = None      # full ValidationReport.to_dict() for schema scorers

    def to_detail_json(self) -> dict[str, Any]:
        return {
            "auto_score": self.auto_score,
            "hr_score": self.hr_score,
            "composite_score": self.composite_score,
            "hard_block": self.hard_block,
            "schema_report": self.schema_report,
            "messages": self.messages,
            "dimensions": [
                {
                    "dimension_key": d.dimension_key,
                    "kind": d.kind.value,
                    "score": round(d.score, 4),
                    "max_score": d.max_score,
                    "norm": round(d.norm, 4),
                    "weight": d.weight,
                    "passed": d.passed,
                    "raw_value": d.raw_value,
                    "detail": d.detail,
                }
                for d in self.dimensions
            ],
        }


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def normalise_continuous(value: float, threshold: float, op: str, tol: float = 1e-9) -> float:
    """Return a [0,1] normalisation of a continuous measurement vs its threshold."""
    if threshold is None:
        raise ValueError("AUTO_CONTINUOUS dimension requires a threshold")
    if op in (">=", ">"):
        if threshold == 0:
            return 1.0 if value >= 0 else 0.0
        return clamp(value / threshold)
    if op in ("<=", "<"):
        # lower-is-better: full credit at or below threshold, decaying above
        if value <= 0:
            return 1.0
        return clamp(threshold / value)
    if op == "==":
        return 1.0 if abs(value - threshold) <= tol else 0.0
    raise ValueError(f"unsupported threshold_op: {op!r}")


def weighted_subscore(results: list[DimensionResult]) -> float | None:
    """Combine dimension norms into a 0–100 sub-score by weight. None if empty."""
    contributing = [r for r in results if r.weight > 0]
    if not contributing:
        return None
    total_w = sum(r.weight for r in contributing)
    if total_w <= 0:
        return None
    return 100.0 * sum(r.norm * r.weight for r in contributing) / total_w


def combine_composite(
    scoring_type: str,
    auto_weight: float,
    hr_weight: float,
    auto_score: float | None,
    hr_score: float | None,
) -> float | None:
    """Hybrid composite (spec §4.4): auto_weight*auto + hr_weight*hr."""
    if scoring_type == "AUTO":
        return auto_score
    if scoring_type == "HR":
        return hr_score
    # HYB
    if auto_score is None or hr_score is None:
        return None
    return auto_weight * auto_score + hr_weight * hr_score
