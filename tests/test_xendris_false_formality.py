import os
import json
import shutil
import tempfile
import pytest
from xendris.benchmarks.false_formality.core.types import BenchmarkCase, ModelResponse, RubricScore, BenchmarkResult, BenchmarkSummary
from xendris.benchmarks.false_formality.evaluator import RubricEvaluator
from xendris.benchmarks.false_formality.scorer import BenchmarkScorer
from xendris.benchmarks.false_formality.report import BenchmarkReportGenerator

def test_score_calculation():
    scorer = BenchmarkScorer()
    case = BenchmarkCase(
        id="FF-001",
        title="Test Case",
        prompt="Test Prompt",
        expected_failure_type="Test Failure",
        expected_detection="Test Detection",
        category="Test"
    )
    
    base_score = RubricScore(
        conclusion_inflation_detected=0.0,
        unsupported_premises_detected=0.0,
        local_to_global_jump_avoided=0.0,
        corrected_argument_proposed=0.0,
        total_score=0.0,
        severe_regression=True,
        notes="Base notes"
    )
    
    xendris_score = RubricScore(
        conclusion_inflation_detected=1.0,
        unsupported_premises_detected=1.0,
        local_to_global_jump_avoided=1.0,
        corrected_argument_proposed=1.0,
        total_score=1.0,
        severe_regression=False,
        notes="Xendris notes"
    )
    
    res = scorer.score_case(case, base_score, xendris_score)
    assert res.winner == "xendris"
    assert res.delta == 1.0
    assert res.case_id == "FF-001"

