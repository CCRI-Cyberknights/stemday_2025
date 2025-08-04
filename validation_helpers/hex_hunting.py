#!/usr/bin/env python3
import os
import sys
import json
import subprocess

CHALLENGE_ID = "16_Hex_Hunting"
BINARY_FILE = "hex_flag.bin"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    unlock_path = os.path.join(
        project_root,
        "web_version_admin",
        "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    )
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
        sys.exit(1)

def validate_flag_in_binary(binary_path, expected_flag):
    if not os.path.isfile(binary_path):
        print(f"❌ ERROR: {binary_path} not found", file=sys.stderr)
        return False

    try:
        strings_out = subprocess.run(["strings", binary_path], stdout=subprocess.PIPE, text=True)
        for line in strings_out.stdout.splitlines():
            if expected_flag in line:
                print(f"✅ Found flag in strings output: {expected_flag}")
                return True
    except Exception as e:
        print(f"❌ Error scanning with strings: {e}", file=sys.stderr)

    try:
        with open(binary_path, "rb") as f:
            if expected_flag.encode("utf-8") in f.read():
                print(f"✅ Found flag in raw bytes: {expected_flag}")
                return True
    except Exception as e:
        print(f"❌ Error reading binary file: {e}", file=sys.stderr)

    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    binary_path = os.path.join(challenge_dir, BINARY_FILE)
    expected_flag = load_expected_flag(project_root)

    if validate_flag_in_binary(binary_path, expected_flag):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
