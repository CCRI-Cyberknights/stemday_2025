#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

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

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    broken_script = os.path.join(script_dir, "broken_flag.py")
    flag_output_file = os.path.join(script_dir, "flag.txt")

    flatten_broken_script_dir(script_dir, "broken_flag.py")

    clear_screen()
    print("🧪 Challenge #09 – Fix the Flag! (Python Edition)")
    print("===============================================\n")
    print(f"📄 Broken script located: {broken_script}\n")
    print("⚠️ This script calculates part of the flag incorrectly.")
    print("👉 Open it in a text editor (nano, vim, or mousepad) and examine the math.")
    print("💡 Your goal: fix the math operation and re-run the script.\n")
    pause("Press ENTER to attempt running the broken script...")

    if not os.path.isfile(broken_script):
        print("❌ ERROR: missing required file 'broken_flag.py'.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print("\n💻 Running: python broken_flag.py")
    print("----------------------------------------------")
    output = run_python_script(broken_script)
    print(output)
    print("----------------------------------------------\n")
    time.sleep(1)

    print("😮 If that output doesn't look right, edit the script and fix the math.")
    pause("Press ENTER once you've fixed it to test again...")

    print("\n🎉 Re-running fixed script...")
    fixed_output = run_python_script(broken_script)
    flag_line = next((line for line in fixed_output.splitlines() if "CCRI-SCRP" in line), None)

    if flag_line:
        print("----------------------------------------------")
        print(flag_line)
        print("----------------------------------------------")
        with open(flag_output_file, "w") as f:
            f.write(flag_line + "\n")
        print(f"📄 Flag saved to: {flag_output_file}\n")
        pause("🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish...")
    else:
        print("⚠️ Still no valid flag. Double-check your math and try again.")
        pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
