#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import shutil

# === CCRI CTF Hub Stopper (Python Edition) ===

def find_project_root():
    """Walk upwards to find the .ccri_ctf_root marker."""
    dir_path = os.path.abspath(os.getcwd())
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?")
    sys.exit(1)

def kill_processes_by_pattern(pattern):
    """Find and kill processes matching a pattern (no prompt)."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", pattern],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        pids = result.stdout.strip().splitlines()
        if pids:
            print(f"⚠️ Found matching process(es): {' '.join(pids)}")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"✅ Killed process {pid}.")
                except ProcessLookupError:
                    print(f"⚠️ Process {pid} already stopped.")
        else:
            print(f"⚠️ No processes found matching: {pattern}")
    except FileNotFoundError:
        print("❌ ERROR: 'pgrep' not found on this system.")
    except Exception as e:
        print(f"❌ ERROR killing processes: {e}")

def clear_port(port):
    """Kill any process listening on a given port (no prompt)."""
    if not shutil.which("lsof"):
        print("⚠️ WARNING: 'lsof' not found. Skipping port cleanup.")
        return

    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        pids = result.stdout.strip().splitlines()
        if pids:
            print(f"⚠️ Found process(es) on port {port}: {' '.join(pids)}")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"✅ Cleared process {pid} on port {port}.")
                except ProcessLookupError:
                    print(f"⚠️ Process {pid} already stopped.")
        else:
            print(f"⚠️ No processes found on port {port}.")
    except Exception as e:
        print(f"❌ ERROR clearing port {port}: {e}")

def main():
    print("🛑 Stopping CCRI CTF Hub...\n")
    project_root = find_project_root()

    # Stop Flask server processes (Admin or Student)
    print("🔍 Searching for running Flask server processes...")
    kill_processes_by_pattern("python3.*server.py")  # Matches Admin server
    kill_processes_by_pattern("python3.*server.pyc") # Matches Student server

    # Stop Flask on port 5000 (backup)
    print("🔍 Checking for processes on port 5000...")
    clear_port(5000)

    # Stop simulated services (Guided: 8000–8100)
    print("🔍 Checking for simulated services on ports 8000–8100...")
    guided_ports_cleared = 0
    for port in range(8000, 8101):
        try:
            result = subprocess.run(
                ["lsof", "-iTCP:%d" % port, "-sTCP:LISTEN"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            if result.stdout.strip():
                clear_port(port)
                guided_ports_cleared += 1
        except Exception:
            break

    if guided_ports_cleared > 0:
        print(f"✅ Cleared {guided_ports_cleared} simulated service(s) on ports 8000–8100.")
    else:
        print("⚠️ No simulated services running on ports 8000–8100.")

    # Stop simulated services (Solo: 9000–9100)
    print("🔍 Checking for simulated services on ports 9000–9100...")
    solo_ports_cleared = 0
    for port in range(9000, 9101):
        try:
            result = subprocess.run(
                ["lsof", "-iTCP:%d" % port, "-sTCP:LISTEN"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            if result.stdout.strip():
                clear_port(port)
                solo_ports_cleared += 1
        except Exception:
            break

    if solo_ports_cleared > 0:
        print(f"✅ Cleared {solo_ports_cleared} simulated service(s) on ports 9000–9100.")
    else:
        print("⚠️ No simulated services running on ports 9000–9100.")

    print("\n🎯 All cleanup complete.")

if __name__ == "__main__":
    main()
