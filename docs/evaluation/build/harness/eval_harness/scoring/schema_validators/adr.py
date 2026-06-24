"""ADR (Architecture Decision Record) validator — docs/schemas/ADR_SCHEMA.md.

Encodes validation rules V-ADR-01 .. V-ADR-12 plus the schema's required
minimum-character content fields. Used both as a standalone deliverable scorer
(D4-AR-1) and as the auto sub-score basis for ADR submissions.
"""
from __future__ import annotations

import re
from typing import Any

from .common import (
    ValidationReport,
    date_le,
    enum_value,
    get,
    is_list,
    min_chars,
)

ADR_ID = re.compile(r"^ADR-\d{4}$")
STATUS = {"PROPOSED", "DECIDED", "DEPRECATED", "SUPERSEDED", "REJECTED"}
DECISION_CLASS = {"STRATEGIC", "TACTICAL", "LOCAL"}
TIER = {
    "HARDWARE", "FIRMWARE", "EMBEDDED-SOFTWARE", "EDGE-AI", "CONNECTIVITY",
    "CLOUD-BACKEND", "DATA-PIPELINE", "SECURITY", "DEVOPS", "CROSS-CUTTING",
}
RECO = {"PROCEED", "PROCEED_WITH_MITIGATION", "REJECT"}
ARCHITECT = "EMBEDDED_SYSTEMS_ARCHITECT_SKILL"


def validate(data: dict[str, Any]) -> ValidationReport:
    r = ValidationReport(schema="ADR")
    status = enum_value(get(data, "status"))
    dclass = enum_value(get(data, "decision_class"))
    options = get(data, "options_considered", [])

    r.check("V-ADR-01", isinstance(data.get("id"), str) and bool(ADR_ID.match(data["id"])),
            "id must match ^ADR-\\d{4}$")
    r.check("V-ADR-02", status in STATUS, f"status {status!r} not in {sorted(STATUS)}")
    r.check("V-ADR-03", dclass in DECISION_CLASS, f"decision_class {dclass!r} invalid")
    r.check("V-ADR-04", enum_value(get(data, "tier")) in TIER, "tier invalid")
    r.check("V-ADR-05", is_list(options, 2), "options_considered needs ≥2 entries")

    each_ok = is_list(options) and all(
        is_list(o.get("pros"), 1) and is_list(o.get("cons"), 1)
        for o in options if isinstance(o, dict)
    )
    r.check("V-ADR-06", bool(options) and each_ok, "each option needs ≥1 pro and ≥1 con")

    if status == "DECIDED":
        approvers = get(data, "approvers", [])
        has_approval = is_list(approvers) and any(
            isinstance(a, dict) and a.get("approved") is True for a in approvers
        )
        r.check("V-ADR-07", data.get("date_decided") and has_approval,
                "DECIDED requires date_decided and ≥1 approver approved=true")

    if status == "SUPERSEDED":
        sb = data.get("superseded_by")
        r.check("V-ADR-08", isinstance(sb, str) and bool(ADR_ID.match(sb)),
                "SUPERSEDED requires superseded_by matching ^ADR-\\d{4}$")

    if dclass == "STRATEGIC":
        approvers = get(data, "approvers", [])
        arch_ok = is_list(approvers) and any(
            ARCHITECT in str(a.get("role", "")) for a in approvers if isinstance(a, dict)
        )
        r.check("V-ADR-09", arch_ok, "STRATEGIC ADR requires an Architect approver")

    r.check("V-ADR-10",
            min_chars(get(data, "context"), 50)
            and min_chars(get(data, "problem_statement"), 30)
            and min_chars(get(data, "decision"), 50)
            and min_chars(get(data, "rationale"), 50)
            and min_chars(get(data, "consequences"), 30),
            "context/problem/decision/rationale/consequences below minimum length")

    r.check("V-ADR-11", date_le(data.get("date_created"), data.get("date_decided")),
            "date_created must be ≤ date_decided")

    bia_reco = get(data, "business_impact_assessment.recommendation")
    if bia_reco is not None:
        r.check("V-ADR-12", bia_reco in RECO, f"BIA recommendation {bia_reco!r} invalid")

    return r
