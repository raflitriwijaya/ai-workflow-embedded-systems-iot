"""IRD (Integration Readiness Declaration) validator — docs/schemas/INTEGRATION_READINESS_DECLARATION_SCHEMA.md.

Encodes V-IRD-01 .. V-IRD-13.
"""
from __future__ import annotations

import re
from typing import Any

from .common import ValidationReport, enum_value, get, is_list

IRD_ID = re.compile(r"^IRD-\d{4}$")
GATE = {"PASS", "PASS_WITH_WAIVER", "FAIL", "INCOMPLETE"}
ATTEST = {"READY", "NOT_READY", "READY_WITH_CONDITIONS"}


def validate(data: dict[str, Any], known_contract_ids: set[str] | None = None) -> ValidationReport:
    r = ValidationReport(schema="IRD")
    gate = enum_value(get(data, "gate_result"))
    scenarios = get(data, "test_scenarios", [])
    contract_id = get(data, "contract.contract_id")

    r.check("V-IRD-01", isinstance(data.get("id"), str) and bool(IRD_ID.match(data["id"])),
            "id must match ^IRD-\\d{4}$")

    if known_contract_ids is not None:
        r.check("V-IRD-02", contract_id in known_contract_ids, "contract_id not in registry")
    else:
        r.check("V-IRD-02", isinstance(contract_id, str) and "↔" in contract_id,
                "contract_id must be a registry key (resolution deferred to ingest)")

    open_ccrs = get(data, "contract.open_ccrs", None)
    if gate == "PASS":
        # Validity rule (not a downstream block): a PASS with open CCRs is simply
        # invalid — the BLOCKING-CCR gate hold is surfaced on the CCR side.
        r.check("V-IRD-03", isinstance(open_ccrs, list) and len(open_ccrs) == 0,
                "gate PASS requires contract.open_ccrs empty")

    r.check("V-IRD-04", gate in GATE, f"gate_result {gate!r} invalid")

    mandatory = [s for s in scenarios if isinstance(s, dict) and s.get("mandatory")]
    if gate == "PASS":
        all_mand_pass = bool(scenarios) and all(s.get("result") == "PASS" for s in mandatory)
        failed = get(data, "metrics.failed_scenarios", 0)
        r.check("V-IRD-05", failed == 0 and all_mand_pass,
                "PASS requires failed_scenarios=0 and all mandatory scenarios PASS")
    if gate == "FAIL":
        r.check("V-IRD-06", any(s.get("result") == "FAIL" for s in mandatory),
                "FAIL requires ≥1 mandatory scenario with result FAIL")
    if gate == "PASS_WITH_WAIVER":
        r.check("V-IRD-07", is_list(get(data, "waivers"), 1),
                "PASS_WITH_WAIVER requires a non-empty waivers list")

    scenario_ids = {s.get("id") for s in scenarios if isinstance(s, dict)}
    waivers = get(data, "waivers", []) or []
    waivers_ok = all(w.get("scenario_id") in scenario_ids for w in waivers if isinstance(w, dict))
    r.check("V-IRD-08", waivers_ok, "each waiver.scenario_id must match a test scenario id")

    sigs = get(data, "signatories", [])
    signed_roles = {str(s.get("role")) for s in sigs if isinstance(s, dict) and s.get("signed") is True}
    prod, cons = str(get(data, "producer_role")), str(get(data, "consumer_role"))
    r.check("V-IRD-09", prod in signed_roles and cons in signed_roles,
            "both producer_role and consumer_role must sign")

    p = get(data, "metrics.passed_scenarios", 0)
    f = get(data, "metrics.failed_scenarios", 0)
    sk = get(data, "metrics.skipped_scenarios", 0)
    ex = get(data, "metrics.executed_scenarios", 0)
    r.check("V-IRD-10", (p + f + sk) == ex, "passed+failed+skipped must equal executed_scenarios")

    if gate in ("FAIL", "PASS_WITH_WAIVER"):
        r.check("V-IRD-11", get(data, "architect_review.reviewed") is True,
                "FAIL/PASS_WITH_WAIVER requires architect_review.reviewed=true")

    attest_ok = all(
        enum_value(s.get("attestation")) in ATTEST for s in sigs if isinstance(s, dict)
    )
    r.check("V-IRD-12", bool(sigs) and attest_ok, "every signatory attestation must be a valid enum")

    has_security = any(
        enum_value(s.get("scenario_type")) == "SECURITY" for s in scenarios if isinstance(s, dict)
    )
    r.check("V-IRD-13", has_security, "≥1 SECURITY scenario required (IEC 62443-4-1 §SVV-3)")

    return r
