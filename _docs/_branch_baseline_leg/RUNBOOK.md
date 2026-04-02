# Baseline-Leg Runbook

This branch exists to compare baseline retrieval legs without disturbing the live app path.

## Single-leg shelf

Example:

```powershell
python .dev-tools/final-tools/tools/baseline_leg_shelf.py `
  --mode ann `
  --ann-provider deterministic `
  --db C:\path\to\cold_anatomy.db `
  --query "lambda expressions" `
  --output-dir C:\path\to\_docs\_branch_baseline_leg\_analysis\shelf_demo
```

Modes:
- `fts`
- `ann`
- `bag`

Outputs:
- one JSON payload
- one Markdown shelf

## Tiny viewer

Example:

```powershell
python .dev-tools/final-tools/tools/baseline_leg_viewer.py `
  --db C:\path\to\cold_anatomy.db `
  --mode ann `
  --ann-provider sentence-transformers `
  --query "lambda expressions" `
  --save-dir C:\path\to\_docs\_branch_baseline_leg\_analysis\viewer_runs
```

Shared-session example:

```powershell
python .dev-tools/final-tools/tools/baseline_leg_viewer.py `
  --db C:\path\to\cold_anatomy.db `
  --mode ann `
  --ann-provider sentence-transformers `
  --query "bag of evidence" `
  --session-file C:\path\to\_docs\_branch_baseline_leg\_analysis\viewer_runs\shared_session.json `
  --event-log C:\path\to\_docs\_branch_baseline_leg\_analysis\viewer_runs\shared_session.jsonl `
  --save-dir C:\path\to\_docs\_branch_baseline_leg\_analysis\viewer_runs
```

Viewer layout:
- query box
- response / summary box
- shelf items as clickable buttons
- item content pane

Shared viewer behavior:
- the viewer can read and write a shared session JSON
- the viewer can append a JSONL event log
- this supports agent-driven and human-driven inspection in the same visible panel
- the updated viewer also supports a session-level control mode:
  - `shared-visible`
  - `background`
- in `shared-visible` mode, agent-written `pending_action` payloads are executed through the visible panel path

Agent action example:

```powershell
python .dev-tools/final-tools/tools/baseline_leg_panel_action.py `
  --session-file C:\path\to\shared_session.json `
  --db C:\path\to\cold_anatomy.db `
  --query "black box" `
  --mode bag `
  --ann-provider sentence-transformers `
  --source agent `
  --control-mode shared-visible
```

Important note:
- if the viewer was already open before this seam was added, restart it once so it loads the updated shared-visible action handler

## Side-by-side compare

Example:

```powershell
python .dev-tools/final-tools/tools/baseline_leg_compare.py `
  --bag-db C:\path\to\reference_probe_073_semgrav_det_steep\cold_anatomy_reference_probe_073_semgrav_det_steep.db `
  --fts-db C:\path\to\reference_probe_073_semgrav_det_steep\cold_anatomy_reference_probe_073_semgrav_det_steep.db `
  --det-ann-db C:\path\to\reference_probe_073_semgrav_det_steep\cold_anatomy_reference_probe_073_semgrav_det_steep.db `
  --st-ann-db C:\path\to\reference_probe_069_semgrav_st_control\cold_anatomy_reference_probe_069_semgrav_st_control.db `
  --output-dir C:\path\to\_docs\_branch_baseline_leg\_analysis\compare_demo
```

Outputs:
- one compare JSON
- one compare Markdown

## How To Read The Result

Look for:
- whether baseline legs land human-facing anchors
- whether they match the bag top or only the bag origin
- whether deterministic ANN diverges sharply from sentence-transformers ANN
- whether that divergence looks useful, warped, or ambiguous
- whether a shared-panel workflow makes the retrieval behavior easier to understand and audit in real time

## Real-English Corpus Note

The current strongest branch-local prose footing is:

- `_corpus_examples/tech_talks`

Why this footing matters:
- it is real mixed English prose rather than artificially narrow reference text
- it contains both casual conversational phrasing and project-specific technical language
- it is compact enough to provision multiple retrieval lanes quickly

Deterministic lane caveat:
- the current deterministic trainer learns from `.txt` corpus files
- emit can still ingest `.md` and `.txt` into the DB
- so deterministic results on `tech_talks` are useful, but they are not yet trained over the exact same file extension mix as the full emitted corpus

## Branch-worthy vs Poison

Branch-worthy:
- reproducible shelf differences
- clean verbatim pullback
- readable compare output
- obvious retrieval-behavior insight

Poison/noise:
- results that depend on changing the live bag path
- comparison payloads that invent fake bag fields for FTS or ANN
- unstable conclusions from one-off runs only
