"""Plain-text formatting for eval reports."""

from __future__ import annotations

from .evaluate import RubricReport, TriggerReport


def _bar(value: float, width: int = 24) -> str:
    filled = int(round(value * width))
    return "█" * filled + "·" * (width - filled)


def format_trigger_report(report: TriggerReport, show_all: bool = False) -> str:
    lines = []
    lines.append(f"Trigger accuracy  [{report.mode}]")
    lines.append("-" * 60)
    lines.append(
        f"  confusion:  TP={report.tp}  FP={report.fp}  TN={report.tn}  FN={report.fn}"
        f"  (n={report.total})"
    )
    lines.append(f"  accuracy   {report.accuracy:6.1%}  {_bar(report.accuracy)}")
    lines.append(f"  precision  {report.precision:6.1%}  {_bar(report.precision)}")
    lines.append(f"  recall     {report.recall:6.1%}  {_bar(report.recall)}")
    lines.append(f"  f1         {report.f1:6.1%}  {_bar(report.f1)}")

    rows = report.results if show_all else report.failures
    if rows:
        heading = "all cases" if show_all else "misclassified cases"
        lines.append("")
        lines.append(f"  {heading}:")
        for r in rows:
            mark = "✓" if r["correct"] else "✗"
            lines.append(
                f"    {mark} {r['kind']:<2} {r['id']:<4} exp={int(r['expected'])} "
                f"pred={int(r['predicted'])}  {r['prompt'][:60]}"
            )
            if not r["correct"]:
                lines.append(f"          ↳ {r['reason'][:80]}")
    elif not show_all:
        lines.append("")
        lines.append("  no misclassified cases.")
    return "\n".join(lines)


def format_rubric_report(report: RubricReport) -> str:
    lines = []
    lines.append(f"Description rubric  [{report.mode}]")
    lines.append("-" * 60)
    for c in report.criteria:
        frac = (c["score"] / c["max"]) if c["max"] else 0
        lines.append(f"  {c['name']:<18} {c['score']:>2}/{c['max']:<2}  {_bar(frac, 16)}")
        lines.append(f"      {c['comment'][:72]}")
    lines.append("-" * 60)
    lines.append(f"  OVERALL  {report.overall}/{report.max_total}")
    if report.summary:
        lines.append(f"  {report.summary}")
    return "\n".join(lines)


def composite_score(trigger: TriggerReport, rubric: RubricReport) -> float:
    """Single 0-100 number: 70% trigger F1, 30% rubric."""
    rubric_pct = (rubric.overall / rubric.max_total * 100) if rubric.max_total else 0
    return round(0.7 * (trigger.f1 * 100) + 0.3 * rubric_pct, 1)
