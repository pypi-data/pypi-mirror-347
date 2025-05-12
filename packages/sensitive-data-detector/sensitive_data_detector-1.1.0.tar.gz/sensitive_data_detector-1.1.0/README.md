# Sensitive Data Detector 🔍

A Python package that helps detect sensitive information in files and code. Protect your codebase from accidental exposure of API keys, passwords, tokens, and other sensitive data.

[![PyPI version](https://badge.fury.io/py/sensitive-data-detector.svg)](https://badge.fury.io/py/sensitive-data-detector)
[![Python Versions](https://img.shields.io/pypi/pyversions/sensitive-data-detector)](https://pypi.org/project/sensitive-data-detector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## 🚀 Features

- 🔑 Detects API keys and tokens
- 📧 Identifies email addresses
- 🔐 Finds sensitive patterns in code
- ⚙️ Configurable detection patterns
- 📁 Works with any text-based file
- 🛡️ Pre-commit hook support
- 🧑‍💻 **Now fully object-oriented for easier extension and testing!**

## 📦 Installation

```bash
pip install sensitive_data_detector
```

## 🎯 Quick Start

```python
from sensitive_data_detector import SensitiveChecker

checker = SensitiveChecker()  # Optionally pass a custom config path
result = checker.has_sensitive_info("path/to/your/file.txt")
if result:
    True #(sensitive info found in the file)
else:
    False #(no sensitive info found)
```

## 🔍 What It Detects

The package detects various types of sensitive information, including:

- API Keys and Tokens
- Email Addresses
- Private Keys
- Access Tokens
- Passwords
- And more configurable patterns

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/akashdv25/sensitive_info_detector.git
cd sensitive_info_detector

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run pre-commit hooks
pre-commit run --all-files
```

## 🔧 Configuration

The package uses a `config.json` file that defines patterns for sensitive information detection. You can customize these patterns for your specific needs.

Default patterns include:
```json
{
    "sensitive_info": {
        "api_keys": "(?i)((api[_-]key|apikey|api_secret|api[_-]token|auth[_-]token|access[_-]token)['\"]?\\s*[:=]\\s*['\"]([\\w\\-._]+)['\"])",
        "emails": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
    }
}
```

## 🐍 Python Version Support

- Python 3.9
- Python 3.10
- Python 3.11

## 🛠️ Built With

- [Python](https://www.python.org/) - Programming Language
- [Black](https://github.com/psf/black) - Code Formatting
- [isort](https://pycqa.github.io/isort/) - Import Sorting
- [Flake8](https://flake8.pycqa.org/) - Code Linting
- [pytest](https://docs.pytest.org/) - Testing Framework
- [pre-commit](https://pre-commit.com/) - Git Hooks Framework
- **Now with full type checking using [mypy](http://mypy-lang.org/)**

## 🆕 Changelog

### v1.1.0 (new)
- Refactored core modules to use object-oriented programming (OOP) principles.
- Added `SensitiveChecker`, `PatternLoader`, `FileReader`, and `ContentAnalyzer` classes.
- Improved type annotations and mypy compatibility.
- Enhanced code maintainability and extensibility.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🔗 Project Links

- [PyPI: sensitive-data-detector](https://pypi.org/project/sensitive-data-detector/)
- [GitHub Repository](https://github.com/akashdv25/sensitive_data_detector)
- [Bug Tracker](https://github.com/akashdv25/sensitive_data_detector/issues)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📫 Contact

Akash Anandani  
* [Email](mailto:akashanandani.56@gmail.com)

---

Made with ❤️ by [Akash Anandani](https://github.com/akashdv25)