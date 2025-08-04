#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import re
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "07_ExtractBinary"
REGEX_PATTERN = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'

def run_strings(binary_path: Path, output_path: Path):
    try:
        with output_path.open("w") as out_f:
            subprocess.run(["strings", str(binary_path)], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.", file=sys.stderr)
        sys.exit(1)

def search_for_flags(file_path: Path, regex):
    matches = []
    try:
        with file_path.open("r") as f:
            for line in f:
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR during flag search: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

def main():
    root = find_project_root()
    mode = os.environ.get("CCRI_MODE", "guided")
    unlock = load_unlock_data(root, CHALLENGE_ID)
    expected_flag = unlock.get("real_flag")

    binary_relpath = f"challenges/{CHALLENGE_ID}/hidden_flag" if mode == "guided" else f"challenges_solo/{CHALLENGE_ID}/hidden_flag"
    binary_path = root / binary_relpath
    extracted_path = Path(__file__).resolve().parent / "extracted_strings.txt"

    if not binary_path.is_file():
        print(f"❌ ERROR: Binary file not found: {binary_path}", file=sys.stderr)
        return 1

    run_strings(binary_path, extracted_path)
    matches = search_for_flags(extracted_path, REGEX_PATTERN)

    if expected_flag in matches:
        print(f"✅ Validation success: found flag {expected_flag}")
        return 0
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found in extracted strings.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
