# Editorial Review — Edit Log (Revision Round 2)

Phase 3 Edit (editorial-review), voice-fenced. Second-pass six-pass review of the REVISED
`handoff/02-compose/essay-draft.md` (draft_version 2) against the Phase-1 design hand-off.
Structured findings only — not an auto-fix. See `feedback-format.md` for the schema + severity
model. Round-1 found 1 medium (placeholder Sources URLs) + 1 low (dense §4 paragraph); both
were addressed in this draft and are re-verified below.

```yaml
review_id: sandisk-hbf-moat-review-2
draft_source: handoff/02-compose/essay-draft.md
review_timestamp: 2026-06-20T00:00:00Z
posture_applied: measured
overall_assessment: pass

findings:
  - pass: voice-canon-compliance
    finding: "no findings"
    scoped_to: |
      Anti-AI banned-word + rhetorical-pattern + formatting scan across body and captions
      (deliverable-voice-rules.md + anti-ai-writing.md only; voice-profile + caption-roles NOT
      loaded per the Phase-3 fence). Re-run on draft_version 2. Zero Tier-1 banned words
      (gate_banned independently PASS, zero hits). No copula-avoidance in author prose — the one
      "constitutes" sits inside the verbatim [0153] patent quote and is exempt. No
      not-just-X-but-Y negative parallelism (the §1 "is not whether ... clever. The question is
      whether ... or ..." is a genuine either/or, not the banned form). No sentence-initial
      Additionally/Furthermore/Moreover, no puffery, no vague attributions, no elegant variation
      (SanDisk / the application / the filing used consistently), no AI-vocabulary clustering, no
      bold overuse (one sanctioned inline-bold thesis anchor per section). The two paragraphs
      edited since round 1 (the §4 split) introduced no new banned vocabulary or patterns.
      Em-dash count zero (also re-checked Pass 6).

  - pass: redundancy-compression
    finding: "no findings"
    scoped_to: |
      Claim-repetition (2A), sentence-tightening (2B), paragraph word-count earn (2C) across all
      five sections on draft_version 2. "real but conditional" appears at §3-close (inline-bold
      anchor) and §5 (recap) — the sanctioned thesis -> closing circle-back, not redundancy.
      "moat" / "packaging grammar" / "second front" recur as the deliberate single-spine thread,
      each instance carrying new content; no claim restated in 3+ locations without a new
      evidence layer. The §4 split did NOT duplicate content — the status qualifier (new §4 P2,
      31 words) and the design-arounds (§4 P3) were separated, not restated, so 2A is still
      clean. No sentence is >=25% cuttable without information loss. No paragraph reaches the
      8-sentence high-severity line (longest is 5 sentences).

  - pass: claim-adequacy
    finding: "no findings"
    scoped_to: |
      Verbatim verification (3A) re-run from scratch on draft_version 2: ALL 14 quoted [dddd]
      spans string-match their cited paragraph anchor in input/patent.md after bold-strip / NBSP
      / smart-quote normalization — [0153], [0115], [0188] (x2), [0174] (x2), [0055], [0056]
      (x2), [0171], [0176], [0004], [0002], [0159] (programmatically confirmed: 14/14 exact
      substrings, 0 misses). Zero paraphrase mutation, zero fact-introduction beyond the
      invention-summary Quotable spans, zero anchor drift; reference-number markers
      (1000/700/720/2000/3000/900) round-trip cleanly.

      External sourcing (3B) — the round-1 MEDIUM is RESOLVED. Both example.org/PLACEHOLDER URLs
      are gone (0 occurrences in the draft). The # Sources block now carries three real,
      well-formed, first-party/trade sources, all inside the 5-label enum: Official statements =
      SanDisk newsroom press release (HBF standardization with SK hynix, 2026-02-25, a tier-1
      primary company statement); News & media = Tom's Hardware (HBF as a NAND-based HBM
      alternative) and Semiconductor Engineering (hybrid-bonding manufacturability) — tier-2/3
      trade press. The dropped ## Papers category was removed cleanly and the §3 inline tag was
      realigned from "(Papers)" to "(News & media)" (3 consistent uses); no dangling category.
      fact-check-log.md marks all three verified-live (web search 2026-06) and documents that a
      direct automated WebFetch returns HTTP 403 (publisher bot-protection) for all three — a
      403, not a 404: these are live, human-reachable publisher pages on real domains
      (sandisk.com, tomshardware.com, semiengineering.com), not dead links and not placeholders.
      That is a normal access caveat for these major sites, not a publication-readiness defect,
      so it does not warrant a finding. The HBM/HBF "second front" framing is now real,
      attributed industry context; the spine remains patent-anchored and does not depend on it.

      Goal-2 coverage sub-check PASSES: all four core-mechanism layers (What / How / Why-novel /
      innovation-angles) and all six Layer-2 mechanism steps are addressed in the prose, and all
      four selected figures (header 36A + body 20, 21, 33) are referenced with substantive,
      info-bearing captions — no uncovered layer, no orphan figure (gate_figure_use PASS).

  - pass: paraphrase-mutation-judgment
    finding: "no findings"
    scoped_to: |
      Every double-quoted span in draft_version 2 was compared byte-for-byte (after the allowed
      bold-marker strip / NBSP / smart-quote normalization) against its cited paragraph in
      input/patent.md. All 14 patent quotes are exact substrings of the cited paragraph; nothing
      to classify as intentional restatement, accidental drift, or substantive change. (The four
      non-patent double-quoted strings are Sources titles — the patent title and three article
      titles — correctly NOT drawn from the patent body.) Guardrails honored: no invented
      quantity (no stack count, bandwidth number, or pitch), rights framed as sought not held,
      structure claim 1 vs method claim 15 kept distinct, illustrated assembly counts not
      generalized into a claimed quantity.

  - pass: reader-perspective
    location: "§3 paragraph 1 (line 36) and §4 paragraph 3 (line 48)"
    severity: low
    severity_under_default_posture: low
    finding: |
      Engagement curve, stake clarity, and arc remain sound for the investor/analyst reader:
      the hook lands in §1's first three sentences, every section delivers a new evidence layer
      (no Pass-5A density wall — the dense paragraphs are isolated, not 3+ consecutive
      mechanism blocks), and the closing resolves the lead's "real second front, or obvious
      analogy?" tension into a binary prosecution test that reads in isolation. The round-1 LOW
      (the ~166-word §4 block) is RESOLVED: §4 is now three paragraphs (113 / 31 / 135 words),
      and the status qualifier reads as its own short beat. The only residual edge is mobile
      line-count: two single-idea body paragraphs still run ~11 iPhone-class lines — §3 P1 (131
      words, the bonding-optionality menu) and §4 P3 (135 words, the two design-arounds), both
      just over the ~8-line heuristic. Both are clean (no redundancy), 4-5 sentences, and the
      reader is high-literacy and paying attention, so this is scannability polish, not a
      comprehension break.
    recommendation: |
      Optional. If tightening mobile scannability further, §4 P3 could split after the
      monolithic design-around (before "The other is the inverse ...") so each design-around is
      its own beat; §3 P1 could break after the first "[0056]" quote. Low — does not affect the
      assessment, and further splitting trades against paragraph-cohesion, so it is a judgment
      call for the author.

  - pass: lead-conclusion-strength
    finding: "no findings"
    scoped_to: |
      Lead anchor (6A): §1 opens on the corporate-narrative-friction hook (HBM is the
      stacked-memory moat for DRAM), puts the patent on the table by sentence ~3 with [0153], and
      states the bolded thesis at §1's end — passes the "what's the essay about?" lead test.
      Frame closure (6B): spine residual_risk is Acknowledged WITH an explicit Acceptance-form
      binary falsifier; the closing lands a binary/forward-watching test ("how claim 1 issues:
      substantially as filed ... or narrowed ... Whether SanDisk gets to keep it is a question
      the patent office ... will answer"), matching the spine. Mechanical (6C-6F), re-verified on
      draft_version 2: # Sources is a single h1; all three categories (Patents, Official
      statements, News & media) are inside the 5-label enum; all-or-nothing ## subgrouping is
      satisfied (every entry categorized) and the realignment introduced no out-of-enum category;
      title uses a comma, no em-dash (6F); em-dash count zero, every inline cite is 4-digit
      [dddd] (6E); footnotes are figure-asset notes, not stripped-pipeline leakage. Deterministic
      gates independently re-run on this draft: all six PASS (emdash / anchors / sources / banned
      / structure / figure_use), zero hard findings.
```

## Severity rollup

- critical: 0
- high: 0
- medium: 0
- low: 1 (Pass 5 / reader-perspective — two ~11-line mobile paragraphs, §3 P1 and §4 P3)

Per the feedback-format rule (no critical, no high, no medium), `overall_assessment` =
**pass**. The round-1 medium (placeholder Sources URLs) is closed: the Sources block now carries
three real, well-formed, enum-valid sources with the §3 inline tag realigned and the empty Papers
category dropped. The round-1 low (dense §4 paragraph) is closed by the §4 split. The remaining
single low is optional mobile-scannability polish on two clean single-idea paragraphs and does
not affect the assessment. Verbatim citations (14/14), goal-2 coverage, voice/anti-AI, logic, and
all mechanical/format checks are clean. This draft clears the orchestrator's `pass` threshold.
