#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "16_Hex_Hunting"
BINARY_NAME = "hex_flag.bin"

def validate_flag_in_binary(binary_path: Path, expected_flag: str) -> bool:
    if not binary_path.exists():
        print(f"❌ ERROR: {binary_path} not found", file=sys.stderr)
        return False

    try:
        result = subprocess.run(["strings", str(binary_path)], stdout=subprocess.PIPE, text=True, check=True)
        for line in result.stdout.splitlines():
            if expected_flag in line:
                print(f"✅ Found flag in strings output: {expected_flag}")
                return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running strings: {e}", file=sys.stderr)

    try:
        if expected_flag.encode("utf-8") in binary_path.read_bytes():
            print(f"✅ Found flag in raw bytes: {expected_flag}")
            return True
    except Exception as e:
        print(f"❌ Error reading binary file: {e}", file=sys.stderr)

    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    flag = data["real_flag"]

    binary_path = root / "challenges" / CHALLENGE_ID / BINARY_NAME

    if validate_flag_in_binary(binary_path, flag):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
