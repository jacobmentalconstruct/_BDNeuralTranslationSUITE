# BDNeuralTranslationSUITE — Project Backlog

_Last updated: 2026-03-28. Mirrored in journal as entry `journal_backlog_001`. Use `_docs/WE_ARE_HERE_NOW.md` as the fastest pickup note after interruption._

---

## Current Footing

Phase 1 baseline is complete and runnable:
- Splitter → NDJSON → Emitter → Nucleus → Cold Artifact works
- Bootstrap Nucleus is live
- App Journal is installed and verified
- Root docs now carry an explicit recovery checkpoint and root architecture note

The project is now pointed at a solid prototype path, not at open-ended invention.

---

## Tranche 9 — Recovery Checkpoint + Doctrine Lock ✅ (2026-03-27)

- [x] Added root [`_docs/ARCHITECTURE.md`] — authoritative architecture truth for the active project line
- [x] Added root [`_docs/WE_ARE_HERE_NOW.md`] — overwrite-at-each-milestone crash-recovery / onboarding note
- [x] Re-centered backlog and dev log on the current root project rather than the old `final/` staging layout
- [x] Recorded current sequencing doctrine:
  - neurons first
  - living graph second
  - bag seam third
- [x] Recorded explicit non-goals so the project does not drift into FFN or bag work too early
- [x] Captured the latest Emitter UI lifecycle cleanup in the active project memory surfaces

---

## Tranche 10 — Splitter Corpus Hardening ACTIVE

Goal: turn the Splitter from “runnable baseline” into a trustworthy neuron-population substrate using real corpus passes.

### Immediate tasks

- [ ] Run `info` and `stream` passes against `_corpus_examples/python-3.10.20-docs-text`
- [ ] Run `info` and `stream` passes against `_corpus_examples/python-3.11.15-docs-text`
- [x] Run a baseline prose ingest against `_corpus_examples/webstersdictinoary.txt`
- [x] Start a recorded corpus metrics table in `_docs/SPLITTER_CORPUS_BASELINES.md`
- [ ] Capture richness / node-kind / engine-mix observations for each corpus
- [ ] Identify the weakest surface populations by corpus and file type
- [ ] Improve TreeSitter / PEG / fallback seams where output is thin, noisy, or obviously mis-shaped
- [x] Push representative corpus output through the Emitter and inspect resulting graph/training-pair quality
- [x] Record graph probe results in `_docs/GRAPH_PROBES.md`
- [x] Establish a repeatable probe-report loop with `.dev-tools/final-tools/tools/graph_probe_report.py`
- [x] Expose bootstrap scaffold dials through Emitter CLI + optional JSON profile
- [x] Persist `bootstrap_profile_effective.json` with emit/probe artifacts
- [x] Add emitter-local tests for bootstrap config validation and scaffold behavior
- [x] Add a tracked starter tuning profile for Python reference probe work
- [x] Add a builder-only probe monitor with live event/log capture and optional tiny monitor UI

### Immediate follow-up fork

- [ ] Decide whether to improve NL/list/index representation one more step before more Emitter work
- [x] If staying in Emitter next: inspect whether prose-heavy bootstrap routing is too grammar-dominant
- [x] After the next targeted change, run Probe 002 and compare it against Probe 001 mechanically
- [x] Moderate the first bootstrap de-bias pass so relation volume recovers without returning to grammar collapse
- [x] Test whether edge-threshold retuning is needed once prose grammatical matching is less absolute
- [x] Run Probe 003 with the tracked starter profile
- [ ] Improve cross-document pull recovery while keeping `grammatical_dominant` well below Probe 001
- [ ] Decide whether Probe 003 should be the new tuning baseline or whether one more starter-profile pass is needed first
- [x] Run Probe 004 through `.dev-tools/final-tools/tools/probe_monitor.py` so the next tuning pass is both observable and reproducible
- [x] Confirm Probe 004 matches the Probe 003 footing and can serve as an observable replay baseline
- [x] Run Probe 005 through `.dev-tools/final-tools/tools/probe_monitor.py` after one targeted profile change
- [x] Run Probe 006 through `.dev-tools/final-tools/tools/probe_monitor.py` after one heading-targeted profile change
- [x] Fix the builder monitor `hold_open` lifecycle by isolating the tiny Tk viewer in its own helper process
- [ ] Decide whether the next cross-document pull attempt should be a bootstrap-code dial rather than another profile-only retune

