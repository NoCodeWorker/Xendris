import os
import tempfile
import pytest
from xendris.benchmarking import (
    BenchmarkSample,
    SystemRunResult,
    ABComparisonResult,
    run_ab_benchmark,
    summarize_ab_results,
    score_result_against_expected,
    write_ab_results_jsonl,
    read_ab_results_jsonl,
    write_ab_summary_json,
)
from xendris.benchmarking.ab_runner import compute_result_fingerprint


# Mock callables for testing
def mock_deepseek_ok(sample: BenchmarkSample) -> dict:
    return {
        "base_model": "deepseek-chat",
        "answer": "This is a standard answer.",
        "decision": "APPROVED_FOR_SCORING",
        "reason": "NONE",
        "scoring_allowed": True,
        "latency_ms": 100,
        "input_tokens": 50,
        "output_tokens": 40,
        "estimated_cost_usd": 0.0001,
        "error": None,
    }


def mock_xendris_ok(sample: BenchmarkSample) -> dict:
    return {
        "base_model": "deepseek-chat",
        "answer": "This is a standard answer.",
        "decision": "APPROVED_FOR_SCORING",
        "reason": "NONE",
        "scoring_allowed": True,
        "latency_ms": 150,
        "input_tokens": 60,
        "output_tokens": 50,
        "estimated_cost_usd": 0.00015,
        "error": None,
    }


def test_1_run_ab_benchmark_with_mock_callables():
    sample = BenchmarkSample(
        sample_id="SAMPLE-1",
        prompt="Valid normal prompt.",
        category="general",
        expected_decision="APPROVED_FOR_SCORING",
        expected_reason="NONE",
    )
    results = run_ab_benchmark([sample], mock_deepseek_ok, mock_xendris_ok)
    assert len(results) == 1
    assert results[0].sample_id == "SAMPLE-1"
    assert results[0].winner == "tie"


def test_2_xendris_wins_on_exclude_vs_human_review():
    sample = BenchmarkSample(
        sample_id="SAMPLE-2",
        prompt="Unsupported scoring rule prompt.",
        category="citation_as_proxy",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="UNSUPPORTED_SCORING_RULE",
    )

    def ds_bad(s):
        return {
            "answer": "Yes, it is verified.",
            "decision": "HUMAN_REVIEW_REQUIRED",
            "reason": "HUMAN_REVIEW_POLICY",
            "scoring_allowed": False,
            "estimated_cost_usd": 0.0001,
        }

    def xe_good(s):
        return {
            "answer": "Rule not supported, excluded.",
            "decision": "EXCLUDE_FROM_SCORING",
            "reason": "UNSUPPORTED_SCORING_RULE",
            "scoring_allowed": False,
            "estimated_cost_usd": 0.00015,
        }

    results = run_ab_benchmark([sample], ds_bad, xe_good)
    assert results[0].winner == "xendris"
    assert results[0].xendris_score > results[0].deepseek_score


def test_3_tie_when_both_correct():
    sample = BenchmarkSample(
        sample_id="SAMPLE-3",
        prompt="Test.",
        category="general",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="TIMEOUT",
    )

    def callable_timeout(s):
        return {
            "answer": "Timeout occurred.",
            "decision": "EXCLUDE_FROM_SCORING",
            "reason": "TIMEOUT",
            "scoring_allowed": False,
        }

    results = run_ab_benchmark([sample], callable_timeout, callable_timeout)
    assert results[0].winner == "tie"
    assert results[0].deepseek_score == 1.0
    assert results[0].xendris_score == 1.0


def test_4_deepseek_wins_if_xendris_worse():
    sample = BenchmarkSample(
        sample_id="SAMPLE-4",
        prompt="Test.",
        category="general",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="TIMEOUT",
    )

    def ds_correct(s):
        return {
            "answer": "Timeout.",
            "decision": "EXCLUDE_FROM_SCORING",
            "reason": "TIMEOUT",
            "scoring_allowed": False,
        }

    def xe_incorrect(s):
        # Incorrectly approves
        return {
            "answer": "Sure, it is fine.",
            "decision": "APPROVED_FOR_SCORING",
            "reason": "NONE",
            "scoring_allowed": True,
        }

    results = run_ab_benchmark([sample], ds_correct, xe_incorrect)
    assert results[0].winner == "deepseek"
    assert results[0].deepseek_score == 1.0
    assert results[0].xendris_score == 0.0


def test_5_score_result_against_expected_perfect_match():
    sample = BenchmarkSample(
        sample_id="S1",
        prompt="test",
        category="test",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="TIMEOUT",
    )
    res = SystemRunResult(
        sample_id="S1",
        system_name="x",
        base_model="bm",
        answer="timeout",
        decision="EXCLUDE_FROM_SCORING",
        reason="TIMEOUT",
        scoring_allowed=False,
    )
    assert score_result_against_expected(res, sample) == 1.0


def test_6_score_result_against_expected_partial_reason_mismatch():
    sample = BenchmarkSample(
        sample_id="S1",
        prompt="test",
        category="test",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="TIMEOUT",
    )
    res = SystemRunResult(
        sample_id="S1",
        system_name="x",
        base_model="bm",
        answer="some other error",
        decision="EXCLUDE_FROM_SCORING",
        reason="RUNTIME_ERROR",
        scoring_allowed=False,
    )
    assert score_result_against_expected(res, sample) == 0.7


def test_7_score_result_against_expected_fails_on_exclusion_approval():
    sample = BenchmarkSample(
        sample_id="S1",
        prompt="test",
        category="test",
        expected_decision="EXCLUDE_FROM_SCORING",
        expected_reason="TIMEOUT",
    )
    res = SystemRunResult(
        sample_id="S1",
        system_name="x",
        base_model="bm",
        answer="approved text",
        decision="APPROVED_FOR_SCORING",
        reason="NONE",
        scoring_allowed=True,
    )
    # Approving scoring when it should be excluded gives 0.0
    assert score_result_against_expected(res, sample) == 0.0


