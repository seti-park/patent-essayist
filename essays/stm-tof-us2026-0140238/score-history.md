# Score history — STM VL53L9CX Article 1 (Mechanism), US 2026/0140238 A1

Compose↔Edit inner loop. Threshold `pass`, posture `measured` (general-audience storytelling,
patent-as-protagonist). Max 4 iterations.

| Iter | Deterministic gates | Editorial assessment | Round result | Note |
|---|---|---|---|---|
| 1 | PASS (0 fail, 7 warn) | revise-recommended | **FAIL** | 0 critical / 0 high / 2 medium / low. Grounding clean; both verbatim anchors exact; no non-assertable spec leaked; "first" properly qualified. Two medium readability findings block `pass`. |
| 2 | PASS (0 fail, 7 warn) | pass | **PASS** | Revisions applied; both mediums resolved; loop terminates. |

Terminated at iteration 2 (cap 4), result PASS.

## Iteration-1 findings and how they were resolved (SETI revise → essay-final.md)
- **medium · §3 cluster sentence (111 words):** split and front-loaded (BLUF). The five adjacent
  ST filing numbers moved to the `# Sources` block; prose now carries the idea, not the catalogue.
  Resolves the cross-listed low on subject-verb agreement ("sit a cluster" → "Around it sits").
- **medium · body length ~1,443 words vs 1,000-1,300 target:** trimmed to ~1,366 words via the
  reviewer's named cuts (the §4 infrared/confidence-data tail dropped; §3 cluster enumeration
  compressed) plus light connective tightening and one borderline forward-gesture removed
  ("the next section is where it pays off"). No spine element, verbatim quote, vocabulary
  definition, or analogy was cut. Residual minor overage is a deliberate accessibility choice
  (goal 3); the platform reference deliverable runs ~1,560 words.
- **accuracy hardening (orchestrator catch, beyond the passes):** the five cluster filings and the
  ST launch press release carried composed/quoted titles that are not in the verified source set.
  Converted to descriptive role glosses / a descriptive locator so no unverified title is presented
  as verbatim. Hero and support titles are verified from the patents and kept as quoted.

## Warn-only (never blocks)
- `typography` LONGSENT x7: all warn-only. Verified as tokenizer joiner artifacts (frontmatter,
  cross-header joins, the Sources block) plus one ~45-word spec-list sentence in §4; the genuine
  111-word run-on was the iteration-1 cluster sentence, now split.

## Hard-gate checks
- Grounding hard-gate (goal 1): clear. No pass-3 high/critical; `gate_anchors` PASS; both verbatim
  anchors verified as exact substrings of source; every `[dddd]` on the allow-list and supportive.
- Goal-2 hard-gate: clear. No figures this run, so figure coverage is satisfied by sufficient use
  of the specification text (every mechanism step grounded in a named paragraph plus two verbatim
  spec/claim quotes). No `FIGUSE-001` (no figures selected).
