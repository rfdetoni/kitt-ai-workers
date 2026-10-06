import unittest
from kitt.evals.retrieval import run_eval


class RetrievalAblationTests(unittest.TestCase):
    def test_graph_and_reranking_exercise_distinct_retrieval_stages(self):
        results = run_eval()["ablations"]
        structural = results["hybrid_structural"]["details"]
        graph = results["hybrid_graph"]["details"]
        reranked = results["hybrid_graph_lexical_rerank"]["details"]
        self.assertTrue(all(item["retrieval"]["graph_candidates"] == 0 for item in structural))
        self.assertTrue(any(item["retrieval"]["graph_candidates"] > 0 for item in graph))
        self.assertTrue(any(item["retrieval"]["semantic_candidates"] > 0 for item in reranked))
        self.assertNotEqual([item["paths"] for item in structural], [item["paths"] for item in graph])
        self.assertTrue(all("elapsed_ms" in item and "tokens" in item for item in graph))
