#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shlex

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def relaunch_in_bigger_terminal(script_path):
    """Re-executes the script in a larger MATE Terminal window for visibility."""
    if os.environ.get("BIGGER_TERMINAL") == "1":
        return

    os.environ["BIGGER_TERMINAL"] = "1"
    abs_script = os.path.abspath(script_path)
    print("🔄 Launching in a larger terminal window for better visibility...")
    time.sleep(1)

    try:
        subprocess.Popen([
            "mate-terminal",
            "--", "bash", "-c",
            f"printf '\\033[8;48;140t'; python3 '{abs_script}'; exec bash"
        ])
        time.sleep(1)
        os._exit(0)
    except FileNotFoundError:
        print("⚠️ MATE Terminal not found. Continuing in current terminal.")

def load_process_map(ps_dump_path):
    """Parses ps_dump.txt and returns a {binary: full_command} mapping."""
    proc_map = {}
    with open(ps_dump_path, "r", encoding="utf-8") as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split(maxsplit=10)
            if len(parts) == 11:
                full_cmd = parts[10]
                try:
                    args = shlex.split(full_cmd)
                    binary = args[0] if args else full_cmd
                except Exception:
                    binary = full_cmd  # Fallback on parsing error

                if binary not in proc_map:
                    proc_map[binary] = full_cmd
    return proc_map

def inspect_process(binary, ps_dump_path):
    """Displays matching line(s) from ps_dump.txt and formats arguments."""
    print(f"\n🔍 Inspecting process: {binary}")
    print("=================================\n")
    time.sleep(0.5)

    try:
        result = subprocess.run(
            ["grep", binary, ps_dump_path],
            stdout=subprocess.PIPE,
            text=True
        )
        if not result.stdout.strip():
            print("⚠️ No matching process found.")
        else:
            formatted = result.stdout.replace("--", "\n    --")
            print(formatted)
            print("=================================")
            return formatted
    except Exception as e:
        print(f"❌ Error inspecting process: {e}")
    return ""

def save_output(text, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Output saved to {os.path.basename(path)}")
    except Exception as e:
        print(f"❌ Failed to save output: {e}")

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    ps_dump_path = os.path.join(script_dir, "ps_dump.txt")

    relaunch_in_bigger_terminal(__file__)
    clear_screen()

    print("🖥️  Process Inspection")
    print("=================================\n")
    print("You've obtained a snapshot of running processes (ps_dump.txt).\n")
    print("🎯 Your goal: Find the rogue process hiding a flag in a --flag= argument!\n")
    print("💡 Tip: The real flag starts with CCRI-AAAA-1111.")
    print("   You'll inspect processes one by one to uncover hidden details.\n")
    pause()

    if not os.path.isfile(ps_dump_path):
        print(f"❌ ERROR: {os.path.basename(ps_dump_path)} not found in this folder!")
        pause("Press ENTER to exit...")
        sys.exit(1)

    proc_map = load_process_map(ps_dump_path)
    display_names = sorted(proc_map.keys())

    while True:
        print("=================================")
        print("📂 Process List (from ps_dump.txt):")
        for idx, name in enumerate(display_names, 1):
            print(f"{idx}. {name}")
        print(f"{len(display_names) + 1}. Exit\n")

        try:
            choice = int(input(f"Select a process to inspect (1-{len(display_names)+1}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            pause()
            clear_screen()
            continue

        if 1 <= choice <= len(display_names):
            binary = display_names[choice - 1]
            result_text = inspect_process(binary, ps_dump_path)

            if result_text:
                while True:
                    print("\nOptions:")
                    print("1. Return to process list")
                    print("2. Save this output to a file (process_output.txt)\n")
                    option = input("Choose an option (1–2): ").strip()

                    if option == "1":
                        clear_screen()
                        break
                    elif option == "2":
                        save_output(result_text, os.path.join(script_dir, "process_output.txt"))
                        pause()
                        clear_screen()
                        break
                    else:
                        print("❌ Invalid choice. Please select 1 or 2.")
        elif choice == len(display_names) + 1:
            print("\n👋 Exiting. Good luck identifying the rogue process!")
            break
        else:
            print("❌ Invalid choice. Please select a valid process.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
