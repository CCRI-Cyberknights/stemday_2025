#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "11_HiddenFlag"

def validate_hidden_flag(directory: Path, expected_flag: str) -> bool:
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(errors="ignore")
                if expected_flag in content:
                    print(f"✅ Validation success: found flag {expected_flag} in {file_path}")
                    return True
            except Exception:
                continue
    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    flag = data["real_flag"]

    junk_dir = root / "challenges" / CHALLENGE_ID / "junk"

    if not junk_dir.is_dir():
        print(f"❌ ERROR: Expected directory not found: {junk_dir}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0 if validate_hidden_flag(junk_dir, flag) else 1)

if __name__ == "__main__":
    main()
