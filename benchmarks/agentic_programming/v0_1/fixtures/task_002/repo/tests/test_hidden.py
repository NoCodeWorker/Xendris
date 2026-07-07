from src.solver import in_range

def test_in_range_above():
    assert in_range(20, 1, 10) is False

def test_in_range_boundary():
    assert in_range(1, 1, 10) is True
    assert in_range(10, 1, 10) is True
