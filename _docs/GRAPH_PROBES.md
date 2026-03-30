# Graph Probes

_Last updated: 2026-03-30. This file records representative Splitter → Emitter probe runs and what they reveal about graph behavior._

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

## Probe 008 — Default Regression After Splitter Signal Controls

**Date:** 2026-03-28

Purpose:
- verify that the new Splitter signal-control layer preserves the current stable Probe 003/004 footing when no custom Splitter profile is supplied

Artifacts:
- `_docs/_analysis/reference_probe_008_default_signal_regression/cold_anatomy_reference_probe_008_default_signal_regression.db`
- `_docs/_analysis/reference_probe_008_default_signal_regression/training_pairs_reference_probe_008_default_signal_regression.json`
- `_docs/_analysis/reference_probe_008_default_signal_regression/graph_probe_report_reference_probe_008_default_signal_regression.json`
- `_docs/_analysis/reference_probe_008_default_signal_regression/splitter_signal_profile_effective.json`
- `_docs/_analysis/reference_probe_008_default_signal_regression/bootstrap_profile_effective.json`

Top-line result:
- `relations = 13510`
- `cross-document nucleus pull edges = 169`
- `above-threshold training pairs = 12249`

Interpretation:
- the Splitter signal-control tranche did not perturb the current working graph footing by default
- Probe 003/004 remains the correct behavioral baseline

---

## Probe 009 — Richer Splitter Reference Profile v1

**Date:** 2026-03-28

Purpose:
- test whether a richer Splitter-side reference extraction profile increases cross-document pull over Probe 008 without changing scorer weights

Signal profile used:
- `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_richer_refs_v1.json`

Bootstrap profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Artifacts:
- `_docs/_analysis/reference_probe_009_richer_refs_v1/cold_anatomy_reference_probe_009_richer_refs_v1.db`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/training_pairs_reference_probe_009_richer_refs_v1.json`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/graph_probe_report_reference_probe_009_richer_refs_v1.json`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/splitter_signal_profile_effective.json`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/probe_008_vs_009_delta.json`
- `_docs/_analysis/reference_probe_009_richer_refs_v1/splitter_reference_signal_summary_008_009.json`

Top-line result vs Probe 008:

| Metric | Probe 008 | Probe 009 | Delta |
|---|---:|---:|---:|
| relations | `13510` | `13510` | `0` |
| cross-document nucleus pull edges | `169` | `169` | `0` |
| above-threshold training pairs | `12249` | `12249` | `0` |

Splitter-side reference signal inspection:

| Metric | Default | Richer refs v1 |
|---|---:|---:|
| ref-bearing hunks | `2` | `2` |
| unique normalized refs | `1` | `1` |
| top reference kinds | `markdown_link = 2` | `markdown_link = 2` |

Observed normalized target:
- `shortstring_longstring`

Interpretation:
1. The new Splitter control layer is real and reproducible.
   - `splitter_signal_profile_effective.json` is now saved with probe artifacts.
   - The stable baseline still replays exactly.

2. The current Python reference text corpus still does not expose enough explicit-reference material to move the graph.
   - The richer Splitter profile did not surface additional usable refs in this corpus export.
   - The active text path still exposes only two ref-bearing hunks and one unique normalized target.

3. The next cross-document gain should probably not come from pushing harder on the same sparse reference lane.
   - Better next candidates are:
     - list/index representation work
     - a different explicit-signal family in structured prose
     - or a corpus export that preserves more reference structure than the current textized form

---

## Probe 010 — List/Index Signal Lane v1

**Date:** 2026-03-28

Purpose:
- test whether turning navigational lists into addressable `md_list_item` units with inferred section-like targets improves the graph over Probe 009

Signal profile used:
- `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`

Bootstrap profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Artifacts:
- `_docs/_analysis/reference_probe_010_list_index_v1/cold_anatomy_reference_probe_010_list_index_v1.db`
- `_docs/_analysis/reference_probe_010_list_index_v1/training_pairs_reference_probe_010_list_index_v1.json`
- `_docs/_analysis/reference_probe_010_list_index_v1/graph_probe_report_reference_probe_010_list_index_v1.json`
- `_docs/_analysis/reference_probe_010_list_index_v1/splitter_signal_profile_effective.json`
- `_docs/_analysis/reference_probe_010_list_index_v1/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_010_list_index_v1/probe_009_vs_010_delta.json`

