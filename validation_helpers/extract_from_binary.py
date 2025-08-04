#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import re

regex_pattern = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'
CHALLENGE_ID = "07_ExtractBinary"

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

def run_strings(binary_path, output_path):
    try:
        with open(output_path, "w") as out_f:
            subprocess.run(["strings", binary_path], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.", file=sys.stderr)
        sys.exit(1)

def search_for_flags(file_path, regex):
    matches = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR during flag search: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

def validate_binary_flag():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    binary_path = os.path.join(script_dir, "..", "challenges", CHALLENGE_ID, "hidden_flag")
    extracted_path = os.path.join(script_dir, "extracted_strings.txt")
    expected_flag = load_expected_flag(project_root)

    if not os.path.isfile(binary_path):
        print(f"❌ ERROR: Binary file not found: {binary_path}", file=sys.stderr)
        sys.exit(1)

    run_strings(binary_path, extracted_path)
    matches = search_for_flags(extracted_path, regex_pattern)

    if expected_flag in matches:
        print(f"✅ Validation success: found flag {expected_flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in extracted strings.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    validate_binary_flag()
