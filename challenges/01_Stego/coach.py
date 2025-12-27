#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Steganography Decode")
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

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what files are here using 'ls' (list segments) with '-l'."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The Guessing Game (CLEAN & NO -f)
        bot.teach_loop(
            instruction=(
                "We see 'squirrel.jpg'. We need to extract the data using 'steghide'.\n"
                "We don't know the password yet, so we have to guess.\n"
                "Common passwords might be: '123456', 'admin', 'password', 'squirrel', etc.\n\n"
                "Construct the command and replace [PASSWORD] with your guess."
            ),
            # NO -f here
            command_template="steghide extract -sf squirrel.jpg -xf flag.txt -p [PASSWORD]",
            
            # NO -f here
            command_prefix="steghide extract -sf squirrel.jpg -xf flag.txt -p ",
            
            correct_password="password",
            
            # CORE HANDLES OVERWRITES HERE
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