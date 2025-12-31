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
CANDIDATES_FILE = "flag_candidates.txt"
REGEX_PATTERN = r"\b[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\b"

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
        print_error(f"Error while scanning auth.log: {e}")
        sys.exit(1)
    return matches

def flatten_authlog_dir(script_dir):
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f == "auth.log" and root != script_dir:
                src = os.path.join(root, f)
                dst = os.path.join(script_dir, f)
                if not os.path.exists(dst):
                    os.rename(src, dst)
        for d in dirs:
            try:
                os.rmdir(os.path.join(root, d))
            except OSError:
                pass

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    log_path = get_path(LOG_FILE)
    candidates_path = get_path(CANDIDATES_FILE)

    flatten_authlog_dir(script_dir)

    # 2. Mission Briefing
    header("🕵️‍♂️ Auth Log Investigation")
    
    print(f"📄 Target file: {Colors.BOLD}{LOG_FILE}{Colors.END}")
    print(f"🔧 Tools in use: {Colors.BOLD}grep, regex{Colors.END}\n")
    print("🎯 Goal: Identify a suspicious login record by analyzing fake auth logs.")
    print("   ➡️ One of these records contains a **PID** that hides the real flag!\n")
    print(f"{Colors.CYAN}💡 What are we doing here?{Colors.END}")
    print(f"   ➤ Real systems keep authentication history in files like {Colors.BOLD}/var/log/auth.log{Colors.END}.")
    print("   ➤ Analysts review these logs to spot brute-force attempts, odd PIDs, or weird usernames.")
    print("   ➤ We'll use pattern matching to hunt for values that look like flags.\n")
    
    require_input("Type 'ready' when you're ready to review the log and search strategy: ", "ready")

    if not os.path.isfile(log_path):
        print_error(f"{LOG_FILE} not found in {script_dir}.")
        sys.exit(1)

    # 3. Strategy Explanation
    header("🛠️ Behind the Scenes")
    print("Step 1: Take a quick look at the top of the log.\n")
    print("   In a real terminal, you might use:")
    print(f"      {Colors.GREEN}head auth.log{Colors.END}")
    print(f"      {Colors.GREEN}less auth.log{Colors.END}\n")
    
    print("Step 2: Use a regular expression (regex) to find values that *look* like flags.\n")
    print("   Our pattern here is:")
    print(f"      {Colors.BOLD}[A-Z0-9]{{4}}-[A-Z0-9]{{4}}-[A-Z0-9]{{4}}{Colors.END}")
    print("   ➤ 4 characters, dash, 4 characters, dash, 4 characters (letters or digits)")
    print("   ➤ This catches ANYID-1234-ABCD-style strings, including fake flags.\n")
    print("Step 3: Narrow things down by also searching with grep for usernames/IPs.\n")
    
    require_input("Type 'view' when you're ready to preview the log: ", "view")

    # 4. Log Preview
    print(f"\n📄 Preview: First 10 lines from {LOG_FILE}")
    print("-" * 50)
    try:
        with open(log_path, "r") as f:
            for i, line in enumerate(f):
                if i >= 10: break
                print(f"{Colors.YELLOW}{line.strip()}{Colors.END}")
    except FileNotFoundError:
        print_error("Could not open auth.log.")
        sys.exit(1)
    print("-" * 50 + "\n")
    
    require_input("Type 'scan' to scan for suspicious entries: ", "scan")

    # 5. Regex Scanning
    print("🔎 Scanning for flag-like patterns (format similar to CCRI-AAAA-1111)...")
    spinner("Analyzing log")

    matches = scan_for_flags(log_path, REGEX_PATTERN)

    if matches:
        with open(candidates_path, "w") as f_out:
            for line in matches:
                f_out.write(line + "\n")

        print(f"\n{Colors.GREEN}📌 Found {len(matches)} potential flag-like strings.{Colors.END}")
        print(f"💾 Saved to: {Colors.BOLD}{CANDIDATES_FILE}{Colors.END}\n")

        require_input("Type 'next' to preview flagged lines: ", "next")
        
        print("🧾 Sample of suspicious entries:")
        print("-" * 50)
        for i, line in enumerate(matches):
            print(f"   ➡️ {Colors.BOLD}{line}{Colors.END}")
            if i >= 4 and len(matches) > 5:
                print("   ... (more found)")
                break
        print("-" * 50 + "\n")
    else:
        print_info("No suspicious entries found in auth.log.")
        pause("Press ENTER to close this terminal...")
        sys.exit(0)

    # 6. Interactive Grep
    print("🧰 Next step: Targeted search with grep.")
    print("   Example commands you might run on a real system:")
    print(f"      {Colors.GREEN}grep 'Failed password' auth.log{Colors.END}")
    print(f"      {Colors.GREEN}grep 'Accepted password' auth.log{Colors.END}")
    print(f"      {Colors.GREEN}grep '192.168.' auth.log{Colors.END}\n")

    pattern = input(f"{Colors.YELLOW}🔎 Enter a username, IP, or keyword to search the full log (or press ENTER to skip): {Colors.END}").strip().lower()
    
    if pattern:
        print(f"\n🔎 Searching for '{Colors.BOLD}{pattern}{Colors.END}' in {LOG_FILE}...\n")
        print("   Command being used under the hood:")
        print(f"      {Colors.GREEN}grep --color=always {pattern} {LOG_FILE}{Colors.END}\n")
        try:
            subprocess.run(["grep", "--color=always", pattern, log_path], check=False)
        except FileNotFoundError:
            print_error("grep command not found.")
    else:
        print_info("Skipping keyword search.")

    # 7. Conclusion
    print(f"\n{Colors.CYAN}🧠 Hint: Only one of the PID entries hides the **real** CCRI flag.{Colors.END}")
    print("   🔍 Compare the suspicious entries, watch for out-of-place PIDs, usernames, or IPs.")
    print(f"   🪪 Final flag format to watch for: {Colors.GREEN}CCRI-AAAA-1111{Colors.END}\n")
    
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()