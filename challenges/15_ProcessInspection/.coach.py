#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Process Hunter (ps & grep)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/15_ProcessInspection"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Context
        bot.teach_step(
            instruction=(
                "We have a file named `ps_dump.txt`.\n"
                "This is a snapshot of all running processes on a compromised system (captured using `ps aux`).\n"
                "Sometimes, careless developers pass secrets as command-line arguments.\n\n"
                "Let's peek at the file."
            ),
            command_to_display="head -n 10 ps_dump.txt"
        )

        # STEP 3: The Problem
        # 
        bot.teach_step(
            instruction=(
                "You see columns for USER, PID, and COMMAND.\n"
                "The COMMAND column shows exactly how the program was launched.\n"
                "If we read the whole file, it would take forever."
            ),
            command_to_display="echo Understood"
        )

        # STEP 4: The Solution
        bot.teach_loop(
            instruction=(
                "We are looking for a flag in the format `CCRI-AAAA-1111`.\n"
                "We suspect it was passed in an argument like `--flag=CCRI...`.\n\n"
                "Use `grep` to search `ps_dump.txt` for the text 'CCRI'."
            ),
            # Template showing the search
            command_template="grep \"CCRI\" ps_dump.txt",
            
            # Prefix for validation
            command_prefix="grep \"CCRI\" ps_dump.txt",
            
            # Since the command itself is the answer, no extra password needed
            correct_password="" 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()