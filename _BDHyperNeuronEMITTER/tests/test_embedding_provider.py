import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


EMITTER_SRC = Path(__file__).resolve().parents[1] / "src"
if str(EMITTER_SRC) not in sys.path:
    sys.path.insert(0, str(EMITTER_SRC))

from core.engine.inference.provider import (
    EmbeddingProviderSpec,
    _lexical_anchor_queries,
    load_embedding_provider_spec,
    query,
    save_embedding_provider_spec,
)
from core.engine.inference.retrieval import AnchorResult


class _FakeEmbedProvider:
    def embed_texts(self, texts):
        return type(
            "EmbedResultLike",
            (),
            {
                "vectors": [[1.0, 0.0] for _ in texts],
                "dimensions": 2,
                "token_counts": [len(t.split()) for t in texts],
                "token_ids": [[] for _ in texts],
            },
        )()


class _FakeHotEngine:
    def __init__(self, decay: float, hop_limit: int) -> None:
        self.decay = decay
        self.hop_limit = hop_limit

    def run(self, subgraph, anchor_ids, top_k: int = 20):
        return [
            type(
                "BagResult",
                (),
                {
                    "occurrence_id": anchor_ids[0],
                    "hunk_id": "h1",
                    "node_kind": "md_paragraph",
                    "activation": 0.91,
                    "attention_weight": 1.0,
                    "static_mass": 10,
                },
            )()
        ]


class EmbeddingProviderTests(unittest.TestCase):
    def test_lexical_anchor_queries_adds_safe_variants(self):
        self.assertEqual(
            _lexical_anchor_queries("eval input"),
            ["eval input", "expression input", "eval_input"],
        )
        self.assertEqual(
            _lexical_anchor_queries("lambda expressions"),
            [
                "lambda expressions",
                "lambda expression",
                "lambdas",
                "anonymous functions",
                "lambda_expressions",
            ],
        )
        self.assertEqual(
            _lexical_anchor_queries("anonymous functions"),
            [
                "anonymous functions",
                "lambda expressions",
                "lambda expression",
                "lambdas",
                "anonymous_functions",
                "anonymous function",
            ],
        )
        self.assertEqual(
            _lexical_anchor_queries("walrus operator"),
            [
                "walrus operator",
                "assignment expressions",
                "assignment expression",
                "walrus_operator",
            ],
        )

    def test_provider_spec_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            saved = save_embedding_provider_spec(
                output_dir,
                EmbeddingProviderSpec(
                    provider="sentence-transformers",
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    artifacts_dir="",
                ),
            )
            self.assertTrue(saved.is_file())
            loaded = load_embedding_provider_spec(output_dir / "cold.db")
            self.assertEqual(loaded.provider, "sentence-transformers")
            self.assertEqual(loaded.model_name, "sentence-transformers/all-MiniLM-L6-v2")

    def test_query_uses_sentence_provider_metadata_for_ann(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            db_path.touch()
            save_embedding_provider_spec(
                db_path.parent,
                EmbeddingProviderSpec(
                    provider="sentence-transformers",
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                ),
            )

            anchors = [
                AnchorResult(
                    occurrence_id="occ-1",
                    hunk_id="h1",
                    score=0.88,
                    origin_id="memory://doc.txt",
                    node_kind="md_paragraph",
                    content_snippet="semantic result",
                )
            ]

            with patch(
                "core.engine.inference.provider.create_embed_provider",
                return_value=_FakeEmbedProvider(),
            ) as create_provider, patch(
                "core.engine.inference.retrieval.fts_search",
                return_value=[],
            ), patch(
                "core.engine.inference.retrieval.ann_search",
                return_value=anchors,
            ) as ann_search, patch(
                "core.engine.inference.retrieval.load_subgraph",
                return_value={"nodes": {}, "edges": [], "inhibit_occ_pairs": []},
            ), patch(
                "core.engine.inference.hot_engine.HotEngine",
                _FakeHotEngine,
            ):
                results = query("semantic check", db_path=db_path, top_k=5)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].occurrence_id, "occ-1")
            create_provider.assert_called_once()
            ann_search.assert_called_once()

    def test_query_runs_fts_over_lexical_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            db_path.touch()

            calls = []

            def _fake_fts(conn, query_text, top_k=10):
                calls.append(query_text)
                if query_text == "expression input":
                    return [
                        AnchorResult(
                            occurrence_id="occ-variant",
                            hunk_id="h-variant",
                            score=0.91,
                            origin_id="memory://toplevel_components.txt",
                            node_kind="md_heading",
                            content_snippet="9.4. Expression input",
                        )
                    ]
                return []

            with patch(
                "core.engine.inference.retrieval.fts_search",
                side_effect=_fake_fts,
            ), patch(
                "core.engine.inference.retrieval.load_subgraph",
                return_value={"nodes": {}, "edges": [], "inhibit_occ_pairs": []},
            ), patch(
                "core.engine.inference.hot_engine.HotEngine",
                _FakeHotEngine,
            ):
                results = query("eval input", db_path=db_path, top_k=5)

            self.assertEqual(calls[:3], ["eval input", "expression input", "eval_input"])
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].occurrence_id, "occ-variant")

    def test_query_runs_fts_over_articulation_alias_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "cold.db"
            db_path.touch()

            calls = []

            def _fake_fts(conn, query_text, top_k=10):
                calls.append(query_text)
                if query_text == "lambda expressions":
                    return [
                        AnchorResult(
                            occurrence_id="occ-lambda",
                            hunk_id="h-lambda",
                            score=0.94,
                            origin_id="memory://expressions.txt",
                            node_kind="md_heading",
                            content_snippet="6.14. Lambda expressions",
                        )
                    ]
                return []

            with patch(
                "core.engine.inference.retrieval.fts_search",
                side_effect=_fake_fts,
            ), patch(
                "core.engine.inference.retrieval.load_subgraph",
                return_value={"nodes": {}, "edges": [], "inhibit_occ_pairs": []},
            ), patch(
                "core.engine.inference.hot_engine.HotEngine",
                _FakeHotEngine,
            ):
                results = query("anonymous functions", db_path=db_path, top_k=5)

            self.assertEqual(calls[:4], ["anonymous functions", "lambda expressions", "lambda expression", "lambdas"])
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].occurrence_id, "occ-lambda")


if __name__ == "__main__":
    unittest.main()
