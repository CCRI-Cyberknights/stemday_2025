#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "12_QRCodes"

def decode_qr(file_path: Path) -> str:
    try:
        result = subprocess.run(
            ["zbarimg", str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: zbarimg is not installed.", file=sys.stderr)
        sys.exit(1)

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = data["real_flag"]
    challenge_dir = root / "challenges" / CHALLENGE_ID
    qr_codes = [challenge_dir / f"qr_0{i}.png" for i in range(1, 6)]

    for qr in qr_codes:
        if not qr.exists():
            print(f"❌ ERROR: QR image missing: {qr}", file=sys.stderr)
            sys.exit(1)
        decoded = decode_qr(qr)
        if expected_flag in decoded:
            print(f"✅ Found flag {expected_flag} in {qr.name}")
            sys.exit(0)

    print(f"❌ Flag {expected_flag} not found in any QR code.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
