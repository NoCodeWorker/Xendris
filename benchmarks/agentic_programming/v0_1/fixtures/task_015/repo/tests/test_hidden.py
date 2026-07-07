from src.solver import safe_average

def test_with_none_values():
    assert safe_average([1, None, 3, None, 5]) == 3.0

def test_single_element():
    assert safe_average([10]) == 10.0

def test_all_none():
    assert safe_average([None, None]) == 0.0
