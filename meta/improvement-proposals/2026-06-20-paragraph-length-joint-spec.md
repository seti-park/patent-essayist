---
proposal_id: 2026-06-20-paragraph-length-joint-spec
created: 2026-06-20T17:40:00Z
status: watch
lever: reference-edit
goal: "3"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/section-blueprint.md (word_target says nothing about the mobile line ceiling) + _shared/references/deliverable-voice-rules.md ("Paragraph length within the format's band" — band defined nowhere concretely, not reconciled with the ~8-line mobile ceiling the editor's pass-5 applies)
recurrence_count: 3
confidence: medium
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 3, pattern_tag: revision-induced-band-break
---

> **Filed `watch` despite reaching recurrence 3 (3/3 essays).** Every occurrence is an
> *accepted deliberate trade-off* — the editor prescribes the split knowingly, the result
> reads as intentional cadence, and the class has **never cost a FAIL or an extra
> iteration**. Same posture the attribution table holds `redundancy-bloat` at (count
> reached, held at watch because no single mechanical rule fits and it never gated a loop).
> The diff is on record so a human can apply early; it is the documented companion to
> `2026-06-11-gate-structure-word-wall.md` (STRUCT-005 warns on walls; this keeps the *fix*
> for a wall from creating a band underrun).

## Problem

The pipeline specifies paragraph length in **two unreconciled places**, so a revision that
satisfies one criterion can break the other:

1. **Mobile ceiling (~8 lines / ~110 words):** applied by editorial pass-5 (reader
   perspective) and the proposed `STRUCT-005` warn. Splitting an over-long paragraph fixes it.
2. **Sentence band (the deliverable-voice "format's band", treated by the editor as 3–7
   sentences):** `deliverable-voice-rules.md` line 24 says only *"Paragraph length within the
   format's band"* — the band is never defined concretely there, and `section-blueprint.md`'s
   `word_target` field (line 18) says nothing about either ceiling.

When pass-5 mandates a split to clear the mobile ceiling, the resulting short paragraph can
fall **under** the sentence band — a `revision-induced-band-break`. 3 records, **3 of 3
essays**, all `low`, all accepted:

- **Run 1, iter 2 (ED2-02):** the iter-1 mobile-wall splits created two 2-sentence paragraphs
  and left SS3 P2 at 2 sentences. Accepted as deliberate cadence acceleration; the editor
  noted "the 8-line mobile ceiling and the 3-7 sentence band conflict at the margins."
- **Run 2, iter 2:** the F11 splits created `§1p3` at 2 sentences and two consecutive
  single-sentence `§3` enumerations; rejoining `§3` would yield 124w, back over the ceiling.
  "Exact recurrence of run-1 ED2-02."
- **Run 3, iter 3:** the round-2-prescribed split of the 150w §4 paragraph (to clear the
  mobile-wall medium that was the last thing before PASS) isolated the final
  two-independent-claims sentence as a **one-sentence paragraph**. Accepted per the round-2
  editor's explicit prescription as deliberate closing emphasis.

The pattern is structural, not a composer error: the two criteria are individually correct but
were never jointly specified, so the editor must adjudicate the conflict by hand every time a
split lands near the band floor.

## Proposed change (exact diff)

A single `reference-edit` across the two artifacts, pinning both criteria in one place and
carving the explicit exception the editor has granted three times.

**File 1: `.claude/skills/essay-en-composer/references/section-blueprint.md`** — extend the
`word_target` field so the composer plans to *both* criteria at once:

```diff
-- `word_target` — integer. Composer writes within ±20%.
+- `word_target` — integer. Composer writes within ±20%. Jointly bounded paragraph length:
+  keep body paragraphs **≤ ~110 words / ~8 mobile lines** (upper, mobile ceiling — see
+  STRUCT-005) **and ≥ 3 sentences** (lower, the deliverable-voice band), EXCEPT deliberate
+  1–2-sentence emphasis/cadence beats at a section open, a section close, or the essay lead,
+  which are sanctioned. When a paragraph must be split to clear the mobile ceiling, prefer a
+  seam that leaves both halves in-band; if the only good seam yields a 1–2-sentence half,
+  that half must be a deliberate emphasis/cadence beat (mark it `structural_note: emphasis
+  beat`), not an accidental fragment.
```

**File 2: `.claude/skills/_shared/references/deliverable-voice-rules.md`** — define the band
concretely and reconcile it with the mobile ceiling (this file is inside the Phase-3 fence, so
the editor can decide the conflict from the rule itself instead of adjudicating ad hoc):

```diff
-- Paragraph length within the format's band; no bold/bullet overuse; no reflexive
-  rule-of-three triads. *(gate warns: `STRUCT-00x`)*
+- Paragraph length jointly bounded: **≥ 3 and ≤ 7 sentences** AND **≤ ~110 words / ~8 mobile
+  lines**. The two bounds can conflict at the margins — a split made to clear the mobile
+  ceiling may drop a half below 3 sentences. A resulting **1–2-sentence paragraph at a
+  section open/close or the essay lead is sanctioned as a deliberate emphasis/cadence beat**
+  (do not flag); a 1–2-sentence fragment mid-section with no cadence purpose is still a
+  finding. The mobile ceiling takes precedence over the sentence floor when they conflict
+  (a breather reads better than a wall). No bold/bullet overuse; no reflexive rule-of-three
+  triads. *(gate warns: `STRUCT-00x`)*
```

## Why this lever

- The root cause is two correct rules specified apart and never reconciled — a pure
  procedural/spec gap, which is exactly what a `reference-edit` fixes. Pinning the numbers and
  the precedence rule in `deliverable-voice-rules.md` (fence-visible) lets the Phase-3 editor
  decide the conflict from the rule, removing the per-run hand-adjudication; pinning them in
  `section-blueprint.md` lets Compose avoid the conflict at planning time.
- **Not gate-promotion:** a sentence-floor gate would have to know whether a 1–2-sentence
  paragraph is a sanctioned cadence beat or an accidental fragment — a judgment, not a regex.
  (The *upper* bound is already going mechanical as STRUCT-005 in the word-wall proposal; this
  proposal deliberately handles only the *lower* bound and the precedence rule, which are
  judgment-bound.)
- **Voice fence preserved:** the edit touches `deliverable-voice-rules.md` and the composer's
  own `section-blueprint.md` — both already inside their phases' fences. It does **not**
  re-expose `voice-profile.md` or any voice-canon entry to Phase 3.
- **Held at `watch`, not recommended-apply:** count reached 3 but every instance was accepted
  as the better trade-off and none gated a loop. This mirrors the deliberate hold on
  `redundancy-bloat`. Promote to `recommended-apply` if a future band-break is *not* accepted
  (i.e. the conflict forces a genuine quality regression or an extra iteration), or if the
  companion STRUCT-005 lands and the joint-spec is wanted to keep its splits in-band.

## Regression expectation

Documentation-only change (two Markdown reference files; no script, no banned list, no
fixture input). After applying:

- `python .claude/skills/_shared/scripts/test_gates.py` — all tests pass, unchanged.
- `python meta/regression.py` — `clean-baseline` and `figure-orphan` fixtures produce
  identical verdicts (no gate reads these files). **Confirmed green at the 2026-06-20
  pre-application baseline** (`REGRESSION: PASS`, 32/32 gate tests, both fixtures ok).
- Success criterion for the next run: when a mobile-ceiling split yields a short paragraph,
  the editor records it as a sanctioned cadence beat by rule (no ad-hoc adjudication), and no
  `revision-induced-band-break` finding is filed as an open conflict.
