#!/bin/bash

# === Binary Forensics Challenge ===

# === Locate Project Root ===
find_project_root() {
    DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    while [ "$DIR" != "/" ]; do
        if [ -f "$DIR/.ccri_ctf_root" ]; then
            echo "$DIR"
            return 0
        fi
        DIR="$(dirname "$DIR")"
    done
    echo "❌ ERROR: Could not find project root marker (.ccri_ctf_root)." >&2
    exit 1
}

PROJECT_ROOT="$(find_project_root)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET_BINARY="$SCRIPT_DIR/hidden_flag"
OUTFILE="$SCRIPT_DIR/extracted_strings.txt"
TEMP_MATCHES="$SCRIPT_DIR/temp_matches.txt"

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
if [[ ! -f "$TARGET_BINARY" ]]; then
    echo
    echo "❌ ERROR: The file 'hidden_flag' was not found in $SCRIPT_DIR."
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Run strings and save results
echo
echo "🔍 Running: strings \"$TARGET_BINARY\" > \"$OUTFILE\""
strings "$TARGET_BINARY" > "$OUTFILE"
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
grep -E "$MATCH_PATTERN" "$OUTFILE" | tee "$TEMP_MATCHES"

COUNT=$(wc -l < "$TEMP_MATCHES")
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
