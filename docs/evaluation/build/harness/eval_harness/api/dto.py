"""Pydantic request/response models for the Ingest + Review API (spec §6.1)."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SubmissionRequest(BaseModel):
    role_code: str = Field(..., examples=["DATA", "FE", "MLOPS"])
    deliverable_id: str = Field(..., examples=["D1-DE-1"])
    producer_type: str = Field(..., pattern="^(HUMAN|AGENT)$")
    artifact_uri: str = Field(..., examples=["s3://eval-harness/submissions/TASK-4421/D1-DE-1.zip"])

    # AUTO scoring input: the CI tool metrics manifest (dimension_key -> value).
    metrics: dict[str, Any] | None = None

    # Baseline-capture metadata
    is_baseline: bool = False
    human_producer_id: str | None = None
    time_spent_minutes: int | None = Field(default=None, ge=0)
    complexity_rating: int | None = Field(default=None, ge=1, le=5)

    # Agent-submission metadata (spec §6.1)
    agent_id: str | None = None
    task_id: str | None = None
    human_reviewer_id: str | None = None
    human_accepted: bool | None = None
    human_edit_required: bool | None = None
    edit_effort_minutes: int | None = Field(default=None, ge=0)

    metadata_json: dict[str, Any] | None = None


class SubmissionResponse(BaseModel):
    submission_id: str
    blind_token: str
    run_id: str
    status: str
    auto_score: float | None = None
    hr_score: float | None = None
    composite_score: float | None = None
    hard_block: bool = False
    messages: list[str] = []


class ReviewRequest(BaseModel):
    blind_token: str
    reviewer_id: str
    # dimension_key -> 0–3 rubric score (or 0/1 for pass-fail dimensions)
    dim_scores: dict[str, float]
    is_adjudicator: bool = False


class ReviewResponse(BaseModel):
    run_id: str
    status: str
    hr_score: float | None = None
    composite_score: float | None = None


class QueueItem(BaseModel):
    blind_token: str
    deliverable_id: str
    role_code: str
    artifact_uri: str
    status: str
