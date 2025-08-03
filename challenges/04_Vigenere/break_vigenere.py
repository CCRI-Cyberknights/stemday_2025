#!/usr/bin/env python3
import os
import sys
import json
import re

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "04_Vigenere"

# === Detect Validation Mode
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

# === Utilities
def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_expected_flag():
    project_root = find_project_root()
    json_file = SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON
    json_path = os.path.join(project_root, "web_version_admin", json_file)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        return unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
        sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

# === Vigenère Logic
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

def find_ccri_flag(text):
    match = re.search(r"CCRI-[A-Z0-9]{4}-\d{4}", text)
    return match.group(0) if match else None

# === Main Logic
def main():
    project_root = find_project_root()
    cwd = os.getcwd()
    script_dir = os.path.abspath(os.path.dirname(__file__))

    # File paths
    if validation_mode:
        cipher_file = os.path.join(cwd, "cipher.txt")
        output_file = os.path.join(cwd, "decoded_output.txt")
    else:
        cipher_file = os.path.join(script_dir, "cipher.txt")
        output_file = os.path.join(script_dir, "decoded_output.txt")

    if not os.path.isfile(cipher_file):
        print(f"❌ ERROR: cipher.txt not found at {cipher_file}")
        sys.exit(1)

    # === Validation Path ===
    if validation_mode:
        expected_flag = load_expected_flag()
        keyword = "login"  # fixed for validation

        with open(cipher_file, "r", encoding="utf-8") as f:
            ciphertext = f.read()
        plaintext = vigenere_decrypt(ciphertext, keyword)

        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(plaintext + "\n")

        found_flag = find_ccri_flag(plaintext)

        if found_flag:
            if found_flag == expected_flag:
                print(f"✅ Validation success: found flag {found_flag}")
                sys.exit(0)
            else:
                print(f"❌ Validation failed: found incorrect flag {found_flag}, expected {expected_flag}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"❌ Validation failed: no CCRI flag found in decoded content", file=sys.stderr)
            print(f"🔎 Debug: Decrypted text was:\n{plaintext}\n")
            sys.exit(1)

    # === Student Mode ===
    clear_screen()
    print("🔐 Vigenère Cipher Breaker")
    print("===============================\n")
    print(f"📄 Encrypted message: {cipher_file}")
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

        flag = find_ccri_flag(plaintext)
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
