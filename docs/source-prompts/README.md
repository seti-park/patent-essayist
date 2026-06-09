# Source prompts — original claude.ai assets (preserved)

The patent-essay system was originally run as **four separate claude.ai Projects**, each
with its own Instructions + Knowledge + skill. Those originals are the reference baseline
for this Claude Code conversion. Preserve them here, verbatim, by phase:

| Dir | Original claude.ai Project | Ports into |
|-----|----------------------------|-----------|
| `01-design/`  | Phase 1 Design (voice-off)   | `.claude/skills/thesis-architect/` |
| `02-compose/` | Phase 2 Compose (voice-on)   | `.claude/skills/essay-en-composer/` + `voice-canon-lookup/` |
| `03-edit/`    | Phase 3 Edit (voice-fenced)  | `.claude/skills/editorial-review/` |

(Phase 4 Promote and Layer-1 figure cleaning are out of scope for this conversion.)

## How porting works

Each target skill's `SKILL.md` has a `<!-- PORTED PROMPT -->` marker showing exactly where
to drop the original skill body. The Knowledge files map to `_shared/references/` canon
(voice-profile, deliverable-voice-rules, anti-ai-writing, x-article-format, caption-roles,
working-dialogue-voice, writing-textbook). Keep each stage's **output contract** intact so
the on-disk hand-off keeps parsing.

Drop the original Instruction + Knowledge text into the matching phase dir here as the
canonical record; the live system reads from `.claude/skills/`, not from this folder.
