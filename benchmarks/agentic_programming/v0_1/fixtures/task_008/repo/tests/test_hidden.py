from src.solver import get_statistics
from src.processor import process

def test_get_statistics_basic():
    result = get_statistics([1, 2, 3, 4, 5])
    assert result["mean"] == 3.0
    assert result["min"] == 1
    assert result["max"] == 5

def test_process_after_rename():
    result = process([1, 2, 3])
    assert result["range"] == 2
