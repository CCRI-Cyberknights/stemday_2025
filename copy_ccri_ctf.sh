#!/bin/bash

# === CCRI_CTF Folder Overwrite Copy Script ===
# Copies the folder this script is in to /home/ccri_stem/Desktop/
# Skips copying this script itself
# Always overwrites existing files

# Resolve the directory where this script is located
SCRIPT_PATH="$(realpath "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
SCRIPT_NAME="$(basename "$SCRIPT_PATH")"
FOLDER_NAME="$(basename "$SCRIPT_DIR")"

# Set destination to same folder name under ccri_stem Desktop
DEST="/home/ccri_stem/Desktop/$FOLDER_NAME"

# Dry run flag
DRY_RUN=false

echo "🔄 CCRI_CTF Overwrite Copy Script"
echo "=================================="
echo
echo "📂 Source folder: $SCRIPT_DIR"
echo "📂 Destination folder: $DEST"
echo

# Ask if user wants to do a dry run
read -p "Do a dry run first? (y/n): " yn
case $yn in
    [Yy]* ) DRY_RUN=true ;;
    * ) DRY_RUN=false ;;
esac

# Perform rsync with overwrite
if $DRY_RUN; then
    echo "📝 Dry run: showing what would be copied..."
    rsync -avhcn --progress \
        --exclude "$SCRIPT_NAME" \
        "$SCRIPT_DIR/" "$DEST/"
    echo
    echo "✅ Dry run complete. No files were copied."
else
    echo "📂 Copying and overwriting all files from:"
    echo "   $SCRIPT_DIR"
    echo "➡️  To:"
    echo "   $DEST"
    echo
    rsync -avhc --progress \
        --exclude "$SCRIPT_NAME" \
        "$SCRIPT_DIR/" "$DEST/"

    # Set ownership
    echo "🔑 Setting ownership to ccri_stem..."
    chown -R ccri_stem:ccri_stem "$DEST"

    # Set permissions
    echo "🔒 Adjusting permissions..."
    chmod -R u+rwX,go-w "$DEST"

    echo
    echo "✅ Overwrite copy complete. Ownership and permissions fixed."
fi

echo
echo "🎯 Done! Switch to ccri_stem to test:"
echo "    su - ccri_stem"
echo "    cd ~/Desktop/$FOLDER_NAME"
echo
