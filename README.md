# patent-essayist

A skill-based Claude Code pipeline that turns an **English patent** (plus pre-cleaned
figures) into a finished **English essay** for X Articles, in three phases —
**Design → Compose → Edit** — with an automated Compose↔Edit quality loop (deterministic
gates + 6-pass editorial review) and a propose-only self-improvement meta-loop.

Full architecture, voice-fencing rules, and loop policy: **[CLAUDE.md](CLAUDE.md)**.

## Run

Place inputs under `input/` (`patent.md`, `figures/fig-NN.png`, optional
`essay-context.md`), then in Claude Code:

```
/patent-essay <patent path | text | number>  [--threshold pass|revise-recommended] [--max-iter 4]
```

The final essay lands at `handoff/03-edit/essay-final.md` with a score history; the run is
archived under `runs/<essay-id>/` and the meta-loop (`pipeline-retro`) may leave an
improvement proposal in `meta/improvement-proposals/` for human review.

Individual phases run standalone: `/thesis-architect`, `/essay-en-composer`,
`/editorial-review`, `/pipeline-retro`.

## Tests

```bash
python .claude/skills/_shared/scripts/test_gates.py   # gate unit suite
python meta/regression.py                             # suite + meta/fixtures/ regression guard
```

Both run in CI (`.github/workflows/gates.yml`) on every push/PR. Pure Python stdlib — no
dependencies to install.

## Layout (short)

| Path | What |
|---|---|
| `.claude/skills/` | The pipeline: orchestrator + 4 phase skills + meta-loop + shared gates/references |
| `handoff/` | Runtime stage artifacts (gitignored; regenerated per run) |
| `meta/` | Persistent memory: findings ledger, attribution table, fixtures, regression guard |
| `runs/` | Per-run archives |
| `docs/source-prompts/` | Frozen verbatim record of the original claude.ai skills |

## Status

Pre-first-production-run: gates, loop contracts, and regression fixtures are in place;
three `_shared/references/` voice files are still scaffolds awaiting the owner's canon
(see `docs/audit/2026-06-10-repo-audit.md` for the full audit and task plan).
