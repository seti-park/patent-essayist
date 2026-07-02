# improvement-proposals/

`pipeline-retro` writes evidence-backed, propose-only improvement proposals here, one file per
proposal (`<date>-<slug>.md`, format in `pipeline-retro/references/proposal-format.md`).

Nothing here is applied automatically. To apply one: review it, run
`python meta/regression.py`, and if green, make the edit, update the proposal's `status:` to
`applied (...)` with a short update note at the top, regenerate the derived tally
(`python meta/tally_ledger.py --write`), and commit citing the triggering finding ids.

Status lifecycle (frontmatter `status:`): `watch` (on file, below the recurrence bar) →
`recommended-apply` (bar crossed — apply next) → `applied (...)` (done, with date + context)
or `escalated` (cascade cap hit — needs a human design decision). A human may apply a `watch`
proposal early when its fix is mechanically proven; say so in the update note.

The 2026-07-02 meta-harvest refactor applied the whole backlog then on file: 8 proposals
(figuse-selection-scope, typography-html-comment, gate-structure word-wall +
sentence-band-align, sources-entry-field-completeness, claim-vs-spec-conflation,
external-fact-scope-discipline, emoji-host-fence-decidable, publication-line-wrap), each as
its own commit. The derived tally in `meta/attribution-table.md` shows per-class proposal
status at a glance.
