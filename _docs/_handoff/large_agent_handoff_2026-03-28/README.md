# Large Agent Handoff Pack

Date: `2026-03-28`

This folder is a temporary handoff package for a large reasoning agent.

It exists because the current project truth does **not** live in the journal DB alone. The most accurate state is spread across:
- root architecture and recovery docs
- probe history and measured deltas
- builder constraint contract
- selected journal continuity records

## What To Read First

1. `WE_ARE_HERE_NOW.md`
2. `ARCHITECTURE.md`
3. `TODO.md`
4. `GRAPH_PROBES.md`
5. `NL_NarrativeDESC.md`
6. `builder_constraint_contract.md`
7. `journal_selected_entries.json`

## Why This Pack Exists

We want a large agent to help explore options for the next prototype step without letting it:
- drift into hype
- ignore the current measured probe loop
- propose bag/FFN work too early
- lose the builder-constraint contract

The specific open problem right now is:

`simple bootstrap profile dials appear close to exhausted for improving cross-document pull on the Python reference corpus without reintroducing coarse grammatical collapse`

## Current Measured Reality

- Probe 003 and Probe 004 are the stable observable baseline.
- Probe 005 was a negative result:
  - shifting some surface weight from `structural` to `statistical` reduced graph activity and slightly reduced cross-document pull.
- Probe 006 was also a negative result:
  - boosting heading-specific grammatical weight did not improve cross-document pull.

So the next useful ideas likely need to be:
- a more granular bootstrap-code dial, or
- a Splitter-side representation improvement

not just another blunt profile-only retune.

## Important Constraints

- This project is a durable evidence / relational-memory engine for agents.
- It is not primarily an answer generator.
- Current build order remains:
  - neurons first
  - living graph second
  - bag seam third
- Do not recommend implementing the bag or FFN yet as the immediate next move.

## Files In This Pack

- `WE_ARE_HERE_NOW.md`
- `ARCHITECTURE.md`
- `TODO.md`
- `DEV_LOG.md`
- `GRAPH_PROBES.md`
- `NL_NarrativeDESC.md`
- `PARKING_LOT_QUESTIONS.md`
- `builder_constraint_contract.md`
- `python_reference_prose_tuning.json`
- `python_reference_crossdoc_tuning_v1.json`
- `python_reference_crossdoc_tuning_v2.json`
- `journal_selected_entries.json`
- `PROMPT_FOR_LARGE_AGENT.md`

## Suggested Use

Give the large agent this whole folder, not only the journal DB.

If the agent also has access to the repo, tell it to inspect:
- `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py`
- `_BDHyperNodeSPLITTER/src/core/engines/peg_eng.py`
- `_BDHyperNodeSPLITTER/src/core/engines/fallback_eng.py`
- `_docs/_analysis/reference_probe_004/`
- `_docs/_analysis/reference_probe_005/`
- `_docs/_analysis/reference_probe_006/`

Delete this folder after handoff if you do not want to keep it.
