import pytest
from morse_converter.core.converter import MorseConverter

class TestMorseConverter:
    """Test suite for MorseConverter class."""

    @pytest.fixture
    def converter(self):
        """Fixture that provides a MorseConverter instance."""
        return MorseConverter()

    # Tests para text_to_morse
    def test_text_to_morse_basic(self, converter):
        """Test basic text to Morse conversion."""
        assert converter.text_to_morse("SOS") == "... --- ..."
        assert converter.text_to_morse("HELLO") == ".... . .-.. .-.. ---"
        assert converter.text_to_morse("12345") == ".---- ..--- ...-- ....- ....."

    def test_text_to_morse_with_spaces(self, converter):
        """Test text to Morse conversion with spaces."""
        assert converter.text_to_morse("HELLO WORLD") == ".... . .-.. .-.. ---  .-- --- .-. .-.. -.."
        assert converter.text_to_morse("A B C") == ".-  -...  -.-."

    def test_text_to_morse_with_punctuation(self, converter):
        """Test text to Morse conversion with punctuation marks."""
        assert converter.text_to_morse("HI!") == ".... ..  -.-.--"
        assert converter.text_to_morse("HELLO.") == ".... . .-.. .-.. ---  .-.-.-"
        assert converter.text_to_morse("HELLO@WORLD") == ".... . .-.. .-.. ---  .--.-.  .-- --- .-. .-.. -.."

    def test_text_to_morse_case_insensitive(self, converter):
        """Test that conversion is case-insensitive."""
        assert converter.text_to_morse("hello") == ".... . .-.. .-.. ---"
        assert converter.text_to_morse("Hello") == ".... . .-.. .-.. ---"
        assert converter.text_to_morse("HELLO") == ".... . .-.. .-.. ---"

    def test_text_to_morse_empty_string(self, converter):
        """Test conversion of empty string."""
        assert converter.text_to_morse("") == ""

    def test_text_to_morse_multiple_spaces(self, converter):
        """Test handling of multiple spaces."""
        assert converter.text_to_morse("A  B") == ".-  -..."
        assert converter.text_to_morse("A   B") == ".-  -..."

    def test_text_to_morse_invalid_input(self, converter):
        """Test invalid input handling."""
        with pytest.raises(TypeError):
            converter.text_to_morse(None)
        
        with pytest.raises(TypeError):
            converter.text_to_morse(123)

        with pytest.raises(ValueError):
            converter.text_to_morse("Hello$World")

    # Tests para morse_to_text
    def test_morse_to_text_basic(self, converter):
        """Test basic Morse to text conversion."""
        assert converter.morse_to_text("... --- ...") == "SOS"
        assert converter.morse_to_text(".... . .-.. .-.. ---") == "HELLO"
        assert converter.morse_to_text(".---- ..--- ...-- ....- .....") == "12345"

    def test_morse_to_text_with_spaces(self, converter):
        """Test Morse to text conversion with word spaces."""
        assert converter.morse_to_text(".... . .-.. .-.. ---  .-- --- .-. .-.. -..") == "HELLO WORLD"
        assert converter.morse_to_text(".-  -...  -.-.") == "A B C"

    def test_morse_to_text_with_punctuation(self, converter):
        """Test Morse to text conversion with punctuation marks."""
        assert converter.morse_to_text(".... ..  -.-.--") == "HI!"
        assert converter.morse_to_text(".... . .-.. .-.. ---  .-.-.-") == "HELLO."

    def test_morse_to_text_empty_string(self, converter):
        """Test conversion of empty string."""
        assert converter.morse_to_text("") == ""

    def test_morse_to_text_invalid_input(self, converter):
        """Test invalid input handling."""
        with pytest.raises(TypeError):
            converter.morse_to_text(None)
        
        with pytest.raises(TypeError):
            converter.morse_to_text(123)

        with pytest.raises(ValueError):
            converter.morse_to_text(".... .... $$$$")

        with pytest.raises(ValueError):
            converter.morse_to_text("...---...") # Secuencia inválida

    @pytest.mark.parametrize("text,expected", [
        ("HELLO", ".... . .-.. .-.. ---"),
        ("SOS", "... --- ..."),
        ("73", "--... ...--"),
        ("HI!", ".... ..  -.-.--"),
        ("", ""),
    ])
    def test_bidirectional_conversion(self, converter, text, expected):
        """Test that conversion works bidirectionally."""
        morse = converter.text_to_morse(text)
        assert morse == expected
        assert converter.morse_to_text(morse) == text
