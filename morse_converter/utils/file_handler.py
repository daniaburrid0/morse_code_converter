from pathlib import Path
from morse_converter.utils import setup_logger

# Configurar logger para este módulo
logger = setup_logger(__name__)

class FileOperationError(Exception):
    """Custom exception for file operation errors."""
    pass

class FileHandler:
    """
    Manages file operations for input/output and configuration.

    Methods:
        read_file(file_path: str) -> str
            Reads content from a file.
        
        write_file(file_path: str, content: str) -> None
            Writes content to a file.
    """

    def read_file(self, file_path: str) -> str:
        """
        Reads content from a file.

        Parameters:
            file_path (str): The path to the file to read.

        Returns:
            str: The content of the file.

        Raises:
            FileOperationError: If the file cannot be read.

        Example:
            >>> handler = FileHandler()
            >>> handler.read_file("example.txt")
            'File content'
        """
        logger.info(f"Attempting to read file: {file_path}")
        try:
            path = Path(file_path)
            
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                raise FileOperationError(f"File not found: {file_path}")
                
            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                raise FileOperationError(f"Path is not a file: {file_path}")
                
            with path.open('r', encoding='utf-8') as file:
                content = file.read()
                logger.debug(f"Successfully read {len(content)} characters from {file_path}")
                return content
                
        except (PermissionError, OSError) as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise FileOperationError(f"Error reading file: {str(e)}")

    def write_file(self, file_path: str, content: str) -> None:
        """
        Writes content to a file.

        Parameters:
            file_path (str): The path to the file to write.
            content (str): The content to write to the file.

        Raises:
            FileOperationError: If the file cannot be written.

        Example:
            >>> handler = FileHandler()
            >>> handler.write_file("example.txt", "New content")
        """
        logger.info(f"Attempting to write to file: {file_path}")
        try:
            path = Path(file_path)
            
            # Crear directorio si no existe
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with path.open('w', encoding='utf-8') as file:
                file.write(content)
                logger.debug(f"Successfully wrote {len(content)} characters to {file_path}")
                
        except (PermissionError, OSError) as e:
            logger.error(f"Error writing to file {file_path}: {str(e)}")
            raise FileOperationError(f"Error writing to file: {str(e)}")
