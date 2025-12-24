#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "03_ROT13"

def rot13(text: str) -> str:
    """Apply ROT13 cipher to input text."""
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr((ord(c) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            result.append(chr((ord(c) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(c)
    return "".join(result)

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"

    # 🧪 Check for sandbox override
    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        input_path = Path(sandbox_override) / "cipher.txt"
    else:
        input_path = root / base_path / challenge_id / "cipher.txt"

    if not input_path.is_file():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        return False

    try:
        decoded = "\n".join(rot13(line) for line in input_path.read_text(encoding="utf-8").splitlines())
    except Exception as e:
        print(f"❌ Failed to decode cipher file: {e}", file=sys.stderr)
        return False

    if flag in decoded:
        print(f"✅ Validation success: found flag {flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded content", file=sys.stderr)
        return False

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
