#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Intercepted Transmission (Base64)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "We have intercepted a suspicious message from a compromised system.\n"
                "Your goal is to decode it and find the hidden CCRI flag.\n\n"
                "First, move into the challenge directory."
            ),
            command_to_display="cd challenges/02_Base64"
        )

        # === SYNC DIRECTORY FOR TAB COMPLETION ===
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what files we captured.\n"
                "We are looking for 'encoded.txt'."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "Let's inspect the data using 'cat'.\n\n"
                "💡 What is Base64?\n"
                "   ➤ A text-based encoding scheme used to represent binary data.\n"
                "   ➤ If you see random characters ending in '==', it is likely Base64."
            ),
            command_to_display="cat encoded.txt"
        )

        # STEP 4: Decoding and Saving
        bot.teach_step(
            instruction=(
                "That definitely looks like Base64. Let's decode it.\n"
                "⚠️ **Important:** We will save the output to a file so we don't lose it.\n\n"
                "Use the greater-than symbol `>` to redirect the output into 'flag.txt'."
            ),
            command_to_display="base64 -d encoded.txt > flag.txt"
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Success! The output was saved to 'flag.txt' instead of printing to the screen.\n"
                "Now, safely read your flag using 'cat'."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()