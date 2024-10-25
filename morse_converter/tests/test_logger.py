import pytest
import logging
import os
from pathlib import Path
from morse_converter.utils.logger import setup_logger, get_logger, LoggerError

class TestLogger:
    """Test suite for logger configuration."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Fixture para limpiar los loggers después de cada test."""
        yield
        # Limpiar los handlers después de cada test
        for name in logging.root.manager.loggerDict:
            logger = logging.getLogger(name)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_setup_logger_with_file(self, tmp_path):
        """Test logger setup with file output."""
        log_file = tmp_path / "test.log"
        logger = setup_logger("test_file_logger", log_file=str(log_file))
        
        # Verificar que el archivo se crea
        assert log_file.exists()
        
        # Escribir un mensaje y verificar que se guarda
        test_message = "Test log message"
        logger.info(test_message)
        
        with open(log_file) as f:
            log_content = f.read()
            assert test_message in log_content

    def test_setup_logger_custom_level(self):
        """Test logger setup with custom level."""
        logger = setup_logger("test_level_logger", level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_setup_logger_custom_format(self):
        """Test logger setup with custom format."""
        custom_format = "%(levelname)s - %(message)s"
        logger = setup_logger("test_format_logger", log_format=custom_format)
        
        # Verificar que el formato se aplica correctamente
        handler = logger.handlers[0]
        assert handler.formatter._fmt == custom_format

    def test_setup_logger_invalid_name(self):
        """Test logger setup with invalid name."""
        with pytest.raises(ValueError):
            setup_logger("")

    def test_setup_logger_invalid_file(self):
        """Test logger setup with invalid file path."""
        # Usar una ruta inválida específica para Windows
        if os.name == 'nt':  # Windows
            invalid_path = "Z:\\invalid\\path\\test.log"  # Unidad que no existe
        else:  # Unix/Linux/Mac
            invalid_path = "/nonexistent/directory/test.log"
            
        with pytest.raises(LoggerError):
            setup_logger("test_logger", log_file=invalid_path)

    def test_get_logger_existing(self):
        """Test getting an existing logger."""
        # Crear un logger primero
        original_logger = setup_logger("test_get_logger")
        
        # Obtener el mismo logger
        retrieved_logger = get_logger("test_get_logger")
        
        assert original_logger is retrieved_logger

    def test_get_logger_new(self):
        """Test getting a new logger."""
        logger = get_logger("test_new_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_new_logger"

    def test_setup_logger_duplicate_handlers(self):
        """Test that duplicate handlers are not added."""
        logger_name = "test_duplicate_logger"
        logger1 = setup_logger(logger_name)
        initial_handlers = len(logger1.handlers)
        
        # Configurar el mismo logger de nuevo
        logger2 = setup_logger(logger_name)
        assert len(logger2.handlers) == initial_handlers
        assert logger1 is logger2
