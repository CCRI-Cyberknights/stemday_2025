#!/usr/bin/env python3
import sys
import os
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

def decode_base64(path: Path) -> str:
    try:
        result = subprocess.run(
            ["base64", "--decode", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("❌ Base64 decoding failed.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return None

def unzip_with_password(zip_path: Path, password: str, extract_to: Path) -> bool:
    try:
        subprocess.run(
            ["unzip", "-o", "-P", password, str(zip_path), "-d", str(extract_to)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to extract {zip_path.name} with given password.", file=sys.stderr)
        return False

def main():
    challenge_id = "05_ArchivePassword"
    root = find_project_root()

    mode = os.environ.get("CCRI_MODE", "guided")
    base_folder = "challenges_solo" if mode == "solo" else "challenges"
    challenge_dir = root / base_folder / challenge_id

    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")
    zip_password = data.get("last_zip_password")

    zip_path = challenge_dir / "secret.zip"
    extract_dir = challenge_dir
    extracted_b64 = extract_dir / "message_encoded.txt"
    output_file = extract_dir / "decoded_output.txt"

    if not zip_path.exists():
        print(f"❌ Zip file missing: {zip_path}", file=sys.stderr)
        return 1

    if not unzip_with_password(zip_path, zip_password, extract_dir):
        return 1

    if not extracted_b64.exists():
        print(f"❌ Extracted file missing: {extracted_b64}", file=sys.stderr)
        return 1

    decoded = decode_base64(extracted_b64)
    if decoded is None:
        return 1

    output_file.write_text(decoded + "\n", encoding="utf-8")

    if flag in decoded:
        print(f"✅ Validation success: flag {flag} found")
        return 0
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded output", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
