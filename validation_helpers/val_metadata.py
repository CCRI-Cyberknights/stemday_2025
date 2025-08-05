#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "10_Metadata"

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    challenge_dir = root / base_path / challenge_id
    target_image = challenge_dir / "capybara.jpg"

    if not target_image.exists():
        print(f"❌ ERROR: File not found: {target_image}", file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            ["exiftool", str(target_image)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        if expected_flag in result.stdout:
            print(f"✅ Validation success: found flag {expected_flag}")
            return True
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found in metadata.", file=sys.stderr)
            return False
    except subprocess.CalledProcessError:
        print("❌ ERROR: exiftool failed to run.", file=sys.stderr)
        return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
