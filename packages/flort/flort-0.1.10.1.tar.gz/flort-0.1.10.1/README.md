# Flort: File Concatenation and Project Overview Tool 🗂️

Flort is a powerful command-line tool designed to help developers create consolidated views of their project's source code. It generates comprehensive project overviews by combining directory trees, Python module outlines, and source file concatenation into a single, easily shareable output file.

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## Features ✨

- **Interactive File Selection UI**: Optional terminal-based interface for intuitive file and directory selection
- **Directory Tree Generation**: Creates visual representation of project structure
- **Source File Concatenation**: Combines multiple source files into a single output
- **Python Module Outline**: Generates detailed outlines of Python modules including:
  - Function signatures with type hints
  - Class hierarchies
  - Docstrings
  - Decorators
- **Flexible File Filtering**:
  - Filter by file extensions
  - Include/exclude hidden files
  - Ignore specific directories
  - Include specific files
- **Configurable Output**: Choose between file output or console display

## Installation 🚀

```bash
pip install flort
```

## Quick Start 🏃‍♂️

Using command line:
```bash
# Basic usage with Python files
flort -e py

# Using interactive UI
flort -u -e py
```

## Usage Examples 📚

### Standard Command Line Usage
```bash
# Basic directory analysis with Python files
flort -e py

# Multiple directories and file types
flort -d src tests -e py,js,css

# Include specific files and ignore directories
flort -e py -f setup.py,README.md -i venv,build

# Output to console with hidden files
flort -a -H -o stdio

# Python outline only, no source dump
flort -e py -O -n

# Complex configuration
flort -d src tests \
    -e py,js \
    -i venv,build \
    -f setup.py \
    -H \
    -o project.txt
```

### Interactive UI Usage (Optional)
The `-u` flag enables an interactive terminal interface for file selection:

```bash
# Basic UI launch
flort -u

# UI with preselected Python files
flort -u -e py

# UI with included files and no output file
flort -u -f setup.py,requirements.txt -o stdio

# UI with multiple extensions and specific directories
flort -u -e py,js,css -d src tests

# UI with all extensions and hidden files
flort -u -a -H

# UI with outline only, no source dump
flort -u -O -n -e py

# UI with full configuration
flort -u \
    -e py,js \
    -i venv,build \
    -f setup.py \
    -H \
    -o project.txt \
    -d src tests
```

### Using Glob Patterns
You can use glob patterns to match files (make sure to quote patterns to prevent shell expansion):

```bash
# Match all Python files
flort -g "*.py"

# Match multiple patterns
flort -g "*.py,*.js"

# Combine with directories
flort -d src -g "*.py"

# Combine with other options
flort -g "*.py" -i venv,build -H
```

## Command Line Options 🎮

| Option | Short | Description |
|--------|-------|-------------|
| `--dir DIRECTORY` | `-d` | Directories to analyze (default: current directory) |
| `--extensions` | `-e` | File extensions to include (comma-separated, without dots: py,js,txt) |
| `--output` | `-o` | Output file path (default: `{current_dir}.flort.txt`) |
| `--outline` | `-O` | Generate Python module outline |
| `--no-dump` | `-n` | Skip source file concatenation |
| `--no-tree` | `-t` | Skip directory tree generation |
| `--all` | `-a` | Include all file types |
| `--hidden` | `-H` | Include hidden files |
| `--ignore-dirs` | `-i` | Comma-separated list of directories to ignore |
| `--include-files` | `-f` | Comma-separated list of files to include |
| `--glob` | `-g` | Glob patterns to match files (comma-separated, quoted: "*.py,*.js") |
| `--ui` | `-u` | Launch interactive file selector UI |
| `--verbose` | `-v` | Enable verbose logging |
| `--archive` | `-z` | Archive output file (zip, tar.gz) |
| `--help` | `-h` | Show help message |

## Interactive UI Controls 🎮

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate files/directories |
| ←/→ | Navigate directory tree |
| SPACE | Toggle selection |
| i | Toggle ignore |
| f | Edit file type filters |
| v | View selected/ignored items |
| q | Save and exit |
| ESC | Exit without saving |

## Output Format 📄

The generated output file follows this structure:

```
## Florted: 2025-01-02 05:54:57

## Directory Tree
|-- project/
|   |-- src/
|   |   |-- main.py
|   |-- tests/
|       |-- test_main.py

## Detailed Python Outline
### File: src/main.py
CLASS: MyClass
  DOCSTRING:
    Class description
  FUNCTION: my_method(arg1: str, arg2: int = 0) -> bool
    DOCSTRING:
      Method description

## File data
--- File: src/main.py
[source code here]
```

## Development 🛠️

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/chris17453/flort.git
cd flort

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=flort tests/
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Add type hints to function signatures
- Include docstrings for classes and functions
- Write unit tests for new features

## License 📝

This project is licensed under the BSD 3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to all contributors who have helped shape Flort
- Inspired by various code analysis and documentation tools in the Python ecosystem

## Support 💬

If you encounter any problems or have suggestions, please [open an issue](https://github.com/chris17453/flort/issues).