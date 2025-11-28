#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    """Force terminal resize for better visibility."""
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def scanning_animation():
    print("\n🔎 Scanning binary for flag-like patterns", end="", flush=True)
    for _ in range(5):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

# === Core Helpers ===
def extract_flag_candidates(binary_path):
    try:
        with open(binary_path, "rb") as f:
            data = f.read()

        # Match CCRI-AAAA-1111, XXXX-YYYY-1111, XXXX-1111-YYYY
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

def show_hex_context(binary_path, offset, context=64):
    start = max(0, offset - 16)
    try:
        # Use str(binary_path) to ensure subprocess handles it correctly
        dd = subprocess.Popen(
            ["dd", f"if={str(binary_path)}", "bs=1", f"skip={start}", f"count={context}"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        xxd = subprocess.Popen(["xxd"], stdin=dd.stdout)
        dd.stdout.close()
        xxd.wait()
    except Exception as e:
        print(f"❌ Could not show hex context: {e}")

# === Main Flow ===
def main():
    # 1. Resize terminal first
    resize_terminal(35, 90)
    clear_screen()

    # 2. RESOLVE ABSOLUTE PATHS (The Fix)
    # This ensures we find the file even if launched from a different folder
    script_dir = Path(__file__).resolve().parent
    binary_path = script_dir / "hex_flag.bin"
    notes_path = script_dir / "notes.txt"

    print("🔍 Hex Flag Hunter")
    print("============================\n")
    print(f"🎯 Target binary: {binary_path.name}")
    print("💡 Goal: Locate the real flag (format: CCRI-AAAA-1111).")
    print("⚠️  Multiple candidate flags are embedded, but only ONE is correct!\n")
    print("🧠 What are we actually doing here?")
    print("   ➤ A compiled/binary file can contain lots of embedded text and data.")
    print("   ➤ Some of those bytes look like flags, others are decoys.")
    print("   ➤ We'll scan the raw bytes for anything that *looks* like a flag,")
    print("      then inspect a hex dump around each candidate to judge context.\n")
    
    # 3. SAFETY CHECK WITH PAUSE
    if not binary_path.is_file():
        print(f"\n❌ CRITICAL ERROR: Cannot find '{binary_path.name}'")
        print(f"   Looking in: {script_dir}")
        print("   Did you move the script or the binary file?\n")
        # Pause allows user to read the error before the window vanishes
        pause("Press ENTER to exit...") 
        sys.exit(1)

    # Clean or create notes file
    if notes_path.exists():
        os.remove(notes_path)

    pause_nonempty("Type 'scan' when you're ready to begin scanning the binary: ")
    scanning_animation()
    
    flags = extract_flag_candidates(binary_path)

    if not flags:
        print("❌ No flag-like patterns found in binary.")
        pause("Press ENTER to exit...")
        sys.exit(1)

    print(f"\n✅ Detected {len(flags)} flag-like pattern(s)!")
    print("🧪 You'll now investigate each one by reviewing its raw hex context.")
    print("   Use what you know about the story + placement to decide what's real.")
    pause_nonempty("🔬 Type anything, then press ENTER to begin reviewing candidates: ")

    for i, (offset, flag) in enumerate(flags):
        clear_screen()
        print("-------------------------------------------------")
        print(f"[{i+1}/{len(flags)}] 🏷️  Candidate Flag: {flag}")
        print(f"📍 Approximate Byte Offset: {offset}")
        print("📖 Hex Dump Around Candidate:")
        show_hex_context(binary_path, offset)

        while True:
            print("\nActions:")
            print("  [1] ✅ Mark as POSSIBLE (save to notes.txt)")
            print("  [2] ➡️  Skip to next candidate")
            print("  [3] 🚪 Quit investigation")
            choice = input("Choose an action (1-3): ").strip()
            if choice == "1":
                with open(notes_path, "a") as f:
                    f.write(flag + "\n")
                print(f"✅ Saved '{flag}' to {notes_path.name}")
                time.sleep(0.6)
                break
            elif choice == "2":
                print("➡️ Skipping to next candidate...")
                time.sleep(0.4)
                break
            elif choice == "3":
                print("👋 Exiting early. Your saved flags are in notes.txt.")
                sys.exit(0)
            else:
                print("⚠️ Invalid input. Please enter 1, 2, or 3.")

    print("\n🎉 Flag inspection complete!")
    print(f"📁 Review your notes: {notes_path.name}")
    print("🧠 Remember: Only one of those candidates is the *true* CCRI flag.")
    pause("🔚 Press ENTER to exit.")

if __name__ == "__main__":
    main()