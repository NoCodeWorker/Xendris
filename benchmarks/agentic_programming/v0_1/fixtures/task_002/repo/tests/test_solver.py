from src.solver import in_range

def test_in_range_within():
    assert in_range(5, 1, 10) is True

def test_in_range_below():
    assert in_range(0, 1, 10) is False
