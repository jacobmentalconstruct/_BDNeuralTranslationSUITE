You are reviewing a prototype codebase called `BDNeuralTranslationSUITE`.

Your job is **not** to rewrite the whole project or invent a new vision. Your job is to analyze the current state, respect the builder constraints, and propose the most promising next options for improving the prototype.

## Read These Files First

In this order:

1. `WE_ARE_HERE_NOW.md`
2. `ARCHITECTURE.md`
3. `TODO.md`
4. `GRAPH_PROBES.md`
5. `NL_NarrativeDESC.md`
6. `builder_constraint_contract.md`
7. `journal_selected_entries.json`

Then inspect these tracked tuning profiles:

- `python_reference_prose_tuning.json`
- `python_reference_crossdoc_tuning_v1.json`
- `python_reference_crossdoc_tuning_v2.json`

If you have access to the repo, inspect these code locations:

- `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py`
- `_BDHyperNeuronEMITTER/src/app.py`
- `_BDHyperNodeSPLITTER/src/core/engines/peg_eng.py`
- `_BDHyperNodeSPLITTER/src/core/engines/fallback_eng.py`

If you have access to the probe artifact folders, inspect:

- `_docs/_analysis/reference_probe_004/`
- `_docs/_analysis/reference_probe_005/`
- `_docs/_analysis/reference_probe_006/`

## What This System Is

This is a durable evidence / relational-memory substrate for agents.

It is trying to preserve context as multi-surface units, connect those units in a graph, and expose evidence with traceable reasons for why connections happened.

It is **not** primarily an answer generator.

The active surfaces are:
- `verbatim`
- `structural`
- `grammatical`
- `statistical`
- `semantic`

Current architecture:
- Splitter populates surfaces
- Emitter / Bootstrap Nucleus decides relation strength and routing profile
- Cold Artifact stores the graph and why edges happened

## Current Project State

The current stable measured baseline is:
- Probe 003
- Probe 004 (observable replay of the same footing)

Important recent measured results:

- Probe 005:
  - shifted some weight from `structural` to `statistical`
  - result: worse graph activity and slightly worse cross-document pull

- Probe 006:
  - increased heading-specific grammatical weight
  - result: no improvement in cross-document pull

Interpretation:
- simple profile-only dials may be close to exhausted for the current target

## The Current Open Problem

We want to improve **cross-document pull quality / count** on the Python reference corpus **without**:
- returning to Probe 001-style grammar collapse
- jumping prematurely to FFN implementation
- jumping prematurely to bag implementation
- abandoning the current measurable probe loop

## What You Should Deliver

Please produce:

1. A short diagnosis of where the current bottleneck most likely is:
   - bootstrap-code dial limitation
   - Splitter representation limitation
   - missing semantic lane
   - some combination

2. A ranked list of the **best next 3 options** for the project.

For each option, include:
- why it is promising
- whether it is scorer-side or Splitter-side
- what exact signal it would add or refine
- what metric movement you would expect in the probe loop
- what risk it carries

3. A recommendation for the **single next experiment** to run.

It should be:
- small
- measurable
- compatible with the current probe workflow
- plausible to implement in one tranche

4. A short note on whether the current simple profile dials are truly close to exhausted, or whether there is still one high-value profile-only move left.

## Important Non-Goals

Do **not** recommend as the immediate next step:
- implementing the bag
- implementing the FFN
- broad retrieval redesign
- replacing the architecture doctrine

Stay grounded in the current code and measured probe history.

## Tone / Framing

Be concrete, non-hype, and technically disciplined.

Treat this as a prototype-tuning consultation, not a greenfield ideation exercise.