Top-line result vs Probe 009:

| Metric | Probe 009 | Probe 010 | Delta |
|---|---:|---:|---:|
| content nodes | `1083` | `1256` | `+173` |
| occurrence nodes | `1102` | `1275` | `+173` |
| relations | `13510` | `17392` | `+3882` |
| cross-document nucleus pull edges | `169` | `115` | `-54` |
| above-threshold training pairs | `12249` | `15963` | `+3714` |

What changed in the Splitter:

- `reference/index.txt` no longer collapses into three `fragment_of_md_list` hunks.
- It now emits individual `md_list_item` units with inferred normalized targets such as:
  - `lexical_analysis`
  - `execution_model`
  - `line_structure`
  - `file_input`

Full-corpus Splitter signal summary under the list profile:

| Metric | Value |
|---|---:|
| hunks | `1275` |
| ref-bearing hunks | `79` |
| unique normalized refs | `77` |

Interpretation:
1. The list/index lane successfully creates the explicit navigational signal that the earlier richer-reference pass failed to expose.
2. The current bootstrap does use that added structure, but mostly as denser local structure:
   - relation volume rises strongly
   - cross-document pull falls
3. So the extracted signal is likely useful, but it is not yet paired with the right scorer behavior.

Current read:
- Probe 010 is not the new baseline.
- It proves that list/index representation is a real signal source.
- The next targeted experiment should likely be scorer-side handling that can use list/index-derived targets without over-rewarding local structural clustering.

---

## Probe 011 — List/Index Lane With Wider Comparison Window

**Date:** 2026-03-28

Purpose:
- test whether the weak Probe 010 cross-document result was caused by the Emitter’s recency window rather than by the list/index signal itself

Signal profile used:
- `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`

Bootstrap profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Emitter window:
- `window_size = 200`

Artifacts:
- `_docs/_analysis/reference_probe_011_list_index_window200/cold_anatomy_reference_probe_011_list_index_window200.db`
- `_docs/_analysis/reference_probe_011_list_index_window200/training_pairs_reference_probe_011_list_index_window200.json`
- `_docs/_analysis/reference_probe_011_list_index_window200/graph_probe_report_reference_probe_011_list_index_window200.json`
- `_docs/_analysis/reference_probe_011_list_index_window200/splitter_signal_profile_effective.json`
- `_docs/_analysis/reference_probe_011_list_index_window200/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_011_list_index_window200/probe_010_vs_011_delta.json`

Top-line result vs Probe 010:

| Metric | Probe 010 | Probe 011 | Delta |
|---|---:|---:|---:|
| relations | `17392` | `22978` | `+5586` |
| cross-document nucleus pull edges | `115` | `1175` | `+1060` |
| above-threshold training pairs | `15963` | `21549` | `+5586` |

Interpretation:
1. Probe 010’s weak cross-document result was heavily constrained by recency clipping.
   - The Emitter only compares each incoming hunk against the previous `window_size` hunks.
   - With the default `50`, many early `index.txt` items aged out before their target documents arrived.

2. The list/index signal from Probe 010 was genuinely useful.
   - Once the comparison window widened to `200`, cross-document pull rose from `115` to `1175`.
   - That places Probe 011 much closer to the original Probe 001 cross-document scale.

3. The problem now shifts from “is the signal real?” to “how do we keep the gain efficiently?”
   - Probe 011 also increased total training pairs sharply:
     - Probe 010: `62475`
     - Probe 011: `234900`
   - So a brute-force larger window works, but likely is not the final answer.

Current read:
- The list/index lane is validated as useful signal.
- The next likely step is a smarter candidate-selection strategy for reference-targeted comparisons rather than relying on ever-larger sliding windows.

---

## Probe 012 — Targeted Reference Candidates v1

**Date:** 2026-03-28

Purpose:
- test whether a targeted reference-aware candidate-selection path can preserve important long-range list/index-to-target comparisons without using a brute-force `window_size = 200`

