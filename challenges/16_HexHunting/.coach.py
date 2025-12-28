#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Hex Hunter (strings & xxd)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/16_HexHunting"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Discovery
        bot.teach_step(
            instruction=(
                "We have a binary file named `hex_flag.bin`.\n"
                "Binaries contain compiled code, which is unreadable garbage to humans.\n"
                "Verify the file is there."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The "Wrong" Way
        # We teach them why 'cat' fails on binaries
        bot.teach_step(
            instruction=(
                "If you try to read it with `cat`, your terminal will fill with noise.\n"
                "Try it anyway to see the 'Matrix code'."
            ),
            command_to_display="cat hex_flag.bin"
        )

        # STEP 4: The "Right" Way (strings)
        bot.teach_step(
            instruction=(
                "That was messy.\n"
                "The command `strings` scans a binary file and prints only the printable characters (text).\n"
                "Run it to find hidden messages."
            ),
            command_to_display="strings hex_flag.bin"
        )

        # STEP 5: The Filter (strings + grep)
        bot.teach_loop(
            instruction=(
                "That's a lot of text.\n"
                "We know the flag contains 'CCRI'.\n"
                "Combine `strings` and `grep` with a pipe `|` to extract only the flag.\n\n"
                "**Note:** You might see multiple fake flags. The real one follows the format `CCRI-AAAA-1111`."
            ),
            # Template showing the pattern
            command_template="strings hex_flag.bin | grep CCRI",
            
            # Prefix for validation
            command_prefix="strings hex_flag.bin | grep ",
            
            # The search term
            correct_password="CCRI" 
        )

        # STEP 6: The "Matrix" View (xxd)
        # This gives them the "Hex Editor" view the original script simulated
        bot.teach_step(
            instruction=(
                "You found the flag!\n"
                "For a true 'Hex Editor' view (seeing the raw bytes next to the text),\n"
                "we use the tool `xxd` (or `hexdump`).\n\n"
                "Run this to see the file in hex format."
            ),
            command_to_display="xxd hex_flag.bin | grep CCRI"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()