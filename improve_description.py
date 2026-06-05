#!/usr/bin/env python3
"""Improve a skill's frontmatter `description`, then prove the improvement.

Pipeline:
  1. Evaluate the current description (run_eval's two measures).
  2. Ask Claude to rewrite it to fix trigger failures and weak rubric criteria
     — preserving the skill's meaning, persona, and every 'NOT ...' scope
     boundary. (Offline: mine missing trigger/scope vocabulary from the
     misclassified examples instead.)
  3. Re-evaluate the rewrite and print a before/after comparison.

By default the improved description is written to outputs/<skill>.improved.md.
Pass --write to patch the SKILL.md in place (only the description field changes).

Examples:
  python improve_description.py
  python improve_description.py --rounds 2
  python improve_description.py --write
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from skill_eval import (
    LLMClient,
    load_dataset,
    load_skill,
    propose_improved_description,
    run_trigger_eval,
    score_rubric,
    write_description,
)
from skill_eval.report import composite_score, format_rubric_report, format_trigger_report


def _evaluate(client: LLMClient, skill, dataset):
    trigger = run_trigger_eval(client, skill, dataset)
    rubric = score_rubric(client, skill)
    return trigger, rubric


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", default="skills/patent-thread", help="path to SKILL.md or its directory")
    ap.add_argument("--dataset", default="data/patent-thread.jsonl", help="labelled prompt set (jsonl)")
    ap.add_argument("--model", default="claude-opus-4-8", help="Anthropic model id")
    ap.add_argument("--rounds", type=int, default=1, help="improvement iterations (default 1)")
    ap.add_argument("--out", help="path to write the improved description (default outputs/<name>.improved.md)")
    ap.add_argument("--write", action="store_true", help="patch the SKILL.md description field in place")
    ap.add_argument("--json", dest="json_out", help="write a machine-readable before/after report")
    args = ap.parse_args(argv)

    try:
        skill = load_skill(args.skill)
        dataset = load_dataset(args.dataset)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    client = LLMClient(model=args.model)

    print("=" * 60)
    print(f"Skill: {skill.name}   ({skill.path})")
    print(f"Mode:  {client.mode.upper()}  — {client.reason}")
    print("=" * 60)

    original_description = skill.description
    base_trigger, base_rubric = _evaluate(client, skill, dataset)
    base_score = composite_score(base_trigger, base_rubric)

    print("\nBEFORE")
    print(f"  description: {skill.description}")
    print()
    print(format_trigger_report(base_trigger))
    print()
    print(format_rubric_report(base_rubric))
    print(f"\n  composite: {base_score}/100")

    all_changes: list[str] = []
    best_desc = skill.description
    best_trigger, best_rubric, best_score = base_trigger, base_rubric, base_score

    for rnd in range(1, args.rounds + 1):
        proposal = propose_improved_description(
            client, skill, dataset, trigger_report=best_trigger, rubric_report=best_rubric
        )
        candidate = proposal["improved_description"]
        all_changes.extend(proposal["changes"])

        # Evaluate the candidate.
        skill.description = candidate
        cand_trigger, cand_rubric = _evaluate(client, skill, dataset)
        cand_score = composite_score(cand_trigger, cand_rubric)

        print("\n" + "-" * 60)
        print(f"round {rnd}  [{proposal['mode']}]  composite {best_score} -> {cand_score}")
        for c in proposal["changes"]:
            print(f"   • {c}")

        if cand_score >= best_score:
            best_desc, best_trigger, best_rubric, best_score = (
                candidate, cand_trigger, cand_rubric, cand_score,
            )
        else:
            print("   (no improvement — keeping previous best, stopping)")
            skill.description = best_desc
            break
        skill.description = best_desc

    print("\n" + "=" * 60)
    print("AFTER")
    print(f"  description: {best_desc}")
    print()
    print(format_trigger_report(best_trigger))
    print()
    print(format_rubric_report(best_rubric))
    print(f"\n  composite: {base_score}/100  ->  {best_score}/100   (Δ {best_score - base_score:+.1f})")

    # Persist the improved description.
    out_path = args.out
    if not out_path:
        base = os.path.splitext(os.path.basename(skill.path))[0]
        safe = skill.name or base
        out_path = os.path.join("outputs", f"{safe}.improved.md")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(best_desc + "\n")
    print(f"\nwrote improved description -> {out_path}")

    if args.write:
        if best_score > base_score:
            write_description(skill.path, best_desc)
            print(f"patched description field in {skill.path}")
        else:
            print(f"--write skipped: no net improvement over baseline ({best_score} <= {base_score})")

    if args.json_out:
        payload = {
            "skill": skill.name,
            "mode": client.mode,
            "before": {
                "description": original_description,
                "trigger": base_trigger.to_dict()["metrics"],
                "rubric": base_rubric.overall,
                "composite": base_score,
            },
            "after": {
                "description": best_desc,
                "trigger": best_trigger.to_dict()["metrics"],
                "rubric": best_rubric.overall,
                "composite": best_score,
            },
            "changes": all_changes,
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"wrote {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
