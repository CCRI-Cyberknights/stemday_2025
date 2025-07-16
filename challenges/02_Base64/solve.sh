#!/bin/bash

# === Base64 Decoder Helper ===

# === Locate Project Root ===
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

clear
echo "🧩 Base64 Decoder Helper"
echo "==========================="
echo
echo "📄 File to analyze: encoded.txt"
echo "🎯 Goal: Decode this file and find the hidden CCRI flag."
echo
echo "💡 What is Base64?"
echo "   ➡️ A text-based encoding scheme that turns binary data into readable text."
echo "   Used to safely transmit data over systems that handle text better than raw binary."
echo
echo "🔧 We'll use the Linux tool 'base64' to reverse the encoding."
echo
read -p "Press ENTER to learn how this works..."

# Explain the decoding command
clear
echo "🛠️ Behind the Scenes"
echo "---------------------------"
echo "To decode the file, we’ll run:"
echo
echo "   base64 --decode encoded.txt"
echo
echo "🔑 Breakdown:"
echo "   base64         → Call the Base64 tool"
echo "   --decode       → Switch from encoding to decoding"
echo "   encoded.txt    → Input file to decode"
echo
read -p "Press ENTER to begin decoding..."

# Simulate analysis
echo
echo "🔍 Checking file for Base64 structure..."
sleep 1
echo "✅ Structure confirmed!"
sleep 0.5

echo
echo "⏳ Decoding content using:"
echo "   base64 --decode \"$SCRIPT_DIR/encoded.txt\""
sleep 1

# Perform decoding
decoded=$(base64 --decode "$SCRIPT_DIR/encoded.txt" 2>/dev/null)
status=$?

if [[ $status -ne 0 || -z "$decoded" ]]; then
    echo
    echo "❌ Decoding failed! This may not be valid Base64, or the file is corrupted."
    echo "💡 Tip: Ensure 'encoded.txt' exists and contains proper Base64 text."
    read -p "Press ENTER to close this terminal..."
    exit 1
fi

# Display and save decoded output
echo
echo "📄 Decoded Message:"
echo "-----------------------------"
echo "$decoded"
echo "-----------------------------"
echo "$decoded" > "$SCRIPT_DIR/decoded_output.txt"

echo
echo "📁 Decoded output saved as: $SCRIPT_DIR/decoded_output.txt"
echo "🔎 Look for a string matching this format: CCRI-AAAA-1111"
echo "🧠 This is your flag. Copy it into the scoreboard!"
echo
read -p "Press ENTER to close this terminal..."
exec $SHELL
