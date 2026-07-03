import pytest

from phyng.benchmarks import BenchmarkDataset


def test_benchmark_dataset_requires_matching_lengths():
    with pytest.raises(ValueError):
        BenchmarkDataset(
            dataset_id="BENCH-BAD",
            name="Bad",
            observable="visibility_loss",
            t=[0.0, 1.0],
            y_true=[1.0],
            provenance_type="SYNTHETIC",
            generation_method="test",
        )


def test_benchmark_dataset_accepts_synthetic_provenance():
    dataset = BenchmarkDataset(
        dataset_id="BENCH-SYN",
        name="Synthetic",
        observable="visibility_loss",
        t=[0.0],
        y_true=[1.0],
        provenance_type="SYNTHETIC",
        generation_method="deterministic test curve",
    )

    assert dataset.provenance_type == "SYNTHETIC"
