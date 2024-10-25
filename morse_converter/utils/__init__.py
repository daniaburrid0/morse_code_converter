# Este archivo indica que el directorio utils es un paquete de Python.

"""
Morse Code Converter Utilities Package

This package contains utility modules for the Morse Code Converter application.

Modules:
    logger: Provides logging functionality for the application.

Classes:
    LoggerError: Custom exception for logging errors.
"""

from morse_converter.utils.logger import (
    setup_logger,
    get_logger,
    LoggerError,
)

__all__ = [
    'setup_logger',
    'get_logger',
    'LoggerError',
]
