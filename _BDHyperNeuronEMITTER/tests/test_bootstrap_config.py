import sys
import unittest
from pathlib import Path


EMITTER_SRC = Path(__file__).resolve().parents[1] / "src"
if str(EMITTER_SRC) not in sys.path:
    sys.path.insert(0, str(EMITTER_SRC))

from core.contract.hyperhunk import HyperHunk
from core.nucleus.bootstrap import BootstrapConfig, BootstrapNucleus


def _make_hunk(
    *,
    content: str,
    node_kind: str,
    structural_path: str,
    heading_trail=None,
    token_count: int = 20,
    embedding=None,
    origin_id: str = "memory://test",
    cross_refs=None,
    normalized_cross_refs=None,
    import_context=None,
):
    hunk = HyperHunk(
        content=content,
        origin_id=origin_id,
        layer_type="CST",
        node_kind=node_kind,
        structural_path=structural_path,
        heading_trail=list(heading_trail or []),
        cross_refs=list(cross_refs or []),
        normalized_cross_refs=list(normalized_cross_refs or []),
        import_context=list(import_context or []),
        token_count=token_count,
    )
    hunk.embedding = embedding
    return hunk


class BootstrapConfigTests(unittest.TestCase):
    def test_default_config_round_trip(self):
        config = BootstrapConfig.default()
        clone = BootstrapConfig.from_dict(config.to_dict())
        self.assertEqual(config.to_dict(), clone.to_dict())

    def test_missing_required_keys_rejected(self):
        payload = BootstrapConfig.default().to_dict()
        del payload["surface_fractions"]
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_old_payload_without_cross_document_profile_still_loads(self):
        payload = BootstrapConfig.default().to_dict()
        del payload["cross_document_profile"]

        config = BootstrapConfig.from_dict(payload)

        self.assertFalse(config.cross_document_profile.enabled)
        self.assertIn("cross_document_profile", config.to_dict())

    def test_negative_values_rejected(self):
        payload = BootstrapConfig.default().to_dict()
        payload["edge_threshold"] = -0.1
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_invalid_threshold_scale_rejected(self):
        payload = BootstrapConfig.default().to_dict()
        payload["semantic_absent_threshold_scale"] = 0.0
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_invalid_explicit_reference_profile_rejected(self):
        payload = BootstrapConfig.default().to_dict()
        payload["explicit_reference_profile"]["target_hint_bonus"] = -0.1
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_invalid_contradiction_profile_rejected(self):
        payload = BootstrapConfig.default().to_dict()
        payload["contradiction_profile"]["reference_miss_penalty"] = -0.1
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_surface_fractions_must_sum_to_one(self):
        payload = BootstrapConfig.default().to_dict()
        payload["surface_fractions"]["grammatical"] = 0.99
        with self.assertRaises(ValueError):
            BootstrapConfig.from_dict(payload)

    def test_default_config_preserves_current_behavior_after_reload(self):
        a = _make_hunk(
            content="Paragraph about imports and modules.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p1",
            heading_trail=["Intro"],
            token_count=24,
        )
        b = _make_hunk(
            content="Another paragraph about modules and imports.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p2",
            heading_trail=["Intro"],
            token_count=26,
        )
        default_nucleus = BootstrapNucleus()
        round_trip_nucleus = BootstrapNucleus(
            config=BootstrapConfig.from_dict(BootstrapConfig.default().to_dict())
        )
        self.assertEqual(
            default_nucleus.evaluate(a, b).__dict__,
            round_trip_nucleus.evaluate(a, b).__dict__,
        )


