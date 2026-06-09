# Style Guide — Voice for Patent Essays

> **Status: SCAFFOLD.** Starter voice/style rules. Refine with your own preferences.
> `essay-write` reads this together with the vendored humanizer skill.

## Voice

- Knowledgeable peer, not a press release and not a textbook. Confident, specific, dry.
- First person sparingly; second person only when it genuinely sharpens a point.
- Active voice by default. Passive only when the actor is irrelevant or unknown.

## Sentences

- Vary length deliberately. Mix short punchy sentences with longer reasoning ones.
- One idea per sentence. If you need two commas to hold it together, split it.
- Prefer concrete nouns and verbs over nominalizations ("decides" > "makes a decision").

## Word choice — ban list (AI tells)

Avoid: *delve, leverage, robust, seamless, underscore, highlight (as a verb), tapestry,
landscape (figurative), realm, navigate (figurative), testament to, in today's …,
it's worth noting, crucial, pivotal, game-changer, unlock, harness, foster.*
The vendored humanizer skill enforces the fuller catalog — this is the quick list.

## Formatting

- Prose, not bullet soup. Bullets only for genuinely parallel discrete items.
- No bold-word-then-colon "definition" lines inside body prose.
- Em dashes are allowed but rationed — no more than one per paragraph.
- No "rule of three" triads as a reflex ("fast, cheap, and reliable").

## Citations

- Reference patent specifics inline: "Claim 7 covers…", "Figure 3 shows…".
- Keep numbers honest; never invent a claim number or quantitative result.

## Relationship to the humanizer skill

`essay-write` drafts using these rules, then runs the vendored
`_shared/vendor/humanizer/SKILL.md` pass over the draft to strip residual AI tells while
preserving meaning. The style guide is the *intent*; the humanizer is the *enforcement*.
