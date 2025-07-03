#!/bin/bash
clear

echo "🌐 Subdomain Sweep"
echo "---------------------------------"
echo "You've discovered five subdomains."
echo "Each one hosts a web page that *might* contain a hidden flag."
echo
echo "💡 Hint: The real flag starts with CCRI-."
echo

domains=(alpha.liber8.local beta.liber8.local gamma.liber8.local delta.liber8.local omega.liber8.local)

while true; do
    echo "Available subdomains:"
    for i in "${!domains[@]}"; do
        echo "$((i+1)). ${domains[$i]}"
    done
    echo "6. Exit"
    echo

    read -p "Select a subdomain to open in browser (1-6): " choice

    if [[ "$choice" -ge 1 && "$choice" -le 5 ]]; then
        file="${domains[$((choice-1))]}.html"
        echo
        echo "🌐 Opening http://${domains[$((choice-1))]} in your browser..."
        xdg-open "$file" >/dev/null 2>&1 &
        echo "👀 Explore the page carefully. The flag may be hidden!"
    elif [[ "$choice" -eq 6 ]]; then
        echo "👋 Exiting. Good luck finding the real flag!"
        break
    else
        echo "❌ Invalid choice. Please select 1-6."
    fi
done
