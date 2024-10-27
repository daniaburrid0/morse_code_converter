"""
Morse Code Converter Package

Este paquete proporciona funcionalidad para convertir texto a código Morse y viceversa,
incluyendo capacidades de reproducción de audio.

Modules:
    core: Funcionalidad principal de conversión y audio
    cli: Interfaz de línea de comandos
    utils: Utilidades de logging y manejo de archivos

Example:
    >>> from morse_converter import MorseConverter
    >>> converter = MorseConverter()
    >>> morse_code = converter.text_to_morse("HELLO")
    >>> print(morse_code)
    '.... . .-.. .-.. ---'
"""

from morse_converter.core import (
    MorseConverter,
    AudioGenerator,
    AudioPlayer,
    InputValidator,
    ValidationError,
    AudioError,
    MorseTimings
)

from morse_converter.utils import (
    setup_logger,
    get_logger,
    FileHandler,
    FileOperationError,
    LoggerError
)

from morse_converter.cli.interface import (
    text_to_morse,
    morse_to_text,
    play_morse
)

# Metadata del paquete
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A Python package for converting text to Morse code and vice versa"

# Definir qué se expone cuando se hace 'from morse_converter import *'
__all__ = [
    # Core components
    'MorseConverter',
    'AudioGenerator',
    'AudioPlayer',
    'InputValidator',
    
    # Exceptions
    'ValidationError',
    'AudioError',
    'FileOperationError',
    'LoggerError',
    
    # Utilities
    'setup_logger',
    'get_logger',
    'FileHandler',
    
    # CLI functions
    'text_to_morse',
    'morse_to_text',
    'play_morse',
    
    # Configuration
    'MorseTimings',
]

# Configuración por defecto del logging
logger = setup_logger(__name__)

def get_version() -> str:
    """
    Retorna la versión actual del paquete.

    Returns:
        str: Versión del paquete
    """
    return __version__

def get_morse_converter() -> MorseConverter:
    """
    Factory function para crear una instancia de MorseConverter.

    Returns:
        MorseConverter: Nueva instancia del convertidor
    """
    return MorseConverter()

def get_audio_system() -> tuple[AudioGenerator, AudioPlayer]:
    """
    Factory function para crear el sistema de audio.

    Returns:
        tuple[AudioGenerator, AudioPlayer]: Tupla con generador y reproductor de audio
    """
    generator = AudioGenerator()
    player = AudioPlayer(generator)
    return generator, player