Signal profile used:
- `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`

Bootstrap profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Emitter settings:
- `window_size = 50`
- `reference_candidate_limit = 24`

Artifacts:
- `_docs/_analysis/reference_probe_012_targeted_candidates_v1/cold_anatomy_reference_probe_012_targeted_candidates_v1.db`
- `_docs/_analysis/reference_probe_012_targeted_candidates_v1/training_pairs_reference_probe_012_targeted_candidates_v1.json`
- `_docs/_analysis/reference_probe_012_targeted_candidates_v1/graph_probe_report_reference_probe_012_targeted_candidates_v1.json`
- `_docs/_analysis/reference_probe_012_targeted_candidates_v1/probe_011_vs_012_delta.json`

Top-line result:

| Metric | Probe 011 | Probe 012 |
|---|---:|---:|
| relations | `22978` | `19602` |
| cross-document nucleus pull edges | `1175` | `115` |
| above-threshold training pairs | `21549` | `18173` |

What Probe 012 proves:
1. The targeted candidate path works mechanically.
   - The concrete pair
     - `index.txt :: li_4`
     - `lexical_analysis.txt :: h1_2_lexical_analysis`
     now lands above threshold under the normal `window_size = 50`.

2. Candidate-selection v1 is not yet broad or well-ranked enough to replace the wider window.
   - It can rescue specific long-range pairs.
   - But it does not recover the broad corpus-wide Probe 011 gain.

3. The design problem is now clearer.
   - We do not need to prove that targeted long-range comparison is possible.
   - We need to improve its recall and ranking enough that it becomes a real substitute for brute-force window growth.

Current read:
- Probe 011 remains the best “what is possible” reference point.
- Probe 012 is the first proof that a narrower long-range candidate path can rescue real target pairs.
- The next likely step is to refine candidate selection rather than abandoning it or returning to blind extraction work.

---

## Pilot Corpus Probe Set 001 — New Local Material Baselines

**Date:** 2026-03-30

Purpose:
- validate the current pipeline and rudimentary bag on fresh local material outside the Python-reference tuning harness
- capture one prose-heavy multi-file corpus, one compact conceptual text corpus, and one mixed project corpus

Shared bootstrap profile:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Shared emitter setting:
- `window_size = 50`

