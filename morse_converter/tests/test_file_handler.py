import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from morse_converter.utils import FileHandler, FileOperationError

class TestFileHandler:
    """Test suite for FileHandler class."""

    @pytest.fixture
    def file_handler(self):
        """Fixture que proporciona una instancia de FileHandler."""
        return FileHandler()

    @pytest.fixture
    def mock_logger(self):
        """Fixture que proporciona un logger mockeado."""
        with patch('morse_converter.utils.file_handler.logger') as mock:
            yield mock

    def test_read_file_success(self, file_handler, tmp_path, mock_logger):
        """Test de lectura exitosa de archivo."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        content = file_handler.read_file(str(test_file))

        assert content == test_content
        mock_logger.info.assert_called_with(f"Attempting to read file: {test_file}")
        mock_logger.debug.assert_called_with(
            f"Successfully read {len(test_content)} characters from {test_file}"
        )

    def test_write_file_success(self, file_handler, tmp_path, mock_logger):
        """Test de escritura exitosa de archivo."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"

        file_handler.write_file(str(test_file), test_content)

        assert test_file.exists()
        assert test_file.read_text() == test_content
        mock_logger.info.assert_called_with(f"Attempting to write to file: {test_file}")
        mock_logger.debug.assert_called_with(
            f"Successfully wrote {len(test_content)} characters to {test_file}"
        )

    def test_read_file_not_found(self, file_handler, mock_logger):
        """Test de manejo de archivo inexistente."""
        non_existent_file = "non_existent.txt"
        
        with pytest.raises(FileOperationError) as exc_info:
            file_handler.read_file(non_existent_file)
        
        assert str(exc_info.value) == f"File not found: {non_existent_file}"
        mock_logger.error.assert_called_with(f"File not found: {non_existent_file}")

    def test_read_file_not_file(self, file_handler, tmp_path, mock_logger):
        """Test de manejo de ruta que no es archivo."""
        with pytest.raises(FileOperationError) as exc_info:
            file_handler.read_file(str(tmp_path))
        
        assert str(exc_info.value) == f"Path is not a file: {tmp_path}"
        mock_logger.error.assert_called_with(f"Path is not a file: {tmp_path}")

    def test_write_file_permission_error(self, file_handler, tmp_path, mock_logger):
        """Test de manejo de error de permisos."""
        test_file = tmp_path / "test.txt"
        
        with patch('pathlib.Path.open') as mock_open:
            mock_open.side_effect = PermissionError("Permission denied")
            
            with pytest.raises(FileOperationError) as exc_info:
                file_handler.write_file(str(test_file), "test content")
        
        assert "Permission denied" in str(exc_info.value)
        mock_logger.error.assert_called_with(
            f"Error writing to file {test_file}: Permission denied"
        )

    def test_write_file_creates_directories(self, file_handler, tmp_path, mock_logger):
        """Test de creación automática de directorios."""
        test_file = tmp_path / "subdir" / "test.txt"
        test_content = "Test content"

        file_handler.write_file(str(test_file), test_content)

        assert test_file.exists()
        assert test_file.read_text() == test_content
        mock_logger.debug.assert_called_with(
            f"Successfully wrote {len(test_content)} characters to {test_file}"
        )

    def test_read_file_encoding(self, file_handler, tmp_path, mock_logger):
        """Test de manejo de codificación."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, 世界!"  # Contenido con caracteres Unicode
        test_file.write_text(test_content, encoding='utf-8')

        content = file_handler.read_file(str(test_file))

        assert content == test_content
        mock_logger.debug.assert_called_with(
            f"Successfully read {len(test_content)} characters from {test_file}"
        )

    def test_write_file_encoding(self, file_handler, tmp_path, mock_logger):
        """Test de escritura con codificación."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, 世界!"  # Contenido con caracteres Unicode

        file_handler.write_file(str(test_file), test_content)

        assert test_file.exists()
        assert test_file.read_text(encoding='utf-8') == test_content
        mock_logger.debug.assert_called_with(
            f"Successfully wrote {len(test_content)} characters to {test_file}"
        )

    def test_read_file_os_error(self, file_handler, tmp_path, mock_logger):
        """Test de manejo de errores del sistema operativo."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        with patch('pathlib.Path.open') as mock_open:
            mock_open.side_effect = OSError("I/O error")
            
            with pytest.raises(FileOperationError) as exc_info:
                file_handler.read_file(str(test_file))

        assert "I/O error" in str(exc_info.value)
        mock_logger.error.assert_called_with(
            f"Error reading file {test_file}: I/O error"
        )

    def test_write_file_os_error(self, file_handler, tmp_path, mock_logger):
        """Test de manejo de errores del sistema operativo en escritura."""
        test_file = tmp_path / "test.txt"

        with patch('pathlib.Path.open') as mock_open:
            mock_open.side_effect = OSError("I/O error")
            
            with pytest.raises(FileOperationError) as exc_info:
                file_handler.write_file(str(test_file), "test content")

        assert "I/O error" in str(exc_info.value)
        mock_logger.error.assert_called_with(
            f"Error writing to file {test_file}: I/O error"
        )
