from src.solver import get_app_config_dir

def test_contains_home():
    result = get_app_config_dir()
    assert "~" not in result

def test_has_config_component():
    result = get_app_config_dir().replace("\\", "/")
    parts = result.split("/")
    assert ".config" in parts
