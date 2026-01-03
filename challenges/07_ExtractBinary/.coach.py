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
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/07_ExtractBinary"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        elif os.path.basename(os.getcwd()) == "07_ExtractBinary":
            pass
        else:
            bot.print_error(f"Could not find '{target_dir}'.")
            return
        # ======================

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
                "**Warning:** You will see a mess of random characters and noise because this is compiled code, not text."
            ),
            command_to_display="cat hidden_flag"
        )

        # STEP 4: The Solution (Strings)
        bot.teach_step(
            instruction=(
                "That was messy. (You might need to type 'reset' if your terminal looks weird afterwards, but usually it's fine).\n\n"
                "To extract human-readable text from a binary, we use the 'strings' command.\n"
                "Run it now to see everything hidden inside."
            ),
            command_to_display="strings hidden_flag"
        )

        # STEP 5: Filtering and Saving
        bot.teach_loop(
            instruction=(
                "That scroll was too fast!\n"
                "We can combine tools to pinpoint the flag:\n"
                "1. `strings` extracts the text.\n"
                "2. `grep` filters for 'CCRI'.\n"
                "3. `>` saves it to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            command_template="strings hidden_flag | grep CCRI > flag.txt",
            
            command_prefix="strings hidden_flag | grep ",
            
            # Enforce the full pipeline structure
            command_regex=r"^strings hidden_flag \| grep CCRI > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 6: Verification
        bot.teach_step(
            instruction=(
                "Success! You extracted the hidden data and saved it.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()