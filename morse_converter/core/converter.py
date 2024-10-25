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

    def _is_punctuation(self, char: str) -> bool:
        """Helper method to check if a character is punctuation."""
        return char in '.!?@,'

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
        
        text = text.upper()
        words = []
        current_word = []
        
        for i, char in enumerate(text):
            if char == ' ':
                if current_word:
                    words.append(' '.join(current_word))
                    current_word = []
            else:
                if char not in self.MORSE_CODE_DICT:
                    raise ValueError(f"Character '{char}' is not supported in Morse code")
                
                morse_char = self.MORSE_CODE_DICT[char]
                
                # Manejar puntuación
                if self._is_punctuation(char):
                    if current_word:
                        words.append(' '.join(current_word))
                        current_word = []
                    words.append(morse_char)
                else:
                    current_word.append(morse_char)
        
        # Agregar la última palabra si existe
        if current_word:
            words.append(' '.join(current_word))
        
        return '  '.join(words)

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
        
        words = morse.split('  ')
        result = []
        
        for word in words:
            chars = word.split()
            text_chars = []
            
            for i, char in enumerate(chars):
                if char not in self.MORSE_TO_TEXT:
                    raise ValueError(f"Invalid Morse code sequence: '{char}'")
                text_char = self.MORSE_TO_TEXT[char]
                
                # Si es puntuación y no es el primer carácter, no agregar espacio
                if self._is_punctuation(text_char) and text_chars:
                    text_chars[-1] = text_chars[-1] + text_char
                else:
                    text_chars.append(text_char)
            
            result.append(''.join(text_chars))
        
        return ' '.join(result)
