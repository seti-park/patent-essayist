# Vendored third-party skills

These skills are bundled (vendored) from upstream open-source projects and used by
`essay-write` (humanizer) and `essay-evaluate` (ai-check). Each retains its own LICENSE.

| Dir | Upstream | License | Used by | Purpose |
|-----|----------|---------|---------|---------|
| `humanizer/` | [blader/humanizer](https://github.com/blader/humanizer) | MIT | `essay-write` | Detect + rewrite AI tells, based on Wikipedia's "Signs of AI writing". |
| `ai-check/` | [harshaneel/humanize](https://github.com/harshaneel/humanize) (`ai-check`) | MIT | `essay-evaluate` | Forensic AI-tell scoring (0–27 + verdict) feeding the rubric penalty. |

## Updating

Re-pull the upstream `SKILL.md` (and any reference files) and copy it here, preserving the
upstream `LICENSE`. Do not edit vendored files in place — adjust behavior via the
`_shared/references/` rubric/style files or the stage skills instead, so updates stay
clean.

## Alternatives considered

Other MIT-licensed scoring-capable humanizers if you want to swap `ai-check`:
[gregorymm/humanize-text](https://github.com/gregorymm/humanize-text) (7 categories, 1–10),
[Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) (43 patterns, 0–100).
