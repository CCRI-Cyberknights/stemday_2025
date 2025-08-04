#!/usr/bin/env python3
import sys
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
        sys.exit(1)

def unzip_with_password(zip_path: Path, password: str, extract_to: Path):
    try:
        subprocess.run(
            ["unzip", "-o", "-P", password, str(zip_path), "-d", str(extract_to)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"❌ Failed to extract {zip_path.name} with given password.", file=sys.stderr)
        sys.exit(1)

def main():
    challenge_id = "05_ArchivePassword"
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)

    flag = data.get("real_flag")
    zip_password = data.get("last_zip_password")
    zip_path = root / "challenges" / challenge_id / "secret.zip"
    extract_dir = zip_path.parent
    extracted_b64 = extract_dir / "message_encoded.txt"
    output_file = extract_dir / "decoded_output.txt"

    if not zip_path.exists():
        print(f"❌ Zip file missing: {zip_path}", file=sys.stderr)
        sys.exit(1)

    unzip_with_password(zip_path, zip_password, extract_dir)

    if not extracted_b64.exists():
        print(f"❌ Extracted file missing: {extracted_b64}", file=sys.stderr)
        sys.exit(1)

    decoded = decode_base64(extracted_b64)
    output_file.write_text(decoded + "\n", encoding="utf-8")

    if flag in decoded:
        print(f"✅ Validation success: flag {flag} found")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded output", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
