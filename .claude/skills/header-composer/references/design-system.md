# Header design system (house grammar)

Derived 2026-06-10 from reference analysis of three high-performing X-Article headers
(Lance Martin "Designing loops", Codez "Master Claude Dynamic Workflow", Mohit Goyal
"I built the loop") against our dark v1-v3 drafts. Frozen here + in
`scripts/make_header.py`; change via `pipeline-retro` proposal, not per run.

## The five rules that make headers work on X

1. **Light card on a dark timeline.** Most X users run dark mode; a cream card is the
   highest-contrast object in the feed. Never ship a dark header.
2. **Flat print, no glow.** Gradients/glows read as promo/crypto; flat ink-on-paper reads
   as editorial/credible. Patent drawings are natively black-line-on-white — this grammar
   is their home turf.
3. **Two colors only.** Ink black + ONE warm orange accent. The accent appears in: kicker,
   badge, one headline word, strike/underline, strip dots, figure caption tick. Nowhere
   else.
4. **Type left, evidence right.** The right side is a real artifact (the patent figure),
   not decoration — it teaches the article's shape before the click.
5. **Micro-furniture signals craft.** Mono letterspaced labels, a filled badge, corner
   ticks, a bottom index strip. Small text need not be legible in the timeline; it reads
   as care.

## Tokens

| Token | Value | Use |
|---|---|---|
| paper | `#F7F3EA` | background |
| ink | `#14161B` | headline, figure linework, big numbers |
| accent | `#E4572E` | the single warm accent (see rule 3) |
| paper-dim | `#B9B1A0` | the struck "old" value |
| gray-text | `#6E6757` | mono microcopy |
| tick | `#C9C2B4` | corner furniture |

## Type

| Role | Font | Notes |
|---|---|---|
| Serif statement | Fraunces (var: opsz 144, wght ~620) | `editorial` headline |
| Display numbers / sans headline | Space Grotesk (var: wght 640-700) | `numbers` variant |
| Microcopy / labels | IBM Plex Mono Medium / SemiBold | UPPERCASE, letterspaced +5..7 |

Fonts vendored in `assets/fonts/` (SIL OFL, licenses alongside).

## Canvas

2000×800 (X Article header is 5:2). Safe margins 92px; corner ticks at 56px. Headline
must survive ~500px-wide timeline scaling: hero element (statement or number) is the only
thing that must be legible at that size.

## Layout recipes

- **editorial**: kicker (accent, bulleted) → badge (accent fill) → 3-line Fraunces
  statement (one accent word max) → bottom index strip. Right: patent figure as ink layer
  (autocontrast → invert → alpha), caption with accent tick.
- **numbers**: kicker left + dim kicker right → struck old value (paper-dim + accent
  strike, rounded caps) → thin arrow → giant ink new value → twin mono captions on one
  baseline (old: gray, new: accent) → flat accent staircase (FIG.9 motif) at the bottom.

## Don'ts

Dark backgrounds; glow/gradients; more than one accent word; repeating the article title;
marketing adjectives in the strip; em-dashes in any copy; per-essay font changes.
