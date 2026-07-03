from phyng.benchmarks import BenchmarkDataset, classify_benchmark_readiness


def test_placeholder_cannot_compute_gain():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-PLACEHOLDER",
        name="Placeholder",
        observable="visibility_loss",
        t=[0.0],
        y_true=[1.0],
        provenance_type="PLACEHOLDER",
    )

    readiness = classify_benchmark_readiness(dataset)

    assert readiness.readiness_status == "NOT_A_BENCHMARK"
    assert readiness.can_compute_gain is False
    assert readiness.gain_label is None


def test_experimental_requires_source():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-EXP",
        name="Experimental without source",
        observable="visibility_loss",
        t=[0.0],
        y_true=[1.0],
        provenance_type="EXPERIMENTAL",
        uncertainty=[0.01],
    )

    readiness = classify_benchmark_readiness(dataset)

    assert readiness.can_compute_gain is False
    assert "source" in readiness.blocked_reason.lower()


def test_experimental_requires_uncertainty():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-EXP-NO-UNC",
        name="Experimental without uncertainty",
        observable="visibility_loss",
        t=[0.0],
        y_true=[1.0],
        provenance_type="EXPERIMENTAL",
        source_ids=["SRC-EXP"],
    )

    readiness = classify_benchmark_readiness(dataset)

    assert readiness.can_compute_gain is False
    assert "uncertainty" in readiness.blocked_reason.lower()


def test_literature_requires_extraction_notes():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-LIT",
        name="Literature without notes",
        observable="visibility_loss",
        t=[0.0],
        y_true=[1.0],
        provenance_type="LITERATURE_EXTRACTED",
        source_ids=["SRC-LIT"],
    )

    readiness = classify_benchmark_readiness(dataset)

    assert readiness.can_compute_gain is False
    assert readiness.readiness_status == "LITERATURE_REQUIRES_EXTRACTION_NOTES"
