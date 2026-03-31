# BDNeuralTranslationSUITE — Test Report

_Generated: 2026-03-30_

This report is a shareable summary of the project's testing over time, with emphasis on:
- end-to-end Splitter -> Emitter graph probes
- bottleneck-focused reference-corpus experiments
- current automated test-suite status
- cross-corpus and bag validation
- embedder comparisons
- recent contradiction and hub-concentration diagnostics

It is intended to be read alongside:
- `_docs/GRAPH_PROBES.md`
- `_docs/DEV_LOG.md`
- `_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`

---

## 1. Current Automated Validation

Last run:
- `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`

Current status:
- `30 / 30` tests passing

Coverage areas included in the current passing suite:
- bootstrap config validation and round-trip behavior
- bootstrap behavior expectations
- contradiction seam behavior
- FTS fallback behavior
- long-range reference candidate selection
- bag output shape
- embedding provider metadata behavior

Current emitter-facing test inventory:
- `test_bag_view.py`
- `test_bootstrap_config.py`
- `test_embedding_provider.py`
- `test_reference_candidate_selection.py`

Current implication:
- the Emitter is stable enough to keep running narrow scorer/candidate experiments without basic regression fear

---

## 2. Reference Probe Timeline

The table below focuses on the Python-reference bottleneck line, because that is the cleanest controlled chronology of the current main problem.

| Probe | Date | Focus | Relations | Cross-Doc Pull | Above Threshold | Total Pairs | Read |
|---|---|---|---:|---:|---:|---:|---|
| `001` | 2026-03-27 | First full Python-reference baseline | `22406` | `1293` | `21145` | `53825` | Strong signal, but grammar-heavy collapse |
| `002` | 2026-03-27 | First prose grammar de-bias | `2897` | `147` | `1636` | `53825` | Overcorrected, starved graph |
| `003` | 2026-03-27 | Starter tuning profile recovery | `13510` | `169` | `12249` | not recorded here | Good stable baseline recovery |
| `004` | 2026-03-28 | Observable replay of Probe 003 | `13510` | `169` | `12249` | not recorded here | Confirmed baseline is stable |
| `005` | 2026-03-28 | Structural -> statistical shift | `9072` | `163` | `7811` | not recorded here | Negative branch |
| `006` | 2026-03-28 | Heading boost | `13510` | `169` | `12249` | not recorded here | No lift |
| `007` | 2026-03-28 | Explicit ref dial | `13511` | `169` | `12250` | not recorded here | Signal too sparse to matter |
| `008` | 2026-03-28 | Post-signal-control default regression | `13510` | `169` | `12249` | not recorded here | Stable replay |
| `009` | 2026-03-28 | Richer reference extraction profile | `13510` | `169` | `12249` | not recorded here | No effect on this textized corpus |
| `010` | 2026-03-28 | List/index lane activation | `17392` | `115` | `15963` | `62475` | More structure, worse long-range pull |
| `011` | 2026-03-28 | Wider window (`200`) | `22978` | `1175` | `21549` | `234900` | Proves long-range signal is real, but too expensive |
| `012` | 2026-03-28 | Targeted reference candidates v1 | `19602` | `115` | `18173` | not recorded here | Narrow path works mechanically, but not broadly enough |
| `013` | 2026-03-30 | Anchor registry v1 | `17428` | `115` | `15999` | `62583` | Selective, still too narrow |
| `014` | 2026-03-30 | Native FTS fallback v1 | `17457` | `115` | `16028` | `63155` | Cheap recall exists, but does not convert |
| `015` | 2026-03-30 | Control replay of current footing | `17457` | `115` | `16028` | `63155` | Confirms local probe footing |
| `015b` | 2026-03-30 | Mild contradiction penalty v1 | `15046` | `115` | `13617` | `63155` | Too blunt, suppressed useful traffic |
| `015c` | 2026-03-30 | Tightened contradiction penalty | `17457` | `115` | `16028` | `63155` | Clean seam, but no bottleneck lift |
| `016` | 2026-03-30 | FTS per-origin cap (`1`) | `17447` | `115` | `16018` | `62789` | De-monopolized fallback lane, still no lift |

### Reference-Line Conclusions

What the reference line has already proved:
- The long-range signal is real.
  - Probe `011` is the clean proof: widening the comparison horizon lifts cross-document pull from `115` to `1175`.
- The current bottleneck is not "there is no long-range structure."
  - It is "how to recover long-range structure under bounded pair cost."
