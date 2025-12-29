#!/usr/bin/env python3
import sys
import os
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from coach_core import Coach

def check_web_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex(('127.0.0.1', 5000)) != 0:
            print("\n❌ ERROR: Web Server not running! Run 'python3 start_web_hub.py' first.\n")
            sys.exit(1)
        sock.close()
    except: pass

def main():
    check_web_server()
    bot = Coach("Network Mapper (nmap)")
    bot.start()

    try:
        bot.teach_step(
            instruction="First, enter the challenge directory.",
            command_to_display="cd challenges/17_NmapScanning"
        )
        os.chdir(os.path.join(os.path.dirname(__file__))) 

        bot.teach_step(
            instruction="We need to scan ports 8000-8100.",
            command_to_display="echo Understood"
        )

        bot.teach_step(
            instruction="Run `nmap` against `localhost` with the port range.",
            command_to_display="nmap -p 8000-8100 localhost"
        )

        # ANCHORED REGEX for curl
        bot.teach_loop(
            instruction="Use `curl` to check the open ports found by nmap.",
            command_template="curl localhost:[PORT]",
            command_prefix="curl localhost:",
            command_regex=r"^curl localhost:\d+$" 
        )

        bot.teach_step(
            instruction="Did you find the flag?",
            command_to_display="echo Done"
        )
        bot.finish()

    except KeyboardInterrupt:
        bot.finish()

if __name__ == "__main__":
    main()