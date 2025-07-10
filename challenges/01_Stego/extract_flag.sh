#!/bin/bash

clear
echo "🕵️ Stego Decode Helper"
echo "=========================="
echo
echo "🎯 Target image: squirrel.jpg"
echo "🔍 Tool: steghide"
echo
echo "💡 What is steghide?"
echo "   ➡️ A Linux tool that can HIDE or EXTRACT secret data inside images or audio files."
echo "   We'll use it to try and extract a hidden message from squirrel.jpg."
echo
read -p "Press ENTER to learn how this works..."

# Explain the extraction command
clear
echo "🛠️ Behind the Scenes"
echo "---------------------------"
echo "When we try a password, this command will run:"
echo
echo "   steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]"
echo
echo "🔑 Breakdown:"
echo "   -sf squirrel.jpg   → Stego file (the image to scan)"
echo "   -xf decoded_message.txt → Extract to this file"
echo "   -p [password]      → Try this password for extraction"
echo
read -p "Press ENTER to begin password testing..."

# Begin password testing loop
while true; do
    read -p "🔑 Enter a password to try (or type 'exit' to quit): " pw

    if [[ -z "$pw" ]]; then
        echo "⚠️ You must enter something. Try again."
        continue
    fi

    if [[ "$pw" == "exit" ]]; then
        echo
        echo "👋 Exiting... good luck on your next mission!"
        read -p "Press ENTER to close this window..."
        exit 0
    fi

    echo
    echo "🔓 Trying password: $pw"
    sleep 0.5
    echo "📦 Scanning squirrel.jpg for hidden data..."
    sleep 1

    # Show command (simulated)
    echo
    echo "💻 Running: steghide extract -sf squirrel.jpg -xf decoded_message.txt -p \"$pw\""
    echo

    # Attempt extraction (force non-interactive, suppress errors)
    steghide extract -sf squirrel.jpg -xf decoded_message.txt -p "$pw" -f <<< "" > /dev/null 2>&1
    status=$?

    if [[ $status -eq 0 && -s decoded_message.txt ]]; then
        echo
        echo "🎉 ✅ SUCCESS! Hidden message recovered:"
        echo "----------------------------"
        cat decoded_message.txt
        echo "----------------------------"
        echo "📁 Saved as decoded_message.txt"
        echo "💡 Look for a string like CCRI-ABCD-1234 to use as your flag."
        echo
        read -p "Press ENTER to close this terminal..."
        exec $SHELL
    else
        echo
        echo "❌ Extraction failed. No hidden data or incorrect password."
        echo "🔁 Try again with a different password."
        echo
        # Clean up any empty/partial file
        rm -f decoded_message.txt
    fi
done
