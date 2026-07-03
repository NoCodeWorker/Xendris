from phyng.benchmarking.baselines import linear_regression_baseline, sklearn_available
from phyng.benchmarking.controls import parameter_fairness, shuffled_target
from phyng.benchmarking.cross_validation import out_of_source_ready
from phyng.benchmarking.leakage import label_direct_interpolation, label_same_source_leakage


def test_sklearn_baselines_available():
    model = linear_regression_baseline([0, 1, 2], [0.0, 0.5, 1.0])

    assert isinstance(sklearn_available(), bool)
    assert model["model_id"] == "LINEAR_REGRESSION_BASELINE"
    assert len(model["prediction"]) == 3


def test_benchmarking_controls_are_available():
    assert shuffled_target([1, 2, 3], seed=1) != [1, 2, 3]
    assert parameter_fairness(2, 2)["fair_or_stricter"] is True
    assert out_of_source_ready(["a", "a"]) is False
    assert out_of_source_ready(["a", "b"]) is True
    assert label_same_source_leakage(["a", "a"]) == "HIGH"
    assert label_direct_interpolation(4, 4) == "BLOCKING"
