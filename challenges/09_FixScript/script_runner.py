#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

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

def patch_operator_in_script(script_path, new_operator):
    try:
        with open(script_path, "r") as f:
            lines = f.readlines()
        with open(script_path, "w") as f:
            for line in lines:
                if line.strip().startswith("code = part1"):
                    f.write(f"code = part1 {new_operator} part2  # <- fixed math\n")
                else:
                    f.write(line)
    except Exception as e:
        print(f"❌ ERROR patching script: {e}")
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
    print("💡 Your goal: try different math operations to fix it.\n")

    pause("Press ENTER to attempt running the broken script...")

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
                with open(flag_output_file, "w") as f:
                    f.write(flag_line + "\n")
                print(f"📄 Flag saved to: {flag_output_file}\n")
                pause("🎯 Copy the flag and enter it in the scoreboard when ready. Press ENTER to finish...")
                break
            else:
                print("⚠️ That flag isn't 4 digits long. Try a different operator.")
        else:
            print("⚠️ No flag found. Double-check the script.")

        print("\n🛠️ Try a different operator to fix the math.")
        op = input("Enter operator to use (+, -, *, /): ").strip()
        if op not in ["+", "-", "*", "/"]:
            print("❌ Invalid operator. Please enter one of: +  -  *  /")
            continue

        patch_operator_in_script(broken_script, op)
        time.sleep(0.5)
        clear_screen()

if __name__ == "__main__":
    main()
