# Revision notes — stm-tof-us2026-0140238

> Post-acceptance **self-audit** delta channel. After the Compose↔Edit inner loop returned
> `pass` with all gates green, two fresh-context adversarial reviewers (impatient general reader
> + skeptical engineer, separate forked contexts) read `essay-final.md` against the raw patents.
> Applied findings are logged below as `## delta` blocks and normalized to
> `meta/findings-ledger.jsonl` with `origin: self-post-accept` (via
> `meta/normalize_revision_notes.py --origin self-post-accept`). Both applied findings are
> grounding corrections verifiable against source, so they were applied even though only one
> reviewer raised each (the rule applies a finding on majority agreement OR a verifiable
> grounding catch). Taste / split / over-edit findings are logged as considered-not-applied and
> were not forced in (the rubric gates OVERREACH, not OVER-HEDGE).

## delta
class: claim-scope-misattribution
round: self-audit-1
before: hero block quote attributed "US 2026/0140238 A1, Abstract and claim 1" with lead-in "Its first claim describes a sensor whose processing circuit, in the patent's own words"
after: attributed to "Abstract" only; lead-in now "The patent puts the whole idea on one line of its abstract"; a following sentence routes claim 1 to its own verbatim fragments ("using a sequential bin-by-bin histogram processing" / "one or more on-the-fly operations" [0015])
rationale: the exact quoted string occurs only in the Abstract; claim 1 reads "process measurement data from the detector array using a sequential bin-by-bin histogram processing" (different verb form and scope), so "and claim 1" mislabeled an abstract-only quote as claim wording.

## delta
class: anchor-incomplete
round: self-audit-1
before: "It can ride on the sensor's own small circuitry [0042], which is what lets a complete sensor shrink to roughly the size of a fingernail."
after: "With local storage cut to a handful of registers, it can ride on the sensor's own small circuitry [0043], which is part of what lets a complete sensor shrink to roughly the size of a fingernail."
rationale: [0042] grounds only memory reduction / streaming; the on-chip conclusion lives in [0043] ("limited local storage in the form of registers ... reducing power consumption and chip area"). Re-anchored the on-chip clause to [0043] (on the allow-list) and hedged the causal link to "part of what lets".

## considered, not applied (taste / single-reviewer / over-edit — logged, not forced)

- Reviewer-A: "the patent refuses to do it" reads as mild anthropomorphism. Held: deliberate, accurate voice idiom; not a grounding issue; single reviewer, taste.
- Reviewer-A: two back-to-back verbatim quotes ([0042]+[0069]) in one §3 sentence read as proof-piling. Held: both are load-bearing grounding for the streaming claim, the heart of the piece; the paragraph was already split for rhythm; Reviewer-B passed quote density and claim-scope.
- Reviewer-A: "twenty billionths of a second ... the round trip doubles that" momentary arithmetic friction. Held: Reviewer-B verified the physics is correct (3 m round trip ~20 ns); A confirmed it reconciles. Reviewers split, taste only.
- Reviewer-B: [0016] sits on a sentence whose lead clause is "to spot a true peak"; the anchor itself supports the running-state clause it is adjacent to. Held: Reviewer-B rated it "acceptable as-is"; the anchor backs the load-bearing clause.
- Reviewer-B: "reads distance straight off it [0003]" leans on the adjacent distance paragraphs. Held: Reviewer-B said "none required"; [0003] supports the actual-travel-time claim, distance derivation is one paragraph away.
- Reviewer-B: "Those five filings are listed in the sources below" sits above a seven-entry Patents list (hero + support + five cluster). Held: prose is precise ("five" = the five cluster filings); Reviewer-B confirmed not a defect, cosmetic only.