Validation run after ingest:
- `python -m unittest discover _BDHyperNodeSPLITTER/tests -v`
- `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
- `python .dev-tools/final-tools/smoke_test.py`
- all passed

### Probe: `tech_talks_probe_001`

Source:
- `_corpus_examples/tech_talks`

Artifacts:
- `_docs/_analysis/tech_talks_probe_001/cold_anatomy_tech_talks_probe_001.db`
- `_docs/_analysis/tech_talks_probe_001/graph_probe_report_tech_talks_probe_001.json`
- `_docs/_analysis/tech_talks_probe_001/bag_query_memory_graph.json`

Top-line result:

| Metric | Value |
|---|---:|
| content nodes | `3103` |
| occurrence nodes | `5106` |
| relations | `160088` |
| training pairs | `254775` |
| above-threshold training pairs | `155922` |
| cross-document nucleus pull edges | `1227` |

Bag check:
- query: `"memory graph"`
- surfaced `8` evidence items across `2` source groups
- strongest evidence clustered in:
  - `Another Crazy Convo.txt`
  - `MicroserviceLIBRARY_ Architectural Overview and .md`

Read:
- the prose-heavy pilot generates a dense, highly active graph
- the rudimentary bag already surfaces coherent evidence clusters on this material

### Probe: `paradigm_probe_001`

Source:
- `_corpus_examples/Paradigm`

Artifacts:
- `_docs/_analysis/paradigm_probe_001/cold_anatomy_paradigm_probe_001.db`
- `_docs/_analysis/paradigm_probe_001/graph_probe_report_paradigm_probe_001.json`
- `_docs/_analysis/paradigm_probe_001/bag_query_identity.json`

Top-line result:

| Metric | Value |
|---|---:|
| content nodes | `158` |
| occurrence nodes | `177` |
| relations | `3498` |
| training pairs | `7575` |
| above-threshold training pairs | `3324` |
| cross-document nucleus pull edges | `2422` |

Bag check:
- query: `"identity"`
- surfaced `8` evidence items across `4` source groups
- strongest evidence clustered in:
  - `MemoryLOG_ClosenessToSource_EnergyConcepts.txt`
  - `Dimensioning_Tools.txt`
  - `MemoryLOG_ComingToTermsWith_Consciousness.txt`

Read:
- even a small conceptual text set can produce useful resurfacing behavior
- the bag summary/grouping path is already informative on compact prose corpora

### Probe: `appbuilder_toolbox_probe_001`

Source:
- `_corpus_examples/_AppBuilderTOOLBOX`

Artifacts:
- `_docs/_analysis/appbuilder_toolbox_probe_001/cold_anatomy_appbuilder_toolbox_probe_001.db`
- `_docs/_analysis/appbuilder_toolbox_probe_001/graph_probe_report_appbuilder_toolbox_probe_001.json`
- `_docs/_analysis/appbuilder_toolbox_probe_001/bag_query_mcp_server.json`

Top-line result:

| Metric | Value |
|---|---:|
| content nodes | `847` |
| occurrence nodes | `883` |
| relations | `11687` |
| training pairs | `42875` |
| above-threshold training pairs | `10943` |
| cross-document nucleus pull edges | `2269` |

Bag check:
- initial query `"registry stamper"` returned no evidence
- follow-up query `"mcp server"` surfaced `8` evidence items across `4` source groups
- strongest evidence clustered in:
  - `src/lib/journal_store.py`
  - `src/lib/tool_pack.py`
  - `src/mcp_server.py`
  - `README.md`

Read:
- the current system can already ingest and retrieve across mixed code + markdown material
- query-anchor quality matters; an empty bag here reflected lexical anchoring, not a failed graph build

### Current Interpretation

1. The prototype is no longer only a Python-reference tuning harness.
   - It now has recorded baselines on fresh local prose-heavy and mixed project corpora.

2. The rudimentary bag is already practically useful.
   - It can surface grouped evidence on both conceptual text sets and project/code corpora.

3. The next meaningful comparison is semantic, not structural.
   - We now have enough working ingestion + bag behavior to compare:
     - current deterministic lane
     - traditional embedder lane
   - and judge them through bag outputs rather than only raw graph metrics.

---

## Embedder Comparison Baseline 001 — Deterministic vs Sentence-Transformer

**Date:** 2026-03-30

Purpose:
- compare the current deterministic semantic lane against a traditional sentence embedder on the same bag/query workflow
- do this on:
  - one prose-heavy corpus
  - one mixed project corpus

Traditional model used:
- `sentence-transformers/all-MiniLM-L6-v2`

Important prep note:
- the comparison work surfaced a deterministic-training bug in `cmd_train()`
- that seam is now fixed, and the deterministic artifacts used below were built from small textized training corpora staged under:
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\training_corpora\tech_talks_textized`
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\training_corpora\appbuilder_toolbox_textized`

### Pair A — `tech_talks`

Deterministic artifacts:
- `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\embedding_artifacts\tech_talks_det_v1`

Probe pair:
- deterministic:
  - `_docs/_analysis/tech_talks_probe_002_det/`
- sentence-transformers:
  - `_docs/_analysis/tech_talks_probe_003_st/`

Top-line comparison:

| Metric | Deterministic | Sentence-Transformers |
|---|---:|---:|
| relations | `141879` | `155790` |
| cross-document nucleus pull edges | `1670` | `1372` |
| above-threshold training pairs | `137636` | `151676` |
| relation-level `semantic_resonance` | `658` | `48` |

Bag comparison for query `"memory graph"`:
- deterministic bag artifact:
  - `_docs/_analysis/tech_talks_probe_002_det/bag_query_memory_graph.json`
- sentence-transformers bag artifact:
  - `_docs/_analysis/tech_talks_probe_003_st/bag_query_memory_graph.json`

Observed bag shape:
- deterministic:
  - evidence spread across `Another Crazy Convo.txt`, `master_spec_text.txt`, and `MicroserviceLIBRARY_...`
  - broader topical spread
- sentence-transformers:
  - evidence collapsed much more heavily toward `master_spec_text.txt`
  - less useful variety for this query

Read:
- the sentence model raised total relation volume
- but the deterministic lane produced better cross-document pull and a more useful evidence bag on this corpus

### Pair B — `_AppBuilderTOOLBOX`

Deterministic artifacts:
- `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\embedding_artifacts\appbuilder_toolbox_det_v1`

Probe pair:
- deterministic:
  - `_docs/_analysis/appbuilder_toolbox_probe_002_det/`
- sentence-transformers:
  - `_docs/_analysis/appbuilder_toolbox_probe_003_st/`

Top-line comparison:

| Metric | Deterministic | Sentence-Transformers |
|---|---:|---:|
| relations | `23676` | `14836` |
| cross-document nucleus pull edges | `4154` | `3232` |
| above-threshold training pairs | `22932` | `14092` |
| relation-level `semantic_resonance` | `862` | `36` |

Bag comparison for query `"mcp server"`:
- deterministic bag artifact:
  - `_docs/_analysis/appbuilder_toolbox_probe_002_det/bag_query_mcp_server.json`
- sentence-transformers bag artifact:
  - `_docs/_analysis/appbuilder_toolbox_probe_003_st/bag_query_mcp_server.json`

Observed bag shape:
- deterministic:
  - broader mixed evidence set across `README.md`, `journal_store.py`, `tool_pack.py`, `mcp_server.py`, and `scaffolds.py`
- sentence-transformers:
  - still useful
  - but narrower, more code-heavy, and less cross-document rich

Read:
- on the mixed project corpus, deterministic is clearly stronger than the sentence model in the current prototype configuration

### Current Interpretation

1. The parallel traditional embedder lane is now real.
   - We can run the same ingest and bag workflow with:
     - deterministic embeddings
     - sentence-transformer embeddings

2. The first comparison does not show an off-the-shelf sentence model beating the current deterministic lane.
   - On both tested corpora, deterministic won on cross-document pull.
   - The bag outputs also looked broader and more useful.

3. That result is meaningful.
   - It suggests the current five-surface deterministic geometry is already carrying substantial semantic/retrieval value.
   - The next comparison should be deliberate, not assumptive:
     - another traditional model
     - another query strategy
     - or better bag-level evaluation criteria

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

---

## Probe 007 — Explicit Reference Dial (Sparse Signal)

**Date:** 2026-03-28

Profile used:
- `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v3.json`

Targeted change:
- added a narrow scorer-side explicit reference boost to structural similarity
- current boost consumes:
  - `cross_refs` overlap
  - a small target-hint match against `origin_id`, `structural_path`, and `heading_trail`

Artifacts:
- `_docs/_analysis/reference_probe_007/cold_anatomy_reference_probe_007.db`
- `_docs/_analysis/reference_probe_007/training_pairs_reference_probe_007.json`
- `_docs/_analysis/reference_probe_007/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_007/graph_probe_report_reference_probe_007.json`
- `_docs/_analysis/reference_probe_007/probe_004_vs_007_delta.json`
- `_docs/_analysis/reference_probe_007/probe_events.jsonl`
- `_docs/_analysis/reference_probe_007/probe_run.log`

Delta vs Probe 004:
- `relations = +1`
- `cross-document nucleus pull = 0`
- `above-threshold training pairs = +1`

Observed extra edge:
- one additional in-document `structural_bridge` relation inside `lexical_analysis.txt`
- both fragments carried the extracted `cross_refs` value:
  - `shortstring | longstring`

Read:
- the scorer-side explicit-reference dial works mechanically
- but the current `cross_refs` surface in this prose corpus is far too sparse to unlock meaningful cross-document lift
- the next likely gain is not more boosting of the current sparse signal
- the next likely gain is richer Splitter-side explicit reference extraction for structured prose

---

## Probe 013 — Anchor Registry v1 (More Selective, Not More Cross-Document)

**Date:** 2026-03-30

Profiles used:
- Splitter:
  - `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`
- Bootstrap:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

Targeted change:
- replaced the simple long-range token index in `GraphAssembler` with a ranked occurrence-level anchor registry
- heading anchors now outrank weaker list-ref-only matches
- overly common anchor terms are suppressed after a configurable threshold so they stop flooding long-range recall
- kept the same Phase 1 envelope:
  - `window_size = 50`
  - `reference_candidate_limit = 24`
  - same heavy scorer as final gate

Artifacts:
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/cold_anatomy_reference_probe_013_anchor_registry_v1.db`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/training_pairs_reference_probe_013_anchor_registry_v1.json`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/bootstrap_profile_effective.json`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/splitter_signal_profile_effective.json`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/graph_probe_report_reference_probe_013_anchor_registry_v1.json`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/probe_events.jsonl`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/probe_run.log`

