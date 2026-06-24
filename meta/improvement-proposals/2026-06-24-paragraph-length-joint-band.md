---
proposal_id: 2026-06-24-paragraph-length-joint-band
created: 2026-06-24T00:00:00Z
status: recommended-apply
lever: reference-edit
goal: "3"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/section-blueprint.md (no paragraph-length plan reconciling the pass-5C mobile-line ceiling with the deliverable-voice 3-7-sentence band)
recurrence_count: 3
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: 029-agility-torso-protrusion, iter: 2, pattern_tag: revision-induced-band-break
---

## Problem

Two paragraph-length criteria are specified in **separate references and conflict at the
margins**, so a revision that fixes one silently breaks the other:

- the **mobile-line ceiling** — "> 8 mobile lines is a failure," words/12 — lives in
  `editorial-review/references/pass-5-reader-perspective.md` §5C (a Phase-3 *editor* rule);
- the **3-7-sentence paragraph band** — "Paragraph length within the format's band" — lives
  in `_shared/references/deliverable-voice-rules.md` (Soft rules) and is enforced by pass-1.

Neither is stated to the *composer at plan time*. `section-blueprint.md` has a `word_target`
**per section** but no paragraph-length field at all, so the composer cannot pre-reconcile the
two, and the conflict surfaces only after a revision:

- **Run 1** (`deleted-dome`, iter 2, ED2-02): the iter-1 mobile-wall splits produced two
  2-sentence closing paragraphs and left SS3 P2 at 2 sentences — under the 3-7 band. Recorded:
  "the 8-line mobile ceiling and the 3-7 sentence band conflict at the margins."
- **Run 2** (`both-and-steel`, iter 2): the F11 mobile-wall splits created paragraphs below the
  band (§1p3 2 sentences; two consecutive single-sentence §3 enumerations); rejoining §3 would
  yield 124w, back over the ceiling — "exact recurrence of run-1 ED2-02."
- **Run 3** (`029-agility-torso-protrusion`, iter 2): the formatting-only mobile-wall fix again
  produced sub-band paragraphs (the one-line "That is the human box-hug, written as a claim."
  landing; P10 ~38w/~3.2 lines), accepted by the editor as intentional cadence beats.

In all three essays the editor accepted the sub-band result as deliberate and shippable — but
spent review effort re-adjudicating it each round, and each round the two criteria were traded
off by hand. The `gate-structure-word-wall` proposal (2026-06-11, `recommended-apply`)
**explicitly named this as the deferred companion**: *"A companion `reference-edit` (a
paragraph word band in `section-blueprint.md`, jointly specified with the deliverable-voice
3-7-sentence band) is deliberately NOT bundled here (one lever per proposal); it is the natural
follow-up if `revision-induced-band-break` (currently 2 records, 2/2 essays) reaches the bar."*

It has now reached the bar: **3 records / 3 essays** = RECUR_THRESHOLD, every occurrence the
identical mechanism → `recommended-apply`, confidence high.

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/section-blueprint.md`**

Add a paragraph-length item to the per-section field list (after the `word_target` bullet):

```diff
 - `section_id` — kebab-case, unique (e.g. `1-lead`, `2-architecture`, `4-closing`).
 - `word_target` — integer. Composer writes within ±20%.
+- `paragraph_plan` — per section, keep each body paragraph inside the JOINT band below.
+  Both criteria are checked at plan time so a later mobile-readability split cannot satisfy
+  one by breaking the other.
 - `voice_canon_reference` — list of `voice-canon-lookup` entry_ids (at least 1).
```

and add a new subsection immediately before "## Patent-fact discipline":

```markdown
## Paragraph-length joint band (mobile ceiling × sentence band)

Two criteria govern paragraph length and they are reconciled HERE, at plan time, because
they live in different downstream references and conflict at the margins (ledger:
`revision-induced-band-break`, 3/3 essays):

- **Mobile-line ceiling** (Phase-3 pass-5C): words ÷ 12 must be ≤ 8 mobile lines; the
  target is ≤ 5. A paragraph over ~96 words (≈ 8 lines) is a wall and must be split. The
  warn-only `STRUCT-005` word-wall gate (~>110w) backstops this mechanically.
- **Sentence band** (deliverable-voice soft rule, pass-1): body paragraphs sit in a 3-7
  sentence band.

These conflict because a long-sentence paragraph can be in-band on sentences yet over the
mobile ceiling; splitting it for mobile then drops one fragment under the sentence band.
Reconcile while drafting, not in revision:

1. **Plan paragraphs near the middle of both bands** (≈ 60-90 words, 3-5 sentences). A
   paragraph planned there rarely needs a mobile split and stays in the sentence band.
2. **If a single cohesive idea must exceed ~96 words**, plan its split seam up front (at a
   sentence boundary that yields two readable beats), so the split is authored, not a later
   patch that strands a 1-2-sentence fragment.
3. **Sanctioned exception — the intentional landing.** A deliberate one- or two-sentence
   paragraph used as an aphoristic landing or cadence beat is allowed BELOW the 3-7 band and
   is NOT a band violation; mark it in `structural_note` as an intended landing. (This
   encodes the editor's accepted-as-deliberate call in all three triggering runs — e.g.
   "That is the human box-hug, written as a claim." — so revision need not re-litigate it.)
   Do not split FOR mobile down to a fragment that is neither in-band nor a marked landing.

Net rule for revision guidance (Phase-3 and the composer's own revision pass): a mobile-wall
split must land each resulting paragraph either inside the 3-7 sentence band OR as a marked
intentional landing — never as an unmarked sub-band fragment created solely to satisfy the
mobile ceiling.
```

## Why this lever

- The defect is a **compose-stage planning gap** (the two criteria are never reconciled before
  drafting), and `section-blueprint.md` is exactly the artifact where per-section length is
  planned — the rule lands where the trade-off is actually made. This is the companion the
  `gate-structure-word-wall` proposal named and deferred to this trigger; the two are
  complementary (the gate *warns* on >110w walls at compose time; this reference tells the
  composer how to split them without breaking the sentence band), one lever each.
- **Not gate-promotion:** "is this 2-sentence paragraph a legitimate landing or an accidental
  sub-band fragment?" is a judgment a regex cannot make (the editor judged it deliberate in all
  three runs). A hard sentence-floor gate would false-fail every sanctioned landing.
- **Not rubric-tuning:** no threshold is mis-calibrated; the bands are individually correct.
  The gap is that they were never specified *jointly* to the stage that must satisfy both.
- **Voice fence:** untouched. The edit is to the Phase-2 composer's own `section-blueprint.md`;
  it references the existing pass-5C and deliverable-voice bands but exposes no `voice-profile`
  or canon entry to Phase 3. (No Phase-3 voice finding is being routed anywhere — this is a
  goal-3 readability/structure finding owned by Compose.)

## Regression expectation

Documentation-only change (one reference file; no script, no `banned_terms.txt`, no fixture
input touched).

- `python .claude/skills/_shared/scripts/test_gates.py` — all tests pass, unchanged.
- `python meta/regression.py` — `clean-baseline` and `figure-orphan` fixtures produce
  identical verdicts (no gate reads `section-blueprint.md`).
- Observable success criterion for the next run: `thesis-trace.md` shows a per-section
  `paragraph_plan`; any sub-band paragraph in the final draft is marked as an intended landing
  in its `structural_note`; zero new `revision-induced-band-break` records where a mobile split
  stranded an *unmarked* sub-band fragment. A fourth occurrence after applying flips the class
  toward `ineffective-patch` / CASCADE accounting.
