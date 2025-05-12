from pathlib import Path
from typing import Optional, Union

from .content_analyze import ContentAnalyzer
from .file_reader import FileReader
from .load_patterns import PatternLoader


class SensitiveChecker:
    """
    A class to check if a file contains any sensitive information.
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.patterns = PatternLoader(config_path).load_patterns()
        self.analyzer = ContentAnalyzer(self.patterns)

    def has_sensitive_info(self, file_path: Union[str, Path]) -> bool:
        """
        Check if the file contains any sensitive information.
        Args:
            file_path: The path to the file to check.
        Returns:
            True if sensitive information is found, False otherwise.
        """
        content = FileReader(file_path).get_file_content()
        results = self.analyzer.analyze_content(content)
        return len(results) > 0
