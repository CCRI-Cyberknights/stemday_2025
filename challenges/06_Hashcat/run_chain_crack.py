#!/usr/bin/env python3
import os
import sys
import subprocess
import time

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

def print_progress_bar(length=30, delay=0.02):
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

# === Helpers ===
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
        with open(output_path, "w", encoding="utf-8") as f_out:
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
                # Directory not empty or other issue; ignore.
                pass

def extract_zip_files_with_passwords(passwords, segments_dir, extracted_dir, decoded_dir):
    os.makedirs(decoded_dir, exist_ok=True)
    for idx, password in enumerate(passwords, start=1):
        zipfile = os.path.join(segments_dir, f"part{idx}.zip")
        print(f"\n📦 Segment {idx}: {zipfile}")

        if not os.path.isfile(zipfile):
            print(f"⚠️ ZIP file missing for segment {idx}, skipping.")
            continue

        if not password:
            print("❌ No password available for this segment (hash not cracked). Skipping.")
            continue

        print(f"🔑 Unlocking with password: {password}")
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
                with open(encoded_path, "r", encoding="utf-8", errors="replace") as ef:
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

        pause_nonempty("Type anything, then press ENTER to continue to the next ZIP...")

def reassemble_flags(decoded_dir, assembled_file):
    decoded_files = sorted(
        [f for f in os.listdir(decoded_dir) if f.endswith(".txt")],
        key=lambda x: int("".join(filter(str.isdigit, x)))
    )
    assembled_lines = []
    try:
        with open(assembled_file, "w", encoding="utf-8") as out_f:
            # Assume each decoded file contains multiple lines,
            # with each line representing a piece of a candidate flag.
            for i in range(5):
                parts = []
                for f in decoded_files:
                    with open(os.path.join(decoded_dir, f), encoding="utf-8") as seg_f:
                        lines = seg_f.readlines()
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
        [
            "hashcat", "-m", "0", "-a", "0",
            hashes_file, wordlist_file,
            "--potfile-path", potfile, "--force"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# === Main Student Flow ===
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
        print("🎯 Goal: Crack hashes, unlock ZIPs, decode Base64, assemble the real CCRI flag.\n")
        print("💡 Scenario:")
        print("   ➤ Each hash unlocks one ZIP file containing a piece of the puzzle.")
        print("   ➤ Each ZIP contains a Base64-encoded text segment.")
        print("   ➤ When all segments are decoded and combined, they form multiple candidate flags.")
        print("   ➤ Only ONE of those flags is the true CCRI-AAAA-1111 flag.\n")
        pause_nonempty("Type 'ready' when you're ready to see the commands behind this challenge: ")

        if not os.path.isfile(hashes_file) or not os.path.isfile(wordlist_file):
            print("❌ ERROR: Required files hashes.txt or wordlist.txt are missing.")
            pause("Press ENTER to close...")
            return

        if not os.path.isdir(segments_dir):
            print("❌ ERROR: Segments folder missing.")
            pause("Press ENTER to close...")
            return

        clear_screen()
        print("🛠️ Behind the Scenes")
        print("---------------------------")
        print("Step 1: Use Hashcat to crack the hashes.\n")
        print("   Command (conceptually):")
        print(f"     hashcat -m 0 -a 0 {os.path.basename(hashes_file)} {os.path.basename(wordlist_file)} \\")
        print(f"       --potfile-path {os.path.basename(potfile)} --force\n")
        print("   -m 0            → Hash mode 0 (raw MD5 in this challenge)")
        print("   -a 0            → Attack mode 0 (straight wordlist attack)")
        print("   hashes.txt      → File containing hashes to crack")
        print("   wordlist.txt    → Candidate passwords to test")
        print("   --potfile-path  → Where cracked hash:password pairs are stored\n")
        print("Step 2: Use each cracked password to unlock a ZIP segment:\n")
        print("   unzip -o -P [password] partN.zip -d extracted/\n")
        print("   -P [password]   → Use this password for the encrypted ZIP")
        print("   -o              → Overwrite existing files without prompting")
        print("   -d extracted/   → Extract into the 'extracted' directory\n")
        print("Step 3: Decode Base64-encoded message segments:\n")
        print("   base64 --decode encoded_X.txt > decoded_segments/decoded_encoded_X.txt\n")
        print("Step 4: Reassemble the decoded pieces into candidate flags.")
        print("   Each decoded file contributes one part of each candidate flag,")
        print("   and we join the pieces together with '-' separators.\n")
        pause_nonempty("Type 'start' when you're ready to begin the chain-cracking process: ")

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
        print_progress_bar(length=20, delay=0.03)
        run_hashcat(hashes_file, wordlist_file, potfile)

        print("\n[✅] Cracked hashes:")
        cracked_passwords_by_hash = {}
        if not os.path.isfile(potfile):
            print("⚠️ No potfile created. Hashcat may not have cracked any hashes.")
        else:
            with open(potfile, "r", encoding="utf-8", errors="replace") as pf:
                for line in pf:
                    if ':' in line:
                        hash_val, password = line.strip().split(':', 1)
                        cracked_passwords_by_hash[hash_val] = password
                        print(f"🔓 {hash_val} : {password}")

        pause_nonempty("\nType anything, then press ENTER to map cracked passwords to ZIP segments...")

        ordered_passwords = []
        with open(hashes_file, "r", encoding="utf-8", errors="replace") as hf:
            for line in hf:
                hash_val = line.strip()
                if not hash_val:
                    continue
                pw = cracked_passwords_by_hash.get(hash_val)
                if pw:
                    ordered_passwords.append(pw)
                else:
                    ordered_passwords.append(None)  # No match for this hash

        print("\n📦 Using cracked passwords to unlock ZIP segments...")
        spinner("Unlocking segments")
        extract_zip_files_with_passwords(ordered_passwords, segments_dir, extracted_dir, decoded_dir)

        print("\n🧩 Assembling candidate flags from decoded pieces...")
        print_progress_bar()
        candidate_flags = reassemble_flags(decoded_dir, assembled_file)

        if not candidate_flags:
            print("⚠️ No flags could be assembled. Check decoded_segments/ for issues.")
        else:
            print("\n🎯 Candidate Flags:")
            for flag in candidate_flags:
                print(f"- {flag}")

            print(f"\n✅ Flags saved to: {assembled_file}")
            print("🧠 Only ONE candidate will match the true CCRI-AAAA-1111 flag pattern used in the challenge story.")

        pause("\n🎉 Press ENTER to exit...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        pause("\n💥 Press ENTER to exit after error...")

if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(__file__))
    student_interactive(script_dir)
