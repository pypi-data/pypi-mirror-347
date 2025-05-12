import json
import os
from pathlib import Path
from typing import Dict, Optional, Union


class PatternLoader:
    """
    A class responsible for loading sensitive information patterns from a configuration file.
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initializes the PatternLoader.

        Args:
            config_path: Optional path to the configuration file.
                         If None, defaults to 'config.json' in the same directory.
        """
        if config_path is None:
            self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        else:
            self.config_path = str(config_path)

    def load_patterns(self) -> Dict[str, str]:
        """
        Loads sensitive information patterns from the config file
        and returns a dictionary of patterns.

        Returns:
            A dictionary where keys are pattern names and values are pattern strings.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            json.JSONDecodeError: If the configuration file is not valid JSON.
            KeyError: If 'sensitive_info' key is missing in the configuration.
        """
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            return config["sensitive_info"]
        except FileNotFoundError:
            # You might want to log this error or handle it differently
            print(f"Error: Configuration file not found at {self.config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.config_path}")
            raise
        except KeyError:
            print("Error: 'sensitive_info' key not found in the configuration file.")
            raise
