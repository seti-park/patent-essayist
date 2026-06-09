# X Articles Format (deliverable shape — Phase 2)

> **Status: SCAFFOLD + canon target.** The structural shape of the published deliverable
> (X Articles). Loaded by Phase 2 to build the section blueprint and by Phase 3 to check
> conformance. Replace with the user's canon; keep the section names the gates key on.

## Shape (starter — port the canon)

- **Title** — no em-dash; carries the thesis angle.
- **Lede / hook** — the tension the essay opens on.
- **Body sections** — each advances one sub-claim of the thesis spine; figures placed per
  `caption-roles.md`; citations are `[dddd]` anchors from the Phase-1 hand-off.
- **Close** — specific, falsifiable so-what.
- **Sources block** — a `## Sources` section at the end, with the 5-category enum and the
  patent-citation format the `gate_sources.py` checks.

## Structural bands (tunable; mirrored in `gate_structure.py` constants)

- Essay-mode paragraphs: roughly 3–7 sentences; hard warn above 8.
- No bold/bullet overuse; bullets only for genuinely parallel discrete items.
- Mode: `essay` (default) vs `wire` — `wire` is a shorter drop; both run the same gates.

<!-- PORT: drop the user's x-article-format canon here. Keep the Sources block contract
     aligned with gate_sources.py (5-category enum, 6-field patent citation,
     all-or-nothing subgrouping). -->
