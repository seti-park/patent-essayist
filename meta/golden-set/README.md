# Golden set — editorial before/after pairs

Raw material for **calibrating an LLM judge against SETI's own editorial decisions**, so that a
judge can eventually be *trusted* to do first-pass ranking (see "Planned" below). The principle:
"human-like" is not directly measurable, but *"how often does a candidate judge agree with SETI's
recorded decision"* is.

## Where the pairs come from

The orchestrator (`patent-essay/SKILL.md`, archive step) now preserves per-iteration drafts at
`runs/<essay-id>/iterations/iter-N-{pre,post}.md`. Each `(pre, post)` pair plus the `edit-log.md`
finding that drove the change is one golden-set record. (Before this change the essay bodies lived
only in gitignored `handoff/` and were overwritten every round — the pairs were being lost. That
gap is why "20-30 pairs already exist" was not actually true; we start accumulating now.)

## Record schema

One JSON object per line in `pairs.jsonl` (append-only), or one folder per pair — either is fine;
the harness reads `pairs.jsonl` first.

```json
{
  "pair_id": "691-tesla-rotor-investor-iter1-finding3",
  "essay_id": "691-tesla-rotor-nonmagnetic-filler-investor",
  "section": "§3",
  "before": "Tesla's move is to stop using steel for the holding job at all.",
  "after":  "Tesla's move is to stop using a steel strut for the holding job.",
  "driving_finding": "red-team-mechanism / overbroad-negation (low)",
  "seti_decision": "accept",          // accept | modify | reject  (what SETI did with the suggestion)
  "dimension": "mechanism-precision"  // voice | mechanism-precision | redundancy | structure | ...
}
```

`seti_decision` is the ground truth a judge is scored against: given `before` vs `after`, did the
judge pick the same direction SETI did?

## Seeding

Seed from the runs we have where the before/after text is recoverable (`runs/691-*`,
`runs/045-*`), then grow automatically as new runs archive their `iterations/`. Target for
enabling the planned harness: **≥ ~15-20 pairs** spanning more than one dimension.

---

## Planned (Phase B — designed, not yet built)

These depend on this golden set reaching size; they are recorded here so the intent is durable.
The design of record is the approved plan; this is the in-repo summary.

### B1 — `meta/judge-calibration.py` (judge agreement harness)
Given the golden-set pairs, present each `(before, after)` to a candidate judge **blind to which
is which and to the generation context**, force it to pick the more natural/stronger version and
**cite the specific sentence(s)** behind its call, then measure **agreement rate** vs
`seti_decision`. Report per-dimension agreement. **Gate: only delegate first-pass ranking to that
judge when agreement ≥ 80%** (configurable); below that, the human stays the first ranker.
Propose-only meta artifact (like everything under `meta/`).

### B2 — comparative generation / pairwise tournament (opt-in compose mode)
A `--compose best-of-N` mode (default **off**): the composer generates a section in **N fresh
contexts** (default 3); a **blind** judge runs a pairwise tournament with canon anchors (e.g. a
voice-canon entry) and **must cite specific sentences** as evidence; only the survivor returns.
**Trusted only after B1 reports ≥ 80% agreement** — until then the judge is not calibrated enough
to delegate to. Cost note: N× generation + tournament per section, hence opt-in, not default.

### Boundary (applies to B1/B2 too)
Statistical proxies (sentence-length variance, etc.) may be **elimination filters**, never the
tournament's optimization **target** — same anti-Goodhart rule as the gates (see
`_shared/references/scoring-rubric.md` "Measurement discipline"). The pairwise judge ranks on
holistic naturalness with sentence-level evidence, not on a proxy score.
