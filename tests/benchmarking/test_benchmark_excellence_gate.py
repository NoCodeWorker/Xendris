from xendris.benchmarking import (
    BenchmarkExcellenceDecision,
    BenchmarkExcellenceIssueSeverity,
    assess_benchmark_excellence,
)


def _complete_summary() -> dict[str, object]:
    return {
        "metadata": {
            "dataset_hash": "a" * 64,
            "dataset_hash_algorithm": "sha256",
            "dataset_name": "Trust Traps v0.1 closed dataset",
            "dataset_version": "0.1",
            "execution_mode": "real-provider",
            "external_data_disclosure": "Only benchmark prompts are sent to the provider.",
            "max_tokens": 1024,
            "model": "deepseek-chat",
            "pricing_assumptions": "Provider-reported token pricing.",
            "provider": "deepseek",
            "python_version": "3.11.9",
            "run_date": "2026-07-06",
            "temperature": 0.0,
            "xendris_version": "0.2.0",
        },
        "total_samples": 100,
        "average_score_deepseek": 0.1,
        "average_score_xendris": 0.9,
        "average_delta": 0.8,
        "average_latency_deepseek_ms": 100.0,
        "average_latency_xendris_ms": 110.0,
        "total_cost_deepseek_usd": 0.01,
        "total_cost_xendris_usd": 0.012,
    }


def _complete_report() -> str:
    return """# Report

## No Universal Superiority Warning

This benchmark does not imply universal model superiority.

## Limitations

This is a closed dataset and benchmark-local result only.
"""


def _codes(assessment) -> set[str]:
    return {issue.code for issue in assessment.issues}


def test_1_complete_assessment_returns_ready_for_interpretation():
    assessment = assess_benchmark_excellence(_complete_summary(), _complete_report())

    assert assessment.decision == BenchmarkExcellenceDecision.READY_FOR_INTERPRETATION
    assert assessment.has_blockers is False
    assert assessment.has_warnings is False


def test_2_missing_dataset_hash_blocks():
    summary = _complete_summary()
    summary["metadata"] = {**summary["metadata"], "dataset_hash": ""}

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_dataset_hash" in _codes(assessment)
    assert assessment.has_blockers is True


def test_3_missing_execution_mode_blocks():
    summary = _complete_summary()
    summary["metadata"] = {key: value for key, value in summary["metadata"].items() if key != "execution_mode"}

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_execution_mode" in _codes(assessment)
    assert assessment.decision == BenchmarkExcellenceDecision.BLOCKED_FOR_INTERPRETATION


def test_4_invalid_total_sample_count_blocks():
    summary = _complete_summary()
    summary["total_samples"] = 0

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "invalid_total_sample_count" in _codes(assessment)


def test_5_missing_score_pair_blocks():
    summary = _complete_summary()
    summary.pop("average_score_deepseek")
    summary.pop("average_score_xendris")

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_comparable_score_pair" in _codes(assessment)


def test_6_missing_average_delta_blocks():
    summary = _complete_summary()
    summary.pop("average_delta")

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_average_delta" in _codes(assessment)


def test_7_missing_no_universal_superiority_warning_blocks():
    report = "## Limitations\n\nClosed dataset only."

    assessment = assess_benchmark_excellence(_complete_summary(), report)

    assert "missing_no_universal_superiority_warning" in _codes(assessment)


def test_8_missing_limitations_section_blocks():
    report = "No Universal Superiority Warning: this does not imply universal superiority."

    assessment = assess_benchmark_excellence(_complete_summary(), report)

    assert "missing_limitations_section" in _codes(assessment)


def test_9_dry_run_with_real_performance_claim_blocks():
    summary = _complete_summary()
    summary["metadata"] = {**summary["metadata"], "execution_mode": "DRY_RUN"}
    report = _complete_report() + "\nThis real provider run proves DeepSeek performance."

    assessment = assess_benchmark_excellence(summary, report)

    assert "dry_run_report_claims_real_provider_performance" in _codes(assessment)


def test_10_dry_run_correct_adds_note():
    summary = _complete_summary()
    summary["metadata"] = {**summary["metadata"], "execution_mode": "DRY_RUN"}

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "dry_run_result" in _codes(assessment)
    assert any(issue.severity == BenchmarkExcellenceIssueSeverity.NOTE for issue in assessment.notes)


def test_11_missing_cost_produces_warning():
    summary = _complete_summary()
    summary.pop("total_cost_deepseek_usd")
    summary.pop("total_cost_xendris_usd")

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_cost_metrics" in _codes(assessment)
    assert assessment.has_warnings is True


def test_12_missing_latency_produces_warning():
    summary = _complete_summary()
    summary.pop("average_latency_deepseek_ms")
    summary.pop("average_latency_xendris_ms")

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "missing_latency_metrics" in _codes(assessment)
    assert assessment.has_warnings is True


def test_13_cost_claim_without_cost_metrics_blocks():
    summary = _complete_summary()
    summary.pop("total_cost_deepseek_usd")
    summary.pop("total_cost_xendris_usd")
    report = _complete_report() + "\nCost is lower than baseline."

    assessment = assess_benchmark_excellence(summary, report)

    assert "missing_cost_metrics" in _codes(assessment)
    assert assessment.has_blockers is True


def test_14_latency_claim_without_latency_metrics_blocks():
    summary = _complete_summary()
    summary.pop("average_latency_deepseek_ms")
    summary.pop("average_latency_xendris_ms")
    report = _complete_report() + "\nLatency is lower than baseline."

    assessment = assess_benchmark_excellence(summary, report)

    assert "missing_latency_metrics" in _codes(assessment)
    assert assessment.has_blockers is True


def test_15_real_provider_run_without_provider_name_blocks():
    summary = _complete_summary()
    summary["metadata"] = {key: value for key, value in summary["metadata"].items() if key != "provider"}

    assessment = assess_benchmark_excellence(summary, _complete_report())

    assert "real_provider_run_missing_provider_name" in _codes(assessment)


def test_16_to_dict_serializes_correctly():
    assessment = assess_benchmark_excellence(_complete_summary(), _complete_report())
    payload = assessment.to_dict()

    assert payload["decision"] == "READY_FOR_INTERPRETATION"
    assert isinstance(payload["issues"], list)
    assert payload["has_blockers"] is False


def test_17_has_blockers_and_has_warnings_work():
    warning_summary = _complete_summary()
    warning_summary["metadata"] = {key: value for key, value in warning_summary["metadata"].items() if key != "python_version"}
    blocked_summary = _complete_summary()
    blocked_summary["total_samples"] = 0

    warning_assessment = assess_benchmark_excellence(warning_summary, _complete_report())
    blocked_assessment = assess_benchmark_excellence(blocked_summary, _complete_report())

    assert warning_assessment.has_warnings is True
    assert warning_assessment.has_blockers is False
    assert blocked_assessment.has_blockers is True


def test_18_public_export_from_xendris_benchmarking_works():
    assert BenchmarkExcellenceDecision.READY_FOR_INTERPRETATION.value == "READY_FOR_INTERPRETATION"
    assert BenchmarkExcellenceIssueSeverity.BLOCKER.value == "BLOCKER"
    assert callable(assess_benchmark_excellence)
