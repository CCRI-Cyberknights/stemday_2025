#!/usr/bin/env python3
import os
import sys
import subprocess
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "17_NmapScanning"

def fetch_port_response(port: int) -> str:
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

def validate_flag(expected_flag: str, expected_port: int) -> bool:
    print(f"🔎 Validating port {expected_port} for expected flag...")
    response = fetch_port_response(expected_port)

    # Keep the containment check if your server includes extra text with the flag
    if expected_flag in response:
        print(f"✅ Validation success: found real flag {expected_flag} on port {expected_port}")
        return True
    else:
        preview = (response[:200] + "…") if len(response) > 200 else response
        print("❌ Flag not found in response.")
        print(f"   Expected flag: {expected_flag}")
        print(f"   Response preview: {preview}")
        return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")
    expected_port = data.get("real_port")

    if not expected_flag or not expected_port:
        print("❌ Missing required validation data (flag or port).", file=sys.stderr)
        return False

    return validate_flag(expected_flag, expected_port)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
