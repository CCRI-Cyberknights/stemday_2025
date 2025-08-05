#!/usr/bin/env python3
import base64
import os
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data

def decode_file(input_path: Path) -> str:
    try:
        encoded = input_path.read_text(encoding="utf-8")
        return base64.b64decode(encoded).decode("utf-8").strip()
    except Exception as e:
        print(f"❌ Error decoding base64: {e}")
        return ""

def validate(mode="guided", challenge_id="02_Base64") -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    if mode == "guided":
        file_rel = data.get("challenge_file", f"challenges/{challenge_id}/encoded.txt")
    else:
        file_rel = f"challenges_solo/{challenge_id}/encoded.txt"

    input_path = root / file_rel
    if not input_path.exists():
        print(f"❌ Challenge file not found: {input_path}")
        return False

    decoded = decode_file(input_path)
    if flag in decoded:
        print(f"✅ Validation success: found flag {flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded content")
        return False

def required_files(mode="guided", challenge_id="02_Base64"):
    """Return a list of required files for validation (used for sandbox pre-checks)."""
    if mode == "guided":
        return [f"challenges/{challenge_id}/encoded.txt"]
    else:
        return [f"challenges_solo/{challenge_id}/encoded.txt"]

    mode = os.environ.get("CCRI_MODE", "guided")
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
