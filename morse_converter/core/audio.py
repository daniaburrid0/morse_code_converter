import numpy as np
import sounddevice as sd
from typing import Optional, List
from dataclasses import dataclass

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

    def __init__(self, frequency: float = 800, sample_rate: int = 44100):
        """
        Initialize the AudioGenerator.

        Parameters:
            frequency (float): Frequency of the tone in Hz
            sample_rate (int): Sample rate for audio generation
        """
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.timings = MorseTimings()
        self._audio_buffer: Optional[np.ndarray] = None

    def _generate_tone(self, duration: float) -> np.ndarray:
        """Generate a sine wave tone."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        return np.sin(2 * np.pi * self.frequency * t)

    def _generate_silence(self, duration: float) -> np.ndarray:
        """Generate a period of silence."""
        return np.zeros(int(self.sample_rate * duration))

    def generate_audio(self, morse: str) -> None:
        """
        Generates audio for the given Morse code.

        Parameters:
            morse (str): The Morse code to be converted to audio.

        Raises:
            AudioError: If audio generation fails.
        """
        try:
            audio_segments: List[np.ndarray] = []
            
            for symbol in morse:
                if symbol == '.':
                    audio_segments.append(self._generate_tone(self.timings.DOT_DURATION))
                    audio_segments.append(self._generate_silence(self.timings.SYMBOL_SPACE))
                elif symbol == '-':
                    audio_segments.append(self._generate_tone(self.timings.DASH_DURATION))
                    audio_segments.append(self._generate_silence(self.timings.SYMBOL_SPACE))
                elif symbol == ' ':
                    audio_segments.append(self._generate_silence(self.timings.WORD_SPACE))

            self._audio_buffer = np.concatenate(audio_segments)
        except Exception as e:
            raise AudioError(f"Failed to generate audio: {str(e)}")

    def set_frequency(self, frequency: float) -> None:
        """Set the tone frequency."""
        if frequency <= 0:
            raise ValueError("Frequency must be positive")
        self.frequency = frequency

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
        if dot_duration is not None:
            self.timings.DOT_DURATION = dot_duration
        if dash_duration is not None:
            self.timings.DASH_DURATION = dash_duration
        if symbol_space is not None:
            self.timings.SYMBOL_SPACE = symbol_space
        if letter_space is not None:
            self.timings.LETTER_SPACE = letter_space
        if word_space is not None:
            self.timings.WORD_SPACE = word_space

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
        self.generator = generator
        self._is_playing = False

    def play_audio(self) -> None:
        """
        Plays the generated Morse code audio.

        Raises:
            AudioError: If audio playback fails.
        """
        try:
            if self.generator._audio_buffer is None:
                raise AudioError("No audio has been generated yet")

            if self._is_playing:
                raise AudioError("Audio is already playing")

            self._is_playing = True
            sd.play(self.generator._audio_buffer, self.generator.sample_rate)
            sd.wait()  # Espera hasta que termine la reproducción
            self._is_playing = False

        except Exception as e:
            self._is_playing = False
            raise AudioError(f"Failed to play audio: {str(e)}")

    def stop_audio(self) -> None:
        """Stops the current audio playback."""
        try:
            sd.stop()
            self._is_playing = False
        except Exception as e:
            raise AudioError(f"Failed to stop audio: {str(e)}")
