#!/usr/bin/env python3
"""Evaluate a skill's frontmatter `description`.

Two measures, combined into one report:
  1. Trigger accuracy — a router, shown only the skill name+description, decides
     whether to invoke the skill for each labelled prompt. Reports
     precision / recall / F1 against the labels.
  2. Description rubric — the description text is graded against a rubric
     (trigger coverage, scope boundaries, clarity, examples, conciseness).

Uses the Anthropic API when ANTHROPIC_API_KEY + the `anthropic` SDK are present;
otherwise falls back to a deterministic, description-driven heuristic so it runs
anywhere. The active mode is printed in the header.

Examples:
  python run_eval.py
  python run_eval.py --skill skills/patent-thread --dataset data/patent-thread.jsonl
  python run_eval.py --all --json outputs/eval.json
"""

from __future__ import annotations

import argparse
import json
import sys

from skill_eval import (
    LLMClient,
    load_dataset,
    load_skill,
    run_trigger_eval,
    score_rubric,
)
from skill_eval.report import composite_score, format_rubric_report, format_trigger_report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", default="skills/patent-thread", help="path to SKILL.md or its directory")
    ap.add_argument("--dataset", default="data/patent-thread.jsonl", help="labelled prompt set (jsonl)")
    ap.add_argument("--description", help="override the skill's description with this text")
    ap.add_argument("--model", default="claude-opus-4-8", help="Anthropic model id")
    ap.add_argument("--all", action="store_true", help="list every case, not just failures")
    ap.add_argument("--json", dest="json_out", help="also write the full report as JSON to this path")
    ap.add_argument("--skip-rubric", action="store_true", help="trigger accuracy only")
    args = ap.parse_args(argv)

    try:
        skill = load_skill(args.skill)
        dataset = load_dataset(args.dataset)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.description:
        skill.description = " ".join(args.description.split())

    client = LLMClient(model=args.model)

    print("=" * 60)
    print(f"Skill: {skill.name}   ({skill.path})")
    print(f"Mode:  {client.mode.upper()}  — {client.reason}")
    print("=" * 60)
    print("Description under test:")
    print(f"  {skill.description}")
    print()

    trigger = run_trigger_eval(client, skill, dataset)
    print(format_trigger_report(trigger, show_all=args.all))
    print()

    rubric = None
    if not args.skip_rubric:
        rubric = score_rubric(client, skill)
        print(format_rubric_report(rubric))
        print()
        print(f"COMPOSITE SCORE: {composite_score(trigger, rubric)}/100  "
              f"(70% trigger-F1 + 30% rubric)")
        print()

    if args.json_out:
        payload = {
            "skill": {"name": skill.name, "description": skill.description, "path": skill.path},
            "mode": client.mode,
            "trigger": trigger.to_dict(),
        }
        if rubric is not None:
            payload["rubric"] = rubric.to_dict()
            payload["composite"] = composite_score(trigger, rubric)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"wrote {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
