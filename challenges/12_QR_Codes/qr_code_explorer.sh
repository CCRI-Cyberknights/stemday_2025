#!/bin/bash

clear

echo "📦 QR Code Explorer"
echo "=========================="
echo
echo "You've discovered a set of mysterious QR codes."
echo
echo "Each one might contain a message — or even the correct flag!"
echo
echo "🔍 You may:"
echo "  • Scan each image with your phone's QR code app"
echo "  • Or let this script automatically decode it for you"
echo
echo "🕒 Each QR will open in the image viewer for 20 seconds."
echo "After that, the decoded result (if found) will be saved"
echo "to a matching .txt file (e.g., qr_03.txt)."
echo
read -p "Press ENTER to begin exploring."
clear

qr_codes=(qr_01.png qr_02.png qr_03.png qr_04.png qr_05.png)

while true; do
    echo "Available QR codes:"
    for i in "${!qr_codes[@]}"; do
        echo "$((i+1)). ${qr_codes[$i]}"
    done
    echo "6. Exit"
    echo

    read -p "Select a QR code to view and decode (1-5), or 6 to exit: " choice

    if [[ "$choice" == "6" ]]; then
        echo "Exiting QR Code Explorer."
        break
    fi

    index=$((choice - 1))
    if [[ "$index" -ge 0 && "$index" -lt 5 ]]; then
        file="${qr_codes[$index]}"
        echo
        echo "Opening $file in image viewer for 20 seconds..."

        xdg-open "$file" >/dev/null 2>&1
        echo "(You have 20 seconds to view the image...)"
        sleep 20
        pkill -f "eom" >/dev/null 2>&1

        echo
        echo "🔎 Scanning QR code in $file..."
        result=$(zbarimg "$file" 2>/dev/null)

        if [[ -z "$result" ]]; then
            echo "❌ No QR code found or unable to decode."
        else
            echo "$result"
            echo "$result" > "${file%.png}.txt"
            echo "✅ Decoded result saved to ${file%.png}.txt"
        fi
        echo
        read -p "Press ENTER to continue."
        clear
    else
        echo "❌ Invalid choice. Please enter a number from 1 to 6."
        read -p "Press ENTER to continue."
        clear
    fi

done
