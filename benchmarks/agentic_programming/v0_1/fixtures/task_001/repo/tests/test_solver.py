from src.solver import count_items

def test_count_items_normal():
    assert count_items([10, 20, 30]) == 3

def test_count_items_empty():
    assert count_items([]) == 0
