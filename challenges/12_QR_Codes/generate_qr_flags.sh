#!/bin/bash

# Make sure qrencode is installed
if ! command -v qrencode &>/dev/null; then
  echo "❌ qrencode is not installed. Please run: sudo apt install qrencode"
  exit 1
fi

# Output folder (current directory)
echo "Generating QR codes in current directory..."

# Real flag
qrencode -o qr_03.png "CCRI-QRCX-4821"
echo "✅ qr_03.png (REAL flag)"

# Decoys
qrencode -o qr_01.png "SCAN-1234-TRAP"
echo "➖ qr_01.png (decoy)"

qrencode -o qr_02.png "DATA-FAKE-2290"
echo "➖ qr_02.png (decoy)"

qrencode -o qr_04.png "FLAG-9999-VOID"
echo "➖ qr_04.png (decoy)"

qrencode -o qr_05.png "CODE-HINT-7777"
echo "➖ qr_05.png (decoy)"

echo "All QR codes generated. You can edit the text in this script to change them later."
