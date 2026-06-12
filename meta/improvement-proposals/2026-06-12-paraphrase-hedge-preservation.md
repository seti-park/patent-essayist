---
proposal_id: 2026-06-12-paraphrase-hedge-preservation
created: 2026-06-12T05:00:00Z
status: recommended-apply
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/citation-format.md (hedge / scope-qualifier handling in quotes and paraphrase)
recurrence_count: 3
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: paraphrase-hedge-compression   # may/can embodiment-hedge cluster
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: paraphrase-hedge-compression  # claim-21 "at least a portion" compressed to full conformity
  - essay_id: tesla-washer-pump-two-wire-moat, iter: 1, pattern_tag: paraphrase-hedge-compression        # EL-06 "In some examples" qualifier dropped on q-0011-2
---

## Problem

3/3 essays compressed a source hedge or scope qualifier when quoting or paraphrasing: may/can
embodiment hedges (deleted-dome), a claim's "at least a portion of" scope limit (both-and-steel),
and the "In some examples" embodiment register on an otherwise byte-exact quote
(tesla-washer-pump EL-06). Each promotes example-embodiment or partial-scope language toward an
unqualified assertion — certainty/scope drift that threatens goal 1 (catch the patent's core
accurately) and, for claim language, overstates what the patent locks. The defect survives the
byte-match discipline because the dropped qualifier sits *outside* the quoted substring;
`gate_anchors` and Pass-3 string matching are structurally blind to it.

`citation-format.md` currently states the verbatim-match rule and "paraphrasing is allowed" but
says nothing about qualifier preservation, so each run relies on the editor to catch it
(it has cost a Pass-3/Pass-… finding every run, three runs straight).

## Proposed change (exact diff)

Against `.claude/skills/essay-en-composer/references/citation-format.md`, insert a new
subsection between the paraphrase allowance and `## Examples` (i.e. after the line
"But: even non-cited prose must not introduce facts. If \"three days later\" is a fact, the date
must be derivable from cited facts."):

```diff
 But: even non-cited prose must not introduce facts. If "three days later" is a fact, the date must be derivable from cited facts.
 
+## Hedge and scope-qualifier preservation
+
+Patent prose is deliberately qualified. When the source span carries a hedge or scope
+qualifier, the essay must preserve it or restate it equivalently — in paraphrase AND in the
+framing around a verbatim quote:
+
+- **Embodiment hedges**: "in some examples", "in one configuration", "may", "can",
+  "in certain embodiments". Dropping one promotes an example to the invention itself.
+- **Scope qualifiers** (claim language): "at least a portion of", "substantially",
+  "approximately", threshold conditions. Dropping one widens the claim's lock.
+
+A quoted substring that byte-matches its anchor is still a paraphrase mutation
+(certainty/scope drift) if the sentence hosting it strips the source's qualifier. When the
+exact qualifier reads awkwardly in essay voice, restate it ("In one configuration, ...",
+"for at least part of the channel") — never delete it silently.
+
+❌ *The pump reports fluid level over the power lines [0011].*  (source: "In some examples, ...")
+
+✓ *In one configuration, the pump reports fluid level over the power lines [0011].*
+
 ## Examples
```

## Why this lever

Reference-edit at the artifact the composer reads while citing is the cheapest durable fix.
Gate-promotion is unsafe: detecting a dropped qualifier requires comparing essay framing against
source-span context — judged, not mechanical, with high false-positive risk on legitimate
restatements. The class is consistent (same mechanism three runs) and low-cost to state as a
rule, so confidence is high despite all records being low/medium severity.

## Regression expectation

`python .claude/skills/_shared/scripts/test_gates.py` and `python meta/regression.py` must still
pass (no gate or fixture parses citation-format.md). After applying, Pass-3/paraphrase passes
should stop producing `paraphrase-hedge-compression` records; the round-2 verifications in all
three runs (qualifier restored, byte-match preserved) demonstrate the rule is satisfiable without
breaking the verbatim-match discipline.
