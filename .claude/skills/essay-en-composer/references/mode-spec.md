# Mode specification

Referenced by essay-en-composer SKILL.md Step 1 (mode selection) and Step 5 (composition rhythm). Defines the two-dimensional mode space, default behavior, mid-pipeline shifts, and per-mode composition rhythm.

## Two dimensions

essay-en-composer operates along two orthogonal dimensions, both selectable at invocation.

### Dimension 1: Mode category

| Mode | Behavior |
|---|---|
| **walkthrough** (default) | Section-by-section composition. SETI mid-session editorial intervention welcome. Catches at sentence or section level for voice, clarity, thesis alignment, audience perception. |
| **strict-execution** | Pure prose expansion from Blueprint. No mid-session intervention. Plan ⊥ Execute strict reading. |
| **pair** | Interactive at each sentence. SETI plus Claude step-by-step dialogue. |

A fourth category, **revision**, exists for orchestrated Compose↔Edit loop rounds only — trigger, scope rule and output contract in `revision-mode.md`.

### Dimension 2: Posture (mode spectrum)

| Posture | Behavior |
|---|---|
| **aggressive** | Thesis-altering catches welcome. Framing changes possible. Voice bold experimentation. |
| **measured** (default) | Voice and clarity polish plus minor thesis adjustment. Major framing preserved. |
| **conservative** | Voice and clarity polish only. Thesis plus framing preserved. Factual accuracy emphasized. |

### Default combination

When mode is not specified at invocation: **walkthrough + measured**.

## Mode selection logic (SKILL Step 1)

- Invocation specifies mode and posture → adopt both
- Invocation specifies only mode → adopt mode and apply default posture (measured)
- Invocation specifies neither → adopt walkthrough plus measured
- Orchestrated runs (`/patent-essay`) → strict-execution plus measured for round 1, revision mode for loop rounds

Confirm mode and posture in the opening response before any composition work.

Example opening:

> "Beginning essay-en-composer in walkthrough mode plus measured posture. Section-by-section composition; please catch any voice, clarity, or thesis concerns mid-session."

## Composition rhythm per mode (SKILL Step 5)

Per-mode composition behavior during Step 5 (compose sections) of the SKILL.md process:

- **walkthrough**: compose section → present → SETI elicit catch → refine if catch → next section. Each section is a checkpoint.
- **strict-execution**: compose all sections → emit full draft → no mid-session checkpoint.
- **pair**: compose sentence → SETI elicit → refine → next sentence. Sentence-level checkpoint.

## Catch scope by posture (walkthrough only)

Mid-session catches in walkthrough mode have posture-bounded scope.

**Measured (default) catches bounded to:**

- Voice and clarity polish (voice canon compliance)
- Sentence-level refinement
- Section transition adjustments
- Minor thesis hint refinement (within blueprint thesis)

**Always out of catch scope** (require blueprint revision — redo the section blueprint (SKILL Step 3), or return to Phase 1 `thesis-architect` if the spine itself is implicated):

- Fact introduction (new facts beyond `invention-summary.md` Quotable spans + `fact-check-log.md`)
- Structural deviation (section reorder, add, remove)
- Major thesis change (`thesis-spine.md` spine modification)

Aggressive posture extends the bounded scope to allow framing variation. Conservative posture narrows the bounded scope to voice and clarity polish only.

## Mid-pipeline mode shift

SETI may explicitly shift mode mid-essay. The nature of an emerging catch may also trigger an implicit shift suggestion:

- Thesis-altering catch in measured-posture walkthrough → propose aggressive shift
- Thesis-altering catch in conservative-posture walkthrough → propose either upgrade to measured or aggressive, or return to Phase 1 `thesis-architect` (thesis-altering catches are spine-level)
- Strict-execution session reveals blueprint coverage incomplete → propose shift to walkthrough or redo the section blueprint (SKILL Step 3)

Surface the shift proposal explicitly. SETI decides: shift, abandon attempt, redo the blueprint (Step 3), or return to Phase 1 `thesis-architect` for spine-level changes.