class BootstrapBehaviorTests(unittest.TestCase):
    def test_disabled_cross_document_profile_preserves_current_behavior(self):
        default_nucleus = BootstrapNucleus()
        disabled_nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": False,
                    "edge_threshold_scale": 0.5,
                    "surface_fractions": {
                        "grammatical": 0.0,
                        "structural": 1.0,
                        "statistical": 0.0,
                        "semantic": 0.0,
                        "verbatim": 0.0,
                    },
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.4,
                        "target_hint_bonus": 0.4,
                        "import_context_overlap_weight": 0.4,
                    },
                }
            })
        )
        a = _make_hunk(
            content="Splitter notes about imports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/splitter.txt",
            structural_path="doc/h1_splitter/p1",
            heading_trail=["Splitter"],
            cross_refs=["hyperhunk.py"],
        )
        b = _make_hunk(
            content="Emitter notes about imports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/emitter.txt",
            structural_path="doc/h1_emitter/p1",
            heading_trail=["Emitter"],
            cross_refs=["hyperhunk.py"],
        )

        self.assertEqual(
            default_nucleus.evaluate(a, b).__dict__,
            disabled_nucleus.evaluate(a, b).__dict__,
        )

    def test_same_document_pair_ignores_cross_document_branch(self):
        default_nucleus = BootstrapNucleus()
        tuned_nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "edge_threshold_scale": 0.5,
                    "surface_fractions": {
                        "grammatical": 0.0,
                        "structural": 1.0,
                        "statistical": 0.0,
                        "semantic": 0.0,
                        "verbatim": 0.0,
                    },
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.4,
                        "target_hint_bonus": 0.4,
                        "import_context_overlap_weight": 0.4,
                    },
                }
            })
        )
        a = _make_hunk(
            content="Intro paragraph about modules and imports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/reference/import.txt",
            structural_path="doc/h1_import/p1",
            heading_trail=["Import System"],
            cross_refs=["import.txt"],
        )
        b = _make_hunk(
            content="Another paragraph about modules and imports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/reference/import.txt",
            structural_path="doc/h1_import/p2",
            heading_trail=["Import System"],
            cross_refs=["import.txt"],
        )

        self.assertEqual(
            default_nucleus.evaluate(a, b).__dict__,
            tuned_nucleus.evaluate(a, b).__dict__,
        )

    def test_code_exact_match_beats_generic_prose_exact_match(self):
        nucleus = BootstrapNucleus()

        code_a = _make_hunk(
            content="def add(x, y): return x + y",
            node_kind="function_definition",
            structural_path="module/add",
        )
        code_b = _make_hunk(
            content="def sub(x, y): return x - y",
            node_kind="function_definition",
            structural_path="module/sub",
        )
        prose_a = _make_hunk(
            content="This paragraph explains the module.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p1",
            heading_trail=["Intro"],
        )
        prose_b = _make_hunk(
            content="This paragraph also explains the module.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p2",
            heading_trail=["Intro"],
        )

        code_score = nucleus.evaluate(code_a, code_b).interaction_vector[0]
        prose_score = nucleus.evaluate(prose_a, prose_b).interaction_vector[0]
        self.assertGreater(code_score, prose_score)

    def test_heading_exact_match_beats_generic_paragraph_exact_match(self):
        nucleus = BootstrapNucleus()
        heading_a = _make_hunk(
            content="4. Execution model",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )
        heading_b = _make_hunk(
            content="6. Expressions",
            node_kind="md_heading",
            structural_path="doc/h1_expressions",
            heading_trail=["Expressions"],
        )
        paragraph_a = _make_hunk(
            content="Paragraph one",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p1",
            heading_trail=["Intro"],
        )
        paragraph_b = _make_hunk(
            content="Paragraph two",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p2",
            heading_trail=["Intro"],
        )

        heading_score = nucleus.evaluate(heading_a, heading_b).interaction_vector[0]
        paragraph_score = nucleus.evaluate(paragraph_a, paragraph_b).interaction_vector[0]
        self.assertGreater(heading_score, paragraph_score)

    def test_fragment_similarity_stays_weak(self):
        nucleus = BootstrapNucleus()
        frag_a = _make_hunk(
            content="fragment alpha",
            node_kind="fragment_of_md_paragraph",
            structural_path="doc/h1_intro/frag1",
            token_count=8,
        )
        frag_b = _make_hunk(
            content="fragment beta",
            node_kind="fragment_of_md_paragraph",
            structural_path="doc/h1_intro/frag2",
            token_count=8,
        )

        frag_score = nucleus.evaluate(frag_a, frag_b).interaction_vector[0]
        self.assertLessEqual(frag_score, 0.12)

    def test_semantic_absent_threshold_scale_changes_only_threshold_decision(self):
        base = BootstrapConfig.default().with_overrides({
            "edge_threshold": 0.34,
            "semantic_absent_threshold_scale": 0.8,
        })
        scaled_nucleus = BootstrapNucleus(config=base)
        default_nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({"edge_threshold": 0.34})
        )

        a = _make_hunk(
            content="Paragraph about imports.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p1",
            heading_trail=["Intro"],
            token_count=20,
        )
        b = _make_hunk(
            content="Paragraph about modules.",
            node_kind="md_paragraph",
            structural_path="doc/h1_intro/p2",
            heading_trail=["Intro"],
            token_count=22,
        )

        default_result = default_nucleus.evaluate(a, b)
        scaled_result = scaled_nucleus.evaluate(a, b)

        self.assertEqual(default_result.connection_strength, scaled_result.connection_strength)
        self.assertEqual(default_result.routing_profile, scaled_result.routing_profile)
        self.assertEqual(default_result.interaction_type, scaled_result.interaction_type)
        self.assertEqual(default_result.interaction_vector, scaled_result.interaction_vector)
        self.assertNotEqual(default_result.above_threshold, scaled_result.above_threshold)

    def test_cross_document_pair_uses_alternate_threshold_and_surface_fractions(self):
        default_nucleus = BootstrapNucleus()
        tuned_nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "edge_threshold_scale": 0.5,
                    "surface_fractions": {
                        "grammatical": 0.0,
                        "structural": 1.0,
                        "statistical": 0.0,
                        "semantic": 0.0,
                        "verbatim": 0.0,
                    },
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.0,
                        "target_hint_bonus": 0.0,
                        "import_context_overlap_weight": 0.0,
                    },
                }
            })
        )
        a = _make_hunk(
            content="Paragraph about module imports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/reference/import.txt",
            structural_path="doc/h1_shared/p1",
            heading_trail=["Shared"],
            token_count=20,
        )
        b = _make_hunk(
            content="Paragraph about module exports.",
            node_kind="md_paragraph",
            origin_id="C:/docs/reference/export.txt",
            structural_path="doc/h1_shared/p2",
            heading_trail=["Shared"],
            token_count=22,
        )

        default_result = default_nucleus.evaluate(a, b)
        tuned_result = tuned_nucleus.evaluate(a, b)

        self.assertLess(
            tuned_nucleus._effective_edge_threshold(a, b),
            default_nucleus._effective_edge_threshold(a, b),
        )
        self.assertEqual(tuned_result.routing_profile["structural"], 1.0)
        self.assertEqual(tuned_result.routing_profile["grammatical"], 0.0)
        self.assertGreater(
            tuned_result.routing_profile["structural"],
            default_result.routing_profile["structural"],
        )

    def test_explicit_cross_ref_boost_improves_structural_signal(self):
        baseline = BootstrapNucleus()
        tuned = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "explicit_reference_profile": {
                    "overlap_weight": 0.0,
                    "target_hint_bonus": 0.2,
                }
            })
        )

        a = _make_hunk(
            content="See the import system details.",
            node_kind="md_paragraph",
            origin_id="memory://import",
            structural_path="doc/h1_import/p1",
            heading_trail=["Import System"],
            cross_refs=["import.txt"],
        )
        b = _make_hunk(
            content="Import machinery reference.",
            node_kind="md_heading",
            origin_id="C:/docs/reference/import.txt",
            structural_path="doc/h1_import_system",
            heading_trail=["Import System"],
        )

        baseline_structural = baseline.evaluate(a, b).interaction_vector[1]
        tuned_structural = tuned.evaluate(a, b).interaction_vector[1]
        self.assertGreater(tuned_structural, baseline_structural)

    def test_cross_document_shared_anchor_signal_raises_structural_support(self):
        baseline = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.0,
                        "target_hint_bonus": 0.0,
                        "import_context_overlap_weight": 0.0,
                    },
                }
            })
        )
        tuned = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.18,
                        "target_hint_bonus": 0.12,
                        "import_context_overlap_weight": 0.15,
                    },
                }
            })
        )
        a = _make_hunk(
            content="Splitter references the HyperHunk contract.",
            node_kind="md_paragraph",
            origin_id="C:/docs/splitter.txt",
            structural_path="doc/h1_splitter/p1",
            heading_trail=["Splitter"],
            cross_refs=["hyperhunk.py"],
            normalized_cross_refs=["hyperhunk"],
            import_context=["core.contract.hyperhunk"],
        )
        b = _make_hunk(
            content="Emitter also references the HyperHunk contract.",
            node_kind="md_paragraph",
            origin_id="C:/docs/emitter.txt",
            structural_path="doc/h1_emitter/p1",
            heading_trail=["Emitter"],
            cross_refs=["hyperhunk.py"],
            normalized_cross_refs=["hyperhunk"],
            import_context=["core.contract.hyperhunk"],
        )

        baseline_structural = baseline.evaluate(a, b).interaction_vector[1]
        tuned_structural = tuned.evaluate(a, b).interaction_vector[1]
        self.assertGreater(tuned_structural, baseline_structural)

    def test_cross_document_pair_without_shared_anchor_signal_gets_no_bonus(self):
        baseline = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.0,
                        "target_hint_bonus": 0.0,
                        "import_context_overlap_weight": 0.0,
                    },
                }
            })
        )
        tuned = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "cross_document_profile": {
                    "enabled": True,
                    "shared_anchor_profile": {
                        "reference_overlap_weight": 0.18,
                        "target_hint_bonus": 0.12,
                        "import_context_overlap_weight": 0.15,
                    },
                }
            })
        )
        a = _make_hunk(
            content="Alpha anchor reference.",
            node_kind="md_paragraph",
            origin_id="C:/docs/alpha.txt",
            structural_path="doc/h1_alpha/p1",
            heading_trail=["Alpha"],
            cross_refs=["alpha_anchor"],
            normalized_cross_refs=["alpha_anchor"],
            import_context=["alpha.module"],
        )
        b = _make_hunk(
            content="Beta anchor reference.",
            node_kind="md_paragraph",
            origin_id="C:/docs/beta.txt",
            structural_path="doc/h1_beta/p1",
            heading_trail=["Beta"],
            cross_refs=["beta_anchor"],
            normalized_cross_refs=["beta_anchor"],
            import_context=["beta.module"],
        )

        baseline_structural = baseline.evaluate(a, b).interaction_vector[1]
        tuned_structural = tuned.evaluate(a, b).interaction_vector[1]
        self.assertEqual(tuned_structural, baseline_structural)

    def test_default_contradiction_profile_is_inert(self):
        nucleus = BootstrapNucleus()
        a = _make_hunk(
            content="See lexical analysis.",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            cross_refs=["lexical_analysis"],
        )
        b = _make_hunk(
            content="Execution model",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )

        result = nucleus.evaluate(a, b)
        self.assertEqual(result.anti_signal_total, 0.0)
        self.assertEqual(result.anti_signal_reasons, [])
        self.assertFalse(result.blocked)
        self.assertEqual(result.connection_strength, result.positive_support)

    def test_contradiction_penalty_down_ranks_explicit_reference_miss(self):
        baseline = BootstrapNucleus()
        tuned = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "contradiction_profile": {
                    "reference_miss_penalty": 0.2,
                    "block_mutually_exclusive_refs": False,
                }
            })
        )
        a = _make_hunk(
            content="See lexical analysis.",
            node_kind="md_paragraph",
            structural_path="doc/h1_reference/p_1",
            cross_refs=["lexical_analysis"],
        )
        b = _make_hunk(
            content="Execution model",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )

        baseline_result = baseline.evaluate(a, b)
        tuned_result = tuned.evaluate(a, b)

        self.assertGreater(baseline_result.connection_strength, tuned_result.connection_strength)
        self.assertGreater(tuned_result.anti_signal_total, 0.0)
        self.assertIn("a_ref_miss_b_target", tuned_result.anti_signal_reasons)
        self.assertFalse(tuned_result.blocked)

    def test_navigational_list_item_refs_do_not_emit_reference_miss_penalty(self):
        nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "contradiction_profile": {
                    "reference_miss_penalty": 0.2,
                    "block_mutually_exclusive_refs": False,
                }
            })
        )
        a = _make_hunk(
            content="See lexical analysis.",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            cross_refs=["lexical_analysis"],
        )
        b = _make_hunk(
            content="Execution model",
            node_kind="md_heading",
            structural_path="doc/h1_execution_model",
            heading_trail=["Execution model"],
        )

        result = nucleus.evaluate(a, b)
        self.assertEqual(result.anti_signal_total, 0.0)
        self.assertEqual(result.anti_signal_reasons, [])
        self.assertFalse(result.blocked)

    def test_contradiction_profile_can_block_mutually_exclusive_refs(self):
        nucleus = BootstrapNucleus(
            config=BootstrapConfig.default().with_overrides({
                "contradiction_profile": {
                    "reference_miss_penalty": 0.0,
                    "block_mutually_exclusive_refs": True,
                }
            })
        )
        a = _make_hunk(
            content="* Lexical analysis",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_1",
            cross_refs=["lexical_analysis"],
        )
        b = _make_hunk(
            content="* Execution model",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_2",
            cross_refs=["execution_model"],
        )

        result = nucleus.evaluate(a, b)
        self.assertTrue(result.blocked)
        self.assertFalse(result.above_threshold)
        self.assertIn("mutually_exclusive_refs", result.anti_signal_reasons)


if __name__ == "__main__":
    unittest.main()
