#!/usr/bin/env python3
import os
import sys
import subprocess
import json

CHALLENGE_ID = "18_Pcap_Search"
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
PCAP_FILE = "traffic.pcap"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find .ccri_ctf_root", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in os.path.abspath(__file__) else "guided"

def fast_search_flag(pcap, flag):
    cmd = f"tshark -r {pcap} -Y 'tcp' -T fields -e tcp.payload | xxd -r -p | strings"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return flag in result.stdout

def main():
    root = find_project_root()
    mode = get_ctf_mode()
    unlock_file = os.path.join(root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)

    if not os.path.exists(PCAP_FILE):
        print(f"❌ {PCAP_FILE} missing")
        sys.exit(1)

    try:
        with open(unlock_file, "r", encoding="utf-8") as f:
            unlocks = json.load(f)
        flag = unlocks[CHALLENGE_ID]["real_flag"]
    except Exception as e:
        print(f"❌ Failed to load unlocks: {e}", file=sys.stderr)
        sys.exit(1)

    found = fast_search_flag(PCAP_FILE, flag)
    if found:
        print(f"✅ Flag '{flag}' found in PCAP")
        sys.exit(0)
    else:
        print(f"❌ Flag '{flag}' NOT found", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
