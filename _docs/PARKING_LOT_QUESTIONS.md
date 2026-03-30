# Parking Lot Questions

_Last updated: 2026-03-27. This file holds higher-level questions worth preserving without letting them derail the current tranche._

## Why this file exists

Some questions are important but not immediately actionable inside the current build loop.

This file is for those questions.

The goal is to preserve direction and curiosity without mixing long-horizon theory work into the next concrete engineering step.

## Current parking-lot questions

### 1. What role should BPE ultimately play?

Questions to keep alive:
- Is BPE mainly a practical token-budget and statistical-surface tool?
- Does BPE define a meaningful constraint surface for where relational meaning can be discovered?
- How much should the eventual system depend on BPE-specific segmentation versus richer language- or modality-specific representations?

Why this matters:
- BPE is currently part of the training and statistical path.
- It may be a useful scaffold, but it may not deserve to define the deeper representational boundaries of the full system.

### 2. How language-specific should the system become?

Questions to keep alive:
- Should the system remain mostly language-agnostic at the shared neuron/graph level?
- Should some surfaces be strongly specialized for natural language, programming languages, or other data types?
- Where is the right boundary between shared cross-domain contract and modality-specific enrichers?

Why this matters:
- The current project already straddles prose and code.
- Future growth may include non-NL and non-code data, which raises contract and routing questions early.

### 3. How far should the graph go toward a manifold-like memory model?

Questions to keep alive:
- Is the graph the primary substrate, or just the visible projection of a deeper relational manifold?
- Which parts of the current system should remain graph-explicit and inspectable?
- Which parts, if any, should eventually be gradient-shaped but not directly graph-shaped?

Why this matters:
- The project originated in a very abstract memory/manifold framing.
- The current prototype is intentionally more concrete and measurable.
- We should keep the connection between those views without letting the abstract framing outrun the code.

### 4. What is the eventual division of labor between scaffold math and learned behavior?

Questions to keep alive:
- Which relational behaviors should remain explicit dials even after the FFN exists?
- Which behaviors should be learned from data and no longer hand-tuned?
- What should always remain inspectable for agent trust and debugging?

Why this matters:
- We are currently tuning the scaffold.
- Later, the FFN must not erase interpretability that the graph/evidence system depends on.

## Current rule for this file

Do not turn these into implementation work unless they directly unblock the active tranche.

When one of these questions becomes actionable, move the concrete part into:
- `_docs/TODO.md`
- `_docs/ARCHITECTURE.md`
- or a tranche-specific design note
