from morse_converter.utils import setup_logger

# Configurar logger para este módulo
logger = setup_logger(__name__)

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
        logger.info(f"Converting text to Morse: {text}")
        try:
            if not isinstance(text, str):
                logger.error("Invalid input type: not a string")
                raise TypeError("Input must be a string")
                
            if not text:
                logger.debug("Empty input text, returning empty string")
                return ""
            
            text = text.upper()
            logger.debug(f"Normalized text: {text}")
            words = []
            current_word = []
            
            for i, char in enumerate(text):
                logger.debug(f"Processing character: {char}")
                if char == ' ':
                    if current_word:
                        words.append(' '.join(current_word))
                        current_word = []
                else:
                    if char not in self.MORSE_CODE_DICT:
                        error_msg = f"Character '{char}' is not supported in Morse code"
                        logger.error(error_msg)
                        raise ValueError(error_msg)
                    
                    morse_char = self.MORSE_CODE_DICT[char]
                    logger.debug(f"Converted '{char}' to '{morse_char}'")
                    
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
            
            result = '  '.join(words)
            logger.info(f"Conversion completed successfully: {result}")
            return result

        except Exception as e:
            logger.error(f"Text to Morse conversion failed: {str(e)}")
            raise

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
        logger.info(f"Converting Morse to text: {morse}")
        try:
            if not isinstance(morse, str):
                logger.error("Invalid input type: not a string")
                raise TypeError("Input must be a string")
                
            if not morse:
                logger.debug("Empty input Morse code, returning empty string")
                return ""
            
            # Validate Morse characters
            invalid_chars = set(morse) - {'.', '-', ' '}
            if invalid_chars:
                error_msg = f"Invalid Morse code characters: {invalid_chars}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            words = morse.split('  ')
            logger.debug(f"Split into words: {words}")
            result = []
            
            for word in words:
                chars = word.split()
                logger.debug(f"Processing word characters: {chars}")
                text_chars = []
                
                for i, char in enumerate(chars):
                    if char not in self.MORSE_TO_TEXT:
                        error_msg = f"Invalid Morse code sequence: '{char}'"
                        logger.error(error_msg)
                        raise ValueError(error_msg)
                    
                    text_char = self.MORSE_TO_TEXT[char]
                    logger.debug(f"Converted '{char}' to '{text_char}'")
                    
                    # Si es puntuación y no es el primer carácter, no agregar espacio
                    if self._is_punctuation(text_char) and text_chars:
                        text_chars[-1] = text_chars[-1] + text_char
                    else:
                        text_chars.append(text_char)
                
                result.append(''.join(text_chars))
            
            final_result = ' '.join(result)
            logger.info(f"Conversion completed successfully: {final_result}")
            return final_result

        except Exception as e:
            logger.error(f"Morse to text conversion failed: {str(e)}")
            raise
