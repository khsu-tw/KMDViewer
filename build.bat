@echo off
REM Build script for MDViewer on Windows

setlocal enabledelayedexpansion

echo ================================
echo MDViewer Build Script (Windows)
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Building executable with PyInstaller...
pyinstaller MDViewer.spec
if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo ================================
echo Build Complete!
echo ================================
echo.
echo Executable location:
echo   dist\MDViewer.exe
echo.
echo To run the application:
echo   dist\MDViewer.exe
echo.
pause
