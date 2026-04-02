# Shared Registry Workflow

## Purpose

This document records the collaboration pattern promoted out of the
`baseline-leg-sidecar` experiment.

The goal is not hidden tool use. The goal is a shared visible working surface
where the human and the builder can stay synchronized to the same query state,
the same evidence shelf, and the same recent action provenance.

## Current Proven Baseline

- A file-backed shared registry is a workable truth surface for collaboration.
- A separate sidecar viewer is a good first mainline landing point.
- Human-driven shared-state viewing is proven.
- Session parity is already useful:
  - query
  - DB
  - mode
  - provider
  - selected item
  - last action label
  - shelf payload
- Agent-driven visible panel actions are not yet a proven mainline behavior.

## Working Doctrine

Preferred collaboration loop:

1. sync to shared state
2. reason from shared state
3. act through the agreed tool or panel surface
4. resync after the action

This project should prefer explicit synchronization over hidden operation when
the work is exploratory, evidence-facing, or intended to teach both sides how
the system behaves.

## Mainline Scope In This Tranche

Promoted:
- registry-first shared-state support
- minimal separate shared viewer sidecar
- visible last-action provenance
- builder/setup documentation for the workflow

Not yet promoted as mainline truth:
- experimental pending-action execution through the viewer
- full live UI telemetry
- background automation assumptions

## Current Tool Surface

Minimal shared-view sidecar tools:
- `.dev-tools/final-tools/tools/baseline_leg_viewer.py`
- `.dev-tools/final-tools/tools/baseline_leg_session.py`

Experimental follow-up helper:
- `.dev-tools/final-tools/tools/baseline_leg_panel_action.py`

The panel-action helper remains experimental unless the viewer is explicitly run
with panel-action execution enabled and that seam is proven reliable.
