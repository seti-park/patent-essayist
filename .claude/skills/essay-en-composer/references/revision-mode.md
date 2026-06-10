# Revision mode (Compose↔Edit loop rounds)

A fourth mode category, alongside walkthrough / strict-execution / pair
(`mode-spec.md`). Used only inside the orchestrated quality loop: the composer enters
revision mode when the invocation supplies a Phase-3 edit-log (plus failing gate
`check_id`s) instead of asking for a fresh draft. First-round composition never uses it.

This file is the contract the orchestrator (`patent-essay` SKILL) and the scoring rubric
point at when they say "feed the findings back to `essay-en-composer` in revision mode".

## Trigger / inputs

- `handoff/03-edit/edit-log.md` — the 6-pass findings (YAML), each with `location`,
  `severity`, `finding`, `recommendation`.
- The failing gate `check_id`s from `run_gates.py --json` (the orchestrator passes them
  along with the edit-log).
- The existing `handoff/02-compose/` bundle — the draft is revised **in place**.
- The Phase-1 handoff (`handoff/01-design/`) stays available read-only for re-anchoring
  (Quotable spans, fact-check-log). `input/patent.md` remains off-limits (fencing).

## Scope rule (what may change)

1. **Targeted edits** — only the sections/paragraphs named in a finding's `location`
   field may be rewritten.
2. **Mechanical global fixes** — violations with a deterministic `check_id`
   (`EMDASH-001`, `BANNED-001`, `ANCHOR-002`, `SOURCES-00x`, `FIGUSE-001`) may be fixed
   wherever they occur: the gates located them precisely, so the fix is not a rewrite.
3. **Everything else stays verbatim.** No opportunistic rewriting of untouched
   sections — the loop must converge, not churn.

## Constraints (unchanged from first-round composition)

- The Plan ⊥ Execute boundary holds (`execution-boundary.md`): no facts beyond
  `invention-summary.md` Quotable spans + `fact-check-log.md` externals. A finding whose
  fix would require a new fact is escalated (below), never improvised.
- Per-section `voice_canon_reference` anchors are preserved, unless the finding targets
  voice/cadence in that section — then re-invoke `voice-canon-lookup` for that section
  before rewriting.
- Posture is inherited from the round-1 invocation (default: measured).

## Escalation (stop, don't improvise)

Findings owned by Phase 1 Design stop the revision instead of being patched in prose —
the same rule as "spine gaps stop composition rather than provoke improvisation":

- pass-4 thesis/section misalignment that would need a different spine→section trace,
- pass-3 coverage `high` that needs a Quotable span the handoff never extracted,
- grounding/adversarial gaps in the spine itself.

On escalation: append a `> Revision note` block to `handoff/02-compose/thesis-trace.md`
naming the blocking finding id(s), and return **"needs Phase-1 revision"** to the
orchestrator. The orchestrator (or SETI) decides whether to re-open `thesis-architect`.

## Outputs (same contract, version bumped)

Re-emit the full `handoff/02-compose/` bundle:

- `essay-draft.md` — frontmatter `draft_version: N+1`, `mode_used: revision`.
- `publication.md` — regenerated via `strip-pipeline.md` (never stale).
- `figures-rationale.md` / `thesis-trace.md` — updated only if placement or trace
  changed; when they do, append a `> Revision note` block citing the triggering
  finding ids.

## Done definition for a round

Every finding in the edit-log is either (a) fixed, (b) explicitly declined with a
one-line reason recorded in a `thesis-trace.md` `> Revision note`, or (c) escalated.
Silent skips are not allowed — the orchestrator re-runs the gates and
`editorial-review` immediately after, so an unaddressed finding just burns an
iteration.
