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
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Trap
        bot.teach_step(
            instruction=(
                "We have a directory named 'junk' that contains the flag.\n"
                "Go inside it."
            ),
            command_to_display="cd junk"
        )

        # Sync directory again to follow them into 'junk'
        os.chdir(os.path.join(os.getcwd(), 'junk'))

        # STEP 3: The Scale of the Problem
        # 
        bot.teach_step(
            instruction=(
                "Let's see what we are up against.\n"
                "Use 'ls -R' (Recursive) to list every file in every subfolder.\n"
                "You'll see it's a mess of hidden and visible files."
            ),
            command_to_display="ls -R"
        )

        # STEP 4: The Solution (grep -r)
        # Instead of guessing filenames, we search for the *content*.
        # grep -r searches recursively through the tree.
        bot.teach_loop(
            instruction=(
                "We don't know which file holds the flag, but we know the flag starts with 'CCRI'.\n"
                "Opening files one by one is too slow.\n\n"
                "Use 'grep' with the '-r' (recursive) flag to search the content of *every* file at once.\n"
                "   grep -r \"[SEARCH_TERM]\" ."
            ),
            # Template showing the pattern
            command_template="grep -r \"CCRI\" .",
            
            # Prefix for validation
            command_prefix="grep -r ",
            
            # Key arguments they must type
            correct_password="\"CCRI\" ." 
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "The grep command showed you exactly which file contains the flag, and even printed the line!\n"
                "Just to be sure, 'cat' the file shown in the output to claim your victory."
            ),
            # We accept any 'cat' command since the filename is random
            command_template="cat [FILE_PATH]",
            command_regex=r"cat .*" 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()