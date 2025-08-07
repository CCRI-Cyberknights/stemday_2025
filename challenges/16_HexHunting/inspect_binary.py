#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

CHALLENGE_ID = "16_Hex_Hunting"
REAL_FLAG_PATTERN = r"CCRI-[A-Z]{4}-\d{4}"
FAKE_FLAG_PATTERN = r"[A-Z]{4}-[A-Z]{4}-\d{4}|[A-Z]{4}-\d{4}-[A-Z]{4}"
BINARY_FILE = "hex_flag.bin"
NOTES_FILE = "notes.txt"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def scanning_animation():
    print("\n🔎 Scanning binary for flag-like patterns", end="", flush=True)
    for _ in range(5):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

def extract_flag_candidates(binary_file):
    try:
        with open(binary_file, "rb") as f:
            data = f.read()

        # Match CCRI-XXXX-1234, XXXX-YYYY-1234, XXXX-1234-YYYY
        flag_pattern = re.compile(
            rb"(CCRI-[A-Z]{4}-\d{4})|([A-Z]{4}-[A-Z]{4}-\d{4})|([A-Z]{4}-\d{4}-[A-Z]{4})"
        )

        matches = []
        for match in flag_pattern.finditer(data):
            flag_bytes = match.group(0)
            try:
                flag_str = flag_bytes.decode("ascii")
                matches.append((match.start(), flag_str))
            except UnicodeDecodeError:
                continue

        return matches

    except Exception as e:
        print(f"❌ Binary scan failed: {e}")
        return []

def show_hex_context(binary_file, offset, context=64):
    start = max(0, offset - 16)
    try:
        dd = subprocess.Popen(
            ["dd", f"if={binary_file}", "bs=1", f"skip={start}", f"count={context}"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        xxd = subprocess.Popen(["xxd"], stdin=dd.stdout)
        dd.stdout.close()
        xxd.wait()
    except Exception as e:
        print(f"❌ Could not show hex context: {e}")

def main():
    clear_screen()
    print("🔍 Hex Flag Hunter")
    print("============================\n")
    print(f"🎯 Target binary: {BINARY_FILE}")
    print("💡 Goal: Locate the real flag (format: CCRI-XXXX-1234).")
    print("⚠️  Multiple candidate flags are embedded, but only ONE is correct!\n")

    if not os.path.exists(BINARY_FILE):
        print(f"❌ Error: Cannot find {BINARY_FILE}")
        sys.exit(1)

    # Clean or create notes file
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)

    pause("🔑 Press ENTER to begin scanning...")
    scanning_animation()
    flags = extract_flag_candidates(BINARY_FILE)

    if not flags:
        print("❌ No flag-like patterns found in binary.")
        sys.exit(1)

    print(f"\n✅ Detected {len(flags)} flag-like pattern(s)!")
    print("🧪 You'll now investigate each one by reviewing its raw hex context.")
    pause("🔬 Press ENTER to begin reviewing candidates...")

    for i, (offset, flag) in enumerate(flags):
        clear_screen()
        print("-------------------------------------------------")
        print(f"[{i+1}/{len(flags)}] 🏷️  Candidate Flag: {flag}")
        print(f"📍 Approximate Byte Offset: {offset}")
        print("📖 Hex Dump Around Candidate:")
        show_hex_context(BINARY_FILE, offset)

        while True:
            print("\nActions:")
            print("  [1] ✅ Mark as POSSIBLE (save to notes.txt)")
            print("  [2] ➡️  Skip to next candidate")
            print("  [3] 🚪 Quit investigation")
            choice = input("Choose an action (1-3): ").strip()
            if choice == "1":
                with open(NOTES_FILE, "a") as f:
                    f.write(flag + "\n")
                print(f"✅ Saved '{flag}' to {NOTES_FILE}")
                time.sleep(0.6)
                break
            elif choice == "2":
                print("➡️ Skipping to next candidate...")
                time.sleep(0.4)
                break
            elif choice == "3":
                print("👋 Exiting early. Your saved flags are in notes.txt.")
                print(f"📁 Saved flags: {NOTES_FILE}")
                sys.exit(0)
            else:
                print("⚠️ Invalid input. Please enter 1, 2, or 3.")

    print("\n🎉 Flag inspection complete!")
    print(f"📁 Review your notes: {NOTES_FILE}")
    pause("🔚 Press ENTER to exit.")

if __name__ == "__main__":
    main()
