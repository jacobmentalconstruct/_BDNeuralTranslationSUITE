# Baseline-Leg Sidecar Conclusion

## What This Branch Proved

- Real-English footing mattered.
  - `_corpus_examples/tech_talks` produced a much more useful baseline than the dictionary footing.
- The retrieval legs expose genuinely different behavior:
  - `fts` is often the cleanest leg for explicit phrase queries
  - sentence-transformers ANN behaves most like a conventional semantic prose baseline
  - deterministic ANN can be provisioned on the same corpus, but on this footing it remained weaker as a standalone prose retriever
  - the `bag` remains the strongest shaped evidence shelf
- Shared-view workflow is a real design gain.
  - human-driven shared-state viewing is proven useful
  - the separate sidecar viewer is the right first landing surface

## What This Branch Did Not Finish

- Agent-driven pending-action execution through the viewer is not yet reliable.
- This branch should not be used to continue broad workflow/UI experimentation.
- This branch should not absorb storage/compression, corpus-platform, or Phase 2 complexity.

## Mainline Takeaways

- Promote shared registry / shared visible state doctrine.
- Promote a minimal separate shared viewer sidecar.
- Keep lexical retrieval as a preserved baseline/control leg.
- Shift corpus doctrine toward:
  - general English first
  - then technical/project prose
  - then code/doc bridge corpora

## Branch Disposition

This branch is now a concluded diagnostic/reference seam.

Keep:
- docs
- artifacts
- comparison tools
- viewer as reference implementation

Do not treat it as:
- a second product line
- the place to continue expanding workflow complexity
- the place to solve upcoming storage/compression architecture
