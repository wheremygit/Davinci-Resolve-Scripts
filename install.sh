#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define target paths
TARGET_DIR="$HOME/.local/share/DaVinciResolve/Fusion/Scripts/Utility"
SCRIPT_SRC_DIR="Davinci Resolve Scripts"

echo "====================================================="
echo "   DaVinci Resolve Smart Importer Installer"
echo "====================================================="

# 1. Check for basic runtime dependencies
echo "--> Checking dependencies..."
if ! command -v ffmpeg &> /dev/null; then
    echo "    ⚠️  Warning: 'ffmpeg' was not found on your path. Please install it."
fi

if ! command -v kdialog &> /dev/null && ! command -v zenity &> /dev/null; then
    echo "    ⚠️  Warning: Neither 'kdialog' nor 'zenity' was found. File selectors may fail."
fi

# 2. Create target utilities directory if missing
echo "--> Creating DaVinci Resolve script directory..."
mkdir -p "$TARGET_DIR"

# 3. Copy scripts over safely
echo "--> Installing scripts into target environment..."
if [ -d "$SCRIPT_SRC_DIR" ]; then
    cp "$SCRIPT_SRC_DIR/Import Media.py" "$TARGET_DIR/"
    cp "$SCRIPT_SRC_DIR/Import Bin.py" "$TARGET_DIR/"
else
    # Fallback if run directly from inside the folder itself
    cp "Import Media.py" "$TARGET_DIR/" 2>/dev/null || true
    cp "Import Bin.py" "$TARGET_DIR/" 2>/dev/null || true
fi

echo "====================================================="
echo " 🎉 Installation Complete!"
echo "====================================================="
echo " The utilities are now available in DaVinci Resolve under:"
echo " Workspace -> Scripts -> Import Media / Import Bin"
echo ""
echo " Feel free to assign custom hotkeys in Keyboard Customization."
