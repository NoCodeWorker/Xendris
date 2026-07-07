from src.solver import evaluate_expression

def test_addition():
    assert evaluate_expression("2+2") == 4

def test_complex_expression():
    assert evaluate_expression("(3+5)*2") == 16

def test_division():
    assert evaluate_expression("10/2") == 5.0
