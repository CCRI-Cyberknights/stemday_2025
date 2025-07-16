#!/bin/bash

# === Metadata Inspection Tool ===

# Locate Project Root
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
    exit 1
}

PROJECT_ROOT="$(find_project_root)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET_IMAGE="$SCRIPT_DIR/capybara.jpg"
OUTPUT_FILE="$SCRIPT_DIR/metadata_dump.txt"

clear
echo "📸 Metadata Inspection Tool"
echo "============================"
echo
echo "🎯 Target image: $(basename "$TARGET_IMAGE")"
echo "🔧 Tool in use: exiftool"
echo
echo "💡 Why exiftool?"
echo "   ➡️ Images often carry *hidden metadata* like camera info, GPS tags, or embedded comments."
echo "   ➡️ This data can hide secrets — including CTF flags!"
echo

# Verify file exists
if [[ ! -f "$TARGET_IMAGE" ]]; then
    echo "❌ ERROR: $(basename "$TARGET_IMAGE") not found in this folder!"
    echo "Make sure the image file is present before running this script."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

echo "📂 Inspecting: $(basename "$TARGET_IMAGE")"
echo "📄 Saving metadata to: $(basename "$OUTPUT_FILE")"
echo
read -p "Press ENTER to run exiftool and extract metadata..." junk

# Run exiftool and save results
echo
echo "🛠️ Running: exiftool $(basename "$TARGET_IMAGE") > $(basename "$OUTPUT_FILE")"
sleep 0.5
exiftool "$TARGET_IMAGE" | tee "$OUTPUT_FILE"

echo
echo "✅ All metadata saved to: $(basename "$OUTPUT_FILE")"
echo

# Gamify exploration
echo "👀 Let’s preview a few key fields:"
echo "----------------------------------------"
grep -E "Camera|Date|Comment|Artist|CCRI" "$OUTPUT_FILE" || echo "⚠️ No common fields found."
echo "----------------------------------------"
echo
sleep 0.5

# Optional search
read -p "🔎 Enter a keyword to search in the metadata (or press ENTER to skip): " keyword
if [[ -n "$keyword" ]]; then
    echo
    echo "🔎 Searching for '$keyword' in $(basename "$OUTPUT_FILE")..."
    grep -i --color=always "$keyword" "$OUTPUT_FILE" || echo "⚠️ No matches found for '$keyword'."
else
    echo "⏭️  Skipping custom search."
fi

echo
echo "🧠 One of these fields hides the correct flag in the format: CCRI-AAAA-1111"
echo "📋 When you find it, copy it into the scoreboard!"
echo
read -p "Press ENTER to close this terminal..." junk
exec $SHELL
