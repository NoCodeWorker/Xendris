from src.solver import factorial
import pytest

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_large():
    assert factorial(10) == 3628800
