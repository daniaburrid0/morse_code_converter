import pytest
import logging
from unittest.mock import Mock, patch
from morse_converter.core.converter import MorseConverter
from morse_converter.core.audio import AudioGenerator, AudioPlayer, AudioError

@patch('morse_converter.core.audio.logger')
@patch('morse_converter.core.converter.logger')
@patch('morse_converter.core.validator.logger')  # Agregamos el validator también
class TestLoggerImplementation:
    """Test suite for logger implementation in core modules."""
    
    def setup_method(self, method):
        """Setup común para todos los tests."""
        self.mock_logger = Mock(spec=logging.Logger)
        
    def setup_mocks(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Configura los mocks para cada test."""
        for mock in [mock_validator_logger, mock_converter_logger, mock_audio_logger]:
            mock.debug = self.mock_logger.debug
            mock.info = self.mock_logger.info
            mock.warning = self.mock_logger.warning
            mock.error = self.mock_logger.error

    def test_converter_text_to_morse_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging en la conversión de texto a Morse."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        converter = MorseConverter()
        test_text = "SOS"
        
        converter.text_to_morse(test_text)
        
        # Verificar llamadas al logger
        self.mock_logger.info.assert_any_call(f"Converting text to Morse: {test_text}")
        self.mock_logger.debug.assert_any_call(f"Normalized text: {test_text}")
        self.mock_logger.debug.assert_any_call("Processing character: S")
        self.mock_logger.info.assert_any_call(
            "Conversion completed successfully: ... --- ..."
        )

    def test_converter_morse_to_text_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging en la conversión de Morse a texto."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        converter = MorseConverter()
        test_morse = "... --- ..."
        
        converter.morse_to_text(test_morse)
        
        # Verificar llamadas al logger
        self.mock_logger.info.assert_any_call(f"Converting Morse to text: {test_morse}")
        self.mock_logger.debug.assert_any_call("Split into words: ['... --- ...']")
        self.mock_logger.info.assert_any_call("Conversion completed successfully: SOS")

    def test_converter_error_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging de errores en el converter."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        converter = MorseConverter()
        
        # Probar error de tipo
        with pytest.raises(TypeError):
            converter.text_to_morse(123)
        self.mock_logger.error.assert_any_call("Invalid input type: not a string")
        
        # Probar carácter inválido
        with pytest.raises(ValueError):
            converter.text_to_morse("Hello#World")
        self.mock_logger.error.assert_any_call(
            "Character '#' is not supported in Morse code"
        )

    def test_audio_generator_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging en AudioGenerator."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        generator = AudioGenerator(frequency=800)
        test_morse = ".-"
        
        # Verificar logging de inicialización
        self.mock_logger.debug.assert_any_call(
            "Initializing AudioGenerator with frequency=800Hz, sample_rate=44100Hz"
        )
        
        # Verificar logging de generación de audio
        generator.generate_audio(test_morse)
        self.mock_logger.info.assert_any_call(f"Generating audio for Morse code: {test_morse}")
        self.mock_logger.debug.assert_any_call("Generating dot tone")
        self.mock_logger.debug.assert_any_call("Generating dash tone")
        self.mock_logger.info.assert_any_call("Audio generation completed successfully")

    def test_audio_player_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging en AudioPlayer."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        generator = AudioGenerator()
        player = AudioPlayer(generator)
        
        # Verificar logging de inicialización
        self.mock_logger.debug.assert_any_call("Initializing AudioPlayer")
        
        # Verificar logging de error al intentar reproducir sin audio
        with pytest.raises(AudioError):
            player.play_audio()
        self.mock_logger.error.assert_any_call(
            "Attempted to play audio without generating it first"
        )

    def test_audio_error_logging(self, mock_validator_logger, mock_converter_logger, mock_audio_logger):
        """Test logging de errores en audio."""
        self.setup_mocks(mock_validator_logger, mock_converter_logger, mock_audio_logger)
        
        generator = AudioGenerator()
        
        # Probar error de frecuencia inválida
        with pytest.raises(ValueError):
            generator.set_frequency(-100)
        self.mock_logger.error.assert_any_call("Invalid frequency value: -100")
        
        # Probar error de reproducción sin buffer
        player = AudioPlayer(generator)
        with pytest.raises(AudioError):
            player.play_audio()
        self.mock_logger.error.assert_any_call(
            "Attempted to play audio without generating it first"
        )
