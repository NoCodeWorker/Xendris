from src.solver import factorial

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_positive():
    assert factorial(5) == 120
