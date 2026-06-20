```yaml
review_id: sandisk-hbf-read-editorial-review-1
draft_source: handoff/02-compose/essay-draft.md
review_timestamp: 2026-06-20T00:00:00Z
posture_applied: measured
overall_assessment: pass

findings:
  - pass: voice-canon-compliance
    finding: "no findings"
    scoped_to: |
      Em-dash count 0 and banned-term count 0 (confirmed by gate_emdash / gate_banned).
      Opening matches opening-industry-norm-reversal (HBM stated as the decades-default,
      then a one-move reversal: two filings say NAND can do it by not ramping down). One
      inline bold thesis anchor in the lead. Closing matches closing-aphoristic-landing
      ("The pitch is a new kind of memory. But the patents are about refusing to let the old
      kind rest." = the X-is-Y / But-Z-is-W syntax). No transition fingerprint (no sentence-
      initial Furthermore/Moreover/Additionally), no copula avoidance, no puffery. The two
      STRUCT-004 triads are a factual inventor list ("Yang, Cao, and Dutta") and a verbatim
      citation title ("SK hynix, Samsung, and SanDisk") — neither is a reflexive stylistic
      triad; cleared.

  - pass: redundancy-compression
    location: lead + §"So is there a moat?"
    severity: low
    severity_under_default_posture: low
    finding: |
      The HBM-supply point is foreshadowed in the lead ("the most supply-constrained part of
      the entire AI stack") and landed again in §5 ("HBM has been effectively sold out through
      2026"). Mild cross-section echo; reads as deliberate setup-and-payoff rather than waste.
    recommendation: |
      Optional. Leave as-is, or trim the lead clause to a bare "supply-constrained" and let §5
      carry the detail. Does not affect assessment.

  - pass: claim-adequacy
    finding: "no findings"
    scoped_to: |
      Every [dddd] inline quote string-matched to an invention-summary Quotable span /
      Quote-anchor verbatim: [0005] q-0005-1; [0006] q-0006-1; [0147] q-0147-2 + "eliminated"
      (subset of q-0147-1); [0148] "less than 1 microseconds" + "always on" (q-0148-1); [0146];
      [0047] (subset of q-0047-1) + "non-discharging read"; [0007] q-0007-1; [0179] (subset of
      q-0179-1); [0019] q-0019-1; [0181] (subset of q-0181-1). [0004] and [0011] are anchored
      paraphrase, no quote. Coverage sub-check (goal 2): all four core-mechanism layers are
      addressed (column hold, no-ramp, row hold, adaptive trigger) and all six selected figures
      are used. External claims (spin-off, HBF program, 8-16x capacity, advisory board, SK hynix
      MOU, roadmap, HBM sell-out) each trace to fact-check-log F1-F7 and appear in # Sources;
      each is fenced ("this next part is not inside the filings") and the 8-16x figure is
      attributed as SanDisk's own claim. No paraphrase mutation.

  - pass: paraphrase-mutation-judgment
    finding: "no findings"
    scoped_to: |
      Spot-checked the highest-risk paraphrases: "at least four such devices around a processor"
      vs [0011] "at least four memory devices that are of similar construction" — faithful, not
      quoted. "skip the discharge, shorten the gap between reads" is an intentional restatement
      of the [0047]/[0179] causal chain, not a verbatim claim. No accidental drift detected.

  - pass: reader-perspective
    location: lead, §"the two voltages", §"row trick", §"So is there a moat?"
    severity: low
    severity_under_default_posture: low
    finding: |
      Eight body paragraphs ran over the ~110-word mobile ceiling (worst: the NAND-string
      primer at 155w, the spin-off/HBF paragraph at 127w). This is the ledger's recurring
      gate-invisible mobile-paragraph-wall class: gate_structure STRUCT-001 counts sentences,
      not words, so these passed the warn gate. Content sequencing and comprehension were
      intact; the issue was purely mobile rendering. [resolved: split at clean sentence seams,
      no wording change; max body paragraph now 111w, gates re-confirmed PASS.]
    recommendation: |
      Applied. Splits are pure paragraph breaks, so anchors/quotes/figure refs are unchanged.
      Reinforces the open mobile-paragraph-wall proposal (now 3/3 essays).

  - pass: lead-conclusion-strength
    finding: "no findings"
    scoped_to: |
      Lead sets the technical-impossibility thesis (NAND too slow/hot for HBM, per [0005]) and
      commits the bold anchor (the fix is an omission). Conclusion closes the frame: lead's
      "refusal to put the array back to sleep" returns as "refusing to let the old kind rest,"
      and the closing re-commits the moat throughline. Forward pointer is concrete (claim
      breadth at grant, more team filings, whether HBF ships in an accelerator in 2026-2027).
      Format: title 12 words, no em-dash; # Sources present once, 5-label enum, subgrouped
      all-or-nothing, no descriptive annotations on entries.
```
