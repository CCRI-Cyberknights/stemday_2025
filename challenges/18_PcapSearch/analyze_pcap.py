#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

# === Configuration ===
PCAP_FILE = "traffic.pcap"
NOTES_FILE = "pcap_notes.txt"
FLAG_REGEX = re.compile(r"(CCRI-[A-Z]{4}-\d{4}|[A-Z]{4}-[A-Z]{4}-\d{4}|[A-Z]{4}-\d{4}-[A-Z]{4})")

# === Helpers ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def check_tshark():
    try:
        subprocess.run(["tshark", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ ERROR: tshark is not installed.")
        pause()
        sys.exit(1)

# === Flag Extraction Phase ===
def extract_flag_candidates(pcap):
    print("🔍 Scanning entire PCAP for flag-like patterns...\n")
    cmd = f"tshark -r {pcap} -Y tcp -T fields -e tcp.payload | xxd -r -p | strings"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)

    found = set()
    for line in result.stdout.splitlines():
        match = FLAG_REGEX.search(line)
        if match:
            found.add(match.group(0).strip())

    return list(found)

# === Flag-to-Stream Mapping ===
def map_flags_to_streams(pcap, flags):
    print("🔗 Mapping detected flags to their TCP stream IDs...\n")
    stream_map = {}

    result = subprocess.run(
        ["tshark", "-r", pcap, "-Y", "tcp", "-T", "fields", "-e", "tcp.stream", "-e", "tcp.payload"],
        stdout=subprocess.PIPE, text=True
    )

    stream_data = {}
    for line in result.stdout.strip().splitlines():
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        stream_id, hex_payload = parts
        if not stream_id or not hex_payload:
            continue
        try:
            stream_id = int(stream_id)
        except ValueError:
            continue
        stream_data.setdefault(stream_id, []).append(hex_payload)

    for stream_id, chunks in stream_data.items():
        full_data = '\n'.join(chunks)
        try:
            payload = subprocess.run(
                ["xxd", "-r", "-p"],
                input=full_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            ).stdout
        except Exception:
            continue

        for flag in flags:
            if flag in payload:
                stream_map.setdefault(stream_id, set()).add(flag)

    return stream_map

# === Display & Interaction ===
def show_stream_summary(pcap, sid):
    print(f"\n🔗 Stream ID: {sid}")
    subprocess.run(["tshark", "-r", pcap, "-qz", f"follow,tcp,ascii,{sid}"])

def save_summary(pcap, sid):
    with open(NOTES_FILE, "a") as f:
        f.write(f"🔗 Stream ID: {sid}\n")
        subprocess.run(["tshark", "-r", pcap, "-qz", f"follow,tcp,ascii,{sid}"], stdout=f)
        f.write("--------------------------------------\n")
    print(f"✅ Saved to {NOTES_FILE}")
    time.sleep(1)

# === Main Driver ===
def main():
    clear_screen()
    print("📡 PCAP Investigation Tool")
    print("==============================\n")
    print(f"Analyzing: {PCAP_FILE}\n")
    print("🎯 Goal: Discover the real flag (CCRI-XXXX-1234).")
    print("🧪 Some streams contain fakes. Only one is correct!\n")
    pause()

    if not os.path.isfile(PCAP_FILE):
        print(f"❌ Missing file: {PCAP_FILE}")
        pause()
        sys.exit(1)

    check_tshark()

    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)

    # Phase 1: Find flag-like values
    flags_found = extract_flag_candidates(PCAP_FILE)
    if not flags_found:
        print("❌ No flag-like patterns found.")
        pause()
        sys.exit(0)

    # Phase 2: Map flags to streams
    stream_map = map_flags_to_streams(PCAP_FILE, flags_found)
    if not stream_map:
        print("❌ No streams matched the candidate flags.")
        pause()
        sys.exit(0)

    candidates = sorted(stream_map.keys())
    print(f"✅ {len(candidates)} stream(s) contain flag-like data.")
    pause()

    # Phase 3: Exploration UI
    while True:
        clear_screen()
        print("📜 Candidate Streams:")
        print("---------------------------")
        for idx, sid in enumerate(candidates, 1):
            print(f"{idx}. Stream ID: {sid} (flag-like content detected)")
        print(f"{len(candidates)+1}. Exit\n")

        try:
            choice = int(input(f"Choose stream to view (1-{len(candidates)+1}): "))
        except ValueError:
            continue

        if 1 <= choice <= len(candidates):
            sid = candidates[choice - 1]
            clear_screen()
            show_stream_summary(PCAP_FILE, sid)

            while True:
                print("\nOptions:")
                print("1) 🔁 Back to list")
                print("2) 💾 Save summary")
                print("3) 🚪 Exit")
                opt = input("Choose (1-3): ").strip()
                if opt == "1":
                    break
                elif opt == "2":
                    save_summary(PCAP_FILE, sid)
                elif opt == "3":
                    sys.exit(0)
        elif choice == len(candidates)+1:
            break

    print(f"\n✅ Done. Notes saved in {NOTES_FILE}")
    pause()

if __name__ == "__main__":
    main()
