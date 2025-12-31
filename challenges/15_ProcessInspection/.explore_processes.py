#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shlex

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
DUMP_FILE = "ps_dump.txt"
OUTPUT_FILE = "process_output.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def relaunch_in_bigger_terminal(script_path):
    """Re-executes the script in a larger MATE Terminal window for visibility."""
    if os.environ.get("BIGGER_TERMINAL") == "1":
        return

    os.environ["BIGGER_TERMINAL"] = "1"
    abs_script = os.path.abspath(script_path)
    print_info("Launching in a larger terminal window for better visibility...")
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
        print_error("MATE Terminal not found. Continuing in current terminal.")

def load_process_map(ps_dump_path):
    """Parses ps_dump.txt and returns a {binary: full_command} mapping."""
    proc_map = {}
    try:
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
    except FileNotFoundError:
        return {}
    return proc_map

def inspect_process(binary, ps_dump_path):
    """Displays matching line(s) from ps_dump.txt and formats arguments."""
    clear_screen()
    print(f"\n🔍 Inspecting process: {Colors.BOLD}{binary}{Colors.END}")
    print("-" * 50)
    time.sleep(0.5)

    try:
        result = subprocess.run(
            ["grep", binary, ps_dump_path],
            stdout=subprocess.PIPE,
            text=True
        )
        if not result.stdout.strip():
            print_error("No matching process found.")
        else:
            # Visual formatting to make long argument lists easier to read
            formatted = result.stdout.replace("--", "\n    --")
            print(f"{Colors.YELLOW}{formatted}{Colors.END}")
            print("-" * 50)
            return formatted
    except Exception as e:
        print_error(f"Error inspecting process: {e}")
    return ""

def save_output(text, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print_success(f"Output saved to {os.path.basename(path)}")
    except Exception as e:
        print_error(f"Failed to save output: {e}")

def main():
    # 1. Setup (Special resize for this challenge)
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    ps_dump_path = get_path(DUMP_FILE)
    output_path = get_path(OUTPUT_FILE)

    relaunch_in_bigger_terminal(__file__)
    
    # 2. Mission Briefing
    header("🖥️  Process Inspection")
    
    print(f"You've obtained a snapshot of running processes ({Colors.BOLD}{DUMP_FILE}{Colors.END}).\n")
    print(f"🎯 Your goal: Find the rogue process hiding a flag in a {Colors.BOLD}--flag={Colors.END} argument!\n")
    print(f"{Colors.CYAN}🧠 Flag format: CCRI-AAAA-1111{Colors.END}")
    print("   Somewhere in the command line of a process, a --flag= argument hides the real CCRI flag.\n")
    
    require_input("Type 'ready' when you're ready to learn how we're inspecting these processes: ", "ready")

    if not os.path.isfile(ps_dump_path):
        print_error(f"{DUMP_FILE} not found in this folder!")
        sys.exit(1)

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("This challenge is based on the output of a Linux process listing command like:\n")
    print(f"   {Colors.GREEN}ps aux{Colors.END}")
    print("\nThat output was saved into ps_dump.txt for offline analysis.")
    print("Each line typically contains:")
    print(f"   {Colors.BOLD}USER  PID  CPU%  MEM%  VSZ  RSS  TTY  STAT  TIME  COMMAND{Colors.END}")
    print("   ...and the COMMAND column includes the full command line.\n")
    print("In a normal investigation, you might do things like:\n")
    print(f"   {Colors.GREEN}grep 'python' ps_dump.txt{Colors.END}       # find all python processes")
    print(f"   {Colors.GREEN}grep '--flag=' ps_dump.txt{Colors.END}      # find any process with a --flag argument\n")
    print("This helper script:")
    print("   ➤ Builds a list of unique binaries from ps_dump.txt")
    print("   ➤ Lets you choose one by name")
    print("   ➤ Shows you the full command line so you can spot suspicious arguments\n")
    
    require_input("Type 'start' when you're ready to view the process list: ", "start")

    proc_map = load_process_map(ps_dump_path)
    display_names = sorted(proc_map.keys())

    # 4. Interactive Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}📂 Process List (from {DUMP_FILE}):{Colors.END}")
        print("-" * 40)
        for idx, name in enumerate(display_names, 1):
            print(f"{Colors.BOLD}{idx}{Colors.END}. {name}")
        print(f"{len(display_names) + 1}. Exit")
        print("-" * 40)

        try:
            choice = int(input(f"\n{Colors.YELLOW}Select a process to inspect (1-{len(display_names)+1}): {Colors.END}").strip())
        except ValueError:
            print_error("Invalid input. Please enter a number.")
            pause()
            continue

        if 1 <= choice <= len(display_names):
            binary = display_names[choice - 1]
            result_text = inspect_process(binary, ps_dump_path)

            if result_text:
                while True:
                    print("\nOptions:")
                    print("1. Return to process list")
                    print(f"2. Save this output to a file ({OUTPUT_FILE})\n")
                    option = input(f"{Colors.YELLOW}Choose an option (1–2): {Colors.END}").strip()

                    if option == "1":
                        break
                    elif option == "2":
                        save_output(result_text, output_path)
                        pause()
                        break
                    else:
                        print_error("Invalid choice.")
        elif choice == len(display_names) + 1:
            print(f"\n{Colors.CYAN}👋 Exiting. Good luck identifying the rogue process!{Colors.END}")
            break
        else:
            print_error("Invalid choice. Please select a valid process.")
            pause()

if __name__ == "__main__":
    main()