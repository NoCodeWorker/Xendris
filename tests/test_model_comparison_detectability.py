from phyng.model_comparison.detectability import classify_detectability


def test_detectability_requires_epsilon():
    assert classify_detectability(1e-7, None) == "DETECTABILITY_REQUIRES_EPSILON"


def test_delta_below_epsilon_is_undetectable():
    assert classify_detectability(1e-9, 1e-6) == "UNDETECTABLE_DIFFERENCE"


def test_delta_above_epsilon_is_detectable_toy_only():
    assert classify_detectability(1e-3, 1e-6) == "DETECTABLE_TOY_DIFFERENCE"
