from kitt.evals.corpus import DEFAULT_EVAL_CORPUS
from kitt.evals.inspect_bridge import to_inspect_records
from kitt.evals.promptfoo_bridge import DEFAULT_RED_TEAM_CASES, promptfoo_config


def test_inspect_bridge_preserves_eval_contract():
    records = to_inspect_records(DEFAULT_EVAL_CORPUS)
    assert len(records) == len(DEFAULT_EVAL_CORPUS)
    assert records[0].id == DEFAULT_EVAL_CORPUS[0].id
    assert records[0].target == DEFAULT_EVAL_CORPUS[0].expected_route
    assert records[0].metadata["expected_intent"] == DEFAULT_EVAL_CORPUS[0].expected_intent


def test_promptfoo_bridge_emits_security_cases():
    config = promptfoo_config("echo")
    assert config["prompts"] == ["{{prompt}}"]
    assert len(config["tests"]) == len(DEFAULT_RED_TEAM_CASES)
    categories = {item["metadata"]["category"] for item in config["tests"]}
    assert {"authorization", "path-boundary", "data-exfiltration"}.issubset(categories)
