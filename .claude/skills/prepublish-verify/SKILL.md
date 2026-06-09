---
name: prepublish-verify
description: "Independent pre-publish verification stage for the patent-essay pipeline. Runs ONCE after the Compose↔Edit inner loop promotes essay-final.md, before archival/publication. Two parallel sub-checks by a FRESH reviewer (not the editor that just passed the draft): (1) an adversarial RED-TEAM close-read of the final essay against the full patent + grounding, and (2) LIVE external SOURCE-RESOLUTION of every body claim and # Sources entry against the web. Emits handoff/03-edit/verification-log.md (same severity model + YAML schema as editorial-review) with an overall_assessment. PROPOSE-ONLY — never auto-fixes. Use when essay-final.md exists and is about to be archived/published. NOT for: the per-round editorial review (Phase 3 editorial-review), thesis design, prose composition, auto-fix."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# prepublish-verify

The pipeline's **publication threshold**. The Compose↔Edit inner loop already cleared the
deterministic gates and the editorial 6-pass; this stage is the *independent second set of
eyes* that runs once, at the threshold, before the essay is archived and published.

```
handoff/03-edit/essay-final.md                       (the accepted draft)
    + input/patent.md                                (FULL patent — grounding source of truth)
    + handoff/01-design/{invention-summary.md, thesis-spine.md, fact-check-log.md}
    + handoff/02-compose/thesis-trace.md             (claim→anchor map; investor body has no inline anchors)
    + Knowledge: _shared/references/{scoring-rubric.md, anti-ai-writing.md, deliverable-voice-rules.md}
                 editorial-review/references/external-fact-verification.md  (5-tier hierarchy + status — SoT)
    → 2 parallel sub-checks (red-team ∥ source-resolution)
    → handoff/03-edit/verification-log.md  (structured YAML + overall_assessment)
    → orchestrator decides: low → surgical fix / surface; medium+ → revise loop (+1)
```

## Why this exists (not a duplicate of editorial Pass 3)

`external-fact-verification.md` states the principle directly: *"The final trust check belongs
at the publication threshold."* Editorial Pass-3 owns **internal grounding** every round
(anchor↔Quotable verbatim, paraphrase mutation, causality) and only **flags** external claims
as verify-candidates. The **authoritative live external check runs here, once** — concentrated
where it belongs, by a reviewer that did not just pass the draft. This removes the per-round
web cost from the inner loop and adds genuine independence.

## Independence (CRITICAL — this is the whole value)

- Run in a **fresh forked context**. Form judgment from the **patent + essay**, not from the
  editor's conclusions.
- **Do NOT load `edit-log.md` as authority.** You may read it only to *deconflict* (avoid
  re-reporting an identical low nit the editor already surfaced) — never to inherit its verdict.
  A clean editorial pass is exactly the thing you are stress-testing.
- **Full patent access** (unlike the editor, you read `input/patent.md` in full) — you need it
  to catch invented numbers and mechanism misstatements.
- **Voice fence (same as editor):** do NOT load `voice-profile.md` / `caption-roles.md`. Voice
  judgment here is limited to `anti-ai-writing.md` (raise-then-disavow / insinuation) +
  `deliverable-voice-rules.md`.

## The two sub-checks (run in parallel)

### A. Red-team — adversarial close-read
You are a skeptical domain expert + a hard-nosed reader. Try to break the essay against the
patent and its grounding. Full checklist + severity mapping + audience branch in
`references/red-team-checklist.md`. Core targets:
- **Patent-attributed numbers** — the patent may disclose *no* quantitative figures; flag any
  body phrasing that implies the patent *proved* a number. (high)
- **Mechanism fidelity** — the essay must describe the actual invention (retained vs removed
  parts, replaced member vs whole). (high if wrong)
- **Scope conflation** — must not blur the patent with adjacent programs/products. (high/medium)
- **Overclaim / boosterism** — the thesis must be earned by the patent's content. (medium)
- **Insinuation** — raise-then-disavow / manufactured drama. (medium; per anti-ai-writing)
- **Ungrounded load-bearing claim** — spot-check each against `thesis-trace.md` / invention
  summary / patent. (high if load-bearing and ungrounded)
- **Finishability** (audience=investor) — does a non-expert get through it; does each section earn its place.

### B. Source-resolution — live external verification
For every external (non-patent) claim in the body **and every `# Sources` entry**:
resolve it against the web, assign a tier and a verification status, recommend a fix.
Procedure in `references/source-resolution.md`. The **5-tier hierarchy and the
verified / partially-verified / unverifiable / contradicted vocabulary are reused verbatim
from `editorial-review/references/external-fact-verification.md`** (single SoT — do not redefine).

## No-web fallback (soft / hard)

Mirror `thesis-architect/references/context-research.md`. If web access is unavailable:
- **soft (default):** still run the red-team offline against the patent; mark every
  source-resolution item `unverifiable — no web` as a **warn**, set `web_access: offline` in the
  log, and **do not block** publication on the source layer. Surface the gap.
- **hard:** halt and report (only when the run explicitly demands web-confirmed sourcing).

## Output — `handoff/03-edit/verification-log.md`

Reuse the editorial **feedback-format** YAML and the **same severity→assessment table** (see
`editorial-review/references/feedback-format.md`). Schema in
`handoff-template/03-edit/verification-log.md`. Every sub-pass must appear, with `"no findings"`
when clean. Compute `overall_assessment` (pass / revise-recommended / revise-required) by the
identical mapping (critical/high → revise-required; medium → revise-recommended; low → pass).

This stage is **propose-only**. It does not edit the essay. The orchestrator applies the policy:
**low** → apply the surgical fix (citation title, scoped wording) directly or surface it;
**medium+** → feed the findings to `essay-en-composer` in revision mode (same revision-input
contract as `edit-log.md`), re-run gates + editorial, then **re-verify** (capped at +1 round).

## Standalone use

`/prepublish-verify` can run on its own against an existing `handoff/03-edit/essay-final.md`
(+ patent + design handoff) to produce a `verification-log.md` without the full pipeline.
