# Score history — US 2024-0192337 B2 crosstalk-rejection article (VL53L9CX series, Article 2 of 3)

Compose↔Edit inner loop. Threshold `pass`, posture `measured`, max 4 iterations, self-audit on
(default), max-selfaudit-iter 3 (default).

## Inner loop

| Iter | Deterministic gates | Editorial assessment | Round result | Note |
|---|---|---|---|---|
| 1 | PASS (0 fail; figure_use also fixed mid-run, see below) | revise-required (1 high, 1 medium, 2 low) | **FAIL** | High: `# Sources` block missing a `## Patents` subheading for the two analyzed patents. Medium: one 234-word/3-idea paragraph in §6 past the compression threshold. Two low/optional notes. |
| 2 | PASS (0 fail, 0 warn beyond non-blocking) | pass (1 low, non-blocking) | **PASS** | High + medium fixed (Sources/Patents added; §6 paragraph split in two, no content cut); one FIG.1 caption tweak applied. Loop terminates. |

Terminated at iteration 2 (cap 4), result PASS. A small optional low-severity polish (citation
field label "filed" -> "priority", matching repo precedent) was applied directly before
promotion since it required no new review round.

### Mid-run infrastructure fix (not an essay defect)
`gate_figure_use` initially returned 6 false-positive `FIGUSE-001` orphans (figures 2, 7, 8, 11,
14, 15) because it scanned figure-selection.md's rejection-rationale prose/HTML-comments (which
legitimately name rejected figures by number) as if they were selections. Confirmed as a script
bug, not a design or draft defect (the actual "## Selected figures" table only ever listed
figures 1/3/6/9/10/12/13, which the draft used correctly). Fixed in
`.claude/skills/_shared/scripts/gate_figure_use.py` (scope parsing to the "## Selected figures"
section, HTML comments stripped) with 2 new unit tests + a regression fixture; full
`meta/regression.py` suite passes, and `essays/agility-us12560948`'s gate result is unchanged.
Committed separately from this essay's content (commit `5568e36`).

## Hard-gate checks (final state)
- Grounding hard-gate (goal 1): clear. No pass-3 high/critical in either review round;
  `gate_anchors` PASS.
- Goal-2 hard-gate: clear. No `FIGUSE-001` (after the gate fix); figures 1, 3, 6, 9, 10, 12, 13
  all used; pass-3 coverage sub-check clean both rounds.

## Layer 3 — post-acceptance self-audit (after inner-loop PASS)

Two fresh-context reviewers per round (impatient investor, skeptical pro-subject reader),
separate forked contexts, no exposure to the design/drafting process, running the
pass-7-adversarial-reader checklist + grounding spot-checks against `essay-final.md` +
`input/patent.md` directly.

| Round | Findings surfaced | Applied (multi-vote) | Considered, not applied |
|---|---|---|---|
| 1 | anchor mis-cite (`[0003]` for a claim [0032] actually supports); "not a per-unit factory trim" asserted as patent fact when the patent's own word for the mechanism is "calibration" [0033]; 3 split 1-1 style/structure checks (BLUF lead-altitude, header-as-claim, section-rhythm); 1 self-doubted single-reviewer meta-posturing note; 1 single-reviewer "steelman could be sharper" suggestion | 2 (both independently verified by the orchestrator against `input/patent.md` directly) | 5 (split between reviewers, or single-reviewer taste/depth suggestions, per `scoring-rubric.md`'s "gates OVERREACH, not OVER-HEDGE") |
| 2 | none new (both reviewers independently re-ran the full checklist plus targeted checks on the round-1 fixes) | 0 | 0 (round 1's split items re-surfaced identically, not new) |
| orchestrator pass (post round-2-dry) | a second, parallel instance of the round-1 "calibration" overreach in §3 (FIG. 9 mechanism paragraph) that neither reviewer's brief scoped them to check (they were asked specifically about the §6 sentence) | 1 (same well-verified pattern as round 1's applied fix; applied directly rather than spinning up a third reviewer round for a single already-validated consistency fix) | — |

**Loop-until-dry: converged at round 2** (cap 3), plus one orchestrator consistency catch after. Fixes were applied "at the source" in
`handoff/01-design/invention-summary.md` (with a `> Revision note`) so a recompose cannot
reintroduce them, then propagated to `essay-draft.md`, `publication.md`, `essay-final.md`. Full
detail + rationale for every applied and not-applied finding: `handoff/03-edit/revision-notes.md`.
Normalized to `meta/findings-ledger.jsonl` as `origin: self-post-accept` (pattern_tags
`anchor-offbyone`, `external-fact-universalization`).

## Contrast / lesson
Both editorial-review rounds' Pass 3 (claim adequacy + fact verification) reported the `[0003]`
citation as clean ("preserves source meaning without drift") in both iterations — this is
exactly the kind of blind-spot the self-audit layer exists to catch: a pass that reports a
citation checked without actually confirming the cited paragraph's content matches the claim
attached to it, versus merely confirming the paragraph exists and is histogram-related.
