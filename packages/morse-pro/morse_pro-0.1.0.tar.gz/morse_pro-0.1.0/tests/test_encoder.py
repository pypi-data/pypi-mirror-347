# tests/test_encoder.py

import pytest
from morse.encoder import encode_to_morse


def test_encode_simple_word():
    assert encode_to_morse("sos") == "... --- ..."

def test_encode_phrase_with_space():
    assert encode_to_morse("hello world") == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

def test_encode_uppercase():
    assert encode_to_morse("HELLO") == ".... . .-.. .-.. ---"

def test_encode_with_numbers():
    assert encode_to_morse("test123") == "- . ... - .---- ..--- ...--"

def test_encode_with_symbols():
    assert encode_to_morse("wait!") == ".-- .- .. - -.-.--"

def test_encode_with_unsupported_char():
    with pytest.raises(ValueError):
        encode_to_morse("hello€")
