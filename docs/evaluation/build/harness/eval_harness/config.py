"""Runtime configuration — environment-driven, no hardcoded credentials.

All secrets (DB password, S3 keys) come from environment variables, satisfying
the task constraint and CLAUDE.md §7.6. ``Settings.load()`` is the single entry
point; everything else receives a ``Settings`` instance.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from .version import ENGINE_VERSION


def _bool(env: str, default: bool) -> bool:
    val = os.environ.get(env)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    # Database (DATABASE_URL wins; otherwise assembled from PG* vars).
    database_url: str | None
    pg_host: str
    pg_port: str
    pg_db: str
    pg_user: str
    pg_password: str
    db_min_conn: int
    db_max_conn: int

    # Artifact store (MinIO/S3-compatible or local file://). Keys come from env.
    artifact_store_uri: str          # e.g. "file:///var/harness/artifacts" or "s3://eval-harness"
    s3_endpoint_url: str | None
    s3_access_key: str | None
    s3_secret_key: str | None

    # API
    api_host: str
    api_port: int

    # Behaviour
    engine_version: str
    blind_scoring: bool              # spec §6.2 — always True in production
    rubric_version: str

    def dsn(self) -> str:
        if self.database_url:
            return self.database_url
        pwd = f" password={self.pg_password}" if self.pg_password else ""
        return (
            f"host={self.pg_host} port={self.pg_port} dbname={self.pg_db} "
            f"user={self.pg_user}{pwd}"
        )

    @classmethod
    def load(cls) -> Settings:
        return cls(
            database_url=os.environ.get("DATABASE_URL"),
            pg_host=os.environ.get("PGHOST", "localhost"),
            pg_port=os.environ.get("PGPORT", "5432"),
            pg_db=os.environ.get("PGDATABASE", "eval_harness"),
            pg_user=os.environ.get("PGUSER", "harness"),
            pg_password=os.environ.get("PGPASSWORD", ""),
            db_min_conn=int(os.environ.get("HARNESS_DB_MIN_CONN", "1")),
            db_max_conn=int(os.environ.get("HARNESS_DB_MAX_CONN", "10")),
            artifact_store_uri=os.environ.get("HARNESS_ARTIFACT_STORE", "file:///var/harness/artifacts"),
            s3_endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            s3_access_key=os.environ.get("S3_ACCESS_KEY"),
            s3_secret_key=os.environ.get("S3_SECRET_KEY"),
            api_host=os.environ.get("HARNESS_API_HOST", "0.0.0.0"),
            api_port=int(os.environ.get("HARNESS_API_PORT", "8080")),
            engine_version=os.environ.get("HARNESS_ENGINE_VERSION", ENGINE_VERSION),
            blind_scoring=_bool("HARNESS_BLIND_SCORING", True),
            rubric_version=os.environ.get("HARNESS_RUBRIC_VERSION", "v1"),
        )
