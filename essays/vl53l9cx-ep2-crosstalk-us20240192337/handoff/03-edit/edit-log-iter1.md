<!--
  Preserved copy of handoff/03-edit/edit-log.md as it stood after editorial-review iteration 1
  (overall_assessment: revise-required), before it was overwritten by iteration 2's full re-review.
  Kept here so pipeline-retro can normalize both iterations' findings for recurrence tracking,
  not just the final passing round.
-->

# Edit Log (iteration 1 — superseded by edit-log.md / editorial-review-2)

```yaml
review_id: vl53l9cx-ep2-crosstalk-us20240192337-editorial-review-1
draft_source: handoff/02-compose/essay-draft.md
review_timestamp: 2026-07-01T09:40:00Z
posture_applied: measured
overall_assessment: revise-required

findings:
  - pass: pass-1-voice-anti-ai
    finding: "no findings"
    scoped_to: "Banned-word grep and banned-pattern grep against deliverable-voice-rules.md + anti-ai-writing.md across all sections. Zero hits. Single closing 🤔 is the sanctioned closing-open-question pattern, not flagged."

  - pass: pass-2-redundancy
    location: "§6 'The Patented Mechanism Behind a Marketing Line', paragraph beginning 'This is where the mechanism meets the product.'"
    severity: medium
    severity_under_default_posture: medium
    finding: |
      This single paragraph is 234 words / ~7 sentences and tangles three distinct ideas
      that phase2-handoff-notes.md itself asked to be kept compact and separate: (1) the
      ST on-chip marketing-claim tie + calibration-free framing, (2) the supporting-patent
      (US 2025-0012901) "changes over time" deepening beat, and (3) the cluster-patents
      one-line breadth gloss. Stacking all three into one unbroken paragraph pushes it past
      the single-idea 150-word earn threshold and correlates with a mobile-rendering concern.
    recommendation: |
      Split into two paragraphs: one carrying the ST marketing-tie + calibration-free beat,
      a second carrying the supporting-patent deepening + cluster-patents gloss. No content cut.
    quote: "This is where the mechanism meets the product. ST's own public description of the VL53L9CX... each one its own fence around a different failure mode."

  - pass: pass-3-fact-paraphrase
    finding: "no findings"
    scoped_to: "Every [dddd] inline citation string-matched byte-for-byte against input/patent.md at its cited paragraph. All 12 unique paragraph numbers trace to invention-summary.md's Quotable spans / Quote anchor table / Layer 2 mechanism list -- no orphan anchors."

  - pass: pass-4-logic-causality
    finding: "no findings"
    scoped_to: "All seven thesis-spine.md spine elements traced to their assigned section; the steelman beat executes the concede-then-refine instruction exactly as specified."

  - pass: pass-5-reader-perspective
    location: "§6, same paragraph flagged under pass-2-redundancy"
    severity: low
    severity_under_default_posture: low
    finding: "Cross-reference to the pass-2-redundancy finding: the same 234-word paragraph renders to roughly 19 mobile lines, past the 8-line target. Resolved as a side effect of the pass-2 fix."
    recommendation: "No separate action needed -- the pass-2-redundancy paragraph split resolves this."

  - pass: pass-6-lead-conclusion-format
    location: "# Sources block"
    severity: high
    severity_under_default_posture: high
    finding: |
      The # Sources block has only ## Official statements and ## Technical specs subheadings.
      It does not list either patent analyzed in the essay body: the subject patent
      US 2024-0192337 B2 or the supporting patent US 2025-0012901. Both handoff-template's and
      essays/agility-us12560948's precedent list the subject patent under a ## Patents
      subheading. Since the block already uses ## subgrouping, the all-or-nothing subgrouping
      rule means every source used -- including the two patents -- must be categorized.
    recommendation: |
      Add a ## Patents subheading (ordered first) with the two patents in 6-field format,
      omitting unstated fields (e.g. publication date) rather than inventing them.

  - pass: pass-7-adversarial-reader
    location: "FIG. 1 caption, sentence 2"
    severity: low
    severity_under_default_posture: low
    finding: "'This essay starts from that same output and asks what else is hiding inside it' contains 'this essay,' borderline self-reference. Judged closer to an exempted functional-scope-disclaimer than banned reader-instruction, but flagged for a second look."
    recommendation: "Optional: rephrase to remove the 'essay' self-reference token."
    quote: "This essay starts from that same output and asks what else is hiding inside it."
```
