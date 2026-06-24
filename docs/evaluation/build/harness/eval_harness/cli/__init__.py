"""Command-line entry points for the Evaluation Harness.

* ``harness-capture``  — submit human baseline samples (spec §5.2)
* ``harness-evaluate`` — submit an agent deliverable and print readiness (spec §6)
"""
from __future__ import annotations

import json
import pathlib
from typing import Any


def to_uri(path_or_uri: str) -> str:
    """Pass through real URIs; turn a local path into an absolute file:// URI."""
    if "://" in path_or_uri:
        return path_or_uri
    return pathlib.Path(path_or_uri).resolve().as_uri()


def load_metrics(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise SystemExit(f"metrics file {path} must contain a JSON object")
    return data


def build_db():
    """Construct the Database from environment settings (lazy import of psycopg2)."""
    from ..config import Settings
    from ..db import Database

    settings = Settings.load()
    return Database(settings.dsn(), settings.db_min_conn, settings.db_max_conn), settings
