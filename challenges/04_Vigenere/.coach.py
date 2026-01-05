#!/usr/bin/env python3
import sys
import os
import time

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
TOOL_NAME = "decoder.py"
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

if len(sys.argv) < 3:
    print("Usage: python3 decoder.py <file> <key>")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f:
        data = f.read().strip()
    
    key = sys.argv[2]
    print(decrypt(data, key))
except Exception as e:
    print(f"Error: {e}")
"""

def create_tool():
    """Writes the solver to the CURRENT working directory."""
    with open(TOOL_NAME, "w") as f:
        f.write(SOLVER_SCRIPT_CONTENT)
    # Make it executable for good measure
    os.chmod(TOOL_NAME, 0o755)

def cleanup_tool():
    """Removes the solver to keep the directory clean."""
    if os.path.exists(TOOL_NAME):
        os.remove(TOOL_NAME)
    if os.path.exists("flag.txt"):
        try:
            os.remove("flag.txt")
        except:
            pass

def main():
    # Ensure clean state
    cleanup_tool()
    
    bot = Coach("Vigenère Cipher Breaker")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory."
            ),
            command_to_display="cd challenges/04_Vigenere"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/04_Vigenere"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction="Check the directory contents.",
            command_to_display="ls -l"
        )

        # STEP 3: Inspection
        bot.teach_step(
            instruction=(
                "Read the encrypted file.\n"
                "It looks like random letters. The README says this is Vigenère."
            ),
            command_to_display="cat cipher.txt"
        )

        # STEP 4: Tool Provisioning
        # The Coach explicitly provides the tool here, filling the gap in the generic README.
        print("\n[Coach] 🛠️  The README notes that you need a tool for this.")
        print("[Coach] 📡  I am generating a Python script named 'decoder.py' for you now...")
        create_tool()
        time.sleep(1)
        
        bot.teach_step(
            instruction=(
                "I have created `decoder.py`.\n"
                "Verify it is now in your directory."
            ),
            command_to_display="ls -l"
        )

        # STEP 5: Intel Analysis (Key Deduction)
        bot.teach_step(
            instruction=(
                "Vigenère requires a **Key**.\n"
                "The **Mission Brief** asks: *'What is the opposite of logout?'*\n"
                "The answer is **login**. That is our key.\n\n"
                "Acknowledge this intel."
            ),
            command_to_display="echo \"Key is login\""
        )

        # STEP 6: Execution
        bot.teach_loop(
            instruction=(
                "Now, run the decoder using the key we found.\n"
                "Redirect `>` the output to `flag.txt`.\n\n"
                "Syntax: `python3 decoder.py cipher.txt [KEY] > flag.txt`"
            ),
            # Template showing the args
            command_template="python3 decoder.py cipher.txt login > flag.txt",
            
            # Validation
            command_prefix="python3 decoder.py",
            command_regex=r"^python3 decoder\.py cipher\.txt login > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verification
        bot.teach_step(
            instruction=(
                "Success! The tool decrypted the data.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        # Cleanup acts as a "Secure Deletion" simulation
        if os.path.exists(TOOL_NAME):
            os.remove(TOOL_NAME)

if __name__ == "__main__":
    main()