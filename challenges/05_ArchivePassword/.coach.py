#!/usr/bin/env python3
import sys
import os
import subprocess
import time

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
CRACKER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import sys
import subprocess
import time

if len(sys.argv) < 3:
    print("Usage: python3 .cracker.py [ZIP_FILE] [WORDLIST]")
    sys.exit(1)

zip_file = sys.argv[1]
wordlist = sys.argv[2]

print(f"Target:   {zip_file}")
print(f"Wordlist: {wordlist}")
print("-" * 40)
print("Starting Brute Force Attack...")
print("-" * 40)

try:
    with open(wordlist, "r", errors="ignore") as f:
        count = 0
        for line in f:
            password = line.strip()
            if not password: continue
            
            count += 1
            # VISUAL: Overwrite the line (\r) to show rapid-fire testing
            print(f"\r[Attempt #{count}] Testing: {password:<20}", end="")
            sys.stdout.flush()
            time.sleep(0.01) 

            res = subprocess.call(
                ["unzip", "-P", password, "-tq", zip_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if res == 0:
                print(f"\n\n{'='*40}")
                print(f"✅ PASSWORD CRACKED: {password}")
                print(f"{'='*40}")
                sys.exit(0)

    print("\n❌ Password not found in wordlist.")
    sys.exit(1)

except FileNotFoundError:
    print(f"\n❌ Error: Could not find {wordlist}")
    sys.exit(1)
"""

def create_local_cracker():
    """Writes the cracker script to the CURRENT working directory."""
    with open(".cracker.py", "w") as f:
        f.write(CRACKER_SCRIPT_CONTENT)

def cleanup_local_cracker():
    """Removes the cracker script from the CURRENT working directory."""
    if os.path.exists(".cracker.py"):
        os.remove(".cracker.py")

def determine_correct_password():
    """
    Runs a quick check in the CURRENT directory to find the real password.
    """
    zip_file = "secret.zip"
    wordlist = "wordlist.txt"

    if not os.path.exists(zip_file) or not os.path.exists(wordlist):
        return "unknown"

    try:
        with open(wordlist, "r", errors="ignore") as f:
            for line in f:
                password = line.strip()
                if not password: continue
                
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
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, move into the challenge directory.\n"
                "We need to find the locked zip file."
            ),
            command_to_display="cd challenges/05_ArchivePassword"
        )
        
        # === SYNC DIRECTORY & CREATE TOOL ===
        target_dir = "challenges/05_ArchivePassword"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        elif os.path.basename(os.getcwd()) == "05_ArchivePassword":
            pass
        else:
            bot.print_error(f"Could not find '{target_dir}'.")
            return

        create_local_cracker()
        real_password = determine_correct_password()
        # ====================================

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "List the files. You will see 'secret.zip' (the target) and 'wordlist.txt' (our weapon)."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Code Transparency
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
                "Now, launch the attack.\n"
                "**Watch the screen**: You will see it trying passwords one by one until it breaks the lock."
            ),
            command_to_display="python3 .cracker.py secret.zip wordlist.txt"
        )

        # STEP 5: Manual Extraction
        # FIXED: Removed 'correct_password' and added 'command_regex' to handle the full string
        bot.teach_loop(
            instruction=(
                f"It worked! The password is **{real_password}**.\n"
                "Now extract the files manually using the '-P' flag."
            ),
            command_template=f"unzip -P {real_password} secret.zip",
            
            # The prefix is still required by the Coach logic, but it won't be used for slicing
            command_prefix="unzip -P",
            
            # Strict regex validation for "unzip -P [pass] secret.zip"
            command_regex=fr"^unzip -P {real_password} secret\.zip$",
            
            clean_files=["message_encoded.txt"]
        )

        # STEP 6: Inspect the contents
        bot.teach_step(
            instruction="The zip contained 'message_encoded.txt'. Read it.",
            command_to_display="cat message_encoded.txt"
        )

        # STEP 7: Final Decode and Save
        bot.teach_loop(
            instruction=(
                "Decode the Base64 message and **save the output** to 'flag.txt'."
            ),
            command_template="base64 -d message_encoded.txt > flag.txt",
            command_prefix="base64 -d",
            command_regex=r"^base64 -d message_encoded\.txt > flag\.txt$",
            clean_files=["flag.txt"]
        )

        # STEP 8: Verification
        bot.teach_step(
            instruction="Success! Read 'flag.txt' to finish.",
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_local_cracker()

if __name__ == "__main__":
    main()