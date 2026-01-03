#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("ROT13 Decoder")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory.\n"
                "We are looking for a file named 'cipher.txt'."
            ),
            command_to_display="cd challenges/03_ROT13"
        )

        # === SYNC DIRECTORY ===
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what we are dealing with using 'ls -l'."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "Read the file using 'cat'.\n"
                "You will see text that looks readable but 'shifted' (e.g., 'Uryyb' instead of 'Hello')."
            ),
            command_to_display="cat cipher.txt"
        )

        # STEP 4: Decoding and Saving
        # ROT13 is a shift of 13 places. We use 'tr' to swap the alphabet.
        # We also use '>' to save the output.
        bot.teach_step(
            instruction=(
                "This is a ROT13 cipher (a Caesar cipher shifted by 13).\n"
                "Since Linux doesn't have a 'rot13' command, we build one using 'tr' (translate).\n\n"
                "We will pipe the file into 'tr' to swap the letters, and redirect `>` the result to 'flag.txt'."
            ),
            command_to_display="cat cipher.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' > flag.txt"
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Perfect. The decrypted text is now safely stored in 'flag.txt'.\n"
                "Read the file to get your flag."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()