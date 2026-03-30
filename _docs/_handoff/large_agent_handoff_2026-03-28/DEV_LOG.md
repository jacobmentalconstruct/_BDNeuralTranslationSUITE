# BDNeuralTranslationSUITE — Dev Log

_Last updated: 2026-03-28. Journal mirror lives in `_docs/_journalDB/app_journal.sqlite3`._

---

## 2026-03-27 — Recovery checkpoint + doctrine lock

Journal entry: `journal_resume_checkpoint_20260327`

- Re-centered the active project truth on the current repo root after the old `final/` move-up.
- Added root [`_docs/ARCHITECTURE.md`] as the authoritative architecture note for the active line.
- Added root [`_docs/WE_ARE_HERE_NOW.md`] as the fastest cold-start / crash-recovery note.
- Rewrote the backlog so it points forward to Splitter corpus hardening instead of lingering in “cleanup just happened” mode.
- Captured the current sequencing doctrine explicitly:
  - neurons first
  - living graph second
  - bag seam third
- Captured current non-goals explicitly:
  - no FFN work yet
  - no bag implementation yet
  - no broad retrieval redesign yet
- Recorded that the Emitter UI lifecycle/threading path was cleaned so worker-thread UI updates are queued back onto the main Tk thread safely.
- Left long-form historical docs in place, but demoted them behind the new active truth surfaces so resuming later will be much cleaner.

## 2026-03-27 — Splitter corpus baseline 001

Journal entry: `journal_splitter_corpus_baseline_001`

- Began Tranche 10 with real corpora instead of synthetic smoke only.
- Ran the Splitter against the Webster dictionary corpus as the prose-floor baseline.
- Confirmed Webster should remain `FallbackEngine` only, then fixed fallback provenance so emitted hunks now stamp `extraction_engine="FallbackEngine"` instead of leaving it blank.
- Ran routing inspection on the Python 3.11 reference docs and confirmed the initial problem: structured `reference/*.txt` documents were collapsing to fallback-only.
- Extended the PEG path so it can recognize structured `.txt` docs using underlined heading syntax rather than requiring only `.md` / `.markdown`.
- Confirmed `lexical_analysis.txt` now routes as `PEGEngine` + `FallbackEngine`, with emitted `md_heading` hunks and populated `heading_trail` instead of all-fallback paragraphs.
- Added `_docs/SPLITTER_CORPUS_BASELINES.md` as the running metrics/observations table for corpus hardening work.
- Remaining weak spots identified immediately:
  - `grammar.txt` and `index.txt` still route fallback-only in the sampled Python reference set
  - one `md_list` artifact remains in the `lexical_analysis.txt` sample and should be inspected later

## 2026-03-27 — Graph probe 001 (Python reference full-pipe)

Journal entry: `journal_graph_probe_001`

- Ran the improved Python reference corpus through the full Splitter → Emitter pipeline.
- Probe artifacts written under `_docs/_analysis/reference_probe_001/`.
- Full-pipe summary:
  - `1102` hunks ingested
  - `1083` content nodes
  - `22406` relations
  - `53825` training pairs
- Confirmed the stronger NL/document path is affecting the graph rather than dying at the handoff:
  - `1293` cross-document nucleus pull edges were created
- Confirmed the current bootstrap nucleus remains heavily grammar-skewed on prose-heavy corpora:
  - `grammatical_dominant` is the majority interaction mode
  - semantic remains zero because no embedding artifacts were loaded
- This is good enough progress to continue, but it also exposed the next meaningful question:
  - improve Splitter list/index representation more, or
  - start refining bootstrap prose interaction behavior in the Emitter

## 2026-03-27 — Probe reporting loop established

Journal entry: `journal_probe_reporting_001`

