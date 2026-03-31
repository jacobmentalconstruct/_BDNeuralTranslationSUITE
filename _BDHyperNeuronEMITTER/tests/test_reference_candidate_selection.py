import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


EMITTER_SRC = Path(__file__).resolve().parents[1] / "src"
if str(EMITTER_SRC) not in sys.path:
    sys.path.insert(0, str(EMITTER_SRC))

from core.assembler.core import GraphAssembler
from core.contract.hyperhunk import HyperHunk


class RecordingNucleus:
    def __init__(self) -> None:
        self.pairs: list[tuple[str, str]] = []

    def evaluate(self, a, b):
        self.pairs.append((a.occurrence_id, b.occurrence_id))
        return SimpleNamespace(
            connection_strength=0.0,
            positive_support=0.0,
            anti_signal_total=0.0,
            anti_signal_reasons=[],
            blocked=False,
            routing_profile={
                "grammatical": 0.0,
                "structural": 0.0,
                "statistical": 0.0,
                "semantic": 0.0,
                "verbatim": 0.0,
            },
            interaction_type="multi_surface",
            interaction_vector=[0.0, 0.0, 0.0, 0.0, 0.0],
            above_threshold=False,
        )


class BlockingNucleus:
    def evaluate(self, a, b):
        return SimpleNamespace(
            connection_strength=0.0,
            positive_support=0.42,
            anti_signal_total=0.42,
            anti_signal_reasons=["mutually_exclusive_refs"],
            blocked=True,
            routing_profile={
                "grammatical": 0.6,
                "structural": 0.2,
                "statistical": 0.1,
                "semantic": 0.0,
                "verbatim": 0.1,
            },
            interaction_type="grammatical_dominant",
            interaction_vector=[0.6, 0.2, 0.1, 0.0, 0.1],
            above_threshold=False,
        )


def _make_hunk(
    *,
    content: str,
    origin_id: str,
    node_kind: str,
    structural_path: str,
    heading_trail=None,
    normalized_cross_refs=None,
):
    return HyperHunk(
        content=content,
        origin_id=origin_id,
        layer_type="CST",
        node_kind=node_kind,
        structural_path=structural_path,
        heading_trail=list(heading_trail or []),
        normalized_cross_refs=list(normalized_cross_refs or []),
        token_count=max(1, len(content.split())),
    )


