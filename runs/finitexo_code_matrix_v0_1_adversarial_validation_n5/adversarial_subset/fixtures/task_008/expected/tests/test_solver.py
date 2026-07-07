from src.solver import get_statistics

def test_get_statistics_basic():
    result = get_statistics([1, 2, 3, 4, 5])
    assert result["mean"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 5

def test_get_statistics_single():
    result = get_statistics([42])
    assert result["mean"] == 42.0
    assert result["min"] == 42
    assert result["max"] == 42
