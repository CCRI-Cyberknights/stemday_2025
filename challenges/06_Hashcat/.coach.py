#!/usr/bin/env python3
import sys
import os
import subprocess

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
# Now heavily commented for educational transparency
CHAIN_BREAKER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# This script automates the manual process of cracking, unzipping, and decoding.

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    hashes_file = os.path.join(base_dir, "hashes.txt")
    wordlist = os.path.join(base_dir, "wordlist.txt")
    potfile = os.path.join(base_dir, "hashcat.potfile")
    segments_dir = os.path.join(base_dir, "segments")
    extracted_dir = os.path.join(base_dir, "extracted")
    assembled_file = os.path.join(base_dir, "assembled_flag.txt")

    # Clean up previous runs
    if os.path.exists(extracted_dir): shutil.rmtree(extracted_dir)
    os.makedirs(extracted_dir, exist_ok=True)

    print("--- STEP 1: AUTOMATED CRACKING ---")
    print(f"Running Hashcat on {hashes_file}...")
    
    # We use subprocess to run the 'hashcat' command just like a human would
    subprocess.run(
        ["hashcat", "-m", "0", "-a", "0", hashes_file, wordlist, "--potfile-path", potfile, "--force"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # Read the results (the 'potfile' contains hash:password)
    cracked_passwords = {}
    if os.path.exists(potfile):
        with open(potfile, "r") as f:
            for line in f:
                if ":" in line:
                    h, p = line.strip().split(":", 1)
                    cracked_passwords[h] = p

    print(f"Successfully cracked {len(cracked_passwords)} passwords.\n")

    print("--- STEP 2: CHAIN UNZIPPING ---")
    # We read the hashes in order, find the password, and unzip the corresponding file
    with open(hashes_file, "r") as f:
        hashes = [line.strip() for line in f if line.strip()]

    decoded_fragments = []

    for i, h in enumerate(hashes):
        part_num = i + 1
        password = cracked_passwords.get(h)
        zip_file = os.path.join(segments_dir, f"part{part_num}.zip")

        if password:
            print(f"Unlocking part{part_num}.zip with password: '{password}'")
            # Run 'unzip' using the cracked password
            subprocess.run(
                ["unzip", "-o", "-P", password, zip_file, "-d", extracted_dir],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            
            # Find the encoded text file inside
            encoded_file = os.path.join(extracted_dir, f"encoded_{part_num}.txt")
            if os.path.exists(encoded_file):
                # Run 'base64 -d' to decode it
                res = subprocess.run(["base64", "-d", encoded_file], capture_output=True, text=True)
                decoded_fragments.append(res.stdout.strip())
        else:
            print(f"Could not crack password for part{part_num}.zip")
            decoded_fragments.append("MISSING")

    print("\n--- STEP 3: REASSEMBLY ---")
    # Combine the fragments into the final flag
    final_flag = "-".join(decoded_fragments)
    
    with open(assembled_file, "w") as f:
        f.write(final_flag + "\n")
    
    print(f"Flag assembled and saved to: {assembled_file}")

if __name__ == "__main__":
    main()
"""

def create_tool():
    tool_path = os.path.join(os.path.dirname(__file__), ".chain_breaker.py")
    with open(tool_path, "w") as f:
        f.write(CHAIN_BREAKER_SCRIPT_CONTENT)
    return tool_path

def cleanup_tool():
    tool_path = os.path.join(os.path.dirname(__file__), ".chain_breaker.py")
    if os.path.exists(tool_path):
        os.remove(tool_path)

def main():
    bot = Coach("Hashcat Chain Reaction")
    bot.start()
    create_tool()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/06_Hashcat"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "We have 'hashes.txt' (targets), 'wordlist.txt' (ammo), and a 'segments' folder.\n"
                "Use 'ls -R' to see the full recursive structure."
            ),
            command_to_display="ls -R"
        )

        # STEP 3: Understanding the Logic
        bot.teach_step(
            instruction=(
                "This attack is a chain reaction:\n"
                "1. Crack MD5 hash -> Get Password.\n"
                "2. Use Password -> Unlock ZIP.\n"
                "3. Decode Base64 -> Get Flag Fragment.\n"
                "4. Repeat for all 5 segments.\n\n"
                "Doing this manually is slow. We need automation.\n"
                "Type 'Understood' to proceed."
            ),
            command_to_display="echo Understood"
        )

        # STEP 4: Code Transparency (NEW STEP)
        bot.teach_step(
            instruction=(
                "We created a script called '.chain_breaker.py' to automate this.\n"
                "**Never run a script without knowing what it does.**\n\n"
                "Read the source code. Look for `subprocess.run`. That is how Python runs Linux commands like 'hashcat' and 'unzip' for you."
            ),
            command_to_display="cat .chain_breaker.py"
        )

        # STEP 5: Run the Tool
        bot.teach_step(
            instruction=(
                "Now that you trust the code, run the chain breaker!"
            ),
            command_to_display="python3 .chain_breaker.py"
        )

        # STEP 6: Verification
        bot.teach_step(
            instruction=(
                "The script assembled the pieces into 'assembled_flag.txt'.\n"
                "Read the file to get your flag."
            ),
            command_to_display="cat assembled_flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_tool()

if __name__ == "__main__":
    main()