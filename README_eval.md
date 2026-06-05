# Skill-description eval harness

Tools for evaluating and improving the frontmatter **`description`** of a skill
— the field a dispatcher reads to decide *when to load the skill*. A good
description fires on the prompts it should and stays quiet on the ones it
shouldn't.

Built around the bundled **`patent-thread`** skill (`skills/patent-thread/SKILL.md`),
but works on any `SKILL.md`.

## Scripts

| Script | What it does |
| --- | --- |
| `run_eval.py` | Scores a description two ways and prints a combined report. |
| `improve_description.py` | Rewrites the description to score higher, then re-evaluates to prove it. |

### `run_eval.py`

Two measures:

1. **Trigger accuracy** — a router, shown *only* the skill name + description,
   decides whether to invoke the skill for each labelled prompt in
   `data/patent-thread.jsonl`. Reported as a confusion matrix +
   precision / recall / F1 / accuracy.
2. **Description rubric** — the description text is graded against five criteria
   (trigger coverage, scope boundaries, purpose clarity, concrete examples,
   conciseness), 0–100.

A **composite** = 70% trigger-F1 + 30% rubric.

```bash
python run_eval.py                       # default skill + dataset
python run_eval.py --all                 # list every case, not just failures
python run_eval.py --json outputs/eval.json
python run_eval.py --description "Make a thread."   # try an alternative description
python run_eval.py --skill path/to/SKILL.md --dataset path/to/set.jsonl
```

### `improve_description.py`

Evaluates the current description, proposes a rewrite that fixes the trigger
failures and weak rubric criteria (preserving the skill's meaning, persona, and
every `NOT ...` scope boundary), then re-evaluates and prints a before/after.

```bash
python improve_description.py            # writes outputs/<name>.improved.md
python improve_description.py --rounds 2 # iterate; keeps a round only if it helps
python improve_description.py --write    # also patch the SKILL.md description in place
python improve_description.py --json outputs/improve.json
```

`--write` only patches when the rewrite beats the baseline, and changes *only*
the `description:` field — the body of the SKILL.md is left byte-for-byte intact.

## Online vs offline

Both scripts print their mode in the header.

- **ONLINE** — when the `anthropic` SDK is installed *and* `ANTHROPIC_API_KEY`
  is set. The router judgment, rubric grading, and rewrite are done by Claude
  (`claude-opus-4-8` by default, adaptive thinking, structured outputs). Override
  with `--model`.
- **OFFLINE** — otherwise. A deterministic, **description-driven** heuristic
  stands in: trigger terms and `NOT ...` boundaries are parsed straight out of
  the description, so editing the description measurably changes the scores. This
  keeps the harness runnable in CI / sandboxes and makes the improvement loop
  demonstrable with no API key.

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python run_eval.py        # now ONLINE
```

### Caveat on the offline improver

The offline rewrite *mines* missing trigger vocabulary from the misclassified
examples and appends it to the description. It filters generic words and rejects
any term that appears in a should-not-trigger prompt (substring-aware, so Korean
particle agglutination can't sneak in a false positive), but the result is still
keyword-level — it reads like a keyword list, not prose. The **online** path
produces a clean, rewritten paragraph. Treat the offline improvement as a
floor/demonstration, not a final edit.

## Layout

```
run_eval.py                     # entrypoint: evaluate
improve_description.py          # entrypoint: improve + re-evaluate
skills/patent-thread/SKILL.md   # the skill under test (vendored from the .skill bundle)
data/patent-thread.jsonl        # labelled prompts (should_trigger true/false)
skill_eval/                     # library
  skills.py     # parse / rewrite SKILL.md frontmatter
  dataset.py    # load the labelled set
  llm.py        # Anthropic client + online/offline flag
  heuristics.py # description-driven trigger/scope parsing (offline)
  evaluate.py   # trigger accuracy + rubric (online + offline)
  improve.py    # propose an improved description (online + offline)
  report.py     # text formatting
outputs/                        # generated artifacts (gitignored-friendly)
```
