#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
# Heavily commented for educational transparency
SOLVER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import sys

# This script decrypts a Vigenere cipher.
# Logic: (CipherChar - KeyChar) % 26 = PlainChar

def decrypt(text, key):
    res = []
    key_idx = 0
    key = key.lower()
    for c in text:
        if c.isalpha():
            # Determine ASCII base (65 for A, 97 for a)
            base = 65 if c.isupper() else 97
            
            # Get shift amount from key character (a=0, b=1, etc.)
            k = ord(key[key_idx % len(key)]) - 97
            
            # Reverse the shift
            # (Current - Base - Shift) % 26 + Base
            res.append(chr((ord(c) - base - k) % 26 + base))
            
            # Move to next letter of the key
            key_idx += 1
        else:
            # Keep punctuation/spaces as is
            res.append(c)
    return "".join(res)

if len(sys.argv) < 2:
    print("Usage: python3 .solver.py [KEY]")
    sys.exit(1)

try:
    # 1. Read Encrypted Data
    with open("cipher.txt", "r") as f:
        data = f.read().strip()
    
    # 2. Run Decryption
    key = sys.argv[1]
    result = decrypt(data, key)
    
    print(f"Decrypting with key '{key}'...\n")
    print(result)
    
    # 3. Save Output
    with open("decoded_output.txt", "w") as f:
        f.write(result)
        
except Exception as e:
    print(f"Error: {e}")
"""

def create_solver_tool():
    """Writes the temporary solver script to the current folder."""
    tool_path = os.path.join(os.path.dirname(__file__), ".solver.py")
    with open(tool_path, "w") as f:
        f.write(SOLVER_SCRIPT_CONTENT)
    return tool_path

def cleanup_solver_tool():
    """Removes the temporary solver script."""
    tool_path = os.path.join(os.path.dirname(__file__), ".solver.py")
    if os.path.exists(tool_path):
        os.remove(tool_path)

def main():
    bot = Coach("Vigenère Cipher Breaker")
    bot.start()

    # 1. Create the tool before we start teaching
    create_solver_tool()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory.\n"
                "We are looking for 'cipher.txt'."
            ),
            command_to_display="cd challenges/04_Vigenere"
        )
        
        # SYNC DIRECTORY
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction="Check the directory contents.",
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "Read the encrypted file.\n"
                "It looks like random letters, but the pattern suggests a Vigenère cipher."
            ),
            command_to_display="cat cipher.txt"
        )

        # STEP 4: Code Transparency (NEW STEP)
        bot.teach_step(
            instruction=(
                "We have a script called '.solver.py' to handle the decryption math.\n"
                "Before we use it, look at the code.\n"
                "Notice the math: `(ord(c) - base - k) % 26`. That reverses the shift!"
            ),
            command_to_display="cat .solver.py"
        )

        # STEP 5: The Ephemeral Tool
        # We guide them to use the tool we just silently created (.solver.py)
        bot.teach_loop(
            instruction="...",
            command_template="python3 .solver.py [KEY]",
            command_prefix="python3 .solver.py ",
            # ANCHORED REGEX
            command_regex=r"^python3 \.solver\.py (login)$", 
            clean_files=["decoded_output.txt"]
        )

        # STEP 6: Verification
        bot.teach_step(
            instruction=(
                "Success! The tool found the flag and saved it to 'decoded_output.txt'.\n"
                "Let's display that file to finish."
            ),
            command_to_display="cat decoded_output.txt"
        )

        # Cleanup happens in finally block
        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        # Ensure we delete the temporary tool even if they crash/exit
        cleanup_solver_tool()

if __name__ == "__main__":
    main()