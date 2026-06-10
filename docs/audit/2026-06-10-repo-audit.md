# Repo Audit & Improvement Plan — patent-essayist

Date: 2026-06-10. Scope: full repository at commit `2216af4`. Method: every claim below is
grounded in a file:line citation or an empirical probe (noted "verified"); facts and
judgments are labeled. No code was modified during the audit.

---

## Executive Summary

**Overall health: B−.** The conversion-layer engineering is genuinely strong — six
dependency-free gate scripts with a consistent contract, 32 passing tests, a regression
guard, a goal→check traceability matrix, and an unusually disciplined propose-only
meta-loop. What drags the grade down is that the four skills that do the actual work were
copied byte-for-byte from claude.ai and never adapted: they reference an environment that no
longer exists, route failures to a skill that was renamed, and the inner quality loop's core
mechanic ("revision mode") is commanded by the orchestrator but defined nowhere. There are
zero Critical findings in the security/data-corruption sense; the executable Python is
clean and safe. The top three risks: (1) the automatic Compose↔Edit loop rests on undefined
behavior, so the first real run will improvise exactly where the system is designed to
forbid improvisation; (2) the editor's only permitted voice reference is an explicit
scaffold, so goal 4b is enforced against starter rules, not the real canon; (3) nothing runs
the tests automatically and run artifacts are gitignored in an ephemeral container, so
regressions and evidence both die silently. The top three opportunities are cheap: small
prose patches fully specify the loop (the hard infrastructure already exists), a one-file CI
workflow wires up the existing test+regression suite in minutes, and a banned-list sync test
plus a fixture per fail-class cements the meta-loop's safety net before the first proposal
ever lands.

---

## Repo Map

**Purpose.** A personal content-production pipeline for SETI (the owner): turn an English
patent + cleaned figures into a publication-ready English essay for X Articles, in three
phases (Design → Compose → Edit) with an automated quality loop and a propose-only
self-improvement meta-loop. Converted from a system of separate claude.ai Projects
(`docs/source-prompts/README.md`).

