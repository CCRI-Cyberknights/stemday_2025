#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

CHALLENGE_ID = "16_Hex_Hunting"
FLAG_PATTERN = r"CCRI-[A-Z]{4}-[0-9]{4}"
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

def search_flags(binary_file, pattern=FLAG_PATTERN):
    try:
        result = subprocess.run(["strings", binary_file], stdout=subprocess.PIPE, text=True)
        return [line.strip() for line in result.stdout.splitlines() if re.match(pattern, line.strip())]
    except Exception as e:
        print(f"❌ Error while scanning binary: {e}")
        return []

def find_offset(binary_file, target_string):
    try:
        result = subprocess.run(["grep", "-abo", target_string, binary_file], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.strip().splitlines():
            return int(line.split(":")[0])
    except:
        return None

def show_hex_context(binary_file, offset, context=64):
    start = max(0, offset - 16)
    try:
        dd = subprocess.Popen(["dd", f"if={binary_file}", "bs=1", f"skip={start}", f"count={context}"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        xxd = subprocess.Popen(["xxd"], stdin=dd.stdout)
        dd.stdout.close()
        xxd.wait()
    except Exception as e:
        print(f"❌ Could not show hex context: {e}")

def main():
    clear_screen()
    print("🔍 Hex Flag Hunter")
    print("============================\n")
    print("🎯 Target binary:", BINARY_FILE)
    print("💡 Goal: Locate the real flag (format: CCRI-XXXX-1234).")
    print("⚠️  Multiple candidate flags are embedded, but only ONE is correct!\n")

    if not os.path.exists(BINARY_FILE):
        print(f"❌ Cannot find {BINARY_FILE}")
        sys.exit(1)

    pause("Press ENTER to begin scanning...")
    scanning_animation()
    flags = search_flags(BINARY_FILE)

    if not flags:
        print("❌ No flag-like patterns found in binary.")
        sys.exit(1)

    print(f"\n✅ Found {len(flags)} candidate flag(s):\n")
    for i, flag in enumerate(flags):
        print(f"  [{i+1}] {flag}")
    print()

    for i, flag in enumerate(flags):
        print("-------------------------------------------------")
        print(f"[{i+1}/{len(flags)}] Candidate Flag: {flag}")
        offset = find_offset(BINARY_FILE, flag)
        if offset is not None:
            print(f"📍 Approximate byte offset: {offset}")
            print("📖 Hex context (around flag):")
            show_hex_context(BINARY_FILE, offset)
        else:
            print("⚠️ Could not find offset for this flag.")

        while True:
            print("\nOptions:")
            print("1) ✅ Mark this flag as POSSIBLE and save to notes.txt")
            print("2) ➡️ Skip to next flag")
            print("3) 🚪 Quit investigation")
            choice = input("Choose an option (1-3): ").strip()
            if choice == "1":
                with open(NOTES_FILE, "a") as f:
                    f.write(flag + "\n")
                print(f"✅ Saved '{flag}' to {NOTES_FILE}")
                time.sleep(0.5)
                break
            elif choice == "2":
                print("➡️ Skipping to next candidate...\n")
                time.sleep(0.5)
                break
            elif choice == "3":
                print("👋 Exiting investigation early.")
                print(f"📁 All saved candidate flags are in {NOTES_FILE}")
                sys.exit(0)
            else:
                print("⚠️ Invalid choice. Please enter 1, 2, or 3.")

    print("\n🎉 Investigation complete!")
    print(f"📁 All saved candidate flags are in {NOTES_FILE}")
    pause()

if __name__ == "__main__":
    main()
