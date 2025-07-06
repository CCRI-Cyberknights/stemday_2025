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

# Check that HTML files exist
missing=0
for domain in "${domains[@]}"; do
    html_file="${domain}.html"
    if [[ ! -f "$html_file" ]]; then
        echo "⚠️ WARNING: Missing file '$html_file'"
        missing=1
    fi
done
if [[ "$missing" -eq 1 ]]; then
    echo
    read -p "⚠️ One or more HTML files are missing. Press ENTER to exit." junk
    exit 1
fi

while true; do
    echo
    echo "Available subdomains:"
    for i in "${!domains[@]}"; do
        echo "$((i+1)). ${domains[$i]}"
    done
    echo "6. Exit"
    echo

    read -p "Select a subdomain to open in browser (1-6): " choice

    if [[ "$choice" -ge 1 && "$choice" -le 5 ]]; then
        file="${domains[$((choice-1))]}.html"
        if [[ ! -f "$file" ]]; then
            echo "❌ ERROR: File '$file' not found!"
            read -p "Press ENTER to continue." junk
            clear
            continue
        fi
        echo
        echo "🌐 Opening http://${domains[$((choice-1))]} in your browser..."
        xdg-open "$file" >/dev/null 2>&1 &
        echo "👀 Explore the page carefully. The flag may be hidden!"
        read -p "Press ENTER to return to the menu." junk
        clear
    elif [[ "$choice" -eq 6 ]]; then
        echo "👋 Exiting. Good luck finding the real flag!"
        break
    else
        echo "❌ Invalid choice. Please select 1-6."
        read -p "Press ENTER to continue." junk
        clear
    fi
done

# Clean exit for web hub
exec $SHELL
