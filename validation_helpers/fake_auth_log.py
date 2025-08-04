#!/usr/bin/env python3
import os
import sys
import json
import re

regex_pattern = r"\bCCRI-[A-Z0-9]{4}-\d{4}\b"
CHALLENGE_ID = "08_FakeAuthLog"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker.", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    json_file = "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    unlock_file = os.path.join(project_root, "web_version_admin", json_file)
    try:
        with open(unlock_file, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
        sys.exit(1)

def scan_for_flags(log_file, regex):
    matches = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR while scanning log: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

def validate_authlog_flag():
    project_root = find_project_root()
    log_path = os.path.join(project_root, "challenges", CHALLENGE_ID, "auth.log")
    expected_flag = load_expected_flag(project_root)

    if not os.path.isfile(log_path):
        print(f"❌ ERROR: auth.log not found at {log_path}", file=sys.stderr)
        sys.exit(1)

    matches = scan_for_flags(log_path, regex_pattern)
    if expected_flag in "\n".join(matches):
        print(f"✅ Validation success: found flag {expected_flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in auth.log.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    validate_authlog_flag()
