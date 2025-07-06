#!/bin/bash

clear
echo "🔐 ROT13 Decoder Terminal"
echo "=========================="
echo
echo "📄 You've recovered a scrambled message from: cipher.txt"
echo "🔍 Agency analysts suspect it's been encoded using the ROT13 cipher."
echo
echo "🔧 Quick Note:"
echo "   ROT13 is a simple Caesar cipher that shifts each letter 13 places."
echo "   It's symmetrical — encoding and decoding are the same operation!"
echo
read -p "Press ENTER to begin decoding..." temp

echo -ne "[🔄] Scanning content"
for i in {1..3}; do sleep 0.4; echo -n "."; done
echo -e "\n[✅] ROT13 structure confirmed.\n"
sleep 0.5

echo "🌀 Running animated ROT13 decoder using Python..."
sleep 0.5

# Inline Python animation
python3 - <<'EOF'
import time
import os
import sys

# Check if file exists and is non-empty
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
                print("🔐 ROT13 Decoder Terminal")
                print("==========================\n")
                print("🌀 Decrypting:\n")
                print("".join(decoded_chars))
                time.sleep(0.02)
            decoded_chars[i] = rot13_char(c)
    return "".join(decoded_chars)

final_message = animate_rot13(encoded)

# Save final output
with open("decoded_output.txt", "w") as f_out:
    f_out.write(final_message)

# Final display
print("\n✅ Final Decoded Message:")
print("-----------------------------")
print(final_message)
print("-----------------------------")
print("📁 Saved to: decoded_output.txt")
EOF

# Check if decoding failed
if [[ $? -ne 0 ]]; then
    echo -e "\n⚠️ ROT13 decoding failed. Check if cipher.txt exists and is valid."
    read -p "Press ENTER to close this terminal..."
    exit 1
fi

echo
echo "⚠️  Multiple code-like values detected."
echo "🔎 Only one matches the official flag format: CCRI-AAAA-1111"
echo "🧠 Review the decoded message and copy the correct flag to submit on the scoreboard."
echo
read -p "Press ENTER to close this terminal..."
exec $SHELL
