#!/bin/bash

# Auto-relaunch in a bigger terminal window
if [[ -z "$BIGGER_TERMINAL" ]]; then
    # Mark that we're already in the bigger terminal if we relaunch
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
echo "---------------------------------"
echo "You've obtained a snapshot of running processes."
echo "Choose a process to view its details."
echo
echo "💡 Hint: The real flag starts with CCRI- and is in a --flag= argument."
echo

# Verify ps_dump.txt exists
if [[ ! -f ps_dump.txt ]]; then
    echo "❌ ERROR: ps_dump.txt not found in this folder!"
    read -p "Press ENTER to exit..." junk
    exit 1
fi

# Build dynamic list of unique COMMAND entries from ps_dump.txt
mapfile -t processes < <(
    awk 'NR>1 && $11 ~ /^\// {print $11}' ps_dump.txt | sort | uniq
)

while true; do
    echo "Processes:"
    for i in "${!processes[@]}"; do
        echo "$((i+1)). ${processes[$i]}"
    done
    echo "$(( ${#processes[@]} + 1 )). Exit"
    echo

    read -p "Select a process to inspect (1-${#processes[@]}): " choice

    if [[ "$choice" -ge 1 && "$choice" -le "${#processes[@]}" ]]; then
        echo
        echo "🔍 Inspecting ${processes[$((choice-1))]} ..."
        echo "---------------------------------"
        echo "USER       PID %CPU %MEM   VSZ    RSS  TTY  STAT  START   TIME  COMMAND"
        echo "-----      --- ---- ----   ----   ---- ---  ----  -----   ----  -------"
        process_output=$(grep "${processes[$((choice-1))]}" ps_dump.txt | sed 's/--/\n    --/g')
        echo "$process_output"
        echo "---------------------------------"

        while true; do
            echo "Options:"
            echo "1. Return to process list"
            echo "2. Save this output to a file"
            echo
            read -p "Choose an option (1-2): " save_choice

            if [[ "$save_choice" == "1" ]]; then
                break
            elif [[ "$save_choice" == "2" ]]; then
                out_file="process_output.txt"
                echo "$process_output" > "$out_file"
                echo "✅ Process details saved to $out_file"
                break
            else
                echo "❌ Invalid choice. Please select 1 or 2."
            fi
        done

        clear
    elif [[ "$choice" -eq "$(( ${#processes[@]} + 1 ))" ]]; then
        echo "👋 Exiting. Good luck identifying the rogue process!"
        break
    else
        echo "❌ Invalid choice. Please select a valid process."
    fi
done

# Clean exit for web hub
exit 0
