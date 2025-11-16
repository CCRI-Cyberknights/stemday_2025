#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re

# === Configuration ===
PCAP_FILE = "traffic.pcap"
NOTES_FILE = "pcap_notes.txt"
FLAG_REGEX = re.compile(
    r"(CCRI-[A-Z]{4}-\d{4}|[A-Z]{4}-[A-Z]{4}-\d{4}|[A-Z]{4}-\d{4}-[A-Z]{4})"
)

# === Helpers ===
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    Prevents students from just mashing ENTER through explanations.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def check_tshark():
    try:
        subprocess.run(
            ["tshark", "-v"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("❌ ERROR: tshark is not installed.")
        pause()
        sys.exit(1)

# === Flag Extraction Phase ===
def extract_flag_candidates(pcap):
    print("🔍 Scanning entire PCAP for flag-like patterns...\n")
    print("Running command:")
    print(
        "  tshark -r traffic.pcap -Y tcp -T fields -e tcp.payload | xxd -r -p | strings\n"
    )
    # tshark:
    #   -r traffic.pcap          → Read packets from the PCAP file
    #   -Y tcp                   → Only TCP packets
    #   -T fields -e tcp.payload → Print just the TCP payload (in hex)
    #
    # xxd -r -p                  → Convert hex payload back into raw bytes
    # strings                    → Show printable text inside those bytes
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
    print("\n🔗 Mapping detected flags to their TCP stream IDs...\n")
    print("Running command:")
    print("  tshark -r traffic.pcap -Y tcp -T fields -e tcp.stream -e tcp.payload\n")

    stream_map = {}

    result = subprocess.run(
        ["tshark", "-r", pcap, "-Y", "tcp", "-T", "fields", "-e", "tcp.stream", "-e", "tcp.payload"],
        stdout=subprocess.PIPE,
        text=True
    )

    # Collect payloads grouped by stream ID
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

    # Rebuild raw payload per stream and check which flags appear where
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
    print("--------------------------------------")
    print("Using tshark to reconstruct the full TCP conversation:")
    print(f"  tshark -r {pcap} -qz follow,tcp,ascii,{sid}\n")
    subprocess.run(["tshark", "-r", pcap, "-qz", f"follow,tcp,ascii,{sid}"])

def save_summary(pcap, sid):
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"🔗 Stream ID: {sid}\n")
        subprocess.run(
            ["tshark", "-r", pcap, "-qz", f"follow,tcp,ascii,{sid}"],
            stdout=f
        )
        f.write("--------------------------------------\n")
    print(f"✅ Saved to {NOTES_FILE}")
    time.sleep(1)

# === Main Driver ===
def main():
    clear_screen()
    print("📡 PCAP Investigation Tool")
    print("==============================\n")
    print(f"Analyzing: {PCAP_FILE}\n")
    print("🎯 Goal: Discover the real flag (CCRI-AAAA-1111).")
    print("🧪 Some TCP streams contain fake flags; only one is correct.\n")
    print("What’s happening behind the scenes?")
    print("  ➤ We read packet data from the PCAP with tshark.")
    print("  ➤ We pull out TCP payloads and convert the hex into raw bytes.")
    print("  ➤ We scan for anything that looks like a flag (real or fake).")
    print("  ➤ Then we map each candidate flag back to its TCP stream so you")
    print("    can inspect the full conversation in context.\n")
    print("In a normal workflow, you might run commands like:")
    print("  tshark -r traffic.pcap")
    print("  tshark -r traffic.pcap -qz follow,tcp,ascii,0")
    print("  tshark -r traffic.pcap -Y tcp -T fields -e tcp.payload | xxd -r -p | strings\n")

    if not os.path.isfile(PCAP_FILE):
        print(f"❌ Missing file: {PCAP_FILE}")
        pause()
        sys.exit(1)

    check_tshark()

    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)

    pause_nonempty("Type 'scan' when you're ready to begin scanning the PCAP: ")

    # Phase 1: Find flag-like values
    flags_found = extract_flag_candidates(PCAP_FILE)
    if not flags_found:
        print("\n❌ No flag-like patterns found.")
        pause()
        sys.exit(0)

    print("\n✅ Candidate flag-like values detected:")
    for f in sorted(flags_found):
        print(f"   ➡️ {f}")
    print()
    pause_nonempty("Type anything, then press ENTER to map these flags back to their TCP streams: ")

    # Phase 2: Map flags to streams
    stream_map = map_flags_to_streams(PCAP_FILE, flags_found)
    if not stream_map:
        print("❌ No streams matched the candidate flags.")
        pause()
        sys.exit(0)

    candidates = sorted(stream_map.keys())
    print(f"\n✅ {len(candidates)} stream(s) contain flag-like data.")
    pause_nonempty("Type anything, then press ENTER to review the candidate streams: ")

    # Phase 3: Exploration UI
    while True:
        clear_screen()
        print("📜 Candidate Streams:")
        print("---------------------------")
        for idx, sid in enumerate(candidates, 1):
            flags_for_stream = ", ".join(sorted(stream_map[sid]))
            print(f"{idx}. Stream ID: {sid} (flags: {flags_for_stream})")
        print(f"{len(candidates)+1}. Exit\n")

        try:
            choice = int(input(f"Choose stream to view (1-{len(candidates)+1}): ").strip())
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
                    print(f"\n✅ Done. Notes saved in {NOTES_FILE}")
                    pause()
                    sys.exit(0)
                else:
                    print("❌ Invalid option. Please choose 1–3.")
        elif choice == len(candidates)+1:
            break

    print(f"\n✅ Done. Notes saved in {NOTES_FILE}")
    pause()

if __name__ == "__main__":
    main()
