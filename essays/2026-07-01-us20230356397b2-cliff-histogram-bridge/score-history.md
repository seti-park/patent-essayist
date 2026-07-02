# Score history — US 2023/0356397 A1 "Cliff Detection in Robotic Devices"

STM VL53L9CX series, article 3 of 3 ("The Bridge"). Compose<->Edit inner loop. Threshold
`pass` (default), posture `measured`, mode `walkthrough`, max 4 iterations.

## Inner loop (Compose ↔ Edit)

| Iter | Deterministic gates | Editorial assessment | Round result | Note |
|---|---|---|---|---|
| 1 | PASS (0 fail; ~2 structure + ~20 typography warn) | `revise-required` — 2 high, 3 medium, 4 low | FAIL | grounding hard-gate breach: a quote verbatim-matching `[0018]` was cited `[0025]` (pass-3, high); 5 paragraphs exceeded the mobile-readability heuristic (pass-5, high); plus a misplaced `[0086]` anchor and 2 overlength paragraphs (medium) |
| 2 | PASS (0 fail) | `revise-recommended` — 1 medium, 1 low | FAIL (below `pass` threshold) | citation fixes ([0025]->[0018], [0086] repositioned, [0036] overclaim softened) and the two flagged paragraph splits resolved both v1 highs cleanly, re-verified byte-for-byte; residual: 5 more paragraphs still marginally over the mobile-line threshold |
| 3 | PASS (0 fail) | `revise-recommended` — 1 medium, 1 low | FAIL | 4 of the 5 flagged paragraphs split; a fresh whole-essay recompute (not just the touched region) surfaced 2 more pre-existing marginal paragraphs plus the steelman/SLAM-fencing paragraph, deliberately left as one rhetorical unit |
| 4 | PASS (0 fail) | **`pass` — 0 high, 0 medium, 1 low** | **PASS** | a script-verified sweep (word_count/12 > 8, i.e. >96 words) confirmed zero paragraphs over threshold across all 32 body paragraphs; loop terminates at the iteration cap (4/4) with a clean pass, not a forced stop |

The single low finding carried unchanged across all 4 rounds (`# Sources` horizon-cluster
entries compressed to number + one-word descriptor, and the hero/secondary patent entries
omitting an unverifiable publication date) was reviewed each round and confirmed a deliberate,
brief-mandated choice, not a defect — `essay-context.md` explicitly instructs the horizon
cluster be "cited only as a horizon, a line or clause each," and `invention-summary.md`'s own
metadata section could not verify a publication date on this extraction's cover fields.

### Hard-gate checks (final state)
- Grounding hard-gate (goal 1): clear. No pass-3 high/critical; `gate_anchors` PASS.
- Goal-2 hard-gate: clear. No `FIGUSE-001`; all 7 figure numbers used (figures 1 and 2 required
  a deliberate bare "FIG. 1" / "FIG. 2" token per a mechanical gate gotcha — see
  `handoff/01-design/figure-selection.md` — since both exist in this patent only as lettered
  sub-figures, 1A-1C and 2A-2D).

### Why 4 iterations, not 1
Every deterministic gate passed clean from the first draft; all 4 rounds were driven purely by
the editorial layer, and 3 of the 4 rounds were the same finding class recurring at shrinking
magnitude (a citation-dense, mechanism-heavy essay kept producing paragraphs that hovered right
around the 96-word/8-mobile-line heuristic boundary as earlier splits were applied). The one
substantive (non-cosmetic) defect — the `[0025]`/`[0018]` mis-citation — was caught and fixed in
round 1->2 and never recurred.

## Post-acceptance self-audit (Layer 3, autonomous)

Two independent rounds, each with 2 reviewers in separate forked contexts (personas: impatient
investor, skeptical pro-subject reader), no exposure to the inner loop's edit-logs, to each
other, or (in round 2) to round 1's findings.

**Round 1 (fresh read of the iteration-4 `pass` draft):** both reviewers independently caught
the same defect from different angles — the essay's central "quote Claim 1 exactly as filed"
sentence was actually the specification-summary paragraph (`[0005]`), missing Claim 1's own
"identifying a convergence..." limitation, and a second reference to that exact claim-1 phrase
was cited to `[0005]` even though that phrase never appears there. Verified byte-for-byte against
`input/patent.md` and applied (this is a recurrence of `claim-vs-spec-citation-conflation`, a
class first seen once before in this system, run 045 — see `revision-notes.md`). Reviewer B
additionally caught a real technical overgeneralization (the essay implied FIGS. 5-7's three
false-positive tests all shared one ambient-light mechanism; only FIG. 5 genuinely does) and a
closing-sentence scope overreach on the STM/SLAM relationship. All 3 applied; 5 further items
(a sanctioned emoji misflagged as an error, a split verdict on lead timing, a steelman-strength
taste critique, an unsourced-but-common-knowledge framing claim, and a borderline
section-length observation both reviewers rated PASS) were considered and logged as
not-applied. Full detail and rationale: `revision-notes.md`.

**Round 2 (confirmation pass, 2 more fresh reviewers, cold read of the round-1-corrected
essay):** ran to satisfy the design's "a second blind pass confirms convergence" requirement.
Reviewer A (impatient investor) found no new high/medium findings and confirmed every round-1
fix held on independent re-check. Reviewer B (skeptical pro-subject reader) surfaced 5 new
candidate findings; each was independently verified against `input/patent.md` (and, for one,
a live web search against ST's actual blog) before deciding: 2 held up and were applied (a
dropped word in a quoted ST blog title, confirmed via live search; an over-generalized
description of FIG. 3's six-line graph that misattributed a "jump" to all six lines when the
patent only describes the three median-distance lines moving at that instant). The other 3 did
not survive verification or the multi-vote bar: a jargon-signpost claim that was factually
wrong on inspection ("time-of-flight" does appear spelled out in the essay's own prose, contra
the reviewer's stated premise), a re-flagged SLAM-wording concern split against Reviewer A's
independent "no findings" the same round, and a technically-accurate-but-genre-disproportionate
claim-1-vs-claim-21 patent-construction observation. Full detail: `revision-notes.md`.

**Convergence assessment:** stopped after round 2 of the 3-round cap. Round 2's hit rate (2
applied of 5 candidates) was lower than round 1's (3 applied, all corroborated or independently
verified), and a majority of round 2's candidates were reviewer artifacts rather than real
defects — a reasonable stopping point short of the cap. The two remaining open items are logged
as watch/design-stage items, not forced into the essay.

Gates re-run after every fix, both rounds: `passed: true`, 0 fail findings across all 11 gates;
every paragraph re-verified under the 96-word mobile-readability threshold (max 95 words, 34
body paragraphs in the final state).

## Meta-loop signal

The primary self-audit finding (`claim-vs-spec-citation-conflation`) is now a **2nd occurrence**
of a class first logged as `watch` (count 1) from run `045-agility-638-last-mile-moat`. Per
`meta/attribution-table.md`'s `RECUR_THRESHOLD` (default 3), this does not yet cross the
auto-promote line, but two independent essays hitting the identical defect shape (verbatim claim
language cited with a specification-paragraph `[dddd]` bracket instead of being attributed by
claim number in prose) is a meaningful signal for `pipeline-retro` to weigh.
