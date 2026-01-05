#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import base64

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
HASHES_FILE = "hashes.txt"
WORDLIST_FILE = "wordlist.txt"
POTFILE = "hashcat.potfile"
SEGMENTS_DIR = "segments"
ASSEMBLED_FILE = "flag.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

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

def internal_assembly_logic():
    """
    Reads the extracted files, decodes them, and merges them in memory.
    Returns a list of assembled flag strings.
    """
    parts = ["encoded_segments1.txt", "encoded_segments2.txt", "encoded_segments3.txt"]
    decoded_columns = []

    # 1. Read and Decode each part
    for p in parts:
        if not os.path.exists(p):
            return []
        
        try:
            with open(p, "rb") as f:
                raw_data = f.read().strip()
            # Decode Base64 in memory
            decoded_text = base64.b64decode(raw_data).decode('utf-8')
            decoded_columns.append(decoded_text.splitlines())
        except Exception:
            return []

    # 2. Stitch columns together
    results = []
    if decoded_columns:
        # Assuming all columns have the same number of lines
        num_rows = len(decoded_columns[0])
        for i in range(num_rows):
            row_pieces = []
            for col in decoded_columns:
                if i < len(col):
                    row_pieces.append(col[i].strip())
                else:
                    row_pieces.append("???")
            results.append("-".join(row_pieces))
            
    return results

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    hashes_path = get_path(HASHES_FILE)
    wordlist_path = get_path(WORDLIST_FILE)
    potfile_path = get_path(POTFILE)
    segments_path = get_path(SEGMENTS_DIR)

    # 2. Mission Briefing
    header("🔓 Hashcat ChainCrack Demo")
    
    print(f"📂 Hashes to crack:     {Colors.BOLD}{HASHES_FILE}{Colors.END}")
    print(f"📦 Encrypted segments:  {Colors.BOLD}segments/part*.zip{Colors.END}\n")
    print("🎯 Goal: Crack hashes, unlock ZIPs, and assemble the hidden flag.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Lock:** Three separate ZIP files, locked with different passwords.")
    print("   ➤ **The Keys:** Passwords hidden behind MD5 hashes.")
    print("   ➤ **The Strategy:** Crack -> Unlock -> Assemble.")
    print("   ➤ **The Requirement:** You must chain multiple tools together.\n")
    
    require_input("Type 'ready' to initialize the attack chain: ", "ready")

    if not os.path.isfile(hashes_path) or not os.path.isfile(wordlist_path):
        print_error("Required files hashes.txt or wordlist.txt are missing.")
        sys.exit(1)

    # 3. Algorithm Explanation
    header("🛠️ Behind the Scenes")
    print("This script simulates a complex automation pipeline:\n")
    
    print("1. **Crack**: It calls `hashcat` to recover the passwords from MD5 hashes.")
    print("2. **Unlock**: It uses those passwords to `unzip` the archive segments.")
    print("3. **Assemble**: It runs an internal algorithm to stitching the files.")
    
    print(f"\n{Colors.CYAN}🧩 The Assembly Logic:{Colors.END}")
    print("   The zips contain fragments of data. Manually pasting them together is slow.")
    print("   This script will load all three text files into memory, decode them from")
    print("   Base64, and align them line-by-line to reconstruct the flag.\n")
    
    require_input("Type 'start' to begin the chain reaction: ", "start")

    # 4. Execution Phase - Step 1: Crack
    # Clean previous run
    if os.path.exists(potfile_path): os.remove(potfile_path)
    
    print(f"\n{Colors.CYAN}🔨 [Phase 1] Cracking Hashes...{Colors.END}")
    spinner("Running Hashcat")
    run_hashcat(hashes_path, wordlist_path, potfile_path)

    # Map hashes to passwords
    cracked_map = {}
    if os.path.exists(potfile_path):
        with open(potfile_path, "r") as f:
            for line in f:
                if ":" in line:
                    h, p = line.strip().split(":", 1)
                    cracked_map[h] = p
    else:
        print_error("Hashcat failed to create a potfile.")
        sys.exit(1)

    # Get ordered passwords based on hashes.txt
    ordered_passwords = []
    with open(hashes_path, "r") as f:
        for line in f:
            h = line.strip()
            if h: ordered_passwords.append(cracked_map.get(h))
            
    print_success("Hashes cracked.")
    for i, pw in enumerate(ordered_passwords):
        print(f"   Hashes #{i+1} -> Password: {Colors.BOLD}{pw}{Colors.END}")
    
    time.sleep(1)

    # 5. Execution Phase - Step 2: Unlock
    print(f"\n{Colors.CYAN}🔓 [Phase 2] Unlocking Archives...{Colors.END}")
    
    # Clean up old extraction
    for f in os.listdir("."):
        if f.startswith("encoded_segments"):
            os.remove(f)

    for i, pw in enumerate(ordered_passwords):
        if not pw:
            print_error(f"   Skipping Part {i+1} (Password unknown)")
            continue
            
        zip_file = os.path.join(segments_path, f"part{i+1}.zip")
        print(f"   Unzipping {os.path.basename(zip_file)} with '{pw}'...", end="")
        
        res = subprocess.run(
            ["unzip", "-o", "-P", pw, zip_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if res.returncode == 0:
            print(f" {Colors.GREEN}OK{Colors.END}")
        else:
            print(f" {Colors.RED}FAILED{Colors.END}")
            
    time.sleep(1)

    # 6. Execution Phase - Step 3: Assemble (Internal)
    print(f"\n{Colors.CYAN}🧩 [Phase 3] Assembling Fragments (Internal Logic)...{Colors.END}")
    spinner("Processing in memory")
    
    candidate_flags = internal_assembly_logic()
    
    if not candidate_flags:
        print_error("Assembly failed. Are the ZIP files empty?")
    else:
        # Save to file
        with open(ASSEMBLED_FILE, "w") as f:
            for flag in candidate_flags:
                f.write(flag + "\n")
            
        print_success("Assembly complete.")
        print("-" * 40)
        for flag in candidate_flags:
            print(f"{Colors.BOLD}{flag}{Colors.END}")
        print("-" * 40 + "\n")
        
        print(f"✅ Flags saved to: {Colors.BOLD}{ASSEMBLED_FILE}{Colors.END}")
        print(f"{Colors.CYAN}🧠 Hint: Look for the one matching CCRI-AAAA-1111.{Colors.END}")

    pause("\n🎉 Press ENTER to exit...")

if __name__ == "__main__":
    main()