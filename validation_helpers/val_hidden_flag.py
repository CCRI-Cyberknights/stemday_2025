#!/usr/bin/env python3
import sys
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

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

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    junk_dir = root / base_path / challenge_id / "junk"

    if not junk_dir.is_dir():
        print(f"❌ ERROR: Expected directory not found: {junk_dir}", file=sys.stderr)
        return False

    return validate_hidden_flag(junk_dir, flag)

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
