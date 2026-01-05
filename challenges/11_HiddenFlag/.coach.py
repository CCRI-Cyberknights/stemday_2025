#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Recursive Hunter (grep -r)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/11_HiddenFlag"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/11_HiddenFlag"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery (The Haystack)
        bot.teach_step(
            instruction=(
                "We have a directory called 'junk'.\n"
                "Use `ls -R` (recursive list) to see the massive amount of files inside."
            ),
            command_to_display="ls -R"
        )

        # STEP 3: Enter the Maze
        bot.teach_step(
            instruction=(
                "That is a lot of files! Checking them manually would take forever.\n"
                "Move inside the directory to start our search."
            ),
            command_to_display="cd junk"
        )
        # === SYNC DIRECTORY ===
        if os.path.exists("junk"):
            os.chdir("junk")
        # ======================

        # STEP 4: GREP (Find the path)
        bot.teach_loop(
            instruction=(
                "We know the flag contains 'CCRI'.\n"
                "Use `grep` with the `-r` (recursive) flag to search every file in the current folder (`.`)."
            ),
            command_template="grep -r \"CCRI\" .",
            
            command_prefix="grep -r ",
            
            # Regex matches: grep -r "CCRI" .
            command_regex=r"^grep -r \"CCRI\" \.$"
        )

        # STEP 5: CAT (Capture the Flag)
        bot.teach_loop(
            instruction=(
                "Look at the output above. `grep` found a match and printed the path (e.g., `./dirs/.hidden`).\n\n"
                "**Copy that path.**\n"
                "Run `cat` on that path and save the output to 'flag.txt'."
            ),
            # Clear visual placeholder for the student
            command_template="cat [PATH_FROM_ABOVE] > flag.txt",
            
            command_prefix="cat ",
            
            # Regex allows any standard file path characters
            command_regex=r"^cat [\w\-\./]+ > flag\.txt$",
            
            clean_files=["flag.txt"]
        )
        
        # STEP 6: Verify
        bot.teach_step(
            instruction=(
                "Success! You surgically isolated the flag file.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()