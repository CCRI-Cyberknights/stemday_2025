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
        # Check port 5000 (main web challenges)
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
    # 1. Pre-flight Check: Ensure the target is actually up
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
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Concept
        bot.teach_step(
            instruction=(
                "We have discovered 5 active API endpoints running on `localhost:5000`.\n"
                "Web servers send invisible data called **Headers** before the actual content.\n"
                "The flag is hidden in a custom header (e.g., `X-Flag`).\n\n"
                "To see headers, we use `curl` with the `-I` (Info/Head) flag.\n"
                "Try inspecting the first endpoint."
            ),
            command_to_display="curl -I http://localhost:5000/mystery/endpoint_1"
        )

        # STEP 3: The Result
        # The user just ran it. They likely saw "200 OK" and "Server: Werkzeug", but no flag.
        bot.teach_step(
            instruction=(
                "You saw standard headers like `Content-Type` and `Server`, but no flag.\n"
                "The flag must be on one of the other endpoints (2, 3, 4, or 5).\n"
                "Checking them one by one is slow. We can use **Brace Expansion**."
            ),
            # Just an echo to confirm they are reading
            command_to_display="echo Understood"
        )

        # STEP 4: Automation (Brace Expansion)
        bot.teach_step(
            instruction=(
                "Bash allows us to generate a list of numbers using `{1..5}`.\n"
                "If we put that in the URL, `curl` will visit all 5 pages automatically!\n\n"
                "Run this command to scan all 5 endpoints at once."
            ),
            command_to_display="curl -I http://localhost:5000/mystery/endpoint_{1..5}"
        )

        # STEP 5: Filtering
        bot.teach_loop(
            instruction=(
                "That was fast! But reading all that output is hard.\n"
                "Let's combine our tools:\n"
                "1. `curl` to fetch the headers.\n"
                "2. `grep` to find the flag 'CCRI'.\n\n"
                "Construct the command!"
            ),
            # Template showing the pipeline
            command_template="curl -I http://localhost:5000/mystery/endpoint_{1..5} | grep CCRI",
            
            # Prefix for validation
            command_prefix="curl -I http://localhost:5000/mystery/endpoint_{1..5} | grep ",
            
            # The search term
            correct_password="CCRI" 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()