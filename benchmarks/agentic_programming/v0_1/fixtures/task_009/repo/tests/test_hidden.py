from src.solver import has_duplicates

def test_has_duplicates_empty():
    assert has_duplicates([]) is False

def test_has_duplicates_single():
    assert has_duplicates([1]) is False

def test_has_duplicates_large():
    data = list(range(500))
    data.append(250)
    assert has_duplicates(data) is True
