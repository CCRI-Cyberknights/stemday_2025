#!/usr/bin/env python3
import os
import sys
import json

CHALLENGE_ID = "13_HTTPHeaders"

def find_project_root():
    path = os.path.abspath(os.path.dirname(__file__))
    while path != "/":
        if os.path.exists(os.path.join(path, ".ccri_ctf_root")):
            return path
        path = os.path.dirname(path)
    print("❌ ERROR: .ccri_ctf_root not found.", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    json_file = "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    unlock_path = os.path.join(project_root, "web_version_admin", json_file)
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            return json.load(f)[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Failed to load expected flag: {e}", file=sys.stderr)
        sys.exit(1)

def validate_responses(challenge_dir, expected_flag):
    for i in range(1, 6):
        file = os.path.join(challenge_dir, f"response_{i}.txt")
        if not os.path.isfile(file):
            print(f"❌ Missing file: {file}", file=sys.stderr)
            continue
        try:
            with open(file, "r", encoding="utf-8") as f:
                if expected_flag in f.read():
                    print(f"✅ Found flag {expected_flag} in {os.path.basename(file)}")
                    return True
        except Exception as e:
            print(f"❌ Error reading {file}: {e}", file=sys.stderr)
    print(f"❌ Flag {expected_flag} not found in any response.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    expected_flag = load_expected_flag(project_root)

    if validate_responses(challenge_dir, expected_flag):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
