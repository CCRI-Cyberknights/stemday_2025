#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

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
        return ""

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    challenge_dir = root / base_path / challenge_id
    qr_codes = [challenge_dir / f"qr_0{i}.png" for i in range(1, 6)]

    for qr in qr_codes:
        if not qr.exists():
            print(f"❌ ERROR: QR image missing: {qr}", file=sys.stderr)
            return False
        decoded = decode_qr(qr)
        if expected_flag in decoded:
            print(f"✅ Found flag {expected_flag} in {qr.name}")
            return True

    print(f"❌ Flag {expected_flag} not found in any QR code.", file=sys.stderr)
    return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
