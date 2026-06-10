<!--
  handoff/03-edit/edit-log.md
  Produced by: editorial-review (Phase 3 Edit — 6-pass review), orchestrated run, round 2.
  Round type: regression review of draft_version 2 (verify round-1 fixes + check revised
  passages for new problems). Round-1 log (review_id ...-editorial-review-1) is preserved
  by the orchestrator's archive step.
  Schema: editorial-review/references/feedback-format.md (+ resolved: section for the
  revision round, per orchestrator instruction).
  Voice fence honored: judged against deliverable-voice-rules.md + anti-ai-writing.md only.
-->

# Edit Log

```yaml
review_id: 001-google-quantum-control-editorial-review-2
draft_source: handoff/02-compose/essay-draft.md
draft_version: 2
review_round: 2
review_timestamp: 2026-06-10T08:20:00Z
posture_applied: measured
overall_assessment: pass

# ------------------------------------------------------------------ resolved
# Round-1 findings (review_id 001-google-quantum-control-editorial-review-1),
# in round-1 document order, each re-verified against draft_version 2 AND
# publication.md (strip-pipeline output confirmed byte-identical body).

resolved:
  - id: r1-f1
    round1: "redundancy-compression, medium, §3 ¶2 (8 sentences / 165 words)"
    status: verified-fixed
    verification: |
      Split landed at exactly the recommended seam (after "...one of those four
      operations (claim 10)."). Measured: paragraph A 4 sentences / 81 words
      (~6.8 mobile lines), paragraph B 4 sentences / 84 words (~7.0 lines) —
      both inside the essay band (3-7 sentences) and under the 8-line mobile
      ceiling. Content verbatim as recommended: all three quoted spans in the
      two halves re-verified byte-exact against invention-summary.md
      (q-0022-2 via "The next sentence finishes the thought", q-0030-1,
      q-0022-4). The optional fuse of the final two sentences was not taken;
      the recommendation marked it optional, and the two short closing
      sentences ("...not a claim limit." / "...legal weight.") read as a
      deliberate couplet, consistent with the draft's section-end cadence.
      No orphaned transition: paragraph B opens "The example current menu is
      concrete" with the [0030] cite grounding "the example" immediately.

  - id: r1-f2
    round1: "claim-adequacy, low, §1 ¶1 s4 ('Google's newest quantum patent' superlative)"
    status: verified-fixed
    verification: |
      Now "A Google patent granted June 9, 2026, builds its controller around
      nine current levels instead [0022]" — the round-1 recommendation's
      second alternative, verbatim. Old text absent from essay-draft.md and
      publication.md (checked both apostrophe forms). Regression check: the
      industry-norm-reversal turn still lands in one sentence against the
      "racks ... visible default" setup; Google is still named in ¶1 (and the
      title); the grant date that the closing's "as of June 9" anchors to is
      preserved. Hook timing unchanged (evidence cite at s2, patent on the
      table at s4).

  - id: r1-f3
    round1: "claim-adequacy, low, §4 noise ¶, [0026] modality ('is configured')"
    status: verified-fixed
    verification: |
      Now: The device itself "can be configured for operation at temperatures
      of 3K or lower" [0026] — exactly the recommended form. The quoted span
      is a byte-verbatim substring of q-0026-1 ("...the circuit device 100 can
      be configured for operation at temperatures of 3K or lower."); confirmed
      in both draft and publication. The modal restores the source's
      modality; the sentence stays grammatical with the quote integrated
      (subject + quoted verb phrase). The remaining dropped hedge ("in some
      implementations") was already adjudicated in round 1 as routine spec
      boilerplate with the 3 K frame independently claim-anchored (claims 6,
      8, 27); not re-raised. Paragraph word count moves 134 -> 135, still the
      round-1 "marginal, not flagged" zone; sentence count 5, in band.

  - id: r1-f4
    round1: "claim-adequacy, low, §5 final ¶ ('the author of the 2019 ISSCC chip')"
    status: verified-fixed
    verification: |
      Now "Joseph Bardin, lead author of the 2019 ISSCC paper (UMass Amherst
      release), is one of this patent's two inventors." — the round-1
      recommendation's first alternative. "lead author" is consistent with
      the Sources author form "Bardin, et al." (Bardin first-listed,
      arXiv 1902.10864) and with fact google-cryo-xy-controller-2019;
      "chip" -> "paper" also removes the author-of-a-hardware-object category
      slip. The closing couplet's "The 2019 chip proved a controller could
      live at 3 kelvin" correctly still refers to the chip itself, not
      authorship. Old text absent from both files.

  - id: r1-f5
    round1: "reader-perspective, low, §4 FIG. 8 ¶ (167w) + §5 ¶2 (156w) mobile walls"
    status: verified-fixed
    verification: |
      Both optional splits taken at the recommended seams, no padding added.
      §4: walk paragraph 5 sentences / 111 words, then the FIG. 8 caption,
      then the quantitative-payoff paragraph 2 sentences / 56 words. §5:
      plane paragraph 4 sentences / 105 words + hedges paragraph 3 sentences /
      51 words ("Two hedges belong on the record." now stands as its own
      beat, as the recommendation intended). Caption relocation (FIG. 8
      caption moved up to sit directly after the walk paragraph, per
      figures-rationale.md revision note): verified non-regressive — it now
      matches the walk-paragraph -> caption pattern of FIG. 3A and makes the
      placement label body-section-4-after-[0074] literally exact; the short
      identifier caption does not break "The numbers the patent attaches..."
      reading through it, since both paragraphs stay on the fast-half subject.
      "On that plane, the differentiator is subtraction." still resolves
      across the new hedges paragraph because that paragraph keeps the plane
      vocabulary live ("flux-type bias controls", "XY-versus-flux layering").
      Residual lengths (105-111 words, ~9 lines at 12 wpl) remain
      quote-integrated structures and sit below round 1's own no-flag
      calibration (the 134-word noise paragraph was judged marginal and not
      flagged); re-flagging them would be churn, not rigor.

  - id: r1-f6
    round1: "lead-conclusion-strength, low, # Sources Papers entry (descriptive title readable as verbatim title)"
    status: verified-fixed
    verification: |
      The recommendation's sanctioned fallback was applied: the entry now
      reads "Bardin, et al. (2019). Cryogenic 28-nm bulk-CMOS qubit
      controller for transmon qubits (descriptive title; ISSCC 2019 / JSSC,
      Nov. 2019). https://arxiv.org/abs/1902.10864". The literal
      "descriptive title" marker makes it unmistakably descriptive; no exact
      title was invented (re-fetch is out of scope in revision mode — the
      correct boundary; a verbatim-title upgrade remains available to a
      future run via Phase 1). Clumsiness check, as instructed: the
      parenthetical is denser than the round-1 example but unambiguous and
      self-documenting, which is the right trade in a sources block; the
      internal semicolon is a parenthetical separator, not a clause join, the
      same already-accepted pattern as §5's "(arXiv 1902.10864; UMass
      Amherst release)". Author form, enum category, subgrouping, and the
      6-field patent entry are unchanged from round 1's clean verdict. Not a
      finding.

# ------------------------------------------------------------------ findings
# New findings on draft_version 2: none. One explicit no-findings entry per
# pass proves each pass ran (empty-pass handling per feedback-format.md).

findings:
  # ---------------------------------------------------------------- pass 1
  - pass: voice-canon-compliance
    finding: "no findings"
    scoped_to: |
      Regression scope: all six revised passages (§1 ¶1, §3 split pair, §4
      noise ¶ [0026] sentence, §4 walk/numbers split + caption position, §5
      split pair + Bardin sentence, Sources Papers entry) re-checked against
      anti-ai-writing.md Tier 1 + Tier 2 and deliverable-voice-rules.md. The
      revision introduced no new vocabulary beyond "lead", "can be",
      "descriptive title", "A Google patent granted" — zero banned-list or
      co-occurrence-cluster hits (mechanical re-grep: clean; gate_banned
      PASS). Formatting recount on v2: exactly 1 bold span (§3 thesis
      anchor), 1 emoji (closing 🤔, allowed placement), 2 semicolons both
      inside parenthetical source lists, em-dash count 0, no new fragments
      or transition-fingerprint openers (Furthermore/Moreover/sentence-
      initial Additionally: zero). §2 and §6 byte-identical per the
      composer's revision note (no finding touched them; spot-grep for all
      six fix strings confirms no spillover) — round-1 no-findings verdict
      carries.

  # ---------------------------------------------------------------- pass 2
  - pass: redundancy-compression
    finding: "no findings"
    scoped_to: |
      The round-1 medium (§3 ¶2) is resolved (see resolved r1-f1). The three
      paragraph splits duplicate no claims: each half carries a distinct idea
      (§3: few-levels-suffice vs worked-current-menu; §4: switch-unit walk vs
      quantitative payoffs; §5: plane distinction vs hedges). No new
      repetition introduced; the nine-levels value still appears in prose
      once in §3 (title and §1 set-up uses unchanged since round 1, judged
      acceptable lead->thesis recap there). Sentence-tightening sweep of the
      revised sentences: nothing >=25% cuttable. All v2 paragraphs now in the
      3-7 sentence band; longest is the unchanged-but-for-one-word noise
      paragraph (135 words), inside round-1 calibration.

  # ---------------------------------------------------------------- pass 3
  - pass: claim-adequacy
    finding: "no findings"
    scoped_to: |
      All three round-1 claim-adequacy findings verified fixed (resolved
      r1-f2/f3/f4). New-problem check on the revised sentences: "A Google
      patent granted June 9, 2026" is fully supported by tier-1 patent
      metadata (grant date 2026-06-09); "lead author" is supported by the
      "Bardin, et al." authorship order in the fact log's tier-2 entry; the
      restored [0026] modal brings the prose strictly closer to source. No
      new external claims, no new numbers, no new anchors introduced by the
      revision (anchor set identical to round 1; gate_anchors PASS). Tier-4
      hedge ("one industry survey") untouched in byte-identical §2.

  # ---------------------------------------------------------------- pass 4
  - pass: paraphrase-mutation-judgment
    finding: "no findings"
    scoped_to: |
      The three quoted spans inside revised passages re-verified byte-exact
      against invention-summary.md: q-0026-1 substring ("can be configured
      for operation at temperatures of 3K or lower"), q-0030-1 substring
      ("a 20 μA pulse..."), q-0022-4 substring ("eight different
      well-defined current levels plus a zero-bias level, for nine total
      levels"). The round-1 modality nick is now closed in the
      strengthening-to-accurate direction; no quote was reworded, split, or
      re-punctuated by the revision (splits fall on paragraph boundaries,
      not inside quoted spans). Logical alignment unchanged: section->spine
      mapping intact (thesis-trace coverage table re-checked), no new causal
      claims, the §5 negative claim and dB-trap handling untouched. The 27
      remaining spans live in passages byte-identical to round 1 — round-1
      30/30 verbatim verdict carries.

  # ---------------------------------------------------------------- pass 5
  - pass: reader-perspective
    finding: "no findings"
    scoped_to: |
      Both round-1 mobile walls resolved at the recommended seams (resolved
      r1-f5). Post-split engagement spot-check: §3's "How small?" pivot now
      opens into a tighter two-beat sequence; §4's caption-as-breather now
      sits between walk and payoff, improving the density signposting; §5's
      hedge beat reads as a deliberate pause before "On that plane, the
      differentiator is subtraction." Transitions across all three new
      paragraph boundaries resolve their referents within one sentence
      ("The example current menu...", "The numbers the patent attaches...",
      "Two hedges belong on the record."). Stake refresh at section closes
      unchanged. Worst remaining paragraph is the noise paragraph at ~11
      lines, quote-integrated, judged marginal-not-flagged in round 1 and
      only +1 word since.

  # ---------------------------------------------------------------- pass 6
  - pass: lead-conclusion-strength
    finding: "no findings"
    scoped_to: |
      Lead/close frame intact after the §1 edit: ¶1 still sets norm ->
      authority -> one-sentence reversal with the patent named and cited by
      s4; the objection is posed in ¶2 ("Hold that objection.") and the
      closing still explicitly returns to it ("Which returns to the opening
      objection...") landing open-question + aphorism, matching the spine's
      residual_risk "Acknowledged"; "as of June 9" still anchors to the
      grant date retained in §1. Mechanical re-verification on v2: em-dash 0
      (title and body), # Sources exactly once, 5 enum categories,
      all-or-nothing subgrouping over 7 entries, patent entry 6 fields,
      author form unchanged, all inline cites 4-digit, blockquote
      attribution lines unchanged, footnotes present in draft and stripped
      from publication.md (publication body byte-identical to draft body
      sans frontmatter/footnotes). Deterministic gates re-confirmed this
      round: emdash/anchors/sources/banned/structure PASS with zero
      findings (figure gates PASS per orchestrator context; all five
      selected units still referenced, FIG. 8 caption move stays inside §4
      per figures-rationale.md). Sources Papers entry: resolved r1-f6, no
      residual finding.
```

