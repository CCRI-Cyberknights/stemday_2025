#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("QR Code Automator")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/12_QRCodes"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/12_QRCodes"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "List the files.\n"
                "You will see 5 QR code images (`qr_01.png` to `qr_05.png`).\n"
                "One of them contains the flag."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Manual Inspection
        bot.teach_step(
            instruction=(
                "Let's look at the first one manually.\n"
                "Use `xdg-open` to launch the image viewer.\n"
                "(If a window opens, close it to continue. If nothing happens, that's okay too)."
            ),
            command_to_display="xdg-open qr_01.png"
        )

        # STEP 4: Command Line Scanning
        bot.teach_step(
            instruction=(
                "Scanning files one by one with a phone is slow.\n"
                "Linux has a tool called `zbarimg` that decodes QR codes directly in the terminal.\n"
                "Try it on the first image."
            ),
            command_to_display="zbarimg qr_01.png"
        )

        # STEP 5: Bulk Scanning (The Wildcard)
        bot.teach_step(
            instruction=(
                "That worked, but we have 5 images. We don't want to type the command 5 times.\n"
                "We can use the asterisk `*` (wildcard) to match **ALL** png files at once.\n\n"
                "Run `zbarimg *.png` to scan everything instantly."
            ),
            command_to_display="zbarimg *.png"
        )

        # STEP 6: Capture (Save Bulk Data)
        bot.teach_loop(
            instruction=(
                "That output scrolled by fast!\n"
                "Let's run the bulk scan again, but this time **save the results** to a file.\n"
                "We will call it `results.txt`."
            ),
            # Template showing the workflow
            command_template="zbarimg *.png > results.txt",
            
            # Strict regex validation
            command_prefix="zbarimg *.png > ",
            command_regex=r"^zbarimg \*\.png > results\.txt$",
            
            clean_files=["results.txt"]
        )

        # STEP 7: Filtering (Extract Flag)
        bot.teach_loop(
            instruction=(
                "Now we have `results.txt` full of raw data.\n"
                "We need to filter it for the 'CCRI' flag.\n"
                "Use `grep` to find the flag and **save it** to 'flag.txt'."
            ),
            command_template="grep \"CCRI\" results.txt > flag.txt",
            
            command_prefix="grep ",
            
            # Regex: grep "CCRI" results.txt > flag.txt
            command_regex=r"^grep \"CCRI\" results\.txt > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 8: Verification
        bot.teach_step(
            instruction=(
                "Success! You processed the images in bulk and isolated the flag.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()