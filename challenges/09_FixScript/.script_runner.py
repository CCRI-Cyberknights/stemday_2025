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

def flatten_broken_script_dir(script_dir, script_name):
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f == script_name and root != script_dir:
                src = os.path.join(root, f)
                dst = os.path.join(script_dir, f)
                if not os.path.exists(dst):
                    os.rename(src, dst)
        for d in dirs:
            try:
                os.rmdir(os.path.join(root, d))
            except OSError:
                pass

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
                if line.strip().startswith("code = part1"):
                    f.write(f"code = part1 {new_operator} part2  # <- fixed math\n")
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

    flatten_broken_script_dir(script_dir, SCRIPT_NAME)

    # 2. Mission Briefing
    header("🧪 Challenge #09 – Fix the Flag! (Python Edition)")
    
    print(f"📄 Broken script located: {Colors.BOLD}{broken_script}{Colors.END}\n")
    print(f"{Colors.RED}⚠️ This script calculates part of the flag incorrectly.{Colors.END}")
    print("💡 Your job is to change the math operator until the flag looks correct.\n")
    
    print("In a normal terminal, you might do something like:")
    print(f"   {Colors.GREEN}python {SCRIPT_NAME}{Colors.END}")
    print(f"   {Colors.GREEN}nano {SCRIPT_NAME}{Colors.END}    # edit the line that combines part1 and part2")
    print(f"   {Colors.GREEN}python {SCRIPT_NAME}{Colors.END}  # run again and check the result\n")
    
    print("This helper automates the edit-run-check cycle so you can focus on the logic:")
    print("   ➤ It runs the script and shows you the output.")
    print("   ➤ You choose which operator to try: +  -  * /")
    print("   ➤ It patches the line   code = part1 ? part2")
    print("      and runs the script again until a valid flag appears.\n")
    
    require_input("Type 'ready' when you're ready to check the files: ", "ready")

    # 3. File Inspection
    clear_screen()
    header("🔍 Source Code Inspection")
    print(f"Opening {Colors.BOLD}{SCRIPT_NAME}{Colors.END} to see what we're dealing with...\n")
    spinner("Reading file")
    
    if not os.path.isfile(broken_script):
        print_error(f"{SCRIPT_NAME} not found in {script_dir}.")
        sys.exit(1)

    print("\n" + "-" * 50)
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
    
    print(f"👀 Notice the line highlighted above? That determines how the flag is built.")
    print("   We need to change that operator to make the math work out.\n")

    require_input("Type 'run' to execute the broken script: ", "run")

    # 4. Interactive Debug Loop
    while True:
        print(f"\n💻 Running: {Colors.BOLD}python {SCRIPT_NAME}{Colors.END}")
        print("-" * 50)
        output = run_python_script(broken_script)
        
        # Highlight potential flag output
        if "CCRI-" in output:
            print(output.replace("CCRI-", f"{Colors.YELLOW}CCRI-") + Colors.END)
        else:
            print(output)
        print("-" * 50 + "\n")

        flag_line = next((line for line in output.splitlines() if "CCRI-SCRP" in line), None)

        if flag_line:
            match = re.search(r"CCRI-SCRP-(\d+)", flag_line)
            if match and len(match.group(1)) == 4:
                print_success("Valid flag found!")
                print(f"\n{Colors.GREEN}{Colors.BOLD}{flag_line}{Colors.END}\n")
                
                with open(flag_output_file, "w", encoding="utf-8") as f:
                    f.write(flag_line + "\n")
                
                print(f"📄 Flag saved to: {Colors.BOLD}{OUTPUT_FLAG_FILE}{Colors.END}")
                pause("🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish...")
                break
            else:
                print(f"{Colors.RED}⚠️ That flag isn't 4 digits long. Try a different operator.{Colors.END}")
        else:
            print(f"{Colors.RED}⚠️ No flag found. Double-check the script output.{Colors.END}\n")

        print(f"\n{Colors.CYAN}🛠️ Try a different operator to fix the math.{Colors.END}")
        print("   Options: +  (addition)   → add part1 and part2")
        print("            -  (subtraction)→ subtract part2 from part1")
        print("            * (multiply)   → multiply the values")
        print("            /  (divide)     → divide part1 by part2 (integer behavior may matter)\n")

        while True:
            op = input(f"{Colors.YELLOW}Enter operator to use (+, -, *, /): {Colors.END}").strip()
            if op in ["+", "-", "*", "/"]:
                break
            print(f"{Colors.RED}❌ Invalid operator. Please enter one of: +  -  * /{Colors.END}")

        patch_operator_in_script(broken_script, op)
        print("\n✏️ Patching broken_flag.py with new operator...")
        spinner("Updating script")
        clear_screen()

if __name__ == "__main__":
    main()