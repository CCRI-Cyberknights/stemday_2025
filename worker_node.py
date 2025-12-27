#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import time

def main():
    if len(sys.argv) < 2:
        return 

    host = '127.0.0.1'
    port = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        time.sleep(1) 
        s.connect((host, port))
    except:
        return

    # Info for the prompt
    user = os.getenv('USER', 'student')
    
    print(f"🔗 Connected to Coach.")
    print("💻 Commands entered in the Coach window will execute here.\n")

    while True:
        # Dynamic CWD for prompt
        cwd = os.getcwd()
        if cwd.startswith(os.path.expanduser("~")):
            display_cwd = "~" + cwd[len(os.path.expanduser("~")):]
        else:
            display_cwd = cwd

        # Receive Command
        data = s.recv(4096).decode('utf-8')
        if not data or data == "EXIT":
            print("\n👋 Session ended.")
            break

        # === SILENT COMMAND HANDLER ===
        # If the command starts with SILENT:, we run it but DO NOT show it.
        if data.startswith("SILENT:"):
            silent_cmd = data[7:] # Strip prefix
            try:
                # Run purely in background
                subprocess.run(silent_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
            # Always send DONE so coach knows we finished the cleanup
            s.sendall(b"DONE")
            continue
        # ==============================

        # Normal Prompt Display
        prompt = f"\033[1;32m{user}@term\033[0m:\033[1;34m{display_cwd}\033[0m$ "
        print(prompt, end="", flush=True)

        # Typing effect
        for char in data:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01) 
        print() 

        # 'cd' Handler
        if data.strip().startswith("cd "):
            path = data.strip()[3:].strip()
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"❌ bash: cd: {path}: No such file or directory")
            except Exception as e:
                print(f"❌ cd error: {e}")
            s.sendall(b"DONE")
            continue

        # Execute standard commands
        try:
            subprocess.run(data, shell=True)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        s.sendall(b"DONE")

    s.close()

if __name__ == "__main__":
    main()