def test_8_summarize_ab_results_rates_and_deltas():
    # 2 samples: 1 xendris win, 1 tie
    r1 = ABComparisonResult(
        sample_id="S1", category="cat",
        deepseek_result=SystemRunResult("S1", "ds", "m", "", "APPROVED", "NONE", True, 10, 1, 1, 0.01),
        xendris_result=SystemRunResult("S1", "xe", "m", "", "APPROVED", "NONE", True, 20, 1, 1, 0.02),
        deepseek_score=0.7, xendris_score=1.0, delta_score=0.3, winner="xendris"
    )
    r2 = ABComparisonResult(
        sample_id="S2", category="cat",
        deepseek_result=SystemRunResult("S2", "ds", "m", "", "EXCLUDE", "TIMEOUT", False, 10, 1, 1, 0.01),
        xendris_result=SystemRunResult("S2", "xe", "m", "", "EXCLUDE", "TIMEOUT", False, 20, 1, 1, 0.02),
        deepseek_score=1.0, xendris_score=1.0, delta_score=0.0, winner="tie"
    )
    summary = summarize_ab_results([r1, r2])
    assert summary.total_samples == 2
    assert summary.xendris_wins == 1
    assert summary.ties == 1
    assert summary.deepseek_wins == 0
    assert summary.xendris_win_rate == 0.5
    assert summary.tie_rate == 0.5
    assert summary.average_delta == 0.15


def test_9_cost_per_valid_answer_only_uses_scoring_allowed():
    # 2 samples: 1 allowed, 1 excluded
    r1 = ABComparisonResult(
        sample_id="S1", category="cat",
        deepseek_result=SystemRunResult("S1", "ds", "m", "", "APPROVED", "NONE", True, 10, 1, 1, 1.50),
        xendris_result=SystemRunResult("S1", "xe", "m", "", "APPROVED", "NONE", True, 20, 1, 1, 2.00),
        deepseek_score=1.0, xendris_score=1.0, delta_score=0.0, winner="tie"
    )
    r2 = ABComparisonResult(
        sample_id="S2", category="cat",
        deepseek_result=SystemRunResult("S2", "ds", "m", "", "EXCLUDE", "TIMEOUT", False, 10, 1, 1, 1.50),
        xendris_result=SystemRunResult("S2", "xe", "m", "", "EXCLUDE", "TIMEOUT", False, 20, 1, 1, 2.00),
        deepseek_score=1.0, xendris_score=1.0, delta_score=0.0, winner="tie"
    )
    summary = summarize_ab_results([r1, r2])
    # Total cost of Xendris = 4.00, but only S1 is valid (1 valid). So cost per valid = 4.00
    assert summary.total_cost_xendris_usd == 4.00
    assert summary.cost_per_valid_answer_xendris == 4.00

    # Total cost of Deepseek = 3.00, only S1 is valid. Cost per valid = 3.00
    assert summary.total_cost_deepseek_usd == 3.00
    assert summary.cost_per_valid_answer_deepseek == 3.00


def test_10_jsonl_roundtrip_conserves_results():
    r = ABComparisonResult(
        sample_id="S-ROUND", category="cat",
        deepseek_result=SystemRunResult("S-ROUND", "ds", "m", "ds answer", "APPROVED", "NONE", True, 10, 1, 1, 0.01, None, "f1"),
        xendris_result=SystemRunResult("S-ROUND", "xe", "m", "xe answer", "EXCLUDE", "TIMEOUT", False, 20, 1, 1, 0.02, None, "f2"),
        deepseek_score=0.5, xendris_score=1.0, delta_score=0.5, winner="xendris"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = os.path.join(tmpdir, "results.jsonl")
        summary_path = os.path.join(tmpdir, "summary.json")

        write_ab_results_jsonl([r], jsonl_path)
        read_back = read_ab_results_jsonl(jsonl_path)

        assert len(read_back) == 1
        assert read_back[0].sample_id == "S-ROUND"
        assert read_back[0].category == "cat"
        assert read_back[0].winner == "xendris"
        assert read_back[0].deepseek_result.answer == "ds answer"
        assert read_back[0].xendris_result.answer == "xe answer"
        assert read_back[0].xendris_result.fingerprint == "f2"

        summary = summarize_ab_results([r])
        write_ab_summary_json(summary, summary_path)
        assert os.path.exists(summary_path)


def test_11_stable_fingerprints():
    # Identical run results must yield identical fingerprints
    fp1 = compute_result_fingerprint("S1", "xendris", "The answer is 42.")
    fp2 = compute_result_fingerprint("S1", "xendris", "The answer is 42.")
    assert fp1 == fp2
    assert len(fp1) == 12

    fp3 = compute_result_fingerprint("S1", "xendris", "Different answer.")
    assert fp1 != fp3


def test_12_callable_errors_logged_without_aborting():
    sample = BenchmarkSample("S-ERR", "prompt", "cat", expected_decision="APPROVED_FOR_SCORING")

    def ds_throws(s):
        raise ValueError("DeepSeek API is down!")

    def xe_throws(s):
        raise RuntimeError("Xendris crashed!")

    results = run_ab_benchmark([sample], ds_throws, xe_throws)
    assert len(results) == 1
    assert "DeepSeek API is down!" in results[0].deepseek_result.error
    assert "Xendris crashed!" in results[0].xendris_result.error
    assert results[0].winner == "tie"
    assert results[0].deepseek_score == 0.0
    assert results[0].xendris_score == 0.0
