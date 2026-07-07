from src.solver import DataAnalyzer

def test_analyze_median_odd():
    da = DataAnalyzer()
    result = da.analyze([1, 3, 3, 6, 7, 8, 9], method="median")
    assert result == 6

def test_analyze_median_even():
    da = DataAnalyzer()
    result = da.analyze([1, 2, 3, 4, 5, 6, 8, 9], method="median")
    assert result == 4.5
