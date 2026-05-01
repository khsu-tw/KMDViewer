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

REM Check for Microsoft C++ Build Tools
echo Checking for Microsoft C++ Build Tools...
set "BUILDTOOLS_FOUND=0"

REM Method 1: Check using vswhere (Visual Studio Installer)
where vswhere >nul 2>&1
if not errorlevel 1 (
    for /f "usebackq tokens=*" %%i in (`vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2^>nul`) do (
        if exist "%%i\VC\Tools\MSVC\" (
            set "BUILDTOOLS_FOUND=1"
            echo [OK] Found Visual Studio Build Tools
        )
    )
)

REM Method 2: Try to find cl.exe (MSVC compiler)
if "%BUILDTOOLS_FOUND%"=="0" (
    cl.exe >nul 2>&1
    if not errorlevel 1 (
        set "BUILDTOOLS_FOUND=1"
        echo [OK] Found MSVC compiler
    )
)

if "%BUILDTOOLS_FOUND%"=="0" (
    echo.
    echo [WARNING] Microsoft C++ Build Tools not detected!
    echo This may cause installation failures for packages that need compilation.
    echo.
    echo Solutions:
    echo   1. Install Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo   2. Use Python 3.11 or 3.12 (better pre-built wheel support)
    echo   3. Continue anyway (will try to use pre-built wheels only)
    echo.
    choice /C YN /M "Continue anyway"
    if errorlevel 2 (
        echo Build cancelled.
        pause
        exit /b 1
    )
)
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt --only-binary :all:
if errorlevel 1 (
    echo Error: Failed to install dependencies
    echo.
    echo Trying alternative installation method...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        echo Please install Visual C++ Build Tools or use Python 3.11/3.12
        pause
        exit /b 1
    )
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