- The current bottleneck is also not solved by a cheap fetch lane alone.
  - Probe `014` recovered `548` selected cross-document FTS candidates and still stayed flat at `115`.
- The contradiction seam is now truthful and implemented, but it is not yet the force shaping this landscape.
  - Probe `015b` showed naive anti-pressure can hurt.
  - Probe `015c` showed the cleaned version is safe but currently weak.
- A single-origin FTS monopoly is not the whole explanation either.
  - Probe `016` reduced FTS-selected candidates sharply without changing the headline plateau.

Current reference-line diagnosis:
- The project now appears to be stuck at **candidate-to-edge conversion**, not at raw candidate discovery.

---

## 3. Cross-Corpus Validation

These tests matter because they show the project is not only a Python-reference harness.

| Probe | Corpus | Relations | Cross-Doc Pull | Above Threshold | Read |
|---|---|---:|---:|---:|---|
| `tech_talks_probe_001` | prose-heavy local corpus | `160088` | `1227` | `155922` | Dense graph, bag already useful |
| `paradigm_probe_001` | compact conceptual corpus | `3498` | `2422` | `3324` | Strong resurfacing on small conceptual text set |
| `appbuilder_toolbox_probe_001` | mixed code + docs | `11687` | `2269` | `10943` | Mixed code/doc ingest and bag retrieval already practical |

Cross-corpus implication:
- the pipeline is viable outside the bottleneck corpus
- the bag seam is already useful in multiple content regimes
- the reference bottleneck is a real local problem, not proof that the whole architecture fails

---

## 4. Embedder Comparison Tests

The project also ran a direct deterministic-vs-traditional comparison on live corpora.

### `tech_talks`

| Mode | Relations | Cross-Doc Pull | Above Threshold | Semantic Resonance | Read |
|---|---:|---:|---:|---:|---|
| Deterministic | `141879` | `1670` | `137636` | `658` | Better cross-doc pull and broader bag evidence |
| Sentence-Transformers | `155790` | `1372` | `151676` | `48` | More relations, but weaker cross-doc retrieval behavior |

### `_AppBuilderTOOLBOX`

| Mode | Relations | Cross-Doc Pull | Above Threshold | Semantic Resonance | Read |
|---|---:|---:|---:|---:|---|
| Deterministic | `23676` | `4154` | `22932` | `862` | Stronger on both graph and bag usefulness |
| Sentence-Transformers | `14836` | `3232` | `14092` | `36` | Useful, but clearly weaker in this prototype shape |

Embedder comparison conclusion:
- the deterministic lane is currently outperforming the tested sentence-transformer baseline on both corpora
- the project's current five-surface deterministic geometry appears to be carrying real semantic/retrieval value

---

## 5. Query and Diagnostic Tests

### Bag Validation

Representative successful bag queries:
- `tech_talks_probe_001` with query `"memory graph"`
- `paradigm_probe_001` with query `"identity"`
- `appbuilder_toolbox_probe_001` with query `"mcp server"`

Observed behavior:
- bag outputs are already grouped, readable, and useful across prose and mixed code/doc corpora
- weak bag output has so far correlated more with poor lexical anchoring than with failed graph construction

### Anisotropic Blur Diagnostic

Reference bottleneck case:
- query: `"lexical analysis"`
- blur collapsed into dense `index.txt` hub neighborhoods
- `top_cross_document_count = 0`

Mixed code/doc case:
- query: `"mcp server"`
- blur surfaced a strong procedural neighborhood
- `top_cross_document_count = 4`

Diagnostic read:
- blur is currently better as a **field-shape / topology diagnostic**
- bag remains the better evidence surface

---

## 6. Latest Contradiction and Hub-Audit Experiments

### Contradiction v1 Runs

| Run | Relations | Cross-Doc Pull | Above Threshold | Anti-Signal Pairs | Blocked Pairs | Read |
|---|---:|---:|---:|---:|---:|---|
| `015` control | `17457` | `115` | `16028` | `0` | `0` | current baseline replay |
| `015b` mild penalty | `15046` | `115` | `13617` | `5898` | `0` | too blunt; suppressed useful navigational traffic |
| `015c` tightened penalty | `17457` | `115` | `16028` | `199` | `0` | seam now clean, but not impactful on bottleneck |

Current contradiction read:
- contradiction v1 is now a truthful soft-pressure seam
- it is useful for inspection/export
- it is not yet the main force shaping the current bottleneck

