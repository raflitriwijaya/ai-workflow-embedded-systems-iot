"""Centralised logging configuration.

JSON-ish single-line logs by default so they ingest cleanly into Loki/the DevOps
observability stack (spec §9.1 "Harness itself monitored via the existing DevOps
observability stack"). Set ``HARNESS_LOG_FORMAT=plain`` for human-readable logs.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        for key in ("submission_id", "run_id", "role", "deliverable_id"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload, default=str)


def configure_logging(level: str | None = None) -> None:
    lvl = (level or os.environ.get("HARNESS_LOG_LEVEL", "INFO")).upper()
    handler = logging.StreamHandler(sys.stdout)
    if os.environ.get("HARNESS_LOG_FORMAT", "json").lower() == "plain":
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    else:
        handler.setFormatter(_JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, lvl, logging.INFO))
