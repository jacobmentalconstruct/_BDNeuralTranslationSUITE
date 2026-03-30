# Graph Probes

_Last updated: 2026-03-28. This file records representative Splitter → Emitter probe runs and what they reveal about graph behavior._

---

## Probe 001 — Python Reference Full-Pipe NL Check

**Date:** 2026-03-27

### Input

Source:
- `_corpus_examples/python-3.11.15-docs-text/reference`

Splitter state at time of run:
- fallback provenance fixed
- structured reST-style `.txt` documents routed into PEG
- `grammar.txt` literal-block misclassification fixed

Artifacts:
- `_docs/_analysis/reference_probe_001/cold_anatomy_reference_probe_001.db`
- `_docs/_analysis/reference_probe_001/training_pairs_reference_probe_001.json`
- `_docs/_analysis/reference_probe_001/graph_probe_report_001.json`

Repeatable reporting workflow:
- builder-side tool: `.dev-tools/final-tools/tools/graph_probe_report.py`
- current loop: `probe -> save JSON report -> compare against previous probe`
- this means future probe passes can be compared mechanically instead of re-deriving metrics ad hoc

---

## Top-Level Run Summary

| Metric | Value |
|---|---|
| hunks ingested | `1102` |
| skipped | `0` |
| content nodes | `1083` |
| occurrence nodes | `1102` |
| relations | `22406` |
| training pairs | `53825` |
| embedded hunks | `0` |

Surface richness reported by the Emitter:

| Surface | Mean richness |
|---|---|
| verbatim | `1.00` |
| structural | `0.75` |
| statistical | `1.00` |
| grammatical | `0.00` |
| semantic | `0.00` |

Notes:
- semantic is expectedly zero because no trained embedding artifacts were loaded
- grammatical showing as `0.00` in the Emitter report is a reporting/model-lens limitation, not proof that the NL improvements vanished

---

## Relation Mix

| Relation metric | Value |
|---|---|
| total `pull` edges | `21417` |
| total `precedes` edges | `989` |
| nucleus pull edges (non structural-only routing) | `21145` |
| cross-document nucleus pull edges | `1293` |

Interaction mode distribution across all relations:

| Mode | Count |
|---|---|
| `grammatical_dominant` | `18836` |
| `structural_bridge` | `3430` |
| `multi_surface` | `140` |

Training-pair distribution:

| Metric | Value |
|---|---|
| above threshold | `21145` |
| below threshold | `32680` |
| mean connection strength | `0.2511` |
| median connection strength | `0.2706` |

Top interaction types in training pairs:
- `grammatical_dominant = 38387`
- `structural_bridge = 14039`
- `statistical_echo = 1172`
- `multi_surface = 227`

---

## What This Probe Proves

1. The improved NL/document path is affecting the graph.
   - The system produced `1293` cross-document nucleus pull edges from prose-heavy reference docs.

2. The richer Splitter output is surviving the handoff.
   - Headings and section structure from the Python reference set reached the Emitter and materially changed relation volume and path shape.

3. The current bootstrap nucleus is still heavily biased toward coarse grammatical similarity.
   - Most non-structural pull edges are still labeled `grammatical_dominant`.
   - This is likely because prose hunks share a small set of node kinds (`md_heading`, `md_paragraph`, `md_code_block`) and semantic embeddings are currently disabled.

4. Structural signal is present, but not the whole story.
   - There are meaningful `structural_bridge` interactions and some `multi_surface` edges.
   - This is enough to justify continuing rather than bouncing immediately back to Splitter-only work.

---

## Example Cross-Document Edges

Representative cross-document nucleus pull edges included:

- `executionmodel.txt :: 4. Execution model`
  ↔ `expressions.txt :: 6. Expressions`
- `import.txt :: 5.7. Package Relative Imports`
  ↔ `index.txt :: The Python Language Reference`