class ReferenceCandidateSelectionTests(unittest.TestCase):
    def test_reference_candidates_can_reach_beyond_sliding_window(self):
        index_item = _make_hunk(
            content="* 2. Lexical analysis",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_4",
            normalized_cross_refs=["lexical_analysis"],
        )
        filler_one = _make_hunk(
            content="filler one",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        target = _make_hunk(
            content="2. Lexical analysis",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_heading",
            structural_path="doc/h1_lexical_analysis",
            heading_trail=["Lexical analysis"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"

            baseline_nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                baseline_nucleus,
                window_size=2,
                reference_candidate_limit=0,
            ) as assembler:
                for hunk in [index_item, filler_one, filler_two, target]:
                    assembler.ingest_one(hunk)

            baseline_pairs = set(baseline_nucleus.pairs)
            self.assertNotIn((index_item.occurrence_id, target.occurrence_id), baseline_pairs)

            indexed_nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                indexed_nucleus,
                window_size=2,
                reference_candidate_limit=8,
            ) as assembler:
                for hunk in [index_item, filler_one, filler_two, target]:
                    assembler.ingest_one(hunk)

            indexed_pairs = set(indexed_nucleus.pairs)
            self.assertIn((index_item.occurrence_id, target.occurrence_id), indexed_pairs)

    def test_anchor_registry_prefers_heading_anchor_over_weaker_reference_match(self):
        weaker_candidate = _make_hunk(
            content="* lexical analysis",
            origin_id="memory://index_b.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_8",
            normalized_cross_refs=["lexical_analysis"],
        )
        filler_one = _make_hunk(
            content="filler one",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        stronger_candidate = _make_hunk(
            content="2. Lexical analysis",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_heading",
            structural_path="doc/h1_lexical_analysis",
            heading_trail=["Lexical analysis"],
        )
        incoming_index = _make_hunk(
            content="* 2. Lexical analysis",
            origin_id="memory://index_a.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_4",
            normalized_cross_refs=["lexical_analysis"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=2,
                reference_candidate_limit=1,
            ) as assembler:
                for hunk in [stronger_candidate, weaker_candidate, filler_one, filler_two, incoming_index]:
                    assembler.ingest_one(hunk)

            pairs = set(nucleus.pairs)
            self.assertIn((stronger_candidate.occurrence_id, incoming_index.occurrence_id), pairs)
            self.assertNotIn((weaker_candidate.occurrence_id, incoming_index.occurrence_id), pairs)

    def test_common_anchor_terms_are_suppressed_after_threshold(self):
        common_a = _make_hunk(
            content="Common",
            origin_id="memory://common_a.txt",
            node_kind="md_heading",
            structural_path="doc/h1_common_a",
            heading_trail=["Common"],
        )
        common_b = _make_hunk(
            content="Common",
            origin_id="memory://common_b.txt",
            node_kind="md_heading",
            structural_path="doc/h1_common_b",
            heading_trail=["Common"],
        )
        filler_one = _make_hunk(
            content="filler one",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        incoming_index = _make_hunk(
            content="* Common",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_4",
            normalized_cross_refs=["common"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=2,
                reference_candidate_limit=8,
                anchor_common_term_threshold=1,
            ) as assembler:
                for hunk in [common_a, common_b, filler_one, filler_two, incoming_index]:
                    assembler.ingest_one(hunk)

            pairs = set(nucleus.pairs)
            self.assertNotIn((common_a.occurrence_id, incoming_index.occurrence_id), pairs)
            self.assertNotIn((common_b.occurrence_id, incoming_index.occurrence_id), pairs)


class FTSFallbackTests(unittest.TestCase):
    """Tests for the ingest-time FTS cheap-fetch fallback in GraphAssembler."""

    def test_fts_fallback_recovers_long_range_candidate_when_anchor_thin(self):
        """FTS fallback should find a cross-document hunk via content match
        when the anchor registry cannot reach it and the sliding window
        has already evicted it."""
        # A distant heading hunk about "Lexical analysis"
        distant_heading = _make_hunk(
            content="2. Lexical analysis describes how tokens are formed.",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_heading",
            structural_path="doc/h1_lexical_analysis",
            heading_trail=["Lexical analysis"],
        )
        # Filler that pushes distant_heading out of the window
        filler_one = _make_hunk(
            content="filler one unrelated",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two unrelated",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        # An index item referencing lexical_analysis — no heading anchor
        # to match on, so anchor registry alone won't reach distant_heading
        index_item = _make_hunk(
            content="* 2. Lexical analysis",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_4",
            normalized_cross_refs=["lexical_analysis"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"

            # Baseline: no FTS, no anchor — pair should NOT appear
            baseline_nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                baseline_nucleus,
                window_size=2,
                reference_candidate_limit=0,
                fts_candidate_limit=0,
            ) as assembler:
                for hunk in [distant_heading, filler_one, filler_two, index_item]:
                    assembler.ingest_one(hunk)

            baseline_pairs = set(baseline_nucleus.pairs)
            self.assertNotIn(
                (distant_heading.occurrence_id, index_item.occurrence_id),
                baseline_pairs,
                "Baseline should NOT reach the distant heading without FTS or anchors",
            )

            # With FTS fallback enabled
            fts_nucleus = RecordingNucleus()
            db_path_fts = Path(tmp) / "cold_fts.db"
            with GraphAssembler(
                db_path_fts,
                fts_nucleus,
                window_size=2,
                reference_candidate_limit=8,
                fts_candidate_limit=8,
                fts_fallback_thin_threshold=2,
            ) as assembler:
                for hunk in [distant_heading, filler_one, filler_two, index_item]:
                    assembler.ingest_one(hunk)

            fts_pairs = set(fts_nucleus.pairs)
            self.assertIn(
                (distant_heading.occurrence_id, index_item.occurrence_id),
                fts_pairs,
                "FTS fallback should recover the distant heading as a candidate",
            )

    def test_fts_fallback_does_not_duplicate_window_or_anchor_candidates(self):
        """FTS should not re-add candidates already in the sliding window
        or already selected by the anchor registry."""
        heading_a = _make_hunk(
            content="Lexical analysis overview paragraph",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_heading",
            structural_path="doc/h1_lexical_analysis",
            heading_trail=["Lexical analysis"],
        )
        # This hunk will be in the sliding window
        window_hunk = _make_hunk(
            content="Lexical analysis is the first phase of compilation.",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_lexical_analysis/p1",
        )
        index_item = _make_hunk(
            content="* Lexical analysis",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            normalized_cross_refs=["lexical_analysis"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=10,  # Large enough that everything stays in window
                reference_candidate_limit=8,
                fts_candidate_limit=8,
                fts_fallback_thin_threshold=99,  # Always fire FTS
            ) as assembler:
                for hunk in [heading_a, window_hunk, index_item]:
                    assembler.ingest_one(hunk)

            # Count how many times each pair appears
            pair_counts = {}
            for pair in nucleus.pairs:
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

            # No pair should appear more than once
            for pair, count in pair_counts.items():
                self.assertEqual(
                    count, 1,
                    f"Pair {pair} appeared {count} times — FTS should not duplicate",
                )

    def test_fts_fallback_stays_off_when_limit_is_zero(self):
        """When fts_candidate_limit=0, FTS fallback should never fire."""
        distant = _make_hunk(
            content="Execution model describes how programs run.",
            origin_id="memory://execution_model.txt",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )
        filler = _make_hunk(
            content="filler",
            origin_id="memory://filler.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        index_item = _make_hunk(
            content="* Execution model",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            normalized_cross_refs=["execution_model"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=1,
                reference_candidate_limit=0,
                fts_candidate_limit=0,  # Explicitly disabled
            ) as assembler:
                for hunk in [distant, filler, index_item]:
                    assembler.ingest_one(hunk)
                stats = assembler.stats()

            self.assertEqual(stats["fts_fallback_fires"], 0)
            pairs = set(nucleus.pairs)
            self.assertNotIn(
                (distant.occurrence_id, index_item.occurrence_id),
                pairs,
            )

    def test_fts_fallback_prefers_cross_document_hits(self):
        """When both same-origin and cross-document FTS hits exist,
        cross-document should fill the budget first."""
        # Same-origin hunk — has matching content
        same_origin = _make_hunk(
            content="Data model structures and storage mechanisms",
            origin_id="memory://index.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_data/p1",
        )
        # Cross-document hunk — also has matching content
        cross_doc = _make_hunk(
            content="Data model defines how objects are represented in memory.",
            origin_id="memory://data_model.txt",
            node_kind="md_heading",
            structural_path="doc/h1_data_model",
            heading_trail=["Data model"],
        )
        # Filler to push both out of window
        filler_one = _make_hunk(
            content="filler one unrelated material",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two unrelated material",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        # The incoming hunk that triggers FTS
        query_hunk = _make_hunk(
            content="* Data model",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_5",
            normalized_cross_refs=["data_model"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=2,
                reference_candidate_limit=8,
                fts_candidate_limit=1,  # Budget = 1, forces preference
                fts_fallback_thin_threshold=99,  # Always fire
            ) as assembler:
                for hunk in [same_origin, cross_doc, filler_one, filler_two, query_hunk]:
                    assembler.ingest_one(hunk)

            pairs = set(nucleus.pairs)
            # Cross-doc hit should be selected
            self.assertIn(
                (cross_doc.occurrence_id, query_hunk.occurrence_id),
                pairs,
                "FTS should prefer the cross-document hit",
            )

    def test_fts_fallback_caps_single_origin_contribution(self):
        """FTS fallback should not let one origin monopolize the fallback budget."""
        same_origin_a = _make_hunk(
            content="Execution model overview and runtime behavior",
            origin_id="memory://index.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_reference/p1",
        )
        same_origin_b = _make_hunk(
            content="Execution model details and frame evaluation",
            origin_id="memory://index.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_reference/p2",
        )
        cross_doc = _make_hunk(
            content="Execution model explains frames and code blocks.",
            origin_id="memory://executionmodel.txt",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )
        filler_one = _make_hunk(
            content="filler one unrelated material",
            origin_id="memory://filler1.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p1",
        )
        filler_two = _make_hunk(
            content="filler two unrelated material",
            origin_id="memory://filler2.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_misc/p2",
        )
        query_hunk = _make_hunk(
            content="* Execution model",
            origin_id="memory://query.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_5",
            normalized_cross_refs=["execution_model"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            nucleus = RecordingNucleus()
            with GraphAssembler(
                db_path,
                nucleus,
                window_size=2,
                reference_candidate_limit=0,
                fts_candidate_limit=2,
                fts_fallback_thin_threshold=99,
                fts_origin_cap=1,
            ) as assembler:
                for hunk in [same_origin_a, same_origin_b, cross_doc, filler_one, filler_two, query_hunk]:
                    assembler.ingest_one(hunk)
                stats = assembler.stats()

            pairs = set(nucleus.pairs)
            self.assertIn((cross_doc.occurrence_id, query_hunk.occurrence_id), pairs)
            same_origin_pairs = {
                (same_origin_a.occurrence_id, query_hunk.occurrence_id),
                (same_origin_b.occurrence_id, query_hunk.occurrence_id),
            }
            self.assertEqual(len(pairs & same_origin_pairs), 1)
            self.assertGreater(stats["fts_origin_cap_skips"], 0)


class ContradictionExportTests(unittest.TestCase):
    def test_blocked_pair_is_not_written_but_is_exported_with_penalty_fields(self):
        a = _make_hunk(
            content="* Lexical analysis",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            normalized_cross_refs=["lexical_analysis"],
        )
        b = _make_hunk(
            content="* Execution model",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_2",
            normalized_cross_refs=["execution_model"],
        )

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            with GraphAssembler(
                db_path,
                BlockingNucleus(),
                window_size=10,
            ) as assembler:
                assembler.ingest_one(a)
                assembler.ingest_one(b)
                stats = assembler.stats()
                training_pairs = assembler.export_training_pairs()

            self.assertEqual(stats["relations"], 0)
            self.assertEqual(stats["contradiction_penalty_pairs"], 1)
            self.assertEqual(stats["contradiction_blocked_pairs"], 1)
            self.assertEqual(len(training_pairs), 1)
            pair = training_pairs[0]
            self.assertEqual(pair["positive_support"], 0.42)
            self.assertEqual(pair["anti_signal_total"], 0.42)
            self.assertEqual(pair["anti_signal_reasons"], ["mutually_exclusive_refs"])
            self.assertTrue(pair["blocked"])
            self.assertFalse(pair["above_threshold"])


if __name__ == "__main__":
    unittest.main()
