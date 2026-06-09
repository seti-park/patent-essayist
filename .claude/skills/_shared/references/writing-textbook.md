# Writing Textbook — English Patent-Essay Structure Rules

> **Status: SCAFFOLD.** These are starter structural rules derived from established
> argumentative/expository writing frameworks. Refine them with your own writing
> textbook material. `essay-structure` reads this file to build the article outline.

## What a "patent essay" is here

A focused English article that takes a single patent (or patent family), derives a
**hypothesis/thesis** about its significance (technical, competitive, or market angle),
and argues it for an informed-but-non-specialist reader. Not a patent summary — an essay
with a point of view, grounded in the patent's claims and disclosure.

## Required structure

1. **Hook + Thesis (1 short paragraph)**
   - Open with a concrete tension, surprise, or stakes drawn from the patent.
   - State the thesis (the derived hypothesis) explicitly in one sentence.

2. **Grounding (1–2 paragraphs)**
   - What the patent actually claims/discloses, in plain language. Cite claim numbers
     or figures where it sharpens the point. No jargon dumps.

3. **Argument body (2–4 sections)**
   - Each section = one supporting sub-claim that advances the thesis.
   - Pattern per section: claim → evidence from the patent → implication.
   - Order sections by logical dependency, not by patent layout.

4. **Counterpoint / limits (1 paragraph)**
   - Honest treatment of what the patent does *not* establish, prior-art tension, or
     where the hypothesis could fail. Strengthens credibility.

5. **So-what close (1 paragraph)**
   - Return to the thesis; state the consequence if it holds. No "the future is bright"
     filler — a specific, falsifiable takeaway.

## Structural rules (enforced by `essay-structure`)

- One thesis, stated once up front and echoed once at the close.
- Every body section must trace back to the thesis; cut sections that don't.
- Claims must be anchored to specific patent content (claim #, figure, passage), not
  vibes.
- Target length: 600–1,100 words unless the orchestrator overrides.
- Outline output format: a nested list with section headers + the sub-claim and the
  specific patent evidence each section will use.

## Anti-patterns to reject at the structure stage

- Listicle structure ("5 ways this patent…") unless explicitly requested.
- Section sprawl: more than 4 body sections usually means the thesis is unfocused.
- Burying the thesis below the grounding section.
- Symmetric "on one hand / on the other hand" with no actual position.
