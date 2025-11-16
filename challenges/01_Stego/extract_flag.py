#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# === Config ===
IMAGE_FILE = "squirrel.jpg"
OUTPUT_FILE = "decoded_message.txt"

# === Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

def pause_nonempty(msg="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    This stops students from just mashing ENTER through everything.
    """
    while True:
        answer = input(msg)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def spinner(message="Working", duration=2.0, interval=0.15):
    """
    Simple text spinner to give the feeling of work being done.
    """
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{message}... {frame}")
        sys.stdout.flush()
        time.sleep(interval)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

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
    print("💡 steghide can hide or extract secret data from files like images.")
    print("   Attackers use it to smuggle data; defenders use it to uncover it.\n")
    pause_nonempty("Type 'ready' when you're ready to see how we'll use steghide: ")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When you try a password, we'll run this command:\n")
    print(f"   steghide extract -sf {IMAGE_FILE} -xf {OUTPUT_FILE} -p [your password]\n")
    print("🔍 Command breakdown:")
    print("   steghide          → The steganography tool")
    print("   extract           → Mode: pull hidden data *out* of a file")
    print("   -sf squirrel.jpg  → 'stego file' (the image that might contain hidden data)")
    print("   -xf decoded_message.txt → Where to save any recovered secret message")
    print("   -p [your password]→ The password used to lock/unlock the hidden data")
    print("   -f                → Overwrite any existing output file without asking\n")
    pause_nonempty("Type 'go' when you're ready to start trying passwords: ")

    image_path = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    while True:
        pw = input("🔑 Enter a password to try (or type 'exit' to quit): ").strip()
        if not pw:
            print("⚠️ Please enter a password.\n")
            continue
        if pw.lower() == "exit":
            print("👋 Exiting. Good luck!")
            pause("Press ENTER to close this terminal...")
            break

        print(f"\n🔓 Trying password: {pw}")
        print(f"📦 Scanning {IMAGE_FILE} for hidden data...\n")

        spinner("Running steghide")

        if run_steghide(pw, image_path, output_path):
            print("🎉 ✅ SUCCESS! Hidden message recovered:\n")
            print("--------------- OUTPUT ---------------")
            with open(output_path, "r", errors="replace") as f:
                print(f.read().strip())
            print("--------------------------------------\n")
            print(f"📁 Saved as {OUTPUT_FILE}")
            print("💡 Look for a string like CCRI-AAAA-1111 to use as your flag.")
            pause("Press ENTER to close this terminal...")
            break
        else:
            print("❌ Incorrect password or no data found.")
            if os.path.exists(output_path):
                os.remove(output_path)
            print("🔁 Try another password.\n")

# === Entry Point ===
if __name__ == "__main__":
    main()
