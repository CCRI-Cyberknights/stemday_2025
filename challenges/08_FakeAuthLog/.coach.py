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
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "We have a file named 'auth.log'.\n"
                "This is a standard Linux log file that records login attempts (SSH, sudo, etc).\n"
                "Check the file size with 'ls -lh' (human readable)."
            ),
            command_to_display="ls -lh"
        )

        # STEP 3: Preview (head)
        bot.teach_step(
            instruction=(
                "Logs can be huge. Reading the whole thing with 'cat' is messy.\n"
                "Use 'head' to look at just the first 20 lines to understand the format."
            ),
            command_to_display="head -n 20 auth.log"
        )

        # STEP 4: Searching (grep)
        # The prompt says the flag format is CCRI-AAAA-1111.
        # Instead of reading 1000 lines, we can just search for "CCRI".
        bot.teach_step(
            instruction=(
                "We are looking for a hidden flag inside a PID (Process ID) field.\n"
                "We know the flag starts with 'CCRI'.\n"
                "Use 'grep' to search the file for that specific text."
            ),
            command_to_display="grep \"CCRI\" auth.log"
        )

        # STEP 5: Advanced Regex (Bonus Lesson)
        # Explain that if we didn't know "CCRI", we could search for the pattern XXXX-XXXX-XXXX
        # grep -E means "Extended Regex"
        bot.teach_loop(
            instruction=(
                "Excellent. You found it.\n\n"
                "**Bonus Lesson:** What if we didn't know it started with 'CCRI'?\n"
                "We could search for the *pattern* (4 chars - 4 chars - 4 chars).\n"
                "Linux uses 'grep -E' for patterns.\n"
                "Try searching for the regex: '[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}'"
            ),
            command_template="grep -E \"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\" auth.log",
            command_prefix="grep -E ",
            correct_password="[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\" auth.log" 
            # Note: The 'correct_password' logic here is checking the suffix of the command 
            # because we are using a loop. The input is "grep -E ...", we check the rest.
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()