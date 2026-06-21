# Header lessons from viral X covers (2026-06-21, SETI)

Source: three high-reach X article covers (RAG / Loops / Stanford STORM). What they
share, and what HeaderKit changed to match.

## 1. No brand watermark on the image

None of the viral covers put the author's brand on the image. On X the **author's
name + handle directly above the card carries the brand** — repeating it on the
image is redundant and steals space from the message. Putting a brand tag on the
cover reads as ad-like, not editorial.

→ HeaderKit drops the series tag from the default composition. `build_header`
defaults `series=""` and only draws the tag when a caller explicitly opts in
(`series="…"` / `--series "…"`). The `series_tag` component stays in the library
for that opt-in case and for video/secondary uses.

## 2. Headline you grasp at a glance

The covers win on one big, bold, high-contrast headline you read without effort —
near-black on a light ground — with a short, clear subtitle underneath. The viewer
"feels" the key sentence in a single look before deciding to stop scrolling.

→ HeaderKit makes the headline dominant: darker `ink` (#1B232E, near-black) for
contrast, larger autosize band (`TITLE_MAX/MIN = 208/124`, bold), and a **clear
sans-serif subtitle** (`F_SANS`, `SUBTITLE=56`) instead of the small technical
mono. The text block is top-anchored and headline-first.

## What we kept

The bright/soft "aurora" ground and the per-essay AI illustration stay — they give
the calm, on-brand canvas. These two changes are about *foreground legibility and
removing redundancy*, not repainting the background.

## Not adopted (yet)

The viral RAG/Loops covers also use a **hand-drawn explanatory diagram** with
colored callout labels that literally teaches the concept. HeaderKit's illustration
is currently abstract (soft forms + conceptual glyphs). A future direction: a
"diagram" illustration backend that renders a small labeled sketch from the thesis.
Tracked as a possible `illustration` backend, not built here.
