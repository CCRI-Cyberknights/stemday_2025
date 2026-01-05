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
            print("\n❌ ERROR: The Web Server is not running!")
            print("This challenge requires the background web services.")
            print("👉 Please open a new terminal tab and run: python3 start_web_hub.py\n")
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
    with open(filename, "w") as f:
        f.write(content)

def cleanup_intel_file():
    if os.path.exists("server_logs.txt"):
        os.remove("server_logs.txt")
    if os.path.exists("flag.txt"):
        os.remove("flag.txt")

def main():
    check_web_server()

    bot = Coach("HTTP Header Detective (curl)")
    
    # Ensure fresh state
    cleanup_intel_file()
    create_intel_file()
    
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/13_HTTPHeaders"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/13_HTTPHeaders"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

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

        # STEP 4: The Concept (Manual Test)
        bot.teach_step(
            instruction=(
                "The logs show 5 endpoints (`endpoint_1` through `5`).\n"
                "The flag is hidden in a custom **Header**.\n\n"
                "Use `curl -I` (Fetch Headers Only) to inspect the first endpoint manually:"
            ),
            command_to_display="curl -I http://localhost:5000/mystery/endpoint_1"
        )

        # STEP 5: Automation (Curl Sequencing)
        bot.teach_step(
            instruction=(
                "You checked one, but we need to check **all 5**.\n"
                "Curl supports **Sequencing** using brackets `[]`.\n"
                "**Important:** You must wrap the URL in quotes `\"` so the shell doesn't break.\n\n"
                "Scan all 5 endpoints at once:"
            ),
            command_to_display="curl -I \"http://localhost:5000/mystery/endpoint_[1-5]\""
        )

        # STEP 6: Filter and Save
        bot.teach_loop(
            instruction=(
                "We scanned the list! Now let's filter the noise.\n"
                "1. Add `-s` (silent) to hide the progress bar.\n"
                "2. Pipe to `grep` to find 'CCRI'.\n"
                "3. **Save** the result to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            # Template showing the logic
            command_template="curl -I -s \"http://localhost:5000/mystery/endpoint_[1-5]\" | grep \"CCRI\" > flag.txt",
            
            # Prefix for visual hint
            command_prefix="curl -I -s ",
            
            # Regex match for the sequence command
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