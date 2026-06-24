"""Artifact ingest helpers — fetch, hash, and parse submitted artifacts.

Supports ``file://`` and ``s3://`` URIs. YAML/JSON and Markdown-frontmatter
artifacts are parsed into a mapping for the schema validators (spec §2.3 step 2:
"normalises the artifact (extracts the scorable representation)"). PyYAML and
boto3 are optional — imported lazily so the pure core never requires them.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any
from urllib.parse import urlparse

LOG = logging.getLogger("harness.artifacts")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(uri: str, settings=None) -> bytes:
    """Fetch raw bytes for a file:// or s3:// artifact URI."""
    parsed = urlparse(uri)
    scheme = parsed.scheme or "file"
    if scheme == "file":
        path = parsed.path
        # Windows file URIs render as /C:/... — strip the leading slash.
        if len(path) >= 3 and path[0] == "/" and path[2] == ":":
            path = path[1:]
        with open(path, "rb") as fh:
            return fh.read()
    if scheme == "s3":
        try:
            import boto3  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("s3:// artifacts require boto3 (pip install boto3)") from exc
        kwargs: dict[str, Any] = {}
        if settings is not None and settings.s3_endpoint_url:
            kwargs["endpoint_url"] = settings.s3_endpoint_url
            kwargs["aws_access_key_id"] = settings.s3_access_key
            kwargs["aws_secret_access_key"] = settings.s3_secret_key
        client = boto3.client("s3", **kwargs)
        obj = client.get_object(Bucket=parsed.netloc, Key=parsed.path.lstrip("/"))
        return obj["Body"].read()
    raise ValueError(f"unsupported artifact URI scheme: {scheme!r}")


def _strip_frontmatter(text: str) -> str | None:
    """Return the YAML frontmatter block of a Markdown file, if present."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def parse_artifact(uri: str, raw: bytes) -> dict | None:
    """Best-effort parse of a governance artifact into a mapping.

    Returns None for binary/code artifacts (which are scored from a CI metrics
    manifest, not by structural parsing).
    """
    lower = uri.lower()
    text: str | None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None

    if lower.endswith(".json"):
        try:
            data = json.loads(text)
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            LOG.warning("artifact %s is not valid JSON", uri)
            return None

    try:
        import yaml  # type: ignore
    except ImportError:  # pragma: no cover
        LOG.warning("PyYAML not installed; cannot parse %s", uri)
        return None

    if lower.endswith((".yaml", ".yml")):
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None

    if lower.endswith((".md", ".markdown")):
        fm = _strip_frontmatter(text)
        if fm is None:
            return None
        data = yaml.safe_load(fm)
        return data if isinstance(data, dict) else None

    # Unknown extension: try YAML as a last resort.
    try:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None
