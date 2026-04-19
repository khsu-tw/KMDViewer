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

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

echo "Cleaning previous builds..."
rm -rf build dist __pycache__ src/__pycache__ src/*/__pycache__
echo "Clean complete."
echo ""

# Set up virtual environment to avoid PEP 668 externally-managed-environment error
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

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
