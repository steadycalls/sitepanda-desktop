#!/bin/bash
# Duda Site Manager - Installation Script

echo "=================================================="
echo "Duda Site Manager - Installation"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check if Python 3.11+ is available
REQUIRED_VERSION="3.11"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "✓ Python version is compatible"
else
    echo "✗ Python 3.11 or higher is required"
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
echo "Installing dependencies..."
pip3 install -r requirements.txt

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

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Installation completed successfully!"
    echo "=================================================="
    echo ""
    echo "To run the application:"
    echo "  python3 app.py"
    echo ""
    echo "For quick start guide, see: QUICK_START.md"
    echo "For full documentation, see: README.md"
    echo ""
else
    echo ""
    echo "✗ Installation test failed"
    echo "Please check the error messages above"
    exit 1
fi
