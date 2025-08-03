#!/usr/bin/env python3
import os
import sys
import subprocess
import json

# === Challenge ID and Constants ===
CHALLENGE_ID = "13_HTTPHeaders"
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    mode = get_ctf_mode()
    unlock_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
        sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

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
        print("❌ ERROR: 'less' command not found on this system.")
        sys.exit(1)

def bulk_scan_for_flags(script_dir):
    try:
        result = subprocess.run(
            ["grep", "-E", "CCRI-[A-Z]{4}-[0-9]{4}", os.path.join(script_dir, "response_*.txt")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("⚠️ No flags found in bulk scan.")
    except Exception as e:
        print(f"❌ ERROR during bulk scan: {e}")

def validate_responses(responses, expected_flag):
    print("🔍 Validation: scanning all HTTP responses for the expected flag...")
    for response in responses:
        try:
            with open(response, "r", encoding="utf-8") as f:
                content = f.read()
                if expected_flag in content:
                    print(f"✅ Validation success: found flag {expected_flag} in {os.path.basename(response)}")
                    return True
        except Exception as e:
            print(f"❌ ERROR reading {response}: {e}")
    print(f"❌ Validation failed: flag {expected_flag} not found in any HTTP response.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    responses = [os.path.join(script_dir, f"response_{i}.txt") for i in range(1, 6)]

    if validation_mode:
        expected_flag = load_expected_flag(project_root)
        sys.exit(0 if validate_responses(responses, expected_flag) else 1)

    # === Student Interactive Mode ===
    clear_screen()
    print("📡 HTTP Headers Mystery")
    print("=================================\n")
    print("🎯 Mission Briefing:")
    print("---------------------------------")
    print("You've intercepted **five HTTP responses** during a network investigation.")
    print("The real flag is hidden in one of their HTTP headers.\n")
    print("🧠 Flag format: CCRI-AAAA-1111")
    print("💡 Tip: HTTP headers are key-value pairs sent by a server along with its response.\n")

    # Pre-flight check
    missing_files = check_response_files(responses)
    if missing_files:
        pause("\n⚠️ Missing one or more response files. Press ENTER to exit.")
        sys.exit(1)

    while True:
        print("\n📂 Available HTTP responses:")
        for i, response in enumerate(responses, 1):
            print(f"{i}. {os.path.basename(response)}")
        print("6. Bulk scan all files for flag-like patterns")
        print("7. Exit\n")

        choice = input("Select an option (1-7): ").strip()

        if choice in {"1", "2", "3", "4", "5"}:
            idx = int(choice) - 1
            file = responses[idx]
            print(f"\n🔍 Opening {os.path.basename(file)} (press 'q' to quit)...")
            print("---------------------------------")
            print("💻 Tip: Press '/' to search within the file for 'CCRI-'\n")
            view_file_with_less(file)
            print("---------------------------------")

        elif choice == "6":
            print("\n🔎 Bulk scanning all HTTP headers for flag patterns...")
            print("💻 Running: grep -E 'CCRI-[A-Z]{{4}}-[0-9]{{4}}' response_*.txt\n")
            bulk_scan_for_flags(script_dir)
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print("\n👋 Exiting HTTP Headers Mystery. Stay sharp, agent!")
            break

        else:
            print("\n❌ Invalid option. Please select a number from 1 to 7.")
            pause()

if __name__ == "__main__":
    main()
