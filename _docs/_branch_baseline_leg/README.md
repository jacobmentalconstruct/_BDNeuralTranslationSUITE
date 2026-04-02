# Baseline-Leg Sidecar Branch

This folder is the branch-local recovery surface for the `codex/baseline-leg-sidecar` experiment.

Purpose:
- measure ordinary retrieval legs against the current bag
- keep the live bag/query path untouched
- produce comparable, verbatim-recoverable evidence shelves

This branch is diagnostic only and is now concluded as a reference seam.

Current branch rules:
- do not modify live bag/query entrypoints
- do not change default bootstrap profiles
- do not overwrite the main recovery docs as branch truth
- do store branch findings here so this branch can be paused or abandoned safely

Primary sidecar tools:
- `.dev-tools/final-tools/tools/baseline_leg_shelf.py`
- `.dev-tools/final-tools/tools/baseline_leg_compare.py`
- `.dev-tools/final-tools/tools/baseline_leg_viewer.py`

Primary branch-local outputs:
- `_docs/_branch_baseline_leg/_analysis/`
- branch-local notes in this folder
- branch conclusion:
  - `_docs/_branch_baseline_leg/CONCLUSION.md`

Current high-signal branch additions:
- a real-English mixed prose footing under `_corpus_examples/tech_talks`
- branch-local sentence-transformers and deterministic DBs for that footing
- a shared-session Tk viewer so the human and the agent can inspect the same retrieval panel state
