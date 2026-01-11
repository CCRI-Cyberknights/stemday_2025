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
    """Creates a dummy intel file so the user has something to 'discover'."""
    filename = "active_portals.txt"
    content = (
        "--- INTERNAL NETWORK CONFIG ---\n"
        "Active Portals:\n"
        "- alpha\n"
        "- beta\n"
        "- gamma\n"
        "- delta\n"
        "- omega\n"
    )
    # Only create if it doesn't exist to avoid overwriting user changes
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(content)

def cleanup_intel_file():
    """Removes the intel file on exit to leave no trace."""
    if os.path.exists("active_portals.txt"):
        os.remove("active_portals.txt")
    if os.path.exists("flag.txt"):
        os.remove("flag.txt")

def main():
    check_web_server()

    bot = Coach("Source Code Hunter (curl)")
    
    # Ensure fresh state
    cleanup_intel_file()
    create_intel_file()
    
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/14_InternalPortals"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/14_InternalPortals"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # STEP 2: Discovery (Recon)
        bot.teach_step(
            instruction=(
                "We need to know what to attack.\n"
                "List the files. You should see an intel file named `active_portals.txt`."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: Read Intel
        bot.teach_step(
            instruction=(
                "Read `active_portals.txt` to find the names of the internal portals."
            ),
            command_to_display="cat active_portals.txt"
        )

        # STEP 4: The Test (Curl one)
        bot.teach_step(
            instruction=(
                "The file lists 5 portals: `alpha`, `beta`, `gamma`, `delta`, and `omega`.\n"
                "To view their source code, we use `curl`.\n\n"
                "Let's manually inspect the first one (`alpha`) to see what we are up against:"
            ),
            command_to_display="curl http://localhost:5000/internal/alpha"
        )

        # STEP 5: Automation (Brace Expansion)
        bot.teach_step(
            instruction=(
                "That was a mess of HTML. The flag is hidden in one of those 5 portals.\n"
                "Instead of typing 5 commands, we can use **Brace Expansion** `{}`.\n"
                "This tells the shell (and curl) to generate multiple URLs.\n\n"
                "Run this to download all 5 portals at once:"
            ),
            command_to_display="curl \"http://localhost:5000/internal/{alpha,beta,gamma,delta,omega}\""
        )

        # STEP 6: Filter and Save
        bot.teach_loop(
            instruction=(
                "We fetched them all! Now we filter the massive output:\n"
                "1. Add `-s` (silent) to clean up the output.\n"
                "2. Pipe to `grep` to find 'CCRI'.\n"
                "3. **Save** the result to 'flag.txt'.\n\n"
                "Construct the command:"
            ),
            # Template showing the logic
            command_template="curl -s \"http://localhost:5000/internal/{alpha,beta,gamma,delta,omega}\" | grep \"CCRI\" > flag.txt",
            
            # Prefix for visual hint
            command_prefix="curl -s ",
            
            # Regex to match the brace expansion command
            # Note: We escape the braces \{ \} for regex
            command_regex=r"^curl -s \"http://localhost:5000/internal/\{alpha,beta,gamma,delta,omega\}\" \| grep \"CCRI\" > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verify
        bot.teach_step(
            instruction=(
                "Success! You enumerated the targets, scanned them, and captured the flag.\n"
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