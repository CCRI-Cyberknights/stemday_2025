#!/usr/bin/env python3
import os
import sys
import re

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
CIPHER_FILE = "cipher.txt"
OUTPUT_FILE = "decoded_output.txt"

# === Vigenère Cipher Logic ===
def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
    if not key: return ciphertext 
    
    key_len = len(key)
    key_indices = [ord(k) - ord('a') for k in key]
    key_pos = 0

    for char in ciphertext:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            pi = ord(char) - offset
            ki = key_indices[key_pos % key_len]
            decrypted = chr((pi - ki) % 26 + offset)
            result.append(decrypted)
            key_pos += 1
        else:
            result.append(char)

    return ''.join(result)

def find_flag(text):
    match = re.search(r"CCRI-[A-Z0-9]{4}-\d{4}", text)
    return match.group(0) if match else None

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# === Main Flow ===
def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    cipher_path = get_path(CIPHER_FILE)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.isfile(cipher_path):
        print_error(f"{CIPHER_FILE} not found.")
        sys.exit(1)

    # 2. Mission Briefing
    header("🔐 Vigenère Cipher Breaker")
    
    print(f"📄 Encrypted message: {Colors.BOLD}{CIPHER_FILE}{Colors.END}")
    print("🎯 Goal: Decrypt the message and locate the CCRI flag.\n")
    print(f"{Colors.CYAN}💡 What is the Vigenère cipher?{Colors.END}")
    print("   ➤ A substitution cipher that uses a repeating keyword.")
    print("   ➤ Each letter of the key shifts the alphabet by a different amount.")
    print("   ➤ Stronger than a basic Caesar cipher because the pattern repeats over a key.\n")
    
    with open(cipher_path, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    require_input("Type 'ready' to load the decryption tool: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("We intercepted an encrypted message stored in cipher.txt.")
    print("In this guided helper, Python is doing the Vigenère math for you.\n")
    print("If you were writing your own tool, a command-line workflow might look like:\n")
    print(f"   {Colors.GREEN}python3 vigenere_helper.py cipher.txt SECRETKEY > decoded_output.txt{Colors.END}\n")
    print("In this challenge, you'll test different keywords to uncover the hidden CCRI flag.\n")
    
    require_input("Type 'start' to see the encrypted message: ", "start")

    # 4. Main Decryption Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}🔐 Vigenère Decryption Tool{Colors.END}")
        print("===========================\n")
        
        print(f"📄 Current File Contents ({Colors.RED}Encrypted{Colors.END}):")
        print("-" * 50)
        preview_lines = ciphertext.splitlines()
        for line in preview_lines[:8]: 
            print(f"> {Colors.YELLOW}{line}{Colors.END}")
        if len(preview_lines) > 8:
            print(f"> {Colors.YELLOW}... [remaining text hidden] ...{Colors.END}")
        print("-" * 50 + "\n")

        key = input(f"{Colors.YELLOW}🔑 Enter a keyword to try (or type 'exit' to quit): {Colors.END}").strip().lower()

        if key == "exit":
            print(f"\n{Colors.CYAN}👋 Exiting. Stay sharp, Agent.{Colors.END}")
            break

        if not key:
            continue

        print(f"\n⏳ Decrypting with keyword: '{Colors.BOLD}{key}{Colors.END}'")
        spinner("Processing")

        plaintext = vigenere_decrypt(ciphertext, key)
        flag = find_flag(plaintext)

        # Show Results
        clear_screen()
        print(f"🔑 Key Used: '{Colors.BOLD}{key}{Colors.END}'")
        print("=============================")
        print("📄 Resulting Text:")
        print("-" * 50)
        # We print a snippet if it's too long, or the whole thing if it fits
        print(plaintext[:500] + ("..." if len(plaintext) > 500 else ""))
        print("-" * 50 + "\n")

        if flag:
            print_success(f"SUCCESS! Flag found: {Colors.BOLD}{flag}{Colors.END}")
            print(f"📁 Saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}\n")
            with open(output_path, "w", encoding="utf-8") as f_out:
                f_out.write(plaintext)
            pause("Press ENTER to close this terminal...")
            break
        else:
            print_error("FAILURE: No valid CCRI flag found in the output.")
            print("   The text still looks like garbage. That was the wrong key.")
            print(f"   (Hint: The key relates to the user {Colors.BOLD}'ccri_stem'{Colors.END} credentials...)\n")
            
            while True:
                again = input(f"{Colors.YELLOW}🔁 Do you want to try another keyword? (yes/no): {Colors.END}").strip().lower()
                if again == "yes":
                    break 
                elif again == "no":
                    print(f"\n{Colors.CYAN}👋 Exiting.{Colors.END}")
                    pause("Press ENTER to close this terminal...")
                    sys.exit(0)
                else:
                    print(f"{Colors.RED}   ❌ Please type 'yes' or 'no'.{Colors.END}\n")

if __name__ == "__main__":
    main()