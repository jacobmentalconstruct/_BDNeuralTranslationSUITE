# Session Close Report - 2026-04-01

This note freezes the late-session breakthroughs, the compact validation set, and the current recommendation before the next pickup.

## What We Just Locked In

- The live probe monitor is now materially better:
  - clearer live metric cards
  - summary and sample tabs in the same window
  - five-surface color cues
  - explicit typed `report_summary` / `report_snapshot` events behind the UI
- The deterministic semantic-gravity lane remains the strongest semantic lane on the current Python-reference footing.
- The new semantic-gravity shape sweep shows **saturation**, not a new hidden regime:
  - stronger gravity still moves the graph slightly
  - but the gains are now marginal
  - the bag-facing top shelf stayed stable across the deterministic variants tested

## Compact Validation Set

### Full emitter suite

- command:
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
- result:
  - `46/46` passing

### Monitor typed-event smoke

- command:
  - `python .dev-tools/final-tools/tools/run_reference_probe_monitor.py --probe-name reference_probe_076_monitor_typed_event_smoke --bootstrap-profile _BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_origin_aware_crossdoc_v1_threshold_058_semantic_gravity_steep.json --embedder deterministic --no-show-ui`
- result:
  - completed cleanly
  - emitted `report_summary`
  - emitted `report_snapshot`
  - wrote the full probe bundle under `_docs/_analysis/reference_probe_076_monitor_typed_event_smoke`

### Bag semantic-shape QC

Artifact:
- [`bag_semantic_shape_qc_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\bag_semantic_shape_qc_2026-04-01\bag_semantic_shape_qc_2026-04-01.md)

Query shelf:
- `lexical analysis`
- `encoding declarations`
- `yield expressions`
- `operator precedence`
- `assignment expressions`
- `lambda expressions`
- `function definitions`
- `import statements`
- `resolution of names`
- `eval input`
- `interactive input`

Result:
- `det_control`: same top shelf as itself on `11/11`
- `det_steep`: same top shelf as control on `11/11`
- `det_softplus`: same top shelf as control on `11/11`
- `det_high`: same top shelf as control on `11/11`
- `det_xhigh`: same top shelf as control on `11/11`

Meaning:
- the deterministic semantic-gravity shape variants did **not** degrade the current human-facing top shelf on this validation set
- so the next choice is not about “which one stops the bag from breaking”
- it is about which one gives the best graph gain without over-collapsing the winner field into pure semantic dominance

## Semantic-Gravity Shape Read

Deterministic lane:

| Profile | Cross-doc pull | Relations | Above-threshold | Cross-doc winner shape |
| --- | ---: | ---: | ---: | --- |
| control | 10955 | 56438 | 55009 | mixed, semantic-led but still visibly multi-surface |
| low | 11697 | 57167 | 55738 | stronger semantic share, still mixed |
| mid | 12052 | 57503 | 56074 | semantic much stronger, diversity dropping |
| steep | 12067 | 57512 | 56083 | near-high lift, but keeps more `multi_surface` / `structural_bridge` |
| softplus | 12106 | 57542 | 56113 | strong compromise, but more semantic-dominant than `steep` |
| high | 12133 | 57568 | 56139 | near-saturation, mostly `semantic_resonance` winners |
| xhigh | 12159 | 57594 | 56165 | only marginal gain over `high`, even more semantic-dominant |

## Current Recommendation

Do **not** treat `xhigh` as the new default just because it is numerically largest.

Current best read:
- `xhigh` is useful as a stress test
- `high` proves the field is real
- `softplus` is a pragmatic strong candidate
- `steep` is the safest balanced candidate if we care about preserving more non-semantic winner geometry

So the immediate next-default question is probably:
- choose between `steep` and `softplus`
- keep `high` and `xhigh` as informative ceiling points, not defaults

## What This Means For Phase 1

Phase 1 is now clearly a **five-surface mapping program**, not a search for one lucky profile.

The current state of the field:
- `structural` is still the main load-bearing surface
- `grammatical` is strongly active
- `semantic` is now clearly useful when treated as a bounded overlay field
- `verbatim` and contradiction / anti-signal still need more deliberate contextual mapping

That means the path stays:
- keep the anchor lens stable
- map bounded overlays and side-lenses carefully
- validate every numeric gain against bag readability and verbatim/structural truth

## Handoff Importance

This session’s handoff package should preserve:
- the monitor upgrade
- the actual code paths changed
- the actual test result (`46/46`)
- the actual probe result records
- the semantic-gravity shape comparison
- the current recommendation (`steep` / `softplus` are safer than `xhigh`)
