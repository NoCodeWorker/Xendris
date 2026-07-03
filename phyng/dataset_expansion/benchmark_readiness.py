"""Benchmark readiness decision for expanded dataset."""

from __future__ import annotations

from phyng.dataset_expansion.schemas import VisibilityDecoherenceDataset


def dependency_availability() -> dict:
    modules = {
        "pandas": "pandas",
        "numpy": "numpy",
        "scikit-learn": "sklearn",
        "scipy": "scipy",
        "pydantic": "pydantic",
        "pytest": "pytest",
        "matplotlib": "matplotlib",
    }
    availability = {}
    for label, module in modules.items():
        try:
            __import__(module)
            availability[label] = True
        except ModuleNotFoundError:
            availability[label] = False
    return availability


def build_benchmark_readiness(dataset: VisibilityDecoherenceDataset) -> dict:
    if dataset.accepted_ytrue_count >= 10 and dataset.source_count >= 2:
        readiness = "READY_FOR_OUT_OF_SOURCE_CONTROL"
        next_phase = "v5.8 - Multi-Source Benchmark & Out-of-Source Control Gate"
    elif dataset.accepted_ytrue_count > 0:
        readiness = "PARTIAL_N_SMALL"
        next_phase = "Targeted visibility/decoherence expansion"
    else:
        readiness = "NOT_READY_NO_YTRUE"
        next_phase = "source/figure review"
    return {
        "artifact_id": "VISIBILITY-DECOHERENCE-BENCHMARK-READINESS-v5_7",
        "readiness": readiness,
        "accepted_ytrue_count_total": dataset.accepted_ytrue_count,
        "independent_source_count": dataset.source_count,
        "out_of_source_split_possible": dataset.source_count >= 2,
        "allowed_next_phase": next_phase,
        "dependency_availability": dependency_availability(),
        "benchmarking_stack_hardened": True,
        "deep_learning_used": False,
        "physical_claim_created": False,
        "frontera_c_validated": False,
    }
