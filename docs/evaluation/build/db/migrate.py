#!/usr/bin/env python3
"""Evaluation Harness — database migration runner.

Applies the versioned SQL files in ``db/migrations/`` (and, with ``--seed``,
``db/seed/``) in lexical order, recording each applied file in a
``schema_migrations`` ledger so re-runs are idempotent.

Design notes
------------
* **Versioning**: every file is named ``NNNN_description.sql``. The numeric
  prefix is the version. Applied versions are recorded with a SHA-256 checksum;
  if a previously-applied file changes on disk the runner aborts (a migration
  must never be edited in place — add a new one).
* **Idempotency**: the migration SQL itself uses ``IF NOT EXISTS`` / ``ON
  CONFLICT`` so a half-applied file can be re-run safely; the ledger then
  prevents redundant work on subsequent runs.
* **Atomicity**: each file is applied in its own transaction.
* **No hardcoded credentials**: connection settings come from ``DATABASE_URL``
  or the standard ``PG*`` environment variables (CLAUDE.md §7.6 / task constraint).

Usage
-----
    python migrate.py --status            # show applied/pending
    python migrate.py                     # apply pending migrations
    python migrate.py --seed              # apply migrations + seed data
    python migrate.py --dry-run --seed    # list what would run, change nothing
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:  # pragma: no cover - dependency guidance
    sys.stderr.write(
        "psycopg2 is required: pip install psycopg2-binary\n"
    )
    raise

LOG = logging.getLogger("harness.migrate")

HERE = Path(__file__).resolve().parent
MIGRATIONS_DIR = HERE / "migrations"
SEED_DIR = HERE / "seed"

LEDGER_DDL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version     TEXT PRIMARY KEY,
    filename    TEXT NOT NULL,
    kind        TEXT NOT NULL,            -- 'migration' | 'seed'
    checksum    CHAR(64) NOT NULL,
    applied_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


@dataclass(frozen=True)
class SqlFile:
    version: str
    kind: str
    path: Path

    @property
    def checksum(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()


def _connect():
    """Open a connection from DATABASE_URL or PG* env vars. Never from literals."""
    dsn = os.environ.get("DATABASE_URL")
    if dsn:
        return psycopg2.connect(dsn)
    missing = [v for v in ("PGHOST", "PGDATABASE", "PGUSER") if not os.environ.get(v)]
    if missing:
        raise SystemExit(
            "No DATABASE_URL and missing env vars: "
            + ", ".join(missing)
            + ". Set DATABASE_URL or PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD."
        )
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ.get("PGPASSWORD", ""),
    )


def _discover(directory: Path, kind: str) -> list[SqlFile]:
    if not directory.is_dir():
        return []
    files: list[SqlFile] = []
    for path in sorted(directory.glob("*.sql")):
        version = path.stem.split("_", 1)[0]
        files.append(SqlFile(version=f"{kind}:{version}", kind=kind, path=path))
    return files


def _ensure_ledger(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(LEDGER_DDL)
    conn.commit()


def _applied(conn) -> dict[str, str]:
    with conn.cursor() as cur:
        cur.execute("SELECT version, checksum FROM schema_migrations;")
        return dict(cur.fetchall())


def _apply_file(conn, sql_file: SqlFile, dry_run: bool) -> None:
    if dry_run:
        LOG.info("DRY-RUN would apply %s (%s)", sql_file.path.name, sql_file.version)
        return
    sql = sql_file.path.read_text(encoding="utf-8")
    LOG.info("applying %s ...", sql_file.path.name)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            cur.execute(
                "INSERT INTO schema_migrations (version, filename, kind, checksum) "
                "VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (version) DO UPDATE SET checksum = EXCLUDED.checksum, "
                "applied_at = now();",
                (sql_file.version, sql_file.path.name, sql_file.kind, sql_file.checksum),
            )
        conn.commit()
        LOG.info("  ok: %s", sql_file.version)
    except Exception:
        conn.rollback()
        LOG.exception("  FAILED: %s (rolled back)", sql_file.path.name)
        raise


def run(seed: bool, dry_run: bool, status_only: bool) -> int:
    plan = _discover(MIGRATIONS_DIR, "migration")
    if seed:
        plan += _discover(SEED_DIR, "seed")
    if not plan:
        LOG.warning("no SQL files found under %s", HERE)
        return 0

    conn = _connect()
    try:
        # gen_random_uuid()/extensions may need autocommit during CREATE EXTENSION
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        _ensure_ledger(conn)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        applied = _applied(conn)

        if status_only:
            for f in plan:
                state = "APPLIED" if f.version in applied else "PENDING"
                drift = ""
                if f.version in applied and applied[f.version] != f.checksum:
                    drift = "  !! CHECKSUM DRIFT (file edited after apply)"
                LOG.info("%-9s %-12s %s%s", state, f.version, f.path.name, drift)
            return 0

        pending = 0
        for f in plan:
            if f.version in applied:
                if applied[f.version] != f.checksum:
                    raise SystemExit(
                        f"Checksum drift on already-applied {f.path.name}. "
                        "Migrations are immutable — add a new migration instead."
                    )
                LOG.debug("skip (already applied): %s", f.version)
                continue
            _apply_file(conn, f, dry_run)
            pending += 1
        LOG.info("done: %d file(s) %s", pending, "would be applied" if dry_run else "applied")
        return 0
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluation Harness DB migrator")
    parser.add_argument("--seed", action="store_true", help="also apply db/seed/*.sql")
    parser.add_argument("--dry-run", action="store_true", help="show plan, change nothing")
    parser.add_argument("--status", action="store_true", help="print applied/pending and exit")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )
    try:
        return run(seed=args.seed, dry_run=args.dry_run, status_only=args.status)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        LOG.error("migration run failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
