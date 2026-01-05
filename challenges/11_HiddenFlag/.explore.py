#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
SEARCH_DIR = "junk"
OUTPUT_FILE = "flag.txt"
KEYWORD = "CCRI"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def main():
    # 1. Setup
    resize_terminal(35, 90)
    search_path = get_path(SEARCH_DIR)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.isdir(search_path):
        print_error(f"Directory '{SEARCH_DIR}' not found.")
        sys.exit(1)

    # 2. Mission Briefing
    header("🕵️ Recursive Search Tool")
    
    print(f"📂 Target Directory: {Colors.BOLD}{SEARCH_DIR}/{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}grep -r{Colors.END}\n")
    print("🎯 Goal: Locate the hidden flag inside a maze of subdirectories.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Environment:** A complex folder structure with many decoys.")
    print("   ➤ **The Camouflage:** The flag might be in a 'hidden' file (starts with `.`).")
    print("   ➤ **The Strategy:** Recursive Search (digging through the whole tree).")
    print("   ➤ **The Tool:** `grep -r` searches text inside every file automatically.\n")
    
    require_input("Type 'ready' to initialize the search tool: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("Searching manually with `cd` and `ls` would take forever.")
    print("Instead, we use `grep` with the `-r` (recursive) flag.\n")
    
    print("Command to be executed:\n")
    print(f"   {Colors.GREEN}grep -r \"{KEYWORD}\" {SEARCH_DIR}/{Colors.END}\n")
    
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}grep{Colors.END}         → The search tool")
    print(f"   {Colors.BOLD}-r{Colors.END}           → Recursive (look inside every folder and sub-folder)")
    print(f"   {Colors.BOLD}\"{KEYWORD}\"{Colors.END}     → The text pattern we are looking for")
    print(f"   {Colors.BOLD}{SEARCH_DIR}/{Colors.END}       → Where to start looking\n")
    
    require_input("Type 'run' to execute the recursive search: ", "run")

    # 4. Execution
    print(f"\n⏳ Searching `{SEARCH_DIR}/` for '{KEYWORD}'...")
    spinner("Scanning directories")

    try:
        # Run grep -r
        result = subprocess.run(
            ["grep", "-r", KEYWORD, search_path],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        print_error("grep command not found.")
        sys.exit(1)

    # 5. Analysis
    if result.returncode == 0 and result.stdout:
        print_success("Match found!")
        print("-" * 50)
        
        # Clean up output for display (relative paths)
        lines = result.stdout.strip().splitlines()
        found_file = None
        
        for line in lines:
            # grep output format is usually "filename:match_text"
            if ":" in line:
                file_part, text_part = line.split(":", 1)
                rel_path = os.path.relpath(file_part, os.path.dirname(search_path))
                
                # Highlight the file path and the match
                print(f"📄 File: {Colors.BOLD}{rel_path}{Colors.END}")
                print(f"📝 Content: {Colors.YELLOW}{text_part.strip()}{Colors.END}")
                found_file = file_part # Save absolute path for extraction
        
        print("-" * 50 + "\n")
        
        # 6. Extraction
        if found_file:
            print(f"{Colors.CYAN}🧠 We found the location! Now let's capture it.{Colors.END}")
            require_input(f"Type 'cat' to read and save the file: ", "cat")
            
            with open(found_file, "r") as f:
                content = f.read()
            
            with open(output_path, "w") as f_out:
                f_out.write(content)
                
            print(f"\n✅ Content saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
            print(f"   Flag Format: CCRI-AAAA-1111\n")

    else:
        print_error(f"No matches found for '{KEYWORD}'.")
        print_info("The directory might be empty, or the flag format is different.")

    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()