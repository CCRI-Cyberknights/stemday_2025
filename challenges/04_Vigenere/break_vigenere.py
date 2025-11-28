#!/usr/bin/env python3
import os
import sys
import re
import time

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    """
    Forces the terminal window to resize to the specified dimensions.
    """
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def spinner(message="Working", duration=2.0, interval=0.15):
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

# === Vigenère Cipher Logic ===
def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
    if not key: return ciphertext # Safety for empty key
    
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

# === Flag Extractor ===
def find_flag(text):
    match = re.search(r"CCRI-[A-Z0-9]{4}-\d{4}", text)
    return match.group(0) if match else None

# === Main Flow ===
def main():
    # 1. Resize Window for better visibility
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    cipher_file = os.path.join(script_dir, "cipher.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    if not os.path.isfile(cipher_file):
        print("❌ ERROR: cipher.txt not found.")
        sys.exit(1)

    clear_screen()
    print("🔐 Vigenère Cipher Breaker")
    print("===============================\n")
    print("📄 Encrypted message: cipher.txt")
    print("🎯 Goal: Decrypt the message and locate the CCRI flag.\n")
    print("💡 What is the Vigenère cipher?")
    print("   ➤ A substitution cipher that uses a repeating keyword.")
    print("   ➤ Each letter of the key shifts the alphabet by a different amount.")
    print("   ➤ Stronger than a basic Caesar cipher because the pattern repeats over a key.\n")
    
    # Read the file first
    with open(cipher_file, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    pause_nonempty("Type 'ready' to load the decryption tool: ")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We intercepted an encrypted message stored in cipher.txt.")
    print("In this guided helper, Python is doing the Vigenère math for you.\n")
    print("If you were writing your own tool, a command-line workflow might look like:\n")
    print("   python3 vigenere_helper.py cipher.txt SECRETKEY > decoded_output.txt\n")
    print("In this challenge, you'll test different keywords to uncover the hidden CCRI flag.\n")
    
    pause_nonempty("Type 'start' to see the encrypted message: ")

    # 2. Main Decryption Loop
    while True:
        clear_screen()
        print("🔐 Vigenère Decryption Tool")
        print("===========================\n")
        
        # DISPLAY THE ORIGINAL CIPHERTEXT (Restored Feature)
        print("📄 Current File Contents (Encrypted):")
        print("-------------------------------------")
        # Print first 5 lines or whole thing if short, to save space
        preview_lines = ciphertext.splitlines()
        for line in preview_lines[:8]: 
            print(f"> {line}")
        if len(preview_lines) > 8:
            print("> ... [remaining text hidden] ...")
        print("-------------------------------------\n")

        key = input("🔑 Enter a keyword to try (or type 'exit' to quit): ").strip()

        if key.lower() == "exit":
            print("\n👋 Exiting. Stay sharp, Agent.")
            break

        if not key:
            continue # Just redraw the screen

        print(f"\n⏳ Decrypting with keyword: '{key}'")
        spinner("Processing")

        plaintext = vigenere_decrypt(ciphertext, key)
        flag = find_flag(plaintext)

        # Show the result of this attempt
        clear_screen()
        print(f"🔑 Key Used: '{key}'")
        print("=============================")
        print("📄 Resulting Text:")
        print("-----------------------------")
        print(plaintext)
        print("-----------------------------\n")

        if flag:
            print(f"✅ SUCCESS! Flag found: {flag}")
            print(f"📁 Saved to: {output_file}\n")
            with open(output_file, "w", encoding="utf-8") as f_out:
                f_out.write(plaintext)
            break
        else:
            print("❌ FAILURE: No valid CCRI flag found in the output.")
            print("   The text still looks like garbage. That was the wrong key.")
            print("   (Hint: The key relates to the user 'ccri_stem' credentials...)\n")
            
            again = input("🔁 Try another keyword? (Y/n): ").strip().lower()
            if again == "n":
                break

    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()