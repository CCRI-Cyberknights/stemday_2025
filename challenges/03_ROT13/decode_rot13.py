#!/usr/bin/env python3
import os
import sys
import time
import json
from pathlib import Path

# === Imports for ROT13 logic ===
dir_path = Path(__file__).resolve().parent
for parent in [dir_path] + list(dir_path.parents):
    if (parent / ".ccri_ctf_root").exists():
        sys.path.insert(0, str(parent))
        break
else:
    print("❌ ERROR: Could not find project root (.ccri_ctf_root)", file=sys.stderr)
    sys.exit(1)

from flag_generators.gen_03_rot13 import ROT13FlagGenerator  # ✅ Animation + rot13 logic

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "03_ROT13"

# === Validation Mode Detection
validation_mode = os.environ.get("CCRI_VALIDATE") == "1"

# === Project Root Detection
def find_project_root():
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".ccri_ctf_root").exists():
            return current
        current = current.parent
    print("❌ ERROR: Could not find .ccri_ctf_root marker.", file=sys.stderr)
    sys.exit(1)

# === Determine Guided or Solo Mode
def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in str(Path(__file__).resolve()) else "guided"

# === Load Flag from JSON
def load_expected_flag():
    project_root = find_project_root()
    json_file = SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON
    path = project_root / "web_version_admin" / json_file
    try:
        with open(path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation flag: {e}", file=sys.stderr)
        sys.exit(1)

# === Utilities
def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

# === Main Logic
def main():
    script_dir = Path(__file__).resolve().parent
    cipher_file = script_dir / "cipher.txt"
    output_file = script_dir / "decoded_output.txt"

    if validation_mode:
        expected_flag = load_expected_flag()

        try:
            with open(cipher_file, "r") as f:
                encoded_lines = f.readlines()
            decoded_message = "".join([ROT13FlagGenerator.rot13(line) for line in encoded_lines])
        except Exception as e:
            print(f"❌ ERROR reading or decoding cipher.txt: {e}", file=sys.stderr)
            sys.exit(1)

        with open(output_file, "w") as f_out:
            f_out.write(decoded_message + "\n")

        if expected_flag in decoded_message:
            print(f"✅ Validation success: found flag {expected_flag}")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found in decoded content", file=sys.stderr)
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🔐 ROT13 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: cipher.txt")
    print("🎯 Goal: Decode this message and find the hidden CCRI flag.\n")
    print("💡 What is ROT13?")
    print("   ➡️ A simple Caesar cipher that shifts each letter 13 places in the alphabet.")
    print("   ➡️ Encoding and decoding use the same operation because 13+13=26 (a full loop!).\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We’ll use a Python helper to process each line:\n")
    print("   For every line in cipher.txt:")
    print("     ➡️ Rotate each letter forward by 13 places (A→N, N→A).\n")
    print("💻 The Python decoder also animates this process so you can watch it work.\n")
    pause("Press ENTER to launch the animated decoder...")

    if not cipher_file.is_file() or cipher_file.stat().st_size == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    with open(cipher_file, "r") as f:
        encoded_lines = f.readlines()

    clear_screen()
    print("🔓 Decoding intercepted message...\n")

    ROT13FlagGenerator.animate_rot13_line_by_line(encoded_lines, delay=0.05)

    decoded_message = "".join([ROT13FlagGenerator.rot13(line) for line in encoded_lines])
    with open(output_file, "w") as f_out:
        f_out.write(decoded_message + "\n")

    print("\n✅ Final Decoded Message saved to:")
    print(f"   📁 {output_file}\n")
    print("🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111")
    print("📋 Copy the correct flag and paste it into the scoreboard when ready.\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
