from kitt.evolution.experience import EpisodeTrace, ExperienceGeneralizer


def test_generalizer_promotes_only_repeated_evidence_backed_success():
    episodes = [
        EpisodeTrace("e1", "Fix flaky settlement migration", "SUCCESS", ("inspect logs", "run tests"), ("test passed",)),
        EpisodeTrace("e2", "Fix flaky settlement migration", "OUTCOME_SUPPORTED", ("inspect logs", "run tests"), ("reproduced", "test passed")),
        EpisodeTrace("e3", "Fix flaky settlement migration", "FAILED", ("edit blindly",), (), ("migration failed",)),
        EpisodeTrace("x1", "Unrelated one-off task", "SUCCESS", ("read file",), ("done",)),
    ]
    items = ExperienceGeneralizer.generalize(episodes, min_support=2, min_success_rate=0.6)
    assert len(items) == 1
    item = items[0]
    assert item.support_count == 3
    assert item.success_count == 2
    assert "run tests" in item.successful_actions
    assert "migration failed" in item.failure_signals
    assert item.confidence > 0.5
