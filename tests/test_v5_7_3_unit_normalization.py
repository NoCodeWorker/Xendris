from phyng.targeted_ytrue.unit_normalization import normalize_visibility_value


def test_accept_requires_numeric_value_and_unit_or_dimensionless():
    value, text, unit, actions = normalize_visibility_value("visibility 38.5 %")

    assert value == 0.385
    assert text == "38.5%"
    assert unit == "dimensionless_fraction"
    assert actions


def test_statistical_error_is_not_ytrue_value():
    value, _text, _unit, _actions = normalize_visibility_value("3 %", "The statistical error amounts to ± 3 %.")

    assert value is None
