# tests/test_decoder.py

import pytest
from morse.decoder import decode_from_morse

def test_decode_simple_word():
    assert decode_from_morse(".... . .-.. .-.. ---") == "HELLO"

def test_decode_phrase_with_space():
    assert decode_from_morse(".... . .-.. .-.. --- / .-- --- .-. .-.. -..") == "HELLO WORLD"

def test_decode_numbers():
    assert decode_from_morse("- .... . .-. . / .. ... / .... --- .-- / - .... .- -") == "THERE IS HOW THAT"

def test_decode_with_symbols():
    assert decode_from_morse(".-.-.- / --..-- / ..--..") == ". , ?"

def test_decode_with_unsupported_char():
    with pytest.raises(ValueError, match="Unknown Morse symbol"):
        decode_from_morse(".... . .-.. .-.. --- / .-- --- .-. .-.. -.. €")
