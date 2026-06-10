# Deliverable Voice Rules (checkable — Phase 2 author, Phase 3 judge)

> **Status: starter rules in effect; grown incrementally.** The *checkable* rules for the
> published essay's voice. Loaded by Phase 2 (to write) and Phase 3 (to judge — this is the
> voice file the editor is allowed to see, since it is rules not persona). Several rules
> here are also enforced mechanically by `_shared/scripts/` so they survive every revision.
> Growth policy (SETI's choice): after each finished essay, rules worth keeping are added
> here via `pipeline-retro` reference-edit proposals — no big-bang canon replacement. Keep
> rule wording concrete (machine-checkable where possible) and keep the gate IDs aligned.

## Hard rules (also enforced by gate scripts)

- **No em-dash** (`—`) in body or title outside verbatim quotes. *(gate: `EMDASH-001`)*
- **Citations resolve + well-formed:** every `[dddd]` anchor is 4-digit zero-padded and
  exists in the Phase-1 hand-off; every figure ref resolves. *(gates: `ANCHOR-001`,
  `ANCHOR-002`, `FIGREF-001`)*
- **No orphan figures:** every figure Phase 1 selected is actually used in the draft.
  *(gate: `FIGUSE-001`)*
- **No banned AI-tell terms/constructions** outside quotes. *(gate: `BANNED-001`; the list
  lives in `anti-ai-writing.md` → `scripts/banned_terms.txt`)*
- **Sources block** present exactly once as `# Sources` (h1), 5-label enum, all-or-nothing
  `##` subgrouping. *(gates: `SOURCES-001/002/003`)*

## Soft rules (Phase-3 judgment + structure gate warnings)

- Paragraph length within the format's band; no bold/bullet overuse; no reflexive
  rule-of-three triads. *(gate warns: `STRUCT-00x`)*
- Active voice by default; concrete nouns/verbs over nominalizations.
- One idea per sentence; vary sentence length deliberately.

<!-- Grown per essay via pipeline-retro proposals (reference-edit lever). Keep any rule
     that must be machine-checked expressed concretely so it can be wired to a gate. -->
