#!/bin/bash

clear
echo "🕵️‍♂️ Auth Log Investigation"
echo "==========================="
echo
echo "Target file: auth.log"
echo "Tool used: grep"
echo
echo "The goal is to identify a suspicious login record by analyzing fake auth logs."
echo "Some logs contain strange PIDs — one of them hides the real flag."
echo

read -p "Press ENTER to preview a few log entries..."

echo
echo "📄 First 10 lines from auth.log:"
echo "--------------------------------"
head -n 10 auth.log
echo "--------------------------------"
sleep 1

echo
echo "🔍 Scanning for entries with suspicious PID patterns (e.g. contain dashes)..."
grep '\[[A-Z0-9\-]\{8,\}\]' auth.log > flag_candidates.txt

echo "📌 Found $(wc -l < flag_candidates.txt) potential suspicious lines."
echo

read -p "Press ENTER to review suspicious lines..." junk
echo
cat flag_candidates.txt | head -n 5
echo "..."
echo

read -p "🔍 Enter a keyword or pattern to search in the full log (or press ENTER to skip): " pattern
if [[ -n "$pattern" ]]; then
    echo
    echo "🔎 Searching for: $pattern"
    grep "$pattern" auth.log
else
    echo "⏭️  Skipping custom search."
fi

echo
echo "🧠 Remember, only ONE of the 5 flagged entries is a valid CCRI flag!"
echo "Format: CCRI-AAAA-1111"
echo

read -p "Press ENTER to close this terminal..." junk
