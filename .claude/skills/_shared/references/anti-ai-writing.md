# Anti-AI-Writing (the strip canon — Phase 2 strip, Phase 3 check)

> **Status: SCAFFOLD + canon target.** SETI's own anti-AI-writing rules are the **source of
> truth** for AI-tell removal (the vendored humanizer/ai-check skills are secondary and
> optional). The banned-term portion of this canon is mirrored into
> `_shared/scripts/banned_terms.txt`, which `gate_banned.py` enforces mechanically.
> Replace the starter list with the user's canon, then re-sync `banned_terms.txt`.

## Banned words / constructions (starter — port the canon, then sync the script)

- Filler verbs/adjectives: *delve, leverage, robust, seamless, underscore, tapestry,
  realm, navigate (figurative), crucial, pivotal, game-changer, unlock, foster.*
- Constructions: *"not just X, but Y"*, *"it's worth noting"*, *"in today's …"*,
  reflexive rule-of-three triads, bold-word-then-colon definition lines.

## The strip pipeline (Phase 2 step 5)

1. Draft in voice (Phase 2 with the full voice stack).
2. Strip residual AI tells per this canon → clean `publication.md`.
3. The deterministic `gate_banned.py` is the mechanical backstop; the canon is the intent.

## Keeping script + canon in sync

When this canon's banned list changes, update `_shared/scripts/banned_terms.txt`
(literals one per line; `re:` prefix for regex). The script is provisional until the canon
lands.

<!-- PORT: drop the user's anti-ai-writing canon here. -->
