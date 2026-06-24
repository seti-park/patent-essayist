# Edit log — US 12,560,948 B2 investor moat article

Phase 3 editorial-review output for the Compose↔Edit inner loop. Posture: measured. Threshold:
`pass`. Three review iterations; the loop terminated at PASS within the 4-iteration cap. Findings
follow `editorial-review/references/feedback-format.md`. Auto-fix is not this skill's job; the
revisions between iterations are recorded under each review.

---

## Review 1 (iteration 1, on the first committed draft)

```yaml
review_id: agility-us12560948-editorial-review-1
draft_source: essays/agility-us12560948/essay-final.md
review_timestamp: 2026-06-24T00:00:00Z
posture_applied: measured
overall_assessment: revise-required

findings:
  - pass: pass-2-redundancy
    location: §"What The Body Forces", paragraph 2 (the cage paragraph)
    severity: high
    severity_under_default_posture: high
    finding: |
      8-sentence paragraph (Pass 2C: an essay paragraph of 8+ sentences is high severity).
      The paragraph bundles the cage setup, the productivity cost, and the boxed-in summary
      with three short punchy sentences. Mechanically it slipped past gate_structure, whose
      threshold is strictly greater than 8.
    recommendation: |
      Split after "...what cheaper machines already do." so the "boxed in / cut the power /
      cage it" closing becomes its own short paragraph.
    quote: "A caged humanoid is an expensive way to do what cheaper machines already do. So the company is boxed in. Cut the power and it falls on someone. Cage it and it earns nothing. The patent steps into exactly that gap."

  - pass: pass-2-redundancy
    location: §"What Claim 1 Locks", paragraph after the claim-1 block quote
    severity: high
    severity_under_default_posture: high
    finding: |
      8-sentence paragraph (Pass 2C). Two ideas tangled: the literal requirements of claim 1,
      and the "protected idea is not the word stop" interpretation plus the Fig. 3 pointer.
    recommendation: |
      Split after "...lower the robot's center-of-gravity [0028]." so the interpretation and
      the figure pointer form a separate paragraph.

  - pass: pass-2-redundancy
    location: §"How Wide Is The Moat", paragraph 1
    severity: high
    severity_under_default_posture: high
    finding: |
      8-sentence paragraph (Pass 2C). The three design-around routes and the "tracks the
      physics" conclusion are one block.
    recommendation: |
      Split after "...or it under-reacts." so the blind-corner caveat and the physics
      conclusion form a separate paragraph.

  - pass: pass-2-redundancy
    location: §"The Investor Read", paragraph 2
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Pass 2B: a single ~60-word sentence carries all three "watch" items with semicolons,
      a non-academic-prose semicolon chain that also reads as a mobile wall (Pass 5C).
    recommendation: |
      Break the watch list into short sentences (or a short list); drop the semicolon chain.

  - pass: pass-3-fact-paraphrase
    location: §"What This Patent Does Not Do", paragraph 2
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Pass 3B: "many capable groups are filing next door" is a competitor-landscape
      generalization with no cited source. External-fact-verification wants competitor/field
      claims anchored, and the claim-scope discipline forbids asserting a universal the record
      does not state.
    recommendation: |
      Ground it in the patent's own References Cited (Tier 2, the filing itself): the citation
      list runs to dozens of adjacent patents and applications.
    related_fact_entry: patent-references-cited

  - pass: pass-3-fact-paraphrase
    location: §Sources, Papers
    severity: low
    severity_under_default_posture: low
    finding: |
      The three academic papers are cited as listed in the patent's Other Publications, with
      title and year but no venue. Verified at Tier 2 (cited in the granted patent); venue
      detail is missing but not load-bearing.
    recommendation: |
      Optional. Leave as-is (provenance is the patent's own reference list) or add venue if a
      primary lookup is run.

  - pass: pass-1-voice-anti-ai
    finding: "no findings"
    scoped_to: "Banned-word/pattern grep (0 hits, confirmed by gate_banned), copula avoidance, transition fingerprint, elegant variation across all sections."

  - pass: pass-3-fact-paraphrase
    finding: "no findings (sub-pass 3A verbatim)"
    scoped_to: "Every [00NN] anchor verified verbatim against invention-summary.md spans; claim-1 block quote checked against the granted claim; no paraphrase mutation."

  - pass: pass-4-logic-causality
    finding: "no findings"
    scoped_to: "Design-around argument grounded in patent mechanism ([0010],[0013],[0033]); strategy inference scoped narrowly (confounders bounded by 'evidence of focus, not a dispositive lock'); no correlation-as-causation; patent and deployments kept separate."

  - pass: pass-5-reader-perspective
    finding: "no findings beyond the paragraph-length items logged under pass-2"
    scoped_to: "Engagement curve, stake clarity at each section boundary, reader profile = tech-industry analyst."

  - pass: pass-6-lead-conclusion-format
    finding: "no findings"
    scoped_to: "Lead anchors thesis by sentence 4; closing returns to the walk-vs-safe-stop frame; em-dash 0; [dddd] 4-digit; # Sources once with 5-label enum, all-or-nothing subgroups; 'Last, First, et al.' author form; title has no em-dash."
```

