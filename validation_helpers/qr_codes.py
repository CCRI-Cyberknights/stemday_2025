#!/usr/bin/env python3
import os
import sys
import json
import subprocess

CHALLENGE_ID = "12_QRCodes"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    path = os.path.join(
        project_root,
        "web_version_admin",
        "validation_unlocks_solo.json" if get_ctf_mode() == "solo" else "validation_unlocks.json"
    )
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR loading flag: {e}", file=sys.stderr)
        sys.exit(1)

def decode_qr(file_path):
    try:
        result = subprocess.run(
            ["zbarimg", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: zbarimg is not installed.", file=sys.stderr)
        sys.exit(1)

def main():
    project_root = find_project_root()
    challenge_dir = os.path.join(project_root, "challenges", CHALLENGE_ID)
    qr_codes = [os.path.join(challenge_dir, f"qr_0{i}.png") for i in range(1, 6)]
    expected_flag = load_expected_flag(project_root)

    for qr in qr_codes:
        if not os.path.exists(qr):
            print(f"❌ ERROR: QR image missing: {qr}", file=sys.stderr)
            sys.exit(1)
        decoded = decode_qr(qr)
        if expected_flag in decoded:
            print(f"✅ Found flag {expected_flag} in {os.path.basename(qr)}")
            sys.exit(0)

    print(f"❌ Flag {expected_flag} not found in any QR code.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
