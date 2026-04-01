import sys
import unittest
from pathlib import Path


EMITTER_SRC = Path(__file__).resolve().parents[1] / "src"
if str(EMITTER_SRC) not in sys.path:
    sys.path.insert(0, str(EMITTER_SRC))

from core.engine.inference.hot_engine import HotEngine


class HotEngineTests(unittest.TestCase):
    def test_propagates_forward_along_source_to_target_edge(self):
        subgraph = {
            "nodes": {
                "A": {
                    "hunk_id": "hA",
                    "node_kind": "test",
                    "attention_weight": 1.0,
                    "static_mass": 1,
                    "vector": None,
                },
                "B": {
                    "hunk_id": "hB",
                    "node_kind": "test",
                    "attention_weight": 1.0,
                    "static_mass": 1,
                    "vector": None,
                },
            },
            "edges": [("A", "pull", "B", 0.5)],
            "inhibit_occ_pairs": [],
        }

        results = HotEngine(decay=0.9, hop_limit=1).run(subgraph, ["A"], top_k=10)
        activations = {item.occurrence_id: item.activation for item in results}

        self.assertAlmostEqual(activations["A"], 0.9)
        self.assertAlmostEqual(activations["B"], 0.5)

    def test_seeded_target_does_not_backpropagate_to_source(self):
        subgraph = {
            "nodes": {
                "A": {
                    "hunk_id": "hA",
                    "node_kind": "test",
                    "attention_weight": 1.0,
                    "static_mass": 1,
                    "vector": None,
                },
                "B": {
                    "hunk_id": "hB",
                    "node_kind": "test",
                    "attention_weight": 1.0,
                    "static_mass": 1,
                    "vector": None,
                },
            },
            "edges": [("A", "pull", "B", 0.5)],
            "inhibit_occ_pairs": [],
        }

        results = HotEngine(decay=0.9, hop_limit=1).run(subgraph, ["B"], top_k=10)
        activations = {item.occurrence_id: item.activation for item in results}

        self.assertAlmostEqual(activations["B"], 0.9)
        self.assertNotIn("A", activations)


if __name__ == "__main__":
    unittest.main()
