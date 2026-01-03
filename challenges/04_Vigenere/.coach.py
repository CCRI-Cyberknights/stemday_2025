#!/usr/bin/env python3
import sys
import os

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
SOLVER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import sys

def decrypt(text, key):
    res = []
    key_idx = 0
    key = key.lower()
    for c in text:
        if c.isalpha():
            base = 65 if c.isupper() else 97
            k = ord(key[key_idx % len(key)]) - 97
            res.append(chr((ord(c) - base - k) % 26 + base))
            key_idx += 1
        else:
            res.append(c)
    return "".join(res)

if len(sys.argv) < 2:
    print("Usage: python3 .solver.py [KEY]")
    sys.exit(1)

try:
    with open("cipher.txt", "r") as f:
        data = f.read().strip()
    
    key = sys.argv[1]
    result = decrypt(data, key)
    
    # Just print the result to stdout
    print(result)
        
except Exception as e:
    print(f"Error: {e}")
"""

def create_local_solver():
    """Writes the solver to the CURRENT working directory."""
    # DEBUG: Uncomment the next line if you need to verify where it is writing
    # print(f"DEBUG: Writing .solver.py to {os.getcwd()}")
    with open(".solver.py", "w") as f:
        f.write(SOLVER_SCRIPT_CONTENT)

def cleanup_local_solver():
    """Removes the solver from the CURRENT working directory."""
    if os.path.exists(".solver.py"):
        os.remove(".solver.py")

def main():
    bot = Coach("Vigenère Cipher Breaker")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory.\n"
                "We are looking for 'cipher.txt'."
            ),
            command_to_display="cd challenges/04_Vigenere"
        )
        
        # === SYNC DIRECTORY ===
        # We assume standard repo structure. 
        # The user ran 'cd challenges/04_Vigenere', so we must follow.
        target_dir = "challenges/04_Vigenere"
        
        # Check if we can find the directory relative to where the script started
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        elif os.path.basename(os.getcwd()) == "04_Vigenere":
            # Just in case we are already there
            pass
        else:
            # Fallback for complex relative paths (development environment)
            bot.print_error(f"Could not find '{target_dir}' from '{os.getcwd()}'")
            return

        # === CREATE TOOL ===
        create_local_solver()
        # ===================

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

        # STEP 4: Code Transparency
        bot.teach_step(
            instruction=(
                "We have a custom script '.solver.py'.\n"
                "Use 'cat' to audit the code before running it.\n"
                "Notice it prints the result but **does not save it**."
            ),
            command_to_display="cat .solver.py"
        )

        # STEP 5: The Ephemeral Tool + Redirection
        bot.teach_loop(
            instruction=(
                "We found a sticky note on the monitor with the word: **login**\n"
                "That must be the key!\n\n"
                "Run the solver with that key, and redirect `>` the output to 'flag.txt'."
            ),
            command_template="python3 .solver.py login > flag.txt",
            
            # === FIX: Added the mandatory command_prefix ===
            command_prefix="python3 .solver.py",
            
            # We strictly enforce the full command via regex
            command_regex=r"^python3 \.solver\.py login > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 6: Verification
        bot.teach_step(
            instruction=(
                "Success! The tool decrypted the data and you safely stored it.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_local_solver()

if __name__ == "__main__":
    main()