- Added builder-side probe reporting tool `.dev-tools/final-tools/tools/graph_probe_report.py`.
- Verified the tool against the existing Python-reference probe artifacts and confirmed it reproduces the manual counts exactly.
- Saved the first machine-readable report at `_docs/_analysis/reference_probe_001/graph_probe_report_001.json`.
- This gives the project a repeatable step-2 loop:
  - make one targeted change
  - rerun the full probe
  - save a JSON report
  - compare against Probe 001 instead of relying on ad hoc SQL and memory
- The project now has measurable ground for oscillating between Splitter and Emitter work without losing the thread.

## 2026-03-27 — Bootstrap de-bias pass 001 + Probe 002

Journal entry: `journal_bootstrap_probe_002`

- Inspected `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py` to trace the prose-heavy `grammatical_dominant` bias from code rather than from probe symptoms alone.
- Confirmed the main seam:
  - exact prose node-kind matches like `md_paragraph` were receiving the same full grammatical credit as exact code-node matches
  - semantic remained zero because no embedding artifacts were loaded
  - with fixed Phase 1 surface fractions, that combination pushed too many prose pairs into grammar-led routing
- Applied one targeted bootstrap change:
  - prose grammatical matching was de-amplified relative to code grammatical matching
- Ran Probe 002 against the same Python reference corpus and recorded artifacts under `_docs/_analysis/reference_probe_002/`.
- Results:
  - `grammatical_dominant` training labels dropped sharply
  - but relation volume also dropped sharply (`22406 -> 2897`)
  - cross-document nucleus pull edges also dropped sharply (`1293 -> 147`)
- Current interpretation:
  - the first de-bias pass proved the distortion is a bootstrap-math problem
  - the first pass is too aggressive to keep as the final tune
  - the next iteration should be moderate, not extreme, and likely needs either softer prose penalties or threshold retuning

## 2026-03-27 — Bootstrap scaffold dials shipped + Probe 003

Journal entry: `journal_bootstrap_scaffold_dials_001`

- Refactored the Emitter bootstrap scorer so it now consumes an explicit `BootstrapConfig` rather than hardcoded module constants.
- Exposed builder-facing tuning through:
  - `--bootstrap-profile`
  - `--edge-threshold`
  - `--dominance-threshold`
- Emit now writes `bootstrap_profile_effective.json` beside the output database, making probe bundles reproducible by default.
- Updated the builder-side `graph_probe_report` tool to include the adjacent effective bootstrap profile when present.
- Added emitter-local tests covering:
  - config validation
  - round-trip serialization
  - basic scaffold behavior expectations
  - semantic-absence threshold scaling behavior
- Added tracked starter profile:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`
- Verified default regression:
  - default-config emit reproduces Probe 002 top-line baseline (`relations = 2897`, `cross-document pull = 147`, `above-threshold = 1636`)
- Ran Probe 003 with the starter profile:
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold pairs = 12249`
  - `grammatical_dominant` training labels reduced to `801`
- Current interpretation:
  - the scaffold dial surface is now good enough for deliberate tuning work
  - the starter profile successfully recovers live-graph volume over Probe 002
  - the next scoring target is cross-document pull recovery, not just raw relation count

## 2026-03-28 — Builder-side probe monitor shipped

Journal entry: pending mirror

- Added `.dev-tools/final-tools/tools/probe_monitor.py` as a builder-only probe runner for Splitter -> Emitter passes.
- The tool writes a replayable observability bundle under `_docs/_analysis/<probe>/`:
  - `probe_events.jsonl`
  - `probe_run.log`
  - `graph_probe_report_<probe>.json`
  - `bootstrap_profile_effective.json` from the runtime emit path
- Added an optional tiny Tk builder monitor window for live viewing while keeping the shipped app cleanly decoupled from `.dev-tools`.
- Added stage events and safer failure cleanup so probe runs leave a useful record even when something breaks midstream.
- Added example job:
  - `.dev-tools/final-tools/jobs/examples/probe_monitor.json`