Top-line results:
- `content_nodes = 1256`
- `occurrence_nodes = 1275`
- `relations = 17428`
- `cross-document nucleus pull edges = 115`
- `above-threshold training pairs = 15999`
- `training pairs total = 62583`

Comparison read:
- relative to Probe 011:
  - cross-document pull is still far below the wide-window high-water mark (`1175`)
  - pair volume remains much lower than the Probe 011 explosion (`62583` vs `234900`)
- relative to Probe 012:
  - cross-document pull is unchanged at `115`
  - relation volume is lower (`17428` vs `19602`)
  - above-threshold training pairs are lower (`15999` vs `18173`)

Interpretation:
- the anchor registry is working as intended in one important sense:
  - it makes long-range candidate recall more selective
  - it suppresses weak/common-anchor flooding
- but the current anchor-only recall lane is still too narrow to recover the Probe 011 gain
- that points to the next likely move being a deterministic cheap-fetch fallback, most likely by reusing SQLite FTS when anchor recall returns too little signal

---

## Query Experiment 001 — Anisotropic Blur Lens

**Date:** 2026-03-30

Builder tool:
- `.dev-tools/final-tools/tools/anisotropic_blur_probe.py`

Purpose:
- test a soft query-conditioned neighborhood projection over existing graph probes
- keep it builder-side and read-only
- see whether the blur reveals useful neighborhood structure or cross-document spread that the current bag does not

