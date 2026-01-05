#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
SCRIPT_NAME = "broken_flag.py"
OUTPUT_FLAG_FILE = "flag.txt"

def get_path(filename):
    """Ensure the file is saved next to this script, regardless of where it's run from."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def run_python_script(script_path):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print_error("Python interpreter not found.")
        sys.exit(1)

def patch_operator_in_script(script_path, new_operator):
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(script_path, "w", encoding="utf-8") as f:
            for line in lines:
                if "code = part1" in line:
                    # Replace whatever operator is there with the new one
                    # Regex looks for: part1 [any char] part2
                    new_line = re.sub(r"part1\s*[\+\-\*\/]\s*part2", f"part1 {new_operator} part2", line)
                    f.write(new_line)
                else:
                    f.write(line)
    except Exception as e:
        print_error(f"Error patching script: {e}")
        sys.exit(1)

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    broken_script = get_path(SCRIPT_NAME)
    flag_output_file = get_path(OUTPUT_FLAG_FILE)

    if not os.path.isfile(broken_script):
        print_error(f"{SCRIPT_NAME} not found in {script_dir}.")
        sys.exit(1)

    # 2. Mission Briefing
    header("🐛 Python Debugging Challenge")
    
    print(f"📄 Broken script: {Colors.BOLD}{SCRIPT_NAME}{Colors.END}")
    print(f"🔧 Strategy: {Colors.BOLD}Debugging{Colors.END}\n")
    print("🎯 Goal: Fix the logic error in the script to reveal the flag.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Problem:** The script executes, but the math logic is flawed.")
    print("   ➤ **The Clue:** It calculates a 4-digit code using `part1` and `part2`.")
    print("   ➤ **The Strategy:** Read -> Analyze -> Edit.")
    print("   ➤ **The Task:** Find the correct operator (+, -, *, /).\n")
    
    require_input("Type 'ready' to inspect the source code: ", "ready")

    # 3. File Inspection
    header("🔍 Step 1: Read Source Code")
    print(f"Opening {Colors.BOLD}{SCRIPT_NAME}{Colors.END}...\n")
    
    print("-" * 50)
    try:
        with open(broken_script, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                # Highlight the broken logic line
                if "code = part1" in line:
                    print(f"{Colors.YELLOW}{Colors.BOLD}>> {line.strip()} <<  (THIS IS THE BUG){Colors.END}")
                else:
                    print(line.rstrip())
    except Exception as e:
        print_error(f"Could not read script: {e}")
    print("-" * 50 + "\n")
    
    print(f"👀 Notice the line highlighted above? That determines the security code.")
    print("   We need to change that operator to make the math work out.\n")

    require_input("Type 'run' to test the current broken script: ", "run")

    # 4. Interactive Debug Loop
    while True:
        clear_screen()
        header("💻 Debug Console")
        print(f"Running: {Colors.BOLD}python {SCRIPT_NAME}{Colors.END}")
        print("-" * 50)
        output = run_python_script(broken_script)
        print(output)
        print("-" * 50 + "\n")

        # Check for success
        # The script prints "Generated Flag: CCRI-AAAA-1111" on success
        if "CCRI-" in output and "INVALID" not in output and "Error" not in output:
             # Find the flag line for saving
            match = re.search(r"CCRI-[A-Z]{4}-\d{4}", output)
            if match:
                flag = match.group(0)
                print_success(f"SUCCESS! Logic Fixed. Flag: {Colors.BOLD}{flag}{Colors.END}")
                with open(flag_output_file, "w") as f:
                    f.write(flag + "\n")
                print(f"📁 Saved to: {Colors.BOLD}{OUTPUT_FLAG_FILE}{Colors.END}")
                pause("Press ENTER to finish...")
                break

        print(f"{Colors.RED}⚠️ The output looks wrong. The math operator is incorrect.{Colors.END}\n")
        
        print(f"{Colors.CYAN}🛠️ Select a patch to apply:{Colors.END}")
        print("   [+] Addition       (part1 + part2)")
        print("   [-] Subtraction    (part1 - part2)")
        print("   [*] Multiplication (part1 * part2)")
        print("   [/] Division       (part1 / part2)")
        print("   [q] Quit")
        
        op = input(f"\n{Colors.YELLOW}Enter operator (+, -, *, /): {Colors.END}").strip()
        
        if op == 'q':
            break
            
        if op in ["+", "-", "*", "/"]:
            print(f"\n✏️ Patching {SCRIPT_NAME} with operator '{op}'...")
            patch_operator_in_script(broken_script, op)
            spinner("Updating code")
        else:
            print(f"{Colors.RED}❌ Invalid operator.{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    main()