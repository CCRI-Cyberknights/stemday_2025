#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil

def find_project_root():
    dir_path = os.path.abspath(os.getcwd())
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?")
    sys.exit(1)

def launch_flask_server(server_path, log_file):
    print(f"🌐 Launching Flask web server from: {server_path}")
    # Start the Flask server as a detached process
    with open(log_file, "w") as log:
        subprocess.Popen(
            [sys.executable, server_path],
            stdout=log,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp  # Detach from parent process group
        )
    time.sleep(2)  # Give Flask time to start
    try:
        subprocess.check_call(
            ["curl", "-s", "http://localhost:5000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ Flask server started successfully.")
    except subprocess.CalledProcessError:
        print(f"❌ ERROR: Flask server failed to start. Check logs at: {log_file}")
        sys.exit(1)

def open_browser():
    print("🌐 Opening browser to http://localhost:5000 ...")
    firefox = shutil.which("firefox")
    if firefox:
        try:
            # Launch Firefox in a new window, fully detached
            subprocess.Popen(
                [firefox, "--new-window", "http://localhost:5000"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )
            print("✅ Firefox launched successfully.")
            return
        except Exception as e:
            print(f"⚠️ Could not launch Firefox: {e}")
    else:
        print("⚠️ Firefox not found. Trying xdg-open...")
        if shutil.which("xdg-open"):
            subprocess.Popen(
                ["xdg-open", "http://localhost:5000"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Browser launched using xdg-open.")
        else:
            print("❌ No browser launcher found. Please open manually: http://localhost:5000")

def main():
    print("🚀 Starting the CCRI CTF Hub...\n")
    project_root = find_project_root()

    # Detect mode
    if os.path.isdir(os.path.join(project_root, "web_version_admin")):
        print("🛠️ Admin/Dev environment detected (web_version_admin found).\n")
        print("Which mode would you like to run?")
        print("1) 🛠️ Admin Mode (full tools, editable flags)")
        print("2) 🎓 Student Mode (restricted, obfuscated flags)\n")
        mode_choice = input("Enter choice [1-2]: ").strip()
        if mode_choice == "1":
            server_dir = os.path.join(project_root, "web_version_admin")
            server_file = "server.py"
        elif mode_choice == "2":
            server_dir = os.path.join(project_root, "web_version")
            server_file = "server.pyc"
        else:
            print("❌ Invalid choice. Exiting.")
            sys.exit(1)
    else:
        print("🎓 Student environment detected (web_version_admin not found).")
        server_dir = os.path.join(project_root, "web_version")
        server_file = "server.pyc"

    server_path = os.path.join(server_dir, server_file)
    if not os.path.isfile(server_path):
        print(f"❌ ERROR: Cannot find {server_file} in {server_dir}")
        sys.exit(1)

    # Check if Flask server already running
    try:
        subprocess.check_call(
            ["lsof", "-i:5000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("🌐 Flask web server is already running. Skipping launch.")
    except subprocess.CalledProcessError:
        log_file = os.path.join(project_root, "web_server.log")
        launch_flask_server(server_path, log_file)

    open_browser()
    print("✅ CCRI CTF Hub is ready!")

if __name__ == "__main__":
    main()
