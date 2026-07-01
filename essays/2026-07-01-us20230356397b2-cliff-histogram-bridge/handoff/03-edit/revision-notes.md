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

## Round 2 (confirmation pass — loop-until-dry, second forked-context round)

Per the design's "a second blind pass confirms convergence" requirement, a second round of 2
fresh reviewers (same two personas, zero exposure to round 1's findings or to each other) read
the round-1-corrected `essay-final.md` cold. Reviewer A (impatient investor) reported no new
high/medium findings and confirmed the round-1 fixes hold (steelman still strong, claim-1 quote
still exact, FIG. 5/6/7 distinction still clean, SLAM claim still proportionate) — 2 new
low-severity observations only (both logged below as not-applied). Reviewer B (skeptical
pro-subject reader) surfaced 5 new items; each was independently verified against
`input/patent.md` (and, for one external claim, a live web search) before deciding whether to
apply -- 2 held up and were applied, 3 did not survive verification or were split against
Reviewer A and are logged as not-applied.

## delta
class: quote-fidelity-gap
round: self-audit-r2
before: "1st 3D ToF LiDAR with 2.3K zones and flood illumination" (as an exact quote of ST's blog title)
after: "1st 3D ToF LiDAR sensor with 2.3K zones and flood illumination" (word "sensor" restored)
rationale: Reviewer B flagged that the essay's quote silently drops a word from ST's actual blog title. Independently verified via a live web search (title snippet returned verbatim: "VL53L9: 1st 3D ToF LiDAR sensor with 2.3K zones and flood illumination... - The ST Blog") -- confirmed real, not a hallucinated web check. The dropped word originated in this run's own `essay-context.md` (which had transcribed the same incomplete quote from the upstream series-context brief) and was carried through unchanged by every pipeline stage; fixed here since this is the first point a byte-level check against the live source was actually performed.

## delta
class: figure-mechanism-oversimplification
round: self-audit-r2
before: "FIG. 3's graph is the same event turned into six lines... sitting flat and evenly spaced while the floor holds, then the peak-intensity lines dropping through the ambient rate one after another, then all six lines jumping together the instant the sensor loses the near floor and starts reading the far one."
after: split into two paragraphs; the medium-range convergence phase (median-distance lines converging toward each other) is now named explicitly, and the final "jump" is correctly attributed to only the three median-distance lines, not all six.
rationale: Reviewer B checked this sentence against patent paragraph [0077] ("the fourth line 310, the fifth line 312, and the sixth line 314 may all increase" -- naming only the three median-distance lines) and against the essay's own earlier description of the peak-intensity lines already having dropped below ambient during the long-range phase (so they would not also "jump" at the short-range instant). Independently re-verified against [0077] and against a direct visual read of `figures/fig-03.png` (six-line graph: three median-distance lines visibly converge before jumping up together at the right edge; the three peak-intensity lines visibly bottom out near the ambient-rate line earlier and stay low). The original sentence also skipped the medium-range convergence phase entirely, collapsing two distinct visual phases into one.

## considered — not applied (round 2)

- **Jargon-as-signpost finding** (Reviewer B, medium: claimed "time-of-flight is never spelled out in the essay's own prose" and SPAD/ROI are jargon gaps): NOT applied. Independently verified false on its central premise -- "time-of-flight" appears spelled out in the essay's own body prose (not just captions), e.g. "A single time-of-flight reading is a snapshot" (opening sentence of section 2). SPAD/ROI-as-acronyms do appear only inside the verbatim claim-1 quote, but their plain-English concepts (counting photons; "the region of interest carves out the bottom three rows") are thoroughly explained in the surrounding prose, which is what the check actually requires. Reviewer A's independent read the same round found no jargon-depth issue. Logged as a reviewer error on verification, not a real defect.
- **SLAM-stack word-choice re-flagged** (Reviewer B only, medium; Reviewer A explicitly re-checked the same sentence the same round and found "no findings"): NOT applied a third time. Split verdict between the two round-2 reviewers on a sentence already softened once in round 1 (see the `closing-scope-overreach` delta above); per self-audit policy, split/taste-level findings are logged, not force-applied, especially on a sentence that has already been revised once for the identical concern.
- **Claim 1 (general, disjunctive) vs. claim 21 (fully elaborated three-range embodiment) scope proximity** (Reviewer B only, medium; not raised by Reviewer A in either round): NOT applied. Verified the underlying patent-construction observation is technically accurate (claim 1's "convergence" test does not itself recite three ranges; the three-range architecture is claim 21's, dependent through claim 9, plus the specification's examples) -- but the essay's own text already has two full paragraphs of narrative distance between the claim-1 quote and the "three recognizable stages" description, never re-invokes "claim 1" for the three-range specifics, and grounds those specifics in specification paragraphs ([0051], [0054], [0083]), not a claim citation. This is a legitimate but genre-inappropriate level of claim-construction precision for a general-audience series essay (see the existing agility-run precedent's own scope note: "not a legal opinion on claim validity"); logged as watch for design-stage awareness rather than a drafting defect.

## Human post-accept update (after archiving, meta-loop, and push — a new revision-delta round)

## delta
class: sources-entry-template-drift
round: human-post-accept-1
before: "US 2021/0268903 (anti-collision)." / "US 2026/0087695 (histogram-based scene change)." / "US 2022/0067346 (depth and inertial fusion)." / "US 2024/0191996 (multi-IMU robotics fusion)." / "US 2022/0080979 (egomotion)." -- bare patent number + one-word descriptor, missing title/assignee/dates/inventors (the 6-field x-articles-format-en.md spec), flagged as a disclosed, non-blocking pass-6 gap in every editorial round of this run (see rounds 1-4 above).
after: all five entries expanded to the full 6-field format matching the hero/secondary patent entries -- title, assignee, filed date, published date, and all inventors -- e.g. "US 2021/0268903 A1, \"Speed Measurement Using Time-of-Flight Sensing and Anti-Collision Protection Using Time-of-Flight Sensing,\" STMicroelectronics (Grenoble 2) SAS, filed 2021-02-15, published 2021-09-02, inventor: Thomas Perotto. (anti-collision)" -- same pattern for the other four. This is the first entries in this essay's Sources block to carry a verified publication date (the hero and secondary-patent entries still omit it -- genuinely unverified on their own extraction, not a template gap).
rationale: SETI supplied the actual USPTO Patent Application Publication PDFs for all five horizon-cluster patents (front-page bibliographic data was image-only, not text-extractable -- rendered to PNG via PyMuPDF and read visually). Every field was read directly from each patent's own front page, the strongest possible source. None of the five are granted (all A1 kind-code applications), so no grant/registration date applies. `fact-check-log.md`'s bundled `horizon-cluster-patents-2026` row was split into 5 individually-sourced rows with the same verified data, closing the fix at the design-artifact level too, not just in the composed prose.
quote: "US 2021/0268903 A1, \"Speed Measurement Using Time-of-Flight Sensing and Anti-Collision Protection Using Time-of-Flight Sensing,\" STMicroelectronics (Grenoble 2) SAS, filed 2021-02-15, published 2021-09-02, inventor: Thomas Perotto."

## Post-fix verification (final, after both self-audit rounds)

- `python3 .claude/skills/_shared/scripts/run_gates.py --draft handoff/02-compose/essay-draft.md --invention-summary handoff/01-design/invention-summary.md --figures handoff/01-design/figures-index.txt --figure-selection handoff/01-design/figure-selection.md --mode essay --json` -> `passed: true`, 0 fail findings across all 11 gates (re-run after all 5 applied deltas, both rounds).
- Every `[dddd]` anchor remaining in the draft (`[0004] [0018] [0019] [0026] [0035] [0036] [0043] [0045] [0046] [0050] [0051] [0054] [0082] [0083] [0086]`) confirmed present in `invention-summary.md`'s anchor set; `[0005]` no longer cited (its content is now correctly quoted as part of the claim-1 sentence, attributed by claim name, not by paragraph bracket).
- All essay-body paragraphs re-verified under the 96-word / 8-mobile-line Pass-5 threshold after every split, including the round-2 FIG. 3 split (max 95 words, 34 body paragraphs total).
- `draft_version` bumped 4 -> 5 (round 1) -> 6 (round 2); `publication.md` regenerated each time; `essay-final.md` re-promoted from the corrected `publication.md` each time.
- **Loop-until-dry status: converged, stopped after round 2 of the 3-round cap.** Round 2 found real issues (2 applied) but at a shrinking hit rate versus round 1 (3 applied), with the majority of round 2's candidate findings failing independent verification (jargon claim factually wrong on inspection) or failing the multi-vote bar (2 of 5 were split between the round's own two reviewers). A third round was judged disproportionate to the marginal remaining risk; the two genuinely open items (SLAM-stack word choice, claim-1/claim-21 proximity) are logged above as watch items for a future design-stage revisit rather than forced into a essay revision that keeps chasing a single adversarial persona's shifting bar.
