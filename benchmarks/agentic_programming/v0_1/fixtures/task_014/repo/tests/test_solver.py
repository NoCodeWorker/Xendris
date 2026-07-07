from src.solver import merge_configs

def test_shallow_merge():
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = merge_configs(base, override, "shallow")
    assert result == {"a": 1, "b": 3, "c": 4}

def test_deep_merge_flat():
    base = {"x": 1, "y": 2}
    override = {"y": 3}
    result = merge_configs(base, override, "deep")
    assert result == {"x": 1, "y": 3}

def test_deep_merge_nested():
    base = {"db": {"host": "localhost", "port": 5432}}
    override = {"db": {"host": "prod-server"}}
    result = merge_configs(base, override, "deep")
    assert result == {"db": {"host": "prod-server", "port": 5432}}
