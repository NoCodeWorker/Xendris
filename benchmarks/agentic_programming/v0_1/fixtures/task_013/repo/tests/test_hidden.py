from src.solver import word_frequency

def test_repeated_word():
    assert word_frequency("spam spam spam spam") == {"spam": 4}

def test_case_sensitivity():
    result = word_frequency("Hello hello HELLO")
    assert result == {"Hello": 1, "hello": 1, "HELLO": 1}

def test_trailing_spaces():
    assert word_frequency("  a  b  a  ") == {"a": 2, "b": 1}
