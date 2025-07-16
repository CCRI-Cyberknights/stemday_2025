#!/bin/bash

# === QR Code Explorer ===

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

clear

echo "📦 QR Code Explorer"
echo "=========================="
echo
echo "🎯 Mission Briefing:"
echo "----------------------------"
echo "🔍 You’ve recovered 5 mysterious QR codes from a digital drop site."
echo "Each one may contain:"
echo "  • A secret message"
echo "  • A fake flag"
echo "  • Or… the **real flag** in CCRI-AAAA-1111 format!"
echo
echo "🛠️ Your options:"
echo "  • Scan with your phone’s QR scanner"
echo "  • OR use this tool to open and auto-decode them"
echo
echo "📖 Behind the scenes:"
echo "   This script runs:"
echo "      zbarimg qr_XX.png"
echo "   → zbarimg scans and decodes barcodes/QR codes from images."
echo
echo "⏳ Each QR image will open in the viewer for **20 seconds**."
echo "   After that, the decoded result (if any) is saved to a text file."
echo
read -p "Press ENTER to begin exploring." junk
clear

# QR code files (resolved to script directory)
qr_codes=("$SCRIPT_DIR/qr_01.png" "$SCRIPT_DIR/qr_02.png" "$SCRIPT_DIR/qr_03.png" "$SCRIPT_DIR/qr_04.png" "$SCRIPT_DIR/qr_05.png")

while true; do
    echo "🗂️  Available QR codes:"
    for i in "${!qr_codes[@]}"; do
        echo "$((i+1)). $(basename "${qr_codes[$i]}")"
    done
    echo "6. Exit Explorer"
    echo

    read -p "Select a QR code to view and decode (1-5), or 6 to exit: " choice

    if [[ "$choice" == "6" ]]; then
        echo
        echo "👋 Exiting QR Code Explorer. Don’t forget to submit the correct flag!"
        break
    fi

    index=$((choice - 1))
    if [[ "$index" -ge 0 && "$index" -lt ${#qr_codes[@]} ]]; then
        file="${qr_codes[$index]}"
        txt_file="${file%.png}.txt"

        echo
        echo "🖼️ Opening $(basename "$file") in image viewer for 20 seconds..."
        xdg-open "$file" >/dev/null 2>&1 & viewer_pid=$!

        sleep 20
        echo "⏳ Time’s up! Closing the viewer..."
        kill "$viewer_pid" 2>/dev/null

        echo
        echo "🔎 Scanning QR code in $(basename "$file")..."
        echo "💻 Running: zbarimg \"$file\""
        echo

        result=$(zbarimg "$file" 2>/dev/null)

        if [[ -z "$result" ]]; then
            echo "❌ No QR code found or unable to decode."
        else
            echo "✅ Decoded result:"
            echo "----------------------------"
            echo "$result"
            echo "----------------------------"
            echo "$result" > "$txt_file"
            echo "💾 Saved to: $(basename "$txt_file")"
        fi

        echo
        read -p "Press ENTER to return to QR list..." junk
        clear
    else
        echo "❌ Invalid choice. Please enter a number from 1 to 6."
        read -p "Press ENTER to continue..." junk
        clear
    fi

done

# Clean exit for web hub
exec $SHELL
