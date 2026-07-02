# Run notes — `2026-07-01-us20230356397b2-cliff-histogram-bridge`

Run-scoped retro narrative, moved verbatim out of `meta/attribution-table.md`
(2026-07-02 meta-harvest refactor). One file per run: parallel Claude Code
sessions append run notes here without ever conflicting on the shared
attribution table. Durable class-routing knowledge stays in the table;
counts are derived by `meta/tally_ledger.py`.

### Update — run `2026-07-01-us20230356397b2-cliff-histogram-bridge`

Row counts above (`redundancy-bloat` 8, `mobile-paragraph-wall` 8 watch + 2 proposed,
`sources-entry-template-drift` 6, `claim-vs-spec-citation-conflation` moved to 2 under
`proposed` now that a proposal file exists for the class, plus new rows
`thesis-restatement-redundancy` 3, `anchor-malformed` 2, `paraphrase-substantive-change` 2,
`closing-scope-overreach` 1, `quote-fidelity-gap` 1, `figure-mechanism-oversimplification` 1)
reflect this run's 13 inner-loop records + its pre-existing 5 self-post-accept records, added by
`pipeline-retro`. Only rows this run's records touch were recomputed from the full ledger; other
rows above (e.g. `claim-scope-misattribution`, `external-fact-universalization`) were not
touched by this run and were left at their prior values, which are already known to lag the
ledger by several intervening runs (`2026-06-26-*`, `2026-06-27-*`) not yet reconciled here — a
full-table recount is a separate, larger task than this run's retro warrants.

**`claim-vs-spec-citation-conflation` is now at 2 total occurrences** (run
`045-agility-638-last-mile-moat` iter 1, `inner-loop`/editorial + this run,
`self-post-accept`/self-audit) — below `RECUR_THRESHOLD` (3). Held at `watch`, not promoted.
See `meta/improvement-proposals/2026-07-01-claim-vs-spec-citation-conflation-watch.md` for the
explicit watch record and the applied-in-advance recommendation (run 045's own logged
recommendation already states the fix; both occurrences self-corrected without needing it
applied, but a 3rd occurrence should auto-promote).

**Within-run recurrence signal:** this run's `mobile-paragraph-wall` recurred 4 times *within
its own inner loop* (iter 1→2→3→4) before resolving at the iteration cap — see the "Within-run
recurrence" section above. This does not change the cross-run recurrence count differently than
a normal 4-record addition would, but it is additional, sharper evidence for the already-on-file
`2026-06-11-gate-structure-word-wall.md` proposal (`recommended-apply`): the gate gap is now
shown to cost iterations within a single essay, not just to recur across essays.
## Within-run recurrence — a distinct signal from cross-run recurrence

`2026-07-01-us20230356397b2-cliff-histogram-bridge` recurred `mobile-paragraph-wall` 4 times
*within its own inner loop* (iter 1 -> 2 -> 3 -> 4, shrinking magnitude each round, only
resolving at the iteration cap). This is the same `pattern_tag` as the existing cross-run
`mobile-paragraph-wall` class (see the main table row above and the recurrence ledger below —
counted together, not double-tracked under a second tag), but the *within-one-essay* shape of
the recurrence is itself a signal distinct from cross-essay recurrence: a single essay needing
3 revision rounds to clear one finding class, even though it converged before the cap, means the
mechanical gate gap (`gate_structure.py` counts sentences, not words) cost this run 3 full
Compose<->Edit iterations it should not have needed. This sharpens (does not replace) the
existing `mobile-paragraph-wall` proposal record: the word-count gate gap is not just a
gate-invisibility problem across essays, it is now demonstrated to be an iteration-cost problem
within a single essay. See `meta/improvement-proposals/2026-06-11-gate-structure-word-wall.md`
(already `recommended-apply`) — this run is additional evidence for that same on-file proposal,
not a new class or a new proposal.
