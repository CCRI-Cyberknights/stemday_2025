#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time
import re
from pathlib import Path

# === Hex Flag Hunter Helper ===

CHALLENGE_ID = "16_Hex_Hunting"
FLAG_PATTERN = r"CCRI-[A-Z]{4}-[0-9]{4}"
BINARY_FILE = "hex_flag.bin"
NOTES_FILE = "notes.txt"
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in str(Path(__file__).resolve()) else "guided"

def load_expected_flag():
    project_root = find_project_root()
    mode = get_ctf_mode()
    unlock_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load {os.path.basename(unlock_path)}: {e}", file=sys.stderr)
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

def search_flags(binary_file, pattern=FLAG_PATTERN):
    try:
        strings_output = subprocess.run(
            ["strings", binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if strings_output.returncode != 0:
            return []
        return [line.strip() for line in strings_output.stdout.splitlines() if re.match(pattern, line.strip())]
    except Exception as e:
        print(f"❌ Error while scanning binary: {e}")
        sys.exit(1)

def find_offset(binary_file, target_string):
    try:
        result = subprocess.run(
            ["grep", "-abo", target_string, binary_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in result.stdout.strip().splitlines():
            return int(line.split(":")[0])
    except:
        return None

def show_hex_context(binary_file, offset, context=64):
    start = max(0, offset - 16)
    try:
        dd = subprocess.Popen(
            ["dd", f"if={binary_file}", "bs=1", f"skip={start}", f"count={context}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        xxd = subprocess.Popen(["xxd"], stdin=dd.stdout)
        dd.stdout.close()
        xxd.wait()
    except Exception as e:
        print(f"❌ Could not show hex context: {e}")

def validate_flag_in_binary(binary_file, expected_flag):
    print("🔍 Validation: scanning hex_flag.bin for expected flag...")
    flags = search_flags(binary_file)
    if expected_flag in flags:
        print(f"✅ Validation success: found flag {expected_flag}")
        return True
    try:
        with open(binary_file, "rb") as f:
            if expected_flag.encode("utf-8") in f.read():
                print(f"✅ Validation fallback: found flag {expected_flag} in raw bytes")
                return True
    except Exception as e:
        print(f"❌ Error during fallback search: {e}", file=sys.stderr)

    print(f"❌ Validation failed: flag {expected_flag} not found", file=sys.stderr)
    return False

def main():
    clear_screen()
    print("🔍 Hex Flag Hunter")
    print("============================\n")
    print("🎯 Target binary:", BINARY_FILE)
    print("💡 Goal: Locate the real flag (format: CCRI-XXXX-1234).")
    print("⚠️  Multiple candidate flags are embedded, but only ONE is correct!\n")

    if not os.path.exists(BINARY_FILE):
        print(f"❌ Cannot find {BINARY_FILE}")
        sys.exit(1)

    if validation_mode:
        expected_flag = load_expected_flag()
        sys.exit(0 if validate_flag_in_binary(BINARY_FILE, expected_flag) else 1)

    pause("Press ENTER to begin scanning...")
    scanning_animation()
    flags = search_flags(BINARY_FILE)

    if not flags:
        print("❌ No flag-like patterns found in binary.")
        sys.exit(1)

    print(f"\n✅ Found {len(flags)} candidate flag(s):\n")
    for i, flag in enumerate(flags):
        print(f"  [{i+1}] {flag}")
    print()

    for i, flag in enumerate(flags):
        print("-------------------------------------------------")
        print(f"[{i+1}/{len(flags)}] Candidate Flag: {flag}")
        offset = find_offset(BINARY_FILE, flag)
        if offset is not None:
            print(f"📍 Approximate byte offset: {offset}")
            print("📖 Hex context (around flag):")
            show_hex_context(BINARY_FILE, offset)
        else:
            print("⚠️ Could not find offset for this flag.")

        while True:
            print("\nOptions:")
            print("1) ✅ Mark this flag as POSSIBLE and save to notes.txt")
            print("2) ➡️ Skip to next flag")
            print("3) 🚪 Quit investigation")
            choice = input("Choose an option (1-3): ").strip()
            if choice == "1":
                with open(NOTES_FILE, "a") as f:
                    f.write(flag + "\n")
                print(f"✅ Saved '{flag}' to {NOTES_FILE}")
                time.sleep(0.5)
                break
            elif choice == "2":
                print("➡️ Skipping to next candidate...\n")
                time.sleep(0.5)
                break
            elif choice == "3":
                print("👋 Exiting investigation early.")
                print(f"📁 All saved candidate flags are in {NOTES_FILE}")
                sys.exit(0)
            else:
                print("⚠️ Invalid choice. Please enter 1, 2, or 3.")

    print("\n🎉 Investigation complete!")
    print(f"📁 All saved candidate flags are in {NOTES_FILE}")
    pause()

if __name__ == "__main__":
    main()
