#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from common import find_project_root, load_unlock_data

def vigenere_decrypt(ciphertext: str, key: str) -> str:
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

def find_flag(text: str) -> str:
    match = re.search(r"CCRI-[A-Z0-9]{4}-\d{4}", text)
    return match.group(0) if match else ""

def main():
    challenge_id = "04_Vigenere"
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)

    flag = data.get("real_flag")
    file_rel = data.get("challenge_file", "challenges/04_Vigenere/cipher.txt")
    input_path = root / file_rel

    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        ciphertext = input_path.read_text(encoding="utf-8")
        decrypted = vigenere_decrypt(ciphertext, "login")  # fixed keyword
        found_flag = find_flag(decrypted)
    except Exception as e:
        print(f"❌ Error decrypting file: {e}", file=sys.stderr)
        sys.exit(1)

    if found_flag:
        if found_flag == flag:
            print(f"✅ Validation success: found flag {found_flag}")
            sys.exit(0)
        else:
            print(f"❌ Incorrect flag found: {found_flag}, expected {flag}", file=sys.stderr)
            sys.exit(1)
    else:
        print("❌ No CCRI flag found in decrypted text.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
