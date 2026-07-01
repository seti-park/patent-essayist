```yaml
review_id: 001-st-histogram-mechanism-editorial-review-1
draft_source: handoff/02-compose/essay-draft.md
review_timestamp: 2026-07-01T07:16:01Z
posture_applied: measured
overall_assessment: revise-recommended

findings:
  # ---------------------------------------------------------------------
  # Pass 1 — Voice canon + anti-AI compliance
  # ---------------------------------------------------------------------
  - pass: pass-1-voice-anti-ai
    location: "§1 (H1 title) vs. §1-hook (first `##` header)"
    severity: medium
    severity_under_default_posture: medium
    finding: |
      The document's `#` H1 title ("A Depth Sensor That Cannot Time a Single Photon
      With a Stopwatch") and the immediately following `##` section header ("A Depth
      Camera Cannot Time a Photon With a Stopwatch") are near-verbatim restatements of
      each other — same "[subject] Cannot Time a [X] With a Stopwatch" sentence frame,
      differing only in "Depth Sensor"/"a Single Photon" vs. "Depth Camera"/"a Photon".
      This reads as a lazy echo rather than an escalation from title-hook to lead-hook,
      and risks looking like elegant-variation-in-reverse (same claim, minimally
      reworded, stacked back to back).
    recommendation: |
      Differentiate the two lines. Either let the H1 stay the punchy declarative and
      make the first `##` header do different work (e.g. name the mechanism or the
      "how" rather than restate the "cannot" framing), or fold the sentiment into one
      and let the second header advance the argument (header-as-claim per pass-7 check 2).
    quote: "A Depth Sensor That Cannot Time a Single Photon With a Stopwatch ... A Depth Camera Cannot Time a Photon With a Stopwatch"

  - pass: pass-1-voice-anti-ai
    finding: "no findings beyond the H1/H2 echo above"
    scoped_to: "Banned-word grep (0 hits), banned-pattern grep (not-just-but, despite-challenges, copula avoidance, vague attributions, puffery, section-summary, elegant variation — none found), triple-empty-modifiers, bold overuse (2 load-bearing bold spans total, both single-paragraph thesis anchors, within budget), bullet overuse (none — no bullets in body prose), emoji (single sanctioned 🤔 at close only). Voice canon cadence/structure inheritance not independently re-judged per the Phase-3 voice fence (voice-profile.md not loaded)."

  # ---------------------------------------------------------------------
  # Pass 2 — Redundancy + compression
  # ---------------------------------------------------------------------
  - pass: pass-2-redundancy
    location: "§3 (¶ starting 'Building the histogram is one problem'), §4 (¶ starting 'Here is where the mechanism'), §4 (¶ starting 'The bin-serial approach instead')"
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Nine of the draft's ~22 body paragraphs run 100-160+ words (paragraphs at lines
      26, 32, 34, 38, 42, 44, 48, 52, 54 by direct word count: 132, 142, 105, 108, 106,
      105, 161, 115, 149 words respectively), several running 5-8 sentences against the
      3-7 sentence essay target. The gate's LONGSENT-001 warn-check independently flags
      18 individual sentences at 37-120 words (target ~15-25) across these same
      paragraphs, including one 120-word run-on (the closing paragraph's final sentence,
      artifact-adjacent to the sentence-splitter but reflecting a genuinely long
      unbroken clause chain). This is real accumulated density, not one outlier — it
      recurs through the "full histogram is never held in memory" throughline (background
      framing → claim-1 verbatim → mechanism verbatim → analogy → FIG. 2 walkthrough),
      each occurrence legitimately adding a new evidence layer (acceptable per 2A's
      "thread bridge" exception), but the sentence-level compression within each
      occurrence is not yet earning its length.
    recommendation: |
      Split the 100+ word paragraphs at their internal idea boundaries — most already
      contain 2 sub-ideas (e.g. the crosstalk-memory paragraph at line 48 fuses the
      quantitative footprint claim with the MCU-demotion claim; these can be two
      paragraphs). Within surviving paragraphs, tighten the longest sentences (the
      67-, 63-, and 120-word ones) by cutting subordinate clauses that restate rather
      than add — this is the compression lever pass-5 also needs for mobile line count.

  - pass: pass-2-redundancy
    location: "§2-§4 (stopwatch / 'full histogram' motif)"
    severity: low
    severity_under_default_posture: low
    finding: |
      The "you cannot time a photon with a stopwatch" framing appears in the lead
      (line 20) and again in the closing (line 58) — this is the acceptable lead↔closing
      bookend pattern (2A), not redundancy. Separately, "full histogram [processing /
      copy / array]" as a contrast term recurs across five paragraphs (32, 34, 38, 42,
      44) but each occurrence adds a new evidence layer (background framing, claim
      verbatim, mechanism verbatim, analogy, structural walkthrough) rather than
      re-asserting the same claim without new support. Flagged for awareness only,
      not as a defect — do not cut any of these five occurrences; the fix belongs to
      Pass 2's sentence-tightening lever above, not to claim deduplication.
    recommendation: |
      No action required. If §3-4 gets restructured for the paragraph-length findings
      above, preserve all five "full histogram" callbacks — they are the mechanism's
      throughline, not filler.

  # ---------------------------------------------------------------------
  # Pass 3 — Claim adequacy + fact verification + paraphrase mutation
  # ---------------------------------------------------------------------
  - pass: pass-3-fact-paraphrase
    finding: |
      All patent-verbatim quotes checked byte-for-byte against `input/patent.md`:
      `[0001]` title, `[0043]`, `[0054]`, `[0055]`, `[0069]`, `[0080]` (both spans),
      `[0101]`, `[0103]`, the Claim-1/`[0015]`-first-aspect composite quote, and the
      Abstract "sequential bin-by-bin histogram processing" line — every one is an
      EXACT match to source text, no drift, no clipping that changes meaning. All
      `[dddd]` citation anchors resolve against `invention-summary.md`'s Quote anchor
      table (no orphan citations, no anchor-missing cases). The auxiliary patent
      (US 2023/0296739) carries exactly one verbatim quote — "each bin of the
      histogram representing a photon count corresponding to a distance from a
      light-ranging system" — matching essay-context.md's pre-cleared anchor exactly,
      with no other fact/quote attributed to it, satisfying the essay-context
      constraint. The five cluster patents (US 2021/0302550, 2020/0400792,
      2018/0253404, 2024/0353538, 2019/0109977) do not appear anywhere in the draft —
      correctly excluded rather than sprawled into a survey aside. The "first direct
      Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio" company quote
      is reproduced with the "in ST's portfolio" qualifier intact, satisfying the
      no-unqualified-"first" constraint; no other "first" claim appears unqualified.
      No iToF/dToF confusion (the distinction at line 24 is correct: dToF = direct
      round-trip timing via SPAD/TDC, iToF = phase-shift). No "directly measures the
      speed of light" framing anywhere. All numeric claims (2,268 zones, 54×42 grid,
      100 fps, 64-zone/8×8 baseline, ~35x, ~19 bytes vs ~256 bytes, ~13x) trace to
      fact-check-log.md tier-1 entries or patent-verbatim `[dddd]` anchors, and the
      35x figure is explicitly hedged as "not a precise figure ST states outright but
      a straightforward ratio" — matching fact-check-log's own hedge instruction.
    scoped_to: "Every [dddd]-cited and double-quoted span in the draft (10 patent-verbatim quotes, 1 company quote, all numeric claims) cross-checked against patent.md, invention-summary.md Quote anchor table, and fact-check-log.md."

  - pass: pass-3-fact-paraphrase
    location: "§2 (¶ starting 'Building the histogram is one problem'), spine element '2-problem' primary anchor `[0004]`"
    severity: low
    severity_under_default_posture: low
    finding: |
      thesis-spine.md's spine→section trace table lists `[0004]` as a primary anchor
      for the 2-problem section ("SPAD-based histogram generation"). The draft's
      corresponding paragraph (line 24: "A single-photon avalanche diode, or SPAD, is
      the component that makes the direct measurement possible... fire the laser many
      times, bucket every returning photon's arrival time into a bin, and build a
      histogram") accurately paraphrases `[0004]`'s content (SPADs detect individual
      photons; systems generate histograms of photon arrival times) but never carries
      an inline `[0004]` citation marker for that specific claim — the paragraph's only
      inline anchor is the auxiliary-patent quote later in the same paragraph. Content
      is accurate (paraphrase mutation classification: intentional restatement, not
      drift), so this is a citation-completeness gap, not a fact-verification failure.
    recommendation: |
      Add `[0004]` as an inline anchor on the SPAD/histogram-generation sentence, e.g.
      "...via a time-to-digital converter (TDC) attached to it `[0004]`." Low-cost fix,
      closes the spine-trace gap cleanly.

  # ---------------------------------------------------------------------
  # Pass 4 — Logical alignment + causality
  # ---------------------------------------------------------------------
  - pass: pass-4-logic-causality
    finding: |
      4A thesis-section alignment: all five spine elements (1-hook, 2-problem,
      3-core-claim, 4-analogy, 5-product-stakes) are carried by their mapped sections
      and each section's prose actually advances its element rather than merely
      mentioning it; no section introduces an out-of-spine claim. 4B causal claim
      quality: the draft's one load-bearing causal-adjacent claim is explicitly
      hedged to correlation/necessary-condition framing rather than asserted as direct
      causation. 4C thesis arc coherence: lead sets up the stopwatch-impossibility
      tension, mechanism section anchors it in patent evidence, analogy section shows
      the implication, closing lands with the lead-frame callback and the
      hedge-qualified engineering-claim-survives-the-product-claim landing.
    scoped_to: "All 5 sections cross-checked against thesis-spine.md's spine→section trace table and adversarial defense block."

  # ---------------------------------------------------------------------
  # Pass 5 — Reader perspective + paragraph readability
  # ---------------------------------------------------------------------
  - pass: pass-5-reader-perspective
    location: "§4 (¶ starting 'Here is where the mechanism becomes intuitive')"
    severity: medium
    severity_under_default_posture: medium
    finding: |
      The essay-context.md audience is "general tech-curious reader, roughly
      high-school-to-early-undergrad literacy." Series-wide vocabulary contract
      requires this essay to explicitly DEFINE "zone / multi-zone = the grid the field
      of view is divided into; each cell yields its own distance reading" since
      Articles 2 and 3 reuse the term without redefinition. The draft uses "zone(s)"
      five times but never states the zone=cell equivalence in one clear defining
      sentence. A first-time reader can infer the connection from proximity, but the
      callback contract asks this essay to *own* the definition outright.
    recommendation: |
      Insert an explicit equivalence at first use, e.g. "give every cell in that
      grid — every zone — its own histogram."

  - pass: pass-5-reader-perspective
    location: "§3-§4 (paragraphs flagged under Pass 2 density)"
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Cross-referencing Pass 2's density finding: the same 100-160+ word paragraphs
      sit in immediate sequence across §3-§4, a 3+ consecutive paragraph run of
      patent-mechanism detail without a reader-surface breath between them (the 5A
      "density wall" pattern; kept at medium given one figure caption provides a
      partial visual surface).
    recommendation: |
      Same fix as Pass 2: split the long paragraphs at their internal idea boundaries.

  - pass: pass-5-reader-perspective
    finding: "no findings beyond the two above"
    scoped_to: "Lead hook-landing, stake clarity, closing-in-isolation test — all clean."

  # ---------------------------------------------------------------------
  # Pass 6 — Lead/conclusion + format compliance
  # ---------------------------------------------------------------------
  - pass: pass-6-lead-conclusion-format
    finding: |
      6A lead anchor passes. 6B frame closure passes (matches thesis-spine's required
      closing-open-question mapping). 6C Sources block passes (6 entries, 3 categories,
      all-or-nothing subgrouping satisfied). 6D author format not applicable (no
      multi-author papers). 6E mechanical compliance passes (em-dash=0, all citations
      4-digit, banned-word grep=0, single # Sources). 6F title passes (12-word
      declarative, no em-dash/colon-subtitle).
    scoped_to: "Lead, closing, full Sources block, title line, full-body mechanical grep."

  # ---------------------------------------------------------------------
  # Pass 7 — Adversarial reader-pass (fresh-eyes)
  # ---------------------------------------------------------------------
  - pass: pass-7-adversarial-reader
    location: "§1 (H1 + first paragraph)"
    severity: low
    severity_under_default_posture: low
    finding: |
      Check 1 (BLUF lead-altitude): PASS with a caveat — tension lands by sentence 2,
      resolution two sentences later, within budget but not maximally front-loaded.
    recommendation: |
      Optional tightening only — no action required to clear the loop.

  - pass: pass-7-adversarial-reader
    finding: |
      Checks 2-7 all PASS: header-as-claim, steelman present (product-identity
      disclaimer conceded at full strength before refinement, matching thesis-spine's
      required steelman beat), no meta posturing, jargon unpacked at first use, no
      stub/rhythm break, thesis not over-restated (asserted in lead + closing only).
    scoped_to: "All 5 body headers, full draft read as both personas, meta/jargon/stub/restatement scans."
```
