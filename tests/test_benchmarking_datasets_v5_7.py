from phyng.benchmarking.datasets import load_ytrue_dataset, normalize_units, validate_ytrue_dataframe


def test_benchmarking_dataset_loader_validates_columns():
    data = load_ytrue_dataset("data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json")
    normalized = normalize_units(data)
    result = validate_ytrue_dataframe(normalized)

    assert result["row_count"] == 4
    assert result["valid"] is True
