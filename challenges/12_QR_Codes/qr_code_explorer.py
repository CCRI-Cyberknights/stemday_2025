#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "12_QRCodes"

# === Detect validation mode
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
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag(project_root):
    mode = get_ctf_mode()
    unlock_path = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)
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

def open_image(file_path, duration=20):
    try:
        viewer_process = subprocess.Popen(
            ["xdg-open", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(duration)
        viewer_process.terminate()
        print("⏳ Time’s up! Closing the viewer...")
    except Exception as e:
        print(f"❌ Could not open image: {e}")

def decode_qr(file_path):
    try:
        result = subprocess.run(
            ["zbarimg", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: zbarimg is not installed.")
        sys.exit(1)

def validate_all_qrs(qr_codes, expected_flag):
    print("🔍 Validation: scanning all QR codes for the expected flag...")
    for qr in qr_codes:
        decoded = decode_qr(qr)
        if expected_flag in decoded:
            print(f"✅ Validation success: found flag {expected_flag} in {os.path.basename(qr)}")
            return True
    print(f"❌ Validation failed: flag {expected_flag} not found in any QR code.", file=sys.stderr)
    return False

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    qr_codes = [os.path.join(script_dir, f"qr_0{i}.png") for i in range(1, 6)]

    if validation_mode:
        expected_flag = load_expected_flag(project_root)
        sys.exit(0 if validate_all_qrs(qr_codes, expected_flag) else 1)

    # === Student Interactive Mode ===
    clear_screen()
    print("📦 QR Code Explorer")
    print("==========================\n")
    print("🎯 Mission Briefing:")
    print("----------------------------")
    print("🔍 You’ve recovered 5 mysterious QR codes from a digital drop site.")
    print("Each one may contain:")
    print("  • A secret message")
    print("  • A fake flag")
    print("  • Or… the **real flag** in CCRI-AAAA-1111 format!\n")
    print("🛠️ Your options:")
    print("  • Scan with your phone’s QR scanner")
    print("  • OR use this tool to open and auto-decode them\n")
    print("📖 Behind the scenes:")
    print("   This script runs:")
    print("      zbarimg qr_XX.png")
    print("   → zbarimg scans and decodes barcodes/QR codes from images.\n")
    print("⏳ Each QR image will open in the viewer for **20 seconds**.")
    print("   After that, the decoded result (if any) is saved to a text file.\n")
    pause("Press ENTER to begin exploring.")
    clear_screen()

    while True:
        print("🗂️  Available QR codes:")
        for i, qr in enumerate(qr_codes, 1):
            print(f"{i}. {os.path.basename(qr)}")
        print("6. Exit Explorer\n")

        choice = input("Select a QR code to view and decode (1-5), or 6 to exit: ").strip()

        if choice == "6":
            print("\n👋 Exiting QR Code Explorer. Don’t forget to submit the correct flag!")
            break

        try:
            index = int(choice) - 1
            if 0 <= index < len(qr_codes):
                file_path = qr_codes[index]
                txt_file = file_path.replace(".png", ".txt")

                print(f"\n🖼️ Opening {os.path.basename(file_path)} in image viewer for 20 seconds...")
                open_image(file_path)

                print(f"\n🔎 Scanning QR code in {os.path.basename(file_path)}...")
                print(f"💻 Running: zbarimg \"{os.path.basename(file_path)}\"\n")

                result = decode_qr(file_path)

                if not result:
                    print("❌ No QR code found or unable to decode.")
                else:
                    print("✅ Decoded result:")
                    print("----------------------------")
                    print(result)
                    print("----------------------------")
                    with open(txt_file, "w") as f:
                        f.write(result + "\n")
                    print(f"💾 Saved to: {os.path.basename(txt_file)}")

                pause("\nPress ENTER to return to QR list...")
                clear_screen()
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 6.")
                pause()
                clear_screen()
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
