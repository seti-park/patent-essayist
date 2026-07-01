# Revision notes — 051-stm-cliff-detection-histogram-bridge

> Revision-delta capture channel. This run's inner loop (Compose<->Edit) reached a clean
> `overall_assessment: pass` on iteration 4/4 (`handoff/03-edit/edit-log.md`,
> `review_id: ...-editorial-review-4`). The deltas below are from the **post-acceptance
> self-audit** (Layer 3, `origin: self-post-accept`): 2 reviewers in separate forked contexts
> (personas: impatient investor, skeptical pro-subject reader), each with zero exposure to the
> prior edit-logs or to each other's findings, independently re-read `essay-final.md` against
> `input/patent.md` cold. Findings below were applied after multi-vote (agreement between both
> reviewers, or independent verification of a single reviewer's grounding claim against
> `input/patent.md` directly — both conditions satisfied for every delta logged here).

## delta
class: claim-vs-spec-citation-conflation
round: self-audit
before: "Claim 1 states it directly... quoting exactly as filed... 'comparing a statistical distribution... detecting an approaching of the edge of the cliff' [0005]" -- and, later, "Claim 1 calls this whole family of changes 'identifying a convergence' [0005]"
after: the claim-1 quote now carries the full granted claim-1 text, including "the comparing comprising identifying a convergence of an intensity of the reflected signals or of a median distance to a ground," attributed by name ("Claim 1 states it directly...") with no [dddd] bracket; the second, redundant "identifying a convergence" [0005] reference was removed (the idea is now covered once, correctly, in the fixed quote)
rationale: both self-audit reviewers independently caught this, from different angles (Reviewer A checked the exact phrase against [0005] and found it absent; Reviewer B independently checked claim 1 as granted against the quoted text and found the quote was actually the [0005]/[0110]/Abstract boilerplate, missing claim 1's own disjunctive limitation). Verified byte-for-byte against input/patent.md before applying: [0005] does not contain "identifying a convergence" anywhere; that phrase exists only in the claims (청구항 0001항, 청구항 0008항), which are not [dddd]-paragraph-numbered in this document. This is the SAME finding class as run 045's first occurrence (see meta/findings-ledger.jsonl, essay_id 045-agility-638-last-mile-moat, pattern_tag claim-vs-spec-citation-conflation, currently status "watch" at count 1) -- this is occurrence #2 of the identical defect shape (verbatim claim language cited with a specification-paragraph [dddd] bracket instead of being attributed by claim number in prose), recommending pipeline-retro promote this class per RECUR_THRESHOLD.

## delta
class: paraphrase-substantive-change
round: self-audit
before: "FIG. 6 runs the equivalent check for the medium-range convergence test, and FIG. 7 covers the simplest of the three, whether the ground has been lost entirely. Two independent signals, checked against a live ambient reading rather than a fixed number, is what keeps 'the floor changed color' from reading as 'the floor ended.'"
after: FIG. 6 is now described as a distinct percentage-convergence test with no ambient-light component; FIG. 7's ambient-rate use is scoped to its actual conditional sub-case (the "distances increase" branch only); closing line changed to "Three separately-triggered tests, not one test run three times, is what keeps..."
rationale: Reviewer B (skeptical pro-subject reader) flagged that "equivalent check" and "two independent signals... ambient reading" imply all three range-tests share one ambient-light-based mechanism. Verified against input/patent.md [0090]-[0091] (FIG. 5 / long range: genuine ambient-rate comparison), [0097]-[0100] (FIG. 6 / medium range: pure percentage-threshold convergence test, no ambient-rate involvement at all), and [0103]-[0106] (FIG. 7 / short range: ground-loss test, ambient-rate only required in the sub-case where distances increase). The original synthesis line overgeneralized three structurally distinct sub-tests into one shared mechanism.

## delta
class: closing-scope-overreach
round: self-audit
before: "**STM is not solving SLAM here. It is building the senses, and the reflex, that a SLAM stack has to stand on before it can do anything else.**"
after: "**STM is not solving SLAM here. It is building one of the senses, and a reflex, a SLAM stack needs if it is going to trust the ground under it.**"
rationale: Reviewer B judged that while the sentence avoids the literal banned phrase ("STM solves SLAM"), "has to stand on before it can do anything else" implies a SLAM stack architecturally depends on this one patent's specific reflex, which overstates the closing claim beyond what the patent supports (cliff/edge detection and SLAM are typically loosely-coupled subsystems in practice). This is a single-reviewer, judgment-level finding (not independently corroborated by Reviewer A, and not a byte-verifiable fact against the patent text the way the two deltas above are) but ties directly to essay-context.md's explicit hard guardrail against overclaiming STM's SLAM role, so it was applied as a minimal, low-risk, non-structural wording change rather than logged as watch-only. Flagging as a new class -- not yet in meta/attribution-table.md -- for pipeline-retro to route (goal 1 grounding-proportionality / thesis-spine adversarial-defense steelman-refine scope, tentatively).

## considered — not applied

- **Closing 🤔 emoji** (both reviewers flagged independently as a tonal misstep / polish concern): NOT applied. Verified against `.claude/skills/_shared/references/deliverable-voice-rules.md` ("No emoji (the single sanctioned closing 🤔 excepted)") and `.claude/skills/editorial-review/references/pass-1-voice-anti-ai.md` ("only 🤔 at essay end for closing-open-question pattern") -- this is sanctioned house style, used exactly once, at the very end, for the closing-open-question pattern. Both reviewers were deliberately kept uncontaminated from pipeline-internal canon (fresh-eyes design), so neither had the context to know this is intentional. False positive, no action.
- **BLUF lands one paragraph late** (Reviewer A only, low-medium; Reviewer B rated the same passage a clean PASS): NOT applied. Split verdict between the two reviewers on a taste-level read; per self-audit policy, split/taste-only findings are logged, not forced in.
- **Steelman answers a scope objection (SLAM) rather than a sharper novelty/validity objection** (both reviewers touched this from different angles -- Reviewer A: "is multi-zone row comparison actually novel"; Reviewer B: closer inspection folded into the FIG 5/6/7 accuracy delta above): NOT applied as a standalone fix. Partially addressed by the FIG 5/6/7 precision delta above (removes the specific technical smoothing that made the existing steelman look thinner than it is). Adding a third, novelty-focused steelman would be new argumentative content beyond a self-audit's surgical-fix scope, and reasonable readers disagree on which objection is "strongest" -- logged as watch for a future design-stage revisit, not a defect.
- **"For decades that was the standard placement"** (Reviewer B, low-medium; unsourced historical-duration claim): NOT applied. Judged as ordinary scene-setting narrative framing (bottom-mounted IR/ultrasonic cliff sensors on robot vacuums are documented from the early-2000s Roomba era, so "decades" is defensible general domain knowledge by 2026) rather than a specific fact requiring a citable source; essay-context.md does not flag this as a fact needing sourcing.
- **Section-length imbalance** (both reviewers, low, explicitly rated PASS/borderline-PASS by both, not a true stub): NOT applied. Within normal rhythm variance; gate_stub independently confirms no hard stub.

## Post-fix verification

- `python3 .claude/skills/_shared/scripts/run_gates.py --draft handoff/02-compose/essay-draft.md --invention-summary handoff/01-design/invention-summary.md --figures handoff/01-design/figures-index.txt --figure-selection handoff/01-design/figure-selection.md --mode essay --json` -> `passed: true`, 0 fail findings across all 11 gates (re-run after all 3 deltas applied).
- Every `[dddd]` anchor remaining in the draft (`[0004] [0018] [0019] [0026] [0035] [0036] [0043] [0045] [0046] [0050] [0051] [0054] [0082] [0083] [0086]`) confirmed present in `invention-summary.md`'s anchor set; `[0005]` no longer cited (its content is now correctly quoted as part of the claim-1 sentence, attributed by claim name, not by paragraph bracket).
- All essay-body paragraphs re-verified under the 96-word / 8-mobile-line Pass-5 threshold after the FIG. 6/7 split (max 95 words).
- `draft_version` bumped 4 -> 5; `publication.md` regenerated; `essay-final.md` re-promoted from the corrected `publication.md`.
