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
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "List the files.\n"
                "You will see 5 QR code images (`qr_01.png` to `qr_05.png`).\n"
                "One of them contains the flag."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Manual Inspection (The Slow Way)
        bot.teach_step(
            instruction=(
                "Let's look at the first one just to see what we are dealing with.\n"
                "Use `xdg-open` to launch the image viewer.\n"
                "(Close the image window after it opens to continue)."
            ),
            command_to_display="xdg-open qr_01.png"
        )

        # STEP 4: Command Line Scanning (The Tool)
        bot.teach_step(
            instruction=(
                "Scanning that with a phone is tedious.\n"
                "Linux has a tool called `zbarimg` that decodes QR codes directly in the terminal.\n"
                "Try it on the first image."
            ),
            command_to_display="zbarimg qr_01.png"
        )

        # STEP 5: Bulk Scanning (The Wildcard)
        # 
        bot.teach_step(
            instruction=(
                "That worked, but we have 5 images. We don't want to type the command 5 times.\n"
                "We can use the asterisk `*` wildcard to match ALL png files at once.\n\n"
                "Run `zbarimg *.png` to scan everything instantly."
            ),
            command_to_display="zbarimg *.png"
        )

        # STEP 6: Capture and Search (Redirection)
        bot.teach_loop(
            instruction=(
                "That output scrolled by fast!\n"
                "Let's run it again, but this time save the results to a file using `>`.\n"
                "Then we will search that file for the flag."
            ),
            # Template showing the workflow
            command_template="zbarimg *.png > results.txt",
            
            # We just verify the redirection part
            command_prefix="zbarimg *.png > ",
            correct_password="results.txt" 
        )

        # STEP 7: The Final Filter
        bot.teach_step(
            instruction=(
                "Now we have a file `results.txt` full of decoded data.\n"
                "Use `grep` to find the 'CCRI' flag inside it."
            ),
            command_to_display="grep \"CCRI\" results.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()