import pytest
from src.solver import calculate_discount

def test_over_100_percent():
    assert calculate_discount(100, 150) == 0.0

def test_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-10, 20)

def test_negative_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, -5)
