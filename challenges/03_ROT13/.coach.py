#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def cleanup():
    if os.path.exists("flag.txt"):
        try:
            os.remove("flag.txt")
        except:
            pass

def main():
    bot = Coach("ROT13 Decoder")
    
    # Ensure clean slate
    cleanup()
    
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory."
            ),
            command_to_display="cd challenges/03_ROT13"
        )

        # === SYNC DIRECTORY ===
        target_dir = "challenges/03_ROT13"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what we are dealing with."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Intel Confirmation
        bot.teach_step(
            instruction=(
                "The **Mission Brief** identifies this as **ROT13** (shifted by 13 places).\n"
                "Let's read `cipher.txt`. You will see it looks English-like but scrambled (e.g., 'Uryyb' instead of 'Hello')."
            ),
            command_to_display="cat cipher.txt"
        )

        # STEP 4: Execution (Building the Tool)
        bot.teach_step(
            instruction=(
                "Linux doesn't have a 'rot13' button, but we can build one using `tr` (translate).\n"
                "We tell it to swap A-Z with N-Z-A-M (shifting the alphabet by 13 places).\n\n"
                "Run this command to decode it and save to `flag.txt`."
            ),
            # This is a complex command, so providing it directly is the right move for this level
            command_to_display="cat cipher.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' > flag.txt"
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Success! The decrypted text is now safely stored in 'flag.txt'.\n"
                "Read the file to get your flag."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()