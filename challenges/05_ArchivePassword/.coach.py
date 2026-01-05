#!/usr/bin/env python3
import sys
import os
import subprocess
import time

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

# === THE EPHEMERAL TOOL CODE ===
TOOL_NAME = "cracker.py"
CRACKER_SCRIPT_CONTENT = r"""#!/usr/bin/env python3
import sys
import subprocess
import time

if len(sys.argv) < 3:
    print("Usage: python3 cracker.py [ZIP_FILE] [WORDLIST]")
    sys.exit(1)

zip_file = sys.argv[1]
wordlist = sys.argv[2]

print(f"Target:   {zip_file}")
print(f"Wordlist: {wordlist}")
print("-" * 40)
print("Starting Dictionary Attack...")
print("-" * 40)

try:
    with open(wordlist, "r", errors="ignore") as f:
        count = 0
        for line in f:
            password = line.strip()
            if not password: continue
            
            count += 1
            print(f"\r[Attempt #{count}] Testing: {password:<20}", end="")
            sys.stdout.flush()
            time.sleep(0.005)

            # Check password using unzip test (-t)
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

def create_tool():
    """Writes the cracker script to the CURRENT working directory."""
    with open(TOOL_NAME, "w") as f:
        f.write(CRACKER_SCRIPT_CONTENT)
    os.chmod(TOOL_NAME, 0o755)

def cleanup_tool():
    """Removes the cracker script."""
    if os.path.exists(TOOL_NAME):
        os.remove(TOOL_NAME)
    if os.path.exists("flag.txt"):
        try:
            os.remove("flag.txt")
        except:
            pass
    if os.path.exists("message_encoded.txt"):
        try:
            os.remove("message_encoded.txt")
        except:
            pass

def determine_correct_password():
    """Quietly finds the password so the Coach can validate user input."""
    zip_file = "secret.zip"
    wordlist = "wordlist.txt"
    if not os.path.exists(zip_file) or not os.path.exists(wordlist):
        return "unknown"
    try:
        with open(wordlist, "r", errors="ignore") as f:
            for line in f:
                password = line.strip()
                if not password: continue
                res = subprocess.call(["unzip", "-P", password, "-tq", zip_file],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res == 0: return password
    except:
        pass
    return "unknown" 

def main():
    cleanup_tool() # Clean slate
    
    bot = Coach("Archive Password Cracker")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction="Move into the challenge directory.",
            command_to_display="cd challenges/05_ArchivePassword"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/05_ArchivePassword"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery
        bot.teach_step(
            instruction="List the files. We have 'secret.zip' and 'wordlist.txt'.",
            command_to_display="ls -l"
        )

        # STEP 3: Tool Provisioning (The Logic Fix)
        # The README says "You need a tool". The Coach says "Here it is."
        print("\n[Coach] 🧠  The Mission Brief says we need to perform a Dictionary Attack.")
        print("[Coach] ⚠️   Doing this manually is impossible.")
        print("[Coach] 📡  I am generating a Python script named 'cracker.py' for you now...")
        create_tool()
        time.sleep(1)

        bot.teach_step(
            instruction="I have created `cracker.py`. Verify it is there.",
            command_to_display="ls -l"
        )

        # STEP 4: Execution
        bot.teach_step(
            instruction=(
                "Launch the attack.\n"
                "Watch it test the passwords from the list against the zip."
            ),
            command_to_display="python3 cracker.py secret.zip wordlist.txt"
        )

        # === Determine Real Password ===
        real_password = determine_correct_password()
        # ===============================

        # STEP 5: Manual Extraction
        bot.teach_loop(
            instruction=f"It worked! The password is **{real_password}**. Extract the file now.",
            command_template=f"unzip -P {real_password} secret.zip",
            command_prefix="unzip -P",
            command_regex=fr"^unzip -P {real_password} secret\.zip$",
            clean_files=["message_encoded.txt"]
        )

        # STEP 6: Inspection
        bot.teach_step(
            instruction="The zip contained 'message_encoded.txt'. Read it.",
            command_to_display="cat message_encoded.txt"
        )

        # STEP 7: Final Decode
        bot.teach_loop(
            instruction="That is Base64. Decode it and save to 'flag.txt'.",
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
        cleanup_tool()

if __name__ == "__main__":
    main()