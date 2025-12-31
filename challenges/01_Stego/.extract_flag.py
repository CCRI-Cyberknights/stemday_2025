#!/usr/bin/env python3
import os
import subprocess
import sys

# === Import Core ===
# Add the root directory to sys.path to find exploration_core.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info

# === Config ===
IMAGE_FILE = "squirrel.jpg"
OUTPUT_FILE = "decoded_message.txt"

# === Utilities ===
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
        print_error("steghide is not installed.")
        return False

# === Main Interactive Loop ===
def main():
    # 1. Title Screen
    header("🕵️ Stego Decode Helper")
    
    print(f"🎯 Target image: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"🔍 Tool: {Colors.BOLD}steghide{Colors.END}\n")
    print("💡 steghide can hide or extract secret data from files like images.")
    print("   Attackers use it to smuggle data; defenders use it to uncover it.\n")
    
    require_input("Type 'ready' when you're ready to see how we'll use steghide: ", "ready")

    # 2. Explainer Screen
    header("🛠️ Behind the Scenes")
    print("When you try a password, we'll run this command:\n")
    print(f"   {Colors.GREEN}steghide extract -sf {IMAGE_FILE} -xf {OUTPUT_FILE} -p [your password]{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}steghide{Colors.END}          → The steganography tool")
    print(f"   {Colors.BOLD}extract{Colors.END}           → Mode: pull hidden data *out* of a file")
    print(f"   {Colors.BOLD}-sf {IMAGE_FILE}{Colors.END}  → 'stego file' (the image that might contain hidden data)")
    print(f"   {Colors.BOLD}-xf {OUTPUT_FILE}{Colors.END} → Where to save any recovered secret message")
    print(f"   {Colors.BOLD}-p [your password]{Colors.END}→ The password used to lock/unlock the hidden data")
    print(f"   {Colors.BOLD}-f{Colors.END}                → Overwrite any existing output file without asking\n")
    
    require_input("Type 'go' when you're ready to start trying passwords: ", "go")

    image_path = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    # 3. Main Logic Loop
    while True:
        # We manually construct the input to keep your exact phrasing
        pw = input(f"{Colors.YELLOW}🔑 Enter a password to try (or type 'exit' to quit): {Colors.END}").strip()
        
        if not pw:
            print_error("Please enter a password.")
            continue
            
        if pw.lower() == "exit":
            print(f"{Colors.CYAN}👋 Exiting. Good luck!{Colors.END}")
            pause("Press ENTER to close this terminal...")
            break

        print(f"\n🔓 Trying password: {Colors.BOLD}{pw}{Colors.END}")
        print(f"📦 Scanning {IMAGE_FILE} for hidden data...\n")

        spinner("Running steghide")

        if run_steghide(pw, image_path, output_path):
            print("\n" + "-" * 50)
            print_success("SUCCESS! Hidden message recovered:")
            print("-" * 50)
            print("--------------- OUTPUT ---------------")
            with open(output_path, "r", errors="replace") as f:
                print(f"{Colors.BOLD}{f.read().strip()}{Colors.END}")
            print("--------------------------------------\n")
            print(f"📁 Saved as {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
            print(f"{Colors.CYAN}💡 Look for a string like CCRI-AAAA-1111 to use as your flag.{Colors.END}")
            pause("Press ENTER to close this terminal...")
            break
        else:
            print_error("Incorrect password or no data found.")
            if os.path.exists(output_path):
                os.remove(output_path)
            print("🔁 Try another password.\n")

# === Entry Point ===
if __name__ == "__main__":
    main()