# MDViewer Development Guide

## Project Overview

MDViewer is a Python-based Markdown viewer with PDF export capability. It's built with PyQt5 for the GUI and uses modern markdown-it-py for parsing.

### Architecture

```
MDViewer
├── Core Layer (src/core/)
│   ├── markdown_processor.py  → Converts MD to HTML
│   ├── pdf_exporter.py        → Converts HTML to PDF
│   └── file_manager.py        → Handles file I/O
└── UI Layer (src/ui/)
    ├── main_window.py         → Main application window
    └── preview_viewer.py      → HTML preview widget
```

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MDViewer.git
cd MDViewer
```

### 2. Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Install Development Tools

```bash
pip install pytest pytest-cov pylint black isort
```

## Running the Application

### Development Mode

```bash
python src/main.py
```

### With Debug Output

```bash
python src/main.py --debug
```

## Project Structure

```
MDViewer/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── markdown_processor.py
│   │   ├── pdf_exporter.py
│   │   └── file_manager.py
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py
│       └── preview_viewer.py
├── resources/
│   ├── icons/
│   └── styles/
├── tests/
│   ├── test_markdown_processor.py
│   ├── test_pdf_exporter.py
│   └── test_file_manager.py
├── requirements.txt
├── setup.py
├── README.md
├── INSTALLATION.md
├── DEVELOPMENT.md
└── MDViewer.spec
```

## Key Components

### MarkdownProcessor (src/core/markdown_processor.py)

Converts Markdown to HTML with syntax highlighting.

**Key Features:**
- Uses `markdown-it-py` for parsing
- Includes plugins for advanced Markdown
- Syntax highlighting with Pygments
- Embedded CSS for styling

**Usage:**
```python
from src.core.markdown_processor import MarkdownProcessor

processor = MarkdownProcessor()
html = processor.process("# Hello\nThis is **bold**")
print(html)
```

### PDFExporter (src/core/pdf_exporter.py)

Converts HTML to PDF with customizable settings.

**Key Features:**
- Uses `weasyprint` for conversion
- Customizable page sizes and margins
- Export to file or bytes
- CSS-based styling

**Usage:**
```python
from src.core.pdf_exporter import PDFExporter

exporter = PDFExporter()
exporter.export_to_file(html_content, "output.pdf")
```

### FileManager (src/core/file_manager.py)

Handles file operations with recent files tracking.

**Key Features:**
- Open and save Markdown files
- Format validation
- Recent files management
- Config persistence

**Usage:**
```python
from src.core.file_manager import FileManager

manager = FileManager()
content = manager.open_file("document.md")
recent = manager.get_recent_files()
```

## Coding Standards

### Code Style

- Follow PEP 8 guidelines
- Use type hints for functions
- Maximum line length: 100 characters
- Use docstrings for all public functions

### Code Formatting

```bash
# Format code with black
black src/

# Sort imports with isort
isort src/

# Check code quality with pylint
pylint src/
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `MarkdownProcessor`)
- **Functions/Methods**: snake_case (e.g., `process_markdown`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_MARGIN`)
- **Private members**: prefix with `_` (e.g., `_setup_ui`)

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_markdown_processor.py
```

### Writing Tests

Example test structure:

```python
import pytest
from src.core.markdown_processor import MarkdownProcessor

class TestMarkdownProcessor:
    def setup_method(self):
        self.processor = MarkdownProcessor()

    def test_basic_conversion(self):
        md = "# Hello"
        html = self.processor.process(md)
        assert "<h1>" in html

    def test_code_highlighting(self):
        md = "```python\nprint('hello')\n```"
        html = self.processor.process(md)
        assert "highlight" in html
```

## Common Tasks

### Adding a New Feature

1. Create a new branch: `git checkout -b feature/my-feature`
2. Implement the feature
3. Add tests in `tests/`
4. Run tests: `pytest`
5. Format code: `black src/` and `isort src/`
6. Commit and push
7. Create a pull request

### Adding Dependencies

1. Add to `requirements.txt`
2. Update `setup.py`
3. Install: `pip install -r requirements.txt`
4. Commit changes

### Building for Release

```bash
# Update version in setup.py and src/__init__.py
# Build executable
bash build.sh  # macOS/Linux
# or
build.bat  # Windows

# Test the executable
./dist/MDViewer
```

## Performance Tips

1. **Markdown Processing**: Cache processed HTML for large documents
2. **Preview Updates**: Debounce rapid text changes
3. **PDF Export**: Consider async processing for large files
4. **Memory**: Monitor for memory leaks in QWebEngineView

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Qt Debugging

```python
# In main_window.py
from PyQt5.QtCore import pyqtRemoveInputHook
pyqtRemoveInputHook()  # For debugging
```

## Future Enhancements

- [ ] Dark mode support
- [ ] Find and replace functionality
- [ ] Document outline/TOC
- [ ] Multiple file tabs
- [ ] Custom CSS themes
- [ ] Plugin system
- [ ] Collaborative editing
- [ ] Export to DOCX, HTML

## Useful Resources

- [PyQt5 Documentation](https://doc.qt.io/qt-5/index.html)
- [markdown-it-py GitHub](https://github.com/executablebooks/markdown-it-py)
- [weasyprint Documentation](https://weasyprint.org/)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

## Getting Help

- Check existing issues on GitHub
- Review the codebase and comments
- Ask questions in discussions
- Submit issues with detailed information

## Submitting Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

Please follow the existing code style and include tests for new features.

---

**Development Guide Version**: 1.0  
**Last Updated**: 2026-04-16