### Hub / Source Concentration Audit

From the current control footing (`reference_probe_015_contradiction_control`):

Cross-document winner concentration:
- `unique_origins = 5`
- `top_1_share = 0.2957`
- `top_3_share = 0.8`
- `top_5_share = 1.0`

Top cross-document source origins:
- `executionmodel.txt` = `34`
- `introduction.txt` = `32`
- `simple_stmts.txt` = `26`
- `lexical_analysis.txt` = `17`
- `import.txt` = `6`

Above-threshold source concentration:
- `unique_origins = 11`
- `top_1_share = 0.2143`
- `top_3_share = 0.515`
- `top_5_share = 0.7796`

Top above-threshold source origins:
- `datamodel.txt` = `3435`
- `index.txt` = `2657`
- `compound_stmts.txt` = `2162`
- `simple_stmts.txt` = `2125`
- `expressions.txt` = `2116`

Interpretation:
- the overall graph is somewhat hub-like
- but the **cross-document winners themselves are not dominated by `index.txt`**
- so the current `115` plateau is not explained simply by "index monopolizes all winning mass"

### FTS Per-Origin Cap Test

`reference_probe_016_fts_origin_cap1` compared against current control:

| Metric | Control (`015`) | Cap = 1 (`016`) | Delta |
|---|---:|---:|---:|
| relations | `17457` | `17447` | `-10` |
| cross-document pull | `115` | `115` | `0` |
| above-threshold pairs | `16028` | `16018` | `-10` |
| training pairs | `63155` | `62789` | `-366` |
| FTS selected | `572` | `206` | `-366` |
| FTS selected cross-doc | `548` | `179` | `-369` |
| FTS origin-cap skips | `0` | `446` | `+446` |

Interpretation:
- the cap is real and active
- but it does not produce the phase shift
- this falsifies the hypothesis that "one FTS origin monopolizing the fallback lane" is the main reason for the plateau

---

## 7. What Has Been Falsified

These are useful because they prevent over-engineering:

- "The bottleneck is just sparse reference extraction."
  - False as a full explanation.
  - Probe `010` and `011` proved the list/index lane is real and useful.

- "The bottleneck is solved by widening the window."
  - False as a practical solution.
  - Probe `011` works, but pair cost explodes.

- "The bottleneck is solved by anchor-only targeted recall."
  - False.
  - Probe `013` stayed at `115`.

- "The bottleneck is solved by adding a cheap FTS fetch lane."
  - False.
  - Probe `014` recovered many cross-document candidates but still stayed at `115`.

- "The current plateau is mainly caused by one fallback origin monopolizing the FTS lane."
  - False.
  - Probe `016` broke that monopoly and still stayed flat.

- "Contradiction pressure is already the key missing physics."
  - False for the current repo state.
  - Probe `015c` shows contradiction v1 is now real but not a bottleneck mover yet.

---

## 8. What The Test History Now Supports

The strongest current claim supported by the tests is:

> The long-range cross-document signal is real, cheap bounded recall can recover candidate neighborhoods, but the project is currently failing at **candidate-to-edge conversion** under bounded cost.

More concretely:
- the system can find distant land
- it can even cheap-fetch some of that land
- but the scorer is still not converting enough of those recovered distant candidates into winning cross-document pull edges

This is where the next test tranche should focus.

---

## 9. Suggested Next Tests

Based on the full test history so far, the highest-value next experiments are:

1. Add loser diagnostics for FTS-selected cross-document candidates.
   - We need to see why recovered candidates fail:
     - low structural support?
     - low grammatical support?
     - threshold margin?
     - dominated by nearer candidates?

2. Compare winning `115` cross-document edges against losing FTS-selected cross-document candidates.
   - Surface-by-surface support decomposition is likely the next real seam.

3. Keep contradiction and hub concentration as diagnostic layers.
   - They are useful now for truth-telling, but not yet the main optimization line.

4. Continue recording every new probe against the same reference footing.
   - The project now has enough history that falsifying bad ideas is almost as valuable as landing a lift.

---

## 10. Bottom Line

The test record says the project is healthy, but the specific bottleneck remains unsolved.

Healthy because:
- automated tests are green
- the bag works
- multiple corpora validate the broader pipeline
- deterministic retrieval is competitive and often stronger than the tested sentence-transformer baseline

Unsolved because:
- the bounded-cost reference line is still flat at `115`
- cheap recall exists
- but conversion still fails

That is the clearest current insight the full test range supports.