### Reference bottleneck case

Query:
- `lexical analysis`

DB:
- `reference_probe_013_anchor_registry_v1`

Artifacts:
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/anisotropic_blur_lexical_analysis.json`
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/bag_query_lexical_analysis.json`

Observed data:
- FTS seeds were sensible and cross-document:
  - `index.txt`
  - `lexical_analysis.txt`
  - `introduction.txt`
  - `expressions.txt`
- local subgraph:
  - `211` nodes
  - `3747` edges
- but the blur top set collapsed into dense `index.txt` list-item hubs
- `top_cross_document_count = 0`

Comparison with bag:
- current bag stayed more source-diverse and more evidentially useful
- bag top groups included:
  - `introduction.txt`
  - `lexical_analysis.txt`
  - `expressions.txt`
  - `index.txt`

Read:
- the blur is highly sensitive to dense local hub structure in this corpus
- useful as a field-shape diagnostic
- not yet useful as a better evidence surface

### Mixed code/doc graph

Query:
- `mcp server`

DB:
- `appbuilder_toolbox_probe_002_det`

Artifacts:
- `_docs/_analysis/appbuilder_toolbox_probe_002_det/anisotropic_blur_mcp_server.json`
- `_docs/_analysis/appbuilder_toolbox_probe_002_det/bag_query_mcp_server_top10.json`

Observed data:
- local subgraph:
  - `304` nodes
  - `6193` edges
- `top_cross_document_count = 4`
- blur top set surfaced a strong procedural neighborhood around:
  - `smoke_test.py`
  - `journal_acknowledge.py`
  - `journal_actions.py`
  - `journal_init.py`
  - `journal_export.py`

Comparison with bag:
- current bag remained more directly relevant to the external-agent use case:
  - `README.md`
  - `tool_pack.py`
  - `mcp_server.py`
  - `journal_store.py`
  - `scaffolds.py`

Read:
- the blur is exposing topological/procedural neighborhood
- the bag is exposing more directly relevant evidence
- so the blur appears additive as a diagnostic lens, not superior as retrieval
