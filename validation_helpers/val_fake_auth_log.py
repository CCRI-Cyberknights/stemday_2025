#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "08_FakeAuthLog"
REGEX_PATTERN = r"\bCCRI-[A-Z0-9]{4}-\d{4}\b"

def scan_for_flags(log_path: Path, regex: str) -> list[str]:
    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if re.search(regex, line)]
    except Exception as e:
        print(f"❌ ERROR while scanning log: {e}", file=sys.stderr)
        return []

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")

    base_folder = "challenges_solo" if mode == "solo" else "challenges"
    log_path = root / base_folder / challenge_id / "auth.log"

    if not log_path.is_file():
        print(f"❌ ERROR: auth.log not found at {log_path}", file=sys.stderr)
        return False

    matches = scan_for_flags(log_path, REGEX_PATTERN)
    if expected_flag in "\n".join(matches):
        print(f"✅ Validation success: found flag {expected_flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in auth.log.", file=sys.stderr)
        return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
