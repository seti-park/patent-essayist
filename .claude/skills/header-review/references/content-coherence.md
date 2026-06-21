# Pass 4 — Content coherence (does the header imply the essay?)

This is the **north-star pass** for the design system. The deliverable's whole
reason to exist (CONTRACT.md sections 0 + 7): an AI-generated illustration + the
title that, **together**, imply the essay's content — "implicating the contents
of the essay when combined with the title." A header that is bright, soft,
legible, and 5:2 but says nothing about *this* essay has still failed.

## The implication test

Hold two things side by side:
1. The rendered header (illustration + title + meta + badge).
2. The essay's one-line **thesis** (what the header must imply).

Then ask, as a first-time reader who has not read the essay:

> From the picture and the title alone, can I guess what this essay is about —
> and is my guess close to the thesis?

- **Yes, and close to the thesis** → `pass`. The illustration's forms/glyphs
  point at the same idea the title names.
- **Yes, but it points somewhere else** → `high`. Title and image imply two
  different essays (e.g. title is about latency, illustration evokes a generic
  network cloud). Mismatch misleads the reader.
- **No — image is generic decoration** → `medium`. The illustration is a pretty
  gradient field with no concept-bearing glyph; the title carries 100% of the
  meaning and the image adds nothing. This is the most common failure.
- **No — image actively misreads** → `high`. The illustration implies a wrong or
  off-topic concept (e.g. a medical motif for a battery patent).

## Decoration vs implication

The illustration grammar (CONTRACT.md section 4, `illustration_grammar.md`) is:
a luminous gradient field + 2-4 soft accent forms + **lightweight conceptual
glyph(s) abstracted from the essay's keywords** (a lens/eye, a timeline, a
shield, etc.). The glyph is what turns decoration into implication.

- The `IllustrationSpec.keywords` (3-6 concept anchors from the essay) are the
  hook. Check that at least one **glyph reads as one of the essay's actual
  concepts**, not a stock motif. A timeline glyph for an essay about latency
  reduction implies the content; three abstract blobs do not.
- Title + glyph should **reinforce**, not duplicate and not diverge. If the title
  already says "sensor fusion" and the glyph is a literal label of "fusion," that
  is redundant but acceptable (`low`); if the glyph evokes an unrelated idea,
  that is `high`.

## What this pass does NOT judge

- **Aesthetic taste / art quality** beyond the bright-soft band — that is pass 2.
- **The illustration algorithm's internals** (`illustration.py`) — judge the
  output's meaning, not how it was generated. A procedural-backend illustration
  and an LLM-backend one are held to the same implication standard.
- **Title wording** — the title comes from the essay (`publication.md`); you are
  judging whether the *image* supports it, not rewriting the title.

## Recommendations should be re-render-able

Because this skill is review-not-fix, a coherence finding's recommendation must
be actionable through `build_header` — almost always a better `--thesis` or a
sharper `keywords` list fed to the illustration engine:

```yaml
- pass: content-coherence
  location: illustration center glyph
  severity: medium
  finding: |
    Header reads as a generic peach-to-sky gradient with three soft blobs. No
    glyph abstracts the essay's concept (an airbag-deploy latency cut via vision
    fusion). Title does all the work; the image is decoration.
  recommendation: |
    Re-run build_header with thesis sharpened to the mechanism and keywords that
    give the engine a concrete glyph to draw, e.g.
    keywords=["vision", "fusion", "timeline", "airbag", "milliseconds"].
```

## Severity quick-reference

| Observation | severity |
|---|---|
| Title + image imply two different essays | high |
| Image implies a wrong/off-topic concept | high |
| Image is generic decoration, no concept glyph | medium |
| Glyph present but weakly tied to a keyword | medium |
| Glyph reinforces the title (mild redundancy) | low |
| Image + title imply the thesis cleanly | no finding (pass) |
