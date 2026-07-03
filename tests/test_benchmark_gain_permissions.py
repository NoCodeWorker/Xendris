from phyng.benchmarks import BenchmarkDataset, classify_benchmark_readiness


def test_synthetic_allows_synthetic_gain_only():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-SYN-GAIN",
        name="Synthetic gain benchmark",
        observable="visibility_loss",
        t=[0.0, 1.0],
        y_true=[1.0, 0.9],
        provenance_type="SYNTHETIC",
        generation_method="deterministic curve",
        allowed_uses=["SyntheticGain calculation"],
        forbidden_uses=["physical PredictiveGain"],
    )

    readiness = classify_benchmark_readiness(dataset)

    assert readiness.can_compute_gain is True
    assert readiness.gain_label == "SyntheticGain"
    assert readiness.allowed_claim_level == 4
    assert "physical PredictiveGain" in dataset.forbidden_uses
