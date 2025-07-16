#!/bin/bash

clear

echo "🗂️  Interactive Hidden File Explorer"
echo "======================================"
echo
echo "📁 Mission Briefing:"
echo "---------------------------"
echo "🎯 You’ve gained access to a suspicious folder named 'junk'."
echo "🔍 Somewhere inside is a *hidden file* containing the **real flag**."
echo "⚠️ Beware: Some files contain fake flags. Only one matches this format: CCRI-AAAA-1111"
echo
echo "🛠️ You’ll use simulated Linux commands to explore:"
echo "   - 'ls -a' to list all files (even hidden ones)"
echo "   - 'cat' to view file contents"
echo "   - 'cd' to move between directories"
echo
echo "💡 Don’t worry! You don’t have to type commands — just choose from the menu."
echo

root_dir="junk"
current_dir="$root_dir"

# Ensure root_dir exists
if [[ ! -d "$root_dir" ]]; then
    echo "❌ ERROR: Folder '$root_dir' not found in this directory!"
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

# Start exploring
while true; do
    clear
    echo "🗂️  Hidden File Explorer"
    echo "--------------------------------------"
    echo "📁 Current directory: $current_dir"
    echo
    echo "Choose an action:"
    echo "1️⃣  Show all files (ls -a)"
    echo "2️⃣  Enter a subdirectory (cd)"
    echo "3️⃣  View a file (cat)"
    echo "4️⃣  Go up one level (cd ..)"
    echo "5️⃣  Exit explorer"
    echo
    read -p "Enter your choice (1-5): " choice

    case $choice in
        1)
            echo
            echo "📂 Running: ls -a \"$current_dir\""
            echo "--------------------------------------"
            ls -a "$current_dir" | sort
            echo "--------------------------------------"
            read -p "Press ENTER to continue..." ;;
        2)
            clear
            echo "📂 Subdirectories in '$current_dir':"
            echo "--------------------------------------"
            subdirs=($(find "$current_dir" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort))
            if [ ${#subdirs[@]} -eq 0 ]; then
                echo "⚠️  No subdirectories found here."
                read -p "Press ENTER to continue..."
            else
                for i in "${!subdirs[@]}"; do
                    printf "%2d) %s\n" "$((i+1))" "${subdirs[$i]}"
                done
                read -p "Enter the number of the directory to enter: " index
                if [[ "$index" =~ ^[0-9]+$ && $index -ge 1 && $index -le ${#subdirs[@]} ]]; then
                    subdir="${subdirs[$((index-1))]}"
                    current_dir="$current_dir/$subdir"
                    echo "📂 Changed directory to: $current_dir"
                    sleep 0.5
                else
                    echo "❌ Invalid selection."
                    read -p "Press ENTER to continue..."
                fi
            fi ;;
        3)
            clear
            echo "📄 Files in '$current_dir':"
            echo "--------------------------------------"
            files=($(find "$current_dir" -mindepth 1 -maxdepth 1 -type f -exec basename {} \; | sort))
            if [ ${#files[@]} -eq 0 ]; then
                echo "⚠️  No files found here."
                read -p "Press ENTER to continue..."
            else
                for i in "${!files[@]}"; do
                    printf "%2d) %s\n" "$((i+1))" "${files[$i]}"
                done
                read -p "Enter the number of the file to view: " index
                if [[ "$index" =~ ^[0-9]+$ && $index -ge 1 && $index -le ${#files[@]} ]]; then
                    file="${files[$((index-1))]}"
                    filepath="$current_dir/$file"
                    clear
                    echo "📄 Running: cat \"$filepath\""
                    echo "--------------------------------------"
                    cat "$filepath"
                    echo "--------------------------------------"
                    echo
                    read -p "Would you like to save this output to results.txt? (y/n): " save_choice
                    if [[ "$save_choice" =~ ^[Yy]$ ]]; then
                        echo -e "\n----- $filepath -----" >> results.txt
                        cat "$filepath" >> results.txt
                        echo "✅ Saved to results.txt"
                    fi
                else
                    echo "❌ Invalid selection."
                    read -p "Press ENTER to continue..."
                fi
            fi ;;
        4)
            if [[ "$current_dir" != "$root_dir" ]]; then
                parent_dir="$(dirname "$current_dir")"
                current_dir="$parent_dir"
                echo "⬆️  Moved up to: $current_dir"
                sleep 0.5
            else
                echo "⚠️ Already at the top-level directory ($root_dir)."
                read -p "Press ENTER to continue..."
            fi ;;
        5)
            echo "👋 Exiting explorer. Good luck finding the *real* flag!"
            break ;;
        *)
            echo "❌ Invalid option. Please enter a number from 1 to 5."
            read -p "Press ENTER to continue..." ;;
    esac
done

# Clean exit for web hub
exec $SHELL
