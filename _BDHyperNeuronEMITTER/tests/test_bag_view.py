import io
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


EMITTER_SRC = Path(__file__).resolve().parents[1] / "src"
if str(EMITTER_SRC) not in sys.path:
    sys.path.insert(0, str(EMITTER_SRC))

import app as emitter_app
from core.assembler.core import GraphAssembler
from core.contract.hyperhunk import HyperHunk
from core.engine.inference.bag_view import build_bag


class AlwaysOnNucleus:
    def evaluate(self, a, b):
        return SimpleNamespace(
            connection_strength=0.5,
            routing_profile={
                "grammatical": 0.2,
                "structural": 0.5,
                "statistical": 0.2,
                "semantic": 0.0,
                "verbatim": 0.1,
            },
            interaction_type="structural_bridge",
            interaction_vector=[0.2, 0.5, 0.2, 0.0, 0.1],
            above_threshold=True,
        )


def _make_hunk(*, content: str, origin_id: str, node_kind: str, structural_path: str):
    return HyperHunk(
        content=content,
        origin_id=origin_id,
        layer_type="CST",
        node_kind=node_kind,
        structural_path=structural_path,
        token_count=max(1, len(content.split())),
    )


class BagViewTests(unittest.TestCase):
    def _build_fixture_db(self, db_path: Path) -> tuple[HyperHunk, HyperHunk]:
        list_item = _make_hunk(
            content="* 2. Lexical analysis",
            origin_id="memory://index.txt",
            node_kind="md_list_item",
            structural_path="doc/h1_reference/li_4",
        )
        heading = _make_hunk(
            content="2. Lexical analysis",
            origin_id="memory://lexical_analysis.txt",
            node_kind="md_heading",
            structural_path="doc/h1_2_lexical_analysis",
        )

        with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
            assembler.ingest_one(list_item)
            assembler.ingest_one(heading)

        return list_item, heading

    def test_build_bag_returns_grouped_pullback_ready_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            list_item, heading = self._build_fixture_db(db_path)

            bag = build_bag(
                query_text="lexical analysis",
                db_path=db_path,
                top_k=5,
                group_by="origin_id",
                pull_occurrence_ids=[heading.occurrence_id],
            )

        self.assertEqual(bag["query"], "lexical analysis")
        self.assertGreaterEqual(bag["bag_summary"]["item_count"], 2)
        self.assertEqual(bag["bag_summary"]["group_by"], "origin_id")
        self.assertGreaterEqual(bag["bag_summary"]["group_count"], 2)

        item_ids = {item["occurrence_id"] for item in bag["items"]}
        self.assertIn(list_item.occurrence_id, item_ids)
        self.assertIn(heading.occurrence_id, item_ids)

        pull_ids = bag["pullback"]["selected_occurrence_ids"]
        self.assertEqual(pull_ids, [heading.occurrence_id])
        self.assertIn("Lexical analysis", bag["pullback"]["items"][0]["pullback_text"])

        first_item = bag["items"][0]
        self.assertIn("item_summary", first_item)
        self.assertIn("why", first_item)

    def test_cmd_bag_emits_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            _, heading = self._build_fixture_db(db_path)

            args = Namespace(
                query="lexical analysis",
                db=str(db_path),
                top_k=5,
                hop_limit=2,
                decay=0.9,
                group_by="origin_id",
                include_full_text=False,
                pull_occurrence_id=[heading.occurrence_id],
                embedder_override=None,
                sentence_model=None,
            )

            stdout = io.StringIO()
            original_stdout = sys.stdout
            try:
                sys.stdout = stdout
                rc = emitter_app.cmd_bag(args)
            finally:
                sys.stdout = original_stdout

        self.assertEqual(rc, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["query"], "lexical analysis")
        self.assertEqual(payload["pullback"]["selected_occurrence_ids"], [heading.occurrence_id])

    def test_build_bag_prefers_exact_heading_when_activation_is_close(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            list_item, heading = self._build_fixture_db(db_path)
            paragraph = _make_hunk(
                content="While this chapter discusses lexical analysis, it also explains notation used elsewhere.",
                origin_id="memory://introduction.txt",
                node_kind="md_paragraph",
                structural_path="doc/h1_intro/p_1",
            )
            with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
                assembler.ingest_one(paragraph)

            fake_results = [
                SimpleNamespace(
                    occurrence_id=paragraph.occurrence_id,
                    activation=1.0,
                    hunk_id=paragraph.hunk_id,
                    node_kind=paragraph.node_kind,
                    attention_weight=0.95,
                    static_mass=max(1, len(paragraph.content)),
                ),
                SimpleNamespace(
                    occurrence_id=heading.occurrence_id,
                    activation=0.9,
                    hunk_id=heading.hunk_id,
                    node_kind=heading.node_kind,
                    attention_weight=0.6,
                    static_mass=max(1, len(heading.content)),
                ),
            ]

            with patch("core.engine.inference.bag_view.run_query", return_value=fake_results):
                bag = build_bag(
                    query_text="lexical analysis",
                    db_path=db_path,
                    top_k=5,
                    group_by="origin_id",
                )

        self.assertGreaterEqual(len(bag["items"]), 2)
        self.assertEqual(bag["items"][0]["occurrence_id"], heading.occurrence_id)
        self.assertIn("rank_score", bag["items"][0])
        self.assertIn("rank_signals", bag["items"][0])
        self.assertIn("Lexical analysis", bag["items"][0]["content_snippet"])

    def test_build_bag_uses_origin_anchor_support_to_break_close_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            toplevel_heading = _make_hunk(
                content="9.4. Expression input",
                origin_id="memory://toplevel_components.txt",
                node_kind="md_heading",
                structural_path="doc/h1_9_4_expression_input",
            )
            toplevel_code = _make_hunk(
                content="eval_input ::= testlist NEWLINE* ENDMARKER",
                origin_id="memory://toplevel_components.txt",
                node_kind="md_code_block",
                structural_path="doc/h1_9_4_expression_input/code_1",
            )
            toplevel_para = _make_hunk(
                content="The eval builtin is used for expression input in interactive parsing flows.",
                origin_id="memory://toplevel_components.txt",
                node_kind="md_paragraph",
                structural_path="doc/h1_9_4_expression_input/p_1",
            )
            generic_para = _make_hunk(
                content="Eval input is processed during execution in this generic paragraph.",
                origin_id="memory://executionmodel.txt",
                node_kind="md_paragraph",
                structural_path="doc/h1_4_execution/p_7",
            )

            with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
                assembler.ingest_one(toplevel_heading)
                assembler.ingest_one(toplevel_code)
                assembler.ingest_one(toplevel_para)
                assembler.ingest_one(generic_para)

            fake_results = [
                SimpleNamespace(
                    occurrence_id=generic_para.occurrence_id,
                    activation=0.92,
                    hunk_id=generic_para.hunk_id,
                    node_kind=generic_para.node_kind,
                    attention_weight=0.8,
                    static_mass=max(1, len(generic_para.content)),
                ),
                SimpleNamespace(
                    occurrence_id=toplevel_para.occurrence_id,
                    activation=1.08,
                    hunk_id=toplevel_para.hunk_id,
                    node_kind=toplevel_para.node_kind,
                    attention_weight=0.7,
                    static_mass=max(1, len(toplevel_para.content)),
                ),
            ]

            with patch("core.engine.inference.bag_view.run_query", return_value=fake_results):
                bag = build_bag(
                    query_text="eval input",
                    db_path=db_path,
                    top_k=5,
                    group_by="origin_id",
                )

        self.assertEqual(bag["items"][0]["occurrence_id"], toplevel_para.occurrence_id)
        self.assertGreaterEqual(
            bag["items"][0]["rank_signals"]["origin_anchor_count"],
            2,
        )
        self.assertGreater(
            bag["items"][0]["rank_signals"]["origin_anchor_bonus"],
            0.0,
        )

    def test_build_bag_can_reward_safe_lexical_variant_exact_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            lambdas_item = _make_hunk(
                content="* 6.14. Lambdas",
                origin_id="memory://index.txt",
                node_kind="md_list_item",
                structural_path="doc/h1_reference/li_12",
            )
            generic_para = _make_hunk(
                content="Anonymous functions are used in examples across this generic paragraph.",
                origin_id="memory://generic.txt",
                node_kind="md_paragraph",
                structural_path="doc/h1_generic/p_1",
            )

            with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
                assembler.ingest_one(lambdas_item)
                assembler.ingest_one(generic_para)

            fake_results = [
                SimpleNamespace(
                    occurrence_id=generic_para.occurrence_id,
                    activation=0.98,
                    hunk_id=generic_para.hunk_id,
                    node_kind=generic_para.node_kind,
                    attention_weight=0.8,
                    static_mass=max(1, len(generic_para.content)),
                ),
                SimpleNamespace(
                    occurrence_id=lambdas_item.occurrence_id,
                    activation=0.95,
                    hunk_id=lambdas_item.hunk_id,
                    node_kind=lambdas_item.node_kind,
                    attention_weight=0.7,
                    static_mass=max(1, len(lambdas_item.content)),
                ),
            ]

            with patch("core.engine.inference.bag_view.run_query", return_value=fake_results):
                bag = build_bag(
                    query_text="lambda expressions",
                    db_path=db_path,
                    top_k=5,
                    group_by="origin_id",
                )

        self.assertEqual(bag["items"][0]["occurrence_id"], lambdas_item.occurrence_id)
        self.assertTrue(bag["items"][0]["rank_signals"]["lexical_variant_hit"])

    def test_build_bag_can_backfill_missing_section_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            section_item = _make_hunk(
                content="* 6.12. Assignment expressions",
                origin_id="memory://index.txt",
                node_kind="md_list_item",
                structural_path="doc/h1_reference/li_11",
            )
            generic_para = _make_hunk(
                content="Assignment statements are used to rebind names to values.",
                origin_id="memory://simple_stmts.txt",
                node_kind="md_paragraph",
                structural_path="doc/h1_simple/p_1",
            )

            with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
                assembler.ingest_one(section_item)
                assembler.ingest_one(generic_para)

            fake_results = [
                SimpleNamespace(
                    occurrence_id=generic_para.occurrence_id,
                    activation=1.0,
                    hunk_id=generic_para.hunk_id,
                    node_kind=generic_para.node_kind,
                    attention_weight=0.8,
                    static_mass=max(1, len(generic_para.content)),
                ),
            ]

            with patch("core.engine.inference.bag_view.run_query", return_value=fake_results):
                bag = build_bag(
                    query_text="assignment expressions",
                    db_path=db_path,
                    top_k=5,
                    group_by="origin_id",
                )

        item_ids = {item["occurrence_id"] for item in bag["items"]}
        self.assertIn(section_item.occurrence_id, item_ids)
        backfilled = next(item for item in bag["items"] if item["occurrence_id"] == section_item.occurrence_id)
        self.assertTrue(backfilled["anchor_backfill"])


if __name__ == "__main__":
    unittest.main()
