"""Evaluation Harness — AI agent performance measurement.

Implements docs/evaluation/EVALUATION_HARNESS_SPEC.md (v1.0.0). The package is
deliberately layered so the scoring/statistics core has no database or web
dependency and can be unit-tested with the standard library alone:

    scoring/   pure-Python scorers + schema validators (ADR/CCR/DQIR/IRD/OCM)
    stats/     pure-Python statistics (percentiles, Fleiss' kappa, ICC, Welch t)
    db/ via db.py    psycopg2 persistence layer (optional at import time)
    api/       FastAPI ingest + review portal (optional at import time)
    cli/       baseline-capture and agent-evaluation entry points
    pipeline/  the scheduled statistical engine job
"""
from .version import ENGINE_VERSION, __version__

__all__ = ["__version__", "ENGINE_VERSION"]
