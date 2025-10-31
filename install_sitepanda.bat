@echo off
REM SitePanda Desktop - One-Click Installer for Windows

echo ==================================================
echo SitePanda Desktop - One-Click Installer
echo ==================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check if pip is available
echo.
echo Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed
    echo Installing pip...
    python -m ensurepip --default-pip
)
echo pip is available

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install -r requirements.txt --user

if %errorlevel% neq 0 (
    echo.
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully

REM Run installation test
echo.
echo Running installation test...
python test_installation.py

if %errorlevel% neq 0 (
    echo.
    echo Installation test failed
    echo Please check the error messages above
    pause
    exit /b 1
)

REM Ask about desktop shortcut
echo.
set /p CREATE_SHORTCUT="Would you like to create desktop shortcuts? (Y/N): "
if /i "%CREATE_SHORTCUT%"=="Y" (
    call create_desktop_shortcut_windows.bat
)

echo.
echo ==================================================
echo Installation completed successfully!
echo ==================================================
echo.
echo To run SitePanda Desktop:
echo   python app.py
echo.
echo Or use the desktop shortcut if you created one
echo.
echo For quick start guide, see: QUICK_START.md
echo For full documentation, see: README.md
echo.
pause
