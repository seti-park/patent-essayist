# Deliverable Voice Rules (checkable — Phase 2 author, Phase 3 judge)

> **Status: SCAFFOLD + canon target.** The *checkable* rules for the published essay's
> voice. Loaded by Phase 2 (to write) and Phase 3 (to judge — this is the voice file the
> editor is allowed to see, since it is rules not persona). Several rules here are also
> enforced mechanically by `_shared/scripts/` so they survive every revision. Replace the
> starter rules with the user's canon; keep the IDs so the gate scripts stay aligned.

## Hard rules (also enforced by gate scripts)

- **No em-dash** (`—`) in body or title outside verbatim quotes. *(gate: `EMDASH-001`)*
- **Citations resolve + well-formed:** every `[dddd]` anchor is 4-digit zero-padded and
  exists in the Phase-1 hand-off; every figure ref resolves. *(gates: `ANCHOR-001`,
  `ANCHOR-002`, `FIGREF-001`)*
- **No orphan figures:** every figure Phase 1 selected is actually used in the draft.
  *(gate: `FIGUSE-001`)*
- **No banned AI-tell terms/constructions** outside quotes. *(gate: `BANNED-001`; the list
  lives in `anti-ai-writing.md` → `scripts/banned_terms.txt`)*
- **No reader-instruction / essay-self-reference posturing** — "read it the way…", "everything
  below…", "the rest of this essay", "watch how…". Insight, not stage directions. *(gate:
  `META-001`; functional scope disclaimers like "this essay does not adjudicate X" are exempt.)*
- **Sources block** present exactly once as `# Sources` (h1), 5-label enum, all-or-nothing
  `##` subgrouping. *(gates: `SOURCES-001/002/003`)*

## Soft rules (Phase-3 judgment + structure gate warnings)

- Paragraph length within the format's band; no bold/bullet overuse; no reflexive
  rule-of-three triads. *(gate warns: `STRUCT-00x`)*
- Active voice by default; concrete nouns/verbs over nominalizations.
- One idea per sentence; vary sentence length deliberately.
- **Lead altitude (BLUF):** in analytical/diligence mode, paragraph 1 states the verdict, not
  a deferred question. **Section headers are claims** (a header-only skim = the argument).
  *(editorial pass-6 / pass-7.)*
- **Jargon as signposts, not deep-dives:** keep the short domain term-of-art the target reader
  scans for (e.g. "Section 101", "Alice"); cut the doctrinal explanation only a specialist
  needs. *(editorial pass-5; class `jargon-overdepth`.)*
- **No stub sections; no gross verbatim repetition; tickers as `$`-cashtags.** *(gate warns:
  `STUB-001`, `DUPE-001`, `CASH-001`.)*

<!-- PORT: drop the user's deliverable-voice-rules canon here. Keep any rule that must be
     machine-checked expressed concretely so it can be wired to a gate script. -->
