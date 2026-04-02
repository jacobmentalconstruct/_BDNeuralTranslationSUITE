# Branch Status

## Branch

- Name: `codex/baseline-leg-sidecar`
- Status: concluded diagnostic branch
- Merge status: do not merge yet
- Abandon status: keep as a reference seam; do not continue expanding it as a second product line

## Purpose

Stand the system on more ordinary retrieval legs and compare them to the current bag without altering the live app path.

## Non-goals

- no live bag/query entrypoint edits
- no schema or ingest changes
- no splitter changes
- no bootstrap profile changes
- no promotion of branch findings into mainline truth without explicit review

## Allowed Areas

- `.dev-tools/final-tools/tools/`
- `_docs/_branch_baseline_leg/`
- branch-local analysis artifacts
- sidecar-only tests

## Latest Trustworthy Findings

- The sidecar branch includes dedicated shelf and compare tools for:
  - `fts`
  - `ann_sentence`
  - `ann_deterministic`
  - current `bag`
- Baseline legs can now be rendered with:
  - top items
  - origin/path metadata
  - snippets
  - optional verbatim pullback
- Branch findings remain branch-local until explicitly promoted
- First branch-local compare artifact:
  - `_docs/_branch_baseline_leg/_analysis/compare_2026-04-02/baseline_leg_compare_2026-04-02.md`
  - `_docs/_branch_baseline_leg/_analysis/compare_2026-04-02/baseline_leg_compare_2026-04-02.json`
- First branch-local pullback shelf artifact:
  - `_docs/_branch_baseline_leg/_analysis/shelf_2026-04-02/fts_encoding_declarations_pullback.md`
  - `_docs/_branch_baseline_leg/_analysis/shelf_2026-04-02/fts_encoding_declarations_pullback.json`
- First measured compare read on the 16-query shelf:
  - `fts`: human-facing tops `10/16`, same-top vs bag `5/16`, same-origin vs bag `6/16`
  - `ann_sentence`: human-facing tops `13/16`, same-top vs bag `6/16`, same-origin vs bag `7/16`
  - `ann_deterministic`: human-facing tops `14/16`, same-top vs bag `4/16`, same-origin vs bag `5/16`
  - `bag`: human-facing tops `15/16`
- Current branch-local interpretation:
  - sentence-transformers ANN is the closest “normal vector” leg on this shelf
  - deterministic ANN remains more divergent from the bag than sentence-transformers ANN
  - the bag still looks like a shaped evidence shelf rather than a plain nearest-neighbor surface
- A second branch-local footing now exists on a real-English mixed prose corpus:
  - `_corpus_examples/tech_talks`
  - branch-local ingest folder:
    - `_docs/_branch_baseline_leg/_analysis/tech_talks_ingest_2026-04-02/`
- The `tech_talks` footing is a better natural-language baseline than `webstersdictinoary.txt` for this branch:
  - much smaller
  - much more structurally meaningful
  - full of ordinary conversational + technical phrasing
- Real-English corpus ingest state:
  - `tech_talks_hunks.ndjson`: `5184` hunks
  - `cold_anatomy_tech_talks_st.db`: sentence-transformers lane
  - `deterministic_artifacts/`: tokenizer + embeddings + inhibit edges trained on `tech_talks`
  - `cold_anatomy_tech_talks_det.db`: deterministic lane
- Shared inspection seam is now real:
  - `baseline_leg_viewer.py` can use a shared session JSON + JSONL event log
  - human and agent can inspect the same panel state instead of narrating separate hidden queries
- Shared-visible control seam is now implemented in the sidecar:
  - viewer now has a session-level control mode:
    - `shared-visible`
    - `background`
  - agent-side panel actions can now be written into the shared session as `pending_action`
  - the viewer is able to consume those actions through its own visible query path when running the updated code
  - helper files:
    - `.dev-tools/final-tools/tools/baseline_leg_session.py`
    - `.dev-tools/final-tools/tools/baseline_leg_panel_action.py`
  - important operational note:
    - an already-open viewer must be restarted to pick up this seam
- First real-English comparative read for query `black box`:
  - `fts` is the cleanest leg
    - exact title hit from `The End of the Black Box_ How Pure Math is Recla.md`
    - human-readable immediately
  - `ann_sentence` finds the broad semantic neighbourhood, but the shelf is fragmentary
  - `ann_deterministic` is weaker still on this query and drifts toward symbolic/code-adjacent fragments from `master_spec_text.txt`
  - `bag` preserves the lexical anchor win and expands it into a broader evidence shelf, but still admits some weaker bleed
- Current branch-local interpretation from the real-English pass:
  - different retrieval legs are genuinely good at different things
  - lexical search should not be discarded just because semantic search exists
  - sentence-transformers ANN currently behaves more like a conventional semantic baseline on prose
  - deterministic ANN is provisioned and testable now, but on this footing it still does not behave like a strong standalone prose retriever
  - the collaborative shared-panel workflow is itself a useful experimental surface and should be treated as a design finding, not just convenience plumbing

## Poison / Noise Criteria

Treat a finding as poison or noise if:
- it depends on edits to the live bag path
- it cannot reproduce from the same DB and query shelf
- it hides retrieval differences behind fake bag-only fields
- it produces a nicer report but weaker evidence grounding
