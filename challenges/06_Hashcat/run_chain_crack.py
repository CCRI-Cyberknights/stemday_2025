#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def print_progress_bar(length=30, delay=0.02):
    for _ in range(length):
        print("█", end="", flush=True)
        time.sleep(delay)
    print()

def decode_base64_file(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        result = subprocess.run(
            ["base64", "--decode", input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        with open(output_path, "w") as f_out:
            f_out.write(result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def flatten_extracted_dir(extracted_dir):
    for root, dirs, files in os.walk(extracted_dir):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(extracted_dir, f)
            if src != dst:
                try:
                    os.rename(src, dst)
                except FileExistsError:
                    os.remove(dst)
                    os.rename(src, dst)
        for d in dirs:
            try:
                os.rmdir(os.path.join(root, d))
            except OSError:
                pass

def extract_zip_files_with_passwords(passwords, segments_dir, extracted_dir, decoded_dir):
    os.makedirs(decoded_dir, exist_ok=True)
    for idx, password in enumerate(passwords, start=1):
        zipfile = os.path.join(segments_dir, f"part{idx}.zip")
        print(f"\n🔑 Unlocking {zipfile} with password: {password}")
        result = subprocess.run(
            ["unzip", "-o", "-P", password, zipfile, "-d", extracted_dir],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to unzip {zipfile} with password '{password}'", file=sys.stderr)
            print(f"📄 unzip error: {result.stderr.strip()}", file=sys.stderr)
            continue

        print(f"✅ Unzipped {zipfile} successfully.")
        flatten_extracted_dir(extracted_dir)

        for f in os.listdir(extracted_dir):
            if f.startswith("encoded_"):
                encoded_path = os.path.join(extracted_dir, f)
                decoded_path = os.path.join(decoded_dir, f"decoded_" + f)

                print(f"\n📦 Encoded Base64 contents from {f}:")
                print("--------------------------")
                with open(encoded_path, "r") as ef:
                    print(ef.read().strip())
                print("--------------------------")

                decoded = decode_base64_file(encoded_path, decoded_path)

                if decoded:
                    print(f"\n🧾 Decoded contents from {f}:")
                    print("--------------------------")
                    print(decoded)
                    print("--------------------------")
                else:
                    print("❌ Failed to decode base64 content.")

        pause("Press ENTER to continue to the next ZIP...")

def reassemble_flags(decoded_dir, assembled_file):
    decoded_files = sorted(
        [f for f in os.listdir(decoded_dir) if f.endswith(".txt")],
        key=lambda x: int("".join(filter(str.isdigit, x)))
    )
    assembled_lines = []
    try:
        with open(assembled_file, "w") as out_f:
            for i in range(5):
                parts = []
                for f in decoded_files:
                    lines = open(os.path.join(decoded_dir, f)).readlines()
                    parts.append(lines[i].strip() if i < len(lines) else "MISSING")
                flag = "-".join(parts)
                assembled_lines.append(flag)
                out_f.write(flag + "\n")
        return assembled_lines
    except Exception as e:
        print(f"❌ ERROR during flag reassembly: {e}", file=sys.stderr)
        return []

def run_hashcat(hashes_file, wordlist_file, potfile):
    subprocess.run(
        ["hashcat", "-m", "0", "-a", "0", hashes_file, wordlist_file,
         "--potfile-path", potfile, "--force"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def student_interactive(script_dir):
    hashes_file = os.path.join(script_dir, "hashes.txt")
    wordlist_file = os.path.join(script_dir, "wordlist.txt")
    potfile = os.path.join(script_dir, "hashcat.potfile")
    segments_dir = os.path.join(script_dir, "segments")
    extracted_dir = os.path.join(script_dir, "extracted")
    decoded_dir = os.path.join(script_dir, "decoded_segments")
    assembled_file = os.path.join(script_dir, "assembled_flag.txt")

    try:
        clear_screen()
        print("🔓 Hashcat ChainCrack Demo")
        print("===============================\n")
        print("📂 Hashes to crack:     hashes.txt")
        print("📖 Wordlist to use:     wordlist.txt")
        print("📦 Encrypted segments:  segments/part*.zip\n")
        print("🎯 Goal: Crack hashes, unlock ZIPs, decode Base64, assemble flag.\n")
        pause()

        if not os.path.isfile(hashes_file) or not os.path.isfile(wordlist_file):
            print("❌ ERROR: Required files hashes.txt or wordlist.txt are missing.")
            pause("Press ENTER to close...")
            return

        if not os.path.isdir(segments_dir):
            print("❌ ERROR: Segments folder missing.")
            pause("Press ENTER to close...")
            return

        print("\n[🧹] Cleaning previous results...")
        for path in [potfile, assembled_file]:
            if os.path.exists(path):
                os.remove(path)
        for d in [extracted_dir, decoded_dir]:
            if os.path.exists(d):
                subprocess.run(["rm", "-rf", d])
        os.makedirs(extracted_dir, exist_ok=True)
        os.makedirs(decoded_dir, exist_ok=True)

        print("\n🛠️ Running Hashcat...")
        pause("Press ENTER to continue...")
        run_hashcat(hashes_file, wordlist_file, potfile)

        print("\n[✅] Cracked hashes:")
        cracked_passwords_by_hash = {}
        with open(potfile, "r") as pf:
            for line in pf:
                if ':' in line:
                    hash_val, password = line.strip().split(':', 1)
                    cracked_passwords_by_hash[hash_val] = password
                    print(f"🔓 {hash_val} : {password}")

        pause("\nPress ENTER to extract ZIPs and decode segments...")
        ordered_passwords = []
        with open(hashes_file, "r") as hf:
            for line in hf:
                hash_val = line.strip()
                pw = cracked_passwords_by_hash.get(hash_val)
                if pw:
                    ordered_passwords.append(pw)
                else:
                    ordered_passwords.append(None)  # No match

        extract_zip_files_with_passwords(ordered_passwords, segments_dir, extracted_dir, decoded_dir)


        print("\n🧩 Assembling candidate flags...")
        print_progress_bar()
        candidate_flags = reassemble_flags(decoded_dir, assembled_file)
        print("\n🎯 Candidate Flags:")
        for flag in candidate_flags:
            print(f"- {flag}")

        print(f"\n✅ Flags saved to: {assembled_file}")
        pause("\n🎉 Press ENTER to exit...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        pause("\n💥 Press ENTER to exit after error...")

if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(__file__))
    student_interactive(script_dir)
