# WE_ARE_HERE_NOW

_Overwrite this file at each small milestone. It is the fastest crash-recovery / cold-start note in the project._

## Last updated

2026-03-28

## Current footing

- The repo root is now the active portable project root.
- Phase 1 baseline is real and runnable.
- Splitter and Emitter are both live enough to continue development.
- Bootstrap Nucleus is the active scorer.
- The bag is still future architecture, not the current build target.

## What we just finished

- Re-centered the project after the old `final/` move-up.
- Verified the App Journal install and launcher path.
- Cleaned major runtime seams in Splitter and Emitter.
- Fixed Emitter UI lifecycle/thread handling so worker-thread UI updates are queued safely onto the main Tk thread.
- Wrote root architecture and recovery docs so the project can survive interruption cleanly.
- Started Splitter corpus hardening with the first recorded corpus baseline.
- Fixed blank fallback provenance (`extraction_engine`) and taught PEG to claim structured reST-style `.txt` reference docs.
- Fixed an NL parsing seam where indented literal blocks in `grammar.txt` were being mistaken for headings.
- Ran the first full Splitter → Emitter probe on the Python reference corpus and confirmed the graph is reacting to the stronger NL path.
- Turned the graph-probe pass into a repeatable measurement loop with a saved JSON report artifact and builder-side reporter tool.
- Inspected the bootstrap nucleus and confirmed the prose-heavy `grammatical_dominant` skew comes from coarse prose node-kind matching plus fixed Phase 1 weights.
- Ran Probe 002 after a first de-bias pass and confirmed the skew is reducible, but the first pass overcorrected and starved relation volume.
- Shipped builder-facing bootstrap scaffold dials through the Emitter CLI plus JSON profile loading.
- Added emitter-local tests for scaffold config validation and behavior.
- Verified default-config regression against Probe 002 and saved effective bootstrap profiles beside probe artifacts.
- Ran Probe 003 with the tracked starter profile and recovered graph volume substantially without returning to grammar collapse.
- Added a builder-only probe monitor under `.dev-tools/final-tools/tools/probe_monitor.py`.
- Verified the monitor writes live `probe_events.jsonl` and `probe_run.log` artifacts under `_docs/_analysis/<probe>/`.
- Added an optional tiny builder monitor window while preserving machine-readable outputs and keeping the shipped app free of `.dev-tools` coupling.
- Updated the final-tools smoke test and example jobs so the probe monitor is part of the validated builder toolbox.
- Ran Probe 004 through the live builder monitor and confirmed it reproduces the Probe 003 footing exactly.
- Fixed the monitor `hold_open` path by moving the tiny Tk viewer into its own helper process so it can stay open for review without crashing the probe runner.
- Ran Probe 005 with a profile-only structural -> statistical shift and confirmed it hurts relation volume while also lowering cross-document pull.
- Ran Probe 006 with a heading-specific grammatical boost and confirmed it does not improve cross-document pull over the Probe 003/004 footing.

## What to do next

Next tranche: **Splitter corpus hardening**

1. Choose the next targeted change:
   - add one more granular bootstrap-code dial aimed at cross-document prose/heading lift, or
   - bounce back to Splitter if the remaining limitation looks representation-driven rather than scorer-driven
2. Make one targeted change only.
3. Rerun the full probe loop with `.dev-tools/final-tools/tools/probe_monitor.py` so events, logs, and report artifacts are captured together.
4. Compare the next probe against Probes 003, 004, 005, and 006 in `_docs/GRAPH_PROBES.md`.

## Do not drift into yet

- FFN Nucleus
- bag implementation
- big retrieval redesign
- broad polishing passes

## Read in this order if resuming cold

1. `_docs/WE_ARE_HERE_NOW.md`
2. `_docs/ARCHITECTURE.md`
3. `_docs/TODO.md`
4. `_docs/DEV_LOG.md`
5. `_docs/SPLITTER_CORPUS_BASELINES.md`
6. `_docs/GRAPH_PROBES.md`
7. `_docs/NL_NarrativeDESC.md`
8. `_docs/PARKING_LOT_QUESTIONS.md`
9. `.dev-tools/final-tools/jobs/examples/probe_monitor.json`
9. App Journal entries:
   - `journal_resume_checkpoint_20260327`
   - `journal_splitter_corpus_baseline_001`
   - `journal_backlog_001`
   - `journal_3e9561e03e68`

## Quick sanity checks

```powershell
python _BDHyperNodeSPLITTER/src/app.py --help
python _BDHyperNeuronEMITTER/src/app.py --help
python .dev-tools/_app-journal/tools/journal_manifest.py run --input-json "{\"project_root\":\"C:/Users/jacob/Documents/_UsefulAgenticBuilderSANDBOX/Claude-Code/_BDNeuralTranslationSUITE\"}"
```

## Known truth about the docs

- `_docs/ARCHITECTURE.md` is the root doctrine.
- `_docs/_BagOfEVIDENCE.md` is legacy context, not active architecture truth.
