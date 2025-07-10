#!/bin/bash

clear
echo "🧪 Binary Forensics Challenge"
echo "============================="
echo
echo "📦 Target binary: hidden_flag"
echo "🔧 Tool in use: strings"
echo
echo "🎯 Goal: Uncover a hidden flag embedded inside this compiled program."
echo
echo "💡 Why use 'strings'?"
echo "   ➡️ 'strings' scans binary files and extracts any readable text sequences."
echo "   ➡️ Often used to find debugging info, secret keys, or flags left behind."
echo
read -p "Press ENTER to scan the binary for readable content..." junk

# --- Pre-flight check ---
if [[ ! -f hidden_flag ]]; then
    echo
    echo "❌ ERROR: The file 'hidden_flag' was not found in this folder."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Run strings and save results
OUTFILE="extracted_strings.txt"
echo
echo "🔍 Running: strings hidden_flag > $OUTFILE"
strings hidden_flag > "$OUTFILE"
sleep 0.5
echo "✅ All extracted strings saved to: $OUTFILE"
echo

# Preview some output
PREVIEW_LINES=15
echo "📄 Previewing the first $PREVIEW_LINES lines of extracted text:"
echo "--------------------------------------------------"
head -n "$PREVIEW_LINES" "$OUTFILE"
echo "--------------------------------------------------"
echo
read -p "Press ENTER to scan for flag patterns..." junk

# Search for flag patterns
echo "🔎 Scanning for flag-like patterns (format: XXXX-YYYY-ZZZZ)..."
sleep 0.5
MATCH_PATTERN='\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'
grep -E "$MATCH_PATTERN" "$OUTFILE" | tee temp_matches.txt

COUNT=$(wc -l < temp_matches.txt)
if [[ "$COUNT" -gt 0 ]]; then
    echo -e "\n📌 Found $COUNT possible flag(s) matching that format!"
else
    echo -e "\n⚠️ No obvious flags found. Try scanning manually in $OUTFILE."
fi

# Optional keyword search
echo
read -p "🔍 Enter a keyword to search in the full dump (or hit ENTER to skip): " keyword
if [[ -n "$keyword" ]]; then
    echo
    echo "🔎 Searching for '$keyword' in $OUTFILE..."
    grep -i --color=always "$keyword" "$OUTFILE" || echo "❌ No matches for '$keyword'."
else
    echo "⏭️  Skipping keyword search."
fi

# Wrap-up
echo
echo "✅ Done! You can inspect $OUTFILE further or try other tools like 'hexdump' for deeper analysis."
echo "🧠 Remember: Only one string matches the official flag format: CCRI-AAAA-1111"
echo
read -p "Press ENTER to close this terminal..." junk
exec $SHELL
