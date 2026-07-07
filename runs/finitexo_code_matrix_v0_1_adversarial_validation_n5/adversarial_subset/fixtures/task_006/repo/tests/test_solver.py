from src.solver import safe_divide

def test_safe_divide_basic():
    assert safe_divide([10, 20, 30], 2) == [5.0, 10.0, 15.0]

def test_safe_divide_empty():
    assert safe_divide([], 5) == []
