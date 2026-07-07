from src.solver import count_items

def test_count_items_single():
    assert count_items([42]) == 1

def test_count_items_many():
    data = list(range(100))
    assert count_items(data) == 100
