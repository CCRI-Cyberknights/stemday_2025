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
  python3 python3-pip python3-venv \
  python3-markdown python3-flask python3-scapy \
  exiftool zbar-tools steghide hashcat unzip nmap tshark qrencode \
  xdg-utils vim-common util-linux

echo
echo "✅ All required tools have been installed."
echo

echo "🎉 Setup complete!"
echo "➡️ You’re ready to start using the CCRI STEM Day CTF."
echo
echo "💡 If you downloaded the CTF manually, make sure to:"
echo "   - Move the folder to your Desktop (if not already there)."
echo "   - Place the **'Launch CCRI CTF Hub.desktop'** shortcut on your Desktop."
echo "   - Right-click the shortcut → Properties → Permissions → ✅ Allow execution."
echo
