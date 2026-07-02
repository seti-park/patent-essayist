# Run notes — `vl53l9cx-ep2-crosstalk-us20240192337`

Run-scoped retro narrative, moved verbatim out of `meta/attribution-table.md`
(2026-07-02 meta-harvest refactor). One file per run: parallel Claude Code
sessions append run notes here without ever conflicting on the shared
attribution table. Durable class-routing knowledge stays in the table;
counts are derived by `meta/tally_ledger.py`.

New first-seen class in `vl53l9cx-ep2-crosstalk-us20240192337` (2026-07-01, inner-loop iter-1
HIGH — the sole driver of that iteration's `revise-required`): **`sources-category-omitted`** —
the `# Sources` block carried only `## Official statements` and `## Technical specs`
subheadings; neither analyzed patent (subject US 2024-0192337 B2, supporting US 2025-0012901)
appeared under a `## Patents` category at all, despite both being cited in-body. Distinct from
the table's two existing Sources-structure classes: `sources-enum-violation` is a *wrong label*
(an ad-hoc category name outside the 5-item enum) and `sources-subgroup-violation` is
*inconsistent subgrouping* (some sources categorized, others not, once `##` is in use) — this is
a *whole required category silently absent* despite in-body use, which neither existing check
tests for. First occurrence, count 1, filed `watch`; needs the human-added attribution-table row
above (marked †) confirmed/refined once a second instance appears. Resolved iter-2 (`## Patents`
added, ordered first, both patents in 6-field format).

This run's `redundancy-bloat` instance (iter-1 MEDIUM, §6 3-idea paragraph) is a **new
sub-mechanism**, not a repeat of a prior flavor: each of the three stacked ideas individually
honored its own word-budget instruction, but the paragraph-level combination pushed past the
single-idea earn threshold — a *budget-per-idea vs. budget-per-paragraph* gap, distinct from the
class's previously observed flavors (word-level doubling, header/body echo, sanctioned
cross-section layering, intensifier tics). Still folded into the umbrella `redundancy-bloat` tag
per the class's existing heterogeneous-sub-mechanisms handling (see below), not split out, since
it is a single low-frequency instance of yet another sub-mechanism rather than a stable new
pattern on its own.

This run's `sources-entry-template-drift` instance (iter-2 LOW — "filed" used instead of the
spec's "priority" label; hero-patent publication date omitted with no placeholder) is the 4th
occurrence of the class and crosses `RECUR_THRESHOLD`. Unlike the prior three occurrences (all
`watch`, no proposal on file), this run's evidence — combined with the prior three — supports a
`recommended-apply` reference-edit: see
`meta/improvement-proposals/2026-07-01-sources-entry-field-completeness.md` (fixes both the
Patents field-4/5 label-locking and unstated-field placeholder convention, and the adjacent
Papers author/venue-unstated convention that drove the first two occurrences).

This run's `meta-reader-instruction` instance (iter-1 LOW, FIG. 1 caption "this essay starts
from...") is the 3rd ledger occurrence of the tag but **does not** warrant a new proposal: unlike
the prior two occurrences (both confirmed violations that were removed), this one was judged
*borderline* and ultimately ruled an exempted functional-scope-disclaimer, not a violation —
`gate_meta` (already gate-promoted in run 045, see the main table above) correctly did not fire.
This is the mechanism working as designed at the judgment layer, complementing rather than
exposing a gap in the mechanical gate; no action proposed.
