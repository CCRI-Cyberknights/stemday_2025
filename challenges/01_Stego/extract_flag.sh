#!/bin/bash

clear
echo "🕵️ Stego Decode Terminal"
echo "========================="
echo
echo "🎯 Target image: squirrel.jpg"
echo "🔍 Tool in use: steghide"
echo "💡 Goal: Recover a hidden flag embedded in the image!"
echo
echo "🔧 Quick Note:"
echo "   'steghide' is a Linux tool that can HIDE or EXTRACT messages inside image or audio files."
echo "   We'll use it to try to extract a hidden message from squirrel.jpg using a password."
echo
read -p "Press ENTER to begin password testing..."

while true; do
    read -p "🔑 Enter the password to try (or type 'exit' to quit): " pw

    if [[ -z "$pw" ]]; then
        echo "⚠️ You must enter something. Try again."
        continue
    fi

    if [[ "$pw" == "exit" ]]; then
        echo "👋 Exiting... good luck on your next mission."
        read -p "Press ENTER to close this window..."
        exit 0
    fi

    echo -ne "\n🔓 Trying password"
    for i in {1..3}; do sleep 0.4; echo -n "."; done
    echo

    echo -ne "📦 Scanning squirrel.jpg for hidden data using steghide"
    for i in {1..4}; do sleep 0.3; echo -n "."; done
    echo

    echo
    echo "🛠️ Running: steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]"
    echo "   -sf = stego file (squirrel.jpg)"
    echo "   -xf = extract to this file (decoded_message.txt)"
    echo "   -p  = use this password"
    echo

    # Attempt extraction (force non-interactive to prevent hanging)
    steghide extract -sf squirrel.jpg -xf decoded_message.txt -p "$pw" -f <<< "" > /dev/null 2>&1
    status=$?

    if [[ $status -eq 0 && -s decoded_message.txt ]]; then
        echo
        echo "🎉 SUCCESS! Hidden message recovered:"
        echo "----------------------------"
        cat decoded_message.txt
        echo "----------------------------"
        echo "📁 A copy has been saved as decoded_message.txt"
        echo "🔎 Review the contents carefully. Only one string matches the CCRI-AAAA-1111 format."
        echo
        read -p "Press ENTER to close this terminal..."
        exec $SHELL
    else
        echo
        echo "❌ Extraction failed. No data recovered or incorrect password."
        echo "🔁 Try again with a different password."
        echo
        # Clean up any empty/partial file
        rm -f decoded_message.txt
    fi
done
