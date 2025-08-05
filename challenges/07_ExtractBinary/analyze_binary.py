#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

regex_pattern = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def run_strings(binary_path, output_path):
    try:
        with open(output_path, "w") as out_f:
            subprocess.run(["strings", binary_path], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.", file=sys.stderr)
        sys.exit(1)

def search_for_flags(file_path, regex):
    matches = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR during flag search: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_binary = os.path.join(script_dir, "hidden_flag")
    outfile = os.path.join(script_dir, "extracted_strings.txt")

    clear_screen()
    print("🧪 Binary Forensics Challenge")
    print("=============================\n")
    print("📦 Target binary: hidden_flag")
    print("🔧 Tool in use: strings\n")
    print("🎯 Goal: Uncover a hidden flag embedded inside this compiled program.\n")
    pause()

    if not os.path.isfile(target_binary):
        print(f"\n❌ ERROR: The file 'hidden_flag' was not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print(f"\n🔍 Running: strings \"{target_binary}\" > \"{outfile}\"")
    run_strings(target_binary, outfile)
    time.sleep(0.5)
    print(f"✅ All extracted strings saved to: {outfile}\n")

    preview_lines = 15
    print(f"📄 Previewing the first {preview_lines} lines of extracted text:")
    print("--------------------------------------------------")
    try:
        with open(outfile, "r") as f:
            for i, line in enumerate(f):
                if i >= preview_lines:
                    break
                print(line.strip())
    except FileNotFoundError:
        print("❌ ERROR: Could not open extracted_strings.txt.")
    print("--------------------------------------------------\n")
    pause("Press ENTER to scan for flag patterns...")

    print("🔎 Scanning for flag-like patterns (format: XXXX-YYYY-ZZZZ)...")
    time.sleep(0.5)
    matches = search_for_flags(outfile, regex_pattern)

    if matches:
        print(f"\n📌 Found {len(matches)} possible flag(s):")
        for m in matches:
            print(f"   ➡️ {m}")
    else:
        print("\n⚠️ No obvious flags found. Try scanning manually in extracted_strings.txt.")

    print()
    keyword = input("🔍 Enter a keyword to search in the full dump (or hit ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {outfile}...")
        try:
            subprocess.run(["grep", "-i", "--color=always", keyword, outfile], check=False)
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping keyword search.")

    print("\n✅ Done! You can inspect extracted_strings.txt further or try other tools like 'hexdump' for deeper analysis.")
    print("🧠 Remember: Only one string matches the official flag format: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
