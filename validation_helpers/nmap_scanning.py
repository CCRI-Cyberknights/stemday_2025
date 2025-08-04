#!/usr/bin/env python3
import sys
import subprocess
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "17_Nmap_Scanning"

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
        print(f"❌ Curl failed: {e}", file=sys.stderr)
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
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = data["real_flag"]
    expected_port = data["real_port"]

    if validate_flag(expected_flag, expected_port):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
