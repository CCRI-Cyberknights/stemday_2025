#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

regex_pattern = r'\b([A-Z0-9]{4}-){2}[A-Z0-9]{4}\b'

# === Terminal Utilities ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    This keeps students from just mashing ENTER through explanations.
    """
    while True:
        answer = input(prompt)
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

# === strings / flag logic ===
def run_strings(binary_path, output_path):
    try:
        with open(output_path, "w", encoding="utf-8", errors="ignore") as out_f:
            subprocess.run(["strings", binary_path], stdout=out_f, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERROR: Failed to run 'strings'.", file=sys.stderr)
        sys.exit(1)

def search_for_flags(file_path, regex):
    matches = []
    try:
        with open(file_path, "r", errors="ignore") as f:
            for i, line in enumerate(f):
                if re.search(regex, line):
                    matches.append(line.strip())
    except Exception as e:
        print(f"❌ ERROR during flag search: {e}", file=sys.stderr)
        sys.exit(1)
    return matches

# === Main Flow ===
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
    print("💡 Why 'strings'?")
    print("   ➤ Compiled programs contain a mix of binary data and human-readable text.")
    print("   ➤ The 'strings' tool scans the file and pulls out the readable text segments.")
    print("   ➤ This is a common first step in binary forensics and malware analysis.\n")
    pause_nonempty("Type 'ready' when you're ready to see the command we'll run: ")

    if not os.path.isfile(target_binary):
        print(f"\n❌ ERROR: The file 'hidden_flag' was not found in {script_dir}.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("To extract all readable strings from the binary, we use:\n")
    print(f"   strings {os.path.basename(target_binary)} > {os.path.basename(outfile)}\n")
    print("🔍 Command breakdown:")
    print("   strings hidden_flag   → Scan the binary for printable text")
    print(f"   > {os.path.basename(outfile):<20}→ Redirect all found strings into a text file")
    print("\nAfter that, we can search inside the text file using tools like 'grep'.\n")
    pause_nonempty("Type 'run' when you're ready to extract strings from the binary: ")

    print(f"\n🔍 Running: strings \"{target_binary}\" > \"{outfile}\"")
    spinner("Extracting strings")
    run_strings(target_binary, outfile)
    time.sleep(0.3)
    print(f"✅ All extracted strings saved to: {outfile}\n")

    preview_lines = 15
    print(f"📄 Previewing the first {preview_lines} lines of extracted text:")
    print("--------------------------------------------------")
    try:
        with open(outfile, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= preview_lines:
                    break
                print(line.strip())
    except FileNotFoundError:
        print("❌ ERROR: Could not open extracted_strings.txt.")
    print("--------------------------------------------------\n")

    # 🔍 KEYWORD SEARCH FIRST
    pause_nonempty("Type anything, then press ENTER to search for a specific keyword...")
    print("You might start by searching for words related to the story, like 'CCRI' or 'Liber8'.")
    keyword = input("🔍 Enter a keyword to search (or hit ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {outfile}...\n")
        print("   Command being used under the hood:")
        print(f"      grep -i {keyword} {os.path.basename(outfile)}\n")
        print("   - grep       → Search for lines matching a pattern")
        print("   - -i         → Case-insensitive search")
        print(f"   - {os.path.basename(outfile)} → File containing all extracted strings\n")
        time.sleep(0.5)
        try:
            subprocess.run(["grep", "-i", "--color=always", keyword, outfile], check=False)
        except FileNotFoundError:
            print("❌ ERROR: grep command not found.")
    else:
        print("⏭️  Skipping keyword search.\n")

    # 🔎 FLAG PATTERN SEARCH
    pause_nonempty("Type anything, then press ENTER to scan for potential flags...")
    print("🔎 Scanning for flag-like patterns (format: XXXX-YYYY-ZZZZ)...")
    time.sleep(0.5)
    matches = search_for_flags(outfile, regex_pattern)

    if matches:
        print(f"\n📌 Found {len(matches)} possible flag(s):")
        for m in matches:
            print(f"   ➡️ {m}")
    else:
        print("\n⚠️ No obvious flags found. Try scanning manually in extracted_strings.txt.")

    print("\n✅ Done! You can inspect extracted_strings.txt further or try other tools like 'hexdump' for deeper analysis.")
    print("🧠 Remember: Only one string matches the official flag format: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()
