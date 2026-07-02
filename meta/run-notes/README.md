# run-notes/

One file per essay run: `<essay-id>.md`, written by `pipeline-retro` at the end of the run's
meta-loop. It holds the run-scoped retro NARRATIVE — what the run surfaced, judgment calls
(hold-at-watch vs promote), which existing classes recurred and how, self-audit calibration
notes — everything that used to be appended to `meta/attribution-table.md` per run.

Why a file per run: the 2026-07-01 runs executed as three parallel Claude Code sessions, and
all three appended their narrative to the same spot in `attribution-table.md` — a guaranteed
3-way merge conflict. Per-run files never conflict. The shared table now carries only durable
class knowledge (the routing tables) plus a tally that is DERIVED from the ledger by
`python meta/tally_ledger.py --write` (checked by `meta/regression.py`).

Companion append-only channels that also never need hand-merging:
- `meta/findings-ledger.jsonl` — normalized records; `.gitattributes` gives it `merge=union`.
- `meta/improvement-proposals/<date>-<slug>.md` — one file per proposal.
