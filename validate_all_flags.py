#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import shutil
from pathlib import Path

# === Paths ===
BASE_DIR = Path.cwd()
CHALLENGES_ROOT = BASE_DIR / "challenges"
CHALLENGES_JSON = BASE_DIR / "web_version_admin/challenges.json"
CHALLENGES_JSON_SOLO = BASE_DIR / "web_version_admin/challenges_solo.json"
UNLOCKS_GUIDED = BASE_DIR / "web_version_admin/validation_unlocks.json"
UNLOCKS_SOLO = BASE_DIR / "web_version_admin/validation_unlocks_solo.json"
VALIDATION_MODULES = BASE_DIR / "validation_helpers"
SANDBOX_ROOT = BASE_DIR / ".validation_sandbox"

# === Mapping: challenge_id -> validation_helpers/module.py ===
CHALLENGE_TO_MODULE = {
    "01_Stego": "stego",
    "02_Base64": "base64",
    "03_ROT13": "rot13",
    "04_Vigenere": "vigenere",
    "05_ArchivePassword": "archive_password",
    "06_Hashcat": "hashcat",
    "07_ExtractBinary": "extract_from_binary",
    "08_FakeAuthLog": "fake_auth_log",
    "09_FixScript": "fix_the_script",
    "10_Metadata": "metadata",
    "11_HiddenFlag": "hidden_flag",
    "12_QRCodes": "qr_codes",
    "13_HTTPHeaders": "http_headers",
    "14_SubdomainSweep": "subdomain_sweep",
    "15_ProcessInspection": "process_inspection",
    "16_Hex_Hunting": "hex_hunting",
    "17_Nmap_Scanning": "nmap_scanning",
    "18_Pcap_Search": "pcap_search"
}

def choose_mode():
    print("\n🎛️ Choose validation mode:")
    print("[1] Guided (default)")
    print("[2] Solo")
    choice = input("Enter choice [1/2]: ").strip()
    return "solo" if choice == "2" else "guided"

def load_challenges(mode):
    path = CHALLENGES_JSON_SOLO if mode == "solo" else CHALLENGES_JSON
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_unlock_data(mode):
    path = UNLOCKS_SOLO if mode == "solo" else UNLOCKS_GUIDED
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_sandbox(challenge_id, mode):
    """Copy challenge folder into a temp sandbox for validation."""
    folder_name = "challenges_solo" if mode == "solo" else "challenges"
    src = BASE_DIR / folder_name / challenge_id
    sandbox_dir = SANDBOX_ROOT / challenge_id

    if sandbox_dir.exists():
        shutil.rmtree(sandbox_dir)
    sandbox_dir.parent.mkdir(parents=True, exist_ok=True)

    if src.exists():
        shutil.copytree(src, sandbox_dir)
    else:
        print(f"⚠️ Challenge folder not found: {src}")

    return sandbox_dir

def run_validator(challenge_id, mode):
    module_name = CHALLENGE_TO_MODULE.get(challenge_id)
    if not module_name:
        print(f"⚠️  Skipped: No module mapping for {challenge_id}")
        return False

    script_path = VALIDATION_MODULES / f"{module_name}.py"
    print(f"\n🔍 Validating {challenge_id} using {script_path}...")

    if not script_path.exists():
        print(f"⚠️  Skipped: {script_path} not found.")
        return False

    # Setup sandbox
    sandbox = setup_sandbox(challenge_id, mode)
    env = os.environ.copy()
    env["CCRI_MODE"] = mode
    env["CCRI_SANDBOX"] = str(sandbox)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=VALIDATION_MODULES,
            env=env,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception running validator: {e}")
        return False

def main():
    print("🚦 CCRI STEMDay Master Validator\n" + "=" * 40)
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else choose_mode()

    if mode not in ("guided", "solo"):
        print("❌ Invalid mode. Use: validate_all_flags.py [guided|solo]")
        sys.exit(1)

    # Clean sandbox
    if SANDBOX_ROOT.exists():
        shutil.rmtree(SANDBOX_ROOT)
    SANDBOX_ROOT.mkdir()

    print(f"🛠️ Mode: {mode.upper()}")
    challenges = load_challenges(mode)

    success = 0
    fail = 0

    for challenge_id in challenges:
        if run_validator(challenge_id, mode):
            success += 1
        else:
            fail += 1

    print("\n📊 Validation Summary:")
    print(f"✅ {success} passed")
    print(f"❌ {fail} failed")
    if fail == 0:
        print("\n🎉 All challenges validated successfully!")
    else:
        print("\n🚨 Some challenges failed. Check messages above.")

if __name__ == "__main__":
    main()
