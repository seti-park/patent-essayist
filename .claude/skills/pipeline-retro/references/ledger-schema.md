# findings-ledger.jsonl schema

`meta/findings-ledger.jsonl` is append-only. One JSON object per line, one object per
normalized finding (or failing gate `check_id`, or empty-pass marker). This is the substrate
the meta-loop scores recurrence over.

## Record fields

```json
{
  "essay_id": "044-tesla-rcm-vindication",
  "iter": 2,
  "run_timestamp": "2026-06-09T10:00:00Z",
  "source": "editorial | gate | red-team | fact-check",
  "pass": "pass-3-fact-paraphrase",
  "check_id": null,
  "severity": "high",
  "goal": "1",
  "root_cause_stage": "compose",
  "root_cause_artifact": "essay-en-composer/references/citation-format.md",
  "pattern_tag": "paraphrase-accidental-drift",
  "finding": "Prose uses 'complements'; source verbatim is 'supplements'.",
  "recommendation": "Re-anchor to source verbatim.",
  "status": "open"
}
```

| Field | Meaning |
|-------|---------|
| `essay_id` | the run's essay id |
| `iter` | inner-loop iteration the finding came from |
| `run_timestamp` | ISO-8601 |
| `source` | `editorial` (edit-log) · `gate` (gate-result.json) · `red-team` / `fact-check` (verification-log, from the independent `prepublish-verify` stage) |
| `pass` | editorial pass name, verify pass name (`red-team-*` / `source-resolution` / `external-claim-verification`), or `null` for gate records |
| `check_id` | gate `check_id` (e.g. `FIGUSE-001`), or `null` for editorial records |
| `severity` | `critical/high/medium/low` (editorial) or `fail/warn` (gate) |
| `goal` | north-star goal threatened: `1 / 2 / 3 / 4a / 4b` (from the matrix) |
| `root_cause_stage` | `design / compose / edit / gate / canon` |
| `root_cause_artifact` | the file/script that should have prevented it (attribution-table) |
| `pattern_tag` | stable slug grouping recurring classes (the recurrence key) |
| `finding` | the observation (verbatim from edit-log) |
| `recommendation` | the editor/gate recommendation |
| `status` | `open / watch / proposed / resolved / escalated` |

## Recurrence key

Recurrence is scored over `(pass_or_check, root_cause_artifact, pattern_tag)`. When the count
reaches `RECUR_THRESHOLD` (default 3) the class is eligible for a `recommended apply` proposal.
Empty-pass "no findings" records carry `severity: none` and never contribute to recurrence —
they exist only to prove a pass ran and to avoid mistaking silence for absence.

**Verification-origin priority (U5).** Records with `source` ∈ {`red-team`, `fact-check`} were
caught by the *independent* `prepublish-verify` stage — i.e. the inner loop's gates + editorial
*systematically missed* them. These use a lowered `RECUR_THRESHOLD` of **2**, and their proposal
must target the **stage that should have caught it** (an editorial pass, a compose reference, or a
gate promotion per `attribution-table.md`), never an essay-only patch. A recurring red-team
`patent-attributed-number`, for example, routes to a compose `citation-format.md` discipline edit
or an editorial Pass-3 strengthening — closing the blind spot, not re-patching prose.

## Append discipline

Never rewrite history. Corrections are new records with `status` transitions
(`open → proposed → resolved`). A proposal that is applied flips the triggering records to
`resolved` (a new appended record references them); an ineffective patch flips them to
`escalated`.
