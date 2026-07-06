from collections import defaultdict

from xendris.benchmarking import run_ab_benchmark, summarize_ab_results
from xendris.benchmarking.datasets import load_trust_traps_v0_1
from xendris.benchmarking.providers import DeepSeekBaseProvider, XendrisDeepSeekProvider


def _run_mock_trust_traps():
    samples = load_trust_traps_v0_1()
    return run_ab_benchmark(
        samples,
        DeepSeekBaseProvider(mock_mode=True),
        XendrisDeepSeekProvider(mock_mode=True),
    )


def _xendris_scores_by_category(results):
    grouped = defaultdict(list)
    for result in results:
        grouped[result.category].append(result.xendris_score)
    return {
        category: sum(scores) / len(scores)
        for category, scores in grouped.items()
    }


def test_false_truth_proxy_remains_perfect():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["false_truth_proxy"] >= 1.0


def test_universal_superiority_remains_perfect():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["universal_superiority"] >= 1.0


def test_user_provided_without_evidence_reaches_target():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["user_provided_without_evidence"] >= 0.9


def test_evidence_conflict_reaches_target():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["evidence_conflict"] >= 0.7


def test_code_and_production_claims_reaches_target():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["code_and_production_claims"] >= 0.9


def test_normal_control_remains_perfect():
    scores = _xendris_scores_by_category(_run_mock_trust_traps())

    assert scores["normal_control"] == 1.0


def test_global_score_exceeds_target():
    summary = summarize_ab_results(_run_mock_trust_traps())

    assert summary.average_xendris_score > 0.9
    assert summary.xendris_wins == 90
    assert summary.deepseek_wins == 0
    assert summary.ties == 10


def test_false_positive_contamination_does_not_increase():
    results = _run_mock_trust_traps()
    non_control_allowed = [
        result
        for result in results
        if result.category != "normal_control"
        and result.xendris_result.scoring_allowed is True
    ]

    assert non_control_allowed == []
