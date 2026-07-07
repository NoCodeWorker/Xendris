from src.solver import DataAnalyzer

def test_analyze_mean():
    da = DataAnalyzer()
    result = da.analyze([1, 2, 3, 4, 5])
    assert result == 3.0

def test_analyze_sum():
    da = DataAnalyzer()
    result = da.analyze([1, 2, 3, 4, 5], method="sum")
    assert result == 15
