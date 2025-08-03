#!/usr/bin/env python3
import os
import subprocess
import sys
import json

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "01_Stego"

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

# === Determine Guided or Solo Mode
def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    path = os.path.abspath(__file__)
    return "solo" if "challenges_solo" in path else "guided"

# === Load Unlock Password
def load_password():
    mode = get_ctf_mode()
    project_root = find_project_root()
    json_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["last_password"]
    except Exception as e:
        print(f"❌ ERROR: Could not load unlock password: {e}", file=sys.stderr)
        sys.exit(1)

# === Steghide Execution
def run_steghide(password, target_image, decoded_file):
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", target_image, "-xf", decoded_file, "-p", password, "-f"],
            input=b"\n",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0 and os.path.exists(decoded_file) and os.path.getsize(decoded_file) > 0
    except FileNotFoundError:
        print("❌ ERROR: steghide is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)

# === Utility
def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

# === Main Script
def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = os.path.join(script_dir, "squirrel.jpg")
    decoded_file = os.path.join(script_dir, "decoded_message.txt")

    if validation_mode:
        correct_password = load_password()
        if run_steghide(correct_password, target_image, decoded_file):
            print(f"✅ Validation success: extracted flag with password '{correct_password}'")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: could not extract flag with password '{correct_password}'", file=sys.stderr)
            sys.exit(1)

    # === Student Mode
    clear_screen()
    print("🕵️ Stego Decode Helper")
    print("==========================\n")
    print("🎯 Target image: squirrel.jpg")
    print("🔍 Tool: steghide\n")
    print("💡 What is steghide?")
    print("   ➡️ A Linux tool that can HIDE or EXTRACT secret data inside images or audio files.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When we try a password, this command will run:\n")
    print("   steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]\n")
    pause()

    while True:
        pw = input("🔑 Enter a password to try (or type 'exit' to quit): ").strip()

        if not pw:
            print("⚠️ You must enter something. Try again.\n")
            continue
        if pw.lower() == "exit":
            print("\n👋 Exiting... good luck on your next mission!")
            pause("Press ENTER to close this window...")
            sys.exit(0)

        print(f"\n🔓 Trying password: {pw}")
        print("📦 Scanning squirrel.jpg for hidden data...\n")

        if run_steghide(pw, target_image, decoded_file):
            print("🎉 ✅ SUCCESS! Hidden message recovered:")
            print("----------------------------")
            with open(decoded_file, "r") as f:
                print(f.read())
            print("----------------------------")
            print("📁 Saved as decoded_message.txt in this folder")
            print("💡 Look for a string like CCRI-ABCD-1234 to use as your flag.\n")
            pause("Press ENTER to close this terminal...")
            sys.exit(0)
        else:
            print("❌ Extraction failed. No hidden data or incorrect password.")
            if os.path.exists(decoded_file):
                os.remove(decoded_file)
            print("🔁 Try again.\n")

if __name__ == "__main__":
    main()
