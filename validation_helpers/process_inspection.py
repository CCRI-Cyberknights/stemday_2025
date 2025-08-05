#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "15_ProcessInspection"

def validate_flag_in_ps_dump(ps_path: Path, expected_flag: str) -> bool:
    if not ps_path.is_file():
        print(f"❌ ERROR: ps_dump.txt not found at {ps_path}", file=sys.stderr)
        return False

    with ps_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if expected_flag in line:
                print(f"✅ Validation success: found flag {expected_flag}")
                return True

    print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
    return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    ps_path = root / base_path / challenge_id / "ps_dump.txt"

    return validate_flag_in_ps_dump(ps_path, expected_flag)

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
