#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import json

# === Constants ===
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
CHALLENGE_ID = "06_Hashcat"

# === Detect Validation Mode
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

# === Utilities
def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker.", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def load_unlock_data(project_root):
    unlock_file = os.path.join(project_root, "web_version_admin", SOLO_JSON if get_ctf_mode() == "solo" else GUIDED_JSON)
    try:
        with open(unlock_file, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        entry = unlocks.get(CHALLENGE_ID)
        expected_flag = entry["real_flag"]
        password_map = entry["hash_password_zip_map"]
        passwords = [v["password"] for v in password_map.values()]
        return expected_flag, passwords
    except Exception as e:
        print(f"❌ ERROR: Could not load unlock data: {e}", file=sys.stderr)
        sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def print_progress_bar(length=30, delay=0.02):
    if validation_mode:
        return
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

def extract_zip_files_with_passwords(passwords, segments_dir, extracted_dir, decoded_dir):
    os.makedirs(decoded_dir, exist_ok=True)
    for idx, password in enumerate(passwords, start=1):
        zipfile = os.path.join(segments_dir, f"part{idx}.zip")
        print(f"\n🔑 Unlocking {zipfile} with password: {password}")
        result = subprocess.run(
            ["unzip", "-P", password, zipfile, "-d", extracted_dir],
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
                decode_base64_file(
                    os.path.join(extracted_dir, f),
                    os.path.join(decoded_dir, f"decoded_{f}")
                )

def validate_challenge(script_dir, project_root):
    segments_dir = os.path.join(script_dir, "segments")
    extracted_dir = os.path.join(script_dir, "extracted")
    decoded_dir = os.path.join(script_dir, "decoded_segments")
    assembled_file = os.path.join(script_dir, "assembled_flag.txt")

    expected_flag, passwords = load_unlock_data(project_root)

    print("\n🛠️ [Validation] Using known passwords to unzip files...")
    extract_zip_files_with_passwords(passwords, segments_dir, extracted_dir, decoded_dir)

    print("\n🧩 Assembling candidate flags...")
    candidate_flags = reassemble_flags(decoded_dir, assembled_file)

    if expected_flag in candidate_flags:
        print(f"✅ Validation success: found flag {expected_flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {expected_flag} not found.", file=sys.stderr)
        sys.exit(1)

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
        cracked_passwords = []
        with open(potfile, "r") as pf:
            for line in pf:
                if ':' in line:
                    hash_val, password = line.strip().split(':', 1)
                    cracked_passwords.append(password)
                    print(f"🔓 {hash_val} : {password}")

        pause("\nPress ENTER to extract ZIPs and decode segments...")
        extract_zip_files_with_passwords(cracked_passwords, segments_dir, extracted_dir, decoded_dir)

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
    project_root = find_project_root()

    if validation_mode:
        validate_challenge(script_dir, project_root)
    else:
        student_interactive(script_dir)