### Revision applied after Review 1

- Split the three 8-sentence paragraphs (cage, claim-1-locks, how-wide).
- Restructured the §"Investor Read" watch list into four short sentences (no semicolon chain).
- Grounded "many capable groups" in the patent's References Cited ("the filing's own list of
  cited references runs to dozens of adjacent patents and applications").

---

## Review 2 (iteration 2, on the revised draft)

```yaml
review_id: agility-us12560948-editorial-review-2
draft_source: essays/agility-us12560948/essay-final.md
review_timestamp: 2026-06-24T00:30:00Z
posture_applied: measured
overall_assessment: revise-required

findings:
  - pass: pass-2-redundancy
    location: §"What This Patent Does Not Do", paragraph 2 (crowded field)
    severity: high
    severity_under_default_posture: high
    finding: |
      Regression introduced by Review 1's fix. Grounding the "many groups" claim added a
      sentence, pushing this paragraph to 8 sentences (Pass 2C high). Mechanically invisible
      again (gate_structure threshold is > 8).
    recommendation: |
      Split after "...what a crowded field looks like." so the forward-citation and the
      product/certification caveats form a separate paragraph.

  - pass: pass-5-reader-perspective
    location: §"Why It Matters Now", paragraph 2
    severity: medium
    severity_under_default_posture: medium
    finding: |
      Pass 5C: ~152-word paragraph (> 8 mobile lines) carrying two ~46-word sentences (the SPAC
      facts and the GXO deployment facts). Also Pass 2C 150+-word multi-idea.
    recommendation: |
      Split at the financing/deployment boundary and tighten the two long sentences.

  - pass: pass-1-voice-anti-ai
    finding: "no findings"
    scoped_to: "Re-grep after revision; 0 banned hits (gate_banned confirms)."
  - pass: pass-3-fact-paraphrase
    finding: "no findings"
    scoped_to: "Review-1 medium (many-groups) resolved by grounding in References Cited; all [00NN] anchors still verbatim."
  - pass: pass-4-logic-causality
    finding: "no findings"
    scoped_to: "Argument structure unchanged by the splits."
  - pass: pass-6-lead-conclusion-format
    finding: "no findings"
    scoped_to: "All six deterministic gates still PASS with zero findings."
```

### Revision applied after Review 2

- Split the crowded-field paragraph after "...what a crowded field looks like."
- Split §"Why It Matters Now" paragraph 2 at the financing/deployment boundary and tightened the
  two long sentences (removed "going onto the balance sheet", "on the record", and "the combined
  company expected to").

---

## Review 3 (iteration 3, on the final draft) — PASS

```yaml
review_id: agility-us12560948-editorial-review-3
draft_source: essays/agility-us12560948/essay-final.md
review_timestamp: 2026-06-24T01:00:00Z
posture_applied: measured
overall_assessment: pass

findings:
  - pass: pass-1-voice-anti-ai
    finding: "no findings"
    scoped_to: "Banned word/pattern grep clean; no copula avoidance, transition fingerprint, or elegant variation."
  - pass: pass-2-redundancy
    finding: "no findings"
    scoped_to: "Every body paragraph now 2-7 sentences (no 8+); no claim repeated 3+ times; no 150+-word single-idea blocks."
  - pass: pass-3-fact-paraphrase
    finding: "no findings"
    scoped_to: "[00NN] anchors verbatim vs invention-summary; external facts (SPAC, GXO) Tier 1-3 sourced and fenced as outside the filing; competitor-field claim grounded in References Cited."
  - pass: pass-4-logic-causality
    finding: "no findings"
    scoped_to: "Mechanism-backed design-around argument; strategy inference scoped; no correlation/causation or reverse-causation drift."
  - pass: pass-5-reader-perspective
    finding: "no findings"
    scoped_to: "Hook lands by sentence 3-4; no density wall; all paragraphs under the mobile line ceiling."
  - pass: pass-6-lead-conclusion-format
    finding: "no findings"
    scoped_to: "Lead/closing frame closure; # Sources 5-label enum + all-or-nothing subgroups; mechanical gates all PASS."
```

---

## Grounding hard-gate check (loop policy)

No pass-3 finding reached `high`/`critical` at any iteration (the pass-3 items were `medium`
and `low`), and `gate_anchors` passed every round, so the grounding hard-gate (goal 1) was never
breached. Goal-2 hard-gate clear: no `FIGUSE-001` orphan and no pass-3 coverage `high`
(figures 1, 3, 6 all used; the invention-summary core mechanism is covered in the draft).
