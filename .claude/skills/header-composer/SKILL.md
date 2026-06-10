---
name: header-composer
description: >
  Phase 4-lite (Promote) stage of the patent-essay pipeline: composes the 5:2 X-Article
  header image for a finished essay. Picks the copy (headline tease, badge number, index
  strip) from the accepted essay + Phase-1 figure selection, writes a header-spec.json,
  and renders it deterministically with scripts/make_header.py (house light-editorial
  design system: cream paper, ink black, single warm-orange accent, real patent figure).
  Use after the Compose↔Edit loop passes, or when asked to make/remake an article header.
  NOT for: promo post text (unported promo-composer), essay composition, figure selection.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# header-composer

Turns the accepted essay into a click-worthy 5:2 header. The aesthetic judgment is frozen
in `references/design-system.md` + `scripts/make_header.py`; this skill's inferential job
is only the **copy and asset choices**, so every run reproduces the house look.

```
handoff/03-edit/essay-final.md  +  handoff/01-design/figure-selection.md
    → choose: variant · headline tease · badge · figure · caption · strip
    → handoff/04-promote/header-spec.json
    → python .claude/skills/header-composer/scripts/make_header.py
        --spec handoff/04-promote/header-spec.json
        --out  handoff/04-promote/header.png
    → view the PNG, fix copy collisions if any, re-render
```

## Inputs

- `handoff/03-edit/essay-final.md` — the accepted essay (title, lead objection, closing
  line, key numbers).
- `handoff/01-design/figure-selection.md` — the header figure row (orientation role) and
  its sheet file under `input/figures/`.
- `references/design-system.md` — the visual grammar. Do not invent a new one per run.

## Copy rules (the inferential part)

1. **Never repeat the article title** — X renders the title directly under the header.
   The header teases; the title pays off. Default headline source, in order of
   preference: the essay's closing line (if ≤ 8 words), the lead's posed objection
   (compressed), or the core numeric contrast.
2. **Badge** = the one number the essay hangs on (e.g. `9 CURRENT LEVELS`). Uppercase,
   ≤ 3 words.
3. **Accent word**: exactly one word of the headline may be `"color": "accent"` — the
   word carrying the reversal (e.g. *never*). Zero is fine; two is not.
4. **Index strip** = 4-6 uppercase tokens walking the essay's spine (component names,
   key quantities). No marketing words.
5. **Figure** = the Phase-1 header figure (orientation role), verbatim file. Caption ≤ 6
   words after `FIG. N · `, stating the absence/contrast the figure proves.
6. Mechanical rules from `_shared/references/deliverable-voice-rules.md` apply to header
   copy: no em-dash, no banned AI-tell terms (use `·` as separator).

## Variants

- `editorial` (default): serif statement + real patent figure. The house header.
- `numbers`: struck old value → giant new value. Use when the essay's hook is a numeric
  collision and the closing line is too long to set well.

Render BOTH when unsure, view them, pick one, and record the choice + reason in one line
of the spec's `"note"` field.

## Outputs

- `handoff/04-promote/header-spec.json` — the full spec (schema:
  `handoff-template/04-promote/header-spec.json`). This file is the reproducibility
  contract: re-running the script on it must regenerate the identical PNG.
- `handoff/04-promote/header.png` — 2000×800 (5:2). Alternate variant, if rendered, as
  `header-alt.png`.

The orchestrator archives both to `runs/<essay-id>/header/`.

## Process

1. Read the essay + figure-selection. Draft the copy per the rules above.
2. Write `header-spec.json`; run the renderer; **view the PNG** (Read tool renders it).
3. Check: headline fits without crowding the figure (the script auto-shrinks, but copy
   that *needed* shrinking below ~96px usually reads worse — shorten the line instead);
   nothing collides; strip ≤ canvas width.
4. Iterate copy (not the design system) until clean. Two iterations is typical.

## Dependencies / fencing

- Pillow (`pip install pillow`) — the repo's only non-stdlib dependency, isolated here;
  the gate layer never imports it. Fonts are vendored under `assets/fonts/` with their
  OFL licenses (Space Grotesk, Fraunces, IBM Plex Mono).
- Voice fencing: this stage reuses sentences already shaped by the voice-on composer and
  passed by the editor; it loads `deliverable-voice-rules.md` for mechanical rules only —
  not `voice-profile.md`, not the voice canon.

## Out of scope

- Promo/digest post text — v1 `promo-composer`, preserved unported in
  `docs/source-prompts/04-promote/`.
- New visual systems per essay (the system is the brand; change it via a
  `pipeline-retro` proposal, not per run).
