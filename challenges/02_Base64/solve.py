#!/usr/bin/env python3
import os
import subprocess
import sys

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

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

def main():
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

    script_dir = os.path.abspath(os.path.dirname(__file__))
    input_file = os.path.join(script_dir, "encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

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
