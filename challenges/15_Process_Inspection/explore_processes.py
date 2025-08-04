#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def relaunch_in_bigger_terminal(script_path):
    if os.environ.get("BIGGER_TERMINAL") == "1":
        return
    os.environ["BIGGER_TERMINAL"] = "1"
    print("🔄 Launching in a larger terminal window for better visibility...")
    time.sleep(1)

    terminal_cmds = [
        ["xfce4-terminal", "--geometry=120x40", "-e", f"bash -c 'exec \"{script_path}\"'"],
        ["gnome-terminal", "--geometry=120x40", "--", "bash", "-c", f"exec \"{script_path}\"'"],
        ["konsole", "--geometry", "120x40", "-e", f"bash -c 'exec \"{script_path}\"'"],
    ]

    for cmd in terminal_cmds:
        try:
            subprocess.Popen(cmd)
            sys.exit(0)
        except FileNotFoundError:
            continue

    print("⚠️ Could not detect a graphical terminal. Continuing in current terminal.")

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    ps_dump = os.path.join(script_dir, "ps_dump.txt")

    relaunch_in_bigger_terminal(__file__)
    clear_screen()

    print("🖥️ Process Inspection")
    print("=================================\n")
    print("You've obtained a snapshot of running processes (ps_dump.txt).\n")
    print("🎯 Your goal: Find the rogue process hiding a flag in a --flag= argument!\n")
    print("💡 Tip: The real flag starts with CCRI-AAAA-1111.")
    print("   You'll inspect processes one by one to uncover hidden details.\n")
    pause()

    if not os.path.isfile(ps_dump):
        print(f"❌ ERROR: {os.path.basename(ps_dump)} not found in this folder!")
        pause("Press ENTER to exit...")
        sys.exit(1)

    # Build unique process list
    processes = []
    with open(ps_dump, "r") as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split()
            if len(parts) > 11 and parts[11].startswith("/"):
                proc_name = parts[11]
                if proc_name not in processes:
                    processes.append(proc_name)

    while True:
        print("=================================")
        print("📂 Process List (from ps_dump.txt):")
        for idx, proc in enumerate(processes, 1):
            print(f"{idx}. {proc}")
        print(f"{len(processes)+1}. Exit\n")

        try:
            choice = int(input(f"Select a process to inspect (1-{len(processes)+1}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            pause()
            clear_screen()
            continue

        if 1 <= choice <= len(processes):
            proc_name = processes[choice - 1]
            print(f"\n🔍 Inspecting process: {proc_name}")
            print("   → Command: grep \"{proc_name}\" ps_dump.txt | sed 's/--/\\n    --/g'")
            print("=================================\n")
            time.sleep(0.5)

            try:
                result = subprocess.run(
                    ["grep", proc_name, ps_dump],
                    stdout=subprocess.PIPE,
                    text=True
                )
                formatted = result.stdout.replace("--", "\n    --")
                print(formatted)
                print("=================================")
            except Exception as e:
                print(f"❌ Error while inspecting process: {e}")

            while True:
                print("\nOptions:")
                print("1. Return to process list")
                print("2. Save this output to a file (process_output.txt)\n")
                save_choice = input("Choose an option (1-2): ").strip()
                if save_choice == "1":
                    clear_screen()
                    break
                elif save_choice == "2":
                    output_file = os.path.join(script_dir, "process_output.txt")
                    with open(output_file, "w") as f:
                        f.write(formatted)
                    print(f"✅ Saved output to {os.path.basename(output_file)}")
                    pause()
                    clear_screen()
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")

        elif choice == len(processes)+1:
            print("\n👋 Exiting. Good luck identifying the rogue process!")
            break
        else:
            print("❌ Invalid choice. Please select a valid process.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
