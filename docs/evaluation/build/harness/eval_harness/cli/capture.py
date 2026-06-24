"""``harness-capture`` — baseline capture tool (spec §5.2).

Submits human-produced deliverable samples to the harness with capture metadata
(role, deliverable, time spent, complexity rating) and reports progress toward
the ≥30-sample-per-deliverable activation threshold (WG-1).

Subcommands
-----------
    submit   ingest one human baseline sample
    status   show sample progress toward ≥30 for a role (or all roles)

Examples
--------
    harness-capture submit --role DATA --deliverable D1-DE-1 \
        --artifact ./pipelines/ingest_dag.py --metrics ./ci_metrics.json \
        --producer-id rani.kusuma --time-spent 95 --complexity 3
    harness-capture status --role DATA
"""
from __future__ import annotations

import argparse
import logging
import sys

from ..logging_setup import configure_logging
from ..service import IngestError, ingest_submission
from . import build_db, load_metrics, to_uri

LOG = logging.getLogger("harness.cli.capture")


def _cmd_submit(args) -> int:
    db, settings = build_db()
    try:
        out = ingest_submission(
            db, settings,
            role_code=args.role, deliverable_id=args.deliverable, producer_type="HUMAN",
            artifact_uri=to_uri(args.artifact), metrics=load_metrics(args.metrics),
            is_baseline=True, human_producer_id=args.producer_id,
            time_spent_minutes=args.time_spent, complexity_rating=args.complexity,
        )
        print(f"captured submission {out['submission_id']}  status={out['status']}  "
              f"composite={out['composite_score']}")
        if out["status"] == "AWAITING_HR":
            print("  -> awaiting human review for the HR sub-score before it counts toward baseline.")

        # Report progress toward the ≥30 threshold (WG-1).
        with db.repository() as repo:
            for row in repo.sample_progress(args.role):
                if row["deliverable_id"] == args.deliverable:
                    met = "OK" if row["threshold_met"] else "PENDING"
                    print(f"  baseline progress {args.deliverable}: "
                          f"{row['baseline_n']}/{row['min_sample']} [{met}]")
        return 0
    except IngestError as exc:
        LOG.error("capture rejected: %s", exc)
        return 2
    finally:
        db.close()


def _cmd_status(args) -> int:
    db, _ = build_db()
    try:
        with db.repository() as repo:
            rows = repo.sample_progress(args.role)
        if not rows:
            print("no deliverables found (is the seed loaded?)")
            return 1
        print(f"{'deliverable':<10} {'name':<42} {'n':>4}/{'min':<3} status")
        for r in rows:
            met = "GREEN" if r["threshold_met"] else "RED"
            print(f"{r['deliverable_id']:<10} {r['deliverable_name'][:42]:<42} "
                  f"{r['baseline_n']:>4}/{r['min_sample']:<3} {met}")
        return 0
    finally:
        db.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness-capture", description="Baseline capture tool")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("submit", help="ingest one human baseline sample")
    s.add_argument("--role", required=True, help="role code, e.g. DATA")
    s.add_argument("--deliverable", required=True, help="deliverable id, e.g. D1-DE-1")
    s.add_argument("--artifact", required=True, help="path or URI to the artifact")
    s.add_argument("--metrics", help="path to a JSON CI metrics manifest (AUTO/HYB deliverables)")
    s.add_argument("--producer-id", required=True, help="human role-holder id")
    s.add_argument("--time-spent", type=int, help="minutes spent producing the deliverable")
    s.add_argument("--complexity", type=int, choices=range(1, 6), help="task complexity 1–5")
    s.set_defaults(func=_cmd_submit)

    st = sub.add_parser("status", help="show baseline sample progress")
    st.add_argument("--role", help="restrict to one role code")
    st.set_defaults(func=_cmd_status)
    return p


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
