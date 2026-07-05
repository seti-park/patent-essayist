# Implementation notes — running decision log

A human-readable memory file for decisions made while editing shipped essays or the
pipeline outside a full run. Newest entry first. Each entry records: what was observed,
the root-cause analysis, what was changed and NOT changed (with reasons), and what the
next run should do differently. The machine-readable twins live in
`meta/findings-ledger.jsonl` (pattern_tag rows) and `meta/improvement-proposals/`;
this file is where the reasoning survives in full sentences.

---

## 2026-07-05 — etched-us20240378175-r2: procedure hijacked the reader's attention (v5 → v6)

### The observation (publisher read, post-publication)

The shipped essay front-loaded patent PROCEDURE — the 3-year examination, the RCE, fees,
liens — and buried the TECHNOLOGY. Predicted reader behavior: engage with the lead,
glaze during the prosecution material, skim or abandon the tech sections that were the
actual payload. Meanwhile `owner-briefing.md` and `promo/promo-pack.md` read fine.
So the defect was essay-body-specific, not a facts problem.

### Root-cause analysis (why the essay went to 삼천포 while the briefing/promo didn't)

1. **The verdict frame became the narrative frame (design stage).** The edition contract
   correctly said a pending application can't support a fence-strength verdict, so the
   verdict must be about what the document IS plus how it's treated (collateral,
   continued prosecution). Phase 1 then let that VERDICT frame set the STORY structure:
   the one-line spine ends on "a bet the company keeps paying to convert into an asset",
   the Q7 hook anchors on prosecution status, and the spine→section trace placed
   prosecution/money at the lead (¶2–3) AND §5 AND the closing. Procedure became the
   plot; the invention became the middle.
2. **A per-item budget eroded through echoes (compose + edit stages).** The user
   decision in essay-context was explicit: "prosecution status: exactly ONE label
   sentence, no battle narrative." The letter of the rule held (one full-detail status
   sentence), but the MOTIF metastasized: "expensive to keep alive", "paid at every
   step", "an RCE is, in substance, a fee paid to keep arguing", "the spending is
   repeated", "keeps paying" — each individually grounded and reviewable, none a status
   label per se, so every pass approved every instance. Nothing counts the aggregate.
3. **No attention-budget instrument exists.** gate_surface checks the title length, the
   first body sentence, and a defensive-open lexicon in the first two sentences — point
   checks at the very top. The cold reader checks stop-points — but a paper-trail hook IS
   hooky, so the lead passed; the failure was the procedural pile-up in ¶2–3 and §5,
   which sits between every existing check. Nothing measures time-to-technology or the
   procedural share of prose.
4. **Why briefing/promo survived:** fixed schemas. The owner briefing gives technology
   and status separate numbered slots; the promo formats (≤280자 / ~300 words) force
   selection of the punchiest content, which is the tech + the date beat. Long-form is
   the only artifact where attention allocation is unconstrained — so it is the artifact
   that needs the budget rule.

### Decisions taken (and not taken)

- **Restructured tech-first, verdict intact.** New title ("Etched's First Patent Filing
  Asks to Delete the Memory Switch") and new lead: the switch-deletion idea + its stated
  effect ([0043]/[0016]/[0044]/[0045]) FIRST, discovery beat second, compact two-sided
  call third. §5 compressed to: the ONE mandated label sentence + full-strength steelman
  + record-of-behavior + one merged lien paragraph + the family note.
- **Cut, with reasons:** the RCE explainer paragraph (procedure lecture beyond the label
  budget), the grant-to-lien three-day timing paragraph (inference-labeled procedure
  trivia), the compiler-applications aside, the repeated-spending motif (kept once, in
  the closing signature line, where it earns its place).
- **Kept, deliberately:** the steelman at full strength (contract-required, and it is a
  THIS-application objection); both liens (both-or-neither evidence rule); all three
  protected signature lines byte-intact; the firm closing unchanged.
- **Verified:** 14/14 gates PASS with zero findings (warns included) after the edit;
  publication.md re-stripped (2,906 words); posting-checklist updated.
- **Not done:** no re-run of the inner loop (this is the human-post-accept channel; the
  deltas are in `revision-notes.md` and normalized to the ledger as
  `procedure-overweight-lead`, goal 5).

### What the next run should do differently

1. **Lead order rule (design + compose):** for verdict editions, the lead answers
   "what does it do and what does that change" BEFORE "what does it cost / where does it
   stand". The discovery/status beat may frame, never dominate: procedure gets at most
   one clause in the lead beyond the required call.
2. **Motif budget, not just sentence budget:** when a brief says "exactly one label
   sentence", treat restatements-in-other-words (spend/fee/keep-alive language) as
   drawing on the same budget. The composer's revision mode and pass-6 should count the
   motif across the whole essay.
3. **Structural home for procedure:** prosecution/finance material lives in ONE pricing
   section (plus the closing's verdict), never distributed across lead + body + closing.
4. **Candidate instrument (proposed, not built):** a warn-only surface check for the
   procedural share of the lead (lexicon: rejection, RCE, examiner, fee, lien, security
   interest, docket...) and/or a time-to-first-tech-anchor measure. See
   `meta/improvement-proposals/2026-07-05-procedure-attention-budget.md`.
5. **Schema-envy heuristic:** when the briefing/promo read better than the essay, suspect
   attention allocation, not facts — the fixed-schema artifacts are the control group.
