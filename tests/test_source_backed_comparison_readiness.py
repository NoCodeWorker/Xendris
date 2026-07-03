from phyng.benchmarks import BenchmarkDataset
from phyng.model_comparison.source_backed import (
    SourceBackedModelSpec,
    evaluate_source_backed_comparison_readiness,
)


def _baseline(status="DIRECTLY_SUPPORTED"):
    return SourceBackedModelSpec(
        model_id="BASE",
        name="Baseline",
        model_role="BASELINE",
        formula="V_base(t)",
        source_ids=["SRC-BASE"] if status == "DIRECTLY_SUPPORTED" else [],
        support_status=status,
    )


def _candidate(status="DIRECTLY_SUPPORTED"):
    return SourceBackedModelSpec(
        model_id="CAND",
        name="Candidate",
        model_role="CANDIDATE",
        formula="V_C(t)",
        source_ids=["SRC-CAND"] if status == "DIRECTLY_SUPPORTED" else [],
        support_status=status,
    )


def _synthetic_benchmark():
    return BenchmarkDataset(
        dataset_id="BENCH-SYN",
        name="Synthetic",
        observable="visibility_loss",
        t=[0.0, 1.0],
        y_true=[1.0, 0.9],
        provenance_type="SYNTHETIC",
        generation_method="deterministic curve",
    )


def test_unsupported_baseline_blocks_physical_comparison():
    readiness = evaluate_source_backed_comparison_readiness(
        "CMP",
        _baseline("UNSUPPORTED"),
        _candidate("DIRECTLY_SUPPORTED"),
        _synthetic_benchmark(),
    )

    assert readiness.can_claim_physical_prediction is False
    assert "source-backed baseline model" in readiness.missing_requirements
    assert readiness.max_claim_level <= 3


def test_source_backed_baseline_allows_limited_comparison():
    readiness = evaluate_source_backed_comparison_readiness(
        "CMP",
        _baseline("DIRECTLY_SUPPORTED"),
        _candidate("DIRECTLY_SUPPORTED"),
        _synthetic_benchmark(),
    )

    assert readiness.can_compute_gain is True
    assert readiness.gain_label == "SyntheticGain"
    assert readiness.max_claim_level == 5
    assert readiness.can_claim_physical_prediction is False


def test_candidate_hypothesis_limits_claim_level():
    readiness = evaluate_source_backed_comparison_readiness(
        "CMP",
        _baseline("DIRECTLY_SUPPORTED"),
        _candidate("HYPOTHETICAL_CANDIDATE"),
        _synthetic_benchmark(),
    )

    assert readiness.max_claim_level == 4
    assert "direct candidate support for physical prediction" in readiness.missing_requirements


def test_reports_generated(tmp_path):
    from phyng.benchmarks import generate_benchmark_registry_report
    from phyng.evidence import default_source_requirements, generate_evidence_reports
    from phyng.model_comparison.source_backed import generate_source_backed_readiness_report

    readiness = evaluate_source_backed_comparison_readiness(
        "CMP",
        _baseline("UNSUPPORTED"),
        _candidate("HYPOTHETICAL_CANDIDATE"),
        _synthetic_benchmark(),
    )

    evidence_paths = generate_evidence_reports(default_source_requirements(), tmp_path)
    benchmark_path = generate_benchmark_registry_report([_synthetic_benchmark()], tmp_path)
    readiness_path = generate_source_backed_readiness_report(readiness, tmp_path)

    assert evidence_paths["source_requirements"].exists()
    assert benchmark_path.exists()
    assert readiness_path.exists()
