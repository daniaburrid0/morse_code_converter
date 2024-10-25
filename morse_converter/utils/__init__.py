# Este archivo indica que el directorio utils es un paquete de Python.

"""
Morse Code Converter Utilities Package

This package contains utility modules for the Morse Code Converter application.

Modules:
    logger: Provides logging functionality for the application.
    file_handler: Provides file operations functionality.

Classes:
    LoggerError: Custom exception for logging errors.
    FileOperationError: Custom exception for file operation errors.
    FileHandler: Handles file read/write operations.
"""

from morse_converter.utils.logger import (
    setup_logger,
    get_logger,
    LoggerError,
)

from morse_converter.utils.file_handler import (
    FileHandler,
    FileOperationError,
)

__all__ = [
    # Logger exports
    'setup_logger',
    'get_logger',
    'LoggerError',
    
    # File Handler exports
    'FileHandler',
    'FileOperationError',
]
