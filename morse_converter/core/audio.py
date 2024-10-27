import numpy as np
import sounddevice as sd
from typing import Optional, List
from dataclasses import dataclass
from morse_converter.utils import setup_logger

# Configurar logger para este módulo
logger = setup_logger(__name__)

@dataclass
class MorseTimings:
    """Timing configurations for Morse code audio."""
    DOT_DURATION: float = 0.1  # segundos
    DASH_DURATION: float = 0.3  # segundos
    SYMBOL_SPACE: float = 0.1   # espacio entre símbolos
    LETTER_SPACE: float = 0.3   # espacio entre letras
    WORD_SPACE: float = 0.7     # espacio entre palabras

class AudioError(Exception):
    """Custom exception for audio-related errors."""
    pass

class AudioGenerator:
    """
    Creates audio representations of Morse code.

    Methods:
        generate_audio(morse: str) -> None
            Generates audio for the given Morse code.
    """

    def __init__(self, frequency: int = 800, volume: float = 0.5):
        """
        Initialize the AudioGenerator.

        Parameters:
            frequency (int): The frequency in Hz for the tones (default: 800)
            volume (float): The volume level from 0.0 to 1.0 (default: 0.5)
        """
        self.frequency = frequency
        self.volume = volume
        self.sample_rate = 44100
        self.timings = MorseTimings()
        self._audio_buffer = None

    def _generate_tone(self, duration: float) -> np.ndarray:
        """Generate a sine wave tone."""
        logger.debug(f"Generating tone with duration={duration}s")
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return np.sin(2 * np.pi * self.frequency * t)

    def _generate_silence(self, duration: float) -> np.ndarray:
        """Generate a period of silence."""
        logger.debug(f"Generating silence with duration={duration}s")
        return np.zeros(int(self.sample_rate * duration))

    def generate_audio(self, morse: str) -> None:
        """
        Generates audio for the given Morse code.

        Parameters:
            morse (str): The Morse code to be converted to audio.

        Raises:
            AudioError: If audio generation fails.
        """
        logger.info(f"Generating audio for Morse code: {morse}")
        try:
            audio_segments: List[np.ndarray] = []
            
            for symbol in morse:
                if symbol == '.':
                    logger.debug("Generating dot tone")
                    audio_segments.append(self._generate_tone(self.timings.DOT_DURATION))
                    audio_segments.append(self._generate_silence(self.timings.SYMBOL_SPACE))
                elif symbol == '-':
                    logger.debug("Generating dash tone")
                    audio_segments.append(self._generate_tone(self.timings.DASH_DURATION))
                    audio_segments.append(self._generate_silence(self.timings.SYMBOL_SPACE))
                elif symbol == ' ':
                    logger.debug("Generating word space")
                    audio_segments.append(self._generate_silence(self.timings.WORD_SPACE))
                else:
                    logger.warning(f"Ignoring invalid symbol: {symbol}")

            self._audio_buffer = np.concatenate(audio_segments)
            logger.info("Audio generation completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to generate audio: {str(e)}")
            raise AudioError(f"Failed to generate audio: {str(e)}")

    def set_frequency(self, frequency: float) -> None:
        """Set the tone frequency."""
        logger.info(f"Setting frequency to {frequency}Hz")
        if frequency <= 0:
            logger.error(f"Invalid frequency value: {frequency}")
            raise ValueError("Frequency must be positive")
        self.frequency = frequency
        logger.debug("Frequency updated successfully")

    def set_timing(self, 
                  dot_duration: Optional[float] = None,
                  dash_duration: Optional[float] = None,
                  symbol_space: Optional[float] = None,
                  letter_space: Optional[float] = None,
                  word_space: Optional[float] = None) -> None:
        """
        Update timing configurations.

        Parameters:
            dot_duration (float): Duration of a dot
            dash_duration (float): Duration of a dash
            symbol_space (float): Space between symbols
            letter_space (float): Space between letters
            word_space (float): Space between words
        """
        logger.info("Updating timing configurations")
        if dot_duration is not None:
            logger.debug(f"Setting dot duration to {dot_duration}s")
            self.timings.DOT_DURATION = dot_duration
        if dash_duration is not None:
            logger.debug(f"Setting dash duration to {dash_duration}s")
            self.timings.DASH_DURATION = dash_duration
        if symbol_space is not None:
            logger.debug(f"Setting symbol space to {symbol_space}s")
            self.timings.SYMBOL_SPACE = symbol_space
        if letter_space is not None:
            logger.debug(f"Setting letter space to {letter_space}s")
            self.timings.LETTER_SPACE = letter_space
        if word_space is not None:
            logger.debug(f"Setting word space to {word_space}s")
            self.timings.WORD_SPACE = word_space
        logger.info("Timing configurations updated successfully")

class AudioPlayer:
    """
    Manages playback operations for Morse code audio.

    Methods:
        play_audio() -> None
            Plays the generated Morse code audio.
        stop_audio() -> None
            Stops the current audio playback.
    """

    def __init__(self, generator: AudioGenerator):
        """
        Initialize the AudioPlayer.

        Parameters:
            generator (AudioGenerator): The audio generator instance to use for playback
        """
        logger.debug("Initializing AudioPlayer")
        self.generator = generator
        self._is_playing = False
        logger.debug("AudioPlayer initialized successfully")

    def play_audio(self) -> None:
        """
        Plays the generated Morse code audio.

        Raises:
            AudioError: If audio playback fails.
        """
        try:
            if self.generator._audio_buffer is None:
                logger.error("Attempted to play audio without generating it first")
                raise AudioError("No audio has been generated yet")

            if self._is_playing:
                logger.warning("Attempted to play audio while already playing")
                raise AudioError("Audio is already playing")

            logger.info("Starting audio playback")
            self._is_playing = True
            sd.play(self.generator._audio_buffer, self.generator.sample_rate)
            sd.wait()  # Espera hasta que termine la reproducción
            self._is_playing = False
            logger.info("Audio playback completed successfully")

        except Exception as e:
            self._is_playing = False
            logger.error(f"Audio playback failed: {str(e)}")
            raise AudioError(f"Failed to play audio: {str(e)}")

    def stop_audio(self) -> None:
        """Stops the current audio playback."""
        try:
            logger.info("Stopping audio playback")
            sd.stop()
            self._is_playing = False
            logger.info("Audio playback stopped successfully")
        except Exception as e:
            logger.error(f"Failed to stop audio: {str(e)}")
            raise AudioError(f"Failed to stop audio: {str(e)}")
