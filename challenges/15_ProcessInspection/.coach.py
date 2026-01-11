#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Process Hunter (grep)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/15_ProcessInspection"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/15_ProcessInspection"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: The Setup
        bot.teach_step(
            instruction=(
                "We have a file named `ps_dump.txt`.\n"
                "This is a snapshot of all running processes (captured with `ps aux`).\n"
                "Developers sometimes carelessly pass secrets as command-line arguments.\n\n"
                "Let's check the size of the file to see what we are up against."
            ),
            command_to_display="wc -l ps_dump.txt"
        )

        # STEP 3: The "Bad" Way (Information Overload)
        bot.teach_step(
            instruction=(
                "That is nearly 100 lines of processes!\n"
                "Let's try to read it manually. Run `cat` to dump the file to the screen.\n"
                "Try to spot the flag as it scrolls by."
            ),
            command_to_display="cat ps_dump.txt"
        )

        # STEP 4: The "Good" Way (The Filter)
        bot.teach_loop(
            instruction=(
                "That was impossible. The text flew by too fast.\n"
                "This is why we use `grep`.\n"
                "It acts as a filter, discarding the noise and showing ONLY the lines matching our pattern.\n\n"
                "Use `grep` to search for 'CCRI' and **save the output** to 'flag.txt'."
            ),
            # Template showing the search
            command_template="grep \"CCRI\" ps_dump.txt > flag.txt",
            
            # Prefix for validation
            command_prefix="grep \"CCRI\" ps_dump.txt",
            
            # Strict Regex
            command_regex=r"^grep \"CCRI\" ps_dump\.txt > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Success! `grep` reduced the noise down to just the lines we care about.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()