#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Binary Forensics (strings)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory."
            ),
            command_to_display="cd challenges/07_ExtractBinary"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "List the files.\n"
                "You will see 'hidden_flag', which is a compiled binary program (executable)."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The Problem (Binary vs Text)
        bot.teach_step(
            instruction=(
                "Try to read the binary file using 'cat'.\n"
                "You will see a mess of random characters and noise. This is compiled code, not text."
            ),
            command_to_display="cat hidden_flag"
        )

        # STEP 4: The Solution (Strings)
        bot.teach_step(
            instruction=(
                "That was messy.\n"
                "To extract human-readable text from a binary, we use the 'strings' command.\n"
                "Let's dump all the strings found in the file."
            ),
            command_to_display="strings hidden_flag"
        )

        # STEP 5: Filtering with Grep
        bot.teach_loop(
            instruction=(
                "That's a lot of output!\n"
                "We can use the pipe operator '|' to send that output into 'grep' to search for the flag.\n"
                "We know the flag contains 'CCRI'.\n\n"
                "Combine 'strings' and 'grep' to find it!"
            ),
            command_template="strings hidden_flag | grep [SEARCH_TERM]",
            command_prefix="strings hidden_flag | grep ",
            correct_password="CCRI"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()