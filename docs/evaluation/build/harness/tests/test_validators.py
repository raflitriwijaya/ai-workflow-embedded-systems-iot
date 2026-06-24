"""Schema-validator tests — fixtures mirror the docs/schemas/*.md example
instances and exercise each V-rule's failure path."""
from __future__ import annotations

from eval_harness.scoring.schema_validators import adr, ccr, dqir, ird, ocm

HEX64 = "a" * 64
ARCH = "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
FW = "[[FIRMWARE_ENGINEER_SKILL]]"
BACK = "[[BACKEND_CLOUD_ENGINEER_SKILL]]"


def _valid_adr() -> dict:
    return {
        "id": "ADR-0007",
        "status": "DECIDED",
        "decision_class": "STRATEGIC",
        "tier": "SECURITY",
        "date_created": "2026-04-10",
        "date_decided": "2026-04-18",
        "approvers": [{"role": ARCH, "approved": True, "date": "2026-04-18"}],
        "options_considered": [
            {"id": "A", "description": "x" * 25, "pros": ["p"], "cons": ["c"]},
            {"id": "B", "description": "y" * 25, "pros": ["p"], "cons": ["c"]},
        ],
        "context": "c" * 60,
        "problem_statement": "p" * 40,
        "decision": "d" * 60,
        "rationale": "r" * 60,
        "consequences": "q" * 40,
        "business_impact_assessment": {"recommendation": "PROCEED"},
    }


def test_adr_valid_passes_all():
    r = adr.validate(_valid_adr())
    assert r.pass_pct == 100.0, r.to_dict()
    assert not r.hard_block


def test_adr_strategic_without_architect_fails_v09():
    data = _valid_adr()
    data["approvers"] = [{"role": FW, "approved": True, "date": "2026-04-18"}]
    r = adr.validate(data)
    assert any(f.rule_id == "V-ADR-09" for f in r.failures())


def test_adr_single_option_fails_v05():
    data = _valid_adr()
    data["options_considered"] = [data["options_considered"][0]]
    r = adr.validate(data)
    assert any(f.rule_id == "V-ADR-05" for f in r.failures())


def _valid_ccr() -> dict:
    return {
        "id": "CCR-0012",
        "date_raised": "2026-05-03",
        "date_resolved": "2026-05-09",
        "contract_reference": {"contract_id": "FW↔CLOUD-MQTT-001"},
        "producer_role": FW,
        "consumer_role": BACK,
        "ambiguity_class": "MISSING_CONSTRAINT",
        "severity": "BLOCKING",
        "status": "CLOSED",
        "ambiguity_description": "a" * 55,
        "impact_if_unresolved": "i" * 35,
        "proposed_clarification": "p" * 35,
        "resolution": {
            "agreed_clarification": "g" * 35,
            "resolution_type": "CONTRACT_UPDATE",
            "contract_update_required": True,
            "adr_required": False,
        },
        "signatories": [
            {"role": FW, "signed": True}, {"role": BACK, "signed": True},
        ],
    }


def test_ccr_valid_passes_all():
    r = ccr.validate(_valid_ccr())
    assert r.pass_pct == 100.0, r.to_dict()


def test_ccr_closed_missing_signatory_fails_v07():
    data = _valid_ccr()
    data["signatories"] = [{"role": FW, "signed": True}]
    r = ccr.validate(data)
    assert any(f.rule_id == "V-CCR-07" for f in r.failures())


def test_ccr_blocking_open_is_hard_block():
    data = _valid_ccr()
    data["status"] = "OPEN"
    data.pop("date_resolved")
    r = ccr.validate(data)
    assert r.hard_block  # BLOCKING + open holds the IRD gate


def _valid_dqir() -> dict:
    return {
        "id": "DQIR-0008",
        "dataset": {"collection_window": {"start": "2026-04-01T00:00:00Z", "end": "2026-04-30T23:59:59Z"}},
        "affected_features": [{"feature_name": "x", "sample_bad_values": ["NaN", "NaN"]}],
        "issue_type": "MISSING_VALUES",
        "severity": "HIGH",
        "quality_dimension": "COMPLETENESS",
        "correction_status": "IN_PROGRESS",
        "metrics": {"total_rows_inspected": 600000, "affected_rows": 142800, "affected_row_percentage": 23.8},
        "training_pipeline_blocked": True,
    }


def test_dqir_valid_passes_all():
    r = dqir.validate(_valid_dqir())
    assert r.pass_pct == 100.0, r.to_dict()


