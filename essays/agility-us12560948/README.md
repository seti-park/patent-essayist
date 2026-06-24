# Agility Robotics moat analysis — US 12,560,948 B2

An investor-facing technical-moat article on Agility Robotics' granted patent
US 12,560,948 B2 ("Escalating hazard-response of dynamically stable mobile robot in a
collaborative environment"), plus its grounding artifacts.

The patent-essay pipeline writes finished essays to gitignored runtime directories
(`handoff/`, `runs/`). This folder is a tracked, self-contained deliverable so the article and
its evidence survive outside a single run.

## Contents

| File | What it is |
|---|---|
| `essay-final.md` | The deliverable article. |
| `invention-summary.md` | Phase-1 grounding: verbatim citation-anchor set + claim-scope map (locked / open / pinned). |
| `figure-selection.md` | Which figures are used (1, 3, 6) and why. |
| `essay-context.md` | The investor / moat framing brief and the angle reframe from the bundled storytelling context. |
| `gate-result.txt` | Output of the six deterministic validation gates (all pass, zero findings). |
| `figures/` | The three patent figures referenced by the article (FIG. 1, 3, 6). |

## The thesis in one line

Agility's defensible technology here is not locomotion. It is the graduated, clearance-aware,
center-of-gravity-lowering way a dynamically stable robot comes to rest near a person, which is
the capability that lets a humanoid leave the cage and work beside people.

## Reproduce the validation

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft essays/agility-us12560948/essay-final.md \
  --invention-summary essays/agility-us12560948/invention-summary.md \
  --figures <(printf '1 2 3 4 5 6 7 8\n') \
  --figure-selection essays/agility-us12560948/figure-selection.md
```

## Scope note

This is a technical and strategic read of the patent for investor diligence. It is not a legal
opinion on claim validity or freedom to operate. Market and financing facts are sourced from
public reporting and are external to the patent; the patent does not establish them.
