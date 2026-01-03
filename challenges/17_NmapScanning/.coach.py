#!/usr/bin/env python3
import sys
import os
import socket

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def check_web_server():
    """Checks if the CTF web server is running on port 5000."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result != 0:
            print("\n\033[91m❌ ERROR: The Web Server is not running!\033[0m")
            print("This challenge requires the background web services.")
            print("👉 Please open a new terminal tab and run: \033[1;93mpython3 start_web_hub.py\033[0m\n")
            sys.exit(1)
    except Exception:
        pass

def main():
    check_web_server()
    bot = Coach("Network Mapper (nmap)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/17_NmapScanning"
        )
        
        # Sync directory
        if os.path.exists("challenges/17_NmapScanning"):
            os.chdir("challenges/17_NmapScanning")

        # STEP 2: The Intel
        bot.teach_step(
            instruction=(
                "Good hackers read documentation before attacking.\n"
                "The `README.md` file contains the intelligence for this mission.\n\n"
                "Read it to find out which ports we need to scan."
            ),
            command_to_display="cat README.md"
        )

        # STEP 3: The Scan
        bot.teach_step(
            instruction=(
                "The README states services are listening between ports **8000 and 8100**.\n"
                "Run `nmap` focused on just that specific range."
            ),
            command_to_display="nmap -p 8000-8100 localhost"
        )

        # STEP 4: Enumeration Loop (The Human Verification)
        found_it = False
        
        while not found_it:
            # 4a. Ask them to check a port
            bot.teach_loop(
                instruction=(
                    "You found multiple open ports! Most are decoys.\n"
                    "We need to check them one by one.\n\n"
                    "Pick an open port from the list above and `curl` it (e.g., `curl localhost:8042`).\n"
                    "Check the output for 'CCRI-...'."
                ),
                command_template="curl localhost:[PORT]",
                command_prefix="curl localhost:",
                command_regex=r"^curl localhost:\d+$"
            )

            # 4b. Ask the user for confirmation (Explicit)
            print("\n" + "="*50)
            user_response = input("❓ Did you see the flag 'CCRI-...' in the output? (type yes or no): ").strip().lower()
            print("="*50 + "\n")

            # We check for 'yes' (and 'y' just in case)
            if user_response == 'yes' or user_response == 'y':
                found_it = True
            else:
                print("❌ Okay, that was a decoy. Let's try another port.\n")

        # STEP 5: The Capture
        bot.teach_loop(
            instruction=(
                "Great work finding the needle in the haystack!\n"
                "Now, run that **specific command** again, but add `> flag.txt` to save the evidence."
            ),
            command_template="curl localhost:[CORRECT_PORT] > flag.txt",
            command_prefix="curl localhost:",
            command_regex=r"^curl localhost:\d+ > flag\.txt$",
            clean_files=["flag.txt"]
        )

        # STEP 6: Verify
        bot.teach_step(
            instruction=(
                "Success! You filtered out the decoys and captured the real target.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()