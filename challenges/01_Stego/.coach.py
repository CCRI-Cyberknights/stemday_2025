#!/usr/bin/env python3
import sys
import os
import subprocess
import re

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def get_stego_password(filename="squirrel.jpg"):
    """
    Reads the file to find the embedded password hint.
    Generators store hints in EXIF data which 'strings' can read.
    """
    try:
        if not os.path.exists(filename):
            return "password"

        # Use strings to scan the binary for the hint text injected by the generator
        output = subprocess.check_output(["strings", filename], text=True)
        
        # Pattern 1 (Guided): "Guided hint: steghide passphrase is 'password'."
        match_guided = re.search(r"passphrase is '(.+?)'", output)
        if match_guided: 
            return match_guided.group(1)
        
        # Pattern 2 (Solo): "The key they whisper is "ckeepers"."
        match_solo = re.search(r"whisper is \"(.+?)\"", output)
        if match_solo: 
            return match_solo.group(1)

    except Exception:
        pass
    
    return "password" # Fallback default

def main():
    bot = Coach("Steganography Decode")

    # 1. Determine the correct password before starting
    # This prevents the coach from giving the wrong instruction in Solo mode
    real_pass = get_stego_password()

    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, we need to enter the challenge directory.\n"
                "Use the 'cd' (change directory) command."
            ),
            command_to_display="cd challenges/01_Stego"
        )
        
        # === CRITICAL: SYNC COACH DIRECTORY ===
        # Now that the student has CD'd in the worker, we move the Coach there too.
        # This allows Tab Completion to find 'squirrel.jpg' in the next steps.
        os.chdir(os.path.join(os.path.dirname(__file__))) 
        # ======================================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what files are here using 'ls' (list segments) with '-l'."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The Extraction
        bot.teach_loop(
            instruction=(
                "We see 'squirrel.jpg'. We need to extract the data using 'steghide'.\n"
                f"We scanned the file metadata and found a hint that the password is: **{real_pass}**\n\n"
                "Construct the command using that password."
            ),
            # Template showing where the password goes
            command_template=f"steghide extract -sf squirrel.jpg -xf flag.txt -p {real_pass}",
            
            # We validate the prefix...
            command_prefix="steghide extract -sf squirrel.jpg -xf flag.txt -p ",
            
            # ...and check for the dynamically found password
            correct_password=real_pass,
            
            # Coach Core handles cleaning up previous failed attempts
            clean_files=["flag.txt"] 
        )

        # STEP 4: Verification
        bot.teach_step(
            instruction=(
                "Great! The tool extracted the secret message to 'flag.txt'.\n"
                "Read the file using 'cat' to get your flag."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()