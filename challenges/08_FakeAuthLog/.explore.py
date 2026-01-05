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
LOG_FILE = "auth.log"
OUTPUT_FILE = "flag.txt"
# This regex matches the format CCRI-AAAA-1111 or similar decoys
REGEX_PATTERN = r"CCRI-[A-Z0-9]{4}-[A-Z0-9]{4}"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def scan_for_flags(log_file, regex_pattern):
    matches = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                if re.search(regex_pattern, line):
                    matches.append(line.strip())
    except Exception as e:
        print_error(f"Error while scanning {log_file}: {e}")
        sys.exit(1)
    return matches

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    log_path = get_path(LOG_FILE)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.isfile(log_path):
        print_error(f"{LOG_FILE} not found in {script_dir}.")
        sys.exit(1)

    # 2. Mission Briefing
    header("📜 Log Analysis & Filtering")
    
    print(f"📄 Target Log: {Colors.BOLD}{LOG_FILE}{Colors.END}")
    print(f"🔧 Tool: {Colors.BOLD}grep{Colors.END}\n")
    print("🎯 Goal: Filter thousands of lines of noise to find the hidden flag.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Problem:** The log file is too large to read line-by-line.")
    print("   ➤ **The Needle:** We are looking for the agency flag format (`CCRI-...`).")
    print("   ➤ **The Strategy:** Filtering (displaying only lines that match criteria).")
    print("   ➤ **The Tool:** `grep` (Global Regular Expression Print).\n")
    
    require_input("Type 'ready' to begin the investigation: ", "ready")

    # 3. Discovery (ls -lh)
    header("🔍 Phase 1: Reconnaissance")
    print("First, let's see how big this haystack is.\n")
    print(f"   {Colors.GREEN}ls -lh {LOG_FILE}{Colors.END}\n")
    
    # Simulate ls -lh output
    size_mb = os.path.getsize(log_path) / 1024 / 1024
    print(f"-rw-r--r-- 1 root root {size_mb:.1f}M {time.strftime('%b %d %H:%M')} {LOG_FILE}\n")
    print(f"That is a {size_mb:.1f}MB text file. Reading it manually is impossible.\n")
    
    require_input("Type 'head' to preview the first few lines: ", "head")

    # 4. Preview (head)
    print(f"\n📄 First 10 lines of {LOG_FILE}:")
    print("-" * 50)
    try:
        with open(log_path, "r") as f:
            for i, line in enumerate(f):
                if i >= 10: break
                print(f"{Colors.YELLOW}{line.strip()}{Colors.END}")
    except FileNotFoundError:
        print_error("Could not open log file.")
    print("-" * 50 + "\n")
    
    print("It's full of SSH login attempts and noise.\n")
    require_input("Type 'filter' to apply the grep tool: ", "filter")

    # 5. Filtering (grep)
    header("🛠️ Phase 2: Filtering")
    print("We will now apply the filter strategy.\n")
    print("Command to be executed:\n")
    print(f"   {Colors.GREEN}grep \"CCRI\" {LOG_FILE} > {OUTPUT_FILE}{Colors.END}\n")
    
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}grep \"CCRI\"{Colors.END}   → Search for lines containing 'CCRI'")
    print(f"   {Colors.BOLD}{LOG_FILE}{Colors.END}        → The source file")
    print(f"   {Colors.BOLD}> {OUTPUT_FILE}{Colors.END}   → Save matches to a file (instead of screen)\n")
    
    require_input("Type 'run' to execute the filter: ", "run")

    print(f"\n⏳ Scanning {LOG_FILE}...")
    spinner("Filtering noise")

    # Perform the scan
    matches = scan_for_flags(log_path, REGEX_PATTERN)

    if matches:
        # Save results
        with open(output_path, "w") as f_out:
            for line in matches:
                f_out.write(line + "\n")

        print("\n")
        print_success("Match found!")
        print("-" * 50)
        for line in matches:
            print(f"{Colors.BOLD}{line}{Colors.END}")
        print("-" * 50 + "\n")
        
        print(f"📁 Evidence saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
        print(f"{Colors.CYAN}🧠 This confirms the user successfully logged in with the flag.{Colors.END}\n")
    else:
        print_error("No matches found for 'CCRI'.")
        print_info("The hacker might have used a different format, or the log is clean.")

    # 6. Advanced (Bonus Lesson)
    print(f"{Colors.CYAN}💡 Bonus Lesson: Regex{Colors.END}")
    print("   If we didn't know the prefix 'CCRI', we could search for the PATTERN.")
    print("   grep -E \"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\"")
    print("   This is called a Regular Expression (Regex).\n")
    
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()