"""token_budget.py — BPE-aware token budget module.

CURRENT IMPLEMENTATION: character-estimate (phase 1 of 2).
Uses avg chars-per-token as a proxy for BPE token count.
Sufficient for Tranche 2. Replace count() and split_to_slices() with
real BPE tokenizer calls in Tranche 3+ when the trained vocab is available.

DESIGN INTENT
-------------
The Splitter's v1 Negotiator used:
    len(content) > max_size   (character count)

This is wrong because embedding windows are measured in tokens, not chars.
Dense Python code and verbose English prose have very different chars-per-token
ratios (2.5-3.5 vs 3.5-5.0), so character-count splits land at wrong places.

The v2 Negotiator uses this module's `fits()` and `split_to_slices()` instead.
When the full BPE tokenizer is available, swap the underlying count() method
and the rest of the API stays identical.

CHARS-PER-TOKEN CALIBRATION
----------------------------
Default 4.0 is a conservative midpoint. Caller can override:
  - Dense code (Python, JS): 3.0–3.5
  - English prose: 4.0–5.0
  - Mixed (docs with code blocks): 3.5–4.0

OVERLAP RATIO
-------------
The context_window is `overlap_ratio` fraction of the token budget carried
forward from the preceding hunk. Default 0.25 = last 25% of tokens.
"""

from __future__ import annotations

from typing import List


class TokenBudget:
    """Token-aware budget calculator and slicer.

    Parameters
    ----------
    max_tokens : int
        Maximum BPE tokens allowed per hunk.
    overlap_ratio : float
        Fraction of max_tokens to carry forward as context_window.
        e.g. 0.25 = last 25% of the budget's token count.
    chars_per_token : float
        Calibration constant for the char-estimate proxy.
        Override per file type for better accuracy.
    """

    def __init__(
        self,
        max_tokens: int = 256,
        overlap_ratio: float = 0.25,
        chars_per_token: float = 4.0,
    ) -> None:
        if max_tokens < 1:
            raise ValueError(f"max_tokens must be >= 1, got {max_tokens!r}")
        if not 0.0 <= overlap_ratio < 1.0:
            raise ValueError(f"overlap_ratio must be in [0.0, 1.0), got {overlap_ratio!r}")
        self.max_tokens = max_tokens
        self.overlap_ratio = overlap_ratio
        self._chars_per_token = chars_per_token
        # Derived char limits
        self._max_chars = max(1, round(max_tokens * chars_per_token))
        self._overlap_chars = max(0, round(max_tokens * overlap_ratio * chars_per_token))

    # ── Token counting ────────────────────────────────────────────────

    def count(self, text: str) -> int:
        """Estimate BPE token count for text.

        Phase 1: character-estimate proxy (len / chars_per_token).
        Phase 2: replace with real BPE tokenizer call.
        Returns at least 1 for any non-empty string.
        """
        if not text:
            return 0
        return max(1, round(len(text) / self._chars_per_token))

    # ── Budget checks ─────────────────────────────────────────────────

    def fits(self, text: str) -> bool:
        """Return True if text fits within the token budget."""
        return self.count(text) <= self.max_tokens

    def headroom(self, text: str) -> int:
        """Remaining token budget after text. Negative means over-budget."""
        return self.max_tokens - self.count(text)

    # ── Slicing ───────────────────────────────────────────────────────

    def split_to_slices(self, text: str) -> List[str]:
        """Split text into a list of budget-sized slices.

        Each slice is guaranteed to fit the token budget.
        Slices at character boundaries (phase 1). Phase 2 will split
        at actual BPE token boundaries.

        Returns a list with at least one element.
        """
        if not text:
            return [""]
        slices = [
            text[i: i + self._max_chars]
            for i in range(0, len(text), self._max_chars)
        ]
        return slices if slices else [text]

    # ── Context window ────────────────────────────────────────────────

    def context_window_tokens(self, prev_content: str) -> str:
        """Extract the trailing overlap from prev_content for context_window.

        Returns the last `overlap_ratio * max_tokens` tokens' worth of chars
        from prev_content. Returns empty string if no overlap is configured
        or if prev_content is empty.
        """
        if not prev_content or self._overlap_chars <= 0:
            return ""
        return prev_content[-self._overlap_chars:]
