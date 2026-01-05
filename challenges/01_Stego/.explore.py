#!/usr/bin/env python3
import os
import subprocess
import sys

# === Import Core ===
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
        # Check if file exists and has content
        return result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except FileNotFoundError:
        print_error("steghide is not installed.")
        return False

# === Main Interactive Loop ===
def main():
    # 1. Title Screen
    header("🕵️ Stego Decode Helper")
    
    print(f"🎯 Target: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"🔍 Tool: {Colors.BOLD}steghide{Colors.END}\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ The target file is locked with a passphrase.")
    print("   ➤ Rumor has it the user used the \"most common password in the world.\"")
    print("   ➤ Your goal: Guess the password to unlock the file.\n")
    
    require_input("Type 'ready' when you are ready to start the extraction tool: ", "ready")

    # 2. Explainer Screen
    header("🛠️ Behind the Scenes")
    print("When you enter a password, this script runs the following Linux command:\n")
    print(f"   {Colors.GREEN}steghide extract -sf {IMAGE_FILE} -xf {OUTPUT_FILE} -p [PASSWORD]{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}steghide{Colors.END}          → The steganography tool")
    print(f"   {Colors.BOLD}extract{Colors.END}           → The action (pull data OUT)")
    print(f"   {Colors.BOLD}-sf {IMAGE_FILE}{Colors.END}  → Source File (the image)")
    print(f"   {Colors.BOLD}-xf {OUTPUT_FILE}{Colors.END} → Extract File (where to save the result)")
    print(f"   {Colors.BOLD}-p [PASSWORD]{Colors.END}     → The key to unlock the data\n")
    
    require_input("Type 'go' when you are ready to guess the password: ", "go")

    image_path = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    # 3. Main Logic Loop
    while True:
        pw = input(f"{Colors.YELLOW}🔑 Enter a password guess (or 'exit'): {Colors.END}").strip()
        
        if not pw:
            continue
            
        if pw.lower() == "exit":
            print(f"{Colors.CYAN}👋 Exiting.{Colors.END}")
            pause("Press ENTER to close this terminal...")
            break

        print(f"\n🔓 Attempting unlock with: {Colors.BOLD}{pw}{Colors.END}")
        spinner("Running steghide")

        if run_steghide(pw, image_path, output_path):
            print("\n" + "=" * 50)
            print_success("ACCESS GRANTED! Message recovered:")
            print("=" * 50)
            print("--------------- CONTENT ---------------")
            with open(output_path, "r", errors="replace") as f:
                print(f"{Colors.BOLD}{f.read().strip()}{Colors.END}")
            print("---------------------------------------\n")
            print(f"📁 Evidence saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
            print(f"{Colors.CYAN}🧠 Look for the flag format: CCRI-AAAA-1111{Colors.END}")
            pause("Press ENTER to close this terminal...")
            break
        else:
            print_error("Access Denied. That password was incorrect.")
            print("💡 Hint: Search Google for 'most common passwords'.\n")
            # Cleanup failed attempt artifacts
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass

# === Entry Point ===
if __name__ == "__main__":
    main()