class InputValidator:
    """
    Ensures input integrity and format compliance for Morse code conversion.

    Methods:
        validate_text_input(text: str) -> bool
            Validates the text input for conversion.
        
        validate_morse_input(morse: str) -> bool
            Validates the Morse code input for conversion.
    """

    def validate_text_input(self, text: str) -> bool:
        """
        Validates the text input for conversion.

        Parameters:
            text (str): The text input to validate.

        Returns:
            bool: True if the input is valid, False otherwise.

        Raises:
            ValidationError: If the input text is invalid.

        Example:
            >>> validator = InputValidator()
            >>> validator.validate_text_input("SOS")
            True
        """
        pass

    def validate_morse_input(self, morse: str) -> bool:
        """
        Validates the Morse code input for conversion.

        Parameters:
            morse (str): The Morse code input to validate.

        Returns:
            bool: True if the input is valid, False otherwise.

        Raises:
            ValidationError: If the input Morse code is invalid.

        Example:
            >>> validator = InputValidator()
            >>> validator.validate_morse_input('... --- ...')
            True
        """
        pass
