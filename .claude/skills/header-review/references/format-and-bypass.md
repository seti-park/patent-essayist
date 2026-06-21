# Passes 1 + 5 — Format & No-bypass (delegated to gate_header)

These two passes are **mechanical**. They do not require visual judgment; they
delegate to the deterministic `_shared/scripts/gate_header.py` gate and report its
result. A fail here is non-negotiable and forces `overall_assessment:
revise-required` (the hard-gate override in `feedback-format.md`).

Run the gate first, then write the two passes from its findings:

```
python .claude/skills/_shared/scripts/gate_header.py
```

(Or import it: `gate_header.check(None, {})` returns `{"gate", "passed",
"findings"}` with `check_id`s, the same shape as the essay gates.)

## Pass 1 — Format

Delegates to **`gate_header_ratio`** (`check_id` `HEADER-RATIO-001` / note
`HEADER-RATIO-000`).

| gate_header finding | header-review severity | meaning |
|---|---|---|
| `HEADER-RATIO-001` | `high` → `revise-required` | a `runs/**/header*.png` is not exactly 5:2 (2.5), or could not be opened |
| `HEADER-RATIO-000` (note) | n/a (`pass`) | no header PNG present yet — record as `"no findings"` with the note in `scoped_to` |
| no findings | `pass` | every header PNG is exactly 5:2 |

Also confirm by inspection: the file is the canonical **3000x1200** raster (the
contract's X-Articles cover size), not just any 5:2. A 5:2 image at a tiny size
is technically in-ratio but below deliverable resolution — flag as `medium` if
the dimensions are far below 3000x1200.

## Pass 5 — No-bypass

Delegates to **`gate_header_bypass`** + **`gate_header_tokens`**.

| gate_header finding | header-review severity | meaning |
|---|---|---|
| `HEADER-BYPASS-001` | `high` → `revise-required` | a raster primitive (`ImageDraw.Draw(`, `Image.new(`) is called outside the headerkit draw allowlist (`components.py`, `render.py`, `illustration.py`) — something hand-drew a header instead of routing through the library |
| `HEADER-TOKENS-001` | `high` → `revise-required` | a header source carries a raw `#RRGGBB` literal instead of a `tokens.Theme` value |
| `HEADER-TOKENS-002` | `high` → `revise-required` | a drawing header source does not import palette from `tokens` |
| `*-000` (note) | n/a (`pass`) | nothing to check yet (no header source / no primitives found) — record `"no findings"` |
| no findings | `pass` | every header routed through HeaderKit with token-sourced color |

## Why these are hard gates

The whole point of HeaderKit (CONTRACT.md sections 1 + 6) is *one source of
truth*: every header is 5:2 and every color comes from a theme token. A bypass or
a stray hex means a header that drifts off-brand or off-ratio without the library
being able to catch it. So unlike the visual passes (2-4), these cannot be
"recommended" — a fail is always `revise-required`.

## Recording a delegated pass

Even when the gate passes, the pass must appear in the YAML output (empty-pass
rule). Put the gate's confirmation in `scoped_to`:

```yaml
- pass: format
  finding: "no findings"
  scoped_to: "gate_header_ratio PASS — runs/044/header.png is 3000x1200, ratio 2.5"

- pass: no-bypass
  finding: "no findings"
  scoped_to: "gate_header_bypass + gate_header_tokens PASS — all primitives in headerkit, no stray hex"
```
