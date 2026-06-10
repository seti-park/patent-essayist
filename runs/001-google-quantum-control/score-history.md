# Score history — 001-google-quantum-control

Patent: US 12,652,259 B1 "Quantum control signal generation" (Google LLC; Bardin, Fatemi).
Thesis (locked, Q7 = technical-impossibility): qubit control does not need fast arbitrary
waveform generation; pre-built calibrated DC currents at 3 K summed by a sub-2-ns switch
network replace the room-temperature DAC + attenuator chain.
Run parameters: threshold=pass, max-iter=4, composer mode strict-execution + measured.

| iter | overall_assessment | gates (failing check_ids) | result | note |
|---|---|---|---|---|
| 1 | revise-recommended | none | FAIL (threshold=pass) | 1 medium (pass-2 §3 paragraph tangle) + 5 low (superlative, [0026] modality flattening, ISSCC attribution, 2 mobile walls, Sources descriptive title) → revision mode |
| 2 | pass | none | **PASS** | all 6 round-1 findings verified-fixed; no new findings; loop ends |

Pipeline incident (iter 1, outside the round result): the documented gate invocation
(`--figure-selection handoff/01-design/figure-selection.md`) ingested the full 17-sheet
mapping table as the "selected" set and reported 10 false FIGUSE-001 orphans; the
orchestrator re-ran against a `## Selected figures`-only slice
(`figure-selection-gate.md`) → all gates PASS, zero findings. Related: `FIG. 3A` /
`FIGS. 3B-3D` sub-letter forms are invisible to the gate regex; sheet filenames
(`fig-16.jpg`) parse as figure numbers. Logged to the ledger; proposal filed.

Final: draft_version 2 promoted to handoff/03-edit/essay-final.md (archived here);
body ~2,260 words + Sources (7 entries, 5 categories); figures FIG. 1, 9, 3A, 3B-3D, 8.
