# Scope Root, Bag Slice, and Two-Sided Anchoring

_Date: 2026-03-31. Status: doctrine / planning truth, not current runtime implementation._

## Why this note exists

The project now has enough signal to see a future retrieval shape more clearly without pretending that shape already exists in runtime.

This note consolidates the new read:
- the bag is not "all knowledge"
- the bag is not just a loose evidence list
- the bag is better understood as a bounded local slice where observer intent and source structure meet

This is a planning surface for later retrieval / bag / walker work. It should not be read as proof that the current runtime already behaves this way.

## The bag as a bounded slice

We cannot activate a manifold field of all human knowledge.

The useful unit is a slice:
- bounded
- inspectable
- tied to the current observer state
- tied to the current source neighborhood

In this framing, the bag is the slice interface.

The observer sees a list of evidence or a pullback surface.
Under the hood, the bag is better understood as an observer-centered local subgraph.

## Anchor node and the five surfaces

The current observational foothold is the anchor node.

The five surfaces explain different aspects of that anchor:
- `verbatim`
  - what this thing actually is, exactly
- `structural`
  - where it sits and how it is positioned
- `semantic`
  - what it resembles or feels like
- `grammatical`
  - how it tends to behave with neighboring things of its kind
- `statistical`
  - what relation regularities and availability patterns surround it

This means the anchor is not understood by one view alone.
It is understood by a layered reading of the local node.

## Two-sided anchoring

The newer and stronger read is that the bag sits between two anchored sides.

### Observer-side anchor

The observer side includes:
- user / human / agent / calling app
- query
- current conversation state
- current local memory state
- current task intent

### Source-side anchor

The source side includes:
- the chosen source entry
- the chosen scope root
- the nearby source structure
- the evidence neighborhood that can legitimately answer the query

### Join boundary

The bag is the bounded join boundary where these two anchored sides meet.

That means the bag is not merely retrieval output.
It is the constrained meeting place between observer intent and source structure.

### Response anchor

The answer is not pre-existing in the same way the source graph is.

So the better later shape is:
- observer-side anchor
- source-side anchor
- bag as bounded join boundary
- response anchor as answer-shape constraint

This keeps the answer grounded without pretending it was already sitting inside the graph verbatim.

## Scope root

The system should not begin from one universal granularity.

It should begin from a chosen scope root such as:
- folder
- file
- heading
- section
- class
- function
- page
- paragraph
- line span

The chosen scope root determines what "nearby" means.

## Resolution grammar

Each scope root should carry a local grammar of next-valid moves.

Examples:
- parent
- child
- sibling
- sequential neighbor
- incoming reference
- outgoing reference

This is the missing control grammar that later bag/walker work needs.

## Direction of spread

The slice should not warm in all directions equally.

Later retrieval should be able to spread by meaningful direction, such as:
- structural
- sequential
- referential
- semantic
- causal or procedural

Intent should bias which directions warm first.

## Stop-unwinding logic

The system should not always decompose deeper.

Later decomposition needs a stop rule:
- stop when the next finer layer no longer adds enough signal
- stop when further fragmentation mostly adds noise
- stop when the local unit is already functionally digestible

This is the safer reading of the weather / coarse-to-fine analogy:
- coarse global view first
- finer nested view only where the local interaction density or ambiguity justifies it

## Weather and chaos framing

Weather and chaos thinking is useful here as a diagnostic analogy, not as current runtime math.

Useful lessons:
- not every valid signal should be resolved at the finest grain at once
- nested resolution is often better than uniform maximal decomposition
- complexity must be controlled with explicit stop rules
- we should preserve the real observation while focusing on the strongest currents

This should remain a north-star lens for complexity control and field diagnostics until the project earns more formal math later.

## Ancestor systems

Two older systems matter as conceptual ancestors.

### `TripartiteDataSTORE`

What it got right:
- preserve multiple kinds of truth
- do not collapse storage into one representation
- keep raw/verbatim, meaning-like structure, and graph-like structure distinct

Why it matters now:
- it is a storage-doctrine ancestor, not the architecture to revert to

### `_NodeWALKER`

What it got right:
- the current node matters
- local traversal matters
- bounded neighborhood interpretation matters
- the user does not need the whole manifold; they need a navigable local region

Why it matters now:
- it is a traversal-doctrine ancestor, not a direct runtime dependency

## Current truth boundary

What this note is claiming:
- the project now has a clearer future bag/walker doctrine
- later retrieval should likely be scope-rooted and slice-based
- two-sided anchoring is a useful way to explain the bag

What this note is **not** claiming:
- that the current runtime bag already behaves this way
- that scope-root traversal is already implemented
- that weather/chaos math is active in the current nucleus
- that this replaces the live Phase 1 bottleneck work

## Practical implication for the next path

Immediate work is still:
- structural-loser versus grammatical-winner conversion analysis
- scorer-side promotion of structurally plausible cross-document bridges

Later retrieval work should probably define and implement:
- scope root
- resolution grammar
- direction of spread
- stop-unwinding logic
- bounded bag slice behavior

This note exists to preserve that direction without letting it outrun the code.
