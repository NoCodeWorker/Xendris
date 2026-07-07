from src.solver import sum_scores

def test_negative_values():
    assert sum_scores([-1, -2, -3]) == -6

def test_mixed_values():
    assert sum_scores([0, 100, -50, 25]) == 75

def test_large_values():
    assert sum_scores([1000, 2000, 3000]) == 6000
