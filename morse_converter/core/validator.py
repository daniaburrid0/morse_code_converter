import re
from typing import Pattern

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class InputValidator:
    """
    Ensures input integrity and format compliance for Morse code conversion.

    Methods:
        validate_text_input(text: str) -> bool
            Validates the text input for conversion.
        
        validate_morse_input(morse: str) -> bool
            Validates the Morse code input for conversion.
    """

    # Patrones de validación
    VALID_TEXT_PATTERN: Pattern = re.compile(r'^[A-Za-z0-9\s.,?!@]+$')
    # Corregimos el patrón Morse agregando los caracteres entre corchetes
    VALID_MORSE_PATTERN: Pattern = re.compile(r'^[.\- \s]+$')
    
    # Constantes de configuración
    MAX_INPUT_LENGTH: int = 1000  # Límite razonable para el input
    MAX_CONSECUTIVE_SPACES: int = 1  # Máximo de espacios consecutivos permitidos

    def validate_text_input(self, text: str) -> bool:
        """
        Validates the text input for conversion.

        Parameters:
            text (str): The text input to validate.

        Returns:
            bool: True if the input is valid, False otherwise.

        Raises:
            ValidationError: If the input text is invalid.
            TypeError: If input is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        if not text:
            raise ValidationError("Input text cannot be empty")

        if len(text) > self.MAX_INPUT_LENGTH:
            raise ValidationError(f"Input text exceeds maximum length of {self.MAX_INPUT_LENGTH} characters")

        if not self.VALID_TEXT_PATTERN.match(text):
            raise ValidationError("Input contains invalid characters")

        if '  ' in text:  # Verificar espacios consecutivos
            raise ValidationError("Multiple consecutive spaces are not allowed")

        return True

    def validate_morse_input(self, morse: str) -> bool:
        """
        Validates the Morse code input for conversion.

        Parameters:
            morse (str): The Morse code input to validate.

        Returns:
            bool: True if the input is valid, False otherwise.

        Raises:
            ValidationError: If the input Morse code is invalid.
            TypeError: If input is not a string.
        """
        if not isinstance(morse, str):
            raise TypeError("Input must be a string")

        if not morse:
            raise ValidationError("Input Morse code cannot be empty")

        if len(morse) > self.MAX_INPUT_LENGTH:
            raise ValidationError(f"Input Morse code exceeds maximum length of {self.MAX_INPUT_LENGTH} characters")

        if not self.VALID_MORSE_PATTERN.match(morse):
            raise ValidationError("Input contains invalid Morse code characters")

        # Validar formato de código Morse
        morse_symbols = morse.split()
        for symbol in morse_symbols:
            if not symbol:  # Espacios múltiples
                raise ValidationError("Invalid Morse code format: multiple consecutive spaces")
            if len(symbol) > 7:  # Longitud máxima razonable para un símbolo Morse
                raise ValidationError(f"Invalid Morse code symbol length: {symbol}")

        return True
