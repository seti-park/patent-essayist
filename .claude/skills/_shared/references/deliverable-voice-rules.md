# Deliverable Voice Rules (checkable — Phase 2 author, Phase 3 judge)

> **Status: SCAFFOLD + canon target.** The *checkable* rules for the published essay's
> voice. Loaded by Phase 2 (to write) and Phase 3 (to judge — this is the voice file the
> editor is allowed to see, since it is rules not persona). Several rules here are also
> enforced mechanically by `_shared/scripts/` so they survive every revision. Replace the
> starter rules with the user's canon; keep the IDs so the gate scripts stay aligned.

## Hard rules (also enforced by gate scripts)

- **No em-dash** (`—`) in body or title outside verbatim quotes. *(gate: `EMDASH-001`)*
- **Citations resolve:** every `[dddd]` anchor and figure ref must exist in the Phase-1
  hand-off. *(gates: `ANCHOR-001`, `FIGREF-001`)*
- **No banned AI-tell terms/constructions** outside quotes. *(gate: `BANNED-001`; the list
  lives in `anti-ai-writing.md` → `scripts/banned_terms.txt`)*
- **Sources block** present and well-formed. *(gates: `SOURCES-00x`)*

## Soft rules (Phase-3 judgment + structure gate warnings)

- Paragraph length within the format's band; no bold/bullet overuse; no reflexive
  rule-of-three triads. *(gate warns: `STRUCT-00x`)*
- Active voice by default; concrete nouns/verbs over nominalizations.
- One idea per sentence; vary sentence length deliberately.

<!-- PORT: drop the user's deliverable-voice-rules canon here. Keep any rule that must be
     machine-checked expressed concretely so it can be wired to a gate script. -->
