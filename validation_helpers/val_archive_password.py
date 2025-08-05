#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

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

def validate(mode="guided", challenge_id="05_ArchivePassword") -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")
    zip_password = data.get("last_zip_password")

    base_folder = "challenges_solo" if mode == "solo" else "challenges"
    sandbox_override = os.environ.get("CCRI_SANDBOX")
    
    if sandbox_override:
        challenge_dir = Path(sandbox_override)
        real_challenge_dir = root / base_folder / challenge_id
        if not challenge_dir.exists():
            print(f"🧪 Copying challenge files into sandbox: {challenge_dir}")
            shutil.copytree(real_challenge_dir, challenge_dir)
    else:
        challenge_dir = root / base_folder / challenge_id

    zip_path = challenge_dir / "secret.zip"
    extract_dir = challenge_dir
    extracted_b64 = extract_dir / "message_encoded.txt"

    if not zip_path.exists():
        print(f"❌ Zip file missing: {zip_path}", file=sys.stderr)
        return False

    if not unzip_with_password(zip_path, zip_password, extract_dir):
        return False

    if not extracted_b64.exists():
        print(f"❌ Extracted file missing: {extracted_b64}", file=sys.stderr)
        return False

    decoded = decode_base64(extracted_b64)
    if decoded is None:
        return False

    # Only write output in the sandbox, for debugging or verification
    if sandbox_override:
        output_file = Path(sandbox_override) / "decoded_output.txt"
        output_file.write_text(decoded + "\n", encoding="utf-8")

    if flag in decoded:
        print(f"✅ Validation success: flag {flag} found")
        return True
    else:
        print(f"❌ Validation failed: flag {flag} not found in decoded output", file=sys.stderr)
        return False

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
