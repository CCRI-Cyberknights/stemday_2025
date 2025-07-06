#!/bin/bash

clear

echo "🗂️  Interactive Hidden File Explorer"
echo "--------------------------------------"
echo

echo "Welcome, agent. You have access to a sample file system that contains a suspicious folder named 'junk'."
echo "Somewhere in there is a hidden file containing the real flag."
echo "Others may look like flags, but only one has the correct format: CCRI-AAAA-1111"
echo

echo "You're about to begin a guided search using real commands under the hood."
echo "You won't have to type any Linux commands — just choose from the options."
echo "(We've already enabled visibility of normally hidden files for you.)"
echo

root_dir="junk"
current_dir="$root_dir"

# Ensure root_dir exists
if [[ ! -d "$root_dir" ]]; then
    echo "❌ ERROR: Folder '$root_dir' not found in this directory!"
    read -p "Press ENTER to close this terminal..." junk
    exit 1
fi

while true; do
    clear
    echo "🗂️  Interactive Hidden File Explorer"
    echo "--------------------------------------"
    echo "📁 Current directory: $current_dir"
    echo "Choose an action:"
    echo "1. Show contents of this directory"
    echo "2. Enter a subdirectory"
    echo "3. View a file"
    echo "4. Go up one level"
    echo "5. Exit"
    echo
    read -p "Enter a number (1-5): " choice

    case $choice in
        1)
            echo
            echo "📁 Contents of '$current_dir':"
            echo "--------------------------------------"
            ls -a "$current_dir" | sort
            read -p "Press ENTER to continue." ;;
        2)
            clear
            echo "📂 Subdirectories in '$current_dir':"
            echo "--------------------------------------"
            subdirs=($(find "$current_dir" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort))
            if [ ${#subdirs[@]} -eq 0 ]; then
                echo "(None found)"
                read -p "Press ENTER to continue."
            else
                for i in "${!subdirs[@]}"; do
                    printf "%d) %s\n" "$((i+1))" "${subdirs[$i]}"
                done
                read -p "Enter number of directory to enter: " index
                if [[ "$index" =~ ^[0-9]+$ && $index -ge 1 && $index -le ${#subdirs[@]} ]]; then
                    subdir="${subdirs[$((index-1))]}"
                    current_dir="$current_dir/$subdir"
                else
                    echo "❌ That is not a valid selection."
                    read -p "Press ENTER to continue."
                fi
            fi ;;
        3)
            clear
            echo "📄 Files in '$current_dir':"
            echo "--------------------------------------"
            files=($(find "$current_dir" -mindepth 1 -maxdepth 1 -type f -exec basename {} \; | sort))
            if [ ${#files[@]} -eq 0 ]; then
                echo "(None found)"
                read -p "Press ENTER to continue."
            else
                for i in "${!files[@]}"; do
                    printf "%d) %s\n" "$((i+1))" "${files[$i]}"
                done
                read -p "Enter number of file to view: " index
                if [[ "$index" =~ ^[0-9]+$ && $index -ge 1 && $index -le ${#files[@]} ]]; then
                    file="${files[$((index-1))]}"
                    filepath="$current_dir/$file"
                    clear
                    echo "----- File Contents: $filepath -----"
                    echo
                    cat "$filepath"
                    echo
                    read -p "Would you like to save this output to results.txt? (y/n): " save_choice
                    if [[ "$save_choice" =~ ^[Yy]$ ]]; then
                        echo >> results.txt
                        echo "----- $filepath -----" >> results.txt
                        cat "$filepath" >> results.txt
                        echo "✅ Saved to results.txt"
                    fi
                else
                    echo "❌ That is not a valid selection."
                    read -p "Press ENTER to continue."
                fi
                read -p "Press ENTER to continue."
            fi ;;
        4)
            if [[ "$current_dir" != "$root_dir" ]]; then
                parent_dir="$(dirname "$current_dir")"
                # Prevent moving above root_dir
                if [[ "$parent_dir" == "$root_dir"* ]]; then
                    current_dir="$parent_dir"
                else
                    current_dir="$root_dir"
                fi
            else
                echo "⚠️ You're already at the top level ($root_dir)."
                read -p "Press ENTER to continue."
            fi ;;
        5)
            echo "Exiting. Good luck finding the real flag!"
            break ;;
        *)
            echo "❌ Invalid option. Please enter a number from 1 to 5."
            read -p "Press ENTER to continue." ;;
    esac
done

# Clean exit for web hub
exec $SHELL
