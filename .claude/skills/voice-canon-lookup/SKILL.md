---
name: voice-canon-lookup
description: >
  Internal helper for Phase 2 (essay-en-composer). Given a specific writing "move" (open a
  section, hand off to a figure, state a claim, close), return the exact voice-canon rule
  that governs it, pulled from the deliverable-voice canon. Used by the composer per
  section; not meant to be invoked directly by the user.
argument-hint: "[the writing move you're about to make]"
allowed-tools: Read, Grep, Glob
---

# Voice Canon Lookup (Phase 2 internal helper)

The composer calls this per section to avoid loading the entire voice stack into every
drafting step and to keep voice application consistent. Given a **move**, return the
governing rule(s) verbatim from the canon, with a one-line application note.

## How it works

1. Identify the move (e.g. *section opener*, *figure hand-off*, *evidence/claim line*,
   *counterpoint*, *close*, *caption*).
2. Look up the relevant rule(s) in:
   - `_shared/references/voice-profile.md`
   - `_shared/references/deliverable-voice-rules.md`
   - `_shared/references/x-article-format.md`
   - `_shared/references/caption-roles.md` (for figure/caption moves)
   - `_shared/references/anti-ai-writing.md` (what to avoid for this move)
3. Return: the exact rule text + a one-line "apply it here like this" note.

<!-- PORTED PROMPT: replace with the user's existing voice-canon-lookup skill body. Keep
     it read-only over the canon so it stays a pure lookup, not a second author. -->

## Output

- **MOVE** — the move being made.
- **RULE(S)** — verbatim from the canon, with the source file noted.
- **APPLY** — one line on how it lands in this section.

This helper never writes files and never overrides the composer's structure; it only
surfaces the canon.
