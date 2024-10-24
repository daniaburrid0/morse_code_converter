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
        pass

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
        pass
