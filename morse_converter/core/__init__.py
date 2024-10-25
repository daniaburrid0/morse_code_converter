"""
Core module for Morse Code Converter.

This module provides the main functionality for converting text to Morse code
and vice versa, along with audio generation and input validation capabilities.
"""

from .converter import MorseConverter
from .validator import InputValidator, ValidationError
from .audio import AudioGenerator, AudioPlayer, AudioError, MorseTimings

__version__ = "1.0.0"

__all__ = [
    'MorseConverter',
    'InputValidator',
    'ValidationError',
    'AudioGenerator',
    'AudioPlayer',
    'AudioError',
    'MorseTimings',
]

# Configuración por defecto
DEFAULT_AUDIO_FREQUENCY = 800  # Hz
DEFAULT_SAMPLE_RATE = 44100   # Hz

def create_converter() -> MorseConverter:
    """
    Factory function to create a preconfigured MorseConverter instance.

    Returns:
        MorseConverter: A new instance of the MorseConverter class.
    """
    return MorseConverter()

def create_audio_system(
    frequency: float = DEFAULT_AUDIO_FREQUENCY,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> tuple[AudioGenerator, AudioPlayer]:
    """
    Factory function to create preconfigured audio components.

    Parameters:
        frequency (float): The frequency to use for audio generation
        sample_rate (int): The sample rate for audio generation

    Returns:
        tuple[AudioGenerator, AudioPlayer]: A tuple containing configured
        AudioGenerator and AudioPlayer instances.
    """
    generator = AudioGenerator(frequency=frequency, sample_rate=sample_rate)
    player = AudioPlayer(generator)
    return generator, player

def create_validator() -> InputValidator:
    """
    Factory function to create a preconfigured InputValidator instance.

    Returns:
        InputValidator: A new instance of the InputValidator class.
    """
    return InputValidator()
