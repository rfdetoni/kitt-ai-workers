import unittest

from kitt.evals.corpus import DEFAULT_EVAL_CORPUS
from kitt.evals.inspect_bridge import to_inspect_records
from kitt.evals.promptfoo_bridge import DEFAULT_RED_TEAM_CASES, promptfoo_config


class EvalBridgeTests(unittest.TestCase):
    def test_inspect_bridge_preserves_eval_contract(self):
        records = to_inspect_records(DEFAULT_EVAL_CORPUS)
        self.assertEqual(len(records), len(DEFAULT_EVAL_CORPUS))
        self.assertEqual(records[0].id, DEFAULT_EVAL_CORPUS[0].id)
        self.assertEqual(records[0].target, DEFAULT_EVAL_CORPUS[0].expected_route)
        self.assertEqual(
            records[0].metadata["expected_intent"],
            DEFAULT_EVAL_CORPUS[0].expected_intent,
        )

    def test_promptfoo_bridge_emits_security_cases(self):
        config = promptfoo_config("echo")
        self.assertEqual(config["prompts"], ["{{prompt}}"])
        self.assertEqual(len(config["tests"]), len(DEFAULT_RED_TEAM_CASES))
        categories = {item["metadata"]["category"] for item in config["tests"]}
        self.assertTrue(
            {"authorization", "path-boundary", "data-exfiltration"}.issubset(categories)
        )


if __name__ == "__main__":
    unittest.main()
