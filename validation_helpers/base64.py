#!/usr/bin/env python3
import sys
import base64
from pathlib import Path
from common import find_project_root, load_unlock_data

def decode_file(input_path: Path) -> str:
    try:
        encoded = input_path.read_text(encoding="utf-8")
        return base64.b64decode(encoded).decode("utf-8").strip()
    except Exception as e:
        print(f"❌ Error decoding base64: {e}")
        return ""

def main():
    challenge_id = "02_Base64"
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)

    flag = data.get("real_flag")
    file_rel = data.get("challenge_file", "challenges/02_Base64/encoded.txt")
    input_path = root / file_rel

    if not input_path.exists():
        print(f"❌ Challenge file not found: {input_path}")
        sys.exit(1)

    decoded = decode_file(input_path)
    if flag in decoded:
        print(f"✅ Validation success: found flag {flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded content")
        sys.exit(1)

if __name__ == "__main__":
    main()
