#!/bin/bash

clear
echo "🧪 Binary Forensics Challenge"
echo "============================="
echo
echo "Target binary: hidden_flag"
echo "Tool used: strings"
echo
echo "The goal is to uncover a hidden flag from inside a compiled program."
echo "We'll preview some of the binary contents and extract possible flag candidates."
echo
read -p "Press ENTER to begin extracting strings from the binary..." junk

# Check for target binary
if [[ ! -f hidden_flag ]]; then
    echo "❌ ERROR: The file 'hidden_flag' was not found in this folder."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

OUTFILE="extracted_strings.txt"
strings hidden_flag > "$OUTFILE"
echo -e "\n📄 Running 'strings' on: hidden_flag"
echo "✅ All strings saved to: $OUTFILE"

# Show preview
PREVIEW_LINES=15
echo -e "\n🔍 Previewing the first $PREVIEW_LINES lines:"
echo "--------------------------------------------------"
head -n "$PREVIEW_LINES" "$OUTFILE"
echo "--------------------------------------------------"

# Animation/break
sleep 0.5
echo -n "\nAnalyzing patterns"
for i in {1..3}; do
    sleep 0.5
    echo -n "."
done
echo -e "\n"
sleep 0.3

# Grep flag-like patterns
MATCH_PATTERN='\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'
echo "🔎 Scanning for flag-like patterns (e.g. AAAA-BBBB-1234)..."
grep -E "$MATCH_PATTERN" "$OUTFILE" | tee temp_matches.txt

COUNT=$(wc -l < temp_matches.txt)
echo -e "\n📌 Found $COUNT possible flag(s) matching that format."

read -p $'\n🔍 Enter a keyword to search in the full dump (or hit ENTER to skip): ' keyword
if [[ -n "$keyword" ]]; then
    echo -e "\n🔎 Searching for '$keyword' in $OUTFILE..."
    grep -i --color=always "$keyword" "$OUTFILE"
else
    echo "⏭️  Skipping keyword search."
fi

echo -e "\n✅ Done. You may now inspect $OUTFILE or try other tools!"
read -p "Press ENTER to close this terminal..."
exec $SHELL
