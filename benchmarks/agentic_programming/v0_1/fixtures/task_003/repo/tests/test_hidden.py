from src.solver import parse_entry

def test_parse_entry_float():
    result = parse_entry("price: 3.14")
    assert result == ("price", 3.14)

def test_parse_entry_malformed():
    assert parse_entry("invalid") is None
    assert parse_entry("") is None
