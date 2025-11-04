@echo off
REM ============================================
REM SitePanda Desktop - Complete Windows Installer
REM ============================================
REM This script:
REM - Checks for Python 3.11+
REM - Installs all dependencies
REM - Tests the installation
REM - Creates desktop shortcut
REM - Launches the application
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  SitePanda Desktop - Windows Installer
echo ========================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo [1/6] Checking Python installation...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.11 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

echo Found Python %PYTHON_VERSION%
echo.

REM Check if version is 3.11 or higher
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo ERROR: Python version is too old.
    echo Found: %PYTHON_VERSION%
    echo Required: 3.11 or higher
    echo.
    echo Please upgrade Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 11 (
    echo ERROR: Python version is too old.
    echo Found: %PYTHON_VERSION%
    echo Required: 3.11 or higher
    echo.
    echo Please upgrade Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python version OK: %PYTHON_VERSION%
echo.

echo [2/6] Installing dependencies...
echo.
echo This may take a few minutes...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip --quiet

REM Install requirements
python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo.
    echo Trying with verbose output...
    python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

echo [3/6] Running installation tests...
echo.

python test_installation.py

if errorlevel 1 (
    echo.
    echo ERROR: Installation test failed.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo Installation test passed!
echo.

echo [4/6] Creating desktop shortcut...
echo.

REM Create VBScript to make shortcut
set "VBS_FILE=%TEMP%\create_shortcut.vbs"
set "DESKTOP=%USERPROFILE%\Desktop"
set "APP_PATH=%SCRIPT_DIR%app.py"
set "ICON_PATH=%SCRIPT_DIR%"

REM Get python.exe path
for /f "delims=" %%i in ('where python') do set "PYTHON_EXE=%%i"

REM Create VBScript
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%DESKTOP%\SitePanda Desktop.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%PYTHON_EXE%" >> "%VBS_FILE%"
echo oLink.Arguments = """%APP_PATH%""" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "SitePanda Desktop - Duda Site Manager with SEO Audits" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

REM Execute VBScript
cscript //nologo "%VBS_FILE%"

REM Clean up
del "%VBS_FILE%"

if exist "%DESKTOP%\SitePanda Desktop.lnk" (
    echo Desktop shortcut created successfully!
) else (
    echo Warning: Could not create desktop shortcut.
)

echo.

echo [5/6] Creating Start Menu shortcut...
echo.

set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

REM Create VBScript for Start Menu
set "VBS_FILE=%TEMP%\create_startmenu.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = "%START_MENU%\SitePanda Desktop.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "%PYTHON_EXE%" >> "%VBS_FILE%"
echo oLink.Arguments = """%APP_PATH%""" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo oLink.Description = "SitePanda Desktop - Duda Site Manager with SEO Audits" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

REM Execute VBScript
cscript //nologo "%VBS_FILE%"

REM Clean up
del "%VBS_FILE%"

if exist "%START_MENU%\SitePanda Desktop.lnk" (
    echo Start Menu shortcut created successfully!
) else (
    echo Warning: Could not create Start Menu shortcut.
)

echo.

echo [6/6] Installation complete!
echo.
echo ========================================
echo  Installation Summary
echo ========================================
echo.
echo Python Version: %PYTHON_VERSION%
echo Installation Directory: %SCRIPT_DIR%
echo Desktop Shortcut: %DESKTOP%\SitePanda Desktop.lnk
echo Start Menu: %START_MENU%\SitePanda Desktop.lnk
echo.
echo ========================================
echo  Next Steps
echo ========================================
echo.
echo 1. Double-click "SitePanda Desktop" on your desktop
echo    OR search for "SitePanda Desktop" in Start Menu
echo.
echo 2. Click "Settings" to configure your credentials:
echo    - Duda API (required)
echo    - AWS S3 (optional)
echo    - SEO Tools (optional - DataForSEO, GA4, GSC)
echo    - Webhooks (optional)
echo.
echo 3. Click "Fetch Data" to start using the application
echo.
echo ========================================
echo  Documentation
echo ========================================
echo.
echo - README.md - General documentation
echo - QUICK_START.md - 5-minute setup guide
echo - USER_GUIDE.md - Comprehensive manual
echo - SEO_AUDIT_GUIDE.md - SEO audit feature guide
echo.
echo ========================================
echo.

set /p LAUNCH="Would you like to launch SitePanda Desktop now? (Y/N): "

if /i "%LAUNCH%"=="Y" (
    echo.
    echo Launching SitePanda Desktop...
    echo.
    start "" "%PYTHON_EXE%" "%APP_PATH%"
    echo Application launched!
    echo You can close this window.
) else (
    echo.
    echo You can launch SitePanda Desktop anytime from:
    echo - Desktop shortcut
    echo - Start Menu
    echo - Or run: python app.py
)

echo.
pause
