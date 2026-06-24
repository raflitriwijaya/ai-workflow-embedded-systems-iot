"""``harness-evaluate`` — agent evaluation pipeline (spec §6).

Submits an agent-produced deliverable (artifact → schema/auto validation →
scoring engine → comparison against the human baseline → readiness) and prints a
readiness verdict. Also recomputes and prints per-role readiness.

Subcommands
-----------
    submit     ingest one agent deliverable and show its score + acceptance
    readiness  recompute and print agent-vs-baseline readiness for a role

Examples
--------
    harness-evaluate submit --role MLOPS --deliverable D1-ML-4 \
        --artifact s3://eval-harness/sub/TASK-91/ocm.yaml \
        --agent-id mlops-agent-v1.2 --task-id TASK-91 --accepted
    harness-evaluate readiness --role MLOPS --recompute
"""
from __future__ import annotations

import argparse
import logging
import sys

from ..logging_setup import configure_logging
from ..service import IngestError, ingest_submission, recompute_readiness
from . import build_db, load_metrics, to_uri

LOG = logging.getLogger("harness.cli.evaluate")


def _cmd_submit(args) -> int:
    db, settings = build_db()
    try:
        out = ingest_submission(
            db, settings,
            role_code=args.role, deliverable_id=args.deliverable, producer_type="AGENT",
            artifact_uri=to_uri(args.artifact), metrics=load_metrics(args.metrics),
            agent_id=args.agent_id, task_id=args.task_id,
            human_reviewer_id=args.reviewer_id,
            human_accepted=args.accepted, human_edit_required=args.edited,
            edit_effort_minutes=args.edit_minutes,
            extra_metadata={"sprint": args.sprint} if args.sprint else None,
        )
        print(f"agent submission {out['submission_id']}  status={out['status']}")
        print(f"  auto={out['auto_score']}  hr={out['hr_score']}  composite={out['composite_score']}")
        if out["hard_block"]:
            print("  !! HARD BLOCK — artifact valid but a downstream gate halts dispatch "
                  "(see messages).")
        for m in out["messages"]:
            print(f"     - {m}")
        if out["status"] == "AWAITING_HR":
            print("  -> queued for blind human review (HR sub-score pending).")
        return 0 if not out["hard_block"] else 3
    except IngestError as exc:
        LOG.error("evaluation rejected: %s", exc)
        return 2
    finally:
        db.close()


def _verdict_icon(state: str) -> str:
    return {"GREEN": "[GREEN]", "YELLOW": "[YELLOW]", "RED": "[RED]"}.get(state, state)


def _cmd_readiness(args) -> int:
    db, settings = build_db()
    try:
        if args.recompute:
            recompute_readiness(db, settings)
        with db.repository() as repo:
            rows = repo.latest_readiness(args.role)
        if not rows:
            print(f"no readiness data for role {args.role} (capture baselines first)")
            return 1
        print(f"Readiness — {args.role}")
        print(f"{'deliverable':<12} {'state':<8} {'base_n':>6} {'base_mean':>9} "
              f"{'agent_n':>7} {'agent_mean':>10} {'welch_p':>8}")
        for r in rows:
            did = r["deliverable_id"] or "(role)"
            bp = f"{r['baseline_mean']:.1f}" if r["baseline_mean"] is not None else "-"
            ap = f"{r['agent_mean']:.1f}" if r["agent_mean"] is not None else "-"
            wp = f"{r['welch_p']:.4f}" if r["welch_p"] is not None else "-"
            print(f"{did:<12} {_verdict_icon(r['readiness']):<8} {r['baseline_n']:>6} {bp:>9} "
                  f"{r['agent_n']:>7} {ap:>10} {wp:>8}")
        return 0
    finally:
        db.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness-evaluate", description="Agent evaluation pipeline")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("submit", help="ingest one agent deliverable")
    s.add_argument("--role", required=True)
    s.add_argument("--deliverable", required=True)
    s.add_argument("--artifact", required=True)
    s.add_argument("--metrics", help="path to JSON CI metrics manifest")
    s.add_argument("--agent-id", required=True)
    s.add_argument("--task-id")
    s.add_argument("--reviewer-id", help="human reviewer who supervised the agent output")
    s.add_argument("--accepted", action="store_true", help="human accepted the artifact")
    s.add_argument("--edited", action="store_true", help="human edited before acceptance")
    s.add_argument("--edit-minutes", type=int, help="minutes spent editing")
    s.add_argument("--sprint", help="sprint label, e.g. 2026-Q3-S4")
    s.set_defaults(func=_cmd_submit)

    r = sub.add_parser("readiness", help="print agent-vs-baseline readiness")
    r.add_argument("--role", required=True)
    r.add_argument("--recompute", action="store_true", help="run the statistical engine first")
    r.set_defaults(func=_cmd_readiness)
    return p


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
