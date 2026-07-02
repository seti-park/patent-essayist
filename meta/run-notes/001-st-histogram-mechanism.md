# Run notes — `001-st-histogram-mechanism`

Run-scoped retro narrative, moved verbatim out of `meta/attribution-table.md`
(2026-07-02 meta-harvest refactor). One file per run: parallel Claude Code
sessions append run notes here without ever conflicting on the shared
attribution table. Durable class-routing knowledge stays in the table;
counts are derived by `meta/tally_ledger.py`.

## Run `001-st-histogram-mechanism` (2026-07-01)

US 2026/0140238 A1, Article 1 of 3 in the STM VL53L9CX series. 3 inner-loop rounds (iter 1
revise-recommended → iter 2 revise-recommended → iter 3 pass), then a dry self-audit round
(0 applied edits — nothing cleared the multi-vote bar).

**`figuse-selection-scope-overread` promoted `watch` → `recommended-apply`** (recurrence_count
1 → 2): this run is the second occurrence the sibling proposal
(`2026-06-24-figuse-selection-scope.md`) predicted verbatim — a `## Selected figures` /
`## Not selected (and why)` sectioned selection file where the dropped figures (FIG. 3-7) are
not echoed in prose, producing 5 real `FIGUSE-001` false fails in every one of the run's 3
rounds (15 false fails total). The orchestrator manually adjudicated goal 2 as clear each
round (the real `## Selected figures` set — FIG. 1, FIG. 2 — has zero orphans). See the
proposal file's 2026-07-01 update block for the full re-verification.

**New class `typography-html-comment-blindspot`** (watch, count 1): `gate_typography.py`'s
`EXCLAIM_RE` exempts Markdown image syntax `![` but not HTML comments `<!--`, so an internal
`<!-- ... -->` process annotation in the draft false-fires `EXCLAIM-001` (hard-fail) on the
comment's opening `!`. Fired in round 1; worked around by deleting the stray comment (a
content-layer fix, not a gate fix). Distinct from `figuse-selection-scope-overread` (different
file, different check) and `figure-token-regex-blindspot` (lettered-panel suffixes, same gate
script but a different regex). Proposal: `2026-07-01-typography-html-comment-blindspot.md`.

**New class `header-title-near-duplicate`** (watch, count 1): the H1 and the first `##`
section header shared the same "[subject] Cannot Time a [X] With a Stopwatch" sentence frame
— a near-verbatim restatement rather than an escalation from title-hook to lead-hook. Resolved
in round 2 (H1 states the paradox, first `##` now states the resolution). Single occurrence;
no proposal filed yet, watching for recurrence. Distinct from `voice-canon-cadence-drift`
(cadence matching against canon exemplars) and from pass-7 check 2 header-as-claim (whether
headers reconstruct the argument on a skim, not whether two adjacent headers duplicate each
other).

**Recurring, matches existing rows (no new class):** `mobile-paragraph-wall` (9 dense
paragraphs in round 1, 1 residual in round 2 — same class as the on-file
`recommended-apply` `2026-06-11-gate-structure-word-wall.md`, now recurrence 8 by record
count); `redundancy-bloat` (the "full histogram" motif recurrence, explicitly judged
sanctioned-layering not filler — same heterogeneous-mechanism class deliberately held at
`watch`, now recurrence 7); `spec-undercoverage` (a `[0004]` spine-trace anchor promised in
`thesis-spine.md` but with no matching Quote-anchor entry in `invention-summary.md` — a
Phase-1 backfill item, logged not papered over, matches this row's existing owner artifact);
`jargon-gloss-gap` (the series-vocabulary "zone = cell" equivalence gap, resolved round 2 —
same mechanism as the existing row, with a series-continuity wrinkle noted in the ledger
record).

**Self-audit calibration data point (does not fit the ledger schema cleanly, flagged for
human judgment):** one self-audit reviewer raised a HIGH-severity claim-scope grounding
finding that did **not** survive the orchestrator's own independent verification against
`input/patent.md` (the reviewer conflated two distinct senses of "full histogram processing
capabilities" in the patent's own vocabulary). Correctly not applied (reviewers split 1-1, no
majority; the orchestrator's direct check refuted rather than confirmed it). Logged as
`self-audit-reviewer-false-positive` (`root_cause_stage: self-audit-process`, not a
design/compose/gate/canon stage) — this is reviewer-precision calibration data, not an essay
defect, and the existing schema's "stage that should have prevented it" framing does not map
cleanly onto "a reviewer's own false-positive rate." Single data point; not a proposal trigger
on its own. Worth tracking as its own dimension if a recurring pattern of claim-scope
false-positives (as opposed to the channel's several *true*-positive catches, e.g.
`anchor-offbyone`, `claim-scope-misattribution` elsewhere in this table) emerges across future
self-audit runs.
