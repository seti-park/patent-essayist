---
proposal_id: 2026-06-30-multi-paragraph-anchor-coverage
created: 2026-06-30T00:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/citation-format.md (Multiple citations — multi-paragraph span anchoring)
recurrence_count: 2
confidence: medium
triggering_findings:
  - essay_id: 2026-06-26-us12560948b2-investor-selfaudit, iter: null, pattern_tag: anchor-incomplete, origin: self-post-accept
  - essay_id: stm-tof-us2026-0140238, iter: null, pattern_tag: anchor-incomplete, origin: self-post-accept
---

## Problem

A goal-1 grounding class, `anchor-incomplete`, now appears in **2 essays / 3 ledger records**,
each caught **only by the autonomous post-acceptance self-audit** (`origin: self-post-accept`)
— never by the inner-loop pass-3 or any deterministic gate. The shared root cause: when an idea
spans **two or more source paragraphs**, the draft attaches a single `[dddd]` anchor to the
paragraph that supports the *first* clause, and the *concluding* clause (which is grounded in a
*later, different* paragraph) inherits that anchor by proximity. The cite is well-formed and
on the allow-list, so `gate_anchors` passes and pass-3's verbatim/allow-list check passes — the
text it quotes really is in the cited paragraph. What is wrong is that the **conclusion is
anchored to the wrong paragraph of the span**, so a fact-checking reader is pointed one
paragraph short of the support.

- **Run `2026-06-26-us12560948b2-investor-selfaudit`** (reviewer C, self-audit): a FIG. 3
  caption anchored "the escalation the claim locks" to `[0033]`, but FIG. 3 is introduced and
  walked as a decision tree in `[0035]`–`[0039]`; `[0033]` supports only the "standing still is
  safer" caveat. Fixed by re-pointing the caption anchor to `[0035]`.
- **Run `stm-tof-us2026-0140238`** (self-audit-1): "It can ride on the sensor's own small
  circuitry `[0042]`, which is what lets a complete sensor shrink to roughly the size of a
  fingernail." `[0042]` grounds only memory reduction / streaming; the **on-chip** conclusion
  ("limited local storage in the form of registers … reducing power consumption and chip area")
  lives in `[0043]`. Fixed by re-anchoring the on-chip clause to `[0043]` and hedging the causal
  link to "part of what lets".

Both are the same failure of a multi-paragraph span: one anchor for two paragraphs' worth of
claim, the conclusion clause silently under-anchored. The current `citation-format.md`
`## Multiple citations` section covers the *opposite* and easier case — "if a sentence draws on
multiple paragraphs … cite each contributing paragraph" — but says nothing about a sentence
whose **conclusion is supported by a later paragraph than its premise**, which is exactly the
case that slips through.

`recurrence_count` is 2 distinct essays (3 records), below `RECUR_THRESHOLD=3` by distinct-essay
count, so this files at **`watch`** per the promotion rules — not `recommended-apply`. It is
nonetheless filed (not merely noted) because: (a) it is a **goal-1 grounding** class; (b) it is
a recurring `self-post-accept` class, which per the ledger schema signals *extend coverage*
(the inner loop is structurally blind to it — pass-3 verifies "quote ∈ cited paragraph" but not
"cited paragraph is the *best/true* support for the clause"); and (c) the owner artifact already
exists, so the fix is a cheap, surgical reference-edit. The exact diff is included so a human
can apply early; a third essay would promote this to `recommended-apply`.

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/citation-format.md`** — extend the
`## Multiple citations` section. Replace the existing section body:

```markdown
## Multiple citations

If a sentence draws on multiple paragraphs:

```markdown
The mechanism — vision input [0016] feeding the controller [0017] within the 70ms window [0024] — is claim-anchored.
```

Cite each contributing paragraph.
```

with:

```markdown
## Multiple citations

If a sentence draws on multiple paragraphs:

```markdown
The mechanism — vision input [0016] feeding the controller [0017] within the 70ms window [0024] — is claim-anchored.
```

Cite each contributing paragraph.

### Multi-paragraph spans — anchor the conclusion, not just the premise

When an idea spans two or more source paragraphs and the **conclusion clause is grounded in a
different (usually later) paragraph than the opening clause**, do NOT let the conclusion inherit
the opening clause's anchor by proximity. Anchor each clause to the paragraph that actually
supports it.

✗ "It can ride on the sensor's own small circuitry [0042], which is what lets the sensor shrink to a fingernail."
   — [0042] supports only the streaming/low-memory premise; the on-chip-shrink conclusion is in [0043].

✓ "With local storage cut to a handful of registers, it can ride on the sensor's own small circuitry [0042], which is part of what lets the sensor shrink to a fingernail [0043]."

Rule: before attaching one anchor to a multi-clause sentence, check whether the **last** clause's
claim is supported by the cited paragraph. If the support lives in a later paragraph, give the
conclusion its own anchor (or use the range form `[0042]–[0043]` only if every intervening
paragraph genuinely contributes). The same applies to **figure-caption anchors** that span a
walked sequence: point the caption at the paragraph that *introduces and walks the figure*, not
at a neighboring paragraph that supports only one caveat (e.g. a decision tree introduced in
[0035]–[0039] is anchored [0035], not the adjacent [0033]).

This is the inner-loop-invisible half of grounding: pass-3 verifies that quoted text is inside
the cited paragraph, but not that the cited paragraph is the *true* support for the clause — so
a conclusion anchored one paragraph short passes every gate and pass-3 yet points a fact-checker
short of the evidence.
```

## Why this lever

- The defect is born in Compose: the composer attaches the anchor at draft time, and the
  available information to place it correctly (which paragraph supports which clause) is fully in
  the `invention-summary.md` Quotable spans / Quote anchor table that Compose already reads. A
  `citation-format.md` reference-edit hits the root at the exact place the rule is consulted.
- **Not gate-promotion.** "Is the cited paragraph the *best* support for the concluding clause?"
  is a semantic judgment over claim/spec content; no regex or string check can decide it without
  re-deriving the patent's support structure (which `execution-boundary.md` forbids the gate
  layer from doing). `gate_anchors` already enforces the mechanical half (4-digit format, chain,
  allow-list); the residual is irreducibly judgmental, so it belongs in the procedure the
  composer follows, not in a script.
- **Not a pass-3 rubric change.** Pass-3 is the wrong tier: the inner loop never sees this class
  (3/3 caught by self-audit), and tightening pass-3 to "verify each clause's anchor is the true
  support" would require the editor to re-derive support structure it is fenced from re-deriving.
  Fixing the *compose-time* convention prevents the defect rather than asking a later reviewer to
  reconstruct it.
- **Fencing preserved.** This is a Phase-2 citation-procedure edit (goal-1 grounding), not a
  voice change; it does not touch `voice-profile.md`, `anti-ai-writing.md`, or any gate.

## Regression expectation

Documentation-only change (one Markdown reference file; no script, no `banned_terms.txt`, no
fixture input). After applying:

- `python .claude/skills/_shared/scripts/test_gates.py` — all tests pass, unchanged (no gate
  reads or parses this file).
- `python meta/regression.py` — `clean-baseline` and `figure-orphan` fixtures produce identical
  verdicts (no gate consumes `citation-format.md`).
- Observable success criterion for the next multi-paragraph-span run: each multi-clause
  conclusion carries an anchor to its own true support paragraph (or a justified range), and the
  self-audit surfaces zero new `anchor-incomplete` findings. A third `anchor-incomplete` record
  in a new essay would instead promote this class to `recommended-apply` and start CASCADE
  accounting on `citation-format.md`.
