# Session Close Report - 2026-04-02

This note freezes the branch reintegration, the real-English baseline leg, and
the current shared-view workflow read before the next pickup.

## What We Just Locked In

- The `baseline-leg-sidecar` branch is now treated as a concluded
  diagnostic/reference seam, not a second product line.
- Mainline doctrine has shifted in two important ways:
  - collaboration should prefer a shared registry / shared visible state
  - corpus planning should now start with general English before code-specific corpora
- A minimal separate shared viewer sidecar is now the intended collaboration surface.
- Human-driven shared-state viewing is proven.
- Agent-driven visible panel action is still experimental and is now explicitly
  disabled by default unless the viewer is launched with `--enable-panel-actions`.

## Real-English Baseline Read

The `tech_talks` footing was the most useful new branch-local corpus result:

- it is small enough to iterate on quickly
- it contains ordinary conversational English plus project-specific technical phrasing
- it exposed meaningful differences between retrieval legs

Current read on that footing:

- `fts`
  - strongest on explicit phrase queries
  - best example: `black box`
- `sentence-transformers` ANN
  - closest thing to a conventional semantic prose baseline
  - useful, but flatter and more fragment-prone than the bag
- deterministic ANN
  - provisioned successfully on the same footing
  - still weaker as a standalone prose retriever on that corpus
- `bag`
  - strongest shaped evidence shelf
  - often preserves the lexical win while widening the evidence region

## Shared Viewer Read

What is now trustworthy:

- the viewer launches on `PHASE_02`
- it writes shared session state
- after human actions, the registry reflects:
  - query
  - mode
  - provider
  - selected item
  - last action label
  - shelf payload

What is not yet trustworthy:

- agent-driven pending-action execution through the panel

So the current trust boundary is:

- shared-state viewing: yes
- shared-state-driven agent action: not yet

## Validation

Mainline branch smoke:

- branch:
  - `PHASE_02`
- viewer smoke:
  - created a fresh shared session on `PHASE_02`
  - session reflected `gravity` / `bag` / `shared-visible` correctly
- sidecar tests:
  - `python -m unittest _BDHyperNeuronEMITTER.tests.test_baseline_leg_sidecar -v`
  - `7/7` passing

## Current Recommendation

Treat the next mainline move as:

1. keep the shared registry doctrine
2. keep the minimal separate shared viewer
3. stop workflow experimentation for now
4. start designing the functional English baseline corpus tranche

Do **not** let the next move become:

- more branch-local workflow invention
- a storage/compression architecture branch
- or a code-first corpus plan

## What Should Shape The Next Pickup

- shared registry is now part of project doctrine
- general English baseline comes before code-specific corpora
- lexical retrieval remains a preserved baseline/control leg
- the bag remains the stronger shaped evidence shelf
- agent-driven panel execution is still a bounded bug/follow-up seam, not current truth
