"""Machine-parseable schema validators for the governance artifacts.

Each module exposes ``validate(data: dict, ...) -> ValidationReport`` encoding the
``V-<SCHEMA>-NN`` rules from the corresponding docs/schemas/*.md file. The
``SCHEMA_VALIDATORS`` registry maps a schema key to its callable so the scorer
registry can dispatch ``scorer_key='schema:OCM'`` etc.
"""
from __future__ import annotations

from collections.abc import Callable

from . import adr, ccr, dqir, ird, ocm
from .common import RuleResult, ValidationReport

SCHEMA_VALIDATORS: dict[str, Callable[..., ValidationReport]] = {
    "ADR": adr.validate,
    "CCR": ccr.validate,
    "DQIR": dqir.validate,
    "IRD": ird.validate,
    "OCM": ocm.validate,
}

__all__ = ["SCHEMA_VALIDATORS", "ValidationReport", "RuleResult", "adr", "ccr", "dqir", "ird", "ocm"]
