from src.analyzer import compute_statistics
from src.validator import check_data

def test_compute_stats():
    stats = compute_statistics([1, 2, 3])
    assert stats["mean"] == 2.0
    assert stats["count"] == 3

def test_check_data():
    result = check_data([1, 2, 3])
    assert result.startswith("ok:")
