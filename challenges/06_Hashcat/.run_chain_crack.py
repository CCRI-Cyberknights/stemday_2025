#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
HASHES_FILE = "hashes.txt"
WORDLIST_FILE = "wordlist.txt"
POTFILE = "hashcat.potfile"
SEGMENTS_DIR = "segments"
EXTRACTED_DIR = "extracted"
DECODED_DIR = "decoded_segments"
ASSEMBLED_FILE = "assembled_flag.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

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
                pass

def extract_zip_files_with_passwords(passwords, segments_dir, extracted_dir, decoded_dir):
    os.makedirs(decoded_dir, exist_ok=True)
    for idx, password in enumerate(passwords, start=1):
        zipfile = os.path.join(segments_dir, f"part{idx}.zip")
        print(f"\n{Colors.CYAN}📦 Segment {idx}: {zipfile}{Colors.END}")

        if not os.path.isfile(zipfile):
            print_error(f"ZIP file missing for segment {idx}, skipping.")
            continue

        if not password:
            print_error("No password available for this segment (hash not cracked). Skipping.")
            continue

        print(f"🔑 Unlocking with password: {Colors.BOLD}{password}{Colors.END}")
        result = subprocess.run(
            ["unzip", "-o", "-P", password, zipfile, "-d", extracted_dir],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_error(f"Failed to unzip {zipfile}")
            continue

        print_success(f"Unzipped {zipfile} successfully.")
        flatten_extracted_dir(extracted_dir)

        # Process Extracted Files
        for f in os.listdir(extracted_dir):
            if f.startswith("encoded_"):
                encoded_path = os.path.join(extracted_dir, f)
                decoded_path = os.path.join(decoded_dir, f"decoded_" + f)

                print(f"📦 Encoded Base64 contents from {f}:")
                print("-" * 30)
                with open(encoded_path, "r", encoding="utf-8", errors="replace") as ef:
                    print(f"{Colors.YELLOW}{ef.read().strip()}{Colors.END}")
                print("-" * 30)

                decoded = decode_base64_file(encoded_path, decoded_path)

                if decoded:
                    print(f"\n🧾 Decoded contents from {f}:")
                    print("-" * 30)
                    print(f"{Colors.GREEN}{decoded}{Colors.END}")
                    print("-" * 30)
                else:
                    print_error("Failed to decode base64 content.")

        require_input("Type 'next' to continue to the next ZIP: ", "next")

def reassemble_flags(decoded_dir, assembled_file):
    decoded_files = sorted(
        [f for f in os.listdir(decoded_dir) if f.endswith(".txt")],
        key=lambda x: int("".join(filter(str.isdigit, x)))
    )
    assembled_lines = []
    try:
        with open(assembled_file, "w", encoding="utf-8") as out_f:
            # We assume 5 lines per file
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
        print_error(f"Flag reassembly failed: {e}")
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

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hashes_path = get_path(HASHES_FILE)
    wordlist_path = get_path(WORDLIST_FILE)
    potfile_path = get_path(POTFILE)
    segments_path = get_path(SEGMENTS_DIR)
    extracted_path = get_path(EXTRACTED_DIR)
    decoded_path = get_path(DECODED_DIR)
    assembled_path = get_path(ASSEMBLED_FILE)

    # 2. Mission Briefing
    header("🔓 Hashcat ChainCrack Demo")
    
    print(f"📂 Hashes to crack:     {Colors.BOLD}{HASHES_FILE}{Colors.END}")
    print(f"📖 Wordlist to use:     {Colors.BOLD}{WORDLIST_FILE}{Colors.END}")
    print(f"📦 Encrypted segments:  {Colors.BOLD}segments/part*.zip{Colors.END}\n")
    print("🎯 Goal: Crack hashes, unlock ZIPs, decode Base64, assemble the real CCRI flag.\n")
    
    print(f"{Colors.CYAN}💡 Scenario:{Colors.END}")
    print("   ➤ Each hash unlocks one ZIP file containing a piece of the puzzle.")
    print("   ➤ Each ZIP contains a Base64-encoded text segment.")
    print("   ➤ When all segments are decoded and combined, they form multiple candidate flags.")
    print("   ➤ Only ONE of those flags is the true CCRI-AAAA-1111 flag.\n")
    
    require_input("Type 'ready' when you're ready to see the commands behind this challenge: ", "ready")

    if not os.path.isfile(hashes_path) or not os.path.isfile(wordlist_path):
        print_error("Required files hashes.txt or wordlist.txt are missing.")
        sys.exit(1)

    if not os.path.isdir(segments_path):
        print_error("Segments folder missing.")
        sys.exit(1)

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("Step 1: Use Hashcat to crack the hashes.\n")
    print(f"   {Colors.GREEN}hashcat -m 0 -a 0 {HASHES_FILE} {WORDLIST_FILE} ...{Colors.END}\n")
    print("   -m 0            → Hash mode 0 (raw MD5)")
    print("   -a 0            → Attack mode 0 (straight wordlist attack)")
    
    print("\nStep 2: Use each cracked password to unlock a ZIP segment:")
    print(f"   {Colors.GREEN}unzip -o -P [password] partN.zip -d extracted/{Colors.END}")
    
    print("\nStep 3: Decode Base64-encoded message segments:")
    print(f"   {Colors.GREEN}base64 --decode encoded_X.txt > decoded.txt{Colors.END}")
    
    print("\nStep 4: Reassemble decoded pieces into candidate flags.")
    
    require_input("Type 'start' when you're ready to begin the chain-cracking process: ", "start")

    # 4. Execution Phase
    print_info("Cleaning previous results...")
    for path in [potfile_path, assembled_path]:
        if os.path.exists(path): os.remove(path)
    for d in [extracted_path, decoded_path]:
        if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(extracted_path, exist_ok=True)
    os.makedirs(decoded_path, exist_ok=True)

    header("🛠️ Running Hashcat...")
    spinner("Cracking hashes")
    run_hashcat(hashes_path, wordlist_path, potfile_path)

    print("\n[✅] Cracked hashes:")
    cracked_passwords_by_hash = {}
    if not os.path.isfile(potfile_path):
        print_error("No potfile created. Hashcat failed.")
    else:
        with open(potfile_path, "r", encoding="utf-8", errors="replace") as pf:
            for line in pf:
                if ':' in line:
                    hash_val, password = line.strip().split(':', 1)
                    cracked_passwords_by_hash[hash_val] = password
                    print(f"🔓 {hash_val} : {Colors.BOLD}{password}{Colors.END}")

    require_input("\nType 'map' to map cracked passwords to ZIP segments: ", "map")

    ordered_passwords = []
    with open(hashes_path, "r", encoding="utf-8", errors="replace") as hf:
        for line in hf:
            hash_val = line.strip()
            if not hash_val: continue
            ordered_passwords.append(cracked_passwords_by_hash.get(hash_val))

    print("\n📦 Using cracked passwords to unlock ZIP segments...")
    extract_zip_files_with_passwords(ordered_passwords, segments_path, extracted_path, decoded_path)

    print("\n🧩 Assembling candidate flags from decoded pieces...")
    candidate_flags = reassemble_flags(decoded_path, assembled_path)

    if not candidate_flags:
        print_error("No flags could be assembled.")
    else:
        header("🎯 Candidate Flags")
        for flag in candidate_flags:
            print(f"- {Colors.BOLD}{flag}{Colors.END}")

        print(f"\n✅ Flags saved to: {Colors.BOLD}{ASSEMBLED_FILE}{Colors.END}")
        print(f"{Colors.CYAN}🧠 Only ONE candidate will match the true CCRI-AAAA-1111 flag pattern used in the challenge story.{Colors.END}")

    pause("\n🎉 Press ENTER to exit...")

if __name__ == "__main__":
    main()