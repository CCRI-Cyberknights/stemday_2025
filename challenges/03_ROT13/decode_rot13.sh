#!/bin/bash

clear
echo "🔐 ROT13 Decoder Helper"
echo "==========================="
echo
echo "📄 File to analyze: cipher.txt"
echo "🎯 Goal: Decode this message and find the hidden CCRI flag."
echo
echo "💡 What is ROT13?"
echo "   ➡️ A simple Caesar cipher that shifts each letter 13 places in the alphabet."
echo "   ➡️ Encoding and decoding use the same operation because 13+13=26 (a full loop!)."
echo
read -p "Press ENTER to learn how the decoder works..."

# Explain the decoding process
clear
echo "🛠️ Behind the Scenes"
echo "---------------------------"
echo "We’ll use a Python helper to process each character:"
echo
echo "   For every letter in cipher.txt:"
echo "     ➡️ Rotate it forward by 13 places (A→N, N→A)."
echo
echo "💻 The Python decoder also animates this process so you can watch it work."
echo
read -p "Press ENTER to launch the animated decoder..." temp

# Run the Python decoder
python3 - <<'EOF'
import time
import os
import sys

# Check if cipher.txt exists
if not os.path.isfile("cipher.txt") or os.path.getsize("cipher.txt") == 0:
    print("\n❌ ERROR: cipher.txt is missing or empty.")
    sys.exit(1)

with open("cipher.txt", "r") as f:
    encoded = f.read()

def rot13_char(c):
    if 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
    else:
        return c

def animate_rot13(encoded_text):
    decoded_chars = list(encoded_text)
    for i in range(len(encoded_text)):
        c = encoded_text[i]
        if c.isalpha():
            for step in range(13):
                rotated = chr(((ord(c.lower()) - ord('a') + step) % 26 + ord('a')))
                if c.isupper():
                    rotated = rotated.upper()
                decoded_chars[i] = rotated
                os.system("clear")
                print("🔐 ROT13 Decoder Helper")
                print("===========================\n")
                print("🌀 Decrypting:\n")
                print("".join(decoded_chars))
                time.sleep(0.02)
            decoded_chars[i] = rot13_char(c)
    return "".join(decoded_chars)

final_message = animate_rot13(encoded)

# Save decoded output
with open("decoded_output.txt", "w") as f_out:
    f_out.write(final_message)

# Display the result
print("\n✅ Final Decoded Message:")
print("-----------------------------")
print(final_message)
print("-----------------------------")
print("📁 Saved to: decoded_output.txt")
EOF

# Check for Python failure
if [[ $? -ne 0 ]]; then
    echo -e "\n⚠️ ROT13 decoding failed. Make sure cipher.txt exists and is valid."
    read -p "Press ENTER to close this terminal..."
    exit 1
fi

echo
echo "🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111"
echo "📋 Copy the correct flag and paste it into the scoreboard when ready."
echo
read -p "Press ENTER to close this terminal..."
exec $SHELL
