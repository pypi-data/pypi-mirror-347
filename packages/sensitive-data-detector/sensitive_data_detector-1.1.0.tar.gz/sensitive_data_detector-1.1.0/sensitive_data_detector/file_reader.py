from pathlib import Path
from typing import Union


class FileReader:
    """
    A class responsible for reading file contents.
    """

    def __init__(self, file_path: Union[str, Path]):
        """
        Initializes the FileReader with the given file path.

        Args:
            file_path: The path to the file as a string or Path object.
        """
        self.path = Path(file_path) if isinstance(file_path, str) else file_path

    def get_file_content(self) -> str:
        """
        Reads and returns the content of the file as a string.

        Returns:
            The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()
