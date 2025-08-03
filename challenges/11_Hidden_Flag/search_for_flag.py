#!/usr/bin/env python3
import os
import sys
import json
import re
import time

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "11_HiddenFlag"

# === Validation Mode Detection
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
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    unlock_path = os.path.join(
        project_root,
        "web_version_admin",
        SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON
    )
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

def list_directory(path):
    try:
        return sorted(os.listdir(path))
    except FileNotFoundError:
        return []

def validate_hidden_flag(root_dir, expected_flag):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r") as f:
                    if expected_flag in f.read():
                        print(f"✅ Validation success: found flag {expected_flag} in {file_path}")
                        return True
            except Exception:
                continue
    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.join(script_dir, "junk")
    results_file = os.path.join(script_dir, "results.txt")
    current_dir = root_dir

    if validation_mode:
        expected_flag = load_expected_flag(project_root)
        sys.exit(0 if validate_hidden_flag(root_dir, expected_flag) else 1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🗂️  Interactive Hidden File Explorer")
    print("======================================\n")
    print("📁 Mission Briefing:")
    print("---------------------------")
    print(f"🎯 You’ve gained access to a suspicious folder: {os.path.basename(root_dir)}")
    print("🔍 Somewhere inside is a *hidden file* containing the **real flag**.")
    print("⚠️ Beware: Some files contain fake flags. Only one matches this format: CCRI-AAAA-1111\n")
    print("🛠️ You’ll use simulated Linux commands to explore:")
    print("   - 'ls -a' to list all files (even hidden ones)")
    print("   - 'cat' to view file contents")
    print("   - 'cd' to move between directories\n")
    print("💡 Don’t worry! You don’t have to type commands — just choose from the menu.\n")

    if not os.path.isdir(root_dir):
        print(f"❌ ERROR: Folder '{root_dir}' not found!")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # === Explorer Loop ===
    while True:
        clear_screen()
        print("🗂️  Hidden File Explorer")
        print("--------------------------------------")
        relative_dir = os.path.relpath(current_dir, script_dir)
        print(f"📁 Current directory: {relative_dir}")
        print("\nChoose an action:")
        print("1️⃣  Show all files (ls -a)")
        print("2️⃣  Enter a subdirectory (cd)")
        print("3️⃣  View a file (cat)")
        print("4️⃣  Go up one level (cd ..)")
        print("5️⃣  Exit explorer\n")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            clear_screen()
            print(f"📂 Running: ls -a \"{relative_dir}\"")
            print("--------------------------------------")
            items = list_directory(current_dir)
            print("\n".join(sorted(items)) if items else "⚠️  No files or directories found.")
            print("--------------------------------------")
            pause()

        elif choice == "2":
            subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
            if not subdirs:
                print("\n⚠️  No subdirectories found here.")
                pause()
                continue
            clear_screen()
            print(f"📂 Subdirectories in '{relative_dir}':")
            print("--------------------------------------")
            for idx, subdir in enumerate(sorted(subdirs), 1):
                print(f"{idx:2d}) {subdir}")
            try:
                index = int(input("\nEnter the number of the directory to enter: ").strip())
                if 1 <= index <= len(subdirs):
                    current_dir = os.path.join(current_dir, subdirs[index - 1])
                else:
                    print("❌ Invalid selection.")
                    pause()
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                pause()

        elif choice == "3":
            files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
            if not files:
                print("\n⚠️  No files found here.")
                pause()
                continue
            clear_screen()
            print(f"📄 Files in '{relative_dir}':")
            print("--------------------------------------")
            for idx, file in enumerate(sorted(files), 1):
                print(f"{idx:2d}) {file}")
            try:
                index = int(input("\nEnter the number of the file to view: ").strip())
                if 1 <= index <= len(files):
                    filepath = os.path.join(current_dir, files[index - 1])
                    clear_screen()
                    print(f"📄 Running: cat \"{os.path.relpath(filepath, script_dir)}\"")
                    print("--------------------------------------")
                    try:
                        with open(filepath, "r") as f:
                            content = f.read()
                            print(content)
                    except Exception as e:
                        print(f"❌ Could not read file: {e}")
                    print("--------------------------------------\n")
                    save_choice = input(f"Would you like to save this output to {os.path.basename(results_file)}? (y/n): ").strip().lower()
                    if save_choice == "y":
                        with open(results_file, "a") as rf:
                            rf.write(f"\n----- {os.path.relpath(filepath, script_dir)} -----\n")
                            rf.write(content)
                        print(f"✅ Saved to {os.path.basename(results_file)}")
                    pause()
                else:
                    print("❌ Invalid selection.")
                    pause()
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                pause()

        elif choice == "4":
            if os.path.abspath(current_dir) != os.path.abspath(root_dir):
                current_dir = os.path.dirname(current_dir)
                print(f"⬆️  Moved up to: {os.path.relpath(current_dir, script_dir)}")
                time.sleep(0.5)
            else:
                print("⚠️ Already at the top-level directory.")
                pause()

        elif choice == "5":
            print("👋 Exiting explorer. Good luck finding the *real* flag!")
            break
        else:
            print("❌ Invalid option. Please enter a number from 1 to 5.")
            pause()

if __name__ == "__main__":
    main()
