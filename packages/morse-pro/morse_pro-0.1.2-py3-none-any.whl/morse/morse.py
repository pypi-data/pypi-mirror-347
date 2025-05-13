# morse/morse.py

from morse.encoder import encode_to_morse
from morse.decoder import decode_from_morse

def main():
    action = input("Do you want to encode (1) or decode (2) a message?")

    if action == '1':
        text = input("Enter the text to encode: ")
        encoded = encode_to_morse(text)
        print(f"Morse message: {encoded}")
    
    elif action == '2':
        morse_code = input("Enter the Morse code to decode: ")
        try:
            decoded = decode_from_morse(morse_code)
            print(f"Decoded message: {decoded}")
        except ValueError as e:
            print(e)
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
