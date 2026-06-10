---
name: editorial-review
description: "Mandatory 6-pass review on every essay draft from Phase 2 Compose. Six passes (voice canon + anti-AI compliance, redundancy + compression, claim adequacy + fact verification + paraphrase mutation, logical alignment + causality, reader perspective + paragraph readability, lead/conclusion + format compliance). Structured YAML feedback — NOT auto-fix. Posture-aware (aggressive / measured / conservative). Use when essay-draft.md lands in handoff/02-compose/ (Phase 3 Edit). NOT for: format-only verification (folded into Pass 6), pool admission (deprecated), auto-fix, voice training corpus admission."
---

# editorial-review

Phase 3 Edit's mandatory inferential review. Six passes. Structured feedback YAML output.

```
handoff/02-compose/essay-draft.md
    + handoff/01-design/{thesis-spine.md, invention-summary.md, fact-check-log.md}
    + input/patent.md (read directly for Pass 3 verbatim checks)
    + references: _shared/references/{deliverable-voice-rules.md, anti-ai-writing.md}
                  + essay-en-composer/references/x-articles-format-en.md (Pass 6 format SoT)
    → 6 passes
    → handoff/03-edit/edit-log.md (structured YAML feedback)
    → findings applied (orchestrated: composer revision mode / standalone: SETI by hand)
    → handoff/03-edit/essay-final.md
```

## Output role

2nd redundancy. SETI editorial intuition = 1st instance.

- Findings supply input for the revise decision. This skill NEVER auto-fixes the draft itself.
- **Who applies the findings depends on how the run was started.** Orchestrated runs
  (`/patent-essay`): the orchestrator feeds this skill's findings to `essay-en-composer`
  in revision mode (`essay-en-composer/references/revision-mode.md`) and, once the loop
  accepts a round, promotes the accepted draft to `handoff/03-edit/essay-final.md` —
  no human in the loop unless SETI intervenes. Standalone runs (`/editorial-review`
  invoked directly): SETI applies findings by hand and produces `essay-final.md`.
- SETI's combined sensitivity (voice + audience perception + adversarial reader + charm/honesty + direct preference) operates outside single-pass inferential reach. This skill cannot substitute for SETI catches.
- Conflict resolution: SETI catch overrides skill output — in both run types.

## Voice fencing (CRITICAL)

Phase 3 does NOT load `voice-profile.md` or `caption-roles.md` (avoid voice drift bias from re-exposure to canon). Voice compliance is verified against `_shared/references/deliverable-voice-rules.md` mechanical rules + `_shared/references/anti-ai-writing.md` banned-pattern list only. This fence is enforced by this SKILL.md (see also the voice-fencing table in `CLAUDE.md`; the meta-loop preserves it via `meta/attribution-table.md` routing).

## Posture lens

3-tier: aggressive / measured (default) / conservative. The same finding receives different severity classification under different posture. See `references/posture-lens.md`.

## When to invoke

After `essay-en-composer` produces `handoff/02-compose/essay-draft.md`. Mandatory on every essay. No skip option. Rationale: v1 historical leaks (paraphrase mutation in published draft) reached publication only because editorial-review was skipped.

## Six passes (v2 locked order)

1. **Voice canon + anti-AI compliance** — voice canon pattern adherence (cadence, structure inheritance) + banned-pattern grep (em-dash count = 0, "delve" / "navigate" / "leverage" etc.). See `references/pass-1-voice-anti-ai.md`.
2. **Redundancy + compression** — claim repetition + sentence tightening + paragraph word-count earn check. See `references/pass-2-redundancy.md`.
3. **Claim adequacy + fact verification + paraphrase mutation** — every `[XXXX]` cite verified against `invention-summary.md` Quotable spans verbatim; external claims verified against `fact-check-log.md` + `input/patent.md`; paraphrase variations classified (intentional restatement / accidental drift / substantive change). See `references/pass-3-fact-paraphrase.md`.
4. **Logical alignment + causality** — 인과 vs 상관 vs 우연 distinction, thesis-section 정렬 check against `thesis-spine.md` spine→section trace. See `references/pass-4-logic-causality.md`.
5. **Reader perspective + paragraph readability** — engagement curve, stake clarity, mobile rendering line count. See `references/pass-5-reader-perspective.md`.
6. **Lead/conclusion + format compliance** — hook anchor to thesis, frame closure, `# Sources` 5-category enum check, "First, et al." format, em-dash count, `[xxxx]` format check, banned-words grep (covers the deterministic-gate absorption). See `references/pass-6-lead-conclusion-format.md`.

