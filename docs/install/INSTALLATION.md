# MDViewer Installation Guide

## Quick Start

### Option 1: Run from Source (Requires Python)

1. **Install Python 3.10+**
   - Download from [python.org](https://www.python.org)
   - Ensure Python is added to PATH

2. **Clone or Download the Project**
   ```bash
   git clone https://github.com/yourusername/MDViewer.git
   cd MDViewer
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python src/main.py
   ```

### Option 2: Use Standalone Executable (Windows/macOS/Linux)

1. **Build the Executable**
   
   **On Windows:**
   ```batch
   build.bat
   ```
   
   **On macOS/Linux:**
   ```bash
   bash build.sh
   chmod +x dist/MDViewer
   ```

2. **Run the Executable**
   
   **On Windows:**
   ```
   dist\MDViewer.exe
   ```
   
   **On macOS:**
   ```bash
   open dist/MDViewer.app
   ```
   
   **On Linux:**
   ```bash
   ./dist/MDViewer
   ```

## System Requirements

### For Running from Source
- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.10 or higher
- **RAM**: Minimum 2 GB
- **Disk Space**: 500 MB for dependencies

### For Running Standalone Executable
- **Operating System**: Windows, macOS, or Linux (corresponding to built executable)
- **RAM**: Minimum 512 MB
- **Disk Space**: 100-200 MB

## Detailed Dependencies

MDViewer requires the following Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | >=5.15.0 | GUI Framework |
| PyQt5-WebEngine | >=5.15.0 | Web rendering |
| markdown-it-py | >=3.0.0 | Markdown parsing |
| mdit-py-plugins | >=0.4.0 | Markdown extensions |
| pygments | >=2.17.0 | Syntax highlighting |
| weasyprint | >=60.0 | PDF generation |
| Pillow | >=10.0.0 | Image processing |

All dependencies are automatically installed with `pip install -r requirements.txt`.

## Installation Troubleshooting

### Issue: "Python command not found"
**Solution**: Ensure Python is installed and added to your system PATH.

### Issue: "PyQt5 installation fails"
**Solution**: 
- On Linux, you may need: `sudo apt-get install python3-pyqt5`
- On macOS with Homebrew: `brew install qt5`

### Issue: "weasyprint fails to install"
**Solution**:
- Ensure you have a C compiler installed
- On Windows: Install Visual Studio Build Tools
- On macOS: Install Xcode Command Line Tools: `xcode-select --install`
- On Linux: `sudo apt-get install build-essential libssl-dev libffi-dev`

### Issue: "Module not found" when running
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Application won't start on Linux
**Solution**: 
- Install additional libraries: `sudo apt-get install libgl1-mesa-glx`
- Try running with verbose output: `python src/main.py --debug`

## Building for Distribution

### Creating an Installer (Windows)

Install NSIS and create an installer:

```bash
pip install pyinstaller nsis
pyinstaller MDViewer.spec
# Then use NSIS to create installer
```

### Creating a DMG (macOS)

```bash
# After building with PyInstaller
pip install create-dmg
create-dmg --volname "MDViewer" --window-pos 200 120 --window-size 800 400 \
    --icon "MDViewer.app" 200 190 \
    dist/MDViewer.dmg dist/MDViewer.app
```

### Creating a DEB Package (Linux)

```bash
pip install fpm
fpm -s dir -t deb -n mdviewer -v 0.1.0 -C dist ./MDViewer
```

## Platform-Specific Notes

### Windows
- PyQt5 works best with Python from python.org
- Use `python` command (not `python3`)
- Administrator privileges may be needed for system-wide installation

### macOS
- Requires macOS 10.13 or higher
- Use `python3` command (not `python`)
- M1/M2 Macs: Ensure Python is installed for ARM64 architecture
- May need to allow app in Security & Privacy settings on first run

### Linux
- Requires X11 or Wayland display server
- Tested on Ubuntu 20.04+, Fedora 32+, Debian 11+
- May need additional development libraries for PyQt5
- Use `python3` command (not `python`)

## Updating MDViewer

### From Source
```bash
cd MDViewer
git pull origin main
pip install -r requirements.txt --upgrade
```

### Standalone Executable
- Download the latest release from GitHub
- Replace the old executable with the new one

## Next Steps

1. **First Run**: Open a Markdown file to test the installation
2. **Create PDF**: Try exporting a document to PDF
3. **Explore Features**: Check out the [README.md](README.md) for usage tips

## Getting Help

- Check [README.md](README.md) for usage instructions
- Review the [Troubleshooting](README.md#troubleshooting) section
- Open an issue on GitHub for bugs or feature requests

---

**Installation Guide Version**: 1.0  
**Last Updated**: 2026-04-16
