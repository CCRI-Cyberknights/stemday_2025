#!/usr/bin/env python3
import sys
import os
import subprocess

# Add root to path to find coach_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def get_correct_stream_id(pcap_file):
    """
    Uses tshark to find which TCP stream actually contains the flag 'CCRI'.
    Returns the stream ID (e.g., '2') as a string.
    """
    if not os.path.exists(pcap_file):
        return "0"
        
    try:
        # We must carefully quote "CCRI" inside the filter so tshark treats it as a string
        # Filter: frame contains "CCRI"
        cmd = [
            "tshark", "-r", pcap_file, 
            "-Y", 'frame contains "CCRI"', 
            "-T", "fields", "-e", "tcp.stream"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # We might get multiple packets from the same stream, so we just take the first one
        streams = result.stdout.strip().split()
        if streams:
            return streams[0]
            
    except FileNotFoundError:
        pass
    return "0" 

def main():
    bot = Coach("Packet Analyzer (tshark)")
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/18_PcapSearch"
        )
        
        # === SYNC DIRECTORY ===
        target_dir = "challenges/18_PcapSearch"
        if os.path.exists(target_dir):
            os.chdir(target_dir)
        # ======================

        # Detect the stream ID dynamically
        target_stream = get_correct_stream_id("traffic.pcap")

        # STEP 2: Discovery
        bot.teach_step(
            instruction=(
                "Let's see what we are dealing with."
            ),
            command_to_display="ls -l"
        )

        # STEP 3: The "Quick" Way (Strings)
        bot.teach_step(
            instruction=(
                "We have `traffic.pcap`. Let's try the 'lazy' method first.\n"
                "Run `strings` to pull all text out of the file."
            ),
            command_to_display="strings traffic.pcap | grep CCRI"
        )

        # STEP 4: The Forensics Lesson (Syntax Fix)
        bot.teach_step(
            instruction=(
                "**Analysis:** `strings` found the text, but stripped the context (IPs, Ports, Time).\n"
                "We need `tshark` to find the **TCP Stream ID** so we can reconstruct the full conversation.\n\n"
                "**Note on Syntax:** We use `'single quotes'` to wrap the command so the `\"double quotes\"` get passed to tshark correctly."
            ),
            # FIX: Using 'frame contains "CCRI"' to satisfy tshark syntax
            command_to_display="tshark -r traffic.pcap -Y 'frame contains \"CCRI\"' -T fields -e tcp.stream"
        )

        # STEP 5: Reconstruct the Stream
        bot.teach_loop(
            instruction=(
                f"The flag is inside Stream **{target_stream}**.\n"
                "Now, let's 'Follow the Stream' to see the full conversation context.\n"
                "This will show us the HTTP Headers (proving it was a web server).\n\n"
                "Construct the command:\n"
                "1. Read file: `-r traffic.pcap`\n"
                "2. Quiet mode: `-q`\n"
                "3. Follow Stream: `-z follow,tcp,ascii,[STREAM_ID]`"
            ),
            # Template showing the correct ID
            command_template=f"tshark -r traffic.pcap -q -z follow,tcp,ascii,{target_stream}",
            
            # Prefix for validation
            command_prefix="tshark -r traffic.pcap -q -z follow,tcp,ascii,",
            
            # Regex ensures they use the correct stream ID
            command_regex=rf"^tshark -r traffic\.pcap -q -z follow,tcp,ascii,{target_stream}$"
        )

        # STEP 6: Save Evidence
        bot.teach_loop(
            instruction=(
                "Look at the output! You can see `HTTP/1.1 200 OK`.\n"
                "This proves the flag came from a web server response.\n\n"
                "Run the command again and save the full evidence to `flag.txt`."
            ),
            command_template=f"tshark -r traffic.pcap -q -z follow,tcp,ascii,{target_stream} > flag.txt",
            
            command_prefix="tshark",
            
            # Regex for the redirect
            command_regex=rf"^tshark -r traffic\.pcap -q -z follow,tcp,ascii,{target_stream} > flag\.txt$",
            
            clean_files=["flag.txt"]
        )

        # STEP 7: Verify
        bot.teach_step(
            instruction=(
                "Success! You reconstructed the packet stream and captured the forensic evidence.\n"
                "Read 'flag.txt' to finish."
            ),
            command_to_display="cat flag.txt"
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()