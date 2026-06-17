---
proposal_id: 2026-06-17-sources-author-form-rule
created: 2026-06-17T00:00:00Z
status: recommended-apply
lever: reference-edit
goal: "4a"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/x-articles-format-en.md (Sources per-item citation format — multi-author author form under-/mis-specified)
recurrence_count: 3
confidence: medium
triggering_findings:
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: sources-entry-template-drift
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: sources-entry-template-drift
  - essay_id: 045-sandisk-hbf-flash-training, iter: 1, pattern_tag: sources-entry-template-drift
---

## Problem

The `# Sources` Papers-entry **author form** is decided improvised at compose time and a
Pass-6 editor has corrected it in **2 of the last 3 essays** (goal 4a, structure/format).
The recurrence is now 3 records ≥ RECUR_THRESHOLD(3):

- Run 2 (US20260158546A1), iter 1 — `sources-entry-template-drift` (medium, F12): Papers
  entries bibliographically inconsistent, varying author forms (surname-only). Fixed by
  hand-normalizing all four entries.
- Run 2, iter 2 — residual `sources-entry-template-drift` (low): author-form polish still
  open ("Strakosova, et al.", "He, et al." surname-only; three-author ASME entry without
  "et al."). Recorded as template polish, "not worth a loop iteration."
- Run 045 (SanDisk HBF), iter 1 — `sources-entry-template-drift` (medium, Pass-6D): the
  LoRA entry read "Hu, et al. (2021)." — surname-only, omitting the lead author's first
  name. Editor rule cited as "Last1, First1, et al."; the paper has 7+ authors led by
  Edward J. Hu. Fixed in iter 2 to "Hu, Edward J., et al. (2021). … arXiv:2106.09685."

Root cause is in the reference itself. `essay-en-composer/references/x-articles-format-en.md`
line 58 states the multi-author rule as **"*First, et al.* 형식"** and the worked example on
line 60 is surname-led (**"Li, Marzook, et al."**). So the artifact both (a) describes the
form ambiguously ("First, et al." can be read as *given-name-first* or as *first-author*) and
(b) shows no "Last, First" example — which is exactly the form the Pass-6D editor enforces.
The composer is faithfully following an under-specified/mis-stated rule; no deterministic gate
sees author-name formatting (`gate_sources` checks the h1, the 5-label enum, and all-or-nothing
subgrouping only), so the defect surfaces only at Pass 6, costing editorial work each run.

This class adjoins two same-owner-artifact siblings already on record but is the only one that
has reached the bar: run-1 `source-pointer-style-drift` (1, inline pointer style, same file)
and the broader `sources-entry-template-drift` history. Distinct-instance count here is 3
across 2 essays, so `confidence: medium` (consistent recurrence, modest blast radius), not
high.

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/x-articles-format-en.md`** — make the
Papers author form explicit and unambiguous (the "Last1, First1, et al." form the editor
enforces), and fix the worked example so it models the lead author's given name.

```diff
 ### Sources per-item citation format

 각 source 의 citation format.

-**Papers (academic)**. 저자 4명 이상 시 *First, et al.* 형식 (full author list 안 함). citation 의 simplicity + Chicago / IEEE style 의 정합.
+**Papers (academic)**. Lead author 는 `Last, First` (성, 이름 — full first name 또는 initial),
+그 뒤 저자 다수 시 `, et al.`. 즉 multi-author 는 **`Last1, First1, et al.`** 형식
+(surname-only 금지 — Pass-6D 에서 "Hu, et al." → "Hu, Edward J., et al." 교정 사례). 저자
+2–3 명은 전원 표기 가능. citation 의 simplicity + Chicago / IEEE style 의 정합.
+
+- Author list 를 신뢰 가능하게 확인 불가한 경우(예: authorless venue): 저자 invent/copy 금지,
+  title 로 entry 를 시작하고 venue/URL 로 traceability 확보 (fact-introduction 회피).

-예 — *Li, Marzook, et al. (2024). "Title". Journal Name, Vol(Issue).*
+예 — *Li, Marzook J., et al. (2024). "Title". Journal Name, Vol(Issue). URL/arXiv-id.*
```

## Why this lever

- The failure is a **compose-stage procedural gap** and `x-articles-format-en.md` is the
  exact artifact the composer consults to format Sources entries — fixing the rule lands
  where the defect is produced. Both editors' corrections were applications of this one rule.
- **Not gate-promotion.** Author-name correctness ("Hu" → "Edward J. Hu") requires knowing
  the paper's real lead author; a regex cannot verify that without false positives, and the
  authorless-venue carve-out is a judgment, not a literal. `gate_sources` deliberately stops
  at the enum/subgroup structure. (`source-pointer-style-drift`, an adjacent same-file class,
  is also reference-shaped, not gate-shaped.)
- **Not rubric-tuning.** Nothing about the threshold or posture is mis-calibrated; the rule
  text is simply wrong/ambiguous. Cheapest durable fix is correcting the rule.
- One lever only: the inline `source-pointer-style-drift` polish (same file) is **not**
  bundled here — it is a separate class still at 1 record (watch).

## Regression expectation

- Documentation-only change (no script touched): `python .claude/skills/_shared/scripts/test_gates.py`
  and `python meta/regression.py` stay green unchanged; `gate_sources` behavior is unaffected
  (it never inspected author names).
- Success criterion for the next paper-citing run: zero Pass-6D author-form findings — the
  composer emits `Last1, First1, et al.` directly, and the authorless-venue case opens with
  its title without inventing authors. A fourth *distinct* author-form correction after
  applying would move this class toward `ineffective-patch` accounting (CASCADE_CAP watch:
  same owner artifact, 0 patches applied so far).
