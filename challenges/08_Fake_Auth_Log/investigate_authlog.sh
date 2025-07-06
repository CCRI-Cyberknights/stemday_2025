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

read -p "Press ENTER to preview a few log entries..." junk

# Check for auth.log first
if [[ ! -f auth.log ]]; then
    echo "❌ ERROR: auth.log not found in this folder."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

echo
echo "📄 First 10 lines from auth.log:"
echo "--------------------------------"
head -n 10 auth.log
echo "--------------------------------"
sleep 1

echo
echo "🔍 Scanning for entries with suspicious PID patterns (e.g. contain dashes)..."
grep '\[[A-Z0-9\-]\{8,\}\]' auth.log > flag_candidates.txt

CAND_COUNT=$(wc -l < flag_candidates.txt)
echo "📌 Found $CAND_COUNT potential suspicious line(s)."
echo

if [[ "$CAND_COUNT" -eq 0 ]]; then
    echo "⚠️ No suspicious entries found."
    read -p "Press ENTER to close this terminal..." junk
    exit 0
fi

read -p "Press ENTER to review suspicious lines..." junk
echo
head -n 5 flag_candidates.txt
echo "..."
echo

read -p "🔍 Enter a keyword or pattern to search in the full log (or press ENTER to skip): " pattern
if [[ -n "$pattern" ]]; then
    echo
    echo "🔎 Searching for: $pattern"
    grep --color=always "$pattern" auth.log || echo "⚠️ No matches found."
else
    echo "⏭️  Skipping custom search."
fi

echo
echo "🧠 Remember, only ONE of the flagged entries is a valid CCRI flag!"
echo "Format: CCRI-AAAA-1111"
echo

read -p "Press ENTER to close this terminal..." junk
exec $SHELL
