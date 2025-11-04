# ============================================
# SitePanda Desktop - PowerShell Installer
# ============================================
# This script:
# - Checks for Python 3.11+
# - Installs all dependencies
# - Tests the installation
# - Creates desktop and Start Menu shortcuts
# - Launches the application
# ============================================

Write-Host ""
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host " SitePanda Desktop - Windows Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Step 1: Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
Write-Host ""

try {
    $PythonVersion = python --version 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    
    # Extract version number
    if ($PythonVersion -match "Python (\d+)\.(\d+)\.(\d+)") {
        $Major = [int]$Matches[1]
        $Minor = [int]$Matches[2]
        $Patch = [int]$Matches[3]
        
        Write-Host "Found Python $Major.$Minor.$Patch" -ForegroundColor Green
        
        # Check version
        if ($Major -lt 3 -or ($Major -eq 3 -and $Minor -lt 11)) {
            Write-Host ""
            Write-Host "ERROR: Python version is too old." -ForegroundColor Red
            Write-Host "Found: $Major.$Minor.$Patch" -ForegroundColor Red
            Write-Host "Required: 3.11 or higher" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please upgrade Python from:" -ForegroundColor Yellow
            Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
            Write-Host ""
            Read-Host "Press Enter to exit"
            exit 1
        }
        
        Write-Host "Python version OK: $Major.$Minor.$Patch" -ForegroundColor Green
    }
}
catch {
    Write-Host ""
    Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11 or higher from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Step 2: Install dependencies
Write-Host "[2/6] Installing dependencies..." -ForegroundColor Yellow
Write-Host ""
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet

# Install requirements
Write-Host "Installing packages..." -ForegroundColor Gray
$InstallResult = python -m pip install -r requirements.txt --quiet 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies." -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying with verbose output..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Run tests
Write-Host "[3/6] Running installation tests..." -ForegroundColor Yellow
Write-Host ""

$TestResult = python test_installation.py 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Installation test failed." -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installation test passed!" -ForegroundColor Green
Write-Host ""

# Step 4: Create desktop shortcut
Write-Host "[4/6] Creating desktop shortcut..." -ForegroundColor Yellow
Write-Host ""

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "SitePanda Desktop.lnk"
$AppPath = Join-Path $ScriptDir "app.py"
$PythonExe = (Get-Command python).Source

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonExe
$Shortcut.Arguments = "`"$AppPath`""
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "SitePanda Desktop - Duda Site Manager with SEO Audits"
$Shortcut.Save()

if (Test-Path $ShortcutPath) {
    Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
} else {
    Write-Host "Warning: Could not create desktop shortcut." -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Create Start Menu shortcut
Write-Host "[5/6] Creating Start Menu shortcut..." -ForegroundColor Yellow
Write-Host ""

$StartMenuPath = [Environment]::GetFolderPath("Programs")
$StartMenuShortcut = Join-Path $StartMenuPath "SitePanda Desktop.lnk"

$Shortcut2 = $WScriptShell.CreateShortcut($StartMenuShortcut)
$Shortcut2.TargetPath = $PythonExe
$Shortcut2.Arguments = "`"$AppPath`""
$Shortcut2.WorkingDirectory = $ScriptDir
$Shortcut2.Description = "SitePanda Desktop - Duda Site Manager with SEO Audits"
$Shortcut2.Save()

if (Test-Path $StartMenuShortcut) {
    Write-Host "Start Menu shortcut created successfully!" -ForegroundColor Green
} else {
    Write-Host "Warning: Could not create Start Menu shortcut." -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Installation complete
Write-Host "[6/6] Installation complete!" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Installation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Python Version: $PythonVersion" -ForegroundColor White
Write-Host "Installation Directory: $ScriptDir" -ForegroundColor White
Write-Host "Desktop Shortcut: $ShortcutPath" -ForegroundColor White
Write-Host "Start Menu: $StartMenuShortcut" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Double-click 'SitePanda Desktop' on your desktop" -ForegroundColor White
Write-Host "   OR search for 'SitePanda Desktop' in Start Menu" -ForegroundColor White
Write-Host ""
Write-Host "2. Click 'Settings' to configure your credentials:" -ForegroundColor White
Write-Host "   - Duda API (required)" -ForegroundColor Gray
Write-Host "   - AWS S3 (optional)" -ForegroundColor Gray
Write-Host "   - SEO Tools (optional - DataForSEO, GA4, GSC)" -ForegroundColor Gray
Write-Host "   - Webhooks (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Click 'Fetch Data' to start using the application" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Documentation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "- README.md - General documentation" -ForegroundColor White
Write-Host "- QUICK_START.md - 5-minute setup guide" -ForegroundColor White
Write-Host "- USER_GUIDE.md - Comprehensive manual" -ForegroundColor White
Write-Host "- SEO_AUDIT_GUIDE.md - SEO audit feature guide" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ask to launch
$Launch = Read-Host "Would you like to launch SitePanda Desktop now? (Y/N)"

if ($Launch -eq "Y" -or $Launch -eq "y") {
    Write-Host ""
    Write-Host "Launching SitePanda Desktop..." -ForegroundColor Green
    Write-Host ""
    Start-Process python -ArgumentList "`"$AppPath`"" -WorkingDirectory $ScriptDir
    Write-Host "Application launched!" -ForegroundColor Green
    Write-Host "You can close this window." -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "You can launch SitePanda Desktop anytime from:" -ForegroundColor White
    Write-Host "- Desktop shortcut" -ForegroundColor Gray
    Write-Host "- Start Menu" -ForegroundColor Gray
    Write-Host "- Or run: python app.py" -ForegroundColor Gray
}

Write-Host ""
Read-Host "Press Enter to exit"