- `simple_stmts.txt :: 7.12. The "global" statement`
  ↔ `toplevel_components.txt :: 9.1. Complete Python programs`

These are not random in the “obviously broken” sense, but they are still driven more by broad section-type affinity than by deep semantic grounding.

---

## What This Probe Does Not Yet Prove

- It does not prove semantic retrieval quality because semantic embeddings were disabled.
- It does not prove that the current routing profiles are ideal for prose, only that they are now reacting to prose structure.
- It does not prove that index/list-heavy documents are represented as richly as they should be.

---

## Next Likely Moves

1. Decide whether to bounce back to Splitter for one more NL pass:
   - clean up the remaining `md_list` / index representation issues

2. Or continue in the Emitter:
   - inspect whether bootstrap routing should be less grammar-heavy for prose-heavy corpora
   - improve probe outputs so training-pair exports include easy human-readable source/target metadata

3. Keep both options open and oscillate deliberately.
   - the project now has enough signal to justify either direction

4. For every future probe:
   - save the graph/training artifacts under `_docs/_analysis/<probe_name>/`
   - run `graph_probe_report.py`
   - record the comparison delta back into this file and `_docs/DEV_LOG.md`

---

## Probe 002 — Bootstrap De-Bias Pass 001

**Date:** 2026-03-27

### Input

Source:
- `_corpus_examples/python-3.11.15-docs-text/reference`

Targeted bootstrap change:
- in `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py`, prose grammatical matching was de-amplified so exact prose node-kind matches no longer receive the same full grammatical credit as exact code-node matches
- exact `md_heading` pairs remain stronger than generic prose, but `md_paragraph` and other broad prose kinds now contribute much less grammatical affinity

Artifacts:
- `_docs/_analysis/reference_probe_002/cold_anatomy_reference_probe_002.db`
- `_docs/_analysis/reference_probe_002/training_pairs_reference_probe_002.json`
- `_docs/_analysis/reference_probe_002/graph_probe_report_002.json`
- `_docs/_analysis/reference_probe_002/probe_001_vs_002_delta.json`

---

## Top-Level Run Summary

| Metric | Probe 001 | Probe 002 | Delta |
|---|---:|---:|---:|
| hunks ingested | `1102` | `1102` | `0` |
| content nodes | `1083` | `1083` | `0` |
| occurrence nodes | `1102` | `1102` | `0` |
| relations | `22406` | `2897` | `-19509` |
| training pairs | `53825` | `53825` | `0` |
| cross-document nucleus pull edges | `1293` | `147` | `-1146` |

Training-pair threshold summary:

| Metric | Probe 001 | Probe 002 | Delta |
|---|---:|---:|---:|
| above threshold | `21145` | `1636` | `-19509` |
| below threshold | `32680` | `52189` | `+19509` |
| mean connection strength | `0.2511` | `0.1559` | `-0.0952` |
| median connection strength | `0.2706` | `0.1512` | `-0.1194` |

---

## Relation Mix Delta

Probe 001 interaction mode distribution:
- `grammatical_dominant = 18836`
- `structural_bridge = 3430`
- `multi_surface = 140`

Probe 002 interaction mode distribution:
- `structural_bridge = 2014`
- `grammatical_dominant = 851`
- `statistical_echo = 20`
- `multi_surface = 12`

Training-pair interaction type distribution shifted from:
- Probe 001:
  - `grammatical_dominant = 38387`
  - `structural_bridge = 14039`
  - `statistical_echo = 1172`
  - `multi_surface = 227`
- Probe 002:
  - `structural_bridge = 39406`
  - `grammatical_dominant = 6936`
  - `multi_surface = 3820`
  - `statistical_echo = 3663`

---

## What Probe 002 Proves

1. The grammatical skew is largely a bootstrap math problem.
   - A single change to prose grammatical scoring collapsed `grammatical_dominant` training labels from `38387` to `6936`.

