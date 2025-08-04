#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

def run_steghide(password: str, image_path: Path, output_path: Path) -> bool:
    """Attempt to extract hidden data from an image using steghide."""
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", str(image_path), "-xf", str(output_path), "-p", password, "-f"],
            input=b"\n",  # Avoids prompt for overwrite
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
    unlock = load_unlock_data(root, challenge_id)

    password = unlock.get("last_password")
    if not password:
        print("❌ ERROR: No password found in unlock metadata.", file=sys.stderr)
        sys.exit(1)

    file_rel = unlock.get("challenge_file", "challenges/01_Stego/squirrel.jpg")
    challenge_dir = root / Path(file_rel).parts[0] / Path(file_rel).parts[1]
    image_path = challenge_dir / "squirrel.jpg"
    output_path = challenge_dir / "decoded_message.txt"

    if not image_path.is_file():
        print(f"❌ ERROR: Image file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    if run_steghide(password, image_path, output_path):
        print(f"✅ Validation success: extracted flag using password '{password}'")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: could not extract flag with password '{password}'", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
