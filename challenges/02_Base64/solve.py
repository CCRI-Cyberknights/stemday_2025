#!/usr/bin/env python3
import os
import subprocess

# === Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

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
    clear_screen()
    print("📡 Intercepted Transmission Decoder")
    print("=====================================\n")
    print("📄 File to analyze: encoded.txt")
    print("🎯 Goal: Decode the intercepted transmission and locate the hidden CCRI flag.\n")
    print("💡 What is Base64?")
    print("   ➤ A text-based encoding scheme used to represent binary data as text.")
    print("   ➤ Common in email, HTTP, and digital certificates.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("This message was intercepted from a compromised Liber8 system.\n")
    print("We’ll use the built-in `base64` tool to decode it:\n")
    print("   base64 --decode encoded.txt\n")
    print("🔍 Command breakdown:")
    print("   base64         → Launch the decoder")
    print("   --decode       → Convert encoded text back to original form")
    print("   encoded.txt    → The file we captured\n")
    pause()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔍 Scanning for Base64 structure...")
    pause("Press ENTER to continue...\n")

    print("📄 Intercepted Base64 Message (encoded.txt):")
    print("---------------------------------------------")
    try:
        with open(input_file, "r", errors="replace") as f:
            print(f.read().strip())
    except FileNotFoundError:
        print("❌ ERROR: encoded.txt not found!")
        pause("Press ENTER to close this terminal...")
        return
    print("---------------------------------------------\n")
    print("🧠 This may look like nonsense, but it's a Base64-encoded message.")
    print("Let's decode it and reveal the original data!\n")
    pause("Press ENTER to decode the message...")

    print("⏳ Decoding intercepted transmission...\n")
    decoded = decode_base64(input_file, output_file)

    if not decoded:
        print("❌ Decoding failed!")
        print("📛 'encoded.txt' may be missing or corrupted.")
        print("💡 Double-check the file contents. They should look like random A-Z, a-z, 0-9, +, and / characters.\n")
        pause("Press ENTER to close this terminal...")
        return

    print("✅ Decoding complete!\n")
    print("📡 Decoded Transmission:")
    print("-----------------------------")
    print(decoded)
    print("-----------------------------\n")
    print(f"📁 Decoded message saved to: {output_file}")
    print("🔎 Look for a flag in this format: CCRI-XXXX-1234")
    print("🧠 Copy the flag into the scoreboard to complete this challenge.\n")
    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()
