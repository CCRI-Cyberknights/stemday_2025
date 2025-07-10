#!/bin/bash

clear
echo "🕵️‍♂️ Auth Log Investigation"
echo "=============================="
echo
echo "📄 Target file: auth.log"
echo "🔧 Tool in use: grep"
echo
echo "🎯 Goal: Identify a suspicious login record by analyzing fake auth logs."
echo "   ➡️ One of these records contains a **PID** that hides the real flag!"
echo
echo "💡 Why grep?"
echo "   ➡️ 'grep' helps us search for patterns in large text files."
echo "   ➡️ We'll look for strange PIDs (e.g., ones containing dashes or letters)."
echo
read -p "Press ENTER to preview a few log entries..." junk

# --- Check for auth.log first ---
if [[ ! -f auth.log ]]; then
    echo
    echo "❌ ERROR: auth.log not found in this folder."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Show preview
echo
echo "📄 Preview: First 10 lines from auth.log"
echo "-------------------------------------------"
head -n 10 auth.log
echo "-------------------------------------------"
echo
read -p "Press ENTER to scan for suspicious entries..." junk

# Grep suspicious PID patterns
echo
echo "🔍 Scanning for entries with unusual PID patterns (e.g., [CCRI-XXXX-1234] or containing dashes)..."
sleep 0.5
grep '\[[A-Z0-9\-]\{8,\}\]' auth.log > flag_candidates.txt

CAND_COUNT=$(wc -l < flag_candidates.txt)
if [[ "$CAND_COUNT" -eq 0 ]]; then
    echo "⚠️ No suspicious entries found in auth.log."
    read -p "Press ENTER to close this terminal..." junk
    exit 0
fi

echo
echo "📌 Found $CAND_COUNT potential suspicious line(s)."
echo "💾 Saved to: flag_candidates.txt"
echo

# Preview suspicious lines
read -p "Press ENTER to preview suspicious entries..." junk
echo
echo "-------------------------------------------"
head -n 5 flag_candidates.txt
[[ "$CAND_COUNT" -gt 5 ]] && echo "... (only first 5 shown)"
echo "-------------------------------------------"
echo

# Optional search
read -p "🔎 Enter a username, IP, or keyword to search in the full log (or press ENTER to skip): " pattern
if [[ -n "$pattern" ]]; then
    echo
    echo "🔎 Searching for '$pattern' in auth.log..."
    grep --color=always "$pattern" auth.log || echo "⚠️ No matches found for '$pattern'."
else
    echo "⏭️  Skipping custom search."
fi

# Wrap-up
echo
echo "🧠 Hint: One of the flagged PIDs hides the official flag!"
echo "   Format: CCRI-AAAA-1111"
echo
read -p "Press ENTER to close this terminal..." junk
exec $SHELL
