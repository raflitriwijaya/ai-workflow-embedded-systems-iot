"""DQIR (Data Quality Issue Report) validator — docs/schemas/DQIR_SCHEMA.md.

Encodes V-DQIR-01 .. V-DQIR-13.
"""
from __future__ import annotations

import re
from typing import Any

from .common import ValidationReport, approx, enum_value, get, is_list, parse_date

DQIR_ID = re.compile(r"^DQIR-\d{4}$")
ISSUE_TYPE = {
    "MISSING_VALUES", "OUT_OF_RANGE", "DISTRIBUTION_DRIFT", "LABEL_INCONSISTENCY",
    "TIMESTAMP_ANOMALY", "SCHEMA_MISMATCH", "SENSOR_FAULT", "PII_LEAKAGE",
}
SEVERITY = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
QUALITY_DIM = {"COMPLETENESS", "ACCURACY", "CONSISTENCY", "TIMELINESS", "VALIDITY", "UNIQUENESS"}
CORRECTION = {"PENDING", "IN_PROGRESS", "CORRECTED", "ACCEPTED", "WONTFIX"}


def validate(data: dict[str, Any]) -> ValidationReport:
    r = ValidationReport(schema="DQIR")
    issue_type = enum_value(get(data, "issue_type"))
    severity = enum_value(get(data, "severity"))
    correction = enum_value(get(data, "correction_status"))
    features = get(data, "affected_features", [])

    r.check("V-DQIR-01", isinstance(data.get("id"), str) and bool(DQIR_ID.match(data["id"])),
            "id must match ^DQIR-\\d{4}$")
    r.check("V-DQIR-02", issue_type in ISSUE_TYPE, f"issue_type {issue_type!r} invalid")
    r.check("V-DQIR-03", severity in SEVERITY, f"severity {severity!r} invalid")
    r.check("V-DQIR-04", enum_value(get(data, "quality_dimension")) in QUALITY_DIM,
            "quality_dimension invalid")
    r.check("V-DQIR-05", correction in CORRECTION, f"correction_status {correction!r} invalid")
    r.check("V-DQIR-06", is_list(features, 1), "affected_features needs ≥1 entry")

    affected = get(data, "metrics.affected_rows")
    total = get(data, "metrics.total_rows_inspected")
    pct = get(data, "metrics.affected_row_percentage")
    if isinstance(affected, (int, float)) and isinstance(total, (int, float)) and total:
        r.check("V-DQIR-07", approx(pct, affected / total * 100.0, 0.1),
                "affected_row_percentage must equal affected_rows/total*100 (±0.1)")
    else:
        r.check("V-DQIR-07", False, "metrics.affected_rows/total_rows_inspected missing or zero")

    if severity in ("CRITICAL", "HIGH"):
        r.check("V-DQIR-08", data.get("training_pipeline_blocked") is True,
                "CRITICAL/HIGH severity requires training_pipeline_blocked=true",
                hard_block=True)

    if correction == "ACCEPTED":
        r.check("V-DQIR-09", severity in ("MEDIUM", "LOW"),
                "ACCEPTED only allowed for MEDIUM/LOW severity")

    if correction == "CORRECTED":
        r.check("V-DQIR-10", bool(data.get("corrected_dataset_version")),
                "CORRECTED requires corrected_dataset_version")

    if issue_type == "DISTRIBUTION_DRIFT":
        r.check("V-DQIR-11", bool(get(data, "baseline_comparison")),
                "DISTRIBUTION_DRIFT requires baseline_comparison block")

    start = parse_date(get(data, "dataset.collection_window.start"))
    end = parse_date(get(data, "dataset.collection_window.end"))
    if start and end:
        r.check("V-DQIR-12", start < end, "collection_window.start must be < end")
    else:
        r.check("V-DQIR-12", False, "collection_window.start/end missing or unparseable")

    samples_ok = all(
        len(f.get("sample_bad_values", []) or []) <= 5
        for f in features if isinstance(f, dict)
    )
    r.check("V-DQIR-13", samples_ok, "sample_bad_values length must be ≤5 per feature")

    return r
