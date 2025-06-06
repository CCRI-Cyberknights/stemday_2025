#!/bin/bash

clear
echo "🕵️ Stego Decode Terminal"
echo "========================="
echo
echo "🎯 Target image: squirrel.jpg"
echo "🔍 Tool in use: steghide"
echo "💡 Goal: Recover a hidden flag embedded in the image!"
echo

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

    # Remove previous extraction result
    [ -f decoded_message.txt ] && rm decoded_message.txt

    echo -ne "\n🔓 Attempting password authentication"
    for i in {1..3}; do sleep 0.4; echo -n "."; done
    echo

    echo -ne "📦 Scanning squirrel.jpg for embedded content"
    for i in {1..4}; do sleep 0.3; echo -n "."; done
    echo

    # Attempt extraction
    steghide extract -sf squirrel.jpg -xf decoded_message.txt -p "$pw" > /dev/null 2>&1

    if [[ -f decoded_message.txt ]]; then
        echo
        echo "🎉 SUCCESS! Hidden message recovered:"
        echo "----------------------------"
        cat decoded_message.txt
        echo "----------------------------"
        echo "📁 A copy has been saved as decoded_message.txt"
        echo "🔎 Review the contents carefully. Only one string matches the CCRI-XXX-### format."
        echo
        read -p "Press ENTER to close this terminal..." done
        exec $SHELL
    else
        echo
        echo "❌ Extraction failed. No data recovered or incorrect password."
        echo "🔁 Try again with a different password."
        echo
    fi
done
