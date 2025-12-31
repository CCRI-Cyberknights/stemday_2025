#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
PCAP_FILE = "traffic.pcap"
NOTES_FILENAME = "pcap_notes.txt"
# Matches variants: CCRI-AAAA-1111, AAAA-AAAA-1111, AAAA-1111-AAAA
FLAG_REGEX = re.compile(
    r"(CCRI-[A-Z]{4}-\d{4}|[A-Z]{4}-[A-Z]{4}-\d{4}|[A-Z]{4}-\d{4}-[A-Z]{4})"
)

# === Helpers ===
def check_tshark():
    try:
        subprocess.run(
            ["tshark", "-v"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print_error("tshark is not installed.")
        print_info("On Debian/Parrot: sudo apt install tshark")
        pause()
        sys.exit(1)

# === Flag Extraction Phase ===
def extract_flag_candidates(pcap_path):
    print(f"{Colors.CYAN}🔍 Scanning entire PCAP for flag-like patterns...{Colors.END}\n")
    print(f"Running command:")
    print(f"  {Colors.GREEN}tshark -r traffic.pcap -Y tcp -T fields -e tcp.payload | xxd -r -p | strings{Colors.END}\n")
    
    # We pipe shell commands, so we use shell=True safely here with a controlled path
    cmd = f"tshark -r '{str(pcap_path)}' -Y tcp -T fields -e tcp.payload | xxd -r -p | strings"
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    except Exception as e:
        print_error(f"Error running extraction: {e}")
        return []

    found = set()
    for line in result.stdout.splitlines():
        match = FLAG_REGEX.search(line)
        if match:
            found.add(match.group(0).strip())

    return list(found)

# === Flag-to-Stream Mapping ===
def map_flags_to_streams(pcap_path, flags):
    print(f"\n{Colors.CYAN}🔗 Mapping detected flags to their TCP stream IDs...{Colors.END}\n")
    print(f"Running command:")
    print(f"  {Colors.GREEN}tshark -r traffic.pcap -Y tcp -T fields -e tcp.stream -e tcp.payload{Colors.END}\n")

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
    spinner("Mapping streams")
    for stream_id, chunks in stream_data.items():
        full_data = '\n'.join(chunks)
        try:
            # We use xxd to reverse the hex so we can search for the plain text flag
            # We pass input via stdin to avoid shell=True complexity
            proc = subprocess.Popen(
                ["xxd", "-r", "-p"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            stdout, _ = proc.communicate(input=full_data)
            payload = stdout
        except Exception:
            continue

        for flag in flags:
            if flag in payload:
                stream_map.setdefault(stream_id, set()).add(flag)

    return stream_map

# === Display & Interaction ===
def show_stream_summary(pcap_path, sid):
    header(f"🔗 Stream ID: {sid}")
    print("Using tshark to reconstruct the full TCP conversation:")
    print(f"  {Colors.GREEN}tshark -r traffic.pcap -qz follow,tcp,ascii,{sid}{Colors.END}\n")
    print("-" * 50)
    
    # This is the "Big Reveal" - we show the real output here
    subprocess.run(["tshark", "-r", str(pcap_path), "-qz", f"follow,tcp,ascii,{sid}"])
    print("-" * 50)

def save_summary(pcap_path, sid, notes_path):
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write(f"🔗 Stream ID: {sid}\n")
        subprocess.run(
            ["tshark", "-r", str(pcap_path), "-qz", f"follow,tcp,ascii,{sid}"],
            stdout=f,
            stderr=subprocess.DEVNULL
        )
        f.write("--------------------------------------\n")
    print_success(f"Saved to {notes_path.name}")
    time.sleep(1)

# === Main Driver ===
def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = Path(__file__).resolve().parent
    pcap_path = script_dir / PCAP_FILE
    notes_path = script_dir / NOTES_FILENAME

    # 2. Mission Briefing
    header("📡 PCAP Investigation Tool")
    
    print(f"Analyzing: {Colors.BOLD}{pcap_path.name}{Colors.END}")
    print(f"🎯 Goal: Discover the real flag ({Colors.GREEN}CCRI-AAAA-1111{Colors.END}).")
    print(f"{Colors.RED}🧪 Some TCP streams contain fake flags; only one is correct.{Colors.END}\n")
    
    print(f"{Colors.CYAN}What’s happening behind the scenes?{Colors.END}")
    print("  ➤ We read packet data from the PCAP with tshark.")
    print("  ➤ We scan for flag patterns, but we will REDACT them initially.")
    print("  ➤ You must inspect the TCP stream to see the full content and context.\n")
    
    if not pcap_path.is_file():
        print_error(f"Missing file '{pcap_path.name}'")
        pause("Press ENTER to exit...")
        sys.exit(1)

    check_tshark()

    if notes_path.exists():
        os.remove(notes_path)

    require_input("Type 'scan' when you're ready to begin scanning the PCAP: ", "scan")

    # 3. Phase 1: Find flag-like values (REDACTED OUTPUT)
    flags_found = extract_flag_candidates(pcap_path)
    if not flags_found:
        print_error("No flag-like patterns found.")
        pause("Press ENTER to exit...")
        sys.exit(0)

    print(f"\n{Colors.GREEN}✅ Scan complete. Detected {len(flags_found)} potential flag patterns.{Colors.END}")
    print("   (Content hidden to prevent spoilers - map to streams to view)\n")
    
    for f in sorted(flags_found):
        # Redaction Logic: Show first 5 chars, hide the rest
        redacted = f[:5] + "****-****"
        print(f"   ➡️  {Colors.YELLOW}{redacted}{Colors.END}")
        
    print()
    require_input("Type 'map' to map these patterns to TCP streams: ", "map")

    # 4. Phase 2: Map flags to streams
    stream_map = map_flags_to_streams(pcap_path, flags_found)
    if not stream_map:
        print_error("No streams matched the candidate flags.")
        pause()
        sys.exit(0)

    candidates = sorted(stream_map.keys())
    print_success(f"{len(candidates)} TCP stream(s) contain suspect data.")
    
    require_input("Type 'investigate' to explore the streams: ", "investigate")

    # 5. Phase 3: Exploration UI (REDACTED MENU)
    while True:
        clear_screen()
        print(f"{Colors.CYAN}📜 Candidate Streams:{Colors.END}")
        print("-" * 40)
        for idx, sid in enumerate(candidates, 1):
            # Don't show the flags here either!
            count = len(stream_map[sid])
            print(f"{Colors.BOLD}{idx}{Colors.END}. Stream ID: {Colors.YELLOW}{sid}{Colors.END} (Contains {count} hidden candidate(s))")
        print(f"{len(candidates)+1}. Exit\n")

        try:
            choice_str = input(f"{Colors.YELLOW}Choose stream to inspect (1-{len(candidates)+1}): {Colors.END}").strip()
            if not choice_str.isdigit():
                print_error("Invalid input. Please enter a number.")
                pause()
                continue
            choice = int(choice_str)
        except ValueError:
            print_error("Invalid input.")
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
                print(f"2) 💾 Save stream summary (to {NOTES_FILENAME})")
                print("3) 🚪 Exit")
                opt = input(f"{Colors.YELLOW}Choose (1-3): {Colors.END}").strip()
                if opt == "1":
                    break
                elif opt == "2":
                    save_summary(pcap_path, sid, notes_path)
                elif opt == "3":
                    print(f"\n{Colors.CYAN}👋 Done. Notes saved in {notes_path.name}{Colors.END}")
                    pause()
                    sys.exit(0)
                else:
                    print_error("Invalid option. Please choose 1–3.")
        elif choice == len(candidates)+1:
            break
        else:
            print_error("Invalid selection.")
            pause()

    print_success(f"Done. Notes saved in {notes_path.name}")
    pause()

if __name__ == "__main__":
    main()