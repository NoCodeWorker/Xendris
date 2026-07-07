from src.solver import merge_configs

def test_deep_merge_multi_level():
    base = {"a": {"b": {"c": 1, "d": 2}, "e": 3}}
    override = {"a": {"b": {"c": 10}}}
    result = merge_configs(base, override, "deep")
    assert result == {"a": {"b": {"c": 10, "d": 2}, "e": 3}}

def test_default_strategy():
    base = {"app": {"theme": "light", "lang": "en"}}
    override = {"app": {"theme": "dark"}}
    result = merge_configs(base, override)
    assert result == {"app": {"theme": "dark", "lang": "en"}}

def test_does_not_mutate_base():
    base = {"nested": {"key": "original"}}
    override = {"nested": {"key": "changed", "new": "added"}}
    merge_configs(base, override, "deep")
    assert base == {"nested": {"key": "original"}}
