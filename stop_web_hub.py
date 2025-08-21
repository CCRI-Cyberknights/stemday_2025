#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import shutil
import time

# === CCRI CTF Hub Stopper (pyz + admin-safe) ===

PATTERNS = [
    r"python.*ccri_ctf\.pyz",   # Student zipapp
    r"python.*web_version_admin/server\.py",  # Admin server
    r"/usr/bin/python.*ccri_ctf\.pyz",
    r"/usr/bin/python.*web_version_admin/server\.py",
]

GUIDED_PORT_RANGE = (8000, 8100)
SOLO_PORT_RANGE   = (9000, 9100)
WEB_PORT          = 5000

def find_project_root():
    """Walk upwards to find the .ccri_ctf_root marker."""
    dir_path = os.path.abspath(os.getcwd())
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?")
    sys.exit(1)

def pids_from_pattern(pattern: str):
    """Return a list of PIDs matching a pgrep -f pattern."""
    try:
        res = subprocess.run(
            ["pgrep", "-f", pattern],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        if res.returncode != 0 or not res.stdout.strip():
            return []
        return [int(x) for x in res.stdout.strip().splitlines() if x.strip().isdigit()]
    except FileNotFoundError:
        print("❌ ERROR: 'pgrep' not found.")
        return []
    except Exception as e:
        print(f"❌ pgrep failed for pattern {pattern}: {e}")
        return []

def term_then_kill(pids, grace=2.0):
    """SIGTERM then SIGKILL after a grace period if still alive."""
    dead = set()
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            dead.add(pid)
    if pids:
        time.sleep(grace)

    # Check who’s still alive
    still = []
    for pid in pids:
        if pid in dead:
            continue
        try:
            os.kill(pid, 0)
            still.append(pid)
        except ProcessLookupError:
            pass

    # SIGKILL stragglers
    for pid in still:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    if pids:
        killed = [str(p) for p in pids]
        print(f"🛑 Terminated PIDs: {' '.join(killed)} (SIGTERM→SIGKILL as needed)")
    return len(pids)

def clear_port(port: int):
    """Kill any process listening on a TCP port."""
    # Prefer lsof, fallback to fuser
    if shutil.which("lsof"):
        res = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        pids = [int(x) for x in res.stdout.strip().splitlines() if x.strip().isdigit()]
    elif shutil.which("fuser"):
        res = subprocess.run(
            ["fuser", "-n", "tcp", str(port)],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
        )
        pids = [int(x) for x in res.stdout.strip().split()] if res.stdout else []
    else:
        print("⚠️ Neither 'lsof' nor 'fuser' present; skipping port cleanup.")
        return 0

    if not pids:
        return 0
    term_then_kill(pids)
    return len(pids)

def sweep_port_range(start: int, end: int):
    total = 0
    for port in range(start, end + 1):
        total += clear_port(port)
    return total

def main():
    print("🛑 Stopping CCRI CTF Hub...\n")
    _ = find_project_root()

    # 1) Kill by process patterns (student/admin)
    total_matched = 0
    for pat in PATTERNS:
        pids = pids_from_pattern(pat)
        if pids:
            print(f"🔍 Pattern match `{pat}` → PIDs: {' '.join(map(str, pids))}")
            total_matched += term_then_kill(pids)
        else:
            print(f"ℹ️ No processes matched `{pat}`")

    # 2) Ensure web port 5000 is free
    print("\n🔧 Ensuring port 5000 is clear...")
    cleared = clear_port(WEB_PORT)
    if cleared:
        print(f"✅ Cleared {cleared} process(es) on port {WEB_PORT}")
    else:
        print("ℹ️ Port 5000 already clear.")

    # 3) (Usually redundant) Sweep simulated service ranges
    # These are in-process threads under server.py; killing main proc should suffice,
    # but we’ll be thorough in case anything was orphaned.
    print("\n🔧 Sweeping guided ports 8000–8100...")
    g = sweep_port_range(*GUIDED_PORT_RANGE)
    print("✅ Cleared guided range." if g else "ℹ️ Guided range already clear.")

    print("\n🔧 Sweeping solo ports 9000–9100...")
    s = sweep_port_range(*SOLO_PORT_RANGE)
    print("✅ Cleared solo range." if s else "ℹ️ Solo range already clear.")

    print("\n🎯 Cleanup complete.")

if __name__ == "__main__":
    main()
