#!/bin/bash

clear
echo "🔐 Vigenère Cipher Breaker"
echo "==============================="
echo
echo "📄 Encrypted message: cipher.txt"
echo "🎯 Goal: Decrypt it and find the CCRI flag."
echo
echo "💡 What is Vigenère?"
echo "   ➡️ A cipher that uses a repeating keyword to shift each letter."
echo "   ➡️ For example, with keyword 'KEY':"
echo "         Plain:  HELLO WORLD"
echo "         Cipher: RIJVS UYVJN"
echo
echo "   Each letter in the keyword decides how far to shift the plaintext letters."
echo
read -p "Press ENTER to learn how we’ll decode this..." temp

# Explain decryption command
clear
echo "🛠️ Behind the Scenes"
echo "-----------------------------"
echo "We’ll use this Python helper:"
echo
echo "   python3 vigenere_decode.py [keyword]"
echo
echo "🔑 It reverses the shifting pattern based on your keyword."
echo "   If the keyword is correct, the flag will appear!"
echo
read -p "Press ENTER to begin keyword testing..." temp

# Check for cipher.txt first
if [[ ! -f cipher.txt ]]; then
    echo "❌ ERROR: cipher.txt not found in this folder."
    read -p "Press ENTER to close this terminal..." temp
    exit 1
fi

# Start keyword attempt loop
while true; do
    read -p "🔑 Enter a keyword to try (or type 'exit' to quit): " key

    if [[ "$key" == "exit" ]]; then
        echo
        echo "👋 Exiting. Stay sharp, Agent!"
        break
    fi

    if [[ -z "$key" ]]; then
        echo "⚠️ Please enter a keyword or type 'exit'."
        continue
    fi

    echo
    echo "🔓 Attempting decryption with keyword: $key"
    sleep 0.5

    # Run Python decoder
    decoded=$(python3 - "$key" <<'EOF'
import sys
from itertools import cycle

key = sys.argv[1]
filename = "cipher.txt"

try:
    with open(filename, "r") as f:
        ciphertext = f.read()
except FileNotFoundError:
    print("❌ cipher.txt not found.")
    sys.exit(1)

def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
    key_len = len(key)
    key_indices = [ord(k) - ord('a') for k in key]
    key_pos = 0

    for char in ciphertext:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            pi = ord(char) - offset
            ki = key_indices[key_pos % key_len]
            decrypted = chr((pi - ki) % 26 + offset)
            result.append(decrypted)
            key_pos += 1
        else:
            result.append(char)
    return ''.join(result)

print(vigenere_decrypt(ciphertext, key))
EOF
    )

    echo
    echo "📄 Decoded Output:"
    echo "-----------------------------"
    echo "$decoded"
    echo "-----------------------------"
    echo

    if echo "$decoded" | grep -qE 'CCRI-[A-Z]{4}-[0-9]{4}'; then
        echo "✅ Flag found in decrypted text!"
        echo "$decoded" > decoded_output.txt
        echo "📁 Saved to: decoded_output.txt"
        echo "📋 Copy the CCRI flag and submit it on the scoreboard."
        break
    else
        echo "❌ No valid CCRI flag format detected."
    fi

    echo
    read -p "🔁 Try another keyword? (Y/n): " again
    while [[ ! "$again" =~ ^[YyNn]?$ ]]; do
        read -p "Please enter Y or N: " again
    done
    [[ "$again" =~ ^[Nn]$ ]] && break
done

echo
read -p "Press ENTER to close this terminal..."
exec $SHELL