**Stack.** Prose-as-code: 173 Markdown files (skill bodies, references, templates, voice
canon) executed by Claude Code, plus ~2,150 lines of Python 3 stdlib (6 gate scripts,
aggregator, test suite, regression guard — zero third-party dependencies, verified on
Python 3.11.15). No package manifest, lockfile, or build config exists, by design. No CI
config exists (no `.github/`). Bilingual Korean/English prose throughout is intentional
(SETI's working language; the voice canon includes `sig-ko-*` Korean signature patterns).

**Maturity.** Pre-first-run. `meta/findings-ledger.jsonl` is empty (0 lines), `runs/`
contains only `.gitkeep`, `meta/improvement-proposals/` contains only its README, and the
attribution table's recurrence ledger says "none yet — first run will populate"
(`meta/attribution-table.md:42`). All recommendations below are calibrated to a personal,
pre-first-run system — not a production service.

**Architecture / data flow.**

```
input/{patent.md, figures/, essay-context.md}
  → /patent-essay (orchestrator, .claude/skills/patent-essay/SKILL.md)
    → P1 thesis-architect (voice-off)  → handoff/01-design/*   (8 artifacts)
    → P2 essay-en-composer (voice-on, calls voice-canon-lookup) → handoff/02-compose/*
    → gates: .claude/skills/_shared/scripts/run_gates.py  (hard pass/fail)
    → P3 editorial-review (voice-fenced, 6 passes) → handoff/03-edit/edit-log.md
    → loop until PASS or --max-iter → handoff/03-edit/essay-final.md
  → archive runs/<essay-id>/ → pipeline-retro (propose-only meta-loop)
    → meta/findings-ledger.jsonl + meta/improvement-proposals/
```

**Key directories.**

| Path | One-liner |
|---|---|
| `.claude/skills/patent-essay/` | Orchestrator: loop policy, thresholds, archive, meta-loop trigger (new, written for this repo) |
| `.claude/skills/{thesis-architect, essay-en-composer, editorial-review, voice-canon-lookup}/` | The four phase skills — **byte-identical copies of the claude.ai originals** (verified, see H1/H3) |
| `.claude/skills/pipeline-retro/` | Propose-only meta-loop (new) |
| `.claude/skills/_shared/references/` | Shared canon: scoring-rubric + anti-ai-writing (real), deliverable-voice-rules + caption-roles + working-dialogue-voice (scaffolds) |
| `.claude/skills/_shared/scripts/` | 6 gates + runner + `banned_terms.txt` + 32-test suite (all passing, verified) |
| `.claude/skills/_shared/vendor/` | MIT-licensed AI-tell skills, absorbed-not-run, licenses retained |
| `handoff/`, `handoff-template/` | Runtime stage artifacts (gitignored) / full-schema templates |
| `runs/`, `meta/` | Per-run archives (gitignored) / persistent memory: ledger, attribution table, fixtures, regression guard |
| `docs/source-prompts/` | Verbatim claude.ai originals incl. unported Phase-4 `promo-composer` (frozen baseline by design) |
| `input/` | Per-run inputs (gitignored) |

**Surprises found during mapping.**
1. The "port" of the four phase skills was a pure copy: diffing every ported `SKILL.md` and
   every ported reference against `docs/source-prompts/` (CRLF-normalized) yields **0 changed
   lines** (verified). The conversion exists only in the new layers around them.
2. Three of five `_shared/references/` files are explicit scaffolds awaiting the real canon.
3. 65 files under `.claude/skills/` have CRLF line endings; there is no `.gitattributes`.
4. No root `README.md`, no `LICENSE`, no CI.
5. The system has never been run end-to-end (empty ledger, empty `runs/`).

---

## Audit Report

Findings are grouped by dimension and sorted by severity. **[F]** = verifiable fact,
**[J]** = judgment. There are **no Critical findings** (no security or data-corruption class
issue); the items marked High are the ones blocking the system's headline feature from
working as specified — they are the "ugly parts" needing utmost priority.

### Architecture & design

**H1 — High. The inner loop's core mechanic, "revision mode," is commanded but defined
nowhere.** [F] The orchestrator feeds failed-round findings "back to `essay-en-composer` in
**revision mode** — it revises `handoff/02-compose/` in place"
(`.claude/skills/patent-essay/SKILL.md:93-94`; also
`_shared/references/scoring-rubric.md:97-98`, `CLAUDE.md:100`). The composer defines only
walkthrough / strict-execution / pair modes (`essay-en-composer/SKILL.md:28-29`,
`references/mode-spec.md`); "revision" appears in its tree only as "blueprint revision —
return to essay-architect" (`references/execution-boundary.md:40,89,107`,
`references/mode-spec.md:60,73-74`) — and **no skill named `essay-architect` exists** (the
Phase-1 skill is `thesis-architect`). [J] Why it matters: in this repo, prose is the
executable. The LLM running Compose on round 2 has no spec for scope (which sections may
change?), constraints (may it introduce facts? re-run the strip pipeline?), or outputs — so
it will improvise, which is precisely the failure mode the gates/fencing/propose-only design
exists to prevent.

