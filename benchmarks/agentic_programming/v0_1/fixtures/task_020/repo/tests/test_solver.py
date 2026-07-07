from src.solver import process_scores

def test_single_student():
    result = process_scores([("Alice", 95)])
    assert result == "Alice: 95/100"

def test_multiple_students():
    result = process_scores([("Bob", 80), ("Carol", 90)])
    assert result == "Bob: 80/100\nCarol: 90/100"
