import logging
import os
from pathlib import Path
from typing import Optional

class LoggerError(Exception):
    """Custom exception for logger configuration errors."""
    pass

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Sets up a logger with the specified configuration.

    Parameters:
        name (str): The name of the logger.
        level (int): The logging level (default: logging.INFO).
        log_file (str, optional): Path to the log file. If None, logs to console only.
        log_format (str, optional): Custom format for log messages.

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        LoggerError: If logger configuration fails.
        ValueError: If invalid parameters are provided.

    Example:
        >>> logger = setup_logger("morse_converter")
        >>> logger.info("Application started")
        >>> logger.error("An error occurred")
    """
    if not name:
        raise ValueError("Logger name cannot be empty")

    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    try:
        # Formato por defecto
        if log_format is None:
            log_format = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(message)s"
            )

        formatter = logging.Formatter(log_format)

        # Configurar handler de consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Configurar handler de archivo si se especifica
        if log_file:
            try:
                log_path = Path(log_file)
                
                # Verificar si la unidad existe (específico para Windows)
                if os.name == 'nt':  # Windows
                    drive = os.path.splitdrive(str(log_path))[0]
                    if drive and not os.path.exists(drive):
                        raise LoggerError(f"Drive does not exist: {drive}")

                log_dir = log_path.parent

                # Verificar si el directorio es accesible
                try:
                    if not log_dir.exists():
                        log_dir.mkdir(parents=True, exist_ok=True)
                except (PermissionError, OSError) as e:
                    raise LoggerError(f"Cannot create or access log directory: {str(e)}")

                # Intentar crear/acceder al archivo
                try:
                    file_handler = logging.FileHandler(str(log_path))
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                except (PermissionError, OSError) as e:
                    raise LoggerError(f"Cannot create or access log file: {str(e)}")

            except Exception as e:
                raise LoggerError(f"Failed to configure log file: {str(e)}")

        return logger

    except Exception as e:
        raise LoggerError(f"Failed to configure logger: {str(e)}")

def get_logger(name: str) -> logging.Logger:
    """
    Gets an existing logger or creates a new one with default configuration.

    Parameters:
        name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: The requested logger instance.

    Example:
        >>> logger = get_logger("morse_converter")
        >>> logger.info("Using existing logger")
    """
    logger = logging.getLogger(name)
    
    # Si el logger no tiene handlers, configurarlo con valores por defecto
    if not logger.handlers:
        return setup_logger(name)
    
    return logger
