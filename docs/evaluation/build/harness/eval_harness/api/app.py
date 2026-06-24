"""Ingest Pipeline + Human Review Portal API (FastAPI) — spec §2.2, §6.

Endpoints
---------
POST /api/v1/submissions        ingest + auto-score an artifact (human or agent)
POST /api/v1/reviews            submit a blind human rubric score for a queued item
GET  /api/v1/reviews/queue      items awaiting HR (blind: no producer identity)
GET  /api/v1/readiness/{role}   latest agent-vs-baseline readiness rows
GET  /api/v1/gates/wave/{wave}  WG-1/WG-2 wave activation gate status
POST /api/v1/readiness/recompute  run the statistical engine on demand
GET  /api/v1/progress           baseline sample progress toward ≥30 (DASH-2)
GET  /healthz                   liveness/DB readiness

Blind scoring (spec §6.2) is enforced structurally: the review queue and review
submission never expose producer_type/agent_id/human_producer_id to the reviewer.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .. import service
from ..config import Settings
from ..db import Database
from ..logging_setup import configure_logging
from ..version import __version__
from .dto import (
    QueueItem,
    ReviewRequest,
    ReviewResponse,
    SubmissionRequest,
    SubmissionResponse,
)

LOG = logging.getLogger("harness.api")


def create_app(settings: Settings | None = None, database: Database | None = None) -> FastAPI:
    settings = settings or Settings.load()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging()
        app.state.settings = settings
        app.state.db = database or Database(settings.dsn(), settings.db_min_conn, settings.db_max_conn)
        LOG.info("evaluation harness API %s starting", __version__)
        try:
            yield
        finally:
            if database is None:
                app.state.db.close()

    app = FastAPI(title="Evaluation Harness API", version=__version__, lifespan=lifespan)

    @app.get("/healthz")
    def healthz():
        ok = app.state.db.healthy()
        if not ok:
            raise HTTPException(status_code=503, detail="database unavailable")
        return {"status": "ok", "version": __version__, "blind_scoring": settings.blind_scoring}

    @app.post("/api/v1/submissions", response_model=SubmissionResponse)
    def submit(req: SubmissionRequest):
        try:
            out = service.ingest_submission(
                app.state.db, app.state.settings,
                role_code=req.role_code, deliverable_id=req.deliverable_id,
                producer_type=req.producer_type, artifact_uri=req.artifact_uri,
                metrics=req.metrics, is_baseline=req.is_baseline,
                agent_id=req.agent_id, task_id=req.task_id,
                human_producer_id=req.human_producer_id,
                time_spent_minutes=req.time_spent_minutes, complexity_rating=req.complexity_rating,
                human_reviewer_id=req.human_reviewer_id, human_accepted=req.human_accepted,
                human_edit_required=req.human_edit_required, edit_effort_minutes=req.edit_effort_minutes,
                extra_metadata=req.metadata_json,
            )
            return SubmissionResponse(**out)
        except service.IngestError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # pragma: no cover
            LOG.exception("submission failed")
            raise HTTPException(status_code=500, detail="internal scoring error") from exc

    @app.post("/api/v1/reviews", response_model=ReviewResponse)
    def review(req: ReviewRequest):
        try:
            out = service.submit_review(
                app.state.db, app.state.settings,
                blind_token=req.blind_token, reviewer_id=req.reviewer_id,
                dim_scores=req.dim_scores, is_adjudicator=req.is_adjudicator,
            )
            return ReviewResponse(**out)
        except service.IngestError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/v1/reviews/queue", response_model=list[QueueItem])
    def queue():
        with app.state.db.repository() as repo:
            rows = repo.review_queue()
        # Blind: deliberately omit producer_type / agent_id / human_producer_id.
        return [QueueItem(blind_token=str(r["blind_token"]), deliverable_id=r["deliverable_id"],
                          role_code=r["role_code"], artifact_uri=r["artifact_uri"],
                          status=r["status"]) for r in rows]

    @app.get("/api/v1/readiness/{role_code}")
    def readiness(role_code: str):
        with app.state.db.repository() as repo:
            rows = repo.latest_readiness(role_code.upper())
        if not rows:
            raise HTTPException(status_code=404, detail=f"no readiness data for role {role_code}")
        return {"role_code": role_code.upper(), "rows": rows}

    @app.get("/api/v1/gates/wave/{wave}")
    def wave_gate(wave: int):
        with app.state.db.repository() as repo:
            row = repo.wave_gate(wave)
            progress = repo.sample_progress()
        if not row:
            raise HTTPException(status_code=404, detail=f"no gate data for wave {wave}")
        return {"wave": wave, "gate": row,
                "sample_progress": [p for p in progress]}

    @app.get("/api/v1/progress")
    def progress():
        with app.state.db.repository() as repo:
            return {"progress": repo.sample_progress()}

    @app.post("/api/v1/readiness/recompute")
    def recompute():
        return service.recompute_readiness(app.state.db, app.state.settings)

    return app


# Module-level ASGI app for `uvicorn eval_harness.api.app:app`.
app = create_app()
