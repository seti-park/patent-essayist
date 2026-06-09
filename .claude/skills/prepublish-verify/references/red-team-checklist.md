# Red-team checklist

The adversarial close-read run by `prepublish-verify` (sub-check A). You are NOT rubber-stamping
a draft the editor already passed — your job is to find what a single clean pass missed. Be
specific: quote the offending text, give the exact location, propose a concrete fix.

Form your judgment from `input/patent.md` (read in full) + `essay-final.md` +
`handoff/02-compose/thesis-trace.md` + `handoff/01-design/invention-summary.md`. Do **not**
treat `edit-log.md` as authority (independence — see SKILL.md).

## Checklist (each maps to a `verification-log` pass + a severity)

| # | Pass name | What to attack | Default severity |
|---|---|---|---|
| 1 | `red-team-grounding` | Each **load-bearing** body claim traces to a real invention-summary anchor / patent paragraph (via `thesis-trace.md` for investor bodies with no inline anchors). | high if a load-bearing claim has no patent basis; low if peripheral |
| 2 | `red-team-mechanism` | The essay describes the **actual** invention: what is retained vs removed, a *member* replaced vs a whole subsystem, the real interlock/structure. No technical misstatement. | **high** if the mechanism is *factually wrong* (reader is misled about what the invention does); **low** if directionally correct but imprecisely scoped (see boundary rule below) |
| 3 | `red-team-overclaim` | No body sentence implies the **patent disclosed a quantitative number** it does not. External/industry numbers must read unambiguously as context (hedged, attributed). Honest "no disclosed numbers" caveat (if applicable) must not be undercut elsewhere. | high (invented/patent-attributed number); medium (false precision / undercut caveat) |
| 4 | `red-team-scope` | The patent is not conflated with adjacent programs, products, or a broader claim than it makes. Fences (e.g. "this is not that program") hold. | high if the reader is misled about scope; medium if a fence is merely soft |
| 5 | `red-team-insinuation` | No raise-then-disavow / manufactured drama / insinuation (per `anti-ai-writing.md`). A person who is both a named inventor and a notable figure is a **neutral credibility fact**, not narrative drama. | medium |
| — | (overbroad negation) | A sweeping negation ("stops using X *at all*") that overstates the patent's actual scope. Report under `red-team-mechanism` (or `red-team-overclaim` if it inflates a result). Apply the boundary rule below. | medium **or** low — see below |

## Severity boundary rule (mechanism precision vs factual error)

The mechanism / overbroad-negation severity is the one boundary that flips the loop's
*behavior*: **medium** triggers a Compose↔Edit revision round (cost), **low** is a surgical
in-place fix. So classify it deliberately, not by feel:

- **medium** — the statement makes a reader believe something **factually false** about the
  invention. The surrounding prose does *not* recover the correct picture. Example: "the rotor
  contains no steel at all" when the laminations are steel — the reader now misunderstands the
  invention.
- **low** — the statement is **directionally true but imprecisely scoped** (an "*at all*"
  overstatement), and the surrounding text still conveys the correct mechanism. Example: "stop
  using steel *for the holding job*" where only the strut member is replaced and the laminations
  (correctly) remain steel — a precision nit, fix the phrase in place, no revision round needed.

When genuinely unsure between the two, prefer **low + a surgical recommendation** unless a reader
would actually walk away with the wrong mechanism — over-escalating to medium spends a full
revision round on a one-line wording fix.

## Audience branch (U6)

Read `audience` from the orchestrator (`deep` | `investor`).

- **investor** — emphasize: **no patent-attributed numbers** (#3), **scope conflation** (#4),
  **insinuation** (#5), and **finishability** (does a non-expert C-level/VC reader get through
  it; does each section earn its place; is the core mechanism clear without jargon). The body has
  **no inline anchors** — verify grounding (#1) via `thesis-trace.md`, never by demanding inline
  `[xxxx]` in the prose.
- **deep** — emphasize: **inline anchor↔claim fidelity in the body** (every `[xxxx]` actually
  supports its sentence), **reference-number correctness** (part numbers match the patent), and
  full-mechanism completeness. Numbers may be patent-sourced here, but still must be faithful.

## Output

One finding per real issue, in the `verification-log` schema (pass, severity, location, finding,
recommendation, optional `quote`). For a clean check emit the pass with `finding: "no findings"`
and `scoped_to:`. Do not invent issues to look productive — a genuine clean result is a valid
result, but say *why* you believe it holds (what you attacked and it survived).
