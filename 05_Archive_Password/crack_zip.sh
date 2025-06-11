#!/bin/bash

clear
echo "🔓 ZIP Password Cracking"
echo "==========================="
echo
echo "Target archive: secret.zip"
echo "Wordlist: wordlist.txt"
echo

found=0
correct_pass=""

# Try each password and display it
while read -r pw; do
    # Clear line properly by padding with spaces
    printf "\r[🔐] Trying password: %-20s" "$pw"
    sleep 0.05
    if unzip -P "$pw" -t secret.zip 2>/dev/null | grep -q "OK"; then
        echo -e "\n\n✅ Password found: $pw"
        correct_pass="$pw"
        found=1
        break
    fi
done < wordlist.txt

if [[ "$found" -eq 0 ]]; then
    echo -e "\n❌ Password not found in the list."
    exit 1
fi

# Ask to proceed
echo
read -p "Proceed to extract the ZIP archive? [Y/n] " go
while [[ ! "$go" =~ ^[YyNn]?$ ]]; do
    read -p "Please enter Y or N: " go
done
[[ "$go" =~ ^[Nn]$ ]] && exit 0

# Extract the ZIP archive using the found password
unzip -P "$correct_pass" secret.zip >/dev/null 2>&1

if [[ ! -f message_encoded.txt ]]; then
    echo "❌ Extraction failed."
    exit 1
fi

# Show base64 content first
echo
echo "📦 Extracted Base64 Data:"
echo "-----------------------------"
cat message_encoded.txt
echo "-----------------------------"

# Prompt before decoding
echo
read -p "Would you like to decode the Base64 message now? [Y/n] " decode
while [[ ! "$decode" =~ ^[YyNn]?$ ]]; do
    read -p "Please enter Y or N: " decode
done

if [[ "$decode" =~ ^[Nn]$ ]]; then
    echo "❌ Skipping Base64 decoding. You can decode it manually later using: base64 --decode message_encoded.txt"
    exit 0
fi

# Decoding animation
echo
echo "🔽 Decoding Base64:"
for i in {1..20}; do
    sleep 0.05
    echo -n "█"
done
echo -e "\n"

# Decode the base64 message
decoded=$(base64 --decode message_encoded.txt 2>/dev/null)

echo
echo "🧾 Decoded Message:"
echo "-----------------------------"
echo "$decoded"
echo "-----------------------------"

# Save decoded output
echo "$decoded" > decoded_output.txt
echo "💾 Decoded message saved to: decoded_output.txt"

echo
echo "🧠 Pick the valid flag from the list (format: CCRI-AAAA-1111) and enter it into the scoreboard."
read -p "Press ENTER to close this terminal..." done
