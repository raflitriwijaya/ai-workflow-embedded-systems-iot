"""OCM (OTA Compatibility Manifest) validator — docs/schemas/OTA_COMPATIBILITY_MANIFEST_SCHEMA.md.

Encodes V-OCM-01 .. V-OCM-16. This validator is the auto-scorer for deliverable
D1-ML-4 (OTA-Ready Model Artifact). A flash/RAM budget FAIL (V-OCM-14) is a hard
block: the manifest is schema-valid but OTA dispatch is halted pending human
approval (spec §8.1 OCM gating; OTA Governance §8.1).
"""
from __future__ import annotations

import re
from typing import Any

from .common import ValidationReport, approx, enum_value, get, is_hex64, is_list, semver_tuple

DQIR_ID = re.compile(r"^DQIR-\d{4}$")
FRAMEWORK = {"TFLITE", "TFLITE_MICRO", "ONNX", "PYTORCH_MOBILE", "CUSTOM"}
QUANT = {"FLOAT32", "FLOAT16", "INT8", "INT4", "BINARY", "NONE"}


def validate(data: dict[str, Any], known_dqir: dict[str, str] | None = None) -> ValidationReport:
    r = ValidationReport(schema="OCM")

    r.check("V-OCM-01", is_hex64(get(data, "model.sha256_hash")), "model.sha256_hash must be 64 hex chars")
    r.check("V-OCM-02", enum_value(get(data, "model.framework")) in FRAMEWORK, "model.framework invalid")
    r.check("V-OCM-03", enum_value(get(data, "model.quantization")) in QUANT, "model.quantization invalid")

    targets = get(data, "target_hardware", [])
    r.check("V-OCM-04",
            is_list(targets, 1) and any(t.get("validated") is True for t in targets if isinstance(t, dict)),
            "≥1 target_hardware entry with validated=true")

    fr = get(data, "resource_budget.flash_required_bytes")
    fb = get(data, "resource_budget.flash_budget_bytes")
    fpct = get(data, "resource_budget.flash_budget_utilisation_pct")
    if isinstance(fr, (int, float)) and isinstance(fb, (int, float)) and fb:
        r.check("V-OCM-05", approx(fpct, fr / fb * 100.0, 0.1),
                "flash_budget_utilisation_pct mismatch")
    else:
        r.check("V-OCM-05", False, "flash_required_bytes/flash_budget_bytes missing or zero")

    rp = get(data, "resource_budget.ram_peak_bytes")
    rb = get(data, "resource_budget.ram_budget_bytes")
    rpct = get(data, "resource_budget.ram_budget_utilisation_pct")
    if isinstance(rp, (int, float)) and isinstance(rb, (int, float)) and rb:
        r.check("V-OCM-06", approx(rpct, rp / rb * 100.0, 0.1), "ram_budget_utilisation_pct mismatch")
    else:
        r.check("V-OCM-06", False, "ram_peak_bytes/ram_budget_bytes missing or zero")

    flash_result = enum_value(get(data, "flash_budget_check.result"))
    if isinstance(fpct, (int, float)):
        r.check("V-OCM-07", (flash_result == "PASS") == (fpct <= 80), "flash result PASS iff util ≤80")
        r.check("V-OCM-08", (flash_result == "WARN") == (80 < fpct <= 95), "flash result WARN iff 80<util≤95")
        r.check("V-OCM-09", (flash_result == "FAIL") == (fpct > 95), "flash result FAIL iff util >95")
    else:
        r.check("V-OCM-07", False, "flash utilisation not numeric")
        r.check("V-OCM-08", False, "flash utilisation not numeric")
        r.check("V-OCM-09", False, "flash utilisation not numeric")

    margin = get(data, "flash_budget_check.margin_bytes")
    if isinstance(fr, (int, float)) and isinstance(fb, (int, float)):
        r.check("V-OCM-10", approx(margin, fb - fr, 0.5), "flash margin_bytes must equal budget − required")
    else:
        r.check("V-OCM-10", False, "cannot verify flash margin (missing byte values)")

    bundle = get(data, "bundle_contents", [])
    bundle_ok = is_list(bundle, 1) and all(
        is_hex64(b.get("sha256_hash")) for b in bundle if isinstance(b, dict)
    )
    r.check("V-OCM-11", bundle_ok, "each bundle_contents sha256_hash must be 64 hex chars")

    sig = get(data, "security.bundle_signature")
    r.check("V-OCM-12", isinstance(sig, str) and len(sig.strip()) > 0, "security.bundle_signature must be non-empty")

    rollout = enum_value(get(data, "deployment.rollout_strategy"))
    if rollout == "CANARY":
        canary = get(data, "deployment.canary_percentage")
        r.check("V-OCM-13", isinstance(canary, int) and 1 <= canary <= 100,
                "canary_percentage must be in [1,100] for CANARY")

    # V-OCM-14: a FAIL budget is a valid-but-blocked manifest (hard block, not invalid).
    ram_result = enum_value(get(data, "ram_budget_check.result"))
    budget_fail = flash_result == "FAIL" or ram_result == "FAIL"
    r.check("V-OCM-14", True if not budget_fail else False,
            "budget FAIL → OTA dispatch blocked, human approval required" if budget_fail
            else "budgets within limits",
            hard_block=budget_fail)

    clearance = get(data, "dqir_clearance", [])
    if isinstance(clearance, list):
        if known_dqir is not None:
            ok = all(known_dqir.get(cid) in ("CORRECTED", "ACCEPTED") for cid in clearance)
            r.check("V-OCM-15", ok, "every dqir_clearance ID must be CORRECTED/ACCEPTED in registry")
        else:
            ok = all(isinstance(cid, str) and bool(DQIR_ID.match(cid)) for cid in clearance)
            r.check("V-OCM-15", ok, "dqir_clearance IDs must match ^DQIR-\\d{4}$ (registry status checked at ingest)")
    else:
        r.check("V-OCM-15", False, "dqir_clearance must be a list (empty allowed)")

    min_v = semver_tuple(get(data, "firmware_compatibility.minimum_version"))
    excluded = get(data, "firmware_compatibility.excluded_versions", []) or []
    if min_v is not None and excluded:
        ok = all((semver_tuple(v) or (0, 0, 0)) >= min_v for v in excluded)
        r.check("V-OCM-16", ok, "excluded_versions must lie within the compatibility range (≥ minimum_version)")
    else:
        r.check("V-OCM-16", True, "no excluded versions to range-check")

    return r
