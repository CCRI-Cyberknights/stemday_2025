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
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "We have an image file: 'capybara.jpg'.\n"
                "Images often contain hidden 'metadata' (EXIF data) like camera model, location, or comments.\n"
                "List the files to confirm it's there."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "To see this hidden data, we use a tool called 'exiftool'.\n"
                "Run it against the image to dump all available metadata."
            ),
            command_to_display="exiftool capybara.jpg"
        )

        # STEP 4: Filtering
        bot.teach_loop(
            instruction=(
                "That was a lot of data!\n"
                "We are looking for a hidden flag, which likely contains the text 'CCRI'.\n"
                "Instead of scrolling, let's use the pipe `|` and `grep` to filter the output."
            ),
            # Template showing the pattern
            command_template="exiftool capybara.jpg | grep [KEYWORD]",
            
            # Prefix for validation
            command_prefix="exiftool capybara.jpg | grep ",
            
            # We accept "CCRI" or "Artist" or "Comment" as valid search terms for this lesson
            # But the 'correct_password' logic in the core expects a single match.
            # We will force them to search for the flag prefix "CCRI" to win.
            correct_password="CCRI"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()