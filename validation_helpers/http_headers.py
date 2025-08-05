#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "13_HTTPHeaders"

def validate_responses(challenge_dir: Path, expected_flag: str) -> bool:
    for i in range(1, 6):
        file = challenge_dir / f"response_{i}.txt"
        if not file.exists():
            print(f"❌ Missing file: {file}", file=sys.stderr)
            continue
        try:
            content = file.read_text(encoding="utf-8", errors="ignore")
            if expected_flag in content:
                print(f"✅ Found flag {expected_flag} in {file.name}")
                return True
        except Exception as e:
            print(f"❌ Error reading {file}: {e}", file=sys.stderr)
    print(f"❌ Flag {expected_flag} not found in any response file.", file=sys.stderr)
    return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    challenge_dir = root / base_path / challenge_id

    return validate_responses(challenge_dir, flag)

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
