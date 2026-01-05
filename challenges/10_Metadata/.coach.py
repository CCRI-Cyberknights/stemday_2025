#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Metadata Inspector (exiftool)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/10_Metadata"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/10_Metadata"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "We have an image file: 'capybara.jpg'.\n"
                "Images often contain hidden 'metadata' (EXIF data) like camera model, GPS, or comments.\n"
                "List the files to confirm it is there."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "To see this hidden data, we use a tool called `exiftool`.\n"
                "Run it against the image to dump all available metadata."
            ),
            command_to_display="exiftool capybara.jpg"
        )

        # STEP 4: Filtering & Saving
        bot.teach_loop(
            instruction=(
                "That was a lot of scrolling!\n"
                "We know the flag contains 'CCRI'. Instead of scrolling manually:\n"
                "1. Use `| grep` to filter for 'CCRI'.\n"
                "2. Use `>` to save the result to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            # Template showing the pattern
            command_template="exiftool capybara.jpg | grep \"CCRI\" > flag.txt",
            
            # Prefix for visual hint
            command_prefix="exiftool capybara.jpg | grep ",
            
            # Strict validation regex
            # Matches: exiftool capybara.jpg | grep "CCRI" > flag.txt
            command_regex=r"^exiftool capybara\.jpg \| grep \"CCRI\" > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Success! You extracted the hidden metadata and saved it.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()