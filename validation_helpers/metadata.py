#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "10_Metadata"

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = data["real_flag"]
    challenge_dir = root / "challenges" / CHALLENGE_ID
    target_image = challenge_dir / "capybara.jpg"

    if not target_image.exists():
        print(f"❌ ERROR: File not found: {target_image}", file=sys.stderr)
        sys.exit(1)

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
            sys.exit(0)
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found in metadata.", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("❌ ERROR: exiftool failed to run.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
