from kitt.evals.memory_long_horizon import run_long_memory_eval


def test_long_horizon_structured_compaction_retains_salient_evidence():
    result = run_long_memory_eval(500)
    assert result["recall"] == 1.0
    assert result["tokens_after"] < result["tokens_before"]
    assert result["retained_ratio"] < 0.25
