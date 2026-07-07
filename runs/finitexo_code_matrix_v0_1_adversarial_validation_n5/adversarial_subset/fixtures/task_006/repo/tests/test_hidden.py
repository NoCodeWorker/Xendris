from src.solver import safe_divide

def test_safe_divide_none_items():
    result = safe_divide(None, 2)
    assert result == []

def test_safe_divide_zero_divisor():
    result = safe_divide([10, 20, 30], 0)
    assert result == []

def test_safe_divide_non_numeric():
    result = safe_divide([1, "x", 2], 2)
    assert result == [0.5, 1.0]
