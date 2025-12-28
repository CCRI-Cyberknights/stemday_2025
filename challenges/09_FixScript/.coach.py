#!/usr/bin/env python3
import sys
import os
import re

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def identify_bug(filepath):
    """
    Reads the file to find the broken line and the operator used.
    Returns the operator symbol (e.g., '*', '-', '/')
    """
    try:
        with open(filepath, "r") as f:
            content = f.read()
        
        # Regex looks for: code = part1 [OPERATOR] part2
        # It captures whatever symbol is in the middle group
        match = re.search(r"code\s*=\s*part1\s*([\+\-\*\/])\s*part2", content)
        if match:
            return match.group(1)
    except:
        pass
    return "*" # Default fallback if we can't read it

def main():
    bot = Coach("Python Debugging")
    bot.start()

    # 1. Analyze the file BEFORE we start teaching
    # This makes the script "smart" enough to handle the randomized generator
    bug_symbol = identify_bug("broken_flag.py")
    
    # Map symbols to human-readable names for the dialogue
    symbol_names = {
        "*": "asterisk (multiplication)",
        "-": "minus sign (subtraction)",
        "/": "slash (division)",
        "+": "plus sign"
    }
    bug_name = symbol_names.get(bug_symbol, "operator")

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/09_FixScript"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction="List the files. You will see 'broken_flag.py'.",
            command_to_display="ls -l"
        )

        # STEP 3: Run the broken code
        bot.teach_step(
            instruction=(
                "Run the script to see the error.\n"
                "The numbers will look wrong because the math is incorrect."
            ),
            command_to_display="python3 broken_flag.py"
        )

        # STEP 4: Editing (Dynamic Instruction)
        # We inject the actual symbol found into the instructions
        bot.teach_step(
            instruction=(
                f"The script is currently using a **{bug_name}** (`{bug_symbol}`), which is incorrect.\n"
                "We need to change it to a **plus sign** (`+`) to make the math work.\n\n"
                "👉 **Task:**\n"
                "   1. `nano broken_flag.py`\n"
                f"   2. Find the line: `code = part1 {bug_symbol} part2`\n"
                f"   3. Change `{bug_symbol}` to `+`\n"
                "   4. Save (Ctrl+O) and Exit (Ctrl+X)."
            ),
            command_to_display="nano broken_flag.py"
        )

        # STEP 5: Verify
        bot.teach_step(
            instruction="Now run the fixed script to get the flag!",
            command_to_display="python3 broken_flag.py"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()