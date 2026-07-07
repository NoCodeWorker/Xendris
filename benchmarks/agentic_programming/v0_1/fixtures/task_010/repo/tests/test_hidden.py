from src.reporter import format_summary
from src.validator import check_data

def test_format_summary():
    result = format_summary([10, 20, 30])
    assert "avg=20.00" in result

def test_check_data_empty():
    result = check_data([])
    assert result == "empty"

def test_check_data_negative():
    result = check_data([-1, 5])
    assert result.startswith("warning:")
    assert "avg=" in result
