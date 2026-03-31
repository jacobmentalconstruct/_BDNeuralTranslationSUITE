# NL Narrative Description

_Reference note: keep for orientation, but do not treat this as the primary active truth surface._

For current architecture and next-step truth, prefer:
- `_docs/ARCHITECTURE.md`
- `_docs/WE_ARE_HERE_NOW.md`
- `_docs/TODO.md`

_Last updated: 2026-03-27. This is a plain-language orientation note for reviewers who need the idea of the system before they inspect the code._

## What this project is

BDNeuralTranslationSUITE is a memory-oriented system for agents.

Its purpose is not to generate final answers by itself. Its purpose is to preserve context as inspectable units, connect those units in a graph, and make it possible for an agent to re-examine prior material instead of losing it when the active context window moves on.

The project is trying to replace a weak pattern:
- short-term context falls out of the sliding window
- the system either drops it or compresses it into a lossy summary

with a stronger pattern:
- context is converted into durable multi-surface units
- those units are connected into a graph with recorded reasons for connection
- later retrieval can bring back evidence and structure, not just a flattened recap

## The basic model

The system treats each memory unit as a small structured object with multiple surfaces.

Right now the active surfaces are:
- `verbatim`: the literal content
- `structural`: where it sits in a document or code hierarchy
- `grammatical`: what kind of thing it is
- `statistical`: token and overlap behavior
- `semantic`: intended future meaning/vector layer

The important idea is that the unit is not defined by only one of these surfaces. It is a combination of them.

## How the current pipeline works

The project is split into two main apps.

### Splitter

The Splitter reads source material and emits NDJSON HyperHunks.

Its job is to populate surfaces. It does not decide graph meaning.

In practical terms, it is the stage that turns raw text, prose, and code into durable units that carry structure and context forward.

### Emitter

The Emitter consumes those HyperHunks and writes the Cold Artifact graph.

Its job is to decide how units relate. It compares pairs of units, computes a connection strength, and stores not only the relation but also the routing profile that explains which surfaces mattered.

This is the beginning of a graph that can later support evidence retrieval instead of mere storage.

## What the bootstrap nucleus is

The current nucleus is a fixed-weight scaffold, not the final learned model.

It exists for practical reasons:
- it gives the system a working relational rule set now
- it lets the graph come alive before the FFN exists
- it generates training data for the later learned scorer
- it exposes where the current relation math is too coarse

At the moment, it is best understood as a temporary interaction law.

It is not the final intelligence of the system. It is the current scoring scaffold that lets the rest of the memory architecture be tested and tuned.

## What is working now

The system is already beyond concept-only status.

What is working in a real sense:
- the Splitter produces multi-surface units
- the Emitter builds a live graph from them
- probe runs can measure how the graph changes as scoring changes
- the bootstrap scorer is now tunable through explicit builder-facing dials
- the project can compare probe outputs mechanically instead of relying on intuition alone

This means the project is in a prototype-tuning phase, not an idea-discovery phase.

## What the project is not claiming yet

The project is not claiming that agent memory is solved.

It is not yet:
- a finished retrieval layer
- a finished bag/STM membrane
- a finished learned nucleus
- a production-ready long-context substitute

The current claim is narrower and more defensible:

the architecture is viable, the graph is real, the memory units are real, and the interaction scaffold is now tunable enough to continue refining the prototype deliberately.

## Why this matters

Many systems treat falling context as disposable and rely on summarization as the main preservation mechanism.

This project is exploring a different approach:
- preserve context as durable units
- preserve multiple surfaces of that context
- preserve why units relate
- allow later systems to revisit evidence instead of trusting a single compressed summary

That is the practical motivation behind the current codebase.

## Current direction

The current development focus is still on the substrate, not the final bag layer.

The immediate work is:
- improve the quality of the bootstrap scaffold
- improve graph behavior on real corpora
- increase useful cross-document relations without returning to coarse over-connection
- accumulate trustworthy training data for the eventual FFN nucleus

The bag remains a later layer that will sit between an agent's short-term memory falloff and this durable graph-backed memory substrate.

## Reviewer guidance

If you are reviewing this project in audio, video, or written form, the safest framing is:

BDNeuralTranslationSUITE is an attempt to build a durable, inspectable relational memory substrate for agents. It currently consists of a multi-surface unit builder, a graph emitter, and a tunable scaffold scorer that records not only that units connect, but why they connect.

That framing is closer to the present code than more ambitious or more dismissive descriptions would be.