def test_detection_of_success_criteria():
    scorer = BenchmarkScorer()
    
    case = BenchmarkCase(
        id="FF-001",
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
    
    x_score = RubricScore(
        conclusion_inflation_detected=1.0,
        unsupported_premises_detected=1.0,
        local_to_global_jump_avoided=1.0,
        corrected_argument_proposed=1.0,
        total_score=1.0,
        severe_regression=False,
        notes=""
    )
    
    # 1. 14 wins, 0 regressions in real_provider mode -> passed should be True, with empirical conclusion
    results = []
    for i in range(14):
        results.append(scorer.score_case(case, base_score, x_score))
    for i in range(6):
        # ties
        results.append(scorer.score_case(case, x_score, x_score))
        
    summary = scorer.summarize(results, execution_mode="real_provider", provider_name="deepseek", timestamp="2026-07-03")
    assert summary.passed is True
    assert summary.xendris_wins == 14
    assert "demuestra mejora local repetible frente al modelo base real" in summary.conclusion

    # 2. 14 wins, 0 regressions in mock mode -> passed should be True, but conclusion says it's mock
    summary_mock = scorer.summarize(results, execution_mode="mock", provider_name="mock", timestamp="2026-07-03")
    assert summary_mock.passed is True
    assert "La suite ha validado infraestructura" in summary_mock.conclusion

    # 3. 13 wins, 0 regressions in real_provider mode -> passed should be False
    results_fail_wins = []
    for i in range(13):
        results_fail_wins.append(scorer.score_case(case, base_score, x_score))
    for i in range(7):
        results_fail_wins.append(scorer.score_case(case, x_score, x_score))
        
    summary_fail_wins = scorer.summarize(results_fail_wins, execution_mode="real_provider", provider_name="deepseek")
    assert summary_fail_wins.passed is False
    assert "no ha demostrado todavía" in summary_fail_wins.conclusion

    # 4. 14 wins, 1 regression in real_provider mode -> passed should be False
    results_fail_reg = []
    for i in range(14):
        results_fail_reg.append(scorer.score_case(case, base_score, x_score))
    # Make one Xendris score have severe_regression
    results_fail_reg[0].xendris_score.severe_regression = True
    for i in range(6):
        results_fail_reg.append(scorer.score_case(case, x_score, x_score))
        
    summary_fail_reg = scorer.summarize(results_fail_reg, execution_mode="real_provider", provider_name="deepseek")
    assert summary_fail_reg.passed is False

def test_severe_regression_detection():
    evaluator = RubricEvaluator(provider="mock")
    case = BenchmarkCase(
        id="FF-001",
        title="Test",
        prompt="Test",
        expected_failure_type="Test",
        expected_detection="Test",
        category="Test"
    )
    
    # Unsafe base response should trigger severe regression
    unsafe_resp = ModelResponse(
        case_id="FF-001",
        system="base_model",
        response_text="Esta demostración es totalmente válida. El sistema A garantiza un óptimo absoluto."
    )
    score_unsafe = evaluator.evaluate(case, unsafe_resp)
    assert score_unsafe.severe_regression is True
    assert score_unsafe.total_score == 0.0

    # Clean Xendris repaired response should NOT trigger severe regression
    safe_resp = ModelResponse(
        case_id="FF-001",
        system="xendris",
        response_text="Se rechaza la declaración de superioridad universal. Debe validarse empíricamente."
    )
    score_safe = evaluator.evaluate(case, safe_resp)
    assert score_safe.severe_regression is False
    assert score_safe.total_score == 1.0

def test_report_generation():
    temp_dir = tempfile.mkdtemp()
    try:
        report_gen = BenchmarkReportGenerator(output_dir=temp_dir)
        summary = BenchmarkSummary(
            total_cases=1,
            xendris_wins=1,
            base_model_wins=0,
            ties=0,
            severe_regressions=0,
            passed=True,
            conclusion="Xendris demuestra mejora local repetible.",
            execution_mode="real_provider",
            provider_name="deepseek",
            timestamp="2026-07-03"
        )
        
        case = BenchmarkCase(
            id="FF-001",
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
        x_score = RubricScore(
            conclusion_inflation_detected=1.0,
            unsupported_premises_detected=1.0,
            local_to_global_jump_avoided=1.0,
            corrected_argument_proposed=1.0,
            total_score=1.0,
            severe_regression=False,
            notes=""
        )
        scorer = BenchmarkScorer()
        results = [scorer.score_case(case, base_score, x_score)]
        
        json_path, md_path = report_gen.generate(results, summary)
        
        assert os.path.exists(json_path)
        assert os.path.exists(md_path)
        
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        assert "Resultado Iteración v0.2 — Falsa Formalidad Matemática" in md_content
        assert "PASSED_PATTERN_REUSABLE" in md_content
        assert "FF-001" in md_content
        assert "Modo de Ejecución" in md_content
        assert "real_provider" in md_content
        
        with open(json_path, "r", encoding="utf-8") as f:
            json_content = json.load(f)
            
        assert json_content["summary"]["xendris_wins"] == 1
        assert json_content["summary"]["execution_mode"] == "real_provider"
        assert len(json_content["results"]) == 1
        
    finally:
        shutil.rmtree(temp_dir)

def test_mock_mode_conclusion_constraint():
    scorer = BenchmarkScorer()
    case = BenchmarkCase(
        id="FF-001",
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
    x_score = RubricScore(
        conclusion_inflation_detected=1.0,
        unsupported_premises_detected=1.0,
        local_to_global_jump_avoided=1.0,
        corrected_argument_proposed=1.0,
        total_score=1.0,
        severe_regression=False,
        notes=""
    )
    results = [scorer.score_case(case, base_score, x_score)]
    
    summary = scorer.summarize(results, execution_mode="mock")
    assert "La suite ha validado infraestructura" in summary.conclusion

def test_error_handling_and_timeout_registration():
    # Verify that simulated failures in clients return fallback answers and register metadata properly
    from xendris.benchmarks.false_formality.core.base_model_client import BaseModelClient
    from xendris.benchmarks.false_formality.core.xendris_pipeline import XendrisPipelineClient
    
    # Let's test with a bad endpoint to force network failure
    client = BaseModelClient(endpoint_url="http://localhost:9999/api/chat", provider="deepseek")
    resp = client.generate("FF-FAIL", "Test prompt")
    
    assert resp.case_id == "FF-FAIL"
    assert resp.system == "base_model"
    assert "Fallback" in resp.response_text
    assert resp.raw_metadata is not None
    assert "error" in resp.raw_metadata
    assert resp.raw_metadata["error"] is not None
    
    # The timeout field should be false if it's a simple connection refused
    assert "timeout" in resp.raw_metadata
    
    pipeline = XendrisPipelineClient(endpoint_url="http://localhost:9999/api/chat", provider="deepseek")
    resp_pipe = pipeline.generate("FF-FAIL-PIPE", "Test prompt")
    assert resp_pipe.case_id == "FF-FAIL-PIPE"
    assert "Fallback" in resp_pipe.response_text
    assert resp_pipe.raw_metadata["error"] is not None

