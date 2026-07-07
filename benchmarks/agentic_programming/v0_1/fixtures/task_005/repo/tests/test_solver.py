from src.solver import extract_values

def test_extract_values_basic():
    data = [{"name": "Alice"}, {"name": "Bob"}]
    assert extract_values(data, "name") == ["Alice", "Bob"]

def test_extract_values_missing_key():
    data = [{"name": "Alice"}, {"age": 30}]
    assert extract_values(data, "name") == ["Alice", None]
