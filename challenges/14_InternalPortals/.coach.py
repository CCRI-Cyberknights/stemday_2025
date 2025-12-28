#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Source Code Hunter (curl)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/14_InternalPortals"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Concept
        bot.teach_step(
            instruction=(
                "We have 5 internal portals: `alpha`, `beta`, `gamma`, `delta`, and `omega`.\n"
                "The flag is hidden in the HTML source code (the 'Body') of one of them.\n\n"
                "To view the source code in the terminal, we use `curl` (without the -I flag).\n"
                "Let's inspect the `alpha` portal first."
            ),
            command_to_display="curl http://localhost:5000/internal/alpha"
        )

        # STEP 3: The Result
        bot.teach_step(
            instruction=(
                "You see a bunch of HTML tags (`<html>`, `<div>`, etc).\n"
                "Somewhere in that mess, or in one of the other 4 portals, is the flag.\n"
                "Checking them one by one is slow. We need automation."
            ),
            command_to_display="echo Understood"
        )

        # STEP 4: Advanced Brace Expansion
        # 
        bot.teach_loop(
            instruction=(
                "Bash Brace Expansion isn't just for numbers.\n"
                "We can provide a comma-separated list of words.\n"
                "   `{alpha,beta,gamma,delta,omega}`\n\n"
                "Construct a command to `curl` all 5 portals at once and pipe the output to `grep` to find 'CCRI'."
            ),
            # Template showing the pattern
            command_template="curl http://localhost:5000/internal/{alpha,beta,gamma,delta,omega} | grep CCRI",
            
            # Prefix for validation
            command_prefix="curl http://localhost:5000/internal/{alpha,beta,gamma,delta,omega} | grep ",
            
            # The search term
            correct_password="CCRI" 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()