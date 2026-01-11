#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Log Analysis (grep)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/08_FakeAuthLog"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/08_FakeAuthLog"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "We have a file named 'auth.log'.\n"
                "This is a standard Linux log file that records login attempts.\n"
                "Check the file size with `ls -lh` (human readable) to see how big it is."
            ),
            command_to_display="ls -lh"
        )

        # STEP 3: Preview (head)
        bot.teach_step(
            instruction=(
                "Logs can be huge. Reading the whole thing with `cat` is messy.\n"
                "Use `head` to look at just the first 20 lines to understand the format."
            ),
            command_to_display="head -n 20 auth.log"
        )

        # STEP 4: Simple Searching + Saving
        bot.teach_loop(
            instruction=(
                "We know the flag starts with 'CCRI'.\n"
                "Instead of reading thousands of lines, use `grep` to search for that specific text.\n"
                "**Save the output** to 'flag.txt'."
            ),
            command_template="grep \"CCRI\" auth.log > flag.txt",
            
            command_prefix="grep \"CCRI\" auth.log",
            
            # Regex enforces the redirection to flag.txt
            command_regex=r"^grep \"CCRI\" auth\.log > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 5: Verify Specific Flag
        bot.teach_step(
            instruction=(
                "Success! You isolated the specific flag.\n"
                "Read 'flag.txt' to confirm."
            ),
            command_to_display="cat flag.txt"
        )

        # STEP 6: Advanced Regex + Saving (New File)
        bot.teach_loop(
            instruction=(
                "**Bonus Lesson:** If we didn't know the 'CCRI' prefix, we could search for the *pattern* (4 chars - 4 chars - 4 chars).\n"
                "Linux uses `grep -E` for extended regex patterns.\n\n"
                "Run this regex search and save the output to a **new file** called 'candidates.txt'."
            ),
            command_template="grep -E \"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\" auth.log > candidates.txt",
            
            command_prefix="grep -E ",
            
            # Use Regex to safely match the complex command string.
            # We escape the brackets \[ \] and braces \{ \} for the python regex engine.
            command_regex=r"^grep -E \"\[A-Z0-9\]\{4\}-\[A-Z0-9\]\{4\}-\[A-Z0-9\]\{4\}\" auth\.log > candidates\.txt$",
            
            clean_files=["candidates.txt"]
        )

        # STEP 7: Verify Candidates
        bot.teach_step(
            instruction=(
                "Read 'candidates.txt'.\n"
                "You will see it captured the 'CCRI' flag PLUS other matching patterns (decoys)."
            ),
            command_to_display="cat candidates.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()