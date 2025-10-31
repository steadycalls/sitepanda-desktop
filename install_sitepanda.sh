#!/bin/bash
# SitePanda Desktop - One-Click Installer for Linux/macOS

set -e  # Exit on error

echo "=================================================="
echo "SitePanda Desktop - One-Click Installer"
echo "=================================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "Detected platform: $PLATFORM"
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "Found Python $PYTHON_VERSION"
    
    # Check if Python 3.11+ is available
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
        echo "✓ Python version is compatible"
    else
        echo "✗ Python 3.11 or higher is required"
        echo "Please install Python 3.11+ and try again"
        exit 1
    fi
else
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.11+ and try again"
    exit 1
fi

# Check if pip is available
echo ""
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3 is available"
else
    echo "✗ pip3 is not found"
    echo "Please install pip3 and try again"
    exit 1
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --user

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Run installation test
echo ""
echo "Running installation test..."
python3 test_installation.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Installation test failed"
    echo "Please check the error messages above"
    exit 1
fi

# Create desktop shortcut
echo ""
echo "Would you like to create a desktop shortcut? (y/n)"
read -r CREATE_SHORTCUT

if [[ "$CREATE_SHORTCUT" =~ ^[Yy]$ ]]; then
    if [ "$PLATFORM" = "Linux" ]; then
        ./create_desktop_shortcut_linux.sh
    elif [ "$PLATFORM" = "Mac" ]; then
        ./create_desktop_shortcut_macos.sh
    fi
fi

echo ""
echo "=================================================="
echo "✓ Installation completed successfully!"
echo "=================================================="
echo ""
echo "To run SitePanda Desktop:"
echo "  python3 app.py"
echo ""
if [ "$PLATFORM" = "Linux" ]; then
    echo "Or find 'SitePanda Desktop' in your application menu"
elif [ "$PLATFORM" = "Mac" ]; then
    echo "Or open 'SitePanda Desktop' from ~/Applications"
fi
echo ""
echo "For quick start guide, see: QUICK_START.md"
echo "For full documentation, see: README.md"
echo ""
