from src.solver import parse_entry

def test_parse_entry_basic():
    result = parse_entry("name: Alice")
    assert result == ("name", "Alice")

def test_parse_entry_numeric():
    result = parse_entry("age: 42")
    assert result == ("age", 42)
