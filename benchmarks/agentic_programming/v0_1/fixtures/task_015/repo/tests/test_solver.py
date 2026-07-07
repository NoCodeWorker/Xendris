from src.solver import safe_average

def test_normal_numbers():
    assert safe_average([1, 2, 3, 4, 5]) == 3.0

def test_empty_list():
    assert safe_average([]) == 0.0
