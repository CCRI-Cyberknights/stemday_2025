#!/usr/bin/env python3
import os
import sys
import json
import subprocess

CHALLENGE_ID = "17_Nmap_Scanning"
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"

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

def fetch_port_response(port):
    try:
        result = subprocess.run(
            ["curl", "-s", f"http://localhost:{port}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Curl failed: {e}")
        return ""

def validate_flag(expected_flag, expected_port):
    print(f"🔎 Validating port {expected_port} for expected flag...")
    response = fetch_port_response(expected_port)
    if expected_flag in response:
        print(f"✅ Found flag at port {expected_port}")
        return True
    else:
        print("❌ Flag not found in response.")
        print("Response:", response)
        return False

def main():
    project_root = find_project_root()
    mode = get_ctf_mode()
    unlock_file = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)

    try:
        with open(unlock_file, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        meta = unlocks[CHALLENGE_ID]
        expected_flag = meta["real_flag"]
        expected_port = meta["real_port"]
    except Exception as e:
        print(f"❌ Could not load validation data: {e}", file=sys.stderr)
        sys.exit(1)

    if validate_flag(expected_flag, expected_port):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
