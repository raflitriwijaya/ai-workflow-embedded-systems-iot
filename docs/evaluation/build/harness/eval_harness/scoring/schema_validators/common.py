"""Shared helpers for the machine-parseable schema validators (docs/schemas/).

Each validator consumes an already-parsed mapping (so it is testable without a
YAML dependency) and returns a :class:`ValidationReport`. The auto sub-score for
a schema-validated deliverable is ``pass_pct`` = passed rules / total rules.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+")


@dataclass
class RuleResult:
    rule_id: str
    passed: bool
    message: str = ""
    # A failed rule may be a *hard block* (e.g. budget FAIL) rather than merely
    # lowering the score. Hard blocks propagate to ScoreResult.hard_block.
    hard_block: bool = False


@dataclass
class ValidationReport:
    schema: str
    results: list[RuleResult] = field(default_factory=list)

    def check(self, rule_id: str, condition: bool, message: str = "", *, hard_block: bool = False) -> bool:
        self.results.append(
            RuleResult(rule_id=rule_id, passed=bool(condition), message=message, hard_block=hard_block)
        )
        return bool(condition)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def pass_pct(self) -> float:
        if not self.results:
            return 0.0
        return 100.0 * self.passed / self.total

    @property
    def hard_block(self) -> bool:
        # A hard block is any rule explicitly flagged as triggering a downstream
        # STOP — OCM budget FAIL halting dispatch, a BLOCKING CCR holding an IRD
        # gate, a CRITICAL/HIGH DQIR blocking the training pipeline. Validators
        # set the flag only on the branch where the block is actually active, so
        # the flag itself is authoritative (independent of pass/fail).
        return any(r.hard_block for r in self.results)

    def failures(self) -> list[RuleResult]:
        return [r for r in self.results if not r.passed]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "pass_pct": round(self.pass_pct, 2),
            "passed": self.passed,
            "total": self.total,
            "hard_block": self.hard_block,
            "failures": [
                {"rule": r.rule_id, "message": r.message, "hard_block": r.hard_block}
                for r in self.failures()
            ],
        }


# ── small typed accessors ─────────────────────────────────────────────────────
def get(d: Any, path: str, default: Any = None) -> Any:
    """Dotted-path getter tolerant of missing keys / non-dict nodes."""
    node = d
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    return node


def is_list(value: Any, min_len: int = 0) -> bool:
    return isinstance(value, list) and len(value) >= min_len


def is_nonempty_str(value: Any, min_len: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= min_len


def min_chars(value: Any, n: int) -> bool:
    return isinstance(value, str) and len(value.strip()) >= n


def is_hex64(value: Any) -> bool:
    return isinstance(value, str) and bool(HEX64.match(value))


def enum_value(node: Any) -> Any:
    """Schemas sometimes render an enum as a scalar ('HIGH') and sometimes as a
    typed block ({'type': 'HIGH', ...}). Normalise to the scalar value."""
    if isinstance(node, dict) and "type" in node:
        return node["type"]
    return node


def enum_ok(value: Any, allowed: set[str]) -> bool:
    return enum_value(value) in allowed


def parse_date(value: Any) -> date | None:
    if isinstance(value, (date, datetime)):
        return value.date() if isinstance(value, datetime) else value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def date_le(a: Any, b: Any) -> bool:
    """True if both dates parse and a <= b, OR either is absent (rule N/A)."""
    da, db = parse_date(a), parse_date(b)
    if da is None or db is None:
        return True
    return da <= db


def semver_tuple(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", value)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def approx(a: float, b: float, tol: float) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False
