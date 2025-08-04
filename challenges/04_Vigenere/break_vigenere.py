#!/usr/bin/env python3
import os
import sys
import re

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.lower()
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

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    cipher_file = os.path.join(script_dir, "cipher.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    if not os.path.isfile(cipher_file):
        print(f"❌ ERROR: cipher.txt not found.")
        sys.exit(1)

    clear_screen()
    print("🔐 Vigenère Cipher Breaker")
    print("===============================\n")
    print("📄 Encrypted message: cipher.txt")
    print("🎯 Goal: Decrypt it and find the CCRI flag.\n")
    pause()

    with open(cipher_file, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    while True:
        key = input("🔑 Enter a keyword to try (or type 'exit' to quit): ").strip()

        if key.lower() == "exit":
            print("\n👋 Exiting. Stay sharp, Agent!")
            break

        if not key:
            print("⚠️ Please enter a keyword or type 'exit'.\n")
            continue

        plaintext = vigenere_decrypt(ciphertext, key)
        print("\n📄 Decoded Output:")
        print("-----------------------------")
        print(plaintext)
        print("-----------------------------\n")

        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(plaintext)

        flag = find_flag(plaintext)
        if flag:
            print(f"✅ Flag found in decrypted text: {flag}")
            print(f"📁 Saved to: {output_file}")
            break
        else:
            print("❌ No valid CCRI flag format detected.\n")
            again = input("🔁 Try another keyword? (Y/n): ").strip().lower()
            if again == "n":
                break

    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
