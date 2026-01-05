#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Hex Flag Hunter")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/16_HexHunting"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/16_HexHunting"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: The Discovery
        bot.teach_step(
            instruction=(
                "We have a binary file named `hex_flag.bin`.\n"
                "Binaries contain compiled code. To a computer, it's instructions.\n"
                "To a human, it looks like garbage.\n\n"
                "Let's see the file size first."
            ),
            command_to_display="ls -lh hex_flag.bin"
        )

        # STEP 3: The "Raw" Way (xxd)
        bot.teach_step(
            instruction=(
                "If we want to see the *actual* data inside, we use a **Hex Dumper**.\n"
                "The tool `xxd` shows the raw hexadecimal values on the left and any printable characters on the right.\n\n"
                "Run this to see the raw structure."
            ),
            command_to_display="xxd hex_flag.bin | head -n 20"
        )

        # STEP 4: The Problem (Noise)
        bot.teach_step(
            instruction=(
                "**Analysis:** Look at that output. It's mostly dots `.` and random symbols.\n"
                "Finding a specific password or flag in thousands of lines of hex code is like finding a needle in a haystack.\n\n"
                "We need a tool that ignores the binary data and **extracts only the human-readable text**."
            ),
            # No command here, just a pause for reading
            command_to_display="clear" 
        )

        # STEP 5: The Solution (strings)
        bot.teach_step(
            instruction=(
                "The tool for this is called `strings`.\n"
                "It scans the file for sequences of printable characters (letters, numbers, punctuation) and prints them.\n\n"
                "Try running it on the binary."
            ),
            command_to_display="strings hex_flag.bin"
        )

        # STEP 6: Refining the Search
        bot.teach_loop(
            instruction=(
                "That's better! But notice it's still 'messy'—`strings` grabs *anything* that looks like text, including random garbage like `H)^8s`.\n\n"
                "We need to filter this output. Since we know the flag format contains 'CCRI', we can combine `strings` with `grep`.\n\n"
                "1. Extract text with `strings`.\n"
                "2. Filter for 'CCRI' with `grep`.\n"
                "3. Save it to `flag.txt`."
            ),
            # Template showing the pipeline
            command_template="strings hex_flag.bin | grep \"CCRI\" > flag.txt",
            
            # Prefix for validation
            command_prefix="strings hex_flag.bin | grep ",
            
            # Regex: strings hex_flag.bin | grep "CCRI" > flag.txt
            command_regex=r"^strings hex_flag\.bin \| grep \"?CCRI\"? > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verify
        bot.teach_step(
            instruction=(
                "Success! You turned raw binary data into a clean text flag.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()