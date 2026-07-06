from collections import Counter

from xendris.benchmarking.programming import (
    EXPECTED_DISTRIBUTION,
    ProgrammingSample,
    load_programming_reliability_v0_1,
    read_programming_results_jsonl,
    run_programming_benchmark,
    score_programming_result,
    summarize_programming_results,
    write_programming_results_jsonl,
)
from xendris.benchmarking.programming.sandbox import extract_python_code


def _sample() -> ProgrammingSample:
    return ProgrammingSample(
        sample_id="PR-NORMAL-CONTROL-999",
        category="normal_control",
        language="python",
        prompt="Return the input unchanged.",
        starter_code="def solve(value):\n    return None\n",
        test_code="assert solve(3) == 3\n",
        expected_behavior="solve returns the input value.",
        expected_decision="INCLUDE",
        expected_reason="PASS",
        forbidden_changes=("public_signature",),
        metadata={},
    )


def _correct_callable(sample: ProgrammingSample) -> dict:
    return {
        "system_name": "fake",
        "answer": "```python\ndef solve(value):\n    return value\n```",
        "latency_ms": 10,
        "estimated_cost_usd": 0.01,
    }


def test_1_dataset_loads_exactly_100_samples():
    samples = load_programming_reliability_v0_1()

    assert len(samples) == 100


def test_2_dataset_distribution_matches_contract():
    samples = load_programming_reliability_v0_1()
    distribution = Counter(sample.category for sample in samples)

    assert dict(distribution) == EXPECTED_DISTRIBUTION


def test_3_sample_ids_are_unique():
    samples = load_programming_reliability_v0_1()
    ids = [sample.sample_id for sample in samples]

    assert len(ids) == len(set(ids))


def test_4_runner_works_with_fake_callable():
    results = run_programming_benchmark([_sample()], _correct_callable)

    assert len(results) == 1
    assert results[0].system_name == "fake"
    assert results[0].fingerprint


def test_5_correct_code_passes_tests():
    result = run_programming_benchmark([_sample()], _correct_callable)[0]

    assert result.tests_passed is True
    assert result.runtime_error is None


def test_6_runtime_error_fails_controlled():
    def bad_callable(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value):\n    return 1 / 0\n```"}

    result = run_programming_benchmark([_sample()], bad_callable)[0]

    assert result.tests_passed is False
    assert result.runtime_error is not None
    assert result.score == 0.0


def test_7_public_signature_change_breaks_contract():
    def changed_signature(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value, extra=None):\n    return value\n```"}

    result = run_programming_benchmark([_sample()], changed_signature)[0]

    assert result.contract_preserved is False
    assert result.score == 0.0


def test_8_unsafe_eval_is_security_risk():
    def unsafe_callable(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value):\n    return eval(value)\n```"}

    result = run_programming_benchmark([_sample()], unsafe_callable)[0]

    assert result.security_risk is True
    assert result.score == 0.0


def test_9_passing_few_tests_does_not_imply_production_ready():
    def overclaim_callable(sample: ProgrammingSample) -> dict:
        return {
            "answer": "```python\ndef solve(value):\n    return value\n```\nProduction ready.",
            "estimated_cost_usd": 0.01,
        }

    production_sample = ProgrammingSample(
        **{**_sample().to_dict(), "prompt": "Make this production ready."}
    )
    result = run_programming_benchmark([production_sample], overclaim_callable)[0]

    assert result.reason == "PRODUCTION_OVERCLAIM"
    assert result.score == 0.0


def test_10_score_one_for_correct_solution():
    result = run_programming_benchmark([_sample()], _correct_callable)[0]

    assert score_programming_result(result, _sample()) == 1.0


def test_11_score_zero_for_broken_contract():
    def changed_signature(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value, extra=None):\n    return value\n```"}

    result = run_programming_benchmark([_sample()], changed_signature)[0]

    assert score_programming_result(result, _sample()) == 0.0


def test_12_summary_calculates_score_by_category():
    result = run_programming_benchmark([_sample()], _correct_callable)[0]
    summary = summarize_programming_results([result])

    assert summary.score_by_category["normal_control"] == 1.0


def test_13_summary_calculates_cost_per_correct_solution():
    result = run_programming_benchmark([_sample()], _correct_callable)[0]
    summary = summarize_programming_results([result])

    assert summary.cost_per_correct_solution == 0.01


def test_14_jsonl_roundtrip_preserves_results(tmp_path):
    results = run_programming_benchmark([_sample()], _correct_callable)
    path = tmp_path / "programming-results.jsonl"

    write_programming_results_jsonl(results, path)
    loaded = read_programming_results_jsonl(path)

    assert len(loaded) == 1
    assert loaded[0].sample_id == results[0].sample_id
    assert loaded[0].fingerprint == results[0].fingerprint


def test_15_normal_control_not_degraded():
    result = run_programming_benchmark([_sample()], _correct_callable)[0]

    assert result.score == 1.0


def test_16_no_real_api_called_in_tests():
    called = {"value": False}

    def local_callable(sample: ProgrammingSample) -> dict:
        called["value"] = True
        return _correct_callable(sample)

    run_programming_benchmark([_sample()], local_callable)

    assert called["value"] is True
    assert extract_python_code(_correct_callable(_sample())["answer"]) is not None
