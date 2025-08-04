#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "15_ProcessInspection"

def validate_flag_in_ps_dump(ps_path: Path, expected_flag: str) -> bool:
    if not ps_path.is_file():
        print(f"❌ ERROR: ps_dump.txt not found at {ps_path}", file=sys.stderr)
        return False

    with ps_path.open("r", encoding="utf-8") as f:
        for line in f:
            if expected_flag in line:
                print(f"✅ Validation success: found flag {expected_flag}")
                return True

    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = data["real_flag"]

    ps_path = root / "challenges" / CHALLENGE_ID / "ps_dump.txt"
    sys.exit(0 if validate_flag_in_ps_dump(ps_path, expected_flag) else 1)

if __name__ == "__main__":
    main()
