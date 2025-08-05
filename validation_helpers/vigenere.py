#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "04_Vigenere"

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

def extract_flag(text: str) -> str:
    match = re.search(r"CCRI-[A-Z0-9]{4}-\d{4}", text)
    return match.group(0) if match else ""

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    expected_flag = data.get("real_flag")

    if mode == "guided":
        file_rel = data.get("challenge_file", f"challenges/{challenge_id}/cipher.txt")
    else:
        file_rel = f"challenges_solo/{challenge_id}/cipher.txt"

    input_path = root / file_rel

    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}", file=sys.stderr)
        return False

    try:
        ciphertext = input_path.read_text(encoding="utf-8")
        decrypted = vigenere_decrypt(ciphertext, "login")  # fixed keyword
        found_flag = extract_flag(decrypted)
    except Exception as e:
        print(f"❌ Error during decryption or extraction: {e}", file=sys.stderr)
        return False

    if not found_flag:
        print("❌ No CCRI flag found in decrypted text.", file=sys.stderr)
        return False

    if found_flag == expected_flag:
        print(f"✅ Validation success: found flag {found_flag}")
        return True
    else:
        print(f"❌ Incorrect flag: found {found_flag}, expected {expected_flag}", file=sys.stderr)
        return False

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)
