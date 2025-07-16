#!/bin/bash

# === HTTP Headers Mystery ===

# Locate Project Root
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

clear

echo "📡 HTTP Headers Mystery"
echo "================================="
echo
echo "🎯 Mission Briefing:"
echo "---------------------------------"
echo "You've intercepted **five HTTP responses** during a network investigation."
echo "The real flag is hidden in one of their HTTP headers."
echo
echo "🧠 Flag format: CCRI-AAAA-1111"
echo "💡 Tip: HTTP headers are key-value pairs sent by a server along with its response."
echo "        We can view and search for hidden data inside them."
echo

responses=("$SCRIPT_DIR/response_1.txt" "$SCRIPT_DIR/response_2.txt" "$SCRIPT_DIR/response_3.txt" "$SCRIPT_DIR/response_4.txt" "$SCRIPT_DIR/response_5.txt")

# --- Pre-flight check ---
missing=0
for f in "${responses[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "❌ ERROR: '$(basename "$f")' not found!"
        missing=1
    fi
done
if [[ "$missing" -eq 1 ]]; then
    echo
    read -p "⚠️ Missing one or more response files. Press ENTER to exit." junk
    exit 1
fi

while true; do
    echo
    echo "📂 Available HTTP responses:"
    for i in "${!responses[@]}"; do
        echo "$((i+1)). $(basename "${responses[$i]}")"
    done
    echo "6. Bulk scan all files for flag-like patterns"
    echo "7. Exit"
    echo

    read -p "Select an option (1-7): " choice

    if [[ "$choice" -ge 1 && "$choice" -le 5 ]]; then
        file="${responses[$((choice-1))]}"
        echo
        echo "🔍 Opening $(basename "$file") (press 'q' to quit)..."
        echo "---------------------------------"
        echo "💻 Tip: Press '/' to search within the file for 'CCRI-'"
        echo
        less "$file"
        echo "---------------------------------"

    elif [[ "$choice" -eq 6 ]]; then
        echo
        echo "🔎 Bulk scanning all HTTP headers for flag patterns..."
        echo "💻 Running: grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' response_*.txt"
        echo
        grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' "$SCRIPT_DIR"/response_*.txt --color=always || echo "⚠️ No flags found in bulk scan."
        echo
        read -p "Press ENTER to return to the menu." junk

    elif [[ "$choice" -eq 7 ]]; then
        echo "👋 Exiting HTTP Headers Mystery. Stay sharp, agent!"
        break

    else
        echo "❌ Invalid option. Please select a number from 1 to 7."
        read -p "Press ENTER to continue." junk
    fi
done

# Clean exit for web hub
exec $SHELL