Causal claim quality is a recurring cross-pass concern (Pass 3 + Pass 5). See `references/causal-reasoning.md`.

## Output format

Structured YAML feedback. See `references/feedback-format.md` for full schema.

Minimal example:

```yaml
review_id: <essay-id>-editorial-review-1
draft_source: handoff/02-compose/essay-draft.md
posture_applied: measured
overall_assessment: revise-required

findings:
  - pass: pass-3-fact-paraphrase
    location: §3, sentence with "complements"
    severity: high
    severity_under_default_posture: high
    finding: |
      Source verbatim is "supplements" (invention-summary.md Quote anchor q-0024-1).
      Prose uses "complements". Accidental drift.
    recommendation: |
      Re-anchor to source verbatim.
```

Feedback gets written to `handoff/03-edit/edit-log.md`. Findings are then applied per the run type (orchestrated: composer revision mode; standalone: SETI) → `handoff/03-edit/essay-final.md`.

## Pre/post conditions

Pre:
- `handoff/02-compose/essay-draft.md` present.
- `handoff/01-design/{thesis-spine.md, invention-summary.md, fact-check-log.md}` accessible.
- `input/patent.md` readable for Pass 3 verbatim verification.
- References loaded: `_shared/references/deliverable-voice-rules.md`, `_shared/references/anti-ai-writing.md`, `essay-en-composer/references/x-articles-format-en.md`, `_shared/references/working-dialogue-voice.md`. (NOT `voice-profile.md` / `caption-roles.md` — voice fencing.)
- Posture confirmed in opening response.

Post:
- `handoff/03-edit/edit-log.md` emitted with one entry per finding.
- Each finding has specific draft location + severity + recommendation.
- `overall_assessment` set per severity rules in `references/feedback-format.md`.
- Auto-fix NOT performed by this skill (findings are applied downstream: composer revision mode in orchestrated runs, SETI by hand in standalone runs).

## Coupling

- ← `essay-en-composer` (`essay-draft.md` input)
- ← `thesis-architect` (handoff/01-design/* for cross-checks)
- → `patent-essay` orchestrator (feeds findings to composer revision mode in the loop) / SETI (applies findings in standalone runs) → `essay-final.md`

## Out of scope

- Auto-fix (SETI decides).
- Pool admission (v1 `pool-admission` skill — dropped).
- Strategic adversarial audit (v1 `strategic-audit` skill — dropped).
- Cross-essay coherence sensing (v1 `cross-essay-coherence-sensor` — dropped).
- Voice canon corpus admission (v1 voice-profile-seti admit step — Phase 3 doesn't touch the canon).

## References

- `references/pass-1-voice-anti-ai.md` — voice canon adherence + anti-AI banned-pattern grep, severity calibration per posture.
- `references/pass-2-redundancy.md` — claim repetition, sentence tightening, paragraph word-count earn.
- `references/pass-3-fact-paraphrase.md` — verbatim verification against Quotable spans + fact-check-log + patent.md; paraphrase mutation classification.
- `references/pass-4-logic-causality.md` — thesis-section 정렬 + 인과/상관/우연 distinction.
- `references/pass-5-reader-perspective.md` — engagement curve, stake clarity, mobile rendering.
- `references/pass-6-lead-conclusion-format.md` — hook/closure + mechanical compliance (em-dash, [xxxx] format, banned-words, Sources 5-category enum, "First, et al.").
- `references/posture-lens.md` — 3-tier posture + per-pass posture sensitivity table.
- `references/external-fact-verification.md` — Pass 3 sub-pass detail, 5-tier source authority hierarchy.
- `references/causal-reasoning.md` — causal claim quality checks (Pass 3 + Pass 5).
- `references/feedback-format.md` — output YAML schema + severity criteria.
