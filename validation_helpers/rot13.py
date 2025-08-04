#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data

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

def main():
    challenge_id = "03_ROT13"
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)

    flag = data["real_flag"]
    file_rel = data.get("challenge_file", "challenges/03_ROT13/cipher.txt")
    input_path = root / file_rel

    if not input_path.is_file():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        decoded = "\n".join(rot13(line) for line in input_path.read_text(encoding="utf-8").splitlines())
    except Exception as e:
        print(f"❌ Failed to decode cipher file: {e}", file=sys.stderr)
        sys.exit(1)

    if flag in decoded:
        print(f"✅ Validation success: found flag {flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded content", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
