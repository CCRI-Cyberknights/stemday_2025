#!/usr/bin/env python3
import os
import sys
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def list_directory(path):
    try:
        return sorted(os.listdir(path))
    except FileNotFoundError:
        return []

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.join(script_dir, "junk")
    results_file = os.path.join(script_dir, "results.txt")
    current_dir = root_dir

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
        pause()
        sys.exit(1)

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
        if choice not in {"1", "2", "3", "4", "5"}:
            print("❌ Invalid option. Please enter a number from 1 to 5.")
            pause()
            continue

        if choice == "1":
            clear_screen()
            print(f"📂 Running: ls -a \"{relative_dir}\"")
            print("--------------------------------------")
            items = list_directory(current_dir)
            print("\n".join(items) if items else "⚠️  No files or directories found.")
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
            for idx, subdir in enumerate(subdirs, 1):
                print(f"{idx:2d}) {subdir}")

            index_input = input("\nEnter the number of the directory to enter: ").strip()
            if index_input.isdigit():
                index = int(index_input)
                if 1 <= index <= len(subdirs):
                    current_dir = os.path.join(current_dir, subdirs[index - 1])
                else:
                    print("❌ Invalid selection.")
                    pause()
            else:
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
            for idx, file in enumerate(files, 1):
                print(f"{idx:2d}) {file}")

            index_input = input("\nEnter the number of the file to view: ").strip()
            if index_input.isdigit():
                index = int(index_input)
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
                        content = ""
                    print("--------------------------------------\n")

                    save_choice = input(f"Would you like to save this output to {os.path.basename(results_file)}? (y/n): ").strip().lower()
                    if save_choice == "y":
                        with open(results_file, "a") as rf:
                            rf.write(f"\n----- {os.path.relpath(filepath, script_dir)} -----\n")
                            rf.write(content)
                        print(f"✅ Saved to: {os.path.basename(results_file)}")
                    pause()
                else:
                    print("❌ Invalid selection.")
                    pause()
            else:
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

if __name__ == "__main__":
    main()
