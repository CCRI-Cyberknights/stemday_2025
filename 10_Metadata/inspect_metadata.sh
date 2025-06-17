#!/bin/bash
clear
echo "📸 Metadata Inspection Tool"
echo "----------------------------"
echo

# Verify file exists
if [[ ! -f capybara.jpg ]]; then
    echo "❌ Error: capybara.jpg not found in this folder!"
    echo "Make sure the image file is present before running this script."
    exit 1
fi

echo "Looking at: capybara.jpg"
echo "Saving metadata to: metadata_dump.txt"
echo
read -p "Press ENTER to inspect the file with exiftool..."

echo
exiftool capybara.jpg | tee metadata_dump.txt
echo
echo "✅ Metadata has been saved to 'metadata_dump.txt'."
echo "👀 Look carefully — only one flag is correct."
echo
read -p "Press ENTER to exit."
