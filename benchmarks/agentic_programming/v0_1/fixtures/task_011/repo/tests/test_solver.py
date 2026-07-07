from src.solver import sum_scores

def test_empty_list():
    assert sum_scores([]) == 0

def test_single_element():
    assert sum_scores([5]) == 5

def test_multiple_elements():
    assert sum_scores([1, 2, 3, 4]) == 10
