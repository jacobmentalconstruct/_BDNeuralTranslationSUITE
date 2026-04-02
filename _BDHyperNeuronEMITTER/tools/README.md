# Builder Tools

This folder is the tracked permanent home for builder-side and sidecar utilities that we want to keep with the app.

Current kept seams:

- `baseline_leg_viewer.py`
  - minimal shared-view retrieval sidecar
- `baseline_leg_session.py`
  - shared registry/session helpers
- `baseline_leg_sidecar_lib.py`
  - FTS / ANN / bag shelf normalization for sidecar inspection
- `baseline_leg_panel_action.py`
  - experimental panel-action helper
- `english_triplet_training_loop.py`
  - controlled English high-contrast bundle generator

Examples and word-list assets live under:

- `examples/`

Builder outputs should go to `_docs/_analysis/`, not back into this source folder.