2. The first bootstrap de-bias pass is too strong to keep as-is.
   - Relation volume fell from `22406` to `2897`.
   - Cross-document nucleus pull edges fell from `1293` to `147`.

3. The current edge threshold now interacts badly with the reduced grammar contribution.
   - Many pairs now read as `structural_bridge`, but their strengths land below the existing `0.3` threshold and therefore do not get written.

4. The result is useful, even though it is not the final tune.
   - It proves the live graph distortion was caused by bootstrap weighting rather than by an architectural flaw in the neuron/graph idea itself.

---

## Current Read

Probe 001 was too grammar-heavy.

Probe 002 is better as a diagnosis than as a final scoring profile:
- it reduced the coarse prose-grammar collapse
- but it overcorrected and starved the graph of live edges

The next bootstrap iteration should be more moderate, not more extreme. The likely path is:
- keep prose grammatical matching lower than code grammatical matching
- but recover some relation volume by moderating the prose penalty and/or retuning the edge threshold after the de-bias

---

## Default Regression — Configurable Scaffold Preserves Probe 002 Baseline

**Date:** 2026-03-27

Purpose:
- verify that the new `BootstrapConfig` + CLI/profile path preserves the current checked-in scaffold behavior by default

Artifacts:
- `_docs/_analysis/reference_probe_default_regression/cold_anatomy_reference_probe_default_regression.db`
- `_docs/_analysis/reference_probe_default_regression/training_pairs_reference_probe_default_regression.json`
- `_docs/_analysis/reference_probe_default_regression/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_default_regression/graph_probe_report_default_regression.json`
- `_docs/_analysis/reference_probe_default_regression/probe_002_vs_default_regression.json`

Top-line regression result:
- `relations = 2897` (matches Probe 002)
- `cross-document nucleus pull edges = 147` (matches Probe 002)
- `above-threshold training pairs = 1636` (matches Probe 002)

This is the acceptance checkpoint that the scaffold-dial implementation did not silently change the existing bootstrap baseline.

---

## Probe 003 — Starter Profile Recovery Pass

**Date:** 2026-03-27

Purpose:
- validate that the new scaffold dial surface is useful in practice
- test a tracked prose-heavy tuning profile against Probes 001 and 002

Profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Artifacts:
- `_docs/_analysis/reference_probe_003/cold_anatomy_reference_probe_003.db`
- `_docs/_analysis/reference_probe_003/training_pairs_reference_probe_003.json`
- `_docs/_analysis/reference_probe_003/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_003/graph_probe_report_003.json`
- `_docs/_analysis/reference_probe_003/probe_001_vs_002_vs_003_delta.json`

---

## Top-Level Run Summary

| Metric | Probe 001 | Probe 002 | Probe 003 |
|---|---:|---:|---:|
| relations | `22406` | `2897` | `13510` |
| cross-document nucleus pull edges | `1293` | `147` | `169` |
| above-threshold training pairs | `21145` | `1636` | `12249` |
| mean connection strength | `0.2511` | `0.1559` | `0.1635` |

Probe 003 interaction mode distribution:
- `structural_bridge = 12531`
- `grammatical_dominant = 727`
- `multi_surface = 235`
- `statistical_echo = 17`

Probe 003 training-pair interaction distribution:
- `structural_bridge = 44997`
- `multi_surface = 5236`
- `statistical_echo = 2791`
- `grammatical_dominant = 801`

---

## What Probe 003 Proves

1. The new scaffold dials are useful, not just formal.
   - A tracked starter profile moved the system from Probe 002's edge-starved state to a much more active live graph.

2. The starter profile meets the current acceptance bar.
   - It restores relation volume substantially over Probe 002.
   - It remains far less grammar-collapsed than Probe 001.

3. The next bottleneck is now more specific.
   - Cross-document pull recovery improved only slightly (`147 -> 169`).
   - That means the next tuning target is not raw edge count alone; it is cross-document evidence lift.

