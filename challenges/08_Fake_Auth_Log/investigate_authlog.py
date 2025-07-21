#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import json
import re

# === Auth Log Investigation Helper ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def scan_for_flags(log_file, regex_pattern):
    """Scan the full log file for flag-like patterns."""
    matches = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                if re.search(regex_pattern, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR while scanning auth.log: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

def flatten_authlog_dir(script_dir):
    """
    Move auth.log to script_dir if it’s inside a nested directory
    and remove empty folders.
    """
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f == "auth.log" and root != script_dir:
                src = os.path.join(root, f)
                dst = os.path.join(script_dir, f)
                if not os.path.exists(dst):
                    os.rename(src, dst)
        # Remove empty dirs
        for d in dirs:
            dir_to_remove = os.path.join(root, d)
            try:
                os.rmdir(dir_to_remove)
            except OSError:
                pass  # Ignore if not empty

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    log_file = os.path.join(script_dir, "auth.log")
    candidates_file = os.path.join(script_dir, "flag_candidates.txt")
    regex_pattern = r"\bCCRI-[A-Z0-9]{4}-\d{4}\b"

    # Flatten directory in case of nested auth.log
    flatten_authlog_dir(script_dir)

    # === Validation Mode: Silent flag check ===
    if validation_mode:
        unlock_file = os.path.join(project_root, "web_version_admin", "validation_unlocks.json")
        try:
            with open(unlock_file, "r", encoding="utf-8") as f:
                unlocks = json.load(f)
            expected_flag = unlocks["08_FakeAuthLog"]["real_flag"]
        except Exception as e:
            print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
            sys.exit(1)

        if not os.path.isfile(log_file):
            print(f"❌ ERROR: auth.log not found in {script_dir}.", file=sys.stderr)
            sys.exit(1)

        matches = scan_for_flags(log_file, regex_pattern)

        # Check if the expected flag is present anywhere in the log
        found_flag = any(expected_flag in line for line in matches)
        if found_flag:
            print(f"✅ Validation success: found flag {expected_flag}")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found in auth.log.", file=sys.stderr)
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🕵️‍♂️ Auth Log Investigation")
    print("==============================\n")
    print("📄 Target file: auth.log")
    print("🔧 Tool in use: grep\n")
    print("🎯 Goal: Identify a suspicious login record by analyzing fake auth logs.")
    print("   ➡️ One of these records contains a **PID** that hides the real flag!\n")
    pause()

    if not os.path.isfile(log_file):
        print(f"\n❌ ERROR: auth.log not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # Preview auth.log
    print("\n📄 Preview: First 10 lines from auth.log")
    print("-------------------------------------------")
    try:
        with open(log_file, "r") as f:
            for i, line in enumerate(f):
                if i >= 10:
                    break
                print(line.strip())
    except FileNotFoundError:
        print("❌ ERROR: Could not open auth.log.")
        sys.exit(1)
    print("-------------------------------------------\n")
    pause("Press ENTER to scan for suspicious entries...")

    # Scan for CCRI-style flags
    print("\n🔍 Scanning for entries with flag-like patterns (format: CCRI-XXXX-1234)...")
    time.sleep(0.5)
    matches = scan_for_flags(log_file, regex_pattern)

    if matches:
        with open(candidates_file, "w") as f_out:
            for line in matches:
                f_out.write(line + "\n")

        print(f"\n📌 Found {len(matches)} potential flag(s).")
        print(f"💾 Saved to: {candidates_file}\n")
        pause("Press ENTER to preview suspicious entries...")
        print("\n-------------------------------------------")
        for i, line in enumerate(matches):
            if i >= 5:
                print("... (only first 5 shown)")
                break
            print(line)
        print("-------------------------------------------\n")
    else:
        print("⚠️ No suspicious entries found in auth.log.")
        pause("Press ENTER to close this terminal...")
        sys.exit(0)

    # Optional search
    pattern = input("🔎 Enter a username, IP, or keyword to search in the full log (or press ENTER to skip): ").strip()
    if pattern:
        print(f"\n🔎 Searching for '{pattern}' in auth.log...")
        try:
            subprocess.run(
                ["grep", "--color=always", pattern, log_file],
                check=False
            )
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping custom search.")

    print("\n🧠 Hint: One of the flagged PIDs hides the official flag!")
    print("   Format: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    validation_mode = os.getenv("CCRI_VALIDATE") == "1"
    main()
