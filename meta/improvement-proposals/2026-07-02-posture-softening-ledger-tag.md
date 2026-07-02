---
proposal_id: 2026-07-02-posture-softening-ledger-tag
created: 2026-07-02T00:00:00Z
status: watch
lever: reference-edit
goal: "4a"
root_cause_stage: retro
root_cause_artifact: pipeline-retro/references/ledger-schema.md + handoff-template/03-edit/revision-notes.md (no field distinguishes a strength-REDUCING applied edit from any other applied edit)
recurrence_count: 1
confidence: medium
triggering_findings:
  - essay_id: 2026-07-01-us20230356397b2-cliff-histogram-bridge, iter: self-audit r1, pattern_tag: closing-scope-overreach (the applied softening of the bolded closing — "the senses, and the reflex, that a SLAM stack has to stand on" → "one of the senses, and a reflex ... if it is going to trust the ground under it")
  - essay_id: (audience feedback, multi-iteration published outputs), reported by SETI 2026-07-02 — readers judge heavily-looped essays "too safe / dispute-avoidant"; the drift is real at the register level but currently unmeasurable from the ledger
---

## Problem

Review pressure in this system is directionally asymmetric by design (Pass 3/4 gate
OVERREACH), and the ledger cannot see the direction of an applied edit. The cliff run's
self-audit softened the essay's bolded closing sentence; the ledger records it as
`closing-scope-overreach` — indistinguishable from any other grounding win. If ten future
rounds each shave a little rhetorical strength, the ledger would show ten legitimate-looking
grounding fixes and no signal that the register drifted — which is exactly what reader
feedback (2026-07-02) now reports from the outside: multi-iteration essays read "too safe /
dispute-avoidant" to investment-diligence readers.

You cannot tune what you cannot see. Before deciding whether the loop over-softens (and how
much of it 6G + the firm-closing default already fix), the softening edits need their own
dimension in the ledger.

## Proposed change (exact diff)

**File 1: `.claude/skills/pipeline-retro/references/ledger-schema.md`** — add an optional
field to "## Record fields":

```markdown
| `posture_delta` | OPTIONAL. For APPLIED edits only: `softened` (the edit reduced the
rhetorical strength of a span that was previously passing — added qualifier, definite→
indefinite article, weakened verb, demoted verdict), `firmed` (the edit strengthened a
hedged span), or absent (strength-neutral). Set at normalization time from the delta's
before/after text. Grounding-forced softenings still carry `softened` — the field records
direction, not legitimacy; legitimacy stays in the finding/recommendation text. |
```

**File 2: `handoff-template/03-edit/revision-notes.md`** — add one optional line to the
`## delta` block schema:

```markdown
posture: softened | firmed | neutral   # direction of the strength change, if any
```

**File 3: `.claude/skills/pipeline-retro/SKILL.md`** — one sentence in Process step 1
(Collect), after the revision-delta normalization:

```markdown
Tag each applied delta's `posture_delta` (softened / firmed / neutral) from its
before/after text, so cumulative register drift across rounds is visible per run
(`softened` count ≫ `firmed` count on a verdict edition is a 6G-adjacent signal even when
every individual softening was grounding-justified).
```

## Why this lever

- Pure instrumentation: no behavior changes, no gate, no threshold — it makes an invisible
  quantity countable. The cheapest possible response to a register-level reader complaint
  that currently has no per-edit evidence trail.
- Not rubric-tuning yet: whether to *limit* softening (e.g., a per-run softened-budget) is a
  posture decision that should wait for data this field generates.
- `watch`, not recommended-apply: one concretely-logged softening instance + register-level
  reader feedback; the schema addition is safe but its value should be confirmed over 2-3
  runs before hardening anything on top of it.

## Regression expectation

Documentation-only (schema + template + skill sentence; the field is optional so
`meta/normalize_revision_notes.py` and existing ledger lines stay valid — verify the script
passes unknown fields through untouched before applying). `test_gates.py` and
`meta/regression.py` unchanged green. Success criterion: the next run's ledger shows
`posture_delta` on every applied delta, and a per-run softened/firmed tally is derivable
(candidate later addition to `meta/tally_ledger.py`).
