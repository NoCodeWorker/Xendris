from src.solver import echo_message

def test_injection_resistant():
    msg = "hello; echo hacked"
    result = echo_message(msg)
    assert result == msg

def test_special_chars():
    msg = "hello && world"
    result = echo_message(msg)
    assert result == msg
