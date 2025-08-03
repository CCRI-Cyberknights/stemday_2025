#!/usr/bin/env python3
import os
import subprocess
import sys
import json

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "02_Base64"

# === Detect Validation Mode
validation_mode = os.environ.get("CCRI_VALIDATE") == "1"

# === Project Root Detection
def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

# === Detect Mode
def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

# === Load Flag
def load_expected_flag():
    project_root = find_project_root()
    mode = get_ctf_mode()
    json_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation flag: {e}", file=sys.stderr)
        sys.exit(1)

# === Base64 Decode Logic
def decode_base64(input_file, output_file):
    try:
        result = subprocess.run(
            ["base64", "--decode", input_file],
            capture_output=True,
            text=True,
            check=True
        )
        decoded = result.stdout.strip()
        if decoded:
            with open(output_file, "w") as f:
                f.write(decoded + "\n")
        return decoded
    except subprocess.CalledProcessError:
        return None

# === Utility
def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

# === Main Logic
def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    input_file = os.path.join(script_dir, "encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    if validation_mode:
        expected_flag = load_expected_flag()
        decoded = decode_base64(input_file, output_file)
        if decoded and expected_flag in decoded:
            print(f"✅ Validation success: found flag {expected_flag}")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found in decoded content", file=sys.stderr)
            sys.exit(1)

    # === Student Mode ===
    clear_screen()
    print("📡 Intercepted Transmission Decoder")
    print("=====================================\n")
    print("📄 File to analyze: encoded.txt")
    print("🎯 Goal: Decode the intercepted transmission and locate the hidden CCRI flag.\n")
    print("💡 What is Base64?")
    print("   ➡️ A text-based encoding scheme that transforms binary data into readable text.")
    print("   ➡️ Commonly used for encoding transmissions so they aren’t corrupted over text-only channels.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("This message was captured from a compromised Liber8 system.\n")
    print("It’s been Base64-encoded for secure transit. To recover it, we’ll use the Linux tool `base64`:\n")
    print("   base64 --decode encoded.txt\n")
    print("🔑 Breakdown:")
    print("   base64         → Call the Base64 tool")
    print("   --decode       → Switch from encoding to decoding")
    print("   encoded.txt    → Input file to decode\n")
    pause()

    print("\n🔍 Scanning file for Base64 structure...")
    pause("Press ENTER to continue decoding...")
    print("✅ Base64 structure confirmed!\n")
    print("⏳ Decoding intercepted transmission...\n")

    decoded = decode_base64(input_file, output_file)

    if not decoded:
        print("\n❌ Decoding failed! This may not be valid Base64, or the file is corrupted.")
        print("💡 Tip: Ensure 'encoded.txt' exists and contains proper Base64 text.\n")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print("\n📡 Decoded Transmission:")
    print("-----------------------------")
    print(decoded)
    print("-----------------------------")
    print(f"\n📁 Decoded output saved as: {output_file}")
    print("🔎 Search carefully for the CCRI flag format: CCRI-AAAA-1111")
    print("🧠 This is your flag. Copy it into the scoreboard!\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
