# morse/decoder.py

MORSE_CODE_DICT = {
    '.-': 'A',    '-...': 'B',    '-.-.': 'C',
    '-..': 'D',   '.': 'E',       '..-.': 'F',
    '--.': 'G',   '....': 'H',    '..': 'I',
    '.---': 'J',  '-.-': 'K',     '.-..': 'L',
    '--': 'M',    '-.': 'N',      '---': 'O',
    '.--.': 'P',  '--.-': 'Q',    '.-.': 'R',
    '...': 'S',   '-': 'T',       '..-': 'U',
    '...-': 'V',  '.--': 'W',     '-..-': 'X',
    '-.--': 'Y',  '--..': 'Z',
    '-----': '0', '.----': '1',   '..---': '2',
    '...--': '3', '....-': '4',   '.....': '5',
    '-....': '6', '--...': '7',   '---..': '8',
    '----.': '9',
    '/': ' ',     '.-.-.-': '.',  '--..--': ',',
    '..--..': '?', '.----.': "'", '-.-.--': '!',
    '-..-.': '/',  '-.--.': '(',  '-.--.-': ')',
    '.-...': '&',  '---...': ':',  '-.-.-.': ';',
    '-...-': '=',  '.-.-.': '+',  '-....-': '-',
    '..--.-': '_', '.-..-.': '"', '...-..-': '$',
    '.--.-.': '@'
}

# Converts Morse code to text.
def decode_from_morse(morse_code: str) -> str:
    morse_words = morse_code.split(" / ")
    decoded_message = []
    
    for word in morse_words:
        decoded_word = []
        for symbol in word.split():
            if symbol not in MORSE_CODE_DICT:
                raise ValueError(f"Unknown Morse symbol : '{symbol}'")
            decoded_word.append(MORSE_CODE_DICT[symbol])
        decoded_message.append(''.join(decoded_word))
    
    return ' '.join(decoded_message)
