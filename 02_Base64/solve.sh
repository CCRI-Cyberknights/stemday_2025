#!/bin/bash

clear
echo "🧩 Base64 Decoder Terminal"
echo "--------------------------"
echo
echo "You've recovered a suspicious message fragment: encoded.txt"
echo "Analysts believe it may contain an encoded message using the base64 format."
echo

read -p "Press ENTER to begin the scan..." junk

# Simulated analysis
echo -ne "\n[🔍] Scanning file for suspicious patterns"
for i in {1..3}; do sleep 0.4; echo -n "."; done
echo -e "\n[✅] Base64 structure confirmed."
sleep 0.5

echo -ne "[🔄] Preparing decoding pipeline"
for i in {1..3}; do sleep 0.3; echo -n "."; done
echo -e "\n[✅] Decoding initialized."
sleep 0.5

echo -ne "[⏳] Decoding content"
for i in {1..3}; do sleep 0.4; echo -n "."; done
echo

# Perform actual decoding
decoded=$(base64 --decode encoded.txt 2>/dev/null)

if [[ -z "$decoded" ]]; then
    echo -e "\n⚠️ Decoding failed! This may not be valid base64, or the file is malformed."
    exit 1
fi

# Display and save decoded output
echo -e "\n📄 Decoded Message:"
echo "------------------------"
echo "$decoded"
echo "------------------------"
echo "$decoded" > decoded_output.txt

echo
echo "📁 A copy of the decoded message has been saved to: decoded_output.txt"
echo "🔎 Multiple code-like strings may be present."
echo "🧠 Only one of them fits the official CCRI flag format: CCRI-XXX-###"
echo "📋 Manually copy the correct flag into the scoreboard when ready."
echo

read -p "Press ENTER to close this terminal..." close
