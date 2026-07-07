from src.solver import get_app_config_dir

def test_returns_string():
    result = get_app_config_dir()
    assert isinstance(result, str)

def test_ends_with_myapp():
    result = get_app_config_dir()
    assert result.endswith("myapp")
