#!/bin/bash
clear
echo "🛰️ Nmap Scan Puzzle"
echo "--------------------------------------"
echo "Several simulated services are running locally (within your CTF app)."
echo
echo "🎯 Your goal: Scan localhost (127.0.0.1) for open ports in the range 8000–8100, and find the REAL flag."
echo
echo "⚠️ Some ports contain random junk responses. Only one flag is correct."

read -p "Press ENTER to begin your scan..."

echo
echo "📡 Running nmap on localhost (127.0.0.1)..."
nmap -p8000-8100 localhost

echo
echo "✅ Scan complete. Now connect to each discovered port using curl or a browser."
echo
echo "Example: curl http://localhost:<port>"
echo
echo "When you’ve found the real flag, return to the CTF portal and submit it."

read -p "Press ENTER when done to continue..."
