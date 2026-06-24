"""CCR (Contract Clarification Record) validator — docs/schemas/CCR_SCHEMA.md.

Encodes V-CCR-01 .. V-CCR-11. Rules that require live registry/time-window
state (V-CCR-02 registry membership, V-CCR-09 10-business-day contract bump) are
evaluated structurally here and resolved fully at the ingest layer when a
``known_contract_ids`` set is supplied.
"""
from __future__ import annotations

import re
from typing import Any

from .common import ValidationReport, date_le, enum_value, get, min_chars

CCR_ID = re.compile(r"^CCR-\d{4}$")
ADR_ID = re.compile(r"^ADR-\d{4}$")
AMBIGUITY = {"MISSING_FIELD", "CONFLICTING_VALUES", "UNCLEAR_SEMANTICS", "MISSING_CONSTRAINT", "SCOPE_BOUNDARY"}
SEVERITY = {"BLOCKING", "HIGH", "MEDIUM", "LOW"}
STATUS = {"OPEN", "IN_REVIEW", "RESOLVED", "CLOSED", "WONTFIX"}
RES_TYPE = {"CONTRACT_UPDATE", "ADR_REQUIRED", "PROCESS_CHANGE", "ACCEPTED_AMBIGUITY"}


def validate(data: dict[str, Any], known_contract_ids: set[str] | None = None) -> ValidationReport:
    r = ValidationReport(schema="CCR")
    status = enum_value(get(data, "status"))
    severity = enum_value(get(data, "severity"))
    contract_id = get(data, "contract_reference.contract_id")
    resolution = get(data, "resolution") or {}

    r.check("V-CCR-01", isinstance(data.get("id"), str) and bool(CCR_ID.match(data["id"])),
            "id must match ^CCR-\\d{4}$")

    if known_contract_ids is not None:
        r.check("V-CCR-02", contract_id in known_contract_ids,
                f"contract_id {contract_id!r} not in registry")
    else:
        r.check("V-CCR-02", isinstance(contract_id, str) and "↔" in contract_id,
                "contract_id must be a registry key 'ROLE↔ROLE-NNN' (registry resolution deferred)")

    r.check("V-CCR-03", enum_value(get(data, "ambiguity_class")) in AMBIGUITY, "ambiguity_class invalid")
    r.check("V-CCR-04", severity in SEVERITY, f"severity {severity!r} invalid")
    r.check("V-CCR-05", status in STATUS, f"status {status!r} invalid")

    if status in ("RESOLVED", "CLOSED"):
        populated = (
            min_chars(resolution.get("agreed_clarification"), 30)
            and enum_value(resolution.get("resolution_type")) in RES_TYPE
            and isinstance(resolution.get("contract_update_required"), bool)
            and isinstance(resolution.get("adr_required"), bool)
        )
        r.check("V-CCR-06", populated, "RESOLVED/CLOSED requires a fully populated resolution block")

    if status == "CLOSED":
        sigs = get(data, "signatories", [])
        signed_roles = {str(s.get("role")) for s in sigs if isinstance(s, dict) and s.get("signed") is True}
        prod, cons = str(get(data, "producer_role")), str(get(data, "consumer_role"))
        r.check("V-CCR-07", prod in signed_roles and cons in signed_roles,
                "CLOSED requires both producer_role and consumer_role signed=true")

    if resolution.get("adr_required") is True:
        linked = resolution.get("linked_adr")
        r.check("V-CCR-08", isinstance(linked, str) and bool(ADR_ID.match(linked)),
                "adr_required=true needs linked_adr matching ^ADR-\\d{4}$")

    if resolution.get("contract_update_required") is True:
        # Full V-CCR-09 (version bump within 10 business days) is a time-window
        # check done at ingest; structurally we require the resolution be present.
        r.check("V-CCR-09", bool(resolution.get("agreed_clarification")),
                "contract_update_required=true: resolution recorded (10-day bump verified at ingest)")

    r.check("V-CCR-10", date_le(data.get("date_raised"), data.get("date_resolved")),
            "date_raised must be ≤ date_resolved")

    # V-CCR-11: BLOCKING + still open is a *valid* artifact state (the gate hold is
    # enforced elsewhere); flag it as a hard block rather than an invalidity.
    if severity == "BLOCKING" and status in ("OPEN", "IN_REVIEW"):
        r.check("V-CCR-11", True, "BLOCKING CCR open — associated IRD gate is held",
                hard_block=True)

    # Required content presence (schema "(required) ≥N chars").
    r.check("REQ-ambiguity_description", min_chars(get(data, "ambiguity_description"), 50),
            "ambiguity_description ≥50 chars required")
    r.check("REQ-impact_if_unresolved", min_chars(get(data, "impact_if_unresolved"), 30),
            "impact_if_unresolved ≥30 chars required")
    r.check("REQ-proposed_clarification", min_chars(get(data, "proposed_clarification"), 30),
            "proposed_clarification ≥30 chars required")

    return r
