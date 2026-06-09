---
name: editorial-review
description: >
  Phase 3 (Edit) of the patent-essay pipeline. Run a 6-pass editorial review over the
  composed draft plus the deterministic gate scripts, producing a YAML edit-log with a
  0–100 score and prioritized findings. Voice-fenced (no voice-profile / caption-roles).
  In the orchestrator's auto loop, findings feed back into Phase 2. Use after
  essay-en-composer, or as step 3 of the orchestrator.
argument-hint: "[optional: posture measured|sharp]"
context: fork
agent: general-purpose
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Editorial Review — Phase 3 (Edit)

Review the composed draft and decide whether it clears the bar. This phase is
**voice-fenced**: it owns *editorial* decisions only. To prevent editor voice drift it
does **not** load `voice-profile.md` or `caption-roles.md`; voice compliance is judged
against `deliverable-voice-rules.md` + `anti-ai-writing.md` and the deterministic gate
scripts.

## Inputs

- `handoff/02-compose/` — `essay-draft.md` (gates run on this), `publication.md`,
  `figures-rationale.md`, `thesis-trace.md`.
- Phase-1 cross-check anchors: `handoff/01-design/thesis-spine.md`,
  `invention-summary.md`, `fact-check-log.md`.
- `input/patent.md` — for **Pass 3** verbatim verification of fact-checked claims.
- Posture from `$ARGUMENTS` (`measured` default, or `sharp`).

## References this phase loads (fenced subset)

- `_shared/references/working-dialogue-voice.md`
- `_shared/references/deliverable-voice-rules.md`
- `_shared/references/anti-ai-writing.md`
- `_shared/references/scoring-rubric.md`
- It must **not** load `voice-profile.md` or `caption-roles.md` (fencing).

## Deterministic gates (mechanical, run first)

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figure-selection.md --json
```

Record every `check_id`. Any gate **fail** is a hard fail (anchor-chain, em-dash, Sources,
banned terms). These are machine checks — do not re-litigate them by eye.

## 6-pass review (PI-derived; replace with the ported skill body)

1. **Thesis adherence** — does every section trace to `thesis-spine.md`?
2. **Grounding / anchor-chain** — every `[dddd]` and figure ref resolves (cross-check the
   gate result + `invention-summary.md`).
3. **Verbatim fact-check** — claims in `fact-check-log.md` verified against
   `input/patent.md` word-for-word.
4. **Voice compliance** — against `deliverable-voice-rules.md` + `anti-ai-writing.md`
   (NOT voice-profile).
5. **Structure / format** — `x-article-format` conformance, paragraph/figure flow.
6. **So-what / close** — specific, falsifiable takeaway, not filler.

<!-- PORTED PROMPT: replace the 6-pass procedure above with the user's existing Phase-3
     Edit skill body (editorial-review). Keep the gate invocation and the output contract
     so the orchestrator loop can parse the score and findings. -->

## Scoring

Per `scoring-rubric.md`: a 0–100 qualitative score, the grounding hard-gate, and the
combination rule (`gates pass AND score ≥ threshold`). The optional vendored `ai-check`
(`_shared/vendor/ai-check/SKILL.md`) may be run as a **secondary** AI-tell cross-check
feeding the voice dimension — it is not the source of truth (the canon is).

## Output contract — write `handoff/03-edit/edit-log.md` (YAML)

```yaml
gates:        # mirror of run_gates.py
  passed: true|false
  failing_check_ids: [ ... ]
passes:       # the 6 passes
  - id: thesis_adherence
    score: 0-100
    findings: [ { id, severity, where, fix } ]
  # ... the other five
score: NN              # overall 0-100 editorial score
grounding_gate: pass|fail
verdict: PASS|FAIL     # PASS ⇔ gates.passed AND score >= threshold AND grounding_gate==pass
revision_actions:      # only when FAIL — top, prioritized, fed verbatim to Phase 2
  - ...
```

On PASS, also copy the accepted publication copy to `handoff/03-edit/essay-final.md`.
`revision_actions` are what the orchestrator feeds back into `essay-en-composer` in
revision mode.
