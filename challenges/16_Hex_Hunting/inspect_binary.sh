#!/bin/bash
clear
echo "🔍 Hex Flag Hunter"
echo "============================"
echo
echo "🎯 Target binary: hex_flag.bin"
echo
echo "💡 Goal: Locate the real flag (format: CCRI-AAAA-1111)."
echo "    ⚠️ 5 candidate flags are embedded, but only ONE is correct!"
echo

read -p "Press ENTER to begin scanning hex_flag.bin..."

# Add some scanning animation
echo -ne "\n🔎 Scanning binary for flag-like patterns"
for i in {1..5}; do
    sleep 0.3
    echo -n "."
done
echo

# Search for flag-like strings
flags=($(grep -aboE '([A-Z]{4}-[A-Z]{4}-[0-9]{4}|[A-Z]{4}-[0-9]{4}-[A-Z]{4})' hex_flag.bin | awk -F: '{print $2}'))

if [[ ${#flags[@]} -eq 0 ]]; then
    echo "❌ No flag-like patterns found. Exiting..."
    exit 1
fi

# Interactive loop over each candidate
echo
echo "✅ Found ${#flags[@]} candidate flag(s)."
echo
for i in "${!flags[@]}"; do
    flag="${flags[$i]}"
    echo "--------------------------------------------"
    echo "[$((i+1))/${#flags[@]}] Candidate Flag: $flag"
    echo "--------------------------------------------"

    # Show hex context around this flag
    offset=$(grep -abo "$flag" hex_flag.bin | head -n1 | cut -d: -f1)
    start=$((offset - 16))
    [ $start -lt 0 ] && start=0
    echo "📖 Hex context (around offset $offset):"
    dd if=hex_flag.bin bs=1 skip=$start count=64 2>/dev/null | xxd

    echo
    echo "Options:"
    echo "1) Mark this flag as POSSIBLE and save to notes.txt"
    echo "2) Skip to next flag"
    echo "3) Quit investigation"
    read -p "Choose an option (1-3): " choice

    case "$choice" in
        1)
            echo "$flag" >> notes.txt
            echo "✅ Saved '$flag' to notes.txt"
            ;;
        2)
            echo "➡️ Skipping to next candidate..."
            ;;
        3)
            echo "👋 Exiting investigation early."
            exit 0
            ;;
        *)
            echo "⚠️ Invalid choice. Skipping to next..."
            ;;
    esac
    echo
done

echo "🎉 Investigation complete!"
echo "📁 All saved candidate flags are in notes.txt"
echo "📝 Review and submit the correct flag to the scoreboard!"
read -p "Press ENTER to close..."
