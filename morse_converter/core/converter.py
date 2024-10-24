class MorseConverter:
    """
    Main conversion engine for text-to-Morse and Morse-to-text operations.

    Methods:
        text_to_morse(text: str) -> str
            Converts plain text to Morse code.
        
        morse_to_text(morse: str) -> str
            Converts Morse code to plain text.
    """

    def text_to_morse(self, text: str) -> str:
        """
        Converts plain text to Morse code.

        Parameters:
            text (str): The text to be converted to Morse code.

        Returns:
            str: The Morse code representation of the input text.

        Raises:
            ValueError: If the input text contains unsupported characters.

        Example:
            >>> converter = MorseConverter()
            >>> converter.text_to_morse("SOS")
            '... --- ...'
        """
        pass

    def morse_to_text(self, morse: str) -> str:
        """
        Converts Morse code to plain text.

        Parameters:
            morse (str): The Morse code to be converted to text.

        Returns:
            str: The plain text representation of the input Morse code.

        Raises:
            ValueError: If the input Morse code is invalid.

        Example:
            >>> converter = MorseConverter()
            >>> converter.morse_to_text('... --- ...')
            'SOS'
        """
        pass
