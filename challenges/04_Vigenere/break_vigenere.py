#!/usr/bin/env python3
import os
import sys
import re
import time  # ✅ added for spinner

# === Terminal Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    This keeps students from just mashing ENTER through explanations.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def spinner(message="Working", duration=2.0, interval=0.15):
    """
    Simple text spinner to give the feeling of work being done.
    """
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
    pause_nonempty("Type 'ready' when you're ready to see how we'd decrypt this: ")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We intercepted an encrypted message stored in cipher.txt.")
    print("In this guided helper, Python is doing the Vigenère math for you.\n")
    print("If you were writing your own tool, a command-line workflow might look like:\n")
    print("   python3 vigenere_helper.py cipher.txt SECRETKEY > decoded_output.txt\n")
    print("🔍 Command breakdown:")
    print("   python3 vigenere_helper.py → Run a Python script that knows the Vigenère algorithm")
    print("   cipher.txt                 → Input file containing the encrypted message")
    print("   SECRETKEY                  → The keyword you want to try")
    print("   > decoded_output.txt       → Save the decrypted result into this file\n")
    print("In this challenge, you'll test different keywords to uncover the hidden CCRI flag.\n")
    pause_nonempty("Type 'start' when you're ready to begin trying keywords: ")

    with open(cipher_file, "r", encoding="utf-8") as f:
        ciphertext = f.read()

    while True:
        key = input("🔑 Enter a keyword to try (or type 'exit' to quit): ").strip()

        if key.lower() == "exit":
            print("\n👋 Exiting. Stay sharp, Agent.")
            break

        if not key:
            print("⚠️ Please enter a keyword or type 'exit'.\n")
            continue

        print(f"\n⏳ Decrypting with keyword: {key}")
        spinner("Decoding message")

        plaintext = vigenere_decrypt(ciphertext, key)

        print("\n📄 Decrypted Output:")
        print("-----------------------------")
        print(plaintext)
        print("-----------------------------\n")

        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(plaintext)

        flag = find_flag(plaintext)
        if flag:
            print(f"✅ Flag found: {flag}")
            print(f"📁 Saved to: {output_file}\n")
            break
        else:
            print("❌ No valid CCRI flag format detected.")
            again = input("🔁 Try another keyword? (Y/n): ").strip().lower()
            if again == "n":
                break

    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()
