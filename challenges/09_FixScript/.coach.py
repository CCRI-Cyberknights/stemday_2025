#!/usr/bin/env python3
import sys
import os
import re

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def get_script_data(filename):
    """
    Reads the file to extract part1, part2, and the current broken symbol.
    Returns: (part1, part2, bug_symbol) or (None, None, None) if failed.
    """
    # Look for file in current directory
    filepath = filename 
    
    try:
        with open(filepath, "r") as f:
            content = f.read()
        
        # Regex to find: part1 = 123
        p1 = re.search(r"part1\s*=\s*(\d+)", content)
        # Regex to find: part2 = 456
        p2 = re.search(r"part2\s*=\s*(\d+)", content)
        # Regex to find: code = part1 [OPERATOR] part2
        bug = re.search(r"code\s*=\s*part1\s*([\+\-\*\/])\s*part2", content)
        
        if p1 and p2 and bug:
            return int(p1.group(1)), int(p2.group(1)), bug.group(1)
            
    except Exception:
        pass
    return None, None, "?"

def generate_math_table(p1, p2):
    """
    Generates a text table showing the result of all 4 operators.
    Returns the string table and the correct symbol.
    """
    if p1 is None or p2 is None:
        return "Could not read data.", "+"

    correct_symbol = "+" # default
    
    # Header
    table =  "\n   Operator | Calculation       | Result      | Status\n"
    table += "   ---------|-------------------|-------------|-----------\n"
    
    for symbol, name in [("+", "Add"), ("-", "Sub"), ("*", "Mult"), ("/", "Div")]:
        try:
            val = eval(f"{p1} {symbol} {p2}")
            
            # Formatting checks
            if isinstance(val, int):
                val_str = f"{val}"
            elif val.is_integer():
                val = int(val)
                val_str = f"{val}"
            else:
                val_str = f"{val:.2f}"
            
            # Logic check: Valid flags use a 4-digit integer code (1000-9999)
            if 1000 <= val <= 9999 and val == int(val):
                status = "✅ VALID (Target)"
                correct_symbol = symbol
            else:
                status = "❌ Invalid"
                
            table += f"      {symbol}     | {p1} {symbol} {p2:<6} | {val_str:<11} | {status}\n"
            
        except ZeroDivisionError:
             table += f"      {symbol}     | {p1} {symbol} {p2:<6} | ERROR       | ❌ Invalid\n"

    return table, correct_symbol

def main():
    bot = Coach("Python Debugging")
    
    # 1. Analyze the file JIT (Just In Time)
    # We do this before starting the bot so we have the 'Intel' ready
    try:
        if os.path.exists("challenges/09_FixScript/broken_flag.py"):
             target_path = "challenges/09_FixScript/broken_flag.py"
        elif os.path.exists("broken_flag.py"):
             target_path = "broken_flag.py"
        else:
             target_path = None

        if target_path:
            p1, p2, bug_symbol = get_script_data(target_path)
            math_table, correct_symbol = generate_math_table(p1, p2)
            
            # Determine human-readable name for the correct symbol
            symbol_map = {"+": "Plus (+)", "-": "Minus (-)", "*": "Multiply (*)", "/": "Divide (/)"}
            correct_name = symbol_map.get(correct_symbol, "Operator")
        else:
            # Fallback if file is missing (prevents crash)
            p1, p2, bug_symbol = 0, 0, "?"
            math_table = "File not found."
            correct_symbol = "+"
            correct_name = "Plus"

    except Exception:
        # Fallback for safety
        p1, p2, bug_symbol = 0, 0, "?"
        math_table = "Error analyzing file."
        correct_symbol = "+"
        correct_name = "Plus"

    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/09_FixScript"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/09_FixScript"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction="List the files. You will see 'broken_flag.py'.",
            command_to_display="ls -l"
        )

        # STEP 3: Read Source Code
        bot.teach_step(
            instruction=(
                "**Before we run it, we must read it.**\n"
                "Use `cat` to see the code.\n"
                "Look for the variables `part1`, `part2`, and the math equation."
            ),
            command_to_display="cat broken_flag.py"
        )

        # STEP 4: Run the broken code
        bot.teach_step(
            instruction=(
                "Now run the script to see the bug in action.\n"
                "The output is likely scrambled or wrong because the operator is incorrect."
            ),
            command_to_display="python3 broken_flag.py"
        )

        # STEP 5: The Debug Analysis & Editing
        bot.teach_step(
            instruction=(
                f"**Analysis:**\n"
                f"The code uses the operator `{bug_symbol}`.\n"
                f"The variables are: `part1={p1}`, `part2={p2}`.\n\n"
                "**Let's calculate all possibilities to find the 4-digit code:**\n"
                f"{math_table}\n"
                f"The table proves the correct operator is **{correct_name}**.\n\n"
                "👉 **Task:**\n"
                "   1. Run `nano broken_flag.py`.\n"
                "   2. **Click the terminal** to focus.\n"
                f"   3. Use **Arrow Keys** to find `{bug_symbol}`.\n"
                f"   4. Delete it and type `{correct_symbol}`.\n"
                "   5. **Save & Exit:** `Ctrl+X`, then `Y`, then `Enter`."
            ),
            command_to_display="nano broken_flag.py"
        )

        # STEP 6: Verify and Save
        bot.teach_loop(
            instruction=(
                "Now that the logic is fixed, run the script and **save the output** to 'flag.txt'."
            ),
            command_template="python3 broken_flag.py > flag.txt",
            command_prefix="python3 broken_flag.py",
            command_regex=r"^python3 broken_flag\.py > flag\.txt$",
            clean_files=["flag.txt"]
        )

        # STEP 7: Final Confirm
        bot.teach_step(
            instruction="Success! Read 'flag.txt' to see the corrected flag.",
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()