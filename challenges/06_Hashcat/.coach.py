#!/usr/bin/env python3
import sys
import os
import subprocess

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL ASSEMBLER TOOL ===
TOOL_NAME = ".assembler.py"
ASSEMBLER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    parts = ["encoded_segments1.txt", "encoded_segments2.txt", "encoded_segments3.txt"]
    decoded_lines = []

    # 1. Decode each file
    for p in parts:
        if not os.path.exists(p):
            print(f"ERROR: Could not find '{p}'. Did you unzip the segments?", file=sys.stderr)
            sys.exit(1)
        
        # Decode using base64 command
        res = subprocess.run(["base64", "-d", p], capture_output=True, text=True)
        decoded_lines.append(res.stdout.splitlines())

    # 2. Merge (Zip) them together
    print("--- REASSEMBLED FLAGS ---")
    
    if decoded_lines:
        num_candidates = len(decoded_lines[0])
        for i in range(num_candidates):
            segment_pieces = []
            for d in decoded_lines:
                if i < len(d):
                    segment_pieces.append(d[i].strip())
                else:
                    segment_pieces.append("MISSING")
            print("-".join(segment_pieces))

if __name__ == "__main__":
    main()
"""

def create_tool():
    """Writes the assembler script to the CURRENT working directory."""
    with open(TOOL_NAME, "w") as f:
        f.write(ASSEMBLER_SCRIPT_CONTENT)

def cleanup_tool():
    """Removes the assembler script and temp files."""
    if os.path.exists(TOOL_NAME):
        os.remove(TOOL_NAME)
    if os.path.exists("hashcat.potfile"):
        os.remove("hashcat.potfile")
    # Optional: cleanup the unzipped parts if you want a fresh start
    for i in range(1, 4):
        if os.path.exists(f"encoded_segments{i}.txt"):
            os.remove(f"encoded_segments{i}.txt")
    if os.path.exists("flag.txt"):
        os.remove("flag.txt")

def get_ordered_passwords():
    """
    Reads hashcat.potfile to map hashes to passwords, ensuring we return them
    in the order requested by hashes.txt (which matches part1, part2, part3).
    """
    potfile = "hashcat.potfile"
    hashes_file = "hashes.txt"
    passwords = []
    
    # Map Hash -> Password
    cracked = {}
    if os.path.exists(potfile):
        with open(potfile, "r") as f:
            for line in f:
                if ":" in line:
                    h, p = line.strip().split(":", 1)
                    cracked[h] = p
    
    # Retrieve in strict input order
    if os.path.exists(hashes_file):
        with open(hashes_file, "r") as f:
            for line in f:
                h = line.strip()
                passwords.append(cracked.get(h, "unknown"))
    
    # Safety padding
    while len(passwords) < 3:
        passwords.append("unknown")
        
    return passwords

def main():
    bot = Coach("Hashcat ChainCrack")
    
    # Ensure clean slate
    cleanup_tool()
    
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/06_Hashcat"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/06_Hashcat"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's survey the battlefield.\n"
                "Use 'ls -R' (recursive list) to see the segments inside the folder."
            ),
            command_to_display="ls -R"
        )

        # STEP 3: Cracking
        bot.teach_step(
            instruction=(
                "We need to crack the hashes to get the passwords.\n"
                "   `-m 0`           → MD5 Mode\n"
                "   `-a 0`           → Dictionary Attack\n"
                "   `--potfile-path` → Saves cracked passwords locally\n\n"
                "Run the attack:"
            ),
            command_to_display="hashcat -m 0 -a 0 hashes.txt wordlist.txt --potfile-path hashcat.potfile"
        )

        # STEP 4: Reveal
        bot.teach_step(
            instruction=(
                "The passwords are saved in the potfile. Now we reveal them using `--show`.\n"
                "💡 **Tip:** Press **Up Arrow** to recall the command, then add ` --show`."
            ),
            command_to_display="hashcat -m 0 -a 0 hashes.txt wordlist.txt --potfile-path hashcat.potfile --show"
        )

        # === READ LOCAL RESULTS ===
        # The coach needs to know the passwords to validate the unzipping
        p1, p2, p3 = get_ordered_passwords()[:3]
        # ==========================

        # STEP 5: Unlock Part 1
        bot.teach_loop(
            instruction=(
                "**Crucial Lesson:** Hashcat's `--show` output matches the input order.\n"
                "1. The **first line** matches the **first zip** (part1).\n"
                f"2. That password is **{p1}**.\n\n"
                "Use it to unzip Part 1:"
            ),
            command_template=f"unzip -o -P {p1} segments/part1.zip",
            command_prefix="unzip -o -P ",
            command_regex=fr"^unzip -o -P {p1} segments/part1\.zip$",
            clean_files=["encoded_segments1.txt"]
        )

        # STEP 6: Unlock Part 2
        bot.teach_loop(
            instruction=(
                "The **second line** matches **part2.zip**.\n"
                f"The password is **{p2}**.\n\n"
                "Unlock Part 2:"
            ),
            command_template=f"unzip -o -P {p2} segments/part2.zip",
            command_prefix="unzip -o -P ",
            command_regex=fr"^unzip -o -P {p2} segments/part2\.zip$",
            clean_files=["encoded_segments2.txt"]
        )

        # STEP 7: Unlock Part 3
        bot.teach_loop(
            instruction=(
                "And the **third line** matches **part3.zip**.\n"
                f"The password is **{p3}**.\n\n"
                "Unlock Part 3:"
            ),
            command_template=f"unzip -o -P {p3} segments/part3.zip",
            command_prefix="unzip -o -P ",
            command_regex=fr"^unzip -o -P {p3} segments/part3\.zip$",
            clean_files=["encoded_segments3.txt"]
        )

        # STEP 8: Tool Provisioning (The Logic Fix)
        print("\n[Coach] 🧠  The Mission Brief says we need to 'Assemble' the data.")
        print("[Coach] ⚠️   We have three separate files. Combining them by hand is slow.")
        print("[Coach] 📡  I am generating a helper script `.assembler.py` for you now...")
        create_tool()

        bot.teach_step(
            instruction=(
                "I have created `.assembler.py`.\n"
                "**Always inspect code before running it.** Read the script now."
            ),
            command_to_display="cat .assembler.py"
        )

        # STEP 9: Assembly
        bot.teach_loop(
            instruction=(
                "The code looks safe (it decodes Base64 and merges the lines).\n"
                "Run it and save the result to 'flag.txt'."
            ),
            command_template="python3 .assembler.py > flag.txt",
            command_prefix="python3 .assembler.py",
            command_regex=r"^python3 \.assembler\.py > flag\.txt$",
            clean_files=["flag.txt"]
        )

        # STEP 10: Finish
        bot.teach_step(
            instruction=(
                "Success! Read 'flag.txt' to see the reassembled flag."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_tool()

if __name__ == "__main__":
    main()