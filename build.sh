#!/bin/bash

# Build script for KMDViewer
# Creates a standalone executable using PyInstaller

set -e

echo "================================"
echo "KMDViewer Build Script"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

echo "Cleaning previous builds..."
rm -rf build dist __pycache__ src/__pycache__ src/*/__pycache__ .venv
echo "Clean complete."
echo ""

# On Linux/ARM (Raspberry Pi / Ubuntu ARM), install PyQt5 via apt to avoid source builds
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Checking system PyQt5 packages..."
    MISSING_PKGS=()
    for pkg in python3-pyqt5 python3-pyqt5.qtwebengine; do
        if ! dpkg -l | grep -q "^ii.*$pkg "; then
            MISSING_PKGS+=("$pkg")
        fi
    done

    if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
        echo "Installing missing system packages: ${MISSING_PKGS[*]}"
        sudo apt-get install -y "${MISSING_PKGS[@]}"
    else
        echo "System PyQt5 packages already installed."
    fi
    echo ""
fi

# Set up virtual environment with system-site-packages so PyQt5 from apt is visible
VENV_DIR=".venv"
echo "Creating virtual environment (--system-site-packages)..."
python3 -m venv --system-site-packages "$VENV_DIR"

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip --quiet

echo "Installing non-Qt Python dependencies..."
# Exclude PyQt5/PyQtWebEngine — provided by system apt packages on Linux
pip install --prefer-binary \
    markdown-it-py==3.0.0 \
    mdit-py-plugins==0.4.0 \
    pygments==2.17.2 \
    "Pillow>=11.0.0" \
    reportlab==4.0.4

echo "Installing PyInstaller..."
pip install --prefer-binary pyinstaller

echo ""
echo "Building executable with PyInstaller..."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    pyinstaller KMDViewer.spec
else
    python3 -m PyInstaller KMDViewer.spec
fi

deactivate

echo ""
echo "================================"
echo "Build Complete!"
echo "================================"
echo ""
echo "Executable location:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  dist/KMDViewer.app"
else
    echo "  dist/KMDViewer"
fi
echo ""
echo "To run the application:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  open dist/KMDViewer.app"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  dist\\KMDViewer.exe"
else
    echo "  ./dist/KMDViewer"
fi
