#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
ZIP_FILE = "secret.zip"
WORDLIST = "wordlist.txt"
B64_FILE = "message_encoded.txt"
OUTPUT_FILE = "decoded_output.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def progress_bar(length=30, delay=0.03):
    for _ in range(length):
        sys.stdout.write("█")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    zip_path = get_path(ZIP_FILE)
    wordlist_path = get_path(WORDLIST)
    b64_path = get_path(B64_FILE)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.isfile(zip_path) or not os.path.isfile(wordlist_path):
        print_error("Missing zip file or wordlist.")
        sys.exit(1)

    # 2. Mission Briefing
    header("🔓 ZIP Password Cracking Challenge")
    
    print(f"📄 Target Archive: {Colors.BOLD}{ZIP_FILE}{Colors.END}")
    print(f"📄 Password List:  {Colors.BOLD}{WORDLIST}{Colors.END}")
    print("🎯 Goal: Automate a dictionary attack to break the lock.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Lock:** Standard ZIP encryption.")
    print("   ➤ **The Strategy:** Dictionary Attack.")
    print("   ➤ **The Concept:** Trying every single word in a list until one works.")
    print("   ➤ **The Requirement:** Humans are too slow. We must use automation.\n")
    
    require_input("Type 'ready' to initialize the attack tools: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("This script simulates the automation required for a Dictionary Attack.")
    print("It effectively writes a loop that runs the following commands thousands of times:\n")
    
    print("Step 1: Test a password candidate (without extracting yet)")
    print(f"   {Colors.GREEN}unzip -P [PASSWORD] -t {ZIP_FILE}{Colors.END}\n")
    
    print("Step 2: If the test returns 'OK', extract the files")
    print(f"   {Colors.GREEN}unzip -o -P [PASSWORD] {ZIP_FILE} -d .{Colors.END}\n")
    
    print("Step 3: Decode the inner content (as seen in Challenge #2)")
    print(f"   {Colors.GREEN}base64 --decode {B64_FILE} > {OUTPUT_FILE}{Colors.END}\n")
    
    require_input("Type 'start' to launch the brute force attack: ", "start")

    # 4. Cracking Phase
    clear_screen()
    print(f"{Colors.CYAN}🔍 Beginning Dictionary Attack...{Colors.END}\n")
    print(f"📁 Wordlist: {Colors.BOLD}{WORDLIST}{Colors.END}")
    print(f"📦 Target:   {Colors.BOLD}{ZIP_FILE}{Colors.END}\n")
    print("⏳ Starting engine...\n")
    progress_bar(length=20, delay=0.04)

    found = False
    password = None

    with open(wordlist_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            pw = line.strip()
            if not pw: continue
            
            # Simulated cracking output - Overwrite line for speed effect
            print(f"\r[🔐] Testing: {Colors.YELLOW}{pw:<20}{Colors.END}", end="", flush=True)
            time.sleep(0.01) # Slightly faster to look cool

            # The actual check
            result = subprocess.run(
                ["unzip", "-P", pw, "-t", zip_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if "OK" in result.stdout:
                print(f"\n\n{Colors.GREEN}✅ MATCH FOUND: {Colors.BOLD}{pw}{Colors.END}")
                password = pw
                found = True
                break

    if not found:
        print("\n")
        print_error("Password not found in wordlist.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # 5. Extraction Phase
    while True:
        proceed = input(f"\n{Colors.YELLOW}📦 Extract and decode the message now? (yes/no): {Colors.END}").strip().lower()
        if proceed == "yes":
            break
        elif proceed == "no":
            print(f"\n{Colors.CYAN}👋 Exiting without extracting.{Colors.END}")
            pause("Press ENTER to close this terminal...")
            return
        else:
            print(f"{Colors.RED}   ❌ Please type 'yes' or 'no'.{Colors.END}")

    print("\n📦 Extracting archive contents...\n")
    spinner("Extracting files")

    subprocess.run(["unzip", "-o", "-P", password, zip_path, "-d", script_dir],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(b64_path):
        print_error("Extraction failed — missing Base64 message.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print(f"📄 Extracted Base64 Message ({B64_FILE}):")
    print("-" * 50)
    with open(b64_path, "r", encoding="utf-8", errors="replace") as f:
        print(f"{Colors.YELLOW}{f.read()}{Colors.END}")
    print("-" * 50 + "\n")

    # 6. Decoding Phase
    while True:
        decode = input(f"{Colors.YELLOW}🔎 Decode the message now? (yes/no): {Colors.END}").strip().lower()
        if decode == "yes":
            break
        elif decode == "no":
            print(f"\n{Colors.CYAN}👋 Exiting without decoding.{Colors.END}")
            pause("Press ENTER to close this terminal...")
            return
        else:
            print(f"{Colors.RED}   ❌ Please type 'yes' or 'no'.{Colors.END}\n")

    print("\n⏳ Decoding message with Base64...\n")
    progress_bar(length=25, delay=0.03)

    result = subprocess.run(["base64", "--decode", b64_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)

    if result.returncode != 0:
        print_error("Decoding failed.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    decoded = result.stdout.strip()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decoded + "\n")

    # 7. Final Success
    print(f"\n{Colors.GREEN}🧾 Decoded Message:{Colors.END}")
    print("-" * 50)
    print(f"{Colors.BOLD}{decoded}{Colors.END}")
    print("-" * 50 + "\n")
    print(f"💾 Saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
    print(f"{Colors.CYAN}🧠 Look for a flag like: CCRI-AAAA-1111{Colors.END}\n")
    
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()