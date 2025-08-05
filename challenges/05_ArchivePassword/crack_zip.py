#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def progress_bar(length=30, delay=0.03):
    for _ in range(length):
        print("█", end="", flush=True)
        time.sleep(delay)
    print()

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    zip_file = os.path.join(script_dir, "secret.zip")
    wordlist = os.path.join(script_dir, "wordlist.txt")
    output_file = os.path.join(script_dir, "decoded_output.txt")
    b64_file = os.path.join(script_dir, "message_encoded.txt")

    clear_screen()
    print("🔓 ZIP Password Cracking Challenge")
    print("======================================\n")
    print("🎯 Goal: Crack the password, extract the archive, and decode the hidden flag.")
    pause()

    if not os.path.isfile(zip_file) or not os.path.isfile(wordlist):
        print("❌ Missing zip file or wordlist.")
        pause()
        sys.exit(1)

    print("🔍 Beginning password cracking...\n")
    found = False
    password = None

    with open(wordlist, "r") as f:
        for line in f:
            pw = line.strip()
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
        pause()
        sys.exit(1)

    proceed = input("\nDo you want to extract and decode the message now? [Y/n] ").strip().lower()
    if proceed == "n":
        return

    subprocess.run(["unzip", "-P", password, zip_file, "-d", script_dir],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.isfile(b64_file):
        print("❌ Extraction failed: missing Base64 message.")
        pause()
        sys.exit(1)

    print("\n📄 Extracted Base64 Message:")
    print("-------------------------------")
    with open(b64_file, "r") as f:
        print(f.read())
    print("-------------------------------\n")

    decode = input("Decode the message now? [Y/n] ").strip().lower()
    if decode == "n":
        return

    result = subprocess.run(["base64", "--decode", b64_file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("❌ Decoding failed.")
        pause()
        sys.exit(1)

    decoded = result.stdout.strip()
    with open(output_file, "w") as f:
        f.write(decoded + "\n")

    print("\n🧾 Decoded Message:")
    print("-------------------------------")
    print(decoded)
    print("-------------------------------\n")
    print(f"💾 Saved to: {output_file}")
    print("🧠 Look for a flag like: CCRI-AAAA-1111")
    pause()

if __name__ == "__main__":
    main()