---

## Current Read

Probe 001:
- too grammar-heavy

Probe 002:
- diagnostic success, but overcorrected

Probe 003:
- good starter recovery profile
- strong enough to become the current tuning footing unless the next pass immediately supersedes it

The next probe should optimize for:
- better cross-document pull recovery
- preserved low grammar collapse
- no return to Probe 001-scale coarse coupling

---

## Probe 004 — Observable Replay Baseline

**Date:** 2026-03-28

Purpose:
- validate the new builder-side probe monitor on a real full-pipe run
- confirm the observability layer does not perturb the current Probe 003 footing

Profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Artifacts:
- `_docs/_analysis/reference_probe_004/cold_anatomy_reference_probe_004.db`
- `_docs/_analysis/reference_probe_004/training_pairs_reference_probe_004.json`
- `_docs/_analysis/reference_probe_004/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_004/graph_probe_report_reference_probe_004.json`
- `_docs/_analysis/reference_probe_004/probe_events.jsonl`
- `_docs/_analysis/reference_probe_004/probe_run.log`
- `_docs/_analysis/reference_probe_004/probe_003_vs_004_delta.json`

Top-line result:
- Probe 004 matched Probe 003 exactly on the tracked top-line metrics
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold training pairs = 12249`
  - `grammatical_dominant` training labels = `801`

What this proves:
1. The builder-side monitor is now part of the real measurement workflow, not a side experiment.
2. The observability layer did not change graph behavior.
3. Probe 003 can now be treated as an observable replay baseline while we tune toward better cross-document pull.

---

## Probe 005 — Structural to Statistical Shift (Negative)

**Date:** 2026-03-28

Profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v1.json`

Targeted change:
- moved a small amount of surface weight from `structural` to `statistical`

Artifacts:
- `_docs/_analysis/reference_probe_005/cold_anatomy_reference_probe_005.db`
- `_docs/_analysis/reference_probe_005/training_pairs_reference_probe_005.json`
- `_docs/_analysis/reference_probe_005/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_005/graph_probe_report_reference_probe_005.json`
- `_docs/_analysis/reference_probe_005/probe_004_vs_005_delta.json`
- `_docs/_analysis/reference_probe_005/probe_events.jsonl`
- `_docs/_analysis/reference_probe_005/probe_run.log`

Delta vs Probe 004:
- `relations = -4438`
- `cross-document nucleus pull = -6`
- `above-threshold training pairs = -4438`
- `statistical_echo` training labels = `+3614`

Read:
- this change pushed more pairs into statistical-style behavior, but it did not improve the target metric
- it reduced overall live-graph volume and slightly worsened cross-document pull
- keep Probe 003/004 as the baseline, not this branch

---

## Probe 006 — Heading Boost (No Lift)

**Date:** 2026-03-28

Profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v2.json`

Targeted change:
- increased `exact_heading_kind` while leaving the rest of the Probe 003/004 profile intact

Artifacts:
- `_docs/_analysis/reference_probe_006/cold_anatomy_reference_probe_006.db`
- `_docs/_analysis/reference_probe_006/training_pairs_reference_probe_006.json`
- `_docs/_analysis/reference_probe_006/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_006/graph_probe_report_reference_probe_006.json`
- `_docs/_analysis/reference_probe_006/probe_004_vs_006_delta.json`
- `_docs/_analysis/reference_probe_006/probe_events.jsonl`
- `_docs/_analysis/reference_probe_006/probe_run.log`

Delta vs Probe 004:
- `relations = 0`
- `cross-document nucleus pull = 0`
- `above-threshold training pairs = 0`
- `grammatical_dominant` training labels = `+78`

Read:
- exact heading amplification alone did not move the cross-document target
- it only shifted some labeling toward grammar while leaving the graph shape unchanged
- simple profile dials may now be close to exhausted for this specific target
