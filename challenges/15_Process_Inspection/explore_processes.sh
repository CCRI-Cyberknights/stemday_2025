#!/bin/bash

# Auto-relaunch in a bigger terminal window
if [[ -z "$BIGGER_TERMINAL" ]]; then
    export BIGGER_TERMINAL=1
    echo "🔄 Launching in a larger terminal window for better visibility..."
    sleep 1

    if command -v xfce4-terminal >/dev/null 2>&1; then
        xfce4-terminal --geometry=120x40 -e "bash -c 'exec \"$0\"'"
        exit
    elif command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal --geometry=120x40 -- bash -c "exec \"$0\""
        exit
    elif command -v konsole >/dev/null 2>&1; then
        konsole --geometry 120x40 -e "bash -c 'exec \"$0\"'"
        exit
    else
        echo "⚠️ Could not detect a graphical terminal. Continuing in current terminal."
    fi
fi

# Main script starts here
clear
echo "🖥️ Process Inspection"
echo "================================="
echo
echo "You've obtained a snapshot of running processes (ps_dump.txt)."
echo
echo "🎯 Your goal: Find the rogue process hiding a flag in a --flag= argument!"
echo
echo "💡 Tip: The real flag starts with CCRI-AAAA-1111."
echo "   You'll inspect processes one by one to uncover hidden details."
echo
read -p "Press ENTER to start exploring..." junk
clear

# Check for ps_dump.txt
if [[ ! -f ps_dump.txt ]]; then
    echo "❌ ERROR: ps_dump.txt not found in this folder!"
    read -p "Press ENTER to exit..." junk
    exit 1
fi

# Build unique process list
mapfile -t processes < <(awk 'NR>1 && $11 ~ /^\// {print $11}' ps_dump.txt | sort | uniq)

while true; do
    echo "================================="
    echo "📂 Process List (from ps_dump.txt):"
    for i in "${!processes[@]}"; do
        echo "$((i+1)). ${processes[$i]}"
    done
    echo "$(( ${#processes[@]} + 1 )). Exit"
    echo
    read -p "Select a process to inspect (1-${#processes[@]}): " choice

    if [[ "$choice" -ge 1 && "$choice" -le "${#processes[@]}" ]]; then
        proc_name="${processes[$((choice-1))]}"
        echo
        echo "🔍 Inspecting process: $proc_name"
        echo "   → Command: grep \"$proc_name\" ps_dump.txt | sed 's/--/\n    --/g'"
        echo "================================="
        sleep 0.5

        # Display details with flags indented
        grep "$proc_name" ps_dump.txt | sed 's/--/\n    --/g'
        echo "================================="

        while true; do
            echo "Options:"
            echo "1. Return to process list"
            echo "2. Save this output to a file (process_output.txt)"
            echo
            read -p "Choose an option (1-2): " save_choice

            if [[ "$save_choice" == "1" ]]; then
                clear
                break
            elif [[ "$save_choice" == "2" ]]; then
                echo "💾 Saving output to process_output.txt..."
                grep "$proc_name" ps_dump.txt | sed 's/--/\n    --/g' > process_output.txt
                echo "✅ Saved successfully."
                read -p "Press ENTER to continue." junk
                clear
                break
            else
                echo "❌ Invalid choice. Please select 1 or 2."
            fi
        done

    elif [[ "$choice" -eq "$(( ${#processes[@]} + 1 ))" ]]; then
        echo
        echo "👋 Exiting. Good luck identifying the rogue process!"
        break
    else
        echo "❌ Invalid choice. Please select a valid process."
        read -p "Press ENTER to continue." junk
        clear
    fi
done

# Clean exit
exit 0
