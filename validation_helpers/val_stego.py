#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "01_Stego"

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

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    unlock = load_unlock_data(root, challenge_id)

    password = unlock.get("last_password")
    real_flag = unlock.get("real_flag")

    if not password:
        print("❌ ERROR: No password found in unlock metadata.", file=sys.stderr)
        return False
    if not real_flag:
        print("❌ ERROR: No real_flag found in unlock metadata. Regenerate or update generator metadata.", file=sys.stderr)
        return False

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    default_rel = f"{base_path}/{challenge_id}/squirrel.jpg"
    file_rel = unlock.get("challenge_file", default_rel)

    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        image_path = Path(sandbox_override) / "squirrel.jpg"
    else:
        image_path = root / file_rel

    output_path = image_path.parent / "decoded_message.txt"

    if not image_path.is_file():
        print(f"❌ ERROR: Image file not found: {image_path}", file=sys.stderr)
        return False

    if not run_steghide(password, image_path, output_path):
        print(f"❌ Validation failed: could not extract with password '{password}'", file=sys.stderr)
        return False

    try:
        text = output_path.read_text(errors="ignore")
    except Exception as e:
        print(f"❌ ERROR: couldn't read extracted file: {e}", file=sys.stderr)
        return False

    # ✅ Require the exact real flag to be present
    if real_flag in text:
        print(f"✅ Validation success: found real flag {real_flag} (password '{password}')")
        return True
    else:
        print("❌ Validation failed: extracted data did not contain the real flag.", file=sys.stderr)
        return False

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
