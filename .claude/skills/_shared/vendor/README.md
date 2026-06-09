# Vendored third-party skills

These skills are bundled (vendored) from upstream open-source projects. Each retains its
own LICENSE.

> **Source of truth is SETI's own canon, not these vendored skills.** AI-tell removal is
> governed by `_shared/references/anti-ai-writing.md` (enforced mechanically by
> `_shared/scripts/gate_banned.py`) and the voice canon. The vendored skills are at most an
> **optional secondary cross-check**, kept here for reference and easy swapping.

| Dir | Upstream | License | Role now | Notes |
|-----|----------|---------|----------|-------|
| `ai-check/` | [harshaneel/humanize](https://github.com/harshaneel/humanize) (`ai-check`) | MIT | **Optional** secondary AI-tell scorer in Phase 3 (`editorial-review`), feeding voice dimension 4 as a cross-check. | Not the source of truth; the canon + gates are. |
| `humanizer/` | [blader/humanizer](https://github.com/blader/humanizer) | MIT | **Demoted — not in the compose path.** | Kept for reference only; its rewrite passes can fight SETI's own voice, so Phase 2 strips via `anti-ai-writing.md`, not this skill. |

## Updating

Re-pull the upstream `SKILL.md` (and any reference files) and copy it here, preserving the
upstream `LICENSE`. Do not edit vendored files in place — adjust behavior via
`_shared/references/` (canon) and `_shared/scripts/` (gates) instead, so updates stay clean.

## Alternatives considered

Other MIT-licensed scoring-capable humanizers if you ever want to swap `ai-check`:
[gregorymm/humanize-text](https://github.com/gregorymm/humanize-text) (7 categories, 1–10),
[Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) (43 patterns, 0–100).
