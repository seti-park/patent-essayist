# Revision notes — 001-st-histogram-mechanism

> Post-acceptance self-audit channel. Two fresh-context adversarial reviewers (no exposure to
> `thesis-spine.md`, `invention-summary.md`, or `edit-log.md` — blind to the design/compose
> process) ran the `pass-7-adversarial-reader` checklist plus grounding spot-checks against
> `handoff/03-edit/essay-final.md` + `input/patent.md`. Round 1 is **dry**: no finding cleared
> the multi-vote bar (reviewer agreement, or a single reviewer's grounding finding independently
> verified against source), so no essay edit was made and the self-audit loop stops here.
> Logged per `origin: self-post-accept` conventions even though nothing was applied, because the
> disagreement itself is useful signal for `pipeline-retro`.

## Round 1 — considered, not applied

### 1. Lead BLUF altitude (pass-7 check 1)
- Reviewer 1 (impatient-investor lens): FAIL, medium — payoff doesn't land until paragraph 2.
- Reviewer 2 (skeptical-pro-subject lens): PASS — declarative verdict lands in paragraph 1.
- Split 1-1, no majority. Matches editorial-review round 3's own conclusion on the same
  question ("PASS with a caveat... kept low severity"). **Not applied** — taste-level, already
  reviewed twice before with the same "acceptable, could be tighter" conclusion.

### 2. Steelman present (pass-7 check 3)
- Reviewer 1: FAIL, medium — wants a steelman of the *engineering* thesis (e.g. "is bin-serial
  streaming actually novel, or a known technique applied to new hardware?"), separate from the
  product-identity steelman the essay already carries.
- Reviewer 2: PASS — finds the product-identity steelman ("STMicroelectronics does not publish
  which patent maps to which line of silicon...") satisfies the check as the single strongest
  objection.
- Split 1-1, no majority. Orchestrator's own review: the product-identity steelman is the
  objectively strongest objection to *this* essay's combined engineering + product-relevance
  argument (verified independently across all 3 editorial-review rounds as landing correctly);
  an engineering-novelty steelman is a legitimate alternative angle but not clearly stronger.
  **Not applied.**

### 3. Claim-scope grounding check — HIGH severity claim, refuted on independent verification
- Reviewer 1 (grounding spot-check 2): FAIL, **high** — argued the essay's line "Claim 1 of the
  patent describes a circuit that never holds that full copy" is contradicted by dependent
  claim 8, "wherein the histogram processing circuit is configured to perform full histogram
  processing capabilities while maintaining low power consumption targets."
- Reviewer 2 (grounding spot-check 10, same territory): PASS — found the essay's Claim 1
  characterization accurate and not broader than the claim language, and noted the
  memory-never-held mechanism is separately sourced to `[0069]`/`[0080]` (spec), not asserted
  as a property of Claim 1's bare language.
- **Orchestrator's own independent verification** (not just deferring to either reviewer):
  grepped every occurrence of "full histogram processing capabilities" in `input/patent.md`
  (`[0036]`, `[0039]`, `[0044]`, `[0235]`, `[0245]`, claim 8, claim 17-adjacent). `[0044]` is
  dispositive: "By implementing these memory-efficient techniques, the system achieves full
  histogram processing capabilities comparable to more resource-intensive solutions while
  maintaining ultra-low power consumption" — the patent's own usage ties "full histogram
  processing capabilities" (comprehensive functional coverage of the histogram, as opposed to a
  bypass/off-chip mode or a narrower sliding-window mode per claim 7) to being *achieved through*
  the memory-lean bin-serial technique, not in tension with it. Claim 7 (sliding window) and
  claim 8 (full histogram processing capabilities) read as a scope-of-coverage pair (windowed
  subset vs. full range), not a memory-storage-model pair (streamed vs. buffered). Reviewer 1's
  reading conflates two distinct senses of "full" in the patent's own vocabulary.
- Per the self-audit's multi-vote rule ("apply when reviewers agree, OR when one reviewer's
  grounding finding is independently verifiable against source"): reviewers disagree (no
  majority), and the orchestrator's own source check refutes rather than confirms the finding.
  **Not applied** — the essay's claim-scope characterization stands as accurate.
- Logged anyway because a high-severity grounding claim that does not survive independent
  verification is itself useful calibration signal for the self-audit process — see the
  `pipeline-retro` note this run surfaces on adversarial-reviewer precision.

### 4. Thesis-restatement frequency (pass-7 check 7)
- Reviewer 1: PASS (clean). Reviewer 2: "borderline PASS, low" — counts 4 assertions of the
  core "bin-by-bin, never fully in memory" verdict, at or slightly past the <=3 guideline, but
  each adds new evidence (quote, mechanism, payoff) rather than repeating the same sentence.
  Matches editorial-review round 1's pass-2 finding on the same "full histogram" motif
  ("flagged for awareness only, not as a defect... do not cut any of these occurrences").
  **Not applied** — already deliberately preserved through 3 editorial-review rounds as the
  essay's throughline, not filler.

### 5. VL53L9CX-header framing (reviewer 1 grounding spot-check 3, low)
- Single reviewer, low severity: the closing section's header ("ST Will Not Say Which Patent
  Built the VL53L9CX, but the Dates Line Up") primes a slightly more confident read than the
  prose that follows ultimately supports, before the text downgrades to the hedged
  engineering-necessity claim.
- Not corroborated by reviewer 2 (who scored the same header a clean PASS on header-as-claim
  and explicitly praised the hedge as well-executed). Single-reviewer, low-severity, taste-level.
  **Not applied.**

## Outcome

0 applied edits. Self-audit round 1 is dry (no finding cleared the agreement-or-verified bar) —
per the loop-until-dry policy, the self-audit stops here rather than spawning a second round.
`essay-final.md` is unchanged from the version accepted by editorial-review round 3.
