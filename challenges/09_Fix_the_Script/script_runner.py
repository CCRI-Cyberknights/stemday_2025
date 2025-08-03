#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import json

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "09_FixScript"

# === Detect Validation Mode
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

# === Utilities
def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_unlock_data(project_root):
    json_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        entry = unlocks[CHALLENGE_ID]
        return entry["real_flag"], entry.get("correct_operator", "+")
    except Exception as e:
        print(f"❌ ERROR: Could not load unlock data: {e}", file=sys.stderr)
        sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('cls' if os.name == 'nt' else 'clear')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
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

def replace_operator(script_path, new_operator):
    try:
        with open(script_path, "r") as f:
            lines = f.readlines()
        with open(script_path, "w") as f:
            for line in lines:
                if "code =" in line and any(op in line for op in ["+", "-", "*", "/"]):
                    f.write(f"code = part1 {new_operator} part2  # <- fixed math\n")
                else:
                    f.write(line)
    except Exception as e:
        print(f"❌ ERROR updating script: {e}")
        sys.exit(1)

# === Main Logic
def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    broken_script = os.path.join(script_dir, "broken_flag.py")
    flag_output_file = os.path.join(script_dir, "flag.txt")

    flatten_broken_script_dir(script_dir, "broken_flag.py")

    # === Validation Mode ===
    if validation_mode:
        expected_flag, correct_op = load_unlock_data(project_root)
        replace_operator(broken_script, correct_op)
        fixed_output = run_python_script(broken_script)

        if expected_flag in fixed_output:
            print(f"✅ Validation success: found flag {expected_flag}")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
            sys.exit(1)

    # === Student Mode ===
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
