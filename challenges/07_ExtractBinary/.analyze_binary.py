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
REGEX_PATTERN = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

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
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print_error(f"Error during flag search: {e}")
        sys.exit(1)
    return matches

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    binary_path = get_path(BINARY_FILE)
    strings_path = get_path(STRINGS_FILE)

    # 2. Mission Briefing
    header("🧪 Binary Forensics Challenge")
    
    print(f"📦 Target binary: {Colors.BOLD}{BINARY_FILE}{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}strings{Colors.END}\n")
    print("🎯 Goal: Uncover a hidden flag embedded inside this compiled program.\n")
    print(f"{Colors.CYAN}💡 Why 'strings'?{Colors.END}")
    print("   ➤ Compiled programs contain a mix of binary data and human-readable text.")
    print("   ➤ The 'strings' tool scans the file and pulls out the readable text segments.")
    print("   ➤ This is a common first step in binary forensics and malware analysis.\n")
    
    require_input("Type 'ready' when you're ready to see the command we'll run: ", "ready")

    if not os.path.isfile(binary_path):
        print_error(f"The file '{BINARY_FILE}' was not found.")
        sys.exit(1)

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
    
    print("You might start by searching for words related to the story, like 'CCRI' or 'Cryptkeepers'.")
    keyword = input(f"{Colors.YELLOW}🔍 Enter a keyword to search (or hit ENTER to skip): {Colors.END}").strip().lower()
    
    if keyword:
        print(f"\n🔎 Searching for '{Colors.BOLD}{keyword}{Colors.END}' in {STRINGS_FILE}...\n")
        print("   Command being used under the hood:")
        print(f"      {Colors.GREEN}grep -i {keyword} {STRINGS_FILE}{Colors.END}\n")
        time.sleep(0.5)
        try:
            subprocess.run(["grep", "-i", "--color=always", keyword, strings_path], check=False)
        except FileNotFoundError:
            print_error("grep command not found.")
    else:
        print_info("Skipping keyword search.\n")

    # 5. Flag Scan
    require_input("Type 'scan' to scan for potential flags: ", "scan")
    
    print("🔎 Scanning for flag-like patterns (format: XXXX-YYYY-ZZZZ)...")
    time.sleep(0.5)
    matches = search_for_flags(strings_path, REGEX_PATTERN)

    if matches:
        print(f"\n{Colors.GREEN}📌 Found {len(matches)} possible flag(s):{Colors.END}")
        for m in matches:
            print(f"   ➡️ {Colors.BOLD}{m}{Colors.END}")
    else:
        print(f"\n{Colors.RED}⚠️ No obvious flags found. Try scanning manually in {STRINGS_FILE}.{Colors.END}")

    print("\n✅ Done! You can inspect extracted_strings.txt further or try other tools like 'hexdump' for deeper analysis.")
    print(f"{Colors.CYAN}🧠 Remember: Only one string matches the official flag format: CCRI-AAAA-1111{Colors.END}\n")
    
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()