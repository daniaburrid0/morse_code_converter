import re
from typing import Pattern
from morse_converter.utils import setup_logger

# Configurar logger para este módulo
logger = setup_logger(__name__)

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
    VALID_MORSE_PATTERN: Pattern = re.compile(r'^[.\- \s]+$')
    
    # Constantes de configuración
    MAX_INPUT_LENGTH: int = 1000
    MAX_CONSECUTIVE_SPACES: int = 1

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
        logger.info(f"Validating text input: {text}")
        try:
            if not isinstance(text, str):
                logger.error("Invalid input type: not a string")
                raise TypeError("Input must be a string")

            if not text:
                logger.error("Empty input text")
                raise ValidationError("Input text cannot be empty")

            if len(text) > self.MAX_INPUT_LENGTH:
                logger.error(f"Input length {len(text)} exceeds maximum {self.MAX_INPUT_LENGTH}")
                raise ValidationError(f"Input text exceeds maximum length of {self.MAX_INPUT_LENGTH} characters")

            if not self.VALID_TEXT_PATTERN.match(text):
                logger.error("Input contains invalid characters")
                raise ValidationError("Input contains invalid characters")

            if '  ' in text:
                logger.error("Multiple consecutive spaces detected")
                raise ValidationError("Multiple consecutive spaces are not allowed")

            logger.debug("Text input validation successful")
            return True

        except (TypeError, ValidationError) as e:
            logger.error(f"Validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during text validation: {str(e)}")
            raise ValidationError(f"Validation failed: {str(e)}")

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
        logger.info(f"Validating Morse input: {morse}")
        try:
            if not isinstance(morse, str):
                logger.error("Invalid input type: not a string")
                raise TypeError("Input must be a string")

            if not morse:
                logger.error("Empty Morse input")
                raise ValidationError("Input Morse code cannot be empty")

            if len(morse) > self.MAX_INPUT_LENGTH:
                logger.error(f"Input length {len(morse)} exceeds maximum {self.MAX_INPUT_LENGTH}")
                raise ValidationError(f"Input Morse code exceeds maximum length of {self.MAX_INPUT_LENGTH} characters")

            if not self.VALID_MORSE_PATTERN.match(morse):
                logger.error("Input contains invalid Morse characters")
                raise ValidationError("Input contains invalid Morse code characters")

            # Validar formato de código Morse
            morse_symbols = morse.split()
            logger.debug(f"Validating Morse symbols: {morse_symbols}")
            
            for symbol in morse_symbols:
                if not symbol:
                    logger.error("Multiple consecutive spaces detected")
                    raise ValidationError("Invalid Morse code format: multiple consecutive spaces")
                if len(symbol) > 7:
                    logger.error(f"Invalid symbol length: {symbol}")
                    raise ValidationError(f"Invalid Morse code symbol length: {symbol}")

            logger.debug("Morse input validation successful")
            return True

        except (TypeError, ValidationError) as e:
            logger.error(f"Validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Morse validation: {str(e)}")
            raise ValidationError(f"Validation failed: {str(e)}")
