#!/usr/bin/env python3
import sys
import os
import subprocess

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
# Heavily commented for educational transparency
CRACKER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import sys
import subprocess

# This script performs a "Dictionary Attack".
# It reads a list of passwords and tries them one by one against the ZIP file.

if len(sys.argv) < 3:
    print("Usage: python3 .cracker.py [ZIP_FILE] [WORDLIST]")
    sys.exit(1)

zip_file = sys.argv[1]
wordlist = sys.argv[2]

print(f"🔨 Starting dictionary attack on {zip_file}...")
print(f"📖 Using wordlist: {wordlist}")
print("-" * 40)

try:
    with open(wordlist, "r", errors="ignore") as f:
        count = 0
        for line in f:
            password = line.strip()
            if not password: continue
            
            count += 1
            if count % 50 == 0:
                print(f"\rTrying password #{count}...", end="")

            # === THE CORE ATTACK ===
            # We run the Linux 'unzip' command in "test mode" (-t).
            # If the exit code is 0, the password was correct.
            res = subprocess.call(
                ["unzip", "-P", password, "-tq", zip_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if res == 0:
                print(f"\n\n✅ Password found: {password}")
                sys.exit(0)

    print("\n❌ Password not found in wordlist.")
    sys.exit(1)

except FileNotFoundError:
    print(f"\n❌ Error: Could not find {wordlist}")
    sys.exit(1)
"""

def create_tool():
    """Writes the temporary cracker script."""
    tool_path = os.path.join(os.path.dirname(__file__), ".cracker.py")
    with open(tool_path, "w") as f:
        f.write(CRACKER_SCRIPT_CONTENT)
    return tool_path

def cleanup_tool():
    """Removes the temporary cracker script."""
    tool_path = os.path.join(os.path.dirname(__file__), ".cracker.py")
    if os.path.exists(tool_path):
        os.remove(tool_path)

def determine_correct_password():
    """
    Runs the cracking logic internally ONCE so the Coach knows the answer.
    This ensures the script works even if you change the secret.zip password later.
    """
    base_dir = os.path.dirname(__file__)
    zip_file = os.path.join(base_dir, "secret.zip")
    wordlist = os.path.join(base_dir, "wordlist.txt")

    try:
        with open(wordlist, "r", errors="ignore") as f:
            for line in f:
                password = line.strip()
                res = subprocess.call(
                    ["unzip", "-P", password, "-tq", zip_file],
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                if res == 0:
                    return password
    except:
        pass
    return "unknown" 

def main():
    bot = Coach("Archive Password Cracker")
    
    # 1. Pre-flight: Determine the password so we can validate user input later
    real_password = determine_correct_password()
    
    bot.start()
    create_tool()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory.\n"
                "We need to find the locked zip file."
            ),
            command_to_display="cd challenges/05_ArchivePassword"
        )
        
        # SYNC DIRECTORY
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "List the files. You will see 'secret.zip' (the target) and 'wordlist.txt' (our weapon)."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Code Transparency (NEW STEP)
        bot.teach_step(
            instruction=(
                "We have a tool called '.cracker.py'.\n"
                "Before running it, let's see how it works.\n"
                "Read the code and look for `subprocess.call`. That is where it runs 'unzip' to test each password."
            ),
            command_to_display="cat .cracker.py"
        )

        # STEP 4: The Ephemeral Tool (Cracking)
        bot.teach_step(
            instruction=(
                "Now that you see how it works, let's run the dictionary attack.\n"
                "We give it the target (secret.zip) and the wordlist."
            ),
            command_to_display="python3 .cracker.py secret.zip wordlist.txt"
        )

        # STEP 5: Manual Extraction
        bot.teach_loop(
            instruction=(
                "The tool found the password!\n"
                "Now we need to extract the files manually using 'unzip'.\n"
                "We use the '-P' flag to provide the password we just found."
            ),
            # Template
            command_template="unzip -P [PASSWORD] secret.zip",
            
            # Prefix
            command_prefix="unzip -P ",
            
            # Validation (using the password we discovered at startup)
            correct_password=real_password,
            
            # Clean up previous extractions so unzip doesn't prompt for overwrite
            clean_files=["message_encoded.txt"]
        )

        # STEP 6: Inspect the contents
        bot.teach_step(
            instruction=(
                "The zip contained a file called 'message_encoded.txt'.\n"
                "Let's look at it using 'cat'."
            ),
            command_to_display="cat message_encoded.txt"
        )

        # STEP 7: Final Decode
        bot.teach_step(
            instruction=(
                "That looks like Base64 again (random characters ending in '=').\n"
                "Decode it to reveal the flag!"
            ),
            command_to_display="base64 -d message_encoded.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_tool()

if __name__ == "__main__":
    main()