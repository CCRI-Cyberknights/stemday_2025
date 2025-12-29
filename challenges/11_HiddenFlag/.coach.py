#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Recursive Hunter (grep -r)")
    bot.start()

    try:
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/11_HiddenFlag"
        )
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        bot.teach_step(
            instruction="Go inside the 'junk' directory.",
            command_to_display="cd junk"
        )
        os.chdir(os.path.join(os.getcwd(), 'junk'))

        bot.teach_step(
            instruction="Use 'ls -R' to see the scale of the problem.",
            command_to_display="ls -R"
        )

        # STEP 4: GREP (Exact Match)
        bot.teach_loop(
            instruction="Use 'grep' with the '-r' (recursive) flag to search for 'CCRI'.",
            command_template="grep -r \"CCRI\" .",
            command_prefix="grep -r ",
            correct_password="\"CCRI\" ."
        )

        # STEP 5: CAT (Anchored Regex)
        # We accept "cat ./path/to/file"
        bot.teach_loop(
            instruction="The grep command showed the file path. Use 'cat' to read it.",
            command_template="cat ./path/to/hidden/file",
            command_prefix="cat ",
            # Regex: Start with cat, space, maybe dot-slash, then chars, dot, chars
            # Example matches: "cat ./backup/.config" or "cat data/.hidden"
            command_regex=r"^cat (\./)?[\w/]+\.[\w]+$" 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()