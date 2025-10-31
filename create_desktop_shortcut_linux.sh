#!/bin/bash
# SitePanda Desktop - Linux Desktop Shortcut Creator

echo "Creating desktop shortcut for SitePanda Desktop..."

# Get the absolute path to the application
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$APP_DIR/app.py"

# Desktop file location
DESKTOP_FILE="$HOME/.local/share/applications/sitepanda-desktop.desktop"

# Create .local/share/applications directory if it doesn't exist
mkdir -p "$HOME/.local/share/applications"

# Create the desktop entry
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SitePanda Desktop
Comment=Manage Duda sites and fetch data
Exec=python3 "$APP_PATH"
Icon=$APP_DIR/assets/icon.png
Terminal=false
Categories=Development;Utility;
Keywords=duda;sitepanda;website;management;
StartupNotify=true
EOF

# Make the desktop file executable
chmod +x "$DESKTOP_FILE"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications"
fi

echo "✓ Desktop shortcut created successfully!"
echo ""
echo "You can now find 'SitePanda Desktop' in your application menu."
echo ""
echo "To create a desktop icon (optional):"
echo "  cp \"$DESKTOP_FILE\" ~/Desktop/"
echo "  chmod +x ~/Desktop/sitepanda-desktop.desktop"
