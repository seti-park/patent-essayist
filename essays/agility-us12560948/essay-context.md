# Essay context — investor / technical-moat angle (US 12,560,948 B2)

Framing brief for this deliverable. Records the audience reframe and the discipline applied, so
the run is reproducible and the editorial choices are on the record.

## Audience and purpose

- **Audience:** technology investors performing diligence.
- **Job to be done:** decide whether Agility Robotics has a real technical moat, using this
  patent as evidence.
- **Deliverable:** a single English analytical article, not the storytelling series essay.

## Angle reframe (important)

The materials bundled with the patent (`Context.md`) were written for a different deliverable: a
Korean, general-audience storytelling series ("patents as a growth diary"), Act 4, story-first,
for readers who do not know Agility. That brief's hook and tone do not fit an investor moat
assessment.

This deliverable keeps the bundled brief's verified **facts** (patent number, dates, claim
language, technical core, the maturation-toward-safety observation) but discards its
**storytelling angle** in favor of the investor / moat question the user actually asked. Where
the two conflict, the user's request controls.

## Discipline applied (from the repo's own lessons and proposals)

- **Claim-scope lock-map** (`meta/improvement-proposals/2026-06-11-claim-scope-lock-map.md`): the
  moat verdict rests only on what independent claim 1 *requires* (locked). Optional embodiments
  in the description and dependent claims are labeled open; example point values are labeled
  pinned. No description-preferred behavior is credited to claim 1.
- **External-fact scope discipline**
  (`meta/improvement-proposals/2026-06-11-external-fact-scope-discipline.md`): market facts are
  scoped to their sources and never universalized.
- **Investor-edition speculation framing**
  (`docs/lessons/investor-edition-speculation-framing.md`): market and financing context is
  fenced as "outside the filing" and sourced; the patent analysis is the spine. No forcing of an
  unstated competitor angle.

## Sourced external facts used

- SPAC merger (Churchill Capital Corp XI), about $2.5B valuation, Nasdaq ticker AGLT, close
  expected around end of 2026, roughly $620M cash incl. a Foxconn-led portion. Source: GeekWire.
- Digit in paid commercial use at GXO (more than 100,000 totes), plus Schaeffler, Toyota Motor
  Manufacturing Canada, Mercado Libre. Sources: GXO press release; Robotics & Automation News.

## Verification

All six deterministic gates pass with zero findings (see `gate-result.txt`). Citation anchors
resolve against `invention-summary.md`; selected figures 1, 3, 6 are all used; Sources block uses
the 5-label category enum with all-or-nothing subgrouping.
