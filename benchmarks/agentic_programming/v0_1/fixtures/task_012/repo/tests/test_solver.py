from src.solver import is_valid_user

def test_valid_user():
    assert is_valid_user("admin", "secret") is True

def test_missing_password():
    assert is_valid_user("admin", "") is False
