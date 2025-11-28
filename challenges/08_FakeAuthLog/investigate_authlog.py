#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

regex_pattern = r"\b[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\b"

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    This keeps students from just mashing ENTER through explanations.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def spinner(message="Working", duration=1.8, interval=0.12):
    """
    Simple text spinner to give the feeling of work being done.
    """
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{message}... {frame}")
        sys.stdout.flush()
        time.sleep(interval)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

# === Core Logic ===
def scan_for_flags(log_file, regex_pattern):
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

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    log_file = os.path.join(script_dir, "auth.log")
    candidates_file = os.path.join(script_dir, "flag_candidates.txt")

    flatten_authlog_dir(script_dir)

    clear_screen()
    print("🕵️‍♂️ Auth Log Investigation")
    print("==============================\n")
    print("📄 Target file: auth.log")
    print("🔧 Tools in use: grep, regex\n")
    print("🎯 Goal: Identify a suspicious login record by analyzing fake auth logs.")
    print("   ➡️ One of these records contains a **PID** that hides the real flag!\n")
    print("💡 What are we doing here?")
    print("   ➤ Real systems keep authentication history in files like /var/log/auth.log.")
    print("   ➤ Analysts review these logs to spot brute-force attempts, odd PIDs, or weird usernames.")
    print("   ➤ We'll use pattern matching to hunt for values that look like flags.\n")
    pause_nonempty("Type 'ready' when you're ready to review the log and search strategy: ")

    if not os.path.isfile(log_file):
        print(f"\n❌ ERROR: auth.log not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("Step 1: Take a quick look at the top of the log.\n")
    print("   In a real terminal, you might use:")
    print("      head auth.log")
    print("      less auth.log\n")
    print("Step 2: Use a regular expression (regex) to find values that *look* like flags.\n")
    print("   Our pattern here is:")
    print("      [A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}")
    print("   ➤ 4 characters, dash, 4 characters, dash, 4 characters (letters or digits)")
    print("   ➤ This catches ANYID-1234-ABCD-style strings, including fake flags.\n")
    print("Step 3: Narrow things down by also searching with grep for usernames/IPs.\n")
    pause_nonempty("Type 'view' when you're ready to preview the log: ")

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
    pause_nonempty("Type anything, then press ENTER to scan for suspicious entries...")

    print("🔎 Scanning for flag-like patterns (format similar to CCRI-AAAA-1111)...")
    spinner("Analyzing log")

    matches = scan_for_flags(log_file, regex_pattern)

    if matches:
        with open(candidates_file, "w") as f_out:
            for line in matches:
                f_out.write(line + "\n")

        print(f"\n📌 Found {len(matches)} potential flag-like strings.")
        print(f"💾 Saved to: {candidates_file}\n")

        pause_nonempty("Type anything, then press ENTER to preview flagged lines...")
        print("🧾 Sample of suspicious entries:")
        print("-------------------------------------------")
        for i, line in enumerate(matches):
            print(f"   ➡️ {line}")
            if i >= 4 and len(matches) > 5:
                print("   ... (more found)")
                break
        print("-------------------------------------------\n")
    else:
        print("⚠️ No suspicious entries found in auth.log.")
        pause("Press ENTER to close this terminal...")
        sys.exit(0)

    print("🧰 Next step: Targeted search with grep.")
    print("   Example commands you might run on a real system:")
    print("      grep 'Failed password' auth.log")
    print("      grep 'Accepted password' auth.log")
    print("      grep '192.168.' auth.log\n")

    pattern = input("🔎 Enter a username, IP, or keyword to search the full log (or press ENTER to skip): ").strip()
    if pattern:
        print(f"\n🔎 Searching for '{pattern}' in auth.log...\n")
        print("   Command being used under the hood:")
        print(f"      grep --color=always {pattern} auth.log\n")
        try:
            subprocess.run(["grep", "--color=always", pattern, log_file], check=False)
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping keyword search.")

    print("\n🧠 Hint: Only one of the PID entries hides the **real** CCRI flag.")
    print("   🔍 Compare the suspicious entries, watch for out-of-place PIDs, usernames, or IPs.")
    print("   🪪 Final flag format to watch for: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
