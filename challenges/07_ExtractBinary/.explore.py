#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
BINARY_FILE = "hidden_flag"
STRINGS_FILE = "extracted_strings.txt"
REGEX_PATTERN = r'CCRI-[A-Z0-9]{4}-\d{4}' # Updated to match standard CCRI flag format precisely

def get_path(filename):
    """Ensure the file is saved next to this script, regardless of where it's run from."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def run_strings(binary_path, output_path):
    try:
        with open(output_path, "w", encoding="utf-8", errors="ignore") as out_f:
            subprocess.run(["strings", binary_path], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print_error("Failed to run 'strings'.")
        sys.exit(1)

def search_for_flags(file_path, regex):
    matches = []
    try:
        with open(file_path, "r", errors="ignore") as f:
            for i, line in enumerate(f):
                # Find all occurrences in the line
                found = re.findall(regex, line)
                for flag in found:
                    matches.append(flag)
    except Exception as e:
        print_error(f"Error during flag search: {e}")
        sys.exit(1)
    return matches

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    binary_path = get_path(BINARY_FILE)
    strings_path = get_path(STRINGS_FILE)

    if not os.path.isfile(binary_path):
        print_error(f"The file '{BINARY_FILE}' was not found.")
        sys.exit(1)

    # 2. Mission Briefing
    header("🧪 Binary Forensics Challenge")
    
    print(f"📦 Target binary: {Colors.BOLD}{BINARY_FILE}{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}strings{Colors.END}\n")
    print("🎯 Goal: Uncover a hidden flag embedded inside this compiled program.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Lock:** The file is a binary executable (not readable text).")
    print("   ➤ **The Strategy:** Static Analysis (reading the raw data bytes).")
    print("   ➤ **The Tool:** The `strings` command pulls readable text out of binary noise.\n")
    
    require_input("Type 'ready' when you're ready to see the command we'll run: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("To extract all readable strings from the binary, we use:\n")
    print(f"   {Colors.GREEN}strings {BINARY_FILE} > {STRINGS_FILE}{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}strings {BINARY_FILE}{Colors.END}   → Scan the binary for printable text")
    print(f"   {Colors.BOLD}> {STRINGS_FILE:<20}{Colors.END}→ Redirect all found strings into a text file")
    print("\nAfter that, we can search inside the text file using tools like 'grep'.\n")
    
    require_input("Type 'run' when you're ready to extract strings from the binary: ", "run")

    print(f"\n🔍 Running: strings \"{BINARY_FILE}\" > \"{STRINGS_FILE}\"")
    spinner("Extracting strings")
    run_strings(binary_path, strings_path)
    time.sleep(0.3)
    print_success(f"All extracted strings saved to: {STRINGS_FILE}\n")

    print(f"📄 Previewing the first 15 lines of extracted text:")
    print("-" * 50)
    try:
        with open(strings_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= 15: break
                print(f"{Colors.YELLOW}{line.strip()}{Colors.END}")
    except FileNotFoundError:
        print_error(f"Could not open {STRINGS_FILE}.")
    print("-" * 50 + "\n")

    # 4. Keyword Search
    require_input("Type 'search' to enter a keyword search mode: ", "search")
    
    print(f"We know the flag starts with '{Colors.BOLD}CCRI{Colors.END}'.")
    keyword = input(f"{Colors.YELLOW}🔍 Enter a keyword to search (or hit ENTER to use 'CCRI'): {Colors.END}").strip()
    
    if not keyword:
        keyword = "CCRI"
    
    print(f"\n🔎 Searching for '{Colors.BOLD}{keyword}{Colors.END}' in {STRINGS_FILE}...\n")
    
    # Show the grep command they are simulating
    print("   Command being used under the hood:")
    print(f"      {Colors.GREEN}grep {keyword} {STRINGS_FILE}{Colors.END}\n")
    time.sleep(0.5)
    
    try:
        # We use subprocess to get the nice colored grep output if available
        subprocess.run(["grep", "--color=always", keyword, strings_path], check=False)
    except FileNotFoundError:
        print_error("grep command not found.")
        
    print("\n")
    print(f"{Colors.CYAN}🧠 Hint: If you see the flag above, copy it!{Colors.END}")
    print(f"   Format: CCRI-AAAA-1111\n")

    # 5. Automated Scan (Backup)
    matches = search_for_flags(strings_path, REGEX_PATTERN)
    if matches:
        print(f"{Colors.GREEN}📌 Automated Scan confirmed {len(matches)} flag(s):{Colors.END}")
        for m in matches:
            print(f"   ➡️ {Colors.BOLD}{m}{Colors.END}")
    
    pause("\nPress ENTER to close this terminal...")

if __name__ == "__main__":
    main()