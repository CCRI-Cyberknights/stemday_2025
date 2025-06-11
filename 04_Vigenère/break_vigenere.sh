#!/bin/bash

clear
echo "🔐 Vigenère Cipher Breaker"
echo "==========================="
echo
echo "📄 You've recovered a scrambled message from: cipher.txt"
echo "🔍 Analysts believe it's encrypted using the Vigenère cipher — a classic cipher that uses a repeating keyword."
echo
echo "🔧 Quick Note:"
echo "   The Vigenère cipher shifts each letter based on the letters in a keyword."
echo "   For example, with the keyword 'KEY', the first letter shifts by K, the second by E, the third by Y, then repeats."
echo
echo "💡 Goal: Try different keywords until the decrypted message reveals a valid flag in the format: CCRI-AAAA-1111"
echo
read -p "Press ENTER to begin..." temp

while true; do
    read -p "🔑 Enter a keyword to try (or type 'exit' to quit): " key

    if [[ "$key" == "exit" ]]; then
        echo "👋 Exiting. Stay sharp, Agent."
        break
    fi

    if [[ ! -f cipher.txt ]]; then
        echo "❌ Error: cipher.txt not found in this folder."
        exit 1
    fi

    echo
    echo "🛠️ Running Vigenère decryption with keyword: $key"
    echo "   → This attempts to reverse the shifting pattern applied with the keyword."
    echo

    # Run Python decoder using key and cipher.txt
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
        echo "✅ Valid flag format detected!"
        echo "$decoded" > decoded_output.txt
        echo "📁 Decoded output saved to: decoded_output.txt"
        break
    else
        echo "❌ No valid CCRI flag format found. Try another key."
    fi

    echo
    read -p "Try another keyword? (Y/n): " again
    while [[ ! "$again" =~ ^[YyNn]?$ ]]; do
        read -p "Please enter Y or N: " again
    done
    [[ "$again" =~ ^[Nn]$ ]] && break
done

echo
read -p "Press ENTER to close this terminal..." close
