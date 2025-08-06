#!/usr/bin/env python3
import os
import subprocess

# === Config ===
IMAGE_FILE = "squirrel.jpg"
OUTPUT_FILE = "decoded_message.txt"

# === Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def run_steghide(password, image_path, output_path):
    """Attempt to extract hidden file using steghide and given password."""
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", image_path, "-xf", output_path, "-p", password, "-f"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except FileNotFoundError:
        print("❌ ERROR: steghide is not installed.")
        return False

# === Main Interactive Loop ===
def main():
    clear_screen()
    print("🕵️ Stego Decode Helper")
    print("==========================\n")
    print(f"🎯 Target image: {IMAGE_FILE}")
    print("🔍 Tool: steghide\n")
    print("💡 steghide can hide or extract secret data from files like images.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When you try a password, we'll run this command:\n")
    print(f"   steghide extract -sf {IMAGE_FILE} -xf {OUTPUT_FILE} -p [your password]\n")
    pause()

    image_path = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    while True:
        pw = input("🔑 Enter a password to try (or type 'exit' to quit): ").strip()
        if not pw:
            print("⚠️ Please enter a password.\n")
            continue
        if pw.lower() == "exit":
            print("👋 Exiting. Good luck!")
            pause()
            break

        print(f"\n🔓 Trying password: {pw}")
        print(f"📦 Scanning {IMAGE_FILE}...\n")

        if run_steghide(pw, image_path, output_path):
            print("🎉 ✅ SUCCESS! Hidden message recovered:\n")
            print("--------------- OUTPUT ---------------")
            with open(output_path, "r", errors="replace") as f:
                print(f.read().strip())
            print("--------------------------------------\n")
            print(f"📁 Saved as {OUTPUT_FILE}")
            print("💡 Look for a string like CCRI-XXXX-#### to use as your flag.")
            pause()
            break
        else:
            print("❌ Incorrect password or no data found.")
            if os.path.exists(output_path):
                os.remove(output_path)
            print("🔁 Try again.\n")

# === Entry Point ===
if __name__ == "__main__":
    main()
