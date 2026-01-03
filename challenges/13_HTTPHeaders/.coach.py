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

def create_intel_file():
    """Creates a dummy log file to reveal the endpoints."""
    filename = "server_logs.txt"
    content = (
        "[INFO] Server started on port 5000\n"
        "[INFO] Deployment successful.\n"
        "[DEBUG] Active API Routes:\n"
        " - /mystery/endpoint_1  (Status: Active)\n"
        " - /mystery/endpoint_2  (Status: Active)\n"
        " - /mystery/endpoint_3  (Status: Active)\n"
        " - /mystery/endpoint_4  (Status: Active)\n"
        " - /mystery/endpoint_5  (Status: Active)\n"
    )
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(content)

def cleanup_intel_file():
    if os.path.exists("server_logs.txt"):
        os.remove("server_logs.txt")

def main():
    check_web_server()

    bot = Coach("HTTP Header Detective (curl)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/13_HTTPHeaders"
        )
        
        # === SYNC & SETUP ===
        target_dir = "challenges/13_HTTPHeaders"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        
        create_intel_file()
        # ====================

        # STEP 2: Discovery (Recon)
        bot.teach_step(
            instruction=(
                "We need to find the API endpoints.\n"
                "List the files. You should see `server_logs.txt`."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Read Logs
        bot.teach_step(
            instruction=(
                "Read the log file to identify our targets."
            ),
            command_to_display="cat server_logs.txt"
        )

        # STEP 4: The Concept
        bot.teach_step(
            instruction=(
                "The logs show 5 endpoints: `endpoint_1` through `endpoint_5`.\n"
                "The flag is hidden in a custom **Header** (e.g., `X-Flag`).\n\n"
                "To see headers, we use `curl` with the `-I` (Info) flag.\n"
                "Test the first endpoint manually:"
            ),
            command_to_display="curl -I http://localhost:5000/mystery/endpoint_1"
        )

        # STEP 5: Automation (Curl Sequencing)
        bot.teach_step(
            instruction=(
                "You checked one, but to be thorough, we must check **all 5**.\n"
                "Since the logs showed a clear pattern (1-5), we can use `curl`'s built-in sequencer `[1-5]`.\n\n"
                "**Note:** Use quotes `\"` to protect the brackets from the shell.\n"
                "Scan all 5 endpoints at once:"
            ),
            command_to_display="curl -I \"http://localhost:5000/mystery/endpoint_[1-5]\""
        )

        # STEP 6: Filter and Save
        bot.teach_loop(
            instruction=(
                "We successfully scanned the whole list!\n"
                "Now filter the output to find the 'CCRI' flag:\n"
                "1. Add `-s` (silent) to clean up the output.\n"
                "2. Pipe to `grep` to find 'CCRI'.\n"
                "3. **Save** the result to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            # Template
            command_template="curl -I -s \"http://localhost:5000/mystery/endpoint_[1-5]\" | grep \"CCRI\" > flag.txt",
            
            # Prefix
            command_prefix="curl -I -s ",
            
            # Regex match
            command_regex=r"^curl -I -s \"http://localhost:5000/mystery/endpoint_\[1-5\]\" \| grep \"CCRI\" > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verify
        bot.teach_step(
            instruction=(
                "Success! You automated the scan and captured the flag.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()
    finally:
        cleanup_intel_file()

if __name__ == "__main__":
    main()