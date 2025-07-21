#!/usr/bin/env python3
import os
import subprocess
import sys

# === Stego Decode Helper ===

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

def run_steghide(password, target_image, decoded_file):
    """Attempt to extract hidden data using steghide."""
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

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = os.path.join(script_dir, "squirrel.jpg")
    decoded_file = os.path.join(script_dir, "decoded_message.txt")

    if validation_mode:
        # 🛠 Validation: use the known correct password
        password_file = os.path.join(project_root, "web_version_admin", "validation_unlocks.json")
        try:
            import json
            with open(password_file, "r", encoding="utf-8") as f:
                unlocks = json.load(f)
            correct_password = unlocks["01_Stego"]["last_password"]
        except Exception as e:
            print(f"❌ ERROR: Could not load validation password: {e}", file=sys.stderr)
            sys.exit(1)

        if run_steghide(correct_password, target_image, decoded_file):
            print(f"✅ Validation success: extracted flag with password '{correct_password}'")
            sys.exit(0)
        else:
            print(f"❌ Validation failed: could not extract flag with password '{correct_password}'", file=sys.stderr)
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🕵️ Stego Decode Helper")
    print("==========================\n")
    print("🎯 Target image: squirrel.jpg")
    print("🔍 Tool: steghide\n")
    print("💡 What is steghide?")
    print("   ➡️ A Linux tool that can HIDE or EXTRACT secret data inside images or audio files.")
    print("   We'll use it to try and extract a hidden message from squirrel.jpg.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When we try a password, this command will run:\n")
    print("   steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]\n")
    print("🔑 Breakdown:")
    print("   -sf squirrel.jpg          → Stego file (the image to scan)")
    print("   -xf decoded_message.txt   → Extract to this file")
    print("   -p [password]             → Try this password for extraction\n")
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
        print(f"💻 Running: steghide extract -sf \"{target_image}\" -xf \"{decoded_file}\" -p \"{pw}\"\n")

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
            print("🔁 Try again with a different password.\n")
            if os.path.exists(decoded_file):
                os.remove(decoded_file)

if __name__ == "__main__":
    # Detect validation mode by environment variable
    validation_mode = os.getenv("CCRI_VALIDATE") == "1"
    main()
