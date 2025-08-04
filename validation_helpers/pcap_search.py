#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "18_Pcap_Search"
PCAP_FILE = "traffic.pcap"

def fast_search_flag(pcap: Path, flag: str) -> bool:
    cmd = f"tshark -r {pcap} -Y 'tcp' -T fields -e tcp.payload | xxd -r -p | strings"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return flag in result.stdout

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)

    flag = data["real_flag"]
    pcap_path = root / "challenges" / CHALLENGE_ID / PCAP_FILE

    if not pcap_path.exists():
        print(f"❌ {PCAP_FILE} missing at {pcap_path}", file=sys.stderr)
        sys.exit(1)

    if fast_search_flag(pcap_path, flag):
        print(f"✅ Flag '{flag}' found in PCAP")
        sys.exit(0)
    else:
        print(f"❌ Flag '{flag}' NOT found in PCAP", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
