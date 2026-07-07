from src.solver import has_duplicates

def test_has_duplicates_true():
    assert has_duplicates([1, 2, 3, 2]) is True

def test_has_duplicates_false():
    assert has_duplicates([1, 2, 3, 4]) is False

def test_has_duplicates_strings():
    assert has_duplicates(["a", "b", "a"]) is True
