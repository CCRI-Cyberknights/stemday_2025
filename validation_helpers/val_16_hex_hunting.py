#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "16_HexHunting"
BINARY_NAME = "hex_flag.bin"

def validate_flag_in_binary(binary_path: Path, expected_flag: str) -> bool:
    if not binary_path.exists():
        print(f"❌ ERROR: {binary_path} not found", file=sys.stderr)
        return False

    # Check strings output
    try:
        result = subprocess.run(["strings", str(binary_path)],
                                stdout=subprocess.PIPE, text=True, check=True)
        for line in result.stdout.splitlines():
            if expected_flag in line:
                print(f"✅ Found flag in strings output: {expected_flag}")
                return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running strings: {e}", file=sys.stderr)

    # Check raw bytes
    try:
        if expected_flag.encode("utf-8") in binary_path.read_bytes():
            print(f"✅ Found flag in raw bytes: {expected_flag}")
            return True
    except Exception as e:
        print(f"❌ Error reading binary file: {e}", file=sys.stderr)

    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        binary_path = Path(sandbox_override) / BINARY_NAME
    else:
        base_folder = "challenges_solo" if mode == "solo" else "challenges"
        binary_path = root / base_folder / challenge_id / BINARY_NAME


    return validate_flag_in_binary(binary_path, flag)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
