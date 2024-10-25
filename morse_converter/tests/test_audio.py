import pytest
import numpy as np
import sounddevice as sd
from unittest.mock import Mock, patch
from morse_converter.core.audio import AudioGenerator, AudioPlayer, AudioError, MorseTimings

class TestAudioGenerator:
    """Test suite for AudioGenerator class."""

    @pytest.fixture
    def generator(self):
        """Fixture that provides an AudioGenerator instance with default settings."""
        return AudioGenerator()

    def test_init_default_values(self):
        """Test initialization with default values."""
        gen = AudioGenerator()
        assert gen.frequency == 800
        assert gen.sample_rate == 44100
        assert isinstance(gen.timings, MorseTimings)
        assert gen._audio_buffer is None

    def test_generate_tone(self, generator):
        """Test tone generation."""
        duration = 0.1
        tone = generator._generate_tone(duration)
        
        # Verificar la forma y características del tono
        expected_samples = int(generator.sample_rate * duration)
        assert len(tone) == expected_samples
        assert isinstance(tone, np.ndarray)
        assert np.max(np.abs(tone)) <= 1.0  # Verificar amplitud normalizada

    def test_generate_silence(self, generator):
        """Test silence generation."""
        duration = 0.1
        silence = generator._generate_silence(duration)
        
        # Verificar el silencio
        expected_samples = int(generator.sample_rate * duration)
        assert len(silence) == expected_samples
        assert isinstance(silence, np.ndarray)
        assert np.all(silence == 0)  # Todos los valores deben ser 0

    def test_generate_audio_basic(self, generator):
        """Test basic Morse code audio generation."""
        morse = ".-"  # Letra 'A'
        generator.generate_audio(morse)
        
        assert generator._audio_buffer is not None
        assert isinstance(generator._audio_buffer, np.ndarray)
        
        # Calcular duración esperada
        dot_duration = generator.timings.DOT_DURATION
        dash_duration = generator.timings.DASH_DURATION
        symbol_space = generator.timings.SYMBOL_SPACE
        expected_duration = dot_duration + symbol_space + dash_duration + symbol_space
        expected_samples = int(generator.sample_rate * expected_duration)
        
        assert len(generator._audio_buffer) == expected_samples

    def test_set_frequency(self, generator):
        """Test frequency setting."""
        new_freq = 1000
        generator.set_frequency(new_freq)
        assert generator.frequency == new_freq

        with pytest.raises(ValueError):
            generator.set_frequency(-100)

    def test_set_timing(self, generator):
        """Test timing configuration."""
        new_dot_duration = 0.2
        new_dash_duration = 0.4
        
        generator.set_timing(
            dot_duration=new_dot_duration,
            dash_duration=new_dash_duration
        )
        
        assert generator.timings.DOT_DURATION == new_dot_duration
        assert generator.timings.DASH_DURATION == new_dash_duration

    def test_generate_audio_error(self, generator):
        """Test error handling in audio generation."""
        with pytest.raises(AudioError):
            generator.generate_audio("invalid#morse")

class TestAudioPlayer:
    """Test suite for AudioPlayer class."""

    @pytest.fixture
    def mock_generator(self):
        """Fixture that provides a mocked AudioGenerator."""
        generator = Mock(spec=AudioGenerator)
        generator.sample_rate = 44100
        generator._audio_buffer = np.zeros(44100)  # 1 segundo de silencio
        return generator

    @pytest.fixture
    def player(self, mock_generator):
        """Fixture that provides an AudioPlayer instance with mocked generator."""
        return AudioPlayer(mock_generator)

    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_audio(self, mock_wait, mock_play, player):
        """Test audio playback."""
        player.play_audio()
        
        mock_play.assert_called_once()
        mock_wait.assert_called_once()
        assert not player._is_playing

    @patch('sounddevice.stop')
    def test_stop_audio(self, mock_stop, player):
        """Test audio stopping."""
        player.stop_audio()
        mock_stop.assert_called_once()
        assert not player._is_playing

    def test_play_without_generated_audio(self):
        """Test playing when no audio has been generated."""
        generator = AudioGenerator()
        player = AudioPlayer(generator)
        
        with pytest.raises(AudioError, match="No audio has been generated yet"):
            player.play_audio()

    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_while_playing(self, mock_wait, mock_play, player):
        """Test attempting to play while audio is already playing."""
        player._is_playing = True
        
        with pytest.raises(AudioError, match="Audio is already playing"):
            player.play_audio()

    @patch('sounddevice.stop')
    def test_stop_audio_error(self, mock_stop, player):
        """Test error handling when stopping audio."""
        mock_stop.side_effect = Exception("Test error")
        
        with pytest.raises(AudioError, match="Failed to stop audio"):
            player.stop_audio()

@pytest.mark.manual  # Marcar como test manual
class TestAudioManual:
    """Test suite for manual audio testing (actual sound output)."""

    @pytest.fixture
    def real_generator(self):
        """Fixture that provides a real AudioGenerator instance."""
        return AudioGenerator(frequency=800)

    @pytest.fixture
    def real_player(self, real_generator):
        """Fixture that provides a real AudioPlayer instance."""
        return AudioPlayer(real_generator)

    def test_play_sos(self, real_generator, real_player):
        """Test playing SOS in Morse code."""
        morse_sos = "... --- ..."  # SOS en código Morse
        real_generator.generate_audio(morse_sos)
        real_player.play_audio()

    def test_play_hello(self, real_generator, real_player):
        """Test playing 'HELLO' in Morse code."""
        morse_hello = ".... . .-.. .-.. ---"  # HELLO en código Morse
        real_generator.generate_audio(morse_hello)
        real_player.play_audio()

    def test_custom_frequency(self, real_generator, real_player):
        """Test playing with different frequencies."""
        morse_a = ".-"  # Letra A
        
        # Probar diferentes frecuencias
        frequencies = [440, 880, 1000]  # Diferentes frecuencias en Hz
        
        for freq in frequencies:
            real_generator.set_frequency(freq)
            real_generator.generate_audio(morse_a)
            real_player.play_audio()
            # Pausa entre sonidos
            import time
            time.sleep(1)

    def test_custom_timing(self, real_generator, real_player):
        """Test playing with different timing settings."""
        morse_hi = ".... .."  # HI en código Morse
        
        # Configuración normal
        real_generator.generate_audio(morse_hi)
        real_player.play_audio()
        
        # Configuración más lenta
        real_generator.set_timing(
            dot_duration=0.2,
            dash_duration=0.6,
            symbol_space=0.2
        )
        real_generator.generate_audio(morse_hi)
        real_player.play_audio()
