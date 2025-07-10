#!/bin/bash
clear
echo "📸 Metadata Inspection Tool"
echo "============================"
echo
echo "🎯 Target image: capybara.jpg"
echo "🔧 Tool in use: exiftool"
echo
echo "💡 Why exiftool?"
echo "   ➡️ Images often carry *hidden metadata* like camera info, GPS tags, or embedded comments."
echo "   ➡️ This data can hide secrets — including CTF flags!"
echo
# Verify file exists
if [[ ! -f capybara.jpg ]]; then
    echo "❌ ERROR: capybara.jpg not found in this folder!"
    echo "Make sure the image file is present before running this script."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

echo "📂 Inspecting: capybara.jpg"
echo "📄 Saving metadata to: metadata_dump.txt"
echo
read -p "Press ENTER to run exiftool and extract metadata..." junk

# Run exiftool and save results
echo
echo "🛠️ Running: exiftool capybara.jpg > metadata_dump.txt"
sleep 0.5
exiftool capybara.jpg | tee metadata_dump.txt

echo
echo "✅ All metadata saved to: metadata_dump.txt"
echo

# Gamify exploration
echo "👀 Let’s preview a few key fields:"
echo "----------------------------------------"
grep -E "Camera|Date|Comment|Artist|CCRI" metadata_dump.txt || echo "⚠️ No common fields found."
echo "----------------------------------------"
echo
sleep 0.5

# Optional search
read -p "🔎 Enter a keyword to search in the metadata (or press ENTER to skip): " keyword
if [[ -n "$keyword" ]]; then
    echo
    echo "🔎 Searching for '$keyword' in metadata_dump.txt..."
    grep -i --color=always "$keyword" metadata_dump.txt || echo "⚠️ No matches found for '$keyword'."
else
    echo "⏭️  Skipping custom search."
fi

echo
echo "🧠 One of these fields hides the correct flag in the format: CCRI-AAAA-1111"
echo "📋 When you find it, copy it into the scoreboard!"
echo
read -p "Press ENTER to close this terminal..." junk
exec $SHELL