**H2 — High. Human-in-the-loop vs. auto-loop contradiction across phase boundaries.** [F]
`editorial-review` states the human applies findings: "SETI revises →
handoff/03-edit/essay-final.md" (`editorial-review/SKILL.md:17`), "Findings supply input for
SETI's revise decision. NOT auto-fix" (`:24`), "Auto-fix NOT performed (SETI decides which
findings to apply)" (`:90`). The orchestrator automates exactly that: the composer revises,
and the orchestrator "promote[s] the accepted draft to `handoff/03-edit/essay-final.md`"
(`patent-essay/SKILL.md:92-99`). Similarly, the composer's default mode (walkthrough)
expects live human catches mid-session ("please catch any voice, clarity, or thesis concerns
mid-session", `mode-spec.md:39`), which cannot happen in an orchestrated run, and the
orchestrator never specifies which composer mode automated runs should use. [J] An LLM
following `editorial-review` literally could stall the loop waiting for SETI, or refuse to
let the composer apply findings; whichever way it resolves, behavior is unspecified.

**H3 — High. Runtime skills reference the dead claude.ai environment.** [F] All four ported
skills carry Project-era preconditions that cannot be satisfied in Claude Code:
"`patent.md` uploaded to Phase 1 Project Knowledge" and "enforced by Phase 1 PI"
(`thesis-architect/SKILL.md:41,43`); "uploaded … to the Phase 2 Compose Project",
"`voice-canon-lookup` skill installed in same Project", "Phase 2 Knowledge files loaded: …"
(`essay-en-composer/SKILL.md:22,52,53`); "`patent.md` re-uploaded to Phase 3 Knowledge",
"enforced by the Phase 3 Project Instructions" (`editorial-review/SKILL.md:13-14,30,82-83`);
"Project Knowledge 의 `deliverable-voice-rules.md`" (`voice-canon-lookup/SKILL.md:82`). [J]
The executing LLM must guess the mapping (Knowledge → `_shared/references/`? uploads →
`input/`?) on every run; guesses will vary between runs and models.

**M1 — Medium. Broken file references: `x-article-format.md` (×3).** [F] Referenced at
`essay-en-composer/SKILL.md:53` and `editorial-review/SKILL.md:14,83`; no such file exists.
The real file is `essay-en-composer/references/x-articles-format-en.md` — which, for
editorial-review, additionally lives in *another skill's* tree with no path given. [J] The
editor's Pass 6 format check depends on this spec; an unresolvable reference invites the LLM
to substitute its own idea of X-Articles format.

**M2 — Medium. Load-bearing references are explicit scaffolds.** [F]
`deliverable-voice-rules.md:3` ("Status: SCAFFOLD + canon target … Replace the starter rules
with the user's canon"), `caption-roles.md:3`, `working-dialogue-voice.md:3`, each with a
`<!-- PORT: drop the user's … canon here -->` marker (`:29`, `:23`, `:21`). [J] Why it
matters: voice fencing makes `deliverable-voice-rules.md` the **only** voice document
Phase 3 may consult (`editorial-review/SKILL.md:30`); the editor is therefore judging goal 4b
against starter rules. CLAUDE.md presents the voice stack as operational without flagging
this.

**M3 — Medium. Stale v1 machinery referenced as live.** [F] 26 occurrences of the dead names
`essay-architect` / `tech-essay-en` / `tech-essay-ko` across 11 runtime files (grep,
verified); e.g. `thesis-architect/references/context-research.md:3` describes "Step 2 pool
admission proposals" although pool admission is explicitly dropped
(`editorial-review/SKILL.md:101-102`), and `mode-spec.md:3` says it is "Referenced by
tech-essay-en SKILL.md".

**M4 — Medium. `--mode wire` is advertised but unspecified.** [F] Exposed in `CLAUDE.md:31`,
the orchestrator's argument hint (`patent-essay/SKILL.md:10`), and reserved as pass-through
in `run_gates.py:117-118`; no skill or reference defines what wire mode changes
(`voice-profile.md:267-269,469` describes what a Wire *is* editorially, but nothing
operationalizes it). [J] A wire-mode run would be improvised end to end.

**L1 — Low. `input/essay-context.md` is declared but never consumed.** [F] Named as an input
at `patent-essay/SKILL.md:28` and `CLAUDE.md:34,72`; no phase skill mentions reading it
(grep, verified).

**L2 — Low (managed risk, not a defect). ~70-file intentional duplication.** [F]
`.claude/skills/` content is duplicated verbatim in `docs/source-prompts/` as a frozen
baseline (`docs/source-prompts/README.md`). [J] Fine today; the moment H1–H3 fixes land, the
trees diverge by design — the README already frames source-prompts as the historical record,
so no sync obligation should ever be implied.

### Code quality (Python)

The gate scripts are well above typical glue-script quality: documented format assumptions,
tunable constants at top of file, a uniform `check(draft_text, context) -> findings` contract
(`_shared/scripts/README.md:42-51`), and conservative false-positive policy. Remaining
findings:

**M5 — Medium. `_parse_figures_file` crashes on plausible LLM-written input.** [F]
`run_gates.py:53` and its duplicate `gate_anchors.py:126` call `int(tok)` with no error
handling; a `figures-index.txt` containing `fig-01` — the repo's *own* figure naming
convention (`input/figures/fig-NN.png`) — raises an uncaught `ValueError` (verified
empirically). [J] The orchestrator LLM writes this file (`patent-essay/SKILL.md:43-45`);
format drift is the expected failure mode, and a traceback mid-loop is much harder for the
orchestrator to recover from than a fail-finding.

**M6 — Medium. Quote masking has verified false-positive edges.** [F] Masking is per-line and
straight-quotes-only (`gate_emdash.py:40-59`, duplicated `gate_banned.py:59-71`). Verified:
(a) a double-quoted span wrapping a line boundary → the em-dash inside the quote on line 2 is
flagged EMDASH-001; (b) curly quotes `“…”` are not recognized → a quoted em-dash and a quoted
banned word are both flagged (empirical probes). [J] Mitigation exists only as a convention
for *patent extraction* (smart→straight normalization,
`thesis-architect/references/quote-anchor-conventions.md:77`); nothing stops the composer
emitting curly quotes in its own prose. Failures are conservative (false fail, never false
pass), so the cost is burned loop iterations and confusing feedback, not shipped violations.

**L3 — Low. Malformed `re:` line in `banned_terms.txt` crashes all gates.** [F]
`gate_banned.py:50` compiles user-maintained regex with no `re.error` handling; the file is
designed to be hand-extended via meta-loop proposals (`banned_terms.txt:9-11`).

**L4 — Low. Helper duplication across gates.** [F] `_report()` ×6 (`gate_emdash.py:103`,
`gate_anchors.py:130`, `gate_sources.py:140`, `gate_banned.py:108`, `gate_structure.py:155`,
`gate_figure_use.py:86`), `_mask_quoted_spans` ×2, `_parse_figures_file` ×2. [J] Deliberate
standalone-script design and acceptable at this scale; the one real risk is the two masking
implementations drifting apart (see M6 fix).

**L5 — Low. `gate_anchors` does not exempt code fences or quotes** (`gate_anchors.py:62-71`),
so `[dddd]`-like tokens in fenced blocks are chain-checked. [F] Conservative direction;
essays rarely contain code.

**L6 — Low. Off-by-one in `gate_sources` location strings.** [F] `start` is a 0-based index
of the line after the header, printed directly as a 1-based line number
(`gate_sources.py:117-123,126-134`). Cosmetic.

### Security

Healthy for this project class, in brief: no secrets (scanned, verified), zero third-party
dependencies, no network calls in scripts, JSON-only parsing, `subprocess.call` without
`shell=True` (`meta/regression.py:47`).

**L7 — Low. No untrusted-input guidance for the LLM layer.** [F] `patent.md` is third-party
text and `thesis-architect` ingests live web-search results (`SKILL.md:27`); no skill
instructs treating that content as data rather than instructions. [J] For a personal pipeline
the blast radius is content integrity and whatever tools the session permits — one sentence
in the orchestrator and thesis-architect would cover it.

### Testing

**M7 — Medium. The safety net exists but nothing runs it.** [F] No CI of any kind (no
`.github/`, verified); `test_gates.py` (32 tests, all passing — verified) and
`meta/regression.py` (gate suite + 2 fixtures, passing — verified) run only when someone
remembers. [J] The meta-loop's whole apply-a-proposal protocol hinges on the regression guard
(`meta/improvement-proposals/README.md:6-8`); unenforced, it will eventually be skipped.

**L8 — Low. Fixture coverage is 2 of ~8 hard-fail classes.** [F] `meta/fixtures/` holds
`clean-baseline` and `figure-orphan` only; hard-fail checks EMDASH-001, ANCHOR-001/002,
FIGREF-001, SOURCES-001/002/003, BANNED-001 have no fixture. [J] Designed to grow organically,
but pre-seeding one per class makes the guard meaningful before the first proposal.

**L9 — Low. Edge-case test gaps mirror M5/M6/L3.** [F] No tests for multi-line quotes, curly
quotes, malformed figures files, or malformed banned-terms regex (all verified to misbehave
above). The banned-list canon↔mirror sync (`anti-ai-writing.md:101-105`,
`banned_terms.txt:9-11` both assign the duty manually) has no mechanical check — currently in
sync (verified: 25 literals + patterns match), and the only thing keeping it so is diligence.

### Performance

Healthy: kilobyte-scale text inputs, stdlib regex, no unbounded growth surfaces; per-call
pattern recompilation in `gate_banned.py:79-80` is irrelevant at this scale. No findings.

### Dependencies

Healthy and notably disciplined: zero runtime dependencies; vendored skills retain upstream
MIT licenses with an explicit absorbed-not-run policy and refresh procedure
(`_shared/vendor/README.md:6-25`).

**L10 — Low. No repo-level LICENSE or rights statement.** [F] Vendor licenses are tracked but
the repository's own content — including SETI's voice canon, which is personal IP — carries no
notice. [J] Needs an intentional owner decision, especially if the repo is or becomes public.

### DevEx & operations

**M8 — Medium. Ephemeral-runtime data-loss path.** [F] `handoff/**` and `runs/**` are
gitignored (`.gitignore:1-6,15-19`) while the documented runtime is Claude Code web
(`CLAUDE.md:1`), where containers are reclaimed after inactivity. [J] Consequences: an
interrupted run loses all hand-off state, making the `/goal` auto-resume backstop
(`patent-essay/SKILL.md:123-130`) ineffective across container loss; and the run archives
that constitute the evidence chain behind improvement proposals (`runs/<id>/gate-result.json`,
`pipeline-retro/SKILL.md:40-41`) evaporate, leaving only the normalized ledger.

**L11 — Low. Mixed line endings, no `.gitattributes`.** [F] 65 CRLF files under
`.claude/skills/` (verified; e.g. `voice-canon/index.yaml`); this audit's own diff tooling
tripped on it, and exact-string Edit operations will too.

**L12 — Low. Inconsistent gate invocation path in docs.** [F]
`scoring-rubric.md:49` says `python _shared/scripts/run_gates.py` (only resolves from inside
`.claude/skills/`); the orchestrator correctly uses the repo-root path
(`patent-essay/SKILL.md:66`).

**L13 — Low. No root `README.md`.** [F] GitHub renders nothing on the landing page; the
excellent CLAUDE.md is invisible there.

### Documentation

**M9 — Medium. CLAUDE.md overstates conversion completeness.** [F] "The real skill bodies
have been ported into `.claude/skills/`" (`CLAUDE.md:8-9`) is literally true but the bodies
are unmodified copies (verified, 0 changed lines) that contradict the automated loop the same
document advertises (`CLAUDE.md:98-101`). [J] In a prose-executed system, a doc/code
contradiction *is* a code/code contradiction; this is the documentation face of H1–H3.

Otherwise documentation is a strength: CLAUDE.md, the scripts README, the vendor README, the
proposals README, and the handoff templates are accurate, current, and unusually explicit
about intent (verified spot-checks: severity enum identical across
`scoring-rubric.md:60-67`, `editorial-review/references/feedback-format.md:12,84-86`, and
`handoff-template/03-edit/edit-log.md:19`; gate table in scripts README matches
implementations).

### Strengths (what to preserve)

1. **Deterministic gate layer**: clean stdlib code, uniform contract, documented format
   assumptions, tunable constants, conservative false-positive philosophy stated in canon
   (`anti-ai-writing.md:86-91`).
2. **Goal→check traceability matrix** (`scoring-rubric.md:19-28`) — every check defends a
   named acceptance goal; rare discipline at any scale.
3. **Two-tier loop design with propose-only meta-loop**, regression guard, cascade cap, and
   audit-trail rules (`pipeline-retro/SKILL.md:31-36,71-83`) — a thoughtfully engineered
   anti-drift architecture.
4. **Voice fencing** specified architecturally and *encoded in the attribution routing* so
   the meta-loop cannot propose breaking it (`meta/attribution-table.md:8-10`).
5. **Canon↔gate mirroring** currently in perfect sync (25 banned words + patterns, verified)
   with the sync duty documented at both ends.
6. **Vendoring hygiene**: licenses retained, absorbed-not-run rationale, upstream links,
   alternatives documented (`_shared/vendor/README.md`).
7. **Consistency elsewhere**: voice-canon `index.yaml` ↔ 33 entry files exactly consistent
   (verified); severity model consistent across three documents; `.gitignore` rationale
   written down (`.gitignore:15-17`).

---

## Improvement Strategy

### Theme 1 — Finish the conversion: make the prose executable in *this* environment
(covers H1, H2, H3, M1, M3, M4, M9, L1)

**Target state:** every runtime skill speaks Claude Code — explicit repo paths instead of
"Project Knowledge", a defined revision mode with scope/constraints/outputs, no references to
nonexistent skills or files, an orchestrator that names the composer mode for automated runs,
and an editorial skill that distinguishes orchestrated runs (composer applies findings) from
standalone runs (SETI applies findings). **Principle:** in an LLM pipeline, ambiguity in
prose is undefined behavior in code; this repo's own design philosophy (gates, fencing,
propose-only) already says so — the skills just haven't caught up. The frozen
`docs/source-prompts/` baseline exists precisely so the live copies can be edited without
losing the originals.

### Theme 2 — Wire the existing safety net to something that pulls it
(covers M7, L8, L9)

**Target state:** a single GitHub Actions workflow runs `test_gates.py` + `meta/regression.py`
on every push/PR (stdlib-only, <1 minute); one fixture per hard-fail check_id; a sync test
that parses the Tier-1 block of `anti-ai-writing.md` and diffs it against `banned_terms.txt`.
**Principle:** the meta-loop's contract ("apply only after regression passes") is only as
strong as its weakest manual step.

### Theme 3 — Gates should fail loudly, never crash, on LLM-written inputs
(covers M5, M6, L3, L5)

**Target state:** malformed context files (figures index, banned-terms regex) produce a
fail-severity finding naming the bad line, not a traceback; quote masking recognizes curly
quotes; the masking helper lives in one place. **Principle:** every input to the gates is
written by an LLM mid-loop; the realistic failure mode is format drift, and the gate's job is
to convert that into actionable findings.

### Theme 4 — Operational fit for an ephemeral runtime
(covers M8, L11, L13, L10)

**Target state:** run archives (`runs/`) are committed after each essay (they are the
evidence chain; the ledger already is committed), hand-off state remains ephemeral but the
orchestrator commits the archive step explicitly; `.gitattributes` pins LF for the runtime
tree while leaving `docs/source-prompts/` byte-frozen; a root README points humans at
CLAUDE.md; the owner makes a license decision.

### What I recommend NOT fixing (explicit trade-offs)

- **Helper duplication across gates (L4)** beyond unifying the quote masker: the
  standalone-script property (each gate runnable with zero imports beyond stdlib) is worth
  more than DRY here.
- **No packaging/pyproject/linting toolchain:** ~2k lines of stdlib scripts in a personal
  repo don't earn a build system. A CI job calling two scripts is the right ceiling.
- **Porting `promo-composer` (Phase 4):** explicitly out of scope per
  `docs/source-prompts/README.md`; don't let it ride along with the conversion fixes.
- **Normalizing or editing `docs/source-prompts/`:** it is the verbatim historical record;
  changing even line endings would destroy its one job.
- **Korean/English mixed prose:** it is the owner's working language and part of the voice
  system, not a defect.
- **`gate_anchors` fence-exemption (L5) and the Sources off-by-one (L6):** fix
  opportunistically; both fail conservative and cost nothing today.

### What "done" looks like (measurable signals)

1. CI badge green on every push; the workflow fails if `test_gates.py` or
   `meta/regression.py` fails.
2. `grep -rn "essay-architect\|tech-essay-en\|x-article-format.md\|Project Knowledge\|re-uploaded" .claude/skills/` returns zero hits.
3. "Revision mode" has a section in `essay-en-composer` (or a dedicated reference) defining
   inputs, scope, constraints, and outputs; the orchestrator and scoring-rubric link to it.
4. Gates never raise an uncaught exception for any text input: malformed-input fixtures exist
   and assert fail-findings, not tracebacks.
5. One fixture per hard-fail check_id under `meta/fixtures/` (≥8 fixtures).
6. An end-to-end dry run on a sample patent completes all three phases plus one revision
   round without the executing LLM having to invent any step.

---

## Task Plan

Effort: S < 2h · M ≈ half-day · L ≈ 1–2 days.

### Milestone 0 — Safety net (before touching skill prose)

| # | Task | Files/areas | Acceptance criteria | Effort | Risk | Depends |
|---|---|---|---|---|---|---|
| T1 | **Add CI workflow** running `test_gates.py` + `meta/regression.py` on push/PR | `.github/workflows/gates.yml` | Workflow runs on push; red on injected test failure; <2 min | S | Low | — |
| T2 | **Fixture per hard-fail class** (EMDASH-001, ANCHOR-001, ANCHOR-002, FIGREF-001, SOURCES-001/002/003, BANNED-001) | `meta/fixtures/*/` | `regression.py` exercises ≥8 fixtures; each asserts its `must_contain_check_ids` | M | Low | — |
| T3 | **Banned-list sync test**: parse `anti-ai-writing.md` Tier-1 code block ↔ `banned_terms.txt` literals | `_shared/scripts/test_gates.py` (new test class) | Removing a word from either file fails the suite | S | Low | — |
| T4 | **`.gitattributes` + LF-normalize the runtime tree only** (leave `docs/source-prompts/` untouched) | `.gitattributes`, 65 files under `.claude/` | `grep -rlI $'\r' .claude/` empty; `git diff -w` shows no content change; source-prompts byte-identical | S | Med (touches many files — verify with whitespace-blind diff) | T1 |

### Milestone 1 — Correctness of the pipeline-as-code

| # | Task | Files/areas | Acceptance criteria | Effort | Risk | Depends |
|---|---|---|---|---|---|---|
| T5 | **Define revision mode** in the composer | `essay-en-composer/SKILL.md` + new `references/revision-mode.md`; link from `patent-essay/SKILL.md:93`, `scoring-rubric.md:97` | Spec covers inputs (edit-log findings + failing check_ids), scope (only sections cited in findings), constraints (no new facts beyond Quotable spans/fact-check-log; strip pipeline re-run; publication.md regenerated), outputs (same contract, `draft_version` incremented) | M | Med (prose change alters composer behavior — gate with T1/T2 + T16 dry run) | T1,T2 |
| T6 | **De-claude.ai-ify the four ported skills**: Project Knowledge → explicit repo paths; "re-uploaded" → `input/patent.md`; fix `x-article-format.md` → `essay-en-composer/references/x-articles-format-en.md` (give editorial-review the cross-skill path); `essay-architect` → `thesis-architect` or "internal blueprint revision"; excise pool-admission residue in `context-research.md` | `thesis-architect/SKILL.md:41,43`; `essay-en-composer/SKILL.md:22,52-53`; `editorial-review/SKILL.md:13-14,30,82-83`; `voice-canon-lookup/SKILL.md:82`; `execution-boundary.md`, `mode-spec.md`, `context-research.md` | "Done" signal #2 grep returns zero hits; output contracts unchanged | L | Med (largest prose surface; originals stay frozen in docs/source-prompts as rollback) | T1,T2,T4 |
| T7 | **Reconcile auto-loop vs SETI-applies**; orchestrator names composer mode for automated runs (recommend `strict-execution` + measured) | `editorial-review/SKILL.md` (orchestrated vs standalone behavior), `patent-essay/SKILL.md` Phase-2 section | editorial-review states: orchestrated runs → composer applies findings via revision mode, SETI override always wins; orchestrator specifies mode | S–M | Low | T5 |
| T8 | **Gate robustness**: figures-parse ValueError → fail finding; `re.error` in banned loader → fail finding naming the line; recognize curly quotes in masking; unify the masker into one shared helper imported by both gates | `run_gates.py:46-54`, `gate_anchors.py:119-127`, `gate_banned.py:36-56,59-71`, `gate_emdash.py:40-59` + tests | The four empirical probes from this audit become passing tests; no input text can raise an uncaught exception | M | Low | T1,T2 |
| T16 | **End-to-end dry run** on a sample patent; archive as the first `runs/` entry | `input/` (sample), full pipeline | All 3 phases + ≥1 revision round complete without the LLM inventing steps; SCORE HISTORY produced; ledger gets first entries | M | Low | T5–T8 |

### Milestone 2 — High-leverage improvements

| # | Task | Files/areas | Acceptance criteria | Effort | Risk | Depends |
|---|---|---|---|---|---|---|
| T9 | **Root README.md** (purpose, quickstart, pointer to CLAUDE.md + scripts README) | `README.md` | Landing page renders; no duplication of CLAUDE.md content beyond a summary | S | Low | — |
| T10 | **Persistence policy for `runs/`**: stop ignoring `runs/**`; orchestrator archive step commits the run | `.gitignore:15-19`, `patent-essay/SKILL.md:106-108` | A completed run's `edit-log.md`/`gate-result.json`/`score-history.md` survive container reclamation | S | Low | owner answer (OQ3) |
| T11 | **Replace the three scaffold references with real canon** (deliverable-voice-rules, caption-roles, working-dialogue-voice) | `_shared/references/*` | SCAFFOLD banners removed; rules concrete enough that Pass 1/Pass 6 cite rule IDs | L | Med (changes editorial behavior) | owner input (OQ2) |
| T12 | **`essay-context.md`: plumb or remove** — recommend plumbing into thesis-architect Step 2 (context research) | `thesis-architect/SKILL.md`, `patent-essay/SKILL.md:28` | Either consumed by a named step or absent from all docs | S | Low | T6 |
| T17 | **Specify or remove `--mode wire`** — recommend a one-page `wire-mode` reference (length target, section count, gate deltas if any) or deletion from the CLI surface until specified | `patent-essay/SKILL.md:10`, `CLAUDE.md:31`, `run_gates.py:117`, composer refs | Wire runs have a spec, or the flag is gone everywhere | M | Low | T6 |

### Milestone 3 — Quality & polish

| # | Task | Files/areas | Acceptance criteria | Effort | Risk | Depends |
|---|---|---|---|---|---|---|
| T13 | Fix `scoring-rubric.md:49` invocation path; `gate_sources` location off-by-one; note duplicate-header behavior in its docstring | `scoring-rubric.md`, `gate_sources.py:117-134` | Paths copy-paste-run from repo root; locations 1-based | S | Low | — |
| T14 | **License / rights statement** per owner decision | `LICENSE` or notice in README | Intentional statement exists, esp. covering the voice canon | S | Low | OQ4 |
| T15 | One-line untrusted-input guidance in orchestrator + thesis-architect (treat patent/web text as data, not instructions) | `patent-essay/SKILL.md`, `thesis-architect/SKILL.md` | Sentence present in both | S | Low | T6 |

### Quick wins (high impact, S effort — do immediately)

- **T1 (CI)** — turns 32 existing tests + the regression guard from optional to enforced.
- **T3 (sync test)** — locks the canon↔gate mirror that currently survives on diligence.
- **T9 (README)** — the repo currently renders blank on GitHub.
- **T12 (essay-context)** and **T13 (path fixes)** — minutes each.
- The figures-parse and regex-error halves of **T8** are each ~20 lines + tests.

### Implementation sketches — top 3 tasks

**T5 — Define revision mode.**
Approach: add `references/revision-mode.md` to the composer rather than bloating SKILL.md;
make it a *fourth mode category* entered only when the invocation provides an edit-log.
Key steps: (1) define inputs: `handoff/03-edit/edit-log.md` findings + failing gate
`check_id`s; (2) scope rule: only sections named in findings' `location` fields may change,
plus mechanical global fixes (em-dash, banned term) anywhere; (3) constraints: the Plan ⊥
Execute boundary still applies — no facts beyond Quotable spans + fact-check-log; the
voice-canon anchor per section is preserved unless the finding targets it; (4) outputs: same
four files, `draft_version: N+1`, strip pipeline re-run so `publication.md` never goes stale;
(5) update `patent-essay/SKILL.md:93` and `scoring-rubric.md:97` to link the new reference.
Gotchas: don't let revision mode re-open thesis selection (a pass-4 spine-misalignment
finding routes to design ownership per `attribution-table.md:26` — in-loop, the composer
should surface "needs Phase-1 revision" and stop rather than improvise a new spine, mirroring
the existing "spine gaps stop composition" rule at `essay-en-composer/SKILL.md:43`).

