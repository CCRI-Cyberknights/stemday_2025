#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "18_PcapSearch"
PCAP_FILE = "traffic.pcap"

def fast_search_flag(pcap: Path, flag: str) -> bool:
    cmd = f"tshark -r {pcap} -Y 'tcp' -T fields -e tcp.payload | xxd -r -p | strings"
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    return flag in result.stdout

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    pcap_path = root / base_path / challenge_id / PCAP_FILE

    if not pcap_path.exists():
        print(f"❌ {PCAP_FILE} missing at {pcap_path}", file=sys.stderr)
        return False

    if fast_search_flag(pcap_path, flag):
        print(f"✅ Flag '{flag}' found in PCAP")
        return True
    else:
        print(f"❌ Flag '{flag}' NOT found in PCAP", file=sys.stderr)
        return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
