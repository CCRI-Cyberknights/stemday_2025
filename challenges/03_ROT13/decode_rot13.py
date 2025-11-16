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

def pause_nonempty(msg="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    This stops students from just mashing ENTER through all the explanations.
    """
    while True:
        answer = input(msg)
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

    pause_nonempty("\n🧠 The message above is scrambled using ROT13. Type anything, then press ENTER to decode...\n")

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
    print("   ➤ Encoding and decoding are the same (apply ROT13 twice = original text).\n")
    pause_nonempty("Type 'ready' when you're ready to learn how we decode this: ")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("We intercepted a scrambled message in cipher.txt.")
    print("In this guided version, Python is doing the ROT13 math for you.\n")
    print("If you were in a regular Linux terminal, you might see commands like:\n")
    print("  Using the `tr` command:")
    print("    tr 'A-Za-z' 'N-ZA-Mn-za-m' < cipher.txt > decoded_output.txt\n")
    print("  Or using Python directly:")
    print("    python3 -c \"import codecs; print(codecs.encode(open('cipher.txt').read(), 'rot_13'))\"")
    print("        > decoded_output.txt\n")
    print("🔍 Command breakdown (tr example):")
    print("   tr 'A-Za-z' 'N-ZA-Mn-za-m' → Translate each A–Z/a–z to the letter 13 ahead")
    print("   < cipher.txt               → Use cipher.txt as input")
    print("   > decoded_output.txt       → Save the decoded text into this file\n")
    pause_nonempty("Type 'show' to watch the scrambled message decode line by line: ")

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
    spinner("Preparing")

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
