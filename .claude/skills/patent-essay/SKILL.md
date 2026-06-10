---
name: patent-essay
description: >
  Orchestrator / entry point for the patent-essay system. Given an English patent (+
  cleaned figures), runs Phase 1 Design → Phase 2 Compose → Phase 3 Edit, automating the
  hand-off between stages on disk and running the Compose↔Edit quality loop until the
  draft clears the deterministic gates and the editorial assessment (or max iterations),
  then runs pipeline-retro to grow the system. Use when asked to turn a patent into a
  finished English essay end to end.
argument-hint: "[patent path | text | number]  [--threshold pass|revise-recommended] [--max-iter N] [--mode essay|wire] [--audience deep|investor] [--verify auto|off]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, WebFetch, WebSearch
---

# Patent Essay — Orchestrator

Drive the three-phase pipeline and the Compose↔Edit quality loop, then the meta-loop. The
patent to process is named in `$ARGUMENTS` (a path under `input/`, raw text, or a patent
number/URL).

This orchestrator owns the **loop policy**; each phase's domain work lives in its own skill.
Stages pass data through **handoff directories on disk**, not chat copy-paste. The four
north-star goals and the goal→check matrix live in `_shared/references/scoring-rubric.md`.

## Inputs (provided per run)

- `input/patent.md` — the English patent (or whatever path `$ARGUMENTS` names).
- `input/figures/fig-NN.png` — pre-cleaned figures (Layer-1 cleaning is out of scope).
- `input/essay-context.md` — optional extra framing/context for the run.

## Parameters

- `--threshold pass|revise-recommended` — minimum editorial `overall_assessment` the loop
  accepts. **Default: `pass`** (clean). `revise-recommended` accepts medium-only findings for
  faster turnaround; it may never be relaxed to `revise-required`. See `scoring-rubric.md`.
- `--max-iter N` — max Compose↔Edit revision rounds. **Default: 4.**
- `--mode essay|wire` — deliverable mode. **Default: essay.**
- `--audience deep|investor` — reader altitude. **Default: `deep`** (patent-fidelity: inline
  `[xxxx]` anchors + reference numbers, full mechanism walkthrough, ~2000+ words). `investor`
  is the accessible altitude for the investor/analyst reader: stake-first, mechanism
  compressed, body under the word ceiling with **no inline anchors / reference numbers**, but
  it **keeps** scannable subheadings, the `# Sources` block, and figures (plain captions). The
  P1 thesis frame, P2 mode, P3 reader profile, and the `gate_readability` gate all shift with
  it. Grounding rigor is unchanged underneath (anchors live in `thesis-trace.md`). See
  `_shared/references/scoring-rubric.md` §"Audience altitude".
- `--verify auto|off` — the independent pre-publish verification stage. **Default: `auto`** (runs
  once after the inner loop passes, before archival — a true publication gate). `off` skips it
  (backward-compatible / offline). See "Pre-publish verification" below.

## Pipeline

Pass `--audience` to every phase. On `investor` it changes the thesis frame (P1), the
compose mode (P2), the editorial reader profile (P3), and activates `gate_readability`.

### Phase 1 — Design  (skill: `thesis-architect`, voice-off)
Invoke `thesis-architect` on the patent **with the audience**. It writes the design hand-off
to `handoff/01-design/` (invention-summary, thesis-spine, thesis-candidates, figure-selection,
figure-rationale, fact-check-log, search-log, phase2-handoff-notes). Also write a plain
`handoff/01-design/figures-index.txt` (one figure token per line, from the cleaned
`input/figures/`) for the gates. On `investor`, the spine favors a forward-capability / market
hook and declares a `reader_stake`; figure-selection picks fewer figures by "helps a
non-expert understand" (see `thesis-architect/references/hook-patterns.md`).

**Thesis selection (auto):** read `thesis-candidates.md` and auto-pick the recommended /
single-spine candidate. Surface the candidate list in one short line so the user can
override; if `$ARGUMENTS` names a specific thesis, use that. Confirm the choice is locked in
`thesis-spine.md`.

### Phase 2 — Compose  (skill: `essay-en-composer`, voice-on)
Invoke `essay-en-composer` **with the audience**. It reads `handoff/01-design/` (it does
**not** read the raw patent) and writes `handoff/02-compose/` (essay-draft, publication,
figures-rationale, thesis-trace). It calls `voice-canon-lookup` internally per section. On
`investor` it uses the accessible blueprint (stake-first, mechanism compressed, word ceiling,
no inline anchors/reference numbers in the body — anchors recorded in `thesis-trace.md`, plain
figure captions); see `essay-en-composer/references/mode-spec.md`.

### Phase 3 — Edit  (skill: `editorial-review`, voice-fenced)
Invoke `editorial-review` **with the audience**. It reads `handoff/02-compose/` + Phase-1
cross-check anchors, runs the 6-pass review (including the pass-3 coverage sub-check for
goal 2), and writes `handoff/03-edit/edit-log.md` with an `overall_assessment`. It does
**not** load `voice-profile` / `caption-roles`. On `investor`, pass-5 judges against the
investor reader profile and verifies grounding via `thesis-trace.md` (the body has no inline
anchors); pass-2 runs the load-bearing audit.

### Deterministic gates (mechanical, run every round before trusting the edit-log)

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figures-index.txt \
  --figure-selection handoff/01-design/figure-selection.md \
  --thesis-spine handoff/01-design/thesis-spine.md \
  --thesis-trace handoff/02-compose/thesis-trace.md \
  --mode <essay|wire> --audience <deep|investor> --json
```

Passing `--thesis-spine` + `--thesis-trace` activates `gate_arc` (per-section length/structure
conformance against the spine's `## Arc budget`). It self-skips (`ARC-000`) if the spine carries
no arc budget, so older runs are unaffected.

