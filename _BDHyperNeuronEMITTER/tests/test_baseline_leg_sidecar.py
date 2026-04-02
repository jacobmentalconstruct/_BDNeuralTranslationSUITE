import sqlite3
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
EMITTER_SRC = REPO_ROOT / "_BDHyperNeuronEMITTER" / "src"
TOOLS_DIR = REPO_ROOT / ".dev-tools" / "final-tools" / "tools"
for path in (str(EMITTER_SRC), str(TOOLS_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

from baseline_leg_session import make_panel_action, merge_session_for_action
from baseline_leg_sidecar_lib import build_sidecar_shelf, compare_leg_specs
from core.assembler.core import GraphAssembler
from core.contract.hyperhunk import HyperHunk
from core.engine.inference.bag_view import build_bag
from core.engine.inference.provider import EmbeddingProviderSpec, save_embedding_provider_spec


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


class _FakeEmbedProvider:
    def __init__(self, vector):
        self._vector = vector

    def embed_texts(self, texts):
        return type(
            "EmbedResultLike",
            (),
            {
                "vectors": [list(self._vector) for _ in texts],
                "dimensions": len(self._vector),
                "token_counts": [len(t.split()) for t in texts],
                "token_ids": [[] for _ in texts],
            },
        )()


def _make_hunk(*, content: str, origin_id: str, node_kind: str, structural_path: str):
    return HyperHunk(
        content=content,
        origin_id=origin_id,
        layer_type="CST",
        node_kind=node_kind,
        structural_path=structural_path,
        token_count=max(1, len(content.split())),
    )


class BaselineLegSidecarTests(unittest.TestCase):
    def _build_fixture_db(self, db_path: Path) -> tuple[HyperHunk, HyperHunk]:
        heading = _make_hunk(
            content="6.14. Lambda expressions",
            origin_id="memory://expressions.txt",
            node_kind="md_heading",
            structural_path="doc/h1_6_14_lambda_expressions",
        )
        paragraph = _make_hunk(
            content="Anonymous functions are described in the lambda expressions section.",
            origin_id="memory://expressions.txt",
            node_kind="md_paragraph",
            structural_path="doc/h1_6_14_lambda_expressions/p_1",
        )

        with GraphAssembler(db_path, AlwaysOnNucleus(), window_size=10) as assembler:
            assembler.ingest_one(heading)
            assembler.ingest_one(paragraph)

        return heading, paragraph

    def _write_vector(self, db_path: Path, occurrence_id: str, vector: list[float]) -> None:
        blob = struct.pack(f"<{len(vector)}f", *vector)
        conn = sqlite3.connect(str(db_path))
        try:
            conn.execute(
                "UPDATE occurrence_nodes SET vector_blob = ? WHERE occurrence_id = ?",
                (blob, occurrence_id),
            )
            conn.commit()
        finally:
            conn.close()

    def test_fts_shelf_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            heading, _ = self._build_fixture_db(db_path)

            shelf = build_sidecar_shelf(
                query_text="lambda expressions",
                db_path=db_path,
                mode="fts",
                top_k=5,
            )

        self.assertEqual(shelf["mode"], "fts")
        self.assertIn("summary", shelf)
        self.assertIn("items", shelf)
        self.assertGreaterEqual(len(shelf["items"]), 1)
        top = shelf["items"][0]
        self.assertEqual(top["occurrence_id"], heading.occurrence_id)
        self.assertIn("score", top)
        self.assertNotIn("activation", top)
        self.assertNotIn("rank_signals", top)

    def test_ann_shelf_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            heading, paragraph = self._build_fixture_db(db_path)
            save_embedding_provider_spec(
                db_path.parent,
                EmbeddingProviderSpec(provider="deterministic", artifacts_dir=str(db_path.parent)),
            )
            self._write_vector(db_path, heading.occurrence_id, [1.0, 0.0])
            self._write_vector(db_path, paragraph.occurrence_id, [0.0, 1.0])

            with patch(
                "baseline_leg_sidecar_lib.create_embed_provider",
                return_value=_FakeEmbedProvider([1.0, 0.0]),
            ):
                shelf = build_sidecar_shelf(
                    query_text="lambda expressions",
                    db_path=db_path,
                    mode="ann",
                    top_k=5,
                    ann_provider="deterministic",
                )

        self.assertEqual(shelf["mode"], "ann")
        self.assertEqual(shelf["provider"]["provider"], "deterministic")
        top = shelf["items"][0]
        self.assertEqual(top["occurrence_id"], heading.occurrence_id)
        self.assertIn("score", top)
        self.assertEqual(top["score_kind"], "cosine")
        self.assertNotIn("activation", top)
        self.assertNotIn("rank_signals", top)

    def test_sidecar_pullback_recovers_verbatim_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            heading, _ = self._build_fixture_db(db_path)

            shelf = build_sidecar_shelf(
                query_text="lambda expressions",
                db_path=db_path,
                mode="fts",
                top_k=5,
                pull_occurrence_ids=[heading.occurrence_id],
            )

        self.assertEqual(shelf["pullback"]["selected_occurrence_ids"], [heading.occurrence_id])
        self.assertIn("Lambda expressions", shelf["pullback"]["items"][0]["pullback_text"])

    def test_sidecar_bag_mode_matches_live_bag_core_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            heading, _ = self._build_fixture_db(db_path)

            expected = build_bag(
                query_text="lambda expressions",
                db_path=db_path,
                top_k=5,
                hop_limit=1,
                decay=0.9,
                group_by="origin_id",
            )
            actual = build_sidecar_shelf(
                query_text="lambda expressions",
                db_path=db_path,
                mode="bag",
                top_k=5,
            )

        self.assertEqual(actual["mode"], "bag")
        self.assertEqual(actual["summary"]["item_count"], expected["bag_summary"]["item_count"])
        self.assertEqual(actual["items"][0]["occurrence_id"], expected["items"][0]["occurrence_id"])
        self.assertEqual(actual["items"][0]["origin_id"], heading.origin_id)

    def test_compare_payload_reports_baseline_overlap(self):
        with patch(
            "baseline_leg_sidecar_lib.build_sidecar_shelf",
            side_effect=[
                {"items": [{"occurrence_id": "fts-1", "origin_id": "memory://fts.txt", "node_kind": "md_heading", "content_snippet": "fts"}]},
                {"items": [{"occurrence_id": "st-1", "origin_id": "memory://st.txt", "node_kind": "md_heading", "content_snippet": "st"}]},
                {"items": [{"occurrence_id": "det-1", "origin_id": "memory://det.txt", "node_kind": "md_paragraph", "content_snippet": "det"}]},
                {"items": [{"occurrence_id": "bag-1", "origin_id": "memory://bag.txt", "node_kind": "md_heading", "content_snippet": "bag"}]},
            ],
        ):
            payload = compare_leg_specs(
                leg_specs=[
                    {"label": "fts", "mode": "fts", "db": str(REPO_ROOT / "fts.db")},
                    {"label": "ann_sentence", "mode": "ann", "db": str(REPO_ROOT / "st.db")},
                    {"label": "ann_deterministic", "mode": "ann", "db": str(REPO_ROOT / "det.db")},
                    {"label": "bag", "mode": "bag", "db": str(REPO_ROOT / "bag.db")},
                ],
                query_shelf=["lambda expressions"],
                top_k=3,
            )

        self.assertIn("difference_read", payload)
        self.assertEqual(payload["legs"]["bag"]["summary"]["same_top_count_vs_bag"], 1)

    def test_make_panel_action_defaults_to_agent_run_query(self):
        action = make_panel_action(
            db="C:/demo/cold.db",
            query="black box",
            mode="fts",
            ann_provider="auto",
            top_k=8,
        )

        self.assertEqual(action["kind"], "run_query")
        self.assertEqual(action["source"], "agent")
        self.assertEqual(action["query"], "black box")
        self.assertTrue(action["action_id"])

    def test_merge_session_for_action_sets_shared_visible_pending_action(self):
        action = make_panel_action(
            db="C:/demo/cold.db",
            query="gravity",
            mode="ann",
            ann_provider="sentence-transformers",
            top_k=5,
            source="agent",
            action_id="abc123",
        )

        merged = merge_session_for_action(
            {
                "query": "old",
                "mode": "fts",
                "ann_provider": "auto",
                "payload": {"items": [1]},
            },
            action,
            control_mode="shared-visible",
        )

        self.assertEqual(merged["query"], "gravity")
        self.assertEqual(merged["mode"], "ann")
        self.assertEqual(merged["ann_provider"], "sentence-transformers")
        self.assertEqual(merged["control_mode"], "shared-visible")
        self.assertEqual(merged["pending_action"]["action_id"], "abc123")
        self.assertEqual(merged["selected_occurrence_id"], "")


if __name__ == "__main__":
    unittest.main()
