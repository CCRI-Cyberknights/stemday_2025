#!/usr/bin/env python3
import socket
import subprocess
import sys
import os
import time
import random
import re

HOST = '127.0.0.1'

class Coach:
    def __init__(self, challenge_name):
        self.challenge_name = challenge_name
        self.port = random.randint(30000, 40000)
        self.server_socket = None
        self.conn = None
        self.worker_process = None
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.worker_script = os.path.join(self.root_dir, "worker_node.py")

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, self.port))
        self.server_socket.listen(1)
        self._spawn_worker()
        print("⏳ Waiting for worker terminal...")
        self.conn, _ = self.server_socket.accept()
        print("✅ Connected!\n")
        print("========================================")
        print(f" 🎓 COACH MODE: {self.challenge_name}")
        print("========================================\n")

    def _spawn_worker(self):
        if not os.path.exists(self.worker_script):
            print(f"❌ Error: Missing {self.worker_script}")
            sys.exit(1)
        term_cmd = "mate-terminal"
        if subprocess.call(["which", "mate-terminal"], stdout=subprocess.DEVNULL) != 0:
            term_cmd = "x-terminal-emulator"
            
        cmd = [
            term_cmd, 
            f"--geometry=90x35+1000+100", 
            f"--title=Worker: {self.challenge_name}", 
            "--", 
            "python3", self.worker_script, str(self.port)
        ]
        
        try:
            self.worker_process = subprocess.Popen(cmd)
        except Exception as e:
            print(f"❌ Failed to launch terminal: {e}")
            sys.exit(1)

    def _clean_files(self, file_list):
        """Helper to silently remove files on the worker."""
        if not file_list: return
        cmd = "rm -f " + " ".join(file_list)
        # Send with SILENT prefix
        self.conn.sendall(f"SILENT:{cmd}".encode('utf-8'))
        _ = self.conn.recv(1024) # Wait for DONE

    def teach_step(self, instruction, command_to_display, command_regex=None, clean_files=None):
        """Standard 'Do exactly this' step."""
        if clean_files: self._clean_files(clean_files)

        print(f"\n\033[96m{instruction}\033[0m")
        print(f"\n👉 Type exactly this command:\n   \033[1;93m{command_to_display}\033[0m")

        while True:
            user_input = input("\n> ").strip()
            
            valid = False
            if command_regex:
                if isinstance(command_regex, str):
                    if re.search(command_regex, user_input): valid = True
                else: 
                    if any(re.search(p, user_input) for p in command_regex): valid = True
            else:
                if user_input == command_to_display: valid = True

            if valid:
                print("✅ Correct.")
                self.conn.sendall(command_to_display.encode('utf-8'))
                _ = self.conn.recv(1024)
                return
            else:
                print(f"❌ Incorrect. Please type exactly: \033[1;93m{command_to_display}\033[0m")

    def teach_loop(self, instruction, command_template, command_prefix, correct_password, clean_files=None):
        """
        Interactive loop for guessing variables.
        clean_files: List of filenames to silently delete before user attempts command.
        """
        print(f"\n\033[96m{instruction}\033[0m")
        print(f"\n👉 Use this format (replace [PASSWORD]):\n   \033[1;93m{command_template}\033[0m")

        while True:
            user_input = input("\n> ").strip()

            # 1. Syntax Check
            if not user_input.startswith(command_prefix):
                 print(f"❌ Syntax Error. The command must start exactly like this:\n   \033[1;93m{command_prefix}...\033[0m")
                 continue
            
            # 2. Cleanup (Silent)
            # We clean before EVERY attempt so the tool never prompts for overwrite
            if clean_files: self._clean_files(clean_files)

            # 3. Run it
            print("⏳ Executing...")
            self.conn.sendall(user_input.encode('utf-8'))
            _ = self.conn.recv(1024) # Wait for DONE signal

            # 4. Success Check
            user_password = user_input[len(command_prefix):].strip()
            
            if user_password == correct_password:
                print("✅ Excellent! Password accepted.")
                return
            else:
                print(f"⚠️  Command ran, but '{user_password}' is not the correct password. Try again!")

    def finish(self):
        print("\n🎉 \033[1;32mMISSION COMPLETE!\033[0m")
        print("You have successfully completed this guided exercise.")
        input("\nPress [ENTER] to close these windows and return to the dashboard...")
        if self.conn:
            try: self.conn.sendall(b"EXIT")
            except: pass
            self.conn.close()
        if self.server_socket: self.server_socket.close()