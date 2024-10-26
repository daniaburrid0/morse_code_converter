# Este archivo indica que el directorio cli es un paquete de Python.

"""
Morse Code Converter CLI Package.

Este módulo proporciona la interfaz de línea de comandos para el conversor de código Morse.
Expone las funciones principales y el punto de entrada de la aplicación.

Functions:
    text_to_morse: Convierte texto a código Morse
    morse_to_text: Convierte código Morse a texto
    play_morse: Reproduce código Morse como audio
    main: Punto de entrada principal de la aplicación
    load_config: Carga la configuración desde archivo JSON
    validate_frequency: Valida el rango de frecuencia de audio

Types:
    Dict[str, Any]: Tipo para la configuración
"""

from morse_converter.cli.interface import (
    app,
    text_to_morse,
    morse_to_text,
    play_morse,
    main,
    load_config,
    validate_frequency,
    config
)

__version__ = "1.0.0"

__all__ = [
    'app',
    'text_to_morse',
    'morse_to_text',
    'play_morse',
    'main',
    'load_config',
    'validate_frequency',
    'config'
]
