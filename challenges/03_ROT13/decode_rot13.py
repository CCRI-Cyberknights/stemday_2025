#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

def rot13(text: str) -> str:
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr((ord(c) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            result.append(chr((ord(c) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(c)
    return "".join(result)

def animate_rot13(lines, delay=0.05):
    for line in lines:
        decoded = rot13(line)
        print(f"> {decoded.strip()}")
        time.sleep(delay)

def main():
    clear_screen()
    print("🔐 ROT13 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: cipher.txt")
    print("🎯 Goal: Decode this message and find the hidden CCRI flag.\n")
    print("💡 What is ROT13?")
    print("   ➡️ A Caesar cipher that shifts each letter 13 places in the alphabet.")
    print("   ➡️ Encoding and decoding are the same.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("For every line in cipher.txt:")
    print("  ➡️ Rotate each letter by 13 positions (A→N, N→A).")
    print("  ➡️ We’ll animate the decoding so you can see it happen.\n")
    pause("Press ENTER to launch the animated decoder...")

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "cipher.txt"
    output_path = script_dir / "decoded_output.txt"

    if not input_path.is_file() or input_path.stat().st_size == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    lines = input_path.read_text(encoding="utf-8").splitlines()
    clear_screen()
    print("🔓 Decoding intercepted message...\n")
    animate_rot13(lines)

    decoded = "\n".join(rot13(line) for line in lines)
    output_path.write_text(decoded + "\n", encoding="utf-8")

    print("\n✅ Final Decoded Message saved to:")
    print(f"   📁 {output_path}\n")
    print("🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111")
    print("📋 Copy the correct flag and paste it into the scoreboard when ready.\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
