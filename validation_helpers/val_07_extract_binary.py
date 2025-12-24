#!/usr/bin/env python3
import os
import sys
import subprocess
import re
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "07_ExtractBinary"
REGEX_PATTERN = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'

def run_strings(binary_path: Path, output_path: Path) -> bool:
    try:
        with output_path.open("w") as out_f:
            subprocess.run(["strings", str(binary_path)], stdout=out_f, check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.", file=sys.stderr)
        return False

def search_for_flags(file_path: Path, regex) -> list[str]:
    matches = []
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR during flag search: {e}", file=sys.stderr)
    return matches

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    unlock = load_unlock_data(root, challenge_id)
    expected_flag = unlock.get("real_flag")

    base_folder = "challenges_solo" if mode == "solo" else "challenges"
    binary_path = root / base_folder / challenge_id / "hidden_flag"
    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        extracted_path = Path(sandbox_override) / "extracted_strings.txt"
    else:
        extracted_path = root / base_folder / challenge_id / "extracted_strings.txt"


    if not binary_path.is_file():
        print(f"❌ ERROR: Binary file not found: {binary_path}", file=sys.stderr)
        return False

    if not run_strings(binary_path, extracted_path):
        return False

    matches = search_for_flags(extracted_path, REGEX_PATTERN)
    if expected_flag in matches:
        print(f"✅ Validation success: found flag {expected_flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in extracted strings.", file=sys.stderr)
        return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
