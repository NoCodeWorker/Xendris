import pytest
from xendris.benchmarks.false_formality.core.types import BenchmarkCase, RubricScore, BenchmarkResult, BenchmarkSummary
from xendris.benchmarks.false_formality.scorer import BenchmarkScorer

def test_scorer_case_scoring_contract():
    scorer = BenchmarkScorer()
    case = BenchmarkCase(
        id="FF-TEST",
        title="Test",
        prompt="Test",
        expected_failure_type="Test",
        expected_detection="Test",
        category="Test"
    )
    base_score = RubricScore(
        conclusion_inflation_detected=0.0,
        unsupported_premises_detected=0.0,
        local_to_global_jump_avoided=0.0,
        corrected_argument_proposed=0.0,
        total_score=0.0,
        severe_regression=True,
        notes=""
    )
    xendris_score = RubricScore(
        conclusion_inflation_detected=1.0,
        unsupported_premises_detected=1.0,
        local_to_global_jump_avoided=1.0,
        corrected_argument_proposed=1.0,
        total_score=1.0,
        severe_regression=False,
        notes=""
    )
    
    result = scorer.score_case(case, base_score, xendris_score)
    assert isinstance(result, BenchmarkResult)
    assert result.case_id == "FF-TEST"
    assert result.winner == "xendris"
    assert result.delta == 1.0

def test_scorer_summary_contract():
    scorer = BenchmarkScorer()
    case = BenchmarkCase(
        id="FF-TEST",
        title="Test",
        prompt="Test",
        expected_failure_type="Test",
        expected_detection="Test",
        category="Test"
    )
    base_score = RubricScore(
        conclusion_inflation_detected=0.0,
        unsupported_premises_detected=0.0,
        local_to_global_jump_avoided=0.0,
        corrected_argument_proposed=0.0,
        total_score=0.0,
        severe_regression=True,
        notes=""
    )
    xendris_score = RubricScore(
        conclusion_inflation_detected=1.0,
        unsupported_premises_detected=1.0,
        local_to_global_jump_avoided=1.0,
        corrected_argument_proposed=1.0,
        total_score=1.0,
        severe_regression=False,
        notes=""
    )
    
    results = [scorer.score_case(case, base_score, xendris_score)]
    summary = scorer.summarize(results)
    
    assert isinstance(summary, BenchmarkSummary)
    assert summary.total_cases == 1
    assert summary.xendris_wins == 1
    assert summary.base_model_wins == 0
    assert summary.ties == 0
    assert summary.severe_regressions == 0
    # Wins (1/1) is less than 14/20 -> passed should be False
    assert summary.passed is False
