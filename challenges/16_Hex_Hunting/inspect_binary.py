#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time
import re

# === Hex Flag Hunter Helper ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def scanning_animation():
    if not validation_mode:
        print("\n🔎 Scanning binary for flag-like patterns", end="", flush=True)
        for _ in range(5):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print()

def search_flags(binary_file, pattern=r"CCRI-[A-Z]{4}-[0-9]{4}"):
    """
    Scan the binary file using strings and regex for flag-like patterns.
    """
    try:
        strings_output = subprocess.run(
            ["strings", binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if strings_output.returncode != 0:
            return []
        flags = []
        for line in strings_output.stdout.strip().splitlines():
            if re.match(pattern, line.strip()):
                flags.append(line.strip())
        return flags
    except Exception as e:
        print(f"❌ Error while scanning binary: {e}")
        sys.exit(1)

def validate_flag_in_binary(binary_file, expected_flag):
    print("🔍 Validation: scanning hex_flag.bin for expected flag...")
    flags = search_flags(binary_file)
    if expected_flag in flags:
        print(f"✅ Validation success: found flag {expected_flag}")
        return True

    # Fallback: raw byte search
    try:
        with open(binary_file, "rb") as f:
            data = f.read()
            if expected_flag.encode("utf-8") in data:
                print(f"✅ Validation fallback: found flag {expected_flag} in raw bytes")
                return True
    except Exception as e:
        print(f"❌ Error during fallback search: {e}", file=sys.stderr)

    print(f"❌ Validation failed: flag {expected_flag} not found", file=sys.stderr)
    return False

# [rest of the script unchanged...]
