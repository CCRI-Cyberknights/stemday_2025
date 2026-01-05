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

# === Vigenère Logic (Internal) ===
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
    
    print(f"📄 Target File: {Colors.BOLD}{CIPHER_FILE}{Colors.END}")
    print("🎯 Goal: Decrypt the message using the correct Keyword.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Cipher:** Vigenère (Polyalphabetic Substitution).")
    print("   ➤ **The Challenge:** Each letter is shifted differently based on a keyword.")
    print("   ➤ **The Clue:** The admin asked: \"What is the opposite of `logout`?\"\n")
    
    with open(cipher_path, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    require_input("Type 'ready' to understand the decryption logic: ", "ready")

    # 3. Algorithm Explanation (Instead of Tool Provisioning)
    header("🛠️ Behind the Scenes")
    print("Deciphering Vigenère by hand is tedious. In a real scenario, you would")
    print("write a script to handle the math for you.\n")
    print("I have a decryption algorithm loaded into memory that does exactly this:\n")
    print(f"   1. It takes your {Colors.BOLD}KEYWORD{Colors.END} (e.g., 'TEST').")
    print("   2. It converts the key into numbers (T=19, E=4, S=18, T=19).")
    print("   3. It subtracts those numbers from the cipher text, looping the key.\n")
    
    print("We will simulate running a command like this:\n")
    print(f"   {Colors.GREEN}python3 decrypt.py {CIPHER_FILE} [YOUR_KEY]{Colors.END}\n")
    
    require_input("Type 'start' to boot the decryption module: ", "start")

    # 4. Main Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}🔐 Vigenère Decryption Console{Colors.END}")
        print("=============================\n")
        
        # Show encrypted snippet
        print(f"📄 {CIPHER_FILE} (First 80 chars):")
        print(f"> {Colors.YELLOW}{ciphertext[:80]}...{Colors.END}\n")

        key = input(f"{Colors.YELLOW}🔑 Enter the keyword based on the clue (or 'exit'): {Colors.END}").strip().lower()

        if key == "exit":
            print(f"\n{Colors.CYAN}👋 Exiting.{Colors.END}")
            break

        if not key:
            continue

        print(f"\n⏳ Running decryption algorithm with key: '{Colors.BOLD}{key}{Colors.END}'")
        spinner("Processing")

        plaintext = vigenere_decrypt(ciphertext, key)
        flag = find_flag(plaintext)

        # Show Results
        clear_screen()
        print(f"🔑 Key Used: '{Colors.BOLD}{key}{Colors.END}'")
        print("=============================")
        print("📄 Resulting Text:")
        print("-" * 50)
        # Show snippet or full text
        print(plaintext[:500] + ("..." if len(plaintext) > 500 else ""))
        print("-" * 50 + "\n")

        if flag:
            print_success(f"SUCCESS! Flag found: {Colors.BOLD}{flag}{Colors.END}")
            print(f"📁 Full output saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}\n")
            with open(output_path, "w", encoding="utf-8") as f_out:
                f_out.write(plaintext)
            
            pause("Press ENTER to close this terminal...")
            break
        else:
            print_error("FAILURE: No valid flag found.")
            print("   The output is still garbled. That was the wrong key.")
            print(f"   (Hint: Read the clue again. What do you do to start a session?)\n")
            
            choice = input(f"{Colors.YELLOW}🔁 Try again? (y/n): {Colors.END}").strip().lower()
            if choice == 'n':
                print(f"\n{Colors.CYAN}👋 Exiting.{Colors.END}")
                sys.exit(0)

if __name__ == "__main__":
    main()