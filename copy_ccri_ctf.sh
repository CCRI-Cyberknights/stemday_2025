#!/bin/bash

# === CCRI_CTF Selective Copy Script ===
# Copies CCRI_CTF folder to the ccri_stem account Desktop
# Finds project root automatically and preserves ownership/permissions

# === Resolve project root ===
find_project_root() {
    DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    while [ "$DIR" != "/" ]; do
        if [ -f "$DIR/.ccri_ctf_root" ]; then
            echo "$DIR"
            return 0
        fi
        DIR="$(dirname "$DIR")"
    done
    echo "❌ ERROR: Could not find project root marker (.ccri_ctf_root)." >&2
    read -p "Press ENTER to exit..." junk
    exit 1
}

PROJECT_ROOT="$(find_project_root)"
SRC="$PROJECT_ROOT"
STUDENT_USER="ccri_stem"
DEST="/home/$STUDENT_USER/Desktop/CCRI_CTF"

# === Dry run flag ===
DRY_RUN=false

echo "🔄 CCRI_CTF Selective Copy Script (Overwrite Mode)"
echo "=================================================="
echo

read -p "Do a dry run first? (y/n): " yn
case $yn in
    [Yy]* ) DRY_RUN=true ;;
    * ) DRY_RUN=false ;;
esac

# === Check for existing destination ===
if [ -d "$DEST" ]; then
    echo "⚠️  Existing CCRI_CTF folder found at $DEST"
    read -p "Delete existing folder before copying? (y/n): " delete_yn
    case $delete_yn in
        [Yy]* )
            echo "🗑️  Deleting $DEST..."
            sudo rm -rf "$DEST"
            echo "✅ Old folder removed."
            ;;
        * )
            echo "🚫 Aborting: Folder already exists and not deleted."
            read -p "Press ENTER to exit..." junk
            exit 1
            ;;
    esac
fi

# === Perform rsync ===
if $DRY_RUN; then
    echo "📝 Dry run: showing what would be copied..."
    rsync -avhn --progress \
        --include ".ccri_ctf_root" \
        --include "challenges/***" \
        --include "web_version/***" \
        --include "Launch CCRI CTF Hub.desktop" \
        --exclude "*" \
        "$SRC/" "$DEST/"
    echo
    echo "✅ Dry run complete. No files were copied."

else
    echo "📂 Copying selected files from:"
    echo "   $SRC"
    echo "➡️  To:"
    echo "   $DEST"
    echo

    # Use rsync without preserving source ownership
    sudo rsync -avh --progress \
        --no-o --no-g \
        --include ".ccri_ctf_root" \
        --include "challenges/***" \
        --include "web_version/***" \
        --include "Launch CCRI CTF Hub.desktop" \
        --exclude "*" \
        "$SRC/" "$DEST/"

    # Set ownership for all copied files to student
    echo "🔑 Setting ownership to $STUDENT_USER..."
    sudo chown -R "$STUDENT_USER:$STUDENT_USER" "$DEST"

    # Set permissions
    echo "🔒 Adjusting permissions..."
    sudo chmod -R u+rwX,go-w "$DEST"

    echo
    echo "✅ Selective copy complete. Ownership and permissions fixed."
fi

# === Summary of Copied Content ===
echo
echo "📄 Summary of $DEST:"
echo "-----------------------------------"
sudo ls -lah "$DEST" | head -n 10
echo "..."

# Show a few sample files
echo
echo "📁 Sample from challenges/:"
sudo ls -lah "$DEST/challenges" | head -n 5
echo "..."

echo "📁 Sample from web_version/:"
sudo ls -lah "$DEST/web_version" | head -n 5
echo "..."

# Confirm .ccri_ctf_root presence and ownership
if [[ -f "$DEST/.ccri_ctf_root" ]]; then
    echo "✅ Found .ccri_ctf_root in $DEST"
    echo "   Ownership:"
    ls -lah "$DEST/.ccri_ctf_root"
else
    echo "⚠️ .ccri_ctf_root not found in $DEST"
fi

echo
echo "🎯 Done! Switch to $STUDENT_USER to test:"
echo "    su - $STUDENT_USER"
echo "    cd ~/Desktop/CCRI_CTF"
read -p "📖 Press ENTER to exit..." junk
