---
proposal_id: 2026-06-11-gate-structure-word-wall
created: 2026-06-11T16:30:00Z
updated: 2026-06-20T17:40:00Z
status: recommended-apply
lever: gate-promotion
goal: "3"
root_cause_stage: compose
root_cause_artifact: _shared/scripts/gate_structure.py (STRUCT-001 counts sentences, not words) + essay-en-composer/references/section-blueprint.md (no word-length band)
recurrence_count: 8
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 2, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 3, pattern_tag: mobile-paragraph-wall
---

> **2026-06-20 refresh (run `274-processor-on-nand-moat`).** Strongest class in the
> ledger: now **8 records across 3/3 essays**, and run 3 escalated it to **high** for
> the first time (the §2 P9 8-sentence/~130w paragraph, a Pass-2C absolute-rule hit that
> co-fires the word-wall heuristic). Run 3 also showed the class is **revision-induced**:
> fixing the round-1 Pass-3B high by re-grounding §4 landed 150 words in one paragraph
> (round-2 sole medium), i.e. a revision *created* a new wall a compose-time STRUCT-005
> word warn would also have caught. Already `recommended-apply`; this run only hardens it.

## Problem

Mobile wall-of-text paragraphs recur in **2 of 2 essays** at `medium` severity (goal 3,
reader understanding), and are structurally invisible to the gate that exists to catch them:
`STRUCT-001` counts **sentences** (max 8), so a 4–6-sentence paragraph of long sentences
sails through while rendering as >8 mobile lines.

- Run 1, iter 1 (medium): three walls — 124w, 120w, 115w (words/12 > 8-line heuristic);
  the run-1 editor already recommended "a word-count warn heuristic (~>110w per paragraph)
  to gate_structure".
- Run 1, iter 2 (low): two carried marginals at the heuristic edge (107w, 99w).
- Run 2, iter 1 (medium): two walls — §1p2 129w, §2p3 136w; again gate-invisible, again
  cost revision work.
- Run 2, iter 2 (low): three retained 96w+ paragraphs needed explicit editorial
  adjudication (114w / 99w / 111w stands accepted with recorded reasons).
- **Run 3, iter 1 (HIGH + medium):** §2 P9 ran to 8 sentences / ~130w (Pass-2C absolute
  rule, the first **high** of this class — and 130w also trips the proposed ~110w word
  heuristic); plus ~11 body paragraphs over the ~8-line mobile heuristic (Pass-5C medium),
  the worst at ~179w and ~166w, all gate-invisible to STRUCT-001.
- **Run 3, iter 2 (medium, revision-induced):** the round-1 Pass-3B fix (re-grounding §4 on
  the two independent claims) landed 150 words in one paragraph — the round-2 sole medium and
  the lone thing standing between the draft and PASS. A compose-time STRUCT-005 warn would
  have flagged it at 150w > 110w, before it cost the round-2 review and the round-3 split.
- **Run 3, iter 3 (resolved):** cleared by the round-2-prescribed split.

Record count is now **8 ≥ RECUR_THRESHOLD(3)**, cross-essay **3/3**, severity now reaches
**high**, mechanically checkable with zero hard-fail risk (`gate_structure` is warn-only by
design) → `recommended-apply`. Run 3 adds two new arguments: the class can be **high**
(so a compose-time warn has real value, not just polish), and it can be **revision-induced**
(so the warn must run on every Compose pass, including revisions — which it does).

## Proposed change (exact diff)

**File 1: `.claude/skills/_shared/scripts/gate_structure.py`**

```diff
 GATE_ID = "structure"
 MAX_SENTENCES_PER_PARA = 8       # STRUCT-001 threshold
+MAX_WORDS_PER_PARA = 110         # STRUCT-005 threshold (~8 mobile lines; ed. heuristic words/12)
 MAX_BOLD_PER_100_WORDS = 2       # STRUCT-002 threshold (spans per 100 words)
```

and, immediately after the STRUCT-001 loop (`findings.append({... "STRUCT-001" ...})` block):

