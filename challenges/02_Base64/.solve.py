#!/usr/bin/env python3
import os
import subprocess
import sys

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info

# === Config ===
INPUT_FILE = "encoded.txt"
OUTPUT_FILE = "decoded_output.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def decode_base64(input_path, output_path):
    """Decode a Base64-encoded file and save the result."""
    try:
        result = subprocess.run(
            ["base64", "--decode", input_path],
            capture_output=True,
            text=True,
            check=True
        )
        decoded = result.stdout.strip()
        if decoded:
            with open(output_path, "w") as f:
                f.write(decoded + "\n")
        return decoded
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None

# === Main Flow ===
def main():
    # 1. Mission Briefing
    header("📡 Intercepted Transmission Decoder")
    
    print(f"📄 File to analyze: {Colors.BOLD}{INPUT_FILE}{Colors.END}")
    print("🎯 Goal: Decode the intercepted transmission and locate the hidden CCRI flag.\n")
    print(f"{Colors.CYAN}💡 What is Base64?{Colors.END}")
    print("   ➤ A text-based encoding scheme used to represent binary data as text.")
    print("   ➤ Common in email, HTTP, and digital certificates.\n")

    require_input("Type 'ready' when you're ready to begin: ", "ready")

    # 2. Tool Explanation
    header("🛠️ Analysis Tools")
    print("We intercepted a suspicious message from a compromised CryptKeepers system.\n")
    print(f"To decode it, we use the Linux {Colors.BOLD}base64{Colors.END} command.\n")
    print("Here’s what the command looks like:\n")
    print(f"   {Colors.GREEN}base64 --decode {INPUT_FILE}{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}base64{Colors.END}         → The Base64 encoder/decoder tool")
    print(f"   {Colors.BOLD}--decode{Colors.END}       → Converts encoded text back to the original data")
    print(f"   {Colors.BOLD}{INPUT_FILE}{Colors.END}    → The file we recovered\n")

    require_input("Type 'view' to inspect the encoded message: ", "view")

    input_path = get_path(INPUT_FILE)
    output_path = get_path(OUTPUT_FILE)

    # 3. File Inspection
    header("🔍 Inspecting intercepted data")
    spinner("Reading file")
    print("\n")

    print(f"📄 Intercepted Message ({INPUT_FILE}):")
    print("-" * 50)
    try:
        with open(input_path, "r", errors="replace") as f:
            print(f"{Colors.YELLOW}{f.read().strip()}{Colors.END}")
    except FileNotFoundError:
        print_error(f"{INPUT_FILE} not found!")
        pause()
        return
    print("-" * 50 + "\n")
    
    print("🧠 At first glance, this looks like random characters.")
    print("But this structure strongly indicates Base64-encoded text.\n")
    print("Next step: decoding the message back into its original form using the Base64 tool.\n")
    print("Command to be executed:\n")
    print(f"   {Colors.GREEN}base64 --decode {INPUT_FILE}{Colors.END}\n")

    require_input("Type 'decode' to begin processing the transmission: ", "decode")

    # 4. Decoding Execution
    print("\n⏳ Processing intercepted transmission...")
    spinner("Decoding")

    decoded = decode_base64(input_path, output_path)

    if not decoded:
        print("\n")
        print_error("Decoding failed!")
        print_info(f"'{INPUT_FILE}' may be missing or corrupted.")
        pause()
        return

    # 5. Success Screen
    print("\n")
    print_success("Transmission successfully decoded!\n")
    print("📄 Decoded Output:")
    print("-" * 50)
    print(f"{Colors.BOLD}{decoded}{Colors.END}")
    print("-" * 50 + "\n")
    print(f"📁 Output saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
    print(f"{Colors.CYAN}🔎 Look for a flag in this format: CCRI-AAAA-1111{Colors.END}")
    print("🎯 Submit your flag in the scoreboard to complete this challenge.\n")

    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()