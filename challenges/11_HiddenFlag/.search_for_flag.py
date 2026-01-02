#!/usr/bin/env python3
import os
import sys
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
ROOT_FOLDER = "junk"
RESULTS_FILE = "results.txt"

def list_directory(path):
    try:
        return sorted(os.listdir(path))
    except FileNotFoundError:
        return []

def main():
    # 1. Setup
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.join(script_dir, ROOT_FOLDER)
    results_path = os.path.join(script_dir, RESULTS_FILE)
    current_dir = root_dir

    # 2. Mission Briefing
    header("🗂️  Interactive Hidden File Explorer")
    
    print("📁 Mission Briefing:")
    print("-" * 30)
    print(f"🎯 You’ve gained access to a suspicious folder: {Colors.BOLD}{ROOT_FOLDER}{Colors.END}")
    print(f"🔍 Somewhere inside is a *hidden file* containing the {Colors.BOLD}real flag{Colors.END}.")
    print(f"{Colors.RED}⚠️ Beware: Some files contain fake flags. Only one matches this format: CCRI-AAAA-1111{Colors.END}\n")
    
    print(f"{Colors.CYAN}🛠️ You’ll use common Linux-style actions to explore:{Colors.END}")
    print(f"   - {Colors.GREEN}'ls -a'{Colors.END} to list all files (even hidden ones)")
    print(f"   - {Colors.GREEN}'cat'{Colors.END} to view file contents")
    print(f"   - {Colors.GREEN}'cd'{Colors.END} to move between directories\n")
    print("💡 Instead of typing commands, you’ll pick actions from a menu —")
    print("   but watch the prompts: they show you what the real commands look like.\n")

    if not os.path.isdir(root_dir):
        print_error(f"Folder '{ROOT_FOLDER}' not found!")
        sys.exit(1)

    require_input("Type 'start' when you're ready to begin exploring the directory tree: ", "start")

    # 3. Explorer Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}🗂️  Hidden File Explorer{Colors.END}")
        print("-" * 40)
        
        relative_dir = os.path.relpath(current_dir, script_dir)
        print(f"📁 Current directory: {Colors.YELLOW}{relative_dir}{Colors.END}")
        
        print("\nChoose an action:")
        print(f"1️⃣  Show all files ({Colors.BOLD}ls -a{Colors.END})")
        print(f"2️⃣  Enter a subdirectory ({Colors.BOLD}cd{Colors.END})")
        print(f"3️⃣  View a file ({Colors.BOLD}cat{Colors.END})")
        print(f"4️⃣  Go up one level ({Colors.BOLD}cd ..{Colors.END})")
        print(f"5️⃣  Exit explorer\n")

        choice = input(f"{Colors.YELLOW}Enter your choice (1-5): {Colors.END}").strip()
        
        if choice not in {"1", "2", "3", "4", "5"}:
            print_error("Invalid option. Please enter a number from 1 to 5.")
            pause()
            continue

        # === Action: List Files ===
        if choice == "1":
            clear_screen()
            print(f"📂 Running: {Colors.GREEN}ls -a \"{relative_dir}\"{Colors.END}")
            print("-" * 40)
            items = list_directory(current_dir)
            if items:
                for item in items:
                    if item.startswith("."):
                        print(f"{Colors.CYAN}{item} (hidden){Colors.END}")
                    else:
                        print(item)
            else:
                print_info("No files or directories found.")
            print("-" * 40)
            pause()

        # === Action: Change Directory (Down) ===
        elif choice == "2":
            subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
            if not subdirs:
                print_info("No subdirectories found here.")
                pause()
                continue

            clear_screen()
            print(f"📂 Subdirectories in '{relative_dir}':")
            print("-" * 40)
            for idx, subdir in enumerate(subdirs, 1):
                print(f"{Colors.BOLD}{idx:2d}) {subdir}{Colors.END}")

            try:
                index = int(input(f"\n{Colors.YELLOW}Enter number to enter: {Colors.END}").strip())
                if 1 <= index <= len(subdirs):
                    current_dir = os.path.join(current_dir, subdirs[index - 1])
                else:
                    print_error("Invalid selection.")
                    pause()
            except ValueError:
                print_error("Invalid input.")
                pause()

        # === Action: View File (cat) ===
        elif choice == "3":
            files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
            if not files:
                print_info("No files found here.")
                pause()
                continue

            clear_screen()
            print(f"📄 Files in '{relative_dir}':")
            print("-" * 40)
            for idx, file in enumerate(files, 1):
                # Highlight hidden files
                if file.startswith("."):
                    print(f"{Colors.BOLD}{idx:2d}) {Colors.CYAN}{file}{Colors.END}")
                else:
                    print(f"{Colors.BOLD}{idx:2d}) {file}{Colors.END}")

            try:
                index_input = input(f"\n{Colors.YELLOW}Enter number to view: {Colors.END}").strip()
                if not index_input.isdigit():
                    print_error("Invalid input. Please enter a number.")
                    pause()
                    continue

                index = int(index_input)
                if 1 <= index <= len(files):
                    filename = files[index - 1]
                    filepath = os.path.join(current_dir, filename)
                    
                    clear_screen()
                    print(f"📄 Running: {Colors.GREEN}cat \"{filename}\"{Colors.END}")
                    print("-" * 40)
                    content = ""
                    try:
                        with open(filepath, "r", errors="replace") as f:
                            content = f.read()
                            print(f"{Colors.YELLOW}{content}{Colors.END}")
                    except Exception as e:
                        print_error(f"Could not read file: {e}")
                    print("-" * 40 + "\n")

                    # === STRICT YES/NO LOOP ===
                    while True:
                        save_choice = input(f"Save output to {RESULTS_FILE}? (yes/no): ").strip().lower()
                        if save_choice == "yes":
                            with open(results_path, "a") as rf:
                                rf.write(f"\n----- {os.path.relpath(filepath, script_dir)} -----\n")
                                rf.write(content)
                            print_success(f"Saved to: {RESULTS_FILE}")
                            pause()
                            break
                        elif save_choice == "no":
                            pause()
                            break
                        else:
                            print_error("Please type 'yes' or 'no'.")
                else:
                    print_error("Invalid selection.")
                    pause()
            except ValueError:
                print_error("Invalid input.")
                pause()

        # === Action: Change Directory (Up) ===
        elif choice == "4":
            if os.path.abspath(current_dir) != os.path.abspath(root_dir):
                current_dir = os.path.dirname(current_dir)
                print(f"⬆️  Moved up to: {os.path.relpath(current_dir, script_dir)}")
                time.sleep(0.3)
            else:
                print_error("Already at the top-level directory.")
                pause()

        # === Action: Exit ===
        elif choice == "5":
            print(f"\n{Colors.CYAN}👋 Exiting explorer. Good luck finding the *real* flag!{Colors.END}")
            break

if __name__ == "__main__":
    main()