Any gate **fail** (exit code 1) — including `FIGUSE-001` (orphan figure), and on `investor`
the readability `READAB-001/002` — is a hard fail regardless of the edit-log.

## Quality loop (inner, auto)

Round result combines the two layers:

- **gates** = pass/fail from `run_gates.py`.
- **assessment** = `overall_assessment` from `edit-log.md` (`pass` / `revise-recommended` /
  `revise-required`).

```
PASS  ⇔  gates all pass
         AND  assessment is acceptable per --threshold
         AND  grounding hard-gate not breached (no pass-3 high/critical, no gate_anchors fail)
         AND  goal-2 hard-gate not breached (no FIGUSE-001, no pass-3 coverage high)
         AND  goal-3 hard-gate not breached (investor only: no READAB-001/READAB-002)
```

While the round is **FAIL** and `iterations < max-iter`:
1. Feed the `edit-log.md` findings (+ failing gate `check_id`s) back to `essay-en-composer` in
   **revision mode** — it revises `handoff/02-compose/` in place.
2. Re-run the gates and re-invoke `editorial-review`.
3. Increment the counter.

Stop on PASS, or at `max-iter`. On stop, promote the accepted draft to
`handoff/03-edit/essay-final.md`.

Each phase's heavy work runs in its own forked context; keep only the structured hand-off
summaries in the main thread to stay within budget.

## Pre-publish verification  (skill: `prepublish-verify`, independent — runs once after the inner loop)

Skip this whole section if `--verify off`. Otherwise, once `essay-final.md` exists, invoke
`prepublish-verify` **with the audience** — a fresh, independent reviewer (NOT the editor that
just passed the draft). It runs two sub-checks **in parallel**:

- **red-team** — adversarial close-read of `essay-final.md` against the **full** `input/patent.md`
  + grounding (`thesis-trace.md`, `invention-summary.md`): invented/patent-attributed numbers,
  mechanism misstatement, scope conflation, overclaim, insinuation, ungrounded load-bearing claims,
  finishability.
- **source-resolution** — **live web** resolution of every external body claim + every `# Sources`
  entry (5-tier hierarchy + verification-status, reused from `external-fact-verification.md`).

It writes `handoff/03-edit/verification-log.md` with its own `overall_assessment` (same
severity→assessment table as the edit-log). It is **propose-only**. No web access → soft mode
(red-team runs offline; source items become non-blocking warns; `web_access: offline` recorded).

**Fold the result into the publish decision:**

```
PUBLISH-READY  ⇔  inner loop already PASS
                  AND verification overall_assessment acceptable per --threshold
                      (i.e. no critical/high; medium only if --threshold revise-recommended)
```

- **low findings** → the orchestrator applies the surgical fix directly (citation title, scoped
  wording) or surfaces it; publish-ready stands.
- **medium+ findings** → feed the verification findings to `essay-en-composer` in **revision mode**
  (same revision-input contract as `edit-log.md` findings), re-run the gates + `editorial-review`,
  re-promote `essay-final.md`, then **re-verify**. This is capped at **+1 verify-triggered round**
  (shared with `--max-iter`). If it still does not clear, ship the best round and state the
  remaining verification findings (same terminal behavior as the inner loop).

## Archive + meta-loop (after the inner loop)

1. **Archive** the run to `runs/<essay-id>/` (append `-investor` to the id for the investor
   altitude so a deep and an investor run of the same patent archive side by side): copy
   `edit-log.md`, the final `run_gates.py --json` output as `gate-result.json`, the
   `verification-log.md` (when `--verify` ran; also on the terminal "shipped with findings" path),
   and write `score-history.md` (include a "Pre-publish verification" section with the verify
   `overall_assessment` + any applied surgical fixes).
   - **Iteration snapshots (golden-set material).** For each revision round N, also copy the
     pre-revision and post-revision drafts to `runs/<essay-id>/iterations/iter-N-pre.md` and
     `iter-N-post.md` (the essay bodies live in gitignored `handoff/` and are otherwise
     overwritten each round). These before/after pairs — together with the `edit-log.md` finding
     that drove each change — are the raw material for `meta/golden-set/` (judge calibration,
     planned). Cheap to capture; do it on every run going forward. See `meta/golden-set/README.md`.
   - **Final essay + thesis-trace.** Also copy `essay-final.md` and
     `handoff/02-compose/thesis-trace.md` into the run archive: the final body is canon-harvest
     material (admission policy in `voice-canon-lookup/SKILL.md`), and the trace's
     `voice_canon_reference`s are the usage data the canon drift watch reads. (Both were being
     lost with gitignored `handoff/` before this.)
2. **Meta-loop (skill: `pipeline-retro`, propose-only):** invoke `pipeline-retro` with the
   run's `edit-log.md` + `gate-result.json` + `verification-log.md`. It normalizes findings into
   `meta/findings-ledger.jsonl` (keyed by goal + owner artifact via the matrix), and when a
   root-cause class recurs it writes an evidence-backed proposal to
   `meta/improvement-proposals/`. It **never** edits a skill — surface only the top proposal
   (if any) to the user in one line.

## Output

- The **final essay** (`handoff/03-edit/essay-final.md`, clean prose).
- A **SCORE HISTORY** table: iteration → `overall_assessment` → gate result (failing
  `check_id`s) → PASS/FAIL → one-line note.
- One line on any new `pipeline-retro` proposal awaiting human review.
- If it never cleared the bar: ship the **best round**, state the remaining findings.

## Optional: wrap with `/goal` as an outer safety net

The orchestrator's own loop already enforces the bar; `/goal` only adds an auto-resume
backstop if a run is interrupted before passing:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with overall_assessment == pass
```
