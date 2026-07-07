from src.solver import calculate_discount

def test_no_discount():
    assert calculate_discount(100, 0) == 100.0

def test_half_off():
    assert calculate_discount(100, 50) == 50.0

def test_small_discount():
    assert calculate_discount(200, 10) == 180.0
