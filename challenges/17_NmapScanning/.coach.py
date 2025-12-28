#!/usr/bin/env python3
import sys
import os
import subprocess
import re

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def main():
    bot = Coach("Network Mapper (nmap)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/17_Nmap"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: The Briefing
        bot.teach_step(
            instruction=(
                "We know there are services running on `localhost` between ports **8000 and 8100**.\n"
                "We don't know which specific ports are open.\n"
                "We need to scan the range to find the open doors."
            ),
            command_to_display="echo Understood"
        )

        # STEP 3: The Scan (Nmap)
        # 
        bot.teach_step(
            instruction=(
                "Run `nmap` against `localhost` specifying the port range with `-p`.\n"
                "   `nmap -p 8000-8100 localhost`\n\n"
                "Look for lines that say **open** in the STATE column."
            ),
            command_to_display="nmap -p 8000-8100 localhost"
        )

        # STEP 4: The Investigation (Curl)
        # We don't know exactly which ports are open (it's random), so we ask the user to investigate.
        bot.teach_loop(
            instruction=(
                "Nmap should have found a few open ports (e.g., 8022, 8045).\n"
                "Most of them contain fake data. One contains the flag.\n"
                "Use `curl` to check the open ports one by one until you find the flag!"
            ),
            # Template showing how to curl a specific port
            command_template="curl localhost:[PORT]",
            
            # We validate that they are running curl against localhost
            command_prefix="curl localhost:",
            
            # We use a regex to accept any port number they might try
            command_regex=r"curl localhost:\d+" 
        )

        # STEP 5: Verification
        bot.teach_step(
            instruction=(
                "Did you find the flag starting with `CCRI`?\n"
                "If so, you have successfully mapped and enumerated a network service.\n"
                "Great work!"
            ),
            command_to_display="echo Done"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()