# Figure Selection

## Selected figures

All 7 of the patent's figure numbers are selected — this patent's figure set is compact
(9 cleaned assets covering FIGS. 1A-1C, 2A-2D, 3-7) and every one earns a place against
the spine: FIGS. 1 and 2 establish the system and the event, FIG. 3 is the single best
visual for the core mechanism, and FIGS. 4-7 are the claimed logic made explicit.

| Figure | File | Thesis point (spine element / section) | caption_role |
|---|---|---|---|
| FIG. 1 | fig-01AB.png (1A-1B), fig-01C.png (1C) | System overview — robot + sensor + navigation system block diagram (1A-1B) and the ROI/row geometry the whole mechanism depends on (1C) (2-problem, 3-core-claim) | header_composite |
| FIG. 2 | fig-02AB.png (2A-2B), fig-02CD.png (2C-2D) | The robot approaching the edge across the too-far / long / medium / short stages — the event the essay narrates (3-core-claim, 4-analogy) | body_figure_carries_unique_info |
| FIG. 3 | fig-03.png | The graph of median ground distance and peak intensity per row over time — row-lines hold flat, diverge, converge, then spike/drop at the edge. Single best visual for the core mechanism (3-core-claim, 4-analogy) | body_figure_carries_unique_info |
| FIG. 4 | fig-04.png | Process flow, all three ranges together — the claimed method stated as a 3-block flowchart (3-core-claim) | body_figure_prose_covers_fully |
| FIG. 5 | fig-05.png | Process flow, long-range detection (peak-intensity-vs-ambient test) (3-core-claim) | body_figure_prose_covers_fully |
| FIG. 6 | fig-06.png | Process flow, medium-range detection (median-distance convergence test) (3-core-claim) | body_figure_prose_covers_fully |
| FIG. 7 | fig-07.png | Process flow, short-range detection (loss-of-ground test) (3-core-claim) | body_figure_prose_covers_fully |

## MECHANICAL GOTCHA — bare "FIG. 1" / "FIG. 2" tokens required in the draft (flag for
Phase 2)

**This note is the load-bearing part of this file for gate compliance — read before
drafting.**

The deterministic figure-use gate (`gate_figure_use.py`) matches figure numbers with
`\bfig(?:ure|\.|-)?\s*0*(\d+)\b` — a word boundary is required immediately after the
digit run. A trailing letter (as in "FIG. 1A" or "FIGS. 1A-1C") breaks that boundary, so
**neither of those tokens registers as a reference to figure 1** under this regex — only
a bare "FIG. 1" / "Figure 1" (no trailing letter) token counts. The same applies to
figure 2: "FIG. 2A", "FIGS. 2A-2D", etc. do not register; only bare "FIG. 2" does.

In this patent, figures 1 and 2 **only exist as lettered sub-figures** — there is no
plain "FIG. 1" or "FIG. 2" drawing, only 1A/1B/1C and 2A/2B/2C/2D. This is the same
mechanical situation a prior run handled for an analogous FIG. 5A-5AD case (see
`meta/improvement-proposals/2026-06-11-figure-token-panel-suffix.md` — the fix is
proposed but not yet applied to the gate scripts as of this run, so the regex above is
still the live, unfixed one).

**Required action for Phase 2 Compose**: the essay draft must include, in addition to
whatever lettered captions it uses (e.g., "FIG. 1B," "FIGS. 2A-2D"), **at least one bare
"FIG. 1" token and at least one bare "FIG. 2" token** somewhere in the body prose — for
example "FIG. 1 shows the mobile robot's front-mounted sensor feeding its navigation
system" or a parenthetical "(FIG. 1)" — so that the mechanical gate registers figures 1
and 2 as used. Without this, `gate_figure_use.py` will hard-fail with two orphan findings
(FIGUSE-001 for figure 1 and figure 2) even though both figures are genuinely,
substantively used in the draft. This is carried forward as trap (d) in
`phase2-handoff-notes.md`.

## Paired-figure relationships (acknowledged)

| Figure(s) | Relationship | Treatment in selection |
|---|---|---|
| FIG. 1A + FIG. 1B + FIG. 1C | same-page sub-figure set (robot overview / navigation block diagram / ROI detail) | All three treated as ONE cognitive unit under "FIG. 1" — none dropped; 1A-1B (fig-01AB.png) and 1C (fig-01C.png) are both selected and both captioned, with the required bare "FIG. 1" token per the gotcha note above |
| FIG. 2A + FIG. 2B + FIG. 2C + FIG. 2D | progressive sequence (too-far → long range → medium range → short range) | All four treated as ONE cognitive unit under "FIG. 2" — the sequence is load-bearing (it IS the event the essay narrates) and splitting it would break the before/after meaning; both cleaned composites (fig-02AB.png, fig-02CD.png) selected together |
| FIG. 4 / FIG. 5 / FIG. 6 / FIG. 7 | overview-then-detail sequence (FIG. 4 = 3-range overview; 5/6/7 = long/medium/short sub-flowcharts) | All four selected as a set — FIG. 4 gives the reader the claimed method at a glance, FIGS. 5-7 back it with the per-range decision logic; none dropped, since together they are the clearest visual restatement of claim 1's "convergence" language |
| FIG. 3 | standalone | Selected as the single best mechanism visual (per essay-context.md's own figure note) — no pairing constraint |

No pair is broken in this selection. All 9 cleaned figure assets are used; all 7 figure
numbers (1-7) are selected.

## Header / body assignment

- **Header**: FIG. 1 (fig-01AB.png, with fig-01C.png as an immediate companion) — the
  robot + sensor + navigation-system overview is the natural entry visual, anchoring the
  hook's "why doesn't a robot vacuum fall down the stairs" question in a concrete system
  before the mechanism unfolds.
- **Body**: FIG. 2 (fig-02AB.png, fig-02CD.png), FIG. 3 (fig-03.png), FIG. 4 (fig-04.png),
  FIG. 5 (fig-05.png), FIG. 6 (fig-06.png), FIG. 7 (fig-07.png).

<!-- No revision-loop triggers encountered during Step 9 of this run. -->
