from src.solver import word_frequency

def test_empty_string():
    assert word_frequency("") == {}

def test_single_word():
    assert word_frequency("hello") == {"hello": 1}

def test_multiple_words():
    result = word_frequency("the cat and the dog")
    assert result == {"the": 2, "cat": 1, "and": 1, "dog": 1}
