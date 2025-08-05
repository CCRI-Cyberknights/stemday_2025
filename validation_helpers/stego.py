#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "01_Stego"

def run_steghide(password: str, image_path: Path, output_path: Path) -> bool:
    """Attempt to extract hidden data from an image using steghide."""
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", str(image_path), "-xf", str(output_path), "-p", password, "-f"],
            input=b"\n",  # Avoids overwrite prompt
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0
    except FileNotFoundError:
        print("❌ ERROR: steghide is not installed.", file=sys.stderr)
        return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    unlock = load_unlock_data(root, challenge_id)

    password = unlock.get("last_password")
    if not password:
        print("❌ ERROR: No password found in unlock metadata.", file=sys.stderr)
        return False

    if mode == "guided":
        file_rel = unlock.get("challenge_file", f"challenges/{challenge_id}/squirrel.jpg")
    else:
        file_rel = f"challenges_solo/{challenge_id}/squirrel.jpg"

    image_path = root / file_rel
    output_path = image_path.parent / "decoded_message.txt"

    if not image_path.is_file():
        print(f"❌ ERROR: Image file not found: {image_path}", file=sys.stderr)
        return False

    if run_steghide(password, image_path, output_path):
        print(f"✅ Validation success: extracted flag using password '{password}'")
        return True
    else:
        print(f"❌ Validation failed: could not extract flag with password '{password}'", file=sys.stderr)
        return False

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
