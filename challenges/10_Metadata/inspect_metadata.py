#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "10_Metadata"

# === Validation Mode Detection
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

# === Utilities
def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    unlock_path = os.path.join(
        project_root,
        "web_version_admin",
        SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON
    )
    try:
        with open(unlock_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
        sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

# === Main Logic
def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = os.path.join(script_dir, "capybara.jpg")
    output_file = os.path.join(script_dir, "metadata_dump.txt")

    if validation_mode:
        expected_flag = load_expected_flag(project_root)

        try:
            result = subprocess.run(
                ["exiftool", target_image],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            if expected_flag in result.stdout:
                print(f"✅ Validation success: found flag {expected_flag}")
                sys.exit(0)
            else:
                print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
                sys.exit(1)
        except subprocess.CalledProcessError:
            print("❌ ERROR: exiftool failed to run.", file=sys.stderr)
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("📸 Metadata Inspection Tool")
    print("============================\n")
    print(f"🎯 Target image: {os.path.basename(target_image)}")
    print("🔧 Tool in use: exiftool\n")
    print("💡 Why exiftool?")
    print("   ➡️ Images often carry *hidden metadata* like camera info, GPS tags, or embedded comments.")
    print("   ➡️ This data can hide secrets — including CTF flags!\n")

    if not os.path.isfile(target_image):
        print(f"❌ ERROR: {os.path.basename(target_image)} not found in this folder!")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print(f"📂 Inspecting: {os.path.basename(target_image)}")
    print(f"📄 Saving metadata to: {os.path.basename(output_file)}\n")
    pause("Press ENTER to run exiftool and extract metadata...")

    print(f"\n🛠️ Running: exiftool {os.path.basename(target_image)} > {os.path.basename(output_file)}\n")
    time.sleep(0.5)
    try:
        with open(output_file, "w") as out_f:
            subprocess.run(
                ["exiftool", target_image],
                stdout=out_f,
                stderr=subprocess.DEVNULL,
                check=True
            )
    except subprocess.CalledProcessError:
        print("❌ ERROR: exiftool failed to run.")
        sys.exit(1)

    print(f"✅ All metadata saved to: {os.path.basename(output_file)}\n")

    print("👀 Let’s preview a few key fields:")
    print("----------------------------------------")
    try:
        subprocess.run(
            ["grep", "-E", "Camera|Date|Comment|Artist|CCRI", output_file],
            check=False
        )
    except FileNotFoundError:
        print("⚠️ No common fields found.")
    print("----------------------------------------\n")

    keyword = input("🔎 Enter a keyword to search in the metadata (or press ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {os.path.basename(output_file)}...")
        subprocess.run(
            ["grep", "-i", "--color=always", keyword, output_file],
            check=False
        )
    else:
        print("⏭️  Skipping custom search.")

    print("\n🧠 One of these fields hides the correct flag in the format: CCRI-AAAA-1111")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
