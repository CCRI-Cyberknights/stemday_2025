#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

# === Terminal Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

# === ROT13 Cipher ===
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

# === Animated Decoder (in-place clean overwrite) ===
def animate_rot13_lines(lines, delay=0.25):
    # Print scrambled lines
    for line in lines:
        print(f"> {line}")

    pause("\n🧠 The message above is scrambled using ROT13. Press ENTER to decode...\n")

    # ✅ Move cursor to top of block (including "🔓..." above)
    print(f"\033[{len(lines) + 4}A", end="")

    for line in lines:
        decoded = rot13(line)
        print("\033[2K\r> " + decoded)
        time.sleep(delay)


# === Main Flow ===
def main():
    clear_screen()
    print("🔐 ROT13 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: cipher.txt")
    print("🎯 Goal: Decode this message and find the hidden CCRI flag.\n")
    print("💡 What is ROT13?")
    print("   ➤ A Caesar cipher that shifts each letter 13 positions.")
    print("   ➤ Encoding and decoding are the same.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We intercepted a scrambled message in cipher.txt.")
    print("Let’s watch it decode — line by line.\n")
    pause("Press ENTER to begin live decoding...")

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "cipher.txt"
    output_path = script_dir / "decoded_output.txt"

    if not input_path.is_file() or input_path.stat().st_size == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    lines = input_path.read_text(encoding="utf-8").splitlines()
    clear_screen()
    print("🔓 Scanning and preparing ROT13 animation...\n")
    animate_rot13_lines(lines, delay=1.0)

    decoded = "\n".join(rot13(line) for line in lines)
    output_path.write_text(decoded + "\n", encoding="utf-8")

    print("\n✅ Final Decoded Message saved to:")
    print(f"   📁 {output_path}\n")
    print("🧠 Look carefully: Only one string matches the CCRI flag format: CCRI-AAAA-1111")
    print("📋 Copy the correct flag and paste it into the scoreboard when ready.\n")
    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()
