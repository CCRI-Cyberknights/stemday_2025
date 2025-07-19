#!/bin/bash
# 🌟 CCRI CyberKnights Student Setup Script
set -e

echo
echo "🚀 Setting up your CCRI STEM Day CTF environment..."
echo "====================================================="
echo

# --- Update package list and install dependencies ---
echo "📦 Installing system dependencies..."
sudo apt update

sudo apt install -y \
  git \
  python3 python3-pip python3-venv \
  python3-markdown python3-flask python3-scapy \
  exiftool zbar-tools steghide hashcat unzip nmap tshark qrencode \
  xdg-utils vim-common util-linux

echo
echo "✅ All required tools have been installed."
echo

# --- Ask if they want to download the CTF repo automatically ---
read -rp "📥 Do you want me to download the CTF folder and set up the Desktop shortcut for you? (y/n): " download_choice

if [[ "$download_choice" =~ ^[Yy]$ ]]; then
    DESKTOP_DIR="$HOME/Desktop"
    CTF_FOLDER="$DESKTOP_DIR/stemday2025_takehome"
    SHORTCUT_FILE="Launch CCRI CTF Hub.desktop"

    echo
    echo "📥 Downloading the CTF bundle to your Desktop..."
    rm -rf "$CTF_FOLDER"  # Remove any previous version to avoid conflicts
    git clone https://github.com/CCRI-Cyberknights/stemday2025_takehome.git "$CTF_FOLDER"

    echo
    echo "📌 Placing Desktop shortcut..."
    cp "$CTF_FOLDER/$SHORTCUT_FILE" "$DESKTOP_DIR/"
    chmod +x "$DESKTOP_DIR/$SHORTCUT_FILE"

    echo
    echo "✅ CTF folder and shortcut are set up on your Desktop."
else
    echo
    echo "💡 Since you chose not to download the CTF automatically, make sure you:"
    echo "   - Move the CTF folder to your Desktop (if not already there)."
    echo "   - Place the **'Launch CCRI CTF Hub.desktop'** file on your Desktop."
    echo "   - Right-click the shortcut → Properties → Permissions → ✅ Allow execution."
    echo
fi

echo "🎉 Setup complete! You’re ready to start exploring the STEM Day CTF."
echo "➡️ To get started, double-click **“Launch CCRI CTF Hub”** on your Desktop."
echo
