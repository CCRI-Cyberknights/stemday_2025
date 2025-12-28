#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def require_input(prompt, expected):
    """
    Pauses and requires the user to type a specific word (case-insensitive) to continue.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

def spinner(message="Working", duration=1.5, interval=0.12):
    """
    Simple text spinner to give the feeling of work being done.
    """
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{message}... {frame}")
        sys.stdout.flush()
        time.sleep(interval)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

# === File Helpers ===
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
        print("❌ ERROR: Python interpreter not found.")
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
        print(f"❌ ERROR patching script: {e}")
        sys.exit(1)

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    broken_script = os.path.join(script_dir, "broken_flag.py")
    flag_output_file = os.path.join(script_dir, "flag.txt")

    flatten_broken_script_dir(script_dir, "broken_flag.py")

    clear_screen()
    print("🧪 Challenge #09 – Fix the Flag! (Python Edition)")
    print("===============================================\n")
    print(f"📄 Broken script located: {broken_script}\n")
    print("⚠️ This script calculates part of the flag incorrectly.")
    print("💡 Your job is to change the math operator until the flag looks correct.\n")
    print("In a normal terminal, you might do something like:\n")
    print("   python broken_flag.py")
    print("   nano broken_flag.py    # edit the line that combines part1 and part2")
    print("   python broken_flag.py  # run again and check the result\n")
    print("This helper automates the edit-run-check cycle so you can focus on the logic:\n")
    print("   ➤ It runs the script and shows you the output.")
    print("   ➤ You choose which operator to try: +  -  * /")
    print("   ➤ It patches the line   code = part1 ? part2")
    print("      and runs the script again until a valid flag appears.\n")
    
    require_input("Type 'ready' when you're ready to check the files: ", "ready")

    if not os.path.isfile(broken_script):
        print(f"\n❌ ERROR: broken_flag.py not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    require_input("Type 'run' to execute the broken script: ", "run")

    while True:
        print("\n💻 Running: python broken_flag.py")
        print("----------------------------------------------")
        output = run_python_script(broken_script)
        print(output)
        print("----------------------------------------------\n")

        flag_line = next((line for line in output.splitlines() if "CCRI-SCRP" in line), None)

        if flag_line:
            match = re.search(r"CCRI-SCRP-(\d+)", flag_line)
            if match and len(match.group(1)) == 4:
                print("✅ Valid flag found!")
                print("----------------------------------------------")
                print(flag_line)
                print("----------------------------------------------")
                with open(flag_output_file, "w", encoding="utf-8") as f:
                    f.write(flag_line + "\n")
                print(f"📄 Flag saved to: {flag_output_file}\n")
                pause("🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish...")
                break
            else:
                print("⚠️ That flag isn't 4 digits long. Try a different operator.")
        else:
            print("⚠️ No flag found. Double-check the script output.\n")

        print("\n🛠️ Try a different operator to fix the math.")
        print("   Options: +  (addition)   → add part1 and part2")
        print("            -  (subtraction)→ subtract part2 from part1")
        print("            * (multiply)   → multiply the values")
        print("            /  (divide)     → divide part1 by part2 (integer behavior may matter)\n")

        while True:
            op = input("Enter operator to use (+, -, *, /): ").strip()
            if op in ["+", "-", "*", "/"]:
                break
            print("❌ Invalid operator. Please enter one of: +  -  * /")

        patch_operator_in_script(broken_script, op)
        print("\n✏️ Patching broken_flag.py with new operator...")
        spinner("Updating script")
        clear_screen()

if __name__ == "__main__":
    main()