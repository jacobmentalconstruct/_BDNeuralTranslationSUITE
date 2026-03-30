# Splitter Corpus Baselines

_Last updated: 2026-03-27. This file records corpus hardening observations and baseline metrics for the Splitter._

---

## Purpose

This is the running record for Tranche 10: Splitter corpus hardening.

Use it to capture:
- routing decisions by corpus
- surface-quality observations
- before/after metrics when Splitter behavior changes
- remaining weak spots that still need hardening

---

## Baseline 001 — Webster + Python Reference

**Date:** 2026-03-27

### Corpus A — Webster dictionary

Path:
- `_corpus_examples/webstersdictinoary.txt`

Goal:
- validate the fallback prose floor

Observed routing:
- `FallbackEngine` only

Sample metrics:

| Metric | Value |
|---|---|
| sample size | 250 hunks |
| node kinds | `paragraph=246`, `fragment_of_paragraph=4` |
| layer types | `REGEX=246`, `CHAR=4` |
| extraction engines | `FallbackEngine=250` |
| mean token count | `29.36` |
| median token count | `16` |
| context window non-empty | `249 / 250` |
| heading trail non-empty | `0 / 250` |
| cross refs non-empty | `0 / 250` |
| document position range | `0.0` → `0.0011` |

Notes:
- This is the correct routing for the corpus.
- The fallback path now stamps `extraction_engine="FallbackEngine"` instead of leaving provenance blank.
- Structural richness is intentionally thin here; this corpus is the prose-floor baseline, not the structured-doc target.

### Corpus B — Python reference docs

Primary inspection paths:
- `_corpus_examples/python-3.11.15-docs-text/reference`
- `_corpus_examples/python-3.11.15-docs-text/reference/lexical_analysis.txt`

Goal:
- ensure structured technical prose does not collapse to plain fallback paragraphs

Observed routing after fix:
- most `reference/*.txt` files now route as `PEGEngine` + `FallbackEngine`
- former holdouts `grammar.txt` and `index.txt` now also route as `PEGEngine` + `FallbackEngine`

`lexical_analysis.txt` sample metrics:

| Metric | Value |
|---|---|
| sample size | 106 hunks |
| node kinds | `md_heading=20`, `md_paragraph=68`, `md_list=1`, `fragment_of_md_code_block=17` |
| layer types | `CST=89`, `CHAR=17` |
| extraction engines | `PEGEngine=106` |
| heading trail non-empty | `106 / 106` |
| cross refs non-empty | `1 / 106` |

Key behavioral change:
- structured `.txt` documents with reStructuredText-style underlined headings are now claimed by PEG instead of falling straight to Fallback

Notes:
- The first title in `lexical_analysis.txt` now emits as:
  - `node_kind = md_heading`
  - `structural_path = doc/h1_2_lexical_analysis`
  - `heading_trail = ["2. Lexical analysis"]`
- This is a real improvement over the previous all-fallback paragraph path.
- `md_list=1` still appears in the sample, which suggests there may be one remaining ambiguous construct in the PEG path worth inspecting later.

Additional routing fix:
- `grammar.txt` now emits a real top-level heading plus token-budgeted `md_code_block` fragments for the large indented grammar block instead of hallucinating headings inside the literal block.
- `index.txt` now routes through PEG, but its long table-of-contents list still collapses into `fragment_of_md_list` chunks because the list is larger than the token budget.

---

## Changes Made For Baseline 001

- `FallbackEngine` now stamps:
  - `extraction_engine="FallbackEngine"`
  - `extraction_confidence=0.6`
- `PEGEngine` now:
  - handles `.rst`
  - can claim structured `.txt` when the content looks like heading-driven prose
  - recognizes underlined heading styles used in the Python reference docs
  - emits heading content from heading title text rather than raw underline blocks
  - treats indented literal blocks as code-style blocks instead of misreading indented `# ...` lines as headings
- `info` routing now reads file content so structured `.txt` detection shows up correctly in CLI inspection output

---

## Remaining Weak Spots

- `index.txt` still degrades into large `fragment_of_md_list` chunks rather than a more inspectable section/index representation
- one `md_list` artifact still appears in `lexical_analysis.txt`
- Webster fallback behavior has correct provenance now, but it still needs a closer qualitative pass on paragraph quality and fragmentation behavior deeper into the file

---

## Next Actions

1. Inspect the lone `md_list` artifact in `lexical_analysis.txt`.
2. Decide whether `index.txt` needs a richer index/list representation beyond token-budgeted list fragments.
3. Run a broader representative stream from the Python reference folder into the Emitter and inspect graph/training-pair quality.
