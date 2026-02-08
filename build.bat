@echo off
REM Build script for Brauler executable

echo ========================================
echo Brauler Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

echo Building executable...
echo.

cd brauler

REM Build the executable
pyinstaller --onefile --windowed --name Brauler main.py

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Executable location: brauler\dist\Brauler.exe
echo.
echo To test: cd brauler\dist ^&^& Brauler.exe
echo.

pause
