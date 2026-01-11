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
                "Binaries contain compiled code, which looks like garbage to humans.\n"
                "Verify the file is there."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The "Wrong" Way (Chaos)
        bot.teach_step(
            instruction=(
                "If you try to read a binary with `cat`, your terminal will interpret the raw bytes as text.\n"
                "This results in 'Matrix code' (garbage).\n"
                "Try it anyway to see the mess."
            ),
            command_to_display="cat hex_flag.bin"
        )

        # STEP 4: The "Hex" Way (Order)
        bot.teach_step(
            instruction=(
                "That was useless. To analyze binaries properly, we need a **Hex Dump**.\n"
                "The tool `xxd` shows the raw Hexadecimal (math) on the left and the ASCII (text) representation on the right.\n\n"
                "Run `xxd` to see the file's true structure."
            ),
            command_to_display="xxd hex_flag.bin"
        )

        # STEP 5: The "Easy" Way (strings)
        bot.teach_step(
            instruction=(
                "You can see the text on the right side of the `xxd` output, but it's mixed with dots and symbols.\n"
                "To extract **only** the readable text, we use the `strings` command.\n\n"
                "Run it to clean up the output."
            ),
            command_to_display="strings hex_flag.bin"
        )

        # STEP 6: Filter and Save (The Solution)
        bot.teach_loop(
            instruction=(
                "That is much clearer! Now we filter for the flag.\n"
                "**Note:** `strings` is 'dumb'—it grabs *any* printable character. You might see random letters attached to the flag (e.g., `xyCCRI...`). This is normal in forensics!\n\n"
                "1. `strings` to clean the binary.\n"
                "2. `grep` to find 'CCRI'.\n"
                "3. `>` to save it to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            # Template showing the pipeline
            command_template="strings hex_flag.bin | grep \"CCRI\" > flag.txt",
            
            # Prefix for validation
            command_prefix="strings hex_flag.bin | grep ",
            
            # Regex: strings hex_flag.bin | grep "CCRI" > flag.txt
            # We allow optional quotes around "CCRI"
            command_regex=r"^strings hex_flag\.bin \| grep \"?CCRI\"? > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verify
        bot.teach_step(
            instruction=(
                "Success! You turned raw binary data into a text flag.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()