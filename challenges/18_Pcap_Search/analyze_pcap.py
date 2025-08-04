#!/usr/bin/env python3
import os
import sys
import subprocess
import time

PCAP_FILE = "traffic.pcap"
NOTES_FILE = "pcap_notes.txt"

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

def extract_tcp_streams(pcap):
    result = subprocess.run(
        ["tshark", "-r", pcap, "-Y", "tcp", "-T", "fields", "-e", "tcp.stream"],
        stdout=subprocess.PIPE, text=True
    )
    return sorted(set(result.stdout.strip().splitlines()))

def scan_for_candidates(pcap, streams):
    pattern = r"[A-Z]{4}-[A-Z]{4}-[0-9]{4}|[A-Z]{4}-[0-9]{4}-[A-Z]{4}"
    candidate_streams = []
    for sid in streams:
        cmd = f"tshark -r {pcap} -Y 'tcp.stream=={sid}' -T fields -e tcp.payload | xxd -r -p | strings"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if any(line for line in result.stdout.splitlines() if pattern in line):
            candidate_streams.append(sid)
    return candidate_streams

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

def main():
    clear_screen()
    print("📡 PCAP Investigation Tool\n==============================\n")
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

    streams = extract_tcp_streams(PCAP_FILE)
    print(f"✅ Found {len(streams)} TCP streams.")
    pause()

    candidates = scan_for_candidates(PCAP_FILE, streams)
    if not candidates:
        print("❌ No flag-like data found in any stream.")
        pause()
        sys.exit(1)

    print(f"✅ {len(candidates)} stream(s) contain flag-like data.")
    pause()

    while True:
        clear_screen()
        print("📜 Candidate Streams:\n---------------------------")
        for idx, sid in enumerate(candidates, 1):
            print(f"{idx}. Stream ID: {sid}")
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
                print("\nOptions:\n1) 🔁 Back to list\n2) 💾 Save summary\n3) 🚪 Exit")
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