<!--
  Reviewer notes (non-schema, for the orchestrator / retro):

  Round-2 scope discipline: §2 and §6 are byte-identical to round 1 (composer revision
  note; corroborated by absence of any fix-string spillover and unchanged word counts) —
  round-1 verdicts carry for them. Deep passes re-run only on the six changed passages
  plus a whole-draft coherence spot-check (frame closure, the three new paragraph
  boundaries, caption adjacency) and a whole-draft mechanical re-grep.

  Fix-quality observations worth one retro line: (1) the composer applied all six
  findings exactly at the recommended seams with zero content churn — revision-mode
  convergence behavior is working as designed; (2) the FIG. 8 caption relocation was a
  fix-induced improvement (figure-caption adjacency now uniform across all body
  figures); (3) the verbatim ISSCC paper title remains unavailable in the Phase-1 fact
  base — if this patent family recurs, Phase 1 should re-capture the exact title so the
  Papers entry can graduate from descriptive to quoted (candidate for the findings
  ledger, owner: thesis-architect/fact-check-log, not a draft defect).

  Timestamp note: round-1 log carried review_timestamp 2026-06-10T09:30:00Z, which is
  ahead of this round's wall clock (08:20Z) — the round-1 stamp was evidently nominal.
  This round's stamp is actual wall clock; archive ordering should key on review_round.

  Assessment arithmetic: 0 critical, 0 high, 0 medium, 0 low -> pass. Per the severity
  table this ends the inner loop; the orchestrator may promote draft_version 2 to
  handoff/03-edit/essay-final.md.
-->
