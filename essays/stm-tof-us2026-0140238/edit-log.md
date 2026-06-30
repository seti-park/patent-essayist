review_id: stm-tof-us2026-0140238-editorial-review-1
draft_source: handoff/02-compose/essay-draft.md
review_timestamp: 2026-06-30T00:00:00Z
posture_applied: measured
overall_assessment: revise-recommended

# Summary
#   Voice-FENCED 7-pass editorial review (deliverable-voice-rules + anti-ai-writing only;
#   voice-profile NOT loaded). Deterministic gates: all 11 PASS (warn-only on LONGSENT x7,
#   FIGREF/FIGUSE skipped — no figures this run).
#   Findings: critical 0 / high 0 / medium 2 / low 5.
#   No publication-blocking defect. Two medium readability findings (the 111-word cluster
#   sentence in §3 and overall body length ~1,443 words vs 1,000-1,300 target) set the
#   assessment to revise-recommended. All Pass-3 fact/anchor/verbatim checks pass clean;
#   all anti-exaggeration guards hold; no non-assertable spec leaked.

findings:

  # ---------- PASS 1: voice canon + anti-AI ----------
  - pass: pass-1-voice-anti-ai
    finding: "no findings"
    scoped_to: |
      Banned-word grep clean (0 hits). No banned rhetorical patterns: no not-just-X-but-Y,
      no despite-the-challenges, no copula avoidance (no represents/serves as/constitutes/
      stands as), no section summaries, no vague attributions, no puffery, no elegant
      variation (STMicroelectronics / ST / "the company" used as stable references, not
      renamed mid-paragraph to disguise repetition). No em-dash in body (em-dash is Pass-6
      mechanical, also clean). Bold used twice as load-bearing vocabulary anchors
      (**histogram**, **zone**) plus one thesis-anchor sentence (**The peak is marked as it
      streams past...**) — within the single-anchor allowance, not bold overuse. No emoji,
      no ALL-CAPS emphasis (acronyms SPAD/TDC/VCSEL-absent are fine). Title Case headers per
      X Articles house style. Voice fence respected: judged on deliverable-voice-rules +
      anti-ai-writing only.

  # ---------- PASS 2: redundancy + compression ----------
  - pass: pass-2-redundancy
    location: §3, paragraph "Here is the move the hero patent is built around" (189 words, 7 sentences)
    severity: low
    severity_under_default_posture: low
    finding: |
      Paragraph runs 189 words carrying one spine idea (stream the histogram, mark the peak
      on the way past, store nothing). Under 8 sentences so not a hard-flag, but it is the
      single densest block in the essay and stacks two verbatim quote fragments ([0042],
      [0069]) plus the conveyor-belt analogy plus the running-state point [0016]. The
      quote-integrated paragraph heuristic (verbatim quote + narrative anchor + cite as a
      unified structure) demotes this to low under measured posture — the rhythm + quote
      anchoring earns the length.
    recommendation: |
      Optional. A reader-perspective split (see pass-5 finding on this paragraph) would also
      resolve the density here. Do NOT cut the [0042]/[0069] verbatim fragments or the
      conveyor analogy — both are required spine content. If splitting, break after
      "...the full chart never has to be stored." so the bold thesis-anchor sentence ends
      paragraph one and the two source quotes open paragraph two.
    quote: "Here is the move the hero patent is built around. ... so it holds a small running state instead of the whole picture [0016]."

  - pass: pass-2-redundancy
    location: §3 "That support filing walks the bins once" (164 w) and §4 "This is where the patent meets a real product" (173 w)
    severity: low
    severity_under_default_posture: low
    finding: |
      Two further 150+ word single-spine paragraphs. §3's support-filing paragraph carries
      one idea (the 2022 single-pass principle, same inventor) but absorbs the 79-word
      cluster sentence (flagged separately in pass-5). §4's product paragraph carries one
      idea (lean processing enables the real VL53L9 numbers) but packs FoV + range + fps +
      on-chip + flood + 35x + "first" caveat into one block. Each is a compression OR split
      candidate; neither is publication-blocking and both stay under 8 sentences.
    recommendation: |
      Lower priority than the cluster-sentence and length findings. If body length is
      trimmed to target (see pass-2 word-count finding), these two paragraphs are the
      natural place to do it without touching a spine element or a verbatim quote.

  - pass: pass-2-redundancy
    location: whole body
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Body prose is ~1,443 words (excluding headings, blockquotes, and the Sources block)
      against the stated 1,000-1,300 target — roughly 110-150 words over. The overage is
      not from claim repetition (no claim appears in 3+ locations; the lead->§5 thesis recap
      is the one acceptable circle-back) but from sentence-level expansiveness in §3 and §4.
      Genuinely cuttable without losing a spine element, a verbatim quote, a vocabulary
      definition, or a needed analogy:
        - §4 "feeding a depth map plus infrared and confidence data to whatever small AI
          runs on the device" — the IR/confidence-data tail is the only place the essay
          drifts past the mechanism into datasheet-adjacent product detail; trimming it
          saves words and tightens scope.
        - §3 cluster sentence's five-filing enumeration can be compressed (see pass-5).
        - Adverbial/connective filler is light but present ("genuinely", "really",
          "straight off it", "the whole game").
    recommendation: |
      Trim toward 1,300. Priority cuts: compress the §3 cluster enumeration and drop the §4
      "infrared and confidence data ... small AI" tail. Do NOT cut: the dToF/iToF/SPAD/TDC
      glosses, the histogram/zone/peak definitions, the conveyor-belt analogy, either
      verbatim block quote, or the Part-2 seam. This is a quality trim, not a blocking
      defect.

  # ---------- PASS 3: claim adequacy + fact verification + paraphrase mutation ----------
  - pass: pass-3-fact-paraphrase
    location: §2 blockquote + §3 inline quotes + §3 support blockquote
    severity: low
    severity_under_default_posture: low
    finding: |
      ALL verbatim and anchor checks pass. Confirmed exact substrings of their sources:
        - HERO block quote "processes time-of-flight measurement data using sequential
          bin-by-bin histogram processing" — exact match, hero Abstract (line 20) and
          claim 1.
        - SUPPORT block quote "each bin of the histogram representing a photon count
          corresponding to a distance from a light-ranging system" — exact match, support
          [0003] (line 31; recurs [0115], [0131], claims).
        - §2 inline quotes "using a sequential bin-by-bin histogram processing" and "one or
          more on-the-fly operations" — both exact substrings of [0015].
        - §3 inline quotes "employs a bin-serial processing approach" + "in a streaming
          fashion, significantly reducing memory requirements" ([0042], exact) and "to
          iterate the histogram by serially computing relevant outputs in a single pass"
          ([0069], exact).
        - §4 "prohibitive" — exact, from [0013].
      Every inline [dddd] is on the invention-summary allow-list AND supports its sentence:
        [0004] (histogram of photon arrival times) supports "records ... how long after
        firing it arrived"; [0003] x2 supports dToF-actual-travel-time and iToF-phase-shift;
        [0042] x2 supports streaming/minimal-memory and on-chip "small circuitry"; [0069]
        supports "single pass"; [0016] (maintain state of most-recently-processed bins)
        supports "small running state"; [0013] supports the memory-prohibitive claim;
        [0015] is referenced in prose ("paragraph [0015]") for the claim wording and is on
        the allow-list. No anchor cites a paragraph outside the allow-list. No paraphrase
        drift detected.
    recommendation: |
      No action. Recorded as an explicit pass of the run's highest-risk area.
    scoped_to: "Both verbatim block quotes, all inline quoted fragments, and all 7 distinct [dddd] anchors verified against input/patent.md and input/patent-support.md."

  - pass: pass-3-fact-paraphrase
    location: §4, product paragraph (external ST facts F1-F5) + Sources
    severity: low
    severity_under_default_posture: low
    finding: |
      External fact check clean. 2,268 zones / 54x42 / "2.3K zones" / ~35x over <=64-zone
      prior gen / 5 cm-9 m / up to 100 fps / on-chip processing / flood illumination / depth
      map output all map to verified Tier-1 ST facts F1-F3 in fact-check-log.md, and all are
      attributed to ST in prose ("STMicroelectronics describes...", "The company frames...").
      The "first" qualifier is handled exactly as required: "the first direct Time-of-Flight
      3D LiDAR all-in-one module in its own portfolio rather than the first ever; multizone
      dToF already existed" — ST's qualified portfolio wording WITH the mandated not-the-
      first-ever caveat. The ~35x is framed as ST's comparison, not as fact. # Sources lists
      the press release, blog, and databrief. NO non-assertable datasheet figure leaked:
      grep for 940 nm / BSI / stacked / VCSEL / BCD / 150 mW / milliwatt / package dims /
      TNR / 1% returns nothing in the draft. Power stays qualitative ("battery-friendly",
      "power-hungry chip ... no longer needs"). Anti-exaggeration guards all hold: no
      "measures the speed of light directly", no claim ST "solves SLAM".
    recommendation: |
      No action. Recorded as an explicit pass.

  # ---------- PASS 4: logical alignment + causality ----------
  - pass: pass-4-logic-causality
    location: §1->§3 (histogram -> peak -> distance) and §4 (lean memory -> on-chip -> small module)
    severity: low
    severity_under_default_posture: low
    finding: |
      Both load-bearing causal chains are stated as the patent supports, no overclaimed
      causation. (1) histogram -> peak -> distance: the prose grounds each step — photons
      sorted into time bins build the histogram [0004]; the tall bar's position is the
      round-trip time and "the round-trip time is the distance" (mechanism, claim 9 content,
      [0004]); this is causation with mechanism shown, counterfactual implicit (no pile-up,
      no peak). (2) lean memory -> on-chip -> small module: stated with correct directionality
      and hedge — "Take the memory away and the rest follows. The processing no longer needs
      a power-hungry chip ... It can ride on the sensor's own small circuitry [0042], which
      is what lets a complete sensor shrink to roughly the size of a fingernail." Leanness is
      attributed to the architecture and the patent's qualitative language per the scope-
      discipline note, NOT to the bare independent claim. Spine->section trace: all five
      design layers (problem / verbatim claim / mechanism / product / why-it-matters) are
      present and in order; no section advances an out-of-spine claim. The product numbers
      are correctly fenced as "what the lean processing enables", never as something claim 1
      recites — the spine's adversarial-defense mitigation is honored.
    recommendation: |
      No action.
    scoped_to: "Both causal chains + spine->section alignment (5 layers) + claim-scope discipline."

  # ---------- PASS 5: reader perspective + paragraph readability ----------
  - pass: pass-5-reader-perspective
    location: §3, "Around the hero sit a cluster of adjacent STMicroelectronics filings..."
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Single sentence of ~79 words (the gate's tokenizer counts 111 with the five
      parenthetical patent numbers split out; either way it is the longest sentence in the
      essay). It enumerates five adjacent ST filings, each with its own patent number, then
      pivots with "but the streaming peak finder is the part this story is about." For the
      stated high-school~undergraduate audience (goal 3), this is a genuine readability
      problem: the reader must hold five parallel clauses and five US-number parentheticals
      across one breath before reaching the point. On a mobile render it is a wall. The
      five-filing roster is also the least spine-critical content in §3 — interesting
      context, not load-bearing for the mechanism.
    recommendation: |
      Split, and front-load the point (BLUF). Lead with the takeaway, then list compactly,
      for example: "The streaming peak finder is the part this story is about. Around it sits
      a cluster of adjacent ST filings, each taking one step of the pipeline — building the
      bins, summing SPAD outputs, extracting distance, sharpening it, and assembling the full
      array." The individual patent numbers can move to the Sources block (where all five
      already appear) so the prose carries the idea, not the catalogue. This single change
      also resolves part of the §3 paragraph-length pass-2 finding and trims the body toward
      target.
    quote: "Around the hero sit a cluster of adjacent STMicroelectronics filings that each take one step of the pipeline, a TDC that builds the bins (US 2021/0302550), ... but the streaming peak finder is the part this story is about."

  - pass: pass-5-reader-perspective
    location: §3, "Here is the move the hero patent is built around" (189 w, 7 sentences)
    severity: low
    severity_under_default_posture: low
    finding: |
      The densest mechanism block: the conveyor-belt analogy, the bold thesis-anchor
      sentence, and two stacked verbatim source quotes ([0042], [0069]) plus the [0016]
      running-state point all land in one paragraph. It is the payoff paragraph so the
      density is partly earned, but a reader at the high-school end may lose the thread
      between the homely conveyor image and the two quoted technical fragments. Not a density
      WALL (it is one paragraph, preceded and followed by lighter ones), so low not high.
    recommendation: |
      Optional split after "...the full chart never has to be stored." (see pass-2). Putting
      the analogy + bold anchor in one paragraph and the two source quotes in the next keeps
      the analogy clean and lets the quotes corroborate it rather than crowd it.

  - pass: pass-5-reader-perspective
    location: §2, "histogram" first appears in the §2 blockquote (line 24) before its §3 definition
    severity: low
    severity_under_default_posture: low
    finding: |
      "histogram" appears inside the verbatim claim quote in §2 ("...bin-by-bin histogram
      processing") and again in §2's gloss ("a single slice of time...") before it is
      formally defined as bold vocabulary in §3 ("That bar chart is a **histogram**"). The
      word is legible in context and the formal definition follows one section later, so this
      is mild, not a comprehension break — but a first-time reader meets the term twice
      before the picture-of-a-bar-chart definition arrives. dToF/iToF/SPAD/TDC/zone/multizone
      are all glossed cleanly on first use; histogram is the one term whose plain definition
      trails its first appearance.
    recommendation: |
      Optional. A four-word appositive at the §2 first use ("...bins, the slices that make up
      a histogram, a bar chart of arrival times...") would close the gap, or accept it given
      the §3 definition lands quickly. Low priority.

  # ---------- PASS 6: lead/conclusion + format compliance ----------
  - pass: pass-6-lead-conclusion-format
    location: §1 lead and §5 conclusion + # Sources + mechanical
    severity: low
    severity_under_default_posture: low
    finding: |
      Lead/closure and all mechanical format checks pass. Lead (§1): opens on the technical-
      impossibility hook the spine declares (flashlight at a wall -> "about twenty billionths
      of a second" -> "you cannot start a stopwatch ... and a sensor cannot really start one
      either"), a declarative reader-experience frame, not a deferred question; the patent's
      problem (time a few photons) is on the table by the end of §1 and the patent itself
      lands in §2. Closure (§5): returns to the frame ("Stream those slices in order, mark
      the peak on the way past, and keep almost nothing in memory") and lands the spine's
      acknowledged residual risk via a clean forward-pointer to Part 2 ("A peak is only as
      trustworthy as the histogram under it ... Part 2 is about learning to trust the
      distance") — matches the spine's one-sentence seam and the closing-forward-watching /
      open-question posture for acknowledged risk. Mechanical: em-dash count 0 (body and
      title); title uses no separator (no em-dash); all inline cites are well-formed 4-digit
      [dddd]; # Sources appears exactly once as h1 with three enum-valid subheadings
      (Patents / Official statements / Technical specs), subgrouping is all-or-nothing (every
      entry categorized); no footnote defs leaked into publication.md; banned-word grep 0.
    recommendation: |
      No action.
    scoped_to: "Lead anchor, frame closure + residual-risk posture, # Sources 5-enum + all-or-nothing, em-dash, [dddd] format, banned-words, footnote strip, title em-dash."

  # ---------- PASS 7: adversarial reader (fresh-eyes) ----------
  - pass: pass-7-adversarial-reader
    location: §3 cluster sentence (cross-listed) + §3 histogram-first-use (cross-listed)
    severity: low
    severity_under_default_posture: low
    finding: |
      Read as (a) impatient general reader and (b) skeptical engineer. Decomposed checklist:
        1. BLUF lead-altitude — PASS. §1 para 1 is a declarative claim ("The honest answer is
           about twenty billionths of a second"), not a deferred question.
        2. Header-as-claim — PASS. All six headers are assertions; a header-only skim
           reconstructs the argument (light too fast -> count photons; claim is one sentence
           about bins; histogram read one bar at a time; lean math -> fits on a fingernail;
           the grammar the series is built on).
        3. Steelman present — PASS (in-scope). The natural strongest objection for THIS piece
           is "a broad one-sentence claim is being credited with a flagship product"; the
           draft pre-empts it: "It is careful with the word 'first' ... multizone dToF already
           existed. What is genuinely new is the resolution and the spread of light, and
           underneath both sits the lean processing the patent describes." The claim/product
           separation is conceded and refined, not dodged.
        4. No meta posturing — PASS. No reader-instruction / essay-self-reference. "and it is
           the grammar everything in this series is built on" is a thesis statement about the
           subject, not a stage direction; "the next section is where it pays off" is a mild
           forward gesture, borderline but not a how-to-read instruction (gate_meta clean).
        5. Jargon as signpost — PASS. dToF/iToF/SPAD/TDC kept short and glossed, not deep-
           dived; the only first-use trailing-definition is "histogram" (cross-listed, low).
        6. No stub / rhythm break — PASS. §5 is the shortest section but is a deliberate
           synthesis+seam, proportionate; gate_stub clean.
        7. Thesis not over-restated — PASS. The core verdict (stream the histogram, find the
           peak, keep almost no memory -> fits on-chip) is asserted in §3, restated once in
           §4 (as the product enabler) and once in §5 (synthesis) = within the <=3-section
           bound; the §5 recap is the sanctioned closing circle-back, not redundant assertion.
      The only adversarial snags are the two already-filed readability items (the 79/111-word
      cluster sentence the impatient reader stumbles on; the histogram term met before its
      definition). No NEW high finding from fresh eyes.
    recommendation: |
      No new action beyond the pass-5 cluster-sentence split and the optional histogram
      first-use gloss. Recorded as an explicit adversarial pass.
    scoped_to: "All 7 pass-7 checks, decomposed yes/no with evidence, read as impatient reader + skeptical engineer."

  # ---------- minor polish ----------
  - pass: pass-5-reader-perspective
    location: §3, "Around the hero sit a cluster ..."
    severity: low
    severity_under_default_posture: low
    finding: |
      Subject-verb agreement: in the inverted locative "Around the hero sit a cluster of
      adjacent ... filings", the postponed grammatical subject is the singular head noun
      "a cluster", so strict prescriptive agreement wants "sits a cluster". ("Cluster of
      [plural]" can take notional-plural agreement, so this is defensible, not an error —
      but a careful reader may read it as a slip.)
    recommendation: |
      If the cluster sentence is rewritten per the pass-5 split (recommended), this resolves
      naturally ("Around it sits a cluster ..."). Otherwise change "sit" -> "sits".
    quote: "Around the hero sit a cluster of adjacent STMicroelectronics filings"

  # ---------- goal-2 (spec coverage replaces figure coverage this run) ----------
  - pass: claim-adequacy
    location: whole essay (goal-2 spec-coverage check)
    severity: low
    severity_under_default_posture: low
    finding: |
      With no figures this run, goal 2 is satisfied by sufficient use of the specification
      text to carry the mechanism — and it is. The essay grounds every mechanism step in
      named specification paragraphs ([0003][0004] problem/dToF-iToF; [0013] memory cost;
      [0015] claim wording; [0042][0069][0016] streaming/single-pass/running-state) plus the
      support filing's principle ([0003]/[0004], named in prose), and lands two verbatim
      spec/claim quotes. The mechanism is carried entirely by prose, as figure-selection.md
      intended. No orphan-figure risk (no figures selected). Specification use is sufficient
      to carry the invention without illustration.
    recommendation: |
      No action.
    scoped_to: "Goal-2 spec-coverage substitute for figure coverage; no figures selected this run."
