---
name: patent-essay
description: >
  Orchestrator / entry point for the patent-essay system. Given an English patent (+
  cleaned figures), runs Phase 1 Design → Phase 2 Compose → Phase 3 Edit, automating the
  hand-off between stages on disk and running the Compose↔Edit quality loop until the
  draft clears the deterministic gates and the editorial assessment (or max iterations),
  then runs an autonomous post-acceptance self-audit and pipeline-retro to grow the system.
  Use when asked to turn a patent into a finished English essay end to end.
argument-hint: "[patent path | text | number]  [--threshold pass|revise-recommended] [--max-iter N] [--mode essay|wire]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, WebFetch, WebSearch
---

# Patent Essay — Orchestrator

Drive the three-phase pipeline and the Compose↔Edit quality loop, then the post-acceptance
self-audit and the meta-loop. The patent to process is named in `$ARGUMENTS` (a path under
`input/`, raw text, or a patent number/URL).

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
- `--self-audit on|off` — run the post-acceptance fresh-context self-audit after the inner loop
  passes. **Default: `on`** at `--threshold pass`. `off` skips it (fast / wire runs).
- `--max-selfaudit-iter N` — max self-audit re-audit rounds (loop-until-dry cap). **Default: 3.**

## Pipeline

### Phase 1 — Design  (skill: `thesis-architect`, voice-off)
Invoke `thesis-architect` on the patent. It writes the design hand-off to
`handoff/01-design/` (invention-summary, thesis-spine, thesis-candidates, figure-selection,
figure-rationale, fact-check-log, search-log, phase2-handoff-notes). Also write a plain
`handoff/01-design/figures-index.txt` (one figure number per line, from the cleaned
`input/figures/`) for the gates.

**Thesis selection (auto):** read `thesis-candidates.md` and auto-pick the recommended /
single-spine candidate. Surface the candidate list in one short line so the user can
override; if `$ARGUMENTS` names a specific thesis, use that. Confirm the choice is locked in
`thesis-spine.md`.

### Phase 2 — Compose  (skill: `essay-en-composer`, voice-on)
Invoke `essay-en-composer`. It reads `handoff/01-design/` (it does **not** read the raw
patent) and writes `handoff/02-compose/` (essay-draft, publication, figures-rationale,
thesis-trace). It calls `voice-canon-lookup` internally per section.

### Phase 3 — Edit  (skill: `editorial-review`, voice-fenced)
Invoke `editorial-review`. It reads `handoff/02-compose/` + Phase-1 cross-check anchors,
runs the 6-pass review (including the pass-3 coverage sub-check for goal 2), and writes
`handoff/03-edit/edit-log.md` with an `overall_assessment`. It does **not** load
`voice-profile` / `caption-roles`.

### Deterministic gates (mechanical, run every round before trusting the edit-log)

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figures-index.txt \
  --figure-selection handoff/01-design/figure-selection.md \
  --mode <essay|wire> --json
```

Any gate **fail** (exit code 1) — including `FIGUSE-001` (orphan figure) — is a hard fail
regardless of the edit-log.

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

## Self-audit (post-acceptance, auto)

After the inner loop promotes `essay-final.md`, run a **fresh-context adversarial self-audit**
before archiving (`--self-audit on`, default). This is the autonomous complement to the human
revision-delta channel: it catches the editorial + grounding blind-spots that survive a `pass`.
It can only **add** findings — the inner-loop bar and the grounding/goal-2 hard-gates stay in force.

Per round:
1. **Spawn ≥2 reviewers in separate forked contexts** (no commitment to the draft) on
   `essay-final.md` + the raw patent, each running the
   `editorial-review/references/pass-7-adversarial-reader.md` checklist plus grounding
   spot-checks: claim-scope against the actual claims, every anchor against its cited paragraph.
   Read as the two personas (impatient investor, skeptical pro-subject reader). Each finding is a
   yes/no with a quoted span or `ABSENT`, never a holistic rating.
2. **Multi-vote.** Apply a finding when the reviewers agree (≥ majority) OR when one reviewer's
   grounding finding is verifiable against the source. Log split / taste-only / over-edit findings
   to `revision-notes.md` as considered-not-applied, and do **not** force them in — the rubric
   gates OVERREACH, not OVER-HEDGE.
3. **Fix at the source.** When a finding traces upstream (e.g. an anchor mislabeled in
   `invention-summary.md`), correct the Phase-1 artifact too, so a recompose can't reintroduce it.
4. **Re-run the gates** and log every applied edit to `handoff/03-edit/revision-notes.md` as a
   `## delta` block (schema: `handoff-template/03-edit/revision-notes.md`).

**Loop until dry:** repeat until a round adds no `high`/`medium` and no agreed-applicable finding,
bounded by `--max-selfaudit-iter` (default 3). Then normalize the deltas to the ledger as the
autonomous origin:

```
python meta/normalize_revision_notes.py \
  --notes handoff/03-edit/revision-notes.md --essay-id <essay-id> \
  --origin self-post-accept --append meta/findings-ledger.jsonl
```

`origin: self-post-accept` keeps these distinct from `inner-loop` ("a pass should have caught it")
and `human-post-accept` ("only a human caught it"). The acceptance set is defined in
`scoring-rubric.md` (Layer 3) and is enforceable as a `/goal` (see below).

## Archive + meta-loop (after the inner loop)

1. **Archive** the run to `runs/<essay-id>/`: copy `edit-log.md`, the final
   `run_gates.py --json` output as `gate-result.json`, and write `score-history.md`.
2. **Meta-loop (skill: `pipeline-retro`, propose-only):** invoke `pipeline-retro` with the
   run's `edit-log.md` + `gate-result.json`. It normalizes the inner-loop findings **and** the
   self-audit's `revision-notes.md` deltas into `meta/findings-ledger.jsonl` (keyed by goal +
   owner artifact via the matrix; self-audit deltas carry `origin: self-post-accept`), and when a
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

For the full autonomous bar, make the post-acceptance self-audit mandatory rather than the
auto-default:

```
/goal the patent-essay run is self-audited: after the inner loop returns pass with all gates green, a fresh-context adversarial pass (>=2 reviewers, pass-7 personas, separate context) returns no unresolved high or medium finding, the grounding hard-gate holds, and a second blind pass confirms convergence
```
