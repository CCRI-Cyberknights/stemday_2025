#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# === Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but do NOT allow empty input.
    This prevents 'enter enter enter' mashing through the whole script.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def spinner(message="Working", duration=2.5, interval=0.15):
    """
    Simple text spinner to fake 'work' being done.
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

def decode_base64(input_file, output_file):
    """Decode a Base64-encoded file and save the result."""
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

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    clear_screen()
    print("📡 Intercepted Transmission Decoder")
    print("=====================================\n")
    print("📄 File to analyze: encoded.txt")
    print("🎯 Goal: Decode the intercepted transmission and locate the hidden CCRI flag.\n")
    print("💡 What is Base64?")
    print("   ➤ A text-based encoding scheme used to represent binary data as text.")
    print("   ➤ Common in email, HTTP, and digital certificates.\n")

    pause_nonempty("Type 'ready' when you're ready to begin: ")

    clear_screen()
    print("🛠️ Analysis Tools")
    print("---------------------------")
    print("We intercepted a suspicious message from a compromised CryptKeepers system.\n")
    print("To decode it, we use the Linux `base64` command.\n")
    print("Here’s what the command looks like:\n")
    print("   base64 --decode encoded.txt\n")
    print("🔍 Command breakdown:")
    print("   base64         → The Base64 encoder/decoder tool")
    print("   --decode       → Converts encoded text back to the original data")
    print("   encoded.txt    → The file we recovered\n")

    pause_nonempty("Type 'continue' to inspect the encoded message: ")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔍 Inspecting intercepted data...\n")
    spinner("Reading file")

    print("📄 Intercepted Message (encoded.txt):")
    print("---------------------------------------------")
    try:
        with open(input_file, "r", errors="replace") as f:
            print(f.read().strip())
    except FileNotFoundError:
        print("❌ ERROR: encoded.txt not found!")
        pause_nonempty("Type anything, then press ENTER to exit...")
        return
    print("---------------------------------------------\n")
    print("🧠 At first glance, this looks like random characters.")
    print("But this structure strongly indicates Base64-encoded text.\n")
    print("Next step: decoding the message back into its original form using the Base64 tool.\n")
    print("Command to be executed:\n")
    print("   base64 --decode encoded.txt\n")

    pause_nonempty("Type 'decode' to begin processing the transmission: ")

    print("\n⏳ Processing intercepted transmission...")
    spinner("Decoding")

    decoded = decode_base64(input_file, output_file)

    if not decoded:
        print("\n❌ Decoding failed!")
        print("📛 'encoded.txt' may be missing or corrupted.")
        pause_nonempty("Type anything, then press ENTER to exit...")
        return

    print("\n✅ Transmission successfully decoded!\n")
    print("📄 Decoded Output:")
    print("-----------------------------")
    print(decoded)
    print("-----------------------------\n")
    print(f"📁 Output saved to: {output_file}")
    print("🔎 Look for a flag in this format: CCRI-AAAA-1111")
    print("🎯 Submit your flag in the scoreboard to complete this challenge.\n")

    input("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()
