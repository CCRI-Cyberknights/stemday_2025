#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import glob

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
    Prevents students from just mashing ENTER through the briefing.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

# === File / Scan Helpers ===
def check_response_files(files):
    missing = []
    for f in files:
        if not os.path.isfile(f):
            print(f"❌ ERROR: '{os.path.basename(f)}' not found!")
            missing.append(f)
    return missing

def view_file_with_less(file_path):
    try:
        subprocess.run(["less", file_path])
    except FileNotFoundError:
        print("❌ ERROR: 'less' command not found.")
        sys.exit(1)

def bulk_scan(script_dir):
    try:
        pattern = os.path.join(script_dir, "response_*.txt")
        matching_files = glob.glob(pattern)

        if not matching_files:
            print("⚠️ No response_*.txt files found.")
            return

        result = subprocess.run(
            ["grep", "-E", r"CCRI-[A-Z]{4}-[0-9]{4}"] + matching_files,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )

        if result.stdout.strip():
            print(result.stdout)
        else:
            print("⚠️ No flag-like patterns found.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    responses = [os.path.join(script_dir, f"response_{i}.txt") for i in range(1, 6)]

    clear_screen()
    print("📡 HTTP Headers Mystery")
    print("=================================\n")
    print("🎯 Mission Briefing:")
    print("---------------------------------")
    print("You've intercepted **five HTTP responses** during a network investigation.")
    print("The real flag is hidden in one of their HTTP headers.\n")
    print("🧠 Flag format: CCRI-AAAA-1111\n")
    print("💡 Quick HTTP refresher:")
    print("   ➤ When you visit a website, the server responds with an HTTP status line,")
    print("      followed by a series of headers like `Server:`, `Content-Type:`, etc.")
    print("   ➤ CTF challenges sometimes hide data inside unusual or custom headers.")
    print("   ➤ Here, one header contains the real CCRI flag; others may be decoys.\n")
    pause_nonempty("Type 'ready' when you're ready to see how we'll inspect these responses: ")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("----------------------------")
    print("In a normal Linux terminal, you might inspect HTTP responses by running:\n")
    print("   less response_1.txt")
    print("   less response_2.txt")
    print("   ...\n")
    print("   ➤ `less` lets you scroll through the file (press 'q' to quit).\n")
    print("To search for flag-like patterns across all responses, you might run:\n")
    print("   grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' response_*.txt\n")
    print("🔍 Command breakdown:")
    print("   grep          → Search for lines matching a pattern")
    print("   -E            → Use extended regular expressions")
    print("   'CCRI-[A-Z]{4}-[0-9]{4}' → Our flag format pattern")
    print("   response_*.txt→ Search across all response files at once\n")
    pause_nonempty("Type 'start' when you're ready to analyze the HTTP responses: ")

    if check_response_files(responses):
        pause("\n⚠️ Missing files. Press ENTER to exit.")
        sys.exit(1)

    while True:
        print("\n📂 Available HTTP responses:")
        for i, r in enumerate(responses, 1):
            print(f"{i}. {os.path.basename(r)}")
        print("6. Bulk scan all files for flag patterns")
        print("7. Exit\n")

        choice = input("Select an option (1–7): ").strip()

        if choice in {"1", "2", "3", "4", "5"}:
            file = responses[int(choice) - 1]
            print(f"\n🔍 Viewing {os.path.basename(file)} (press 'q' to quit)...\n")
            view_file_with_less(file)

        elif choice == "6":
            print("\n🔎 Bulk scanning for flags...")
            print("💻 Running: grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' response_*.txt\n")
            bulk_scan(script_dir)
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print("\n👋 Exiting HTTP Headers Mystery. Stay sharp, agent!")
            break

        else:
            print("\n❌ Invalid option.")
            pause()

if __name__ == "__main__":
    main()
