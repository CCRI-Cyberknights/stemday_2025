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
        # Command: tshark -r traffic.pcap -Y "frame contains CCRI" -T fields -e tcp.stream
        # This asks tshark to list the stream IDs of any packet containing "CCRI"
        cmd = [
            "tshark", "-r", pcap_file, 
            "-Y", "frame contains CCRI", 
            "-T", "fields", "-e", "tcp.stream"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # We might get multiple packets from the same stream, so we just take the first one
        streams = result.stdout.strip().split()
        if streams:
            return streams[0]
            
    except FileNotFoundError:
        # Fail gracefully if tshark isn't installed (though it should be on Parrot)
        pass
    return "0" # Default fallback

def main():
    bot = Coach("Packet Analyzer (tshark)")
    
    # 1. Analyze the PCAP before starting to find the dynamic Stream ID
    target_stream = get_correct_stream_id("traffic.pcap")
    
    bot.start()

    try:
        # STEP 1: Navigation
        bot.teach_step(
            instruction=(
                "First, enter the challenge directory."
            ),
            command_to_display="cd challenges/18_PCAP"
        )
        
        # Sync directory
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        # STEP 2: Quick Scan (strings)
        bot.teach_step(
            instruction=(
                "We have a packet capture file: `traffic.pcap`.\n"
                "Before using complex tools, let's try the 'quick and dirty' method.\n"
                "Run `strings` on the pcap to see if the flag is in plain text."
            ),
            command_to_display="strings traffic.pcap | grep CCRI"
        )

        # STEP 3: The Problem (Context)
        bot.teach_step(
            instruction=(
                "You probably saw multiple flags or fragments.\n"
                "`strings` shows the text, but it loses the **context** (who sent it, and what was the reply).\n"
                "To see the full conversation, we need `tshark`.\n"
                "First, let's find the **TCP Stream ID** of the packets containing 'CCRI'."
            ),
            command_to_display="tshark -r traffic.pcap -Y \"frame contains CCRI\" -T fields -e tcp.stream"
        )

        # STEP 4: Follow TCP Stream
        # 
        bot.teach_loop(
            instruction=(
                f"The previous command identified that Stream **{target_stream}** contains the flag.\n"
                "Now we 'Follow the TCP Stream' to reconstruct the entire conversation (like reading a chat log).\n\n"
                "Command syntax: `tshark -r [FILE] -q -z follow,tcp,ascii,[STREAM_ID]`"
            ),
            # Template showing the correct ID
            command_template=f"tshark -r traffic.pcap -q -z follow,tcp,ascii,{target_stream}",
            
            # Prefix for validation
            command_prefix="tshark -r traffic.pcap -q -z follow,tcp,ascii,",
            
            # We explicitly check for the ID we found earlier
            correct_password=target_stream 
        )

        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()