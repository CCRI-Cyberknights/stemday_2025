#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

# === Configuration ===
NOTES_FILENAME = "pcap_notes.txt"
# Matches variants: CCRI-AAAA-1111, AAAA-AAAA-1111, AAAA-1111-AAAA
FLAG_REGEX = re.compile(
    r"(CCRI-[A-Z]{4}-\d{4}|[A-Z]{4}-[A-Z]{4}-\d{4}|[A-Z]{4}-\d{4}-[A-Z]{4})"
)

# === Helpers ===
def resize_terminal(rows=35, cols=90):
    """Force terminal resize for better visibility."""
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def require_input(prompt, expected):
    """
    Pauses and requires the user to type a specific word (case-insensitive) to continue.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

def check_tshark():
    try:
        subprocess.run(
            ["tshark", "-v"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("❌ ERROR: tshark is not installed.")
        print("   On Debian/Parrot: sudo apt install tshark")
        pause()
        sys.exit(1)

# === Flag Extraction Phase ===
def extract_flag_candidates(pcap_path):
    print("🔍 Scanning entire PCAP for flag-like patterns...\n")
    print("Running command:")
    print("  tshark -r traffic.pcap -Y tcp -T fields -e tcp.payload | xxd -r -p | strings\n")
    
    cmd = f"tshark -r '{str(pcap_path)}' -Y tcp -T fields -e tcp.payload | xxd -r -p | strings"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)

    found = set()
    for line in result.stdout.splitlines():
        match = FLAG_REGEX.search(line)
        if match:
            found.add(match.group(0).strip())

    return list(found)

# === Flag-to-Stream Mapping ===
def map_flags_to_streams(pcap_path, flags):
    print("\n🔗 Mapping detected flags to their TCP stream IDs...\n")
    print("Running command:")
    print("  tshark -r traffic.pcap -Y tcp -T fields -e tcp.stream -e tcp.payload\n")

    stream_map = {}
    
    # We need to find which stream contains which flag
    result = subprocess.run(
        ["tshark", "-r", str(pcap_path), "-Y", "tcp", "-T", "fields", "-e", "tcp.stream", "-e", "tcp.payload"],
        stdout=subprocess.PIPE,
        text=True
    )

    stream_data = {}
    for line in result.stdout.strip().splitlines():
        parts = line.split('\t')
        if len(parts) != 2: continue
        stream_id, hex_payload = parts
        try:
            stream_id = int(stream_id)
            stream_data.setdefault(stream_id, []).append(hex_payload)
        except ValueError:
            continue

    # Check payloads
    for stream_id, chunks in stream_data.items():
        full_data = '\n'.join(chunks)
        # Convert hex back to bytes for checking
        try:
            # We use xxd to reverse the hex so we can search for the plain text flag
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
def show_stream_summary(pcap_path, sid):
    print(f"\n🔗 Stream ID: {sid}")
    print("--------------------------------------")
    print("Using tshark to reconstruct the full TCP conversation:")
    print(f"  tshark -r traffic.pcap -qz follow,tcp,ascii,{sid}\n")
    
    # This is the "Big Reveal" - we show the real output here
    subprocess.run(["tshark", "-r", str(pcap_path), "-qz", f"follow,tcp,ascii,{sid}"])

def save_summary(pcap_path, sid, notes_path):
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write(f"🔗 Stream ID: {sid}\n")
        subprocess.run(
            ["tshark", "-r", str(pcap_path), "-qz", f"follow,tcp,ascii,{sid}"],
            stdout=f
        )
        f.write("--------------------------------------\n")
    print(f"✅ Saved to {notes_path.name}")
    time.sleep(1)

# === Main Driver ===
def main():
    resize_terminal(35, 90)
    clear_screen()

    script_dir = Path(__file__).resolve().parent
    pcap_path = script_dir / "traffic.pcap"
    notes_path = script_dir / NOTES_FILENAME

    print("📡 PCAP Investigation Tool")
    print("==============================\n")
    print(f"Analyzing: {pcap_path.name}")
    print("🎯 Goal: Discover the real flag (CCRI-AAAA-1111).")
    print("🧪 Some TCP streams contain fake flags; only one is correct.\n")
    print("What’s happening behind the scenes?")
    print("  ➤ We read packet data from the PCAP with tshark.")
    print("  ➤ We scan for flag patterns, but we will REDACT them initially.")
    print("  ➤ You must inspect the TCP stream to see the full content and context.\n")
    
    if not pcap_path.is_file():
        print(f"\n❌ CRITICAL ERROR: Missing file '{pcap_path.name}'")
        pause("Press ENTER to exit...")
        sys.exit(1)

    check_tshark()

    if notes_path.exists():
        os.remove(notes_path)

    require_input("Type 'scan' when you're ready to begin scanning the PCAP: ", "scan")

    # Phase 1: Find flag-like values (REDACTED OUTPUT)
    flags_found = extract_flag_candidates(pcap_path)
    if not flags_found:
        print("\n❌ No flag-like patterns found.")
        pause("Press ENTER to exit...")
        sys.exit(0)

    print(f"\n✅ Scan complete. Detected {len(flags_found)} potential flag patterns.")
    print("   (Content hidden to prevent spoilers - map to streams to view)\n")
    
    for f in sorted(flags_found):
        # Redaction Logic: Show first 5 chars, hide the rest
        # e.g., CCRI-****-****
        redacted = f[:5] + "****-****"
        print(f"   ➡️  {redacted}")
        
    print()
    require_input("Type 'map' to map these patterns to TCP streams: ", "map")

    # Phase 2: Map flags to streams
    stream_map = map_flags_to_streams(pcap_path, flags_found)
    if not stream_map:
        print("❌ No streams matched the candidate flags.")
        pause()
        sys.exit(0)

    candidates = sorted(stream_map.keys())
    print(f"\n✅ {len(candidates)} TCP stream(s) contain suspect data.")
    
    require_input("Type 'investigate' to explore the streams: ", "investigate")

    # Phase 3: Exploration UI (REDACTED MENU)
    while True:
        clear_screen()
        print("📜 Candidate Streams:")
        print("---------------------------")
        for idx, sid in enumerate(candidates, 1):
            # Don't show the flags here either!
            count = len(stream_map[sid])
            print(f"{idx}. Stream ID: {sid} (Contains {count} hidden candidate(s))")
        print(f"{len(candidates)+1}. Exit\n")

        try:
            choice_str = input(f"Choose stream to inspect (1-{len(candidates)+1}): ").strip()
            if not choice_str.isdigit():
                print("❌ Invalid input. Please enter a number.")
                pause()
                continue
            choice = int(choice_str)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            pause()
            continue

        if 1 <= choice <= len(candidates):
            sid = candidates[choice - 1]
            clear_screen()
            
            # THE REVEAL happens inside this function
            show_stream_summary(pcap_path, sid)

            while True:
                print("\nOptions:")
                print("1) 🔁 Back to list")
                print("2) 💾 Save stream summary (with flags)")
                print("3) 🚪 Exit")
                opt = input("Choose (1-3): ").strip()
                if opt == "1":
                    break
                elif opt == "2":
                    save_summary(pcap_path, sid, notes_path)
                elif opt == "3":
                    print(f"\n✅ Done. Notes saved in {notes_path.name}")
                    pause()
                    sys.exit(0)
                else:
                    print("❌ Invalid option. Please choose 1–3.")
        elif choice == len(candidates)+1:
            break
        else:
            print("❌ Invalid selection.")
            pause()

    print(f"\n✅ Done. Notes saved in {notes_path.name}")
    pause()

if __name__ == "__main__":
    main()