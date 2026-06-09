# Anti-AI-Writing canon (Phase 2 strip, Phase 3 Pass 1 check)

SETI's anti-AI-tell rules are the source of truth for naturalness (north-star goal 4b). This
canon has two tiers:

- **Mechanical subset** — the unambiguous banned words/patterns, mirrored to
  `_shared/scripts/banned_terms.txt` and hard-enforced by `gate_banned.py`. A hit fails the
  loop round.
- **Judgment list** — the richer set of AI tells (copula avoidance, transition fingerprint,
  hedging, scaffolding, etc.) that editorial **Pass 1** evaluates with context. These are not
  mechanically gated because flagging them blindly would false-fail legitimate prose.

The two well-researched vendored skills (`_shared/vendor/humanizer`, `_shared/vendor/ai-check`)
have been **absorbed into this canon** and are kept only as reference (they are NOT run in the
runtime loop — a generic detector would fight SETI's voice). The meta-loop (`pipeline-retro`)
grows this canon over time and proposes promotions into the mechanical subset when a pattern
recurs and is safe to enforce.

## Tier 1 — Mechanical banned list (mirrored to banned_terms.txt)

### Banned words (Pass 1 — high severity, hard gate)

```
delve, tapestry, vibrant, pivotal, crucial, fostering, underscore, meticulous,
intricate, testament, garner, bolstered, showcase, enhance, enduring, valuable,
boasts, renowned, multifaceted, leverage, navigate, resonate, nestled,
groundbreaking, interplay
```

Context-dependent (canon-banned, but left to judgment to avoid false fails):
- **landscape** — banned in the abstract sense ("competitive landscape"); fine geographically.
- **Additionally** — banned sentence-initial only (the gate regex catches the sentence-initial form).

### Banned rhetorical patterns (Pass 1 — high severity)

- **not-just-X-but-Y / not-only-but** negative parallelism. *(gated)*
- **despite-the-challenges** throat-clearing introductions. *(gated)*
- **copula avoidance** — "serves as a / stands as a / represents a / constitutes" in place of
  is/are. *(serves/stands-as-a gated; the rest judged)*
- **section summaries / generic conclusions** — "In summary", "To recap", "In conclusion". *(gated)*
- **filler announcement** — "It's worth noting that…". *(gated)*
- **vague attributions** — "Many experts believe", "It is widely accepted", "Studies show".
- **puffery** — "remarkable", "extraordinary", "unprecedented".
- **elegant variation** — the same subject renamed mid-paragraph (Tesla → the EV maker → the
  Austin-based company).

## Tier 2 — Judgment list (Pass 1, absorbed from vendored research)

### AI vocabulary co-occurrence (humanizer §7)

Beyond the banned words above, watch for clustering of: *actually, align with, emphasizing,
highlight (verb), key (adjective), unlock, foster, seamless, robust, realm, game-changer.*
A single use may be fine; a cluster is an AI tell.

### Transition-word fingerprint (ai-check Signal F)

Strong tells as paragraph openers: **Furthermore, Moreover, Additionally** (sentence-initial),
"It is clear that", "This highlights/underscores the importance of", "As previously mentioned",
"Needless to say". Moderate: "Turns out / it turns out that" as a manufactured-discovery pivot;
tutorial-voice transitions ("The standard fix is…", "The common approach is…");
announcement-colon patterns ("The key insight:", "What surprised me was…").

### Structural / punctuation tells (humanizer §§14–19, ai-check Signal G)

- **Em dashes** — cut them (also `gate_emdash`). Double em-dash wrapping and em-dash-as-pivot
  are near-certain AI tells.
- **Semicolons** joining two independent clauses in non-academic prose.
- **Mid-sentence colons** after an incomplete clause ("The problem: nobody tests this").
- **Boldface overuse** (also `STRUCT-002`); **inline-header vertical lists**; **Title Case in
  body headings** where sentence case is the house style; **emoji** (only 🤔 at a
  `closing-open-question` ending).

### Content-shape tells (humanizer §§1–6, 25)

- Undue emphasis on significance / legacy / "broader trends".
- "-ing"-ending superficial analyses ("highlighting the importance of…").
- Promotional / advertisement language; "challenges and future prospects" outline sections.
- Generic positive conclusions ("a bright future", "continues to evolve").

### Raise-then-disavow / manufactured insinuation

Raising a suggestive idea and then disavowing it — "X, but that is a coincidence, not a plan" — lets the prose collect the reader's frisson while dodging the claim. To a skeptical reader it reads as manipulation: the writer wants credit for the implication without owning it. Either state the point plainly if it does real work, or cut it. (Real example: a same-name coincidence floated as color, then waved off — the insinuation lands anyway, which is the problem.)

### Hedging & filler (humanizer §§23–24, ai-check Signal C)

- Filler phrases ("in order to" → "to", "due to the fact that" → "because", "at this point in
  time" → "now", "has the ability to" → "can").
- Stacked hedges ("could potentially possibly").

## What NOT to flag (false-positive guard)

Preserve genuine human writing: domain terms used precisely, deliberate repetition for
emphasis, one well-placed em-dash inside a verbatim patent quote (allowed by `gate_emdash`),
intentional sentence fragments for cadence that match the voice canon. The judgment list is for
*clusters and patterns*, not isolated single words in otherwise human prose.

## The strip pipeline (Phase 2 step 7)

1. Draft in voice (Phase 2, full voice stack on).
2. Strip residual AI tells per this canon → clean `publication.md` (see
   `essay-en-composer/references/strip-pipeline.md`).
3. `gate_banned.py` is the mechanical backstop; editorial Pass 1 is the judgment backstop;
   this canon is the intent both enforce.

## Keeping script + canon in sync

When the Tier-1 list changes, update `_shared/scripts/banned_terms.txt` (literals one per
line; `re:` prefix for regex) so `gate_banned.py` stays aligned. `pipeline-retro` proposes
these edits with evidence; a human applies them after the regression check.