**T6 — De-claude.ai-ify the ported skills.**
Approach: mechanical translation pass with a fixed substitution table, one skill per commit so
each diff is reviewable against the frozen original. Table: "uploaded to Phase N Project
Knowledge" → "present at `<repo path>`"; "re-uploaded" → "read from `input/patent.md`";
"Knowledge files loaded: X" → "references loaded: `<explicit path>` per the voice-fencing
table in CLAUDE.md"; "Phase N Project Instructions / PI" → "this SKILL.md"; "installed in
same Project" → "available as a sibling skill"; `x-article-format.md` →
`essay-en-composer/references/x-articles-format-en.md`; `essay-architect` →
`thesis-architect` where it means Phase 1, → "internal blueprint revision" where it means the
composer's own Step-3 blueprint (`execution-boundary.md:89` context decides which). Gotchas:
`context-research.md:3`'s "pool admission proposals" is dropped machinery — delete the
sentence, don't translate it; keep every output contract line untouched (the hand-off paths
are already correct); run the "done" grep from strategy signal #2 as the acceptance check.

**T1 — CI workflow.**
Approach: single job, no dependencies to install.
```yaml
# .github/workflows/gates.yml
on: [push, pull_request]
jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: python .claude/skills/_shared/scripts/test_gates.py
      - run: python meta/regression.py
```
Gotchas: `regression.py` already runs the test suite as a subprocess
(`meta/regression.py:43-48`), so the two steps overlap — keep both anyway: the first gives a
clean failure signal if the suite itself is broken, the second proves the fixture path works.

