#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def require_input(prompt, expected):
    """
    Pauses and requires the user to type a specific word (case-insensitive) to continue.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

def progress_bar(length=30, delay=0.03):
    for _ in range(length):
        print("█", end="", flush=True)
        time.sleep(delay)
    print()

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

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    zip_file = os.path.join(script_dir, "secret.zip")
    wordlist = os.path.join(script_dir, "wordlist.txt")
    b64_file = os.path.join(script_dir, "message_encoded.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")

    clear_screen()
    print("🔓 ZIP Password Cracking Challenge")
    print("======================================\n")
    print("🎯 Goal: Crack the password, extract the archive, and decode the hidden flag.\n")
    print("💡 Scenario:")
    print("   ➤ CryptKeepers has locked important data inside an encrypted ZIP archive.")
    print("   ➤ You recovered a wordlist of possible passwords.")
    print("   ➤ Your mission: try each password until the archive opens, then decode the contents.\n")
    
    require_input("Type 'ready' when you're ready to see how this works behind the scenes: ", "ready")

    if not os.path.isfile(zip_file) or not os.path.isfile(wordlist):
        print("❌ ERROR: Missing zip file or wordlist.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("Step 1: Dictionary attack against a protected ZIP file.\n")
    print("For each candidate password in wordlist.txt, we run a command like:\n")
    print(f"   unzip -P [password] -t {os.path.basename(zip_file)}\n")
    print("🔍 Command breakdown:")
    print("   unzip                → Tool for working with ZIP archives")
    print("   -P [password]        → Use this password to try to unlock the archive")
    print("   -t                   → 'Test' the ZIP file without fully extracting it")
    print(f"   {os.path.basename(zip_file):<21}→ The encrypted archive we captured\n")
    print("If the test reports 'OK', we know we found the correct password.\n")
    print("Step 2: Once we have the password, we extract the archive.\n")
    print(f"   unzip -o -P [password] {os.path.basename(zip_file)} -d .\n")
    print("   -o    → Overwrite any existing files without asking")
    print("   -d .  → Extract into the current directory\n")
    print("Step 3: Inside the archive is a Base64-encoded message.\n")
    print("   base64 --decode message_encoded.txt > decoded_output.txt\n")
    print("   base64         → Base64 encoder/decoder tool")
    print("   --decode       → Convert encoded text back to original")
    print("   message_encoded.txt → Encoded message from the ZIP")
    print("   > decoded_output.txt → Save the decoded message to a file\n")
    
    require_input("Type 'start' when you're ready to begin the cracking process: ", "start")

    clear_screen()
    print("🔍 Beginning password cracking...\n")
    print("📁 Wordlist:", os.path.basename(wordlist))
    print("📦 Target ZIP:", os.path.basename(zip_file), "\n")
    print("⏳ Launching dictionary attack...\n")
    progress_bar(length=20, delay=0.04)

    found = False
    password = None

    with open(wordlist, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            pw = line.strip()
            if not pw:
                continue
            print(f"\r[🔐] Trying password: {pw:<20}", end="", flush=True)
            time.sleep(0.05)

            result = subprocess.run(
                ["unzip", "-P", pw, "-t", zip_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if "OK" in result.stdout:
                print(f"\n✅ Password found: {pw}")
                password = pw
                found = True
                break

    if not found:
        print("\n❌ Password not found in wordlist.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    # === Extraction Prompt ===
    while True:
        proceed = input("\n📦 Extract and decode the message now? (yes/no): ").strip().lower()
        if proceed == "yes":
            break
        elif proceed == "no":
            print("\n👋 Exiting without extracting.")
            pause("Press ENTER to close this terminal...")
            return
        else:
            print("   ❌ Please type 'yes' or 'no'.")

    print("\n📦 Extracting archive contents...\n")
    spinner("Extracting files")

    subprocess.run(["unzip", "-o", "-P", password, zip_file, "-d", script_dir],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(b64_file):
        print("❌ ERROR: Extraction failed — missing Base64 message.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print("📄 Extracted Base64 Message:")
    print("-------------------------------")
    with open(b64_file, "r", encoding="utf-8", errors="replace") as f:
        print(f.read())
    print("-------------------------------\n")

    # === Decode Prompt ===
    while True:
        decode = input("🔎 Decode the message now? (yes/no): ").strip().lower()
        if decode == "yes":
            break
        elif decode == "no":
            print("\n👋 Exiting without decoding.")
            pause("Press ENTER to close this terminal...")
            return
        else:
            print("   ❌ Please type 'yes' or 'no'.\n")

    print("\n⏳ Decoding message with Base64...\n")
    progress_bar(length=25, delay=0.03)

    # === Decode Base64 ===
    result = subprocess.run(["base64", "--decode", b64_file],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)

    if result.returncode != 0:
        print("❌ Decoding failed.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    decoded = result.stdout.strip()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(decoded + "\n")

    print("\n🧾 Decoded Message:")
    print("-------------------------------")
    print(decoded)
    print("-------------------------------\n")
    print(f"💾 Saved to: {output_file}")
    print("🧠 Look for a flag like: CCRI-AAAA-1111\n")
    pause("Press ENTER to close this terminal...")

# === Entry Point ===
if __name__ == "__main__":
    main()