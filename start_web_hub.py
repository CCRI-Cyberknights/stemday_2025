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
    with open(log_file, "w") as log:
        subprocess.Popen(
            [sys.executable, server_path],
            stdout=log,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp
        )
    time.sleep(2)
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
    elif shutil.which("xdg-open"):
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

    has_admin = os.path.isdir(os.path.join(project_root, "web_version_admin"))
    has_student = os.path.isdir(os.path.join(project_root, "web_version"))

    if has_admin and has_student:
        print("🧭 Both Admin and Student environments detected.")
        choice = input("🔄 Launch which mode? [1] Admin [2] Student (default): ").strip()
        base_mode = "admin" if choice == "1" else "student"
    elif has_admin:
        print("🛠️ Only Admin environment detected.")
        base_mode = "admin"
    elif has_student:
        print("🎓 Only Student environment detected.")
        base_mode = "student"
    else:
        print("❌ ERROR: No valid web_version or web_version_admin folder found.")
        sys.exit(1)

    os.environ["CCRI_CTF_MODE"] = base_mode
    server_dir = os.path.join(project_root, "web_version_admin" if base_mode == "admin" else "web_version")
    server_file = "server.py" if base_mode == "admin" else "server.pyc"
    server_path = os.path.join(server_dir, server_file)

    if not os.path.isfile(server_path):
        print(f"❌ ERROR: Cannot find {server_file} in {server_dir}")
        sys.exit(1)

    try:
        subprocess.check_call(["lsof", "-i:5000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🌐 Flask web server is already running. Skipping launch.")
    except subprocess.CalledProcessError:
        log_file = os.path.join(project_root, "web_server.log")
        launch_flask_server(server_path, log_file)

    open_browser()
    print("✅ CCRI CTF Hub is ready!")

if __name__ == "__main__":
    main()
