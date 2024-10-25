class MorseConverter:
    """
    Main conversion engine for text-to-Morse and Morse-to-text operations.

    Methods:
        text_to_morse(text: str) -> str
            Converts plain text to Morse code.
        
        morse_to_text(morse: str) -> str
            Converts Morse code to plain text.
    """
    # Dictionary to store the Morse code for each letter
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.', ' ': ' ',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
        '@': '.--.-.'
    }
    
    # Crear diccionario inverso para la conversión de Morse a texto
    MORSE_TO_TEXT = {value: key for key, value in MORSE_CODE_DICT.items()}

    def text_to_morse(self, text: str) -> str:
        """
        Converts plain text to Morse code.

        Parameters:
            text (str): The text to be converted to Morse code.

        Returns:
            str: The Morse code representation of the input text.

        Raises:
            TypeError: If input is not a string
            ValueError: If the input text contains unsupported characters.
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
            
        if not text:
            return ""
        
        text = ' '.join(text.split())  # Normalize spaces
        text = text.upper()
        
        def convert_char(char: str) -> str:
            if char not in self.MORSE_CODE_DICT:
                raise ValueError(f"Character '{char}' is not supported in Morse code")
            return self.MORSE_CODE_DICT[char]
        
        return ' '.join(convert_char(char) for char in text)

    def morse_to_text(self, morse: str) -> str:
        """
        Converts Morse code to plain text.

        Parameters:
            morse (str): The Morse code to be converted to text.

        Returns:
            str: The plain text representation of the input Morse code.

        Raises:
            TypeError: If input is not a string
            ValueError: If the input Morse code is invalid.
        """
        if not isinstance(morse, str):
            raise TypeError("Input must be a string")
            
        if not morse:
            return ""
        
        # Validate Morse characters
        invalid_chars = set(morse) - {'.', '-', ' '}
        if invalid_chars:
            raise ValueError(f"Invalid Morse code characters: {invalid_chars}")
        
        # Handle multiple spaces and split
        morse_chars = [char for char in morse.split(' ') if char]
        
        result = []
        for char in morse_chars:
            if char not in self.MORSE_TO_TEXT:
                raise ValueError(f"Invalid Morse code sequence: '{char}'")
            result.append(self.MORSE_TO_TEXT[char])
        
        return ''.join(result)
