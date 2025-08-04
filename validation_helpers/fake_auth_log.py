#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "08_FakeAuthLog"
REGEX_PATTERN = r"\bCCRI-[A-Z0-9]{4}-\d{4}\b"

def scan_for_flags(log_path: Path, regex: str):
    try:
        with log_path.open("r") as f:
            return [line.strip() for line in f if re.search(regex, line)]
    except Exception as e:
        print(f"❌ ERROR while scanning log: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = data.get("real_flag")

    mode = os.environ.get("CCRI_MODE", "guided")
    log_relpath = f"challenges/{CHALLENGE_ID}/auth.log" if mode == "guided" else f"challenges_solo/{CHALLENGE_ID}/auth.log"
    log_path = root / log_relpath

    if not log_path.is_file():
        print(f"❌ ERROR: auth.log not found at {log_path}", file=sys.stderr)
        return 1

    matches = scan_for_flags(log_path, REGEX_PATTERN)

    if expected_flag in "\n".join(matches):
        print(f"✅ Validation success: found flag {expected_flag}")
        return 0
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in auth.log.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
