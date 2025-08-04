#!/usr/bin/env python3
import os
import sys
import json

CHALLENGE_ID = "11_HiddenFlag"

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

def load_expected_flag(project_root):
    path = os.path.join(
        project_root,
        "web_version_admin",
        "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    )
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR loading flag: {e}", file=sys.stderr)
        sys.exit(1)

def validate_hidden_flag(root_dir, expected_flag):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r") as f:
                    if expected_flag in f.read():
                        print(f"✅ Validation success: found flag {expected_flag} in {file_path}")
                        return True
            except Exception:
                continue
    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    junk_dir = os.path.join(challenge_dir, "junk")
    expected_flag = load_expected_flag(project_root)

    if not os.path.isdir(junk_dir):
        print(f"❌ ERROR: Expected directory not found: {junk_dir}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0 if validate_hidden_flag(junk_dir, expected_flag) else 1)

if __name__ == "__main__":
    main()
