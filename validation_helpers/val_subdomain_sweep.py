#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "14_SubdomainSweep"

def validate_subdomains(domains, challenge_dir: Path, expected_flag: str) -> bool:
    for domain in domains:
        file_path = challenge_dir / f"{domain}.liber8.local.html"
        if not file_path.is_file():
            print(f"❌ Missing file: {file_path}", file=sys.stderr)
            continue
        try:
            if expected_flag in file_path.read_text(encoding="utf-8", errors="ignore"):
                print(f"✅ Found flag {expected_flag} in {file_path.name}")
                return True
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}", file=sys.stderr)

    print(f"❌ Flag {expected_flag} not found in any subdomain file.", file=sys.stderr)
    return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    unlock = load_unlock_data(root, challenge_id)
    expected_flag = unlock.get("real_flag")
    if not expected_flag:
        print("❌ ERROR: Flag not present in unlock data", file=sys.stderr)
        return False

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    
    # 🧪 Sandbox override
    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        challenge_dir = Path(sandbox_override)
    else:
        challenge_dir = root / base_path / challenge_id

    domains = ["alpha", "beta", "gamma", "delta", "omega"]
    return validate_subdomains(domains, challenge_dir, expected_flag)

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
