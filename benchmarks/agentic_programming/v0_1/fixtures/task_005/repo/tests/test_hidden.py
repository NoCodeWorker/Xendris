from src.solver import extract_values

def test_extract_values_all_missing():
    data = [{"id": 1}, {"id": 2}]
    assert extract_values(data, "name") == [None, None]

def test_extract_values_empty():
    assert extract_values([], "key") == []
