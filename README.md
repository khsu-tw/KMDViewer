# MDViewer

A Python-based Markdown Viewer with PDF export capability. View, edit, and convert Markdown files to PDF with an intuitive desktop interface.

## Features

- 📖 **Open Markdown Files** - Browse and open `.md` files from your computer
- 👁️ **Live Preview** - Real-time rendering as you type or edit
- 📄 **PDF Export** - Convert Markdown to professional PDF with customizable settings
- 🎨 **Rich Formatting** - Support for code highlighting, tables, blockquotes, and more
- 📋 **Recent Files** - Quick access to recently opened files
- 🚀 **Standalone Executable** - Package as a single executable file

## System Requirements

- Python 3.11 or higher
- PyQt5
- Dependencies listed in `requirements.txt`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MDViewer.git
cd MDViewer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python src/main.py
```

Or using the setup.py:

```bash
python -m pip install -e .
mdviewer
```

## Building Standalone Executable

To create a standalone executable using PyInstaller:

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the Executable

```bash
pyinstaller --onefile --windowed --name MDViewer src/main.py
```

The executable will be created in the `dist/` directory.

## Usage

### Opening Files
- Use the **File > Open** menu or press `Ctrl+O`
- Select a Markdown file from your computer
- The file will be displayed in the editor and preview panes

### Live Preview
- The preview updates automatically as you type
- Use **View > Refresh Preview** or press `F5` to manually refresh
- Supports Markdown syntax including:
  - Headers (# to ######)
  - Lists (ordered and unordered)
  - Code blocks with syntax highlighting
  - Tables
  - Blockquotes
  - Links and images
  - And more!

### Exporting to PDF
1. Click **File > Export as PDF** or press `Ctrl+E`
2. Configure page settings (size, margins) in the dialog
3. Choose the output location and filename
4. Click **Export** to generate the PDF

## Project Structure

```
MDViewer/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── markdown_processor.py   # Markdown to HTML conversion
│   │   ├── pdf_exporter.py         # HTML to PDF export
│   │   └── file_manager.py         # File operations
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py   # Main application window
│       └── preview_viewer.py # HTML preview widget
├── resources/               # Application resources (icons, etc.)
├── requirements.txt         # Python dependencies
├── setup.py                # Package configuration
├── README.md               # This file
└── Workplan.md            # Project workplan
```

## Key Dependencies

- **PyQt5** - GUI framework
- **markdown-it-py** - Markdown parsing and rendering
- **pygments** - Syntax highlighting for code blocks
- **weasyprint** - HTML to PDF conversion
- **Pillow** - Image handling

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+E` | Export as PDF |
| `Ctrl+Q` | Exit application |
| `F5` / `Ctrl+R` | Refresh preview |
| `Ctrl+Shift+C` | Clear editor |

## Roadmap

- [ ] Dark mode support
- [ ] Find and replace in editor
- [ ] Document outline/table of contents
- [ ] Theme customization
- [ ] Support for additional markdown extensions
- [ ] Multi-file editing with tabs

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Application won't start
- Make sure Python 3.11+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that PyQt5 is properly installed: `python -c "from PyQt5 import QtCore; print('OK')"`

### Preview not updating
- Try refreshing with `F5` or **View > Refresh Preview**
- Check that the Markdown syntax is valid

### PDF export fails
- Ensure weasyprint and its dependencies are installed
- Try with simpler Markdown content first to isolate the issue
- Check file permissions in the output directory

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Version**: 0.1.0  
**Last Updated**: 2026-04-16
