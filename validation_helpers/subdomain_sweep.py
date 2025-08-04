#!/usr/bin/env python3
import os
import sys
import json

CHALLENGE_ID = "14_SubdomainSweep"

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
    unlock_file = "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    unlock_path = os.path.join(project_root, "web_version_admin", unlock_file)
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            return json.load(f)[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Failed to load expected flag from {unlock_path}: {e}", file=sys.stderr)
        sys.exit(1)

def validate_subdomains(domains, challenge_dir, expected_flag):
    for domain in domains:
        file_path = os.path.join(challenge_dir, f"{domain}.liber8.local.html")
        if not os.path.isfile(file_path):
            print(f"❌ Missing file: {file_path}", file=sys.stderr)
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if expected_flag in f.read():
                    print(f"✅ Found flag {expected_flag} in {os.path.basename(file_path)}")
                    return True
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}", file=sys.stderr)
    print(f"❌ Flag {expected_flag} not found in any subdomain file.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    expected_flag = load_expected_flag(project_root)
    domains = ["alpha", "beta", "gamma", "delta", "omega"]

    if validate_subdomains(domains, challenge_dir, expected_flag):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
