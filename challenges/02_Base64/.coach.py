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
        # Moves the coach process into the folder so "enc[TAB]" works
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

        # STEP 4: Decoding
        bot.teach_step(
            instruction=(
                "That content definitely looks like Base64.\n"
                "We can use the Linux 'base64' tool to reverse it.\n\n"
                "🔍 Command breakdown:\n"
                "   base64       → The decoding tool\n"
                "   -d           → The 'decode' flag (converts text back to data)\n"
                "   encoded.txt  → The file we are processing"
            ),
            command_to_display="base64 -d encoded.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()