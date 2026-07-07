from src.solver import echo_message

def test_basic_echo():
    assert echo_message("hello") == "hello"

def test_multiple_words():
    assert echo_message("hello world") == "hello world"