```diff
     # STRUCT-001: long paragraphs
     for start, text in paragraphs:
         n = _count_sentences(text)
         if n > MAX_SENTENCES_PER_PARA:
             findings.append({
                 "check_id": "STRUCT-001",
                 "severity": "warn",
                 "message": "paragraph has %d sentences (max %d)" % (n, MAX_SENTENCES_PER_PARA),
                 "location": "line %d" % start,
             })
+
+    # STRUCT-005: mobile wall-of-text by WORD count. Sentence counting (STRUCT-001)
+    # misses 4-6-sentence paragraphs of long sentences that render >8 mobile lines
+    # (recurring pass-5 medium in 2/2 essays; see mobile-paragraph-wall in the ledger).
+    for start, text in paragraphs:
+        n_words = len(re.findall(r"\S+", text))
+        if n_words > MAX_WORDS_PER_PARA:
+            findings.append({
+                "check_id": "STRUCT-005",
+                "severity": "warn",
+                "message": "paragraph has %d words (max %d; ~8 mobile lines at 12-14 w/line)"
+                           % (n_words, MAX_WORDS_PER_PARA),
+                "location": "line %d" % start,
+            })
```

Also update the module docstring check list:

```diff
   STRUCT-004: rule-of-three — sentences with an "A, B, and C" triad of short items.
+  STRUCT-005: a body paragraph with more than MAX_WORDS_PER_PARA words (mobile wall).
```

**File 2: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestStructure`:

```diff
     def test_bullet_overuse_warns(self):
         draft = "Intro line.\n- a\n- b\n- c\n- d\n"
         r = gate_structure.check(draft, {})
         self.assertTrue(_has(r, "STRUCT-003"))
+
+    def test_word_wall_warns_even_with_few_sentences(self):
+        # 2 sentences x 56 words = 112 words: invisible to STRUCT-001, caught by STRUCT-005.
+        para = " ".join(["word"] * 56) + ". " + " ".join(["word"] * 56) + "."
+        r = gate_structure.check(para + "\n", {})
+        self.assertTrue(r["passed"])  # warn only, never a hard fail
+        self.assertTrue(_has(r, "STRUCT-005"))
+        self.assertFalse(_has(r, "STRUCT-001"))
+
+    def test_normal_paragraph_no_word_wall_warning(self):
+        r = gate_structure.check("Short paragraph. Two sentences only.\n", {})
+        self.assertFalse(_has(r, "STRUCT-005"))
```

**File 3: `.claude/skills/_shared/references/scoring-rubric.md`** — keep the gate table in
sync (one cell):

```diff
-| `structure`  | (none — all warn) | `STRUCT-001..004` | 3, 4a |
+| `structure`  | (none — all warn) | `STRUCT-001..005` | 3, 4a |
```

## Why this lever

- The defect is purely mechanical (word arithmetic) and the editor has now performed the
  identical arithmetic by hand in **seven** review rounds across three essays; that is exactly
  what gate promotion is for. The run-1 editorial recommendation named this promotion verbatim.
- Zero false-positive *blast radius*: `gate_structure` is warn-only by design, so STRUCT-005
  can never fail a round; it feeds pass-5 exactly where the manual arithmetic feeds today.
  Note: run 2's accepted final retains three adjudicated 96–114w paragraphs; STRUCT-005
  would warn on the two >110w ones — that is intended behavior (warn → pass-5 adjudication,
  which already recorded those stands as accepted).
- A companion `reference-edit` (a paragraph word band in `section-blueprint.md`, jointly
  specified with the deliverable-voice 3–7-sentence band) is deliberately NOT bundled here
  (one lever per proposal); it is the natural follow-up to `revision-induced-band-break`,
  which **as of run 3 has reached 3 records / 3 essays** and now has its own proposal
  (`2026-06-20-paragraph-length-joint-spec.md`, filed `watch`) — splits that satisfy the
  mobile ceiling by breaking the sentence band. The two are complementary: STRUCT-005 warns
  on walls; the joint-spec keeps the fix for a wall from creating a band underrun.

## Regression expectation

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing tests pass unchanged
  (STRUCT-005 is additive, warn-only) + the 2 new cases pass.
- `python meta/regression.py`: `clean-baseline` fixture must still report `gate_pass: true`
  with **no STRUCT-005 finding** (its paragraphs are short — verify; if any fixture
  paragraph exceeds 110 words the fixture's `must_not_contain_check_ids` should not list
  STRUCT-005 since warns don't affect `gate_pass`); `figure-orphan` fixture must still fail
  on `FIGUSE-001` only. **Confirmed green at the pre-application baseline 2026-06-20**
  (`REGRESSION: PASS`, 32/32 gate tests, both fixtures ok).
- Success criterion for the next run: zero pass-5 `medium` wall findings; walls surface as
  STRUCT-005 warns at compose time instead of costing an editorial round.
