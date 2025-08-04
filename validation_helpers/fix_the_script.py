#!/usr/bin/env python3
import os
import sys
import json
import subprocess

CHALLENGE_ID = "09_FixScript"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_unlock_data(project_root):
    unlocks_path = os.path.join(project_root, "web_version_admin",
                                "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json")
    try:
        with open(unlocks_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        entry = unlocks[CHALLENGE_ID]
        return entry["real_flag"], entry.get("correct_operator", "+")
    except Exception as e:
        print(f"❌ ERROR loading unlock data: {e}", file=sys.stderr)
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
        print(f"❌ ERROR updating script: {e}", file=sys.stderr)
        sys.exit(1)

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
        print("❌ ERROR: Python interpreter not found.", file=sys.stderr)
        sys.exit(1)

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    script_path = os.path.join(challenge_dir, "broken_flag.py")

    if not os.path.isfile(script_path):
        print(f"❌ ERROR: broken_flag.py not found in {challenge_dir}", file=sys.stderr)
        sys.exit(1)

    expected_flag, correct_op = load_unlock_data(project_root)
    replace_operator(script_path, correct_op)

    output = run_python_script(script_path)
    if expected_flag in output:
        print(f"✅ Validation success: found flag {expected_flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in output.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