def test_dqir_high_severity_unblocked_fails_v08():
    data = _valid_dqir()
    data["training_pipeline_blocked"] = False
    r = dqir.validate(data)
    assert any(f.rule_id == "V-DQIR-08" for f in r.failures())


def test_dqir_bad_arithmetic_fails_v07():
    data = _valid_dqir()
    data["metrics"]["affected_row_percentage"] = 50.0
    r = dqir.validate(data)
    assert any(f.rule_id == "V-DQIR-07" for f in r.failures())


def _valid_ird() -> dict:
    scen = lambda i, t, m, res: {  # noqa: E731
        "id": f"TS-00{i}", "description": "d" * 25, "scenario_type": t,
        "mandatory": m, "executed": True, "result": res,
    }
    return {
        "id": "IRD-0018",
        "contract": {"contract_id": "FW↔CLOUD-MQTT-001", "open_ccrs": []},
        "producer_role": FW,
        "consumer_role": BACK,
        "gate_result": "PASS",
        "test_scenarios": [
            scen(1, "HAPPY_PATH", True, "PASS"),
            scen(2, "ERROR", True, "PASS"),
            scen(3, "SECURITY", True, "PASS"),
        ],
        "waivers": [],
        "metrics": {"total_scenarios": 3, "executed_scenarios": 3, "passed_scenarios": 3,
                    "failed_scenarios": 0, "skipped_scenarios": 0},
        "signatories": [
            {"role": FW, "signed": True, "attestation": "READY"},
            {"role": BACK, "signed": True, "attestation": "READY"},
        ],
    }


def test_ird_valid_passes_all():
    r = ird.validate(_valid_ird())
    assert r.pass_pct == 100.0, r.to_dict()


def test_ird_pass_with_open_ccr_fails_v03():
    data = _valid_ird()
    data["contract"]["open_ccrs"] = ["CCR-0099"]
    r = ird.validate(data)
    assert any(f.rule_id == "V-IRD-03" for f in r.failures())


def test_ird_without_security_scenario_fails_v13():
    data = _valid_ird()
    for s in data["test_scenarios"]:
        if s["scenario_type"] == "SECURITY":
            s["scenario_type"] = "ERROR"
    r = ird.validate(data)
    assert any(f.rule_id == "V-IRD-13" for f in r.failures())


def _valid_ocm(util_pct: float = 35.6) -> dict:
    flash_budget = 524288
    flash_required = int(round(flash_budget * util_pct / 100.0))
    result = "PASS" if util_pct <= 80 else ("WARN" if util_pct <= 95 else "FAIL")
    return {
        "model": {"sha256_hash": HEX64, "framework": "TFLITE_MICRO", "quantization": "INT8"},
        "target_hardware": [{"hardware_id": "GW-1", "validated": True}],
        "firmware_compatibility": {"minimum_version": "2.4.2", "excluded_versions": ["2.5.0"]},
        "resource_budget": {
            "flash_required_bytes": flash_required,
            "flash_budget_bytes": flash_budget,
            "flash_budget_utilisation_pct": round(flash_required / flash_budget * 100.0, 4),
            "ram_peak_bytes": 204800,
            "ram_budget_bytes": 327680,
            "ram_budget_utilisation_pct": round(204800 / 327680 * 100.0, 4),
        },
        "flash_budget_check": {"result": result, "margin_bytes": flash_budget - flash_required},
        "ram_budget_check": {"result": "PASS", "margin_bytes": 327680 - 204800},
        "security": {"bundle_signature": "c2lnbmF0dXJl"},
        "deployment": {"rollout_strategy": "CANARY", "canary_percentage": 5},
        "bundle_contents": [{"filename": "m.tflite", "sha256_hash": HEX64, "size_bytes": 1}],
        "dqir_clearance": ["DQIR-0008"],
    }


def test_ocm_valid_passes_all():
    r = ocm.validate(_valid_ocm())
    assert r.pass_pct == 100.0, r.to_dict()
    assert not r.hard_block


def test_ocm_flash_fail_is_hard_block():
    r = ocm.validate(_valid_ocm(util_pct=97.0))
    assert r.hard_block  # V-OCM-14: budget FAIL halts dispatch
    assert any(f.rule_id == "V-OCM-14" for f in r.failures())


def test_ocm_bad_utilisation_arithmetic_fails_v05():
    data = _valid_ocm()
    data["resource_budget"]["flash_budget_utilisation_pct"] = 10.0
    r = ocm.validate(data)
    assert any(f.rule_id == "V-OCM-05" for f in r.failures())
