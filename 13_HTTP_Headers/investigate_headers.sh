#!/bin/bash
clear

echo "📡 HTTP Headers Mystery"
echo "---------------------------------"
echo "You've intercepted five HTTP responses."
echo "Each one might contain a secret flag hidden in the headers."
echo
echo "💡 Hint: The real flag starts with CCRI-."
echo "👩‍💻 Tip: When viewing a file, press 'q' to quit and return to this menu."
echo

responses=(response_1.txt response_2.txt response_3.txt response_4.txt response_5.txt)

while true; do
    echo "Available HTTP responses:"
    for i in "${!responses[@]}"; do
        echo "$((i+1)). ${responses[$i]}"
    done
    echo "6. Exit"
    echo

    read -p "Select a response file to explore (1-6): " choice

    if [[ "$choice" -ge 1 && "$choice" -le 5 ]]; then
        file="${responses[$((choice-1))]}"
        echo
        echo "🔍 Opening $file (press 'q' to quit)..."
        echo "---------------------------------"
        less "$file"
        echo "---------------------------------"
    elif [[ "$choice" -eq 6 ]]; then
        echo "👋 Exiting. Happy hunting!"
        break
    else
        echo "❌ Invalid choice. Please select 1-6."
    fi
done