### Exit criteria

- [ ] At least one code-heavy corpus and one prose-heavy corpus ingest cleanly
- [ ] Grammatical and structural richness are meaningfully above all-fallback baseline where richer parsers apply
- [ ] Representative output survives Splitter → Emitter handoff without schema/path surprises
- [ ] We have a small, real training batch worth keeping for later FFN work

---

## Prototype Path After Tranche 10

### Tranche 11 — Graph Validation + Retrieval Sanity
- [ ] Inspect Cold Artifact output on real ingests
- [ ] Verify routing profiles and edge reasons are useful to a human/agent inspector
- [ ] Tighten schema/versioning/query seams only where real corpus behavior demands it

### Tranche 12 — FFN Training Data Discipline
- [ ] Define training-record quality checks
- [ ] Define evaluation metrics and bootstrap-vs-FFN comparison method
- [ ] Export and curate enough interaction data to justify FFN bring-up

### Tranche 13 — First FFN Nucleus Prototype
- [ ] Implement the first learned scorer
- [ ] Compare against bootstrap behavior before allowing it to replace the bootstrap path

### Tranche 14 — Bag Seam Prototype
- [ ] Define the bag as the STM falloff membrane into the durable graph
- [ ] Prove capture, listing, resurfacing, and context rehydration

---

## Explicit Non-Goals Right Now

- [ ] Do not implement the bag yet
- [ ] Do not implement the FFN yet
- [ ] Do not do broad retrieval redesign before corpus-driven graph validation
- [ ] Do not treat long-form historical docs as the primary truth over `_docs/ARCHITECTURE.md` and `_docs/WE_ARE_HERE_NOW.md`

---

## Known Technical Debt

| Item | Component | Priority | Notes |
|---|---|---|---|
| Keep shared and local contract copies synchronized | Both | Pre-ship | The shared `contract/` design surface and the component-local copies can drift. Any contract evolution must be mirrored deliberately before shipping standalone cuts. |
| Token budget uses char-estimate, not real tokenizer | Splitter | Phase 2 | `negotiator.py` still estimates tokens via character count. Real BPE tokenizer integration should wait until corpus/training artifacts are stable enough to justify it. |
| `_merge_hunk_stream` position heuristic | Splitter | Low | Secondary-engine hunk matching still relies on `document_position` tolerance. Good enough for now, but content-hash matching may be needed after larger corpus passes. |
| Cold Artifact schema evolution needs versioning discipline | Emitter | Medium | Future query/index work should be versioned deliberately rather than patched ad hoc. |
| Historical `final/...` path language remains in long-form docs and journal history | Root docs + journal | Low | This is mostly historical drift, not runtime risk. Keep active truth in the new root docs and normalize long-form/historical surfaces gradually. |
| `_docs/_BagOfEVIDENCE.md` is legacy, not active architecture truth | Root docs | Low | Keep as historical context for now, but do not let it compete with the current neuron/graph/bag doctrine. Archive or relocate later if it keeps confusing pickup flow. |

---

## Compliance Checklist (per builder contract)

- [x] Root `_docs/ARCHITECTURE.md` exists
- [x] Root recovery note `_docs/WE_ARE_HERE_NOW.md` exists
- [x] `_docs/builder_constraint_contract.md` exists
- [x] Component builder contracts exist in both component `_docs/` folders
- [x] `SOURCE_PROVENANCE.md` exists in both component `_docs/` folders
- [x] App journal install verified — manifest, DB, launcher path, and MCP smoke pass
- [x] App journal backlog mirror exists (`journal_backlog_001`)
- [x] Root docs now identify active truth surfaces and current next tranche
- [ ] Long-form historical docs and journal exports still need gradual normalization away from `final/...` language