- Updated the final-tools manifest/docs/smoke test so the probe monitor is part of the validated toolbox rather than an ad hoc local script.
- Verified:
  - `python -m py_compile` passed on the touched builder-tool files
  - `python .dev-tools/final-tools/smoke_test.py` passed, including `probe_monitor`
- Resulting workflow improvement:
  - future Probe 004+ runs can be watched live while still producing durable machine-readable artifacts for comparison

## 2026-03-28 — Probe 004 observable replay baseline

Journal entry: pending mirror

- Ran Probe 004 against the same Python reference corpus and the same tracked starter profile used for Probe 003, but through the new builder-side probe monitor.
- Probe 004 wrote the normal graph artifacts plus live-monitor artifacts:
  - `_docs/_analysis/reference_probe_004/probe_events.jsonl`
  - `_docs/_analysis/reference_probe_004/probe_run.log`
- Probe 004 matched Probe 003 exactly on the tracked top-line metrics:
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold training pairs = 12249`
  - `grammatical_dominant` training labels = `801`
- Interpretation:
  - the monitor layer is observational only; it did not perturb the run
  - Probe 003 is now confirmed as a stable observable baseline rather than a one-off good pass
- Follow-up builder UX improvement:
  - extended `probe_monitor.py` with `hold_open` so the tiny monitor window can stay open after completion until manually closed

## 2026-03-28 — Probe 005/006 tuning negatives + monitor hold-open fix

Journal entry: pending mirror

- Probe 005 tested a profile-only shift from `structural` weight into `statistical` weight using:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v1.json`
- Result:
  - `relations = 9072` (`-4438` vs Probe 004)
  - `cross-document nucleus pull edges = 163` (`-6` vs Probe 004)
  - `above-threshold training pairs = 7811` (`-4438` vs Probe 004)
- Interpretation:
  - cross-document lift is not hiding behind a general statistical boost
  - this branch hurt graph activity and should not replace the Probe 003/004 baseline

- Probe 006 tested a heading-targeted grammatical boost using:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v2.json`
- Result:
  - `relations = 13510` (matches Probe 004)
  - `cross-document nucleus pull edges = 169` (matches Probe 004)
  - `grammatical_dominant` training labels rose from `801` to `879`
- Interpretation:
  - simple heading-weight amplification did not improve cross-document pull
  - it only shifted some interaction labeling toward grammar without lifting the target metric

- Builder monitor lifecycle fix:
  - the first `hold_open` implementation exposed a Tk teardown/thread issue
  - fixed by moving the tiny viewer into a standalone helper process:
    - `.dev-tools/final-tools/tools/probe_monitor_viewer.py`
  - validated with a UI auto-close smoke and the full final-tools smoke suite

- Current read after Probes 005 and 006:
  - Probe 003/004 remains the stable baseline
  - the next cross-document lift attempt likely needs either:
    - a more granular bootstrap-code dial, or
    - richer representation work from the Splitter

## 2026-03-26 — Phase 1 baseline cleanup + App Journal verification

Journal entry: `journal_final_cleanup_20260326`

- Promoted the extracted app line from design-stage staging area to a runnable Phase 1 baseline.
- Removed runtime dependence on the shared design contract by giving Splitter and Emitter local runtime contract ownership.
- Fixed Splitter CLI hygiene and UTF-8 output so NDJSON handoff is stable on Windows.
- Fixed Emitter runtime seams, including import fallbacks and embed-provider compatibility.
- Turned Splitter’s richer engines into declared dependencies and preserved provenance when the Negotiator fragments AST/CST-derived hunks.
- Re-ran smoke flows:
  - Splitter → Emitter markdown smoke passed
  - TreeSitter-backed code-path smoke passed with non-zero grammatical richness
  - App Journal manifest and package smoke passed after MCP stdio framing was corrected
- Restored a root launcher for the journal so the repo again has an obvious human entrypoint.

## Historical anchor

- `journal_tranche7_devlog` remains the tranche-specific log for the Emitter CLI, GUI, and original Phase 1 integration milestone.
