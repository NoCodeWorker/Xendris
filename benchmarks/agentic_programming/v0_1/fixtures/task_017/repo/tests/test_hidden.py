import pytest
from src.solver import evaluate_expression

def test_malicious_import():
    with pytest.raises((ValueError, SyntaxError, NameError)):
        evaluate_expression("__import__('os').system('echo hacked')")

def test_subtraction():
    assert evaluate_expression("100-25") == 75

def test_mixed_operators():
    assert evaluate_expression("2*3+4*5") == 26