---

## Open Questions (need a human decision)

1. **OQ1 — Loop autonomy at publication:** the orchestrator auto-promotes the accepted draft
   to `essay-final.md`. Should a human approval step remain before "final" (the original
   system's posture), or is full-auto intended? T7's wording depends on this; my default
   recommendation in T7 assumes full-auto per CLAUDE.md with SETI override.
2. **OQ2 — Canon for the three scaffolds:** only SETI can supply the real
   `deliverable-voice-rules` / `caption-roles` / `working-dialogue-voice` content (T11).
   Possible source: distill from `voice-profile.md` + published essays — but that's an
   editorial decision, not an engineering one.
3. **OQ3 — Run-archive persistence:** commit `runs/<essay-id>/` (recommended in an ephemeral
   container; it is the proposals' evidence chain) or keep ephemeral by intent?
4. **OQ4 — License/visibility:** is this repo meant to stay private? The voice canon is
   personal IP; if the repo is or becomes public, an explicit rights statement matters (T14).
5. **OQ5 — Wire mode:** is `--mode wire` worth specifying now (T17), or should the flag be
   removed until a wire run is actually wanted?

---

*Lighter-review areas: the 33 voice-canon entry bodies and the Phase-4 `promo-composer`
source were skimmed for structure/consistency only (content is editorial canon, out of audit
scope); `handoff-template/` files were spot-checked against the schemas the skills cite, not
line-audited. Everything else above received full review.*
