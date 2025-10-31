#!/bin/bash
# SitePanda Desktop - macOS Application Creator

echo "Creating macOS application for SitePanda Desktop..."

# Get the absolute path to the application
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PATH="$APP_DIR/app.py"

# Application bundle location
APP_BUNDLE="$HOME/Applications/SitePanda Desktop.app"

# Create the application bundle structure
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Create the launcher script
cat > "$APP_BUNDLE/Contents/MacOS/SitePanda" << EOF
#!/bin/bash
cd "$APP_DIR"
python3 "$APP_PATH"
EOF

# Make the launcher executable
chmod +x "$APP_BUNDLE/Contents/MacOS/SitePanda"

# Create Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>SitePanda Desktop</string>
    <key>CFBundleDisplayName</key>
    <string>SitePanda Desktop</string>
    <key>CFBundleIdentifier</key>
    <string>com.sitepanda.desktop</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>SPDA</string>
    <key>CFBundleExecutable</key>
    <string>SitePanda</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo "✓ macOS application created successfully!"
echo ""
echo "Application location: $APP_BUNDLE"
echo ""
echo "You can now:"
echo "  1. Open Finder and navigate to ~/Applications"
echo "  2. Double-click 'SitePanda Desktop' to launch"
echo "  3. Drag it to your Dock for quick access"
echo ""
echo "Note: If you see a security warning, go to System Preferences → Security & Privacy"
echo "      and click 'Open Anyway' to allow the application to run."
