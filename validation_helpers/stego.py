#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

def run_steghide(password: str, image_path: Path, output_path: Path) -> bool:
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", str(image_path), "-xf", str(output_path), "-p", password, "-f"],
            input=b"\n",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0
    except FileNotFoundError:
        print("❌ ERROR: steghide is not installed.", file=sys.stderr)
        return False

def main():
    challenge_id = "01_Stego"
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)

    password = data.get("last_password")
    if not password:
        print("❌ ERROR: No password found in unlock metadata.", file=sys.stderr)
        sys.exit(1)

    challenge_dir = root / "challenges" / data.get("challenge_file", "01_Stego").split("/")[1]
    target_image = challenge_dir / "squirrel.jpg"
    decoded_output = challenge_dir / "decoded_message.txt"

    if not target_image.exists():
        print(f"❌ ERROR: Target image not found: {target_image}", file=sys.stderr)
        sys.exit(1)

    if run_steghide(password, target_image, decoded_output):
        print(f"✅ Validation success: extracted flag with password '{password}'")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: could not extract flag with password '{password}'", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
