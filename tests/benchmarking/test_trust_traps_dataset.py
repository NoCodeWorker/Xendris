import os
import tempfile
import pytest
from xendris.benchmarking import run_ab_benchmark, summarize_ab_results, BenchmarkSample
from xendris.benchmarking.datasets import load_trust_traps_v0_1, load_benchmark_samples_jsonl
from xendris.benchmarking.ab_runner import compute_result_fingerprint
from xendris.benchmarking.export_jsonl import write_ab_results_jsonl, read_ab_results_jsonl


def test_1_load_trust_traps_v0_1_returns_100_samples():
    samples = load_trust_traps_v0_1()
    assert len(samples) == 100


def test_2_all_sample_ids_are_unique():
    samples = load_trust_traps_v0_1()
    ids = [s.sample_id for s in samples]
    assert len(ids) == len(set(ids))


def test_3_and_4_expected_categories_and_distribution():
    samples = load_trust_traps_v0_1()
    categories = [s.category for s in samples]

    expected_categories = {
        "false_truth_proxy",
        "universal_superiority",
        "user_provided_without_evidence",
        "evidence_conflict",
        "code_and_production_claims",
        "fallback_runtime_timeout",
        "normal_control",
    }

    assert set(categories) == expected_categories

    # Verify distribution
    from collections import Counter
    counts = Counter(categories)
    assert counts["false_truth_proxy"] == 20
    assert counts["universal_superiority"] == 15
    assert counts["user_provided_without_evidence"] == 15
    assert counts["evidence_conflict"] == 15
    assert counts["code_and_production_claims"] == 15
    assert counts["fallback_runtime_timeout"] == 10
    assert counts["normal_control"] == 10


def test_5_all_samples_have_non_empty_prompt():
    samples = load_trust_traps_v0_1()
    for s in samples:
        assert s.prompt is not None
        assert len(s.prompt.strip()) > 0


def test_6_all_samples_have_expected_decision():
    samples = load_trust_traps_v0_1()
    for s in samples:
        assert s.expected_decision is not None
        assert len(s.expected_decision.strip()) > 0


def test_7_expected_reason_exists_when_corresponding():
    samples = load_trust_traps_v0_1()
    for s in samples:
        if s.category != "normal_control":
            assert s.expected_reason is not None
            assert len(s.expected_reason.strip()) > 0


def test_8_loader_jsonl_roundtrip_with_benchmark_sample():
    samples = load_trust_traps_v0_1()

    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_path = os.path.join(tmpdir, "samples_test.jsonl")

        # Write samples out using custom JSONL writing (or standard json)
        import json
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for s in samples:
                serialized = {
                    "sample_id": s.sample_id,
                    "prompt": s.prompt,
                    "category": s.category,
                    "expected_decision": s.expected_decision,
                    "expected_reason": s.expected_reason,
                    "expected_answer": s.expected_answer,
                    "metadata": s.metadata,
                }
                f.write(json.dumps(serialized, ensure_ascii=False) + "\n")

        # Read back
        read_samples = load_benchmark_samples_jsonl(jsonl_path)
        assert len(read_samples) == 100
        assert read_samples[0].sample_id == samples[0].sample_id
        assert read_samples[0].prompt == samples[0].prompt


def test_9_no_unknown_categories():
    samples = load_trust_traps_v0_1()
    allowed_categories = {
        "false_truth_proxy",
        "universal_superiority",
        "user_provided_without_evidence",
        "evidence_conflict",
        "code_and_production_claims",
        "fallback_runtime_timeout",
        "normal_control",
    }
    for s in samples:
        assert s.category in allowed_categories


def test_10_normal_control_does_not_dominate_dataset():
    samples = load_trust_traps_v0_1()
    normal_count = sum(1 for s in samples if s.category == "normal_control")
    # normal_control must represent exactly 10% (10 out of 100)
    assert normal_count == 10
    assert normal_count < (len(samples) / 2)


def test_11_dataset_runnable_with_mock_callables():
    samples = load_trust_traps_v0_1()

    def mock_deepseek(s):
        # Base model always approves everything blindly
        return {
            "answer": "Yes, this is fully correct.",
            "decision": "APPROVED_FOR_SCORING",
            "reason": "NONE",
            "scoring_allowed": True,
            "latency_ms": 100,
            "estimated_cost_usd": 0.0001,
        }

    def mock_xendris(s):
        # Xendris correctly gates and excludes the traps
        if s.category == "normal_control":
            return {
                "answer": "Explicación correcta.",
                "decision": "APPROVED_FOR_SCORING",
                "reason": "NONE",
                "scoring_allowed": True,
                "latency_ms": 150,
                "estimated_cost_usd": 0.00015,
            }
        elif s.category == "evidence_conflict":
            return {
                "answer": "Conflicto detectado.",
                "decision": "HUMAN_REVIEW_REQUIRED",
                "reason": s.expected_reason,
                "scoring_allowed": False,
                "latency_ms": 150,
                "estimated_cost_usd": 0.00015,
            }
        else:
            return {
                "answer": "Excluido por seguridad.",
                "decision": "EXCLUDE_FROM_SCORING",
                "reason": s.expected_reason,
                "scoring_allowed": False,
                "latency_ms": 150,
                "estimated_cost_usd": 0.00015,
            }

    results = run_ab_benchmark(samples, mock_deepseek, mock_xendris)
    assert len(results) == 100

    summary = summarize_ab_results(results)
    assert summary.total_samples == 100
    # Xendris should win on all 90 traps, and tie on the 10 normal controls
    assert summary.xendris_wins == 90
    assert summary.ties == 10
    assert summary.deepseek_wins == 0
    assert summary.xendris_win_rate == 0.9
    assert summary.tie_rate == 0.1


def test_12_stable_fingerprints_across_runs():
    samples = load_trust_traps_v0_1()
    fp1_list = [compute_result_fingerprint(s.sample_id, "xendris", "Output text") for s in samples]
    fp2_list = [compute_result_fingerprint(s.sample_id, "xendris", "Output text") for s in samples]
    assert fp1_list == fp2_list
    assert len(fp1_list) == 100
    for fp in fp1_list:
        assert len(fp) == 12
