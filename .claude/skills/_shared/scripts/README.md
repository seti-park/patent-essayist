# Patent-essay validation gates

Deterministic, mechanical checks that a finished English essay draft must pass.
Pure Python 3 standard library — **no pip installs**. Every gate is runnable
standalone and importable; `run_gates.py` aggregates all five.

> **Provisional notice.** The real upstream handoff data formats (draft,
> invention-summary, figures index, sources schema, banned-term canon) are still
> **TBD**. These scripts use the documented, pragmatic formats below and are
> written to be easily retargeted: all tunable constants sit at the top of each
> file, and `banned_terms.txt` is a hand-seeded starter list meant to be
> replaced by the upstream anti-ai-writing canon.

## Files

| File                | Purpose |
|---------------------|---------|
| `gate_emdash.py`    | Em-dash / en-dash usage gate |
| `gate_anchors.py`   | Citation-anchor chain + figure-reference gate |
| `gate_sources.py`   | Sources-block structure gate |
| `gate_banned.py`    | Banned-terms / AI-tell phrase gate |
| `gate_structure.py` | Structural heuristics (all warn-only) |
| `banned_terms.txt`  | Provisional banned-term data file (see its header) |
| `run_gates.py`      | Aggregator + CLI |
| `test_gates.py`     | `unittest` suite (inline fixtures) |

## Format assumptions

- **Draft** is Markdown.
- **Quoted text** = anything inside double quotes `"..."` OR a Markdown
  blockquote line starting with `>`. Em-dashes and banned terms inside quoted
  text are allowed (verbatim source quotes). Fenced code blocks (```` ``` ````
  / `~~~`) are also exempt.
- **Citation anchors** = inline tokens `\[(\d{4})\]`, e.g. `[0123]`.
- **Figure refs** = `Figure N` / `Fig. N` / `Fig N` (case-insensitive), N int.
- **Sources block** = a Markdown header matching `^#{1,6}\s+Sources\s*$` near
  the end of the doc; the block runs to the next same-or-higher-level header.
- **Source entry** = a top-level list item; its category comes from a bold
  lead-in `**Category:**` or a dash lead-in `- Category — ...`.

## Shared gate contract

Each gate exposes:

```python
def check(draft_text: str, context: dict) -> dict
# -> {"gate": str, "passed": bool,
#     "findings": [{"check_id": str,
#                   "severity": "fail"|"warn",
#                   "message": str,
#                   "location": str}, ...]}
```

`context` keys consumed: `invention_summary_text` (str), `figures_index`
(list[int]), plus optional `banned_terms_file` / `banned_patterns` for the
banned gate, and a reserved `mode` pass-through.

## Usage

Aggregator:

```bash
python run_gates.py --draft DRAFT.md \
    [--invention-summary SUMMARY.txt] \
    [--figures FIGS.txt] \
    [--mode essay|wire] \
    [--json]
```

- `--figures` file: one integer per line, or comma/space separated.
- Exit code: `0` if no gate emits a `fail` finding, else `1`.
- **Warnings never fail the run.**
- `--json` emits `{"passed": bool, "gates": [...per-gate dicts...]}`.

Standalone gates:

```bash
python gate_emdash.py    DRAFT.md
python gate_anchors.py   DRAFT.md [--invention-summary S.txt] [--figures F.txt]
python gate_sources.py   DRAFT.md
python gate_banned.py    DRAFT.md [--terms banned_terms.txt]
python gate_structure.py DRAFT.md
```

Each prints a human-readable report and exits `0` (pass) / `1` (fail).

## Checks at a glance

| check_id     | sev  | meaning |
|--------------|------|---------|
| EMDASH-001   | fail | em-dash `—` outside quoted text / code |
| EMDASH-002   | warn | en-dash `–` used as a sentence connector |
| ANCHOR-001   | fail | `[dddd]` anchor not present in invention-summary |
| ANCHOR-000   | warn | no invention-summary provided; check skipped |
| FIGREF-001   | fail | figure number not in `figures_index` |
| FIGREF-000   | warn | no `figures_index` provided; check skipped |
| SOURCES-001  | fail | no Sources block found |
| SOURCES-002  | fail | entry category not in `ALLOWED_CATEGORIES` |
| SOURCES-003  | fail | `Patent` entry lacks `PATENT_CITATION_FIELDS` fields |
| SOURCES-004  | warn | mixed subgrouping (some entries under sub-groups, some not) |
| BANNED-001   | fail | banned literal/regex hit outside quoted text |
| STRUCT-001   | warn | paragraph > `MAX_SENTENCES_PER_PARA` sentences |
| STRUCT-002   | warn | bold spans > `MAX_BOLD_PER_100_WORDS` per 100 words |
| STRUCT-003   | warn | bullet lines > `MAX_BULLET_FRACTION` of non-blank lines |
| STRUCT-004   | warn | rule-of-three `A, B, and C` triad detected |

## Tunable constants

Edit the clearly-commented constants at the top of each gate file:

- `gate_emdash.py`: `EM_DASH`, `EN_DASH`, en-dash connector regex.
- `gate_anchors.py`: `ANCHOR_RE`, `FIGREF_RE`.
- `gate_sources.py`: `ALLOWED_CATEGORIES`, `PATENT_CITATION_FIELDS`.
- `gate_banned.py`: `BANNED_TERMS_FILE` (+ edit `banned_terms.txt`).
- `gate_structure.py`: `MAX_SENTENCES_PER_PARA`, `MAX_BOLD_PER_100_WORDS`,
  `MAX_BULLET_FRACTION`.

## Tests

```bash
python test_gates.py
```

Runs the full `unittest` suite (inline fixtures, no external files) and prints a
pass/fail summary; exits nonzero on any failure.
