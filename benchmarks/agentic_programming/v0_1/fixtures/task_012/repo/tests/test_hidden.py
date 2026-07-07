from src.solver import is_valid_user

def test_missing_username():
    assert is_valid_user("", "secret") is False

def test_both_empty():
    assert is_valid_user("", "") is False

def test_returns_boolean():
    result = is_valid_user("user", "pass")
    assert result is True or result is False
