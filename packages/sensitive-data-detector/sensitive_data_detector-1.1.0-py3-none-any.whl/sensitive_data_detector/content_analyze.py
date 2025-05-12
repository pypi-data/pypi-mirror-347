import re
from typing import Dict, List


class ContentAnalyzer:
    """
    A class to analyze content for sensitive information using provided patterns.
    """

    def __init__(self, patterns: Dict[str, str]):
        """
        Initializes the ContentAnalyzer with a set of patterns.

        Args:
            patterns: A dictionary where keys are pattern names and values are regex patterns.
        """
        self.patterns = patterns

    def analyze_content(self, content: str) -> Dict[str, List[str]]:
        """
        Analyzes the content for sensitive information.

        Args:
            content: The content to be analyzed.

        Returns:
            A dictionary with pattern types and their matches.
        """
        results = {}
        for pattern_name, pattern in self.patterns.items():
            matches = re.finditer(pattern, content)
            found_matches = [match.group(0) for match in matches]
            if found_matches:
                results[pattern_name] = found_matches
        return results
