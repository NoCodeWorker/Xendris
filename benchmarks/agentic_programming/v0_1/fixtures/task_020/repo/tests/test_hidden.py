from src.solver import process_scores

def test_empty_list():
    assert process_scores([]) == ""

def test_edge_scores():
    result = process_scores([("Zero", 0), ("Full", 100)])
    assert result == "Zero: 0/100\nFull: 100/100"

def test_long_names():
    result = process_scores([("Christopher", 88)])
    assert result == "Christopher: 88/100"
