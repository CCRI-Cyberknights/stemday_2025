#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time
from pathlib import Path

# === PCAP Investigation Tool Helper ===

CHALLENGE_ID = "18_Pcap_Search"
GUIDED_JSON = "validation_unlocks.json"
SOLO_JSON = "validation_unlocks_solo.json"
validation_mode = os.getenv("CCRI_VALIDATE") == "1"

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode():
    mode = os.environ.get("CCRI_MODE")
    if mode in ("guided", "solo"):
        return mode
    return "solo" if "challenges_solo" in str(Path(__file__).resolve()) else "guided"

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def check_tshark():
    try:
        subprocess.run(["tshark", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ ERROR: tshark is not installed or not in PATH.")
        if not validation_mode:
            pause()
        sys.exit(1)

def fast_validate_flag(pcap_file, expected_flag):
    try:
        cmd = f"tshark -r {pcap_file} -Y 'tcp' -T fields -e tcp.payload | xxd -r -p | strings"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if expected_flag in result.stdout:
            print(f"✅ Validation success: found flag {expected_flag}")
            return True
        else:
            print(f"❌ Validation failed: flag {expected_flag} not found", file=sys.stderr)
            return False
    except Exception as e:
        print(f"❌ ERROR during fast validation: {e}", file=sys.stderr)
        return False

def extract_tcp_streams(pcap_file):
    result = subprocess.run(
        ["tshark", "-r", pcap_file, "-Y", "tcp", "-T", "fields", "-e", "tcp.stream"],
        stdout=subprocess.PIPE,
        text=True
    )
    return sorted(set(result.stdout.strip().splitlines()))

def scan_for_flags(pcap_file, streams):
    flag_streams = []
    pattern = r"[A-Z]{4}-[A-Z]{4}-[0-9]{4}|[A-Z]{4}-[0-9]{4}-[A-Z]{4}"
    for sid in streams:
        cmd = f"tshark -r {pcap_file} -Y 'tcp.stream=={sid}' -T fields -e tcp.payload | xxd -r -p | strings"
        grep = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if any(line for line in grep.stdout.splitlines() if pattern in line):
            print(f"\n🔎 Found potential flag in Stream ID: {sid}")
            flag_streams.append(sid)
    print("\n✅ Scan complete.")
    return flag_streams

def show_stream_details(pcap_file, sid):
    print(f"🔗 Stream ID: {sid}")
    print("-----------------------------------------")
    result = subprocess.run(
        ["tshark", "-r", pcap_file, "-Y", f"tcp.stream=={sid}", "-T", "fields",
         "-e", "ip.src", "-e", "tcp.srcport", "-e", "ip.dst", "-e", "tcp.dstport"],
        stdout=subprocess.PIPE, text=True
    )
    fields = result.stdout.strip().splitlines()[0].split()
    if len(fields) >= 4:
        print(f"📨 From: {fields[0]}:{fields[1]}\n📬 To: {fields[2]}:{fields[3]}")
    print("\n📝 Payload Preview:")
    subprocess.run(["tshark", "-r", pcap_file, "-qz", f"follow,tcp,ascii,{sid}"])

def save_stream_summary(pcap_file, sid, out_file):
    with open(out_file, "a") as f:
        f.write(f"🔗 Stream ID: {sid}\n")
        result = subprocess.run(
            ["tshark", "-r", pcap_file, "-Y", f"tcp.stream=={sid}", "-T", "fields",
             "-e", "ip.src", "-e", "tcp.srcport", "-e", "ip.dst", "-e", "tcp.dstport"],
            stdout=subprocess.PIPE, text=True
        )
        fields = result.stdout.strip().splitlines()[0].split()
        if len(fields) >= 4:
            f.write(f"📨 From: {fields[0]}:{fields[1]}\n📬 To: {fields[2]}:{fields[3]}\n")
        f.write("Payload:\n")
        subprocess.run(["tshark", "-r", pcap_file, "-qz", f"follow,tcp,ascii,{sid}"], stdout=f)
        f.write("-----------------------------------------\n")
    print(f"✅ Saved to {os.path.basename(out_file)}")
    time.sleep(1)

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(script_dir)

    check_tshark()
    pcap_file = os.path.join(script_dir, "traffic.pcap")
    if not os.path.isfile(pcap_file):
        print(f"❌ ERROR: {os.path.basename(pcap_file)} not found in this folder!")
        if not validation_mode:
            pause()
        sys.exit(1)

    if validation_mode:
        mode = get_ctf_mode()
        unlock_file = os.path.join(project_root, "web_version_admin", SOLO_JSON if mode == "solo" else GUIDED_JSON)
        try:
            with open(unlock_file, "r", encoding="utf-8") as f:
                unlocks = json.load(f)
            expected_flag = unlocks[CHALLENGE_ID]["real_flag"]
        except Exception as e:
            print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0 if fast_validate_flag(pcap_file, expected_flag) else 1)

    # === Student Mode ===
    clear_screen()
    print("📡 PCAP Investigation Tool")
    print("==============================\n")
    print("You've intercepted network traffic in: traffic.pcap\n")
    print("🎯 Goal: Investigate the traffic and identify the REAL flag.")
    print("⚠️ Four streams contain fake flags. Only ONE has the real flag (CCRI-AAAA-1111 format).\n")
    print("🔧 Under the hood:")
    print("   1️⃣ We'll use 'tshark' to extract all TCP streams.")
    print("   2️⃣ Then, we’ll scan them for flag-like patterns.")
    print("   3️⃣ You’ll review candidate streams interactively.\n")
    pause()

    out_file = os.path.join(script_dir, "pcap_notes.txt")
    if os.path.isfile(out_file):
        os.remove(out_file)

    streams = extract_tcp_streams(pcap_file)
    print(f"\n✅ Found {len(streams)} TCP streams in the capture.")
    pause()

    flag_streams = scan_for_flags(pcap_file, streams)
    if not flag_streams:
        print("\n❌ No flag-like patterns found in any stream.")
        pause()
        sys.exit(1)

    print(f"\n✅ Found {len(flag_streams)} stream(s) with flag-like patterns.")
    pause("📖 Press ENTER to review candidate streams interactively...")

    while True:
        clear_screen()
        print("-----------------------------------------")
        print("📜 Flag Candidate Streams:")
        for idx, sid in enumerate(flag_streams, 1):
            print(f"{idx}. Stream ID: {sid}")
        print(f"{len(flag_streams)+1}. Exit\n")

        try:
            choice = int(input(f"Select a stream to view (1-{len(flag_streams)+1}): ").strip())
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        if 1 <= choice <= len(flag_streams):
            sid = flag_streams[choice - 1]
            clear_screen()
            show_stream_details(pcap_file, sid)

            while True:
                print("\nOptions:")
                print("1) 🔁 Return to candidate list")
                print(f"2) 💾 Save this stream’s summary to {os.path.basename(out_file)}")
                print("3) 🚪 Exit tool")
                sub_choice = input("Choose an option (1-3): ").strip()
                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    save_stream_summary(pcap_file, sid, out_file)
                elif sub_choice == "3":
                    print("👋 Exiting tool.")
                    sys.exit(0)
                else:
                    print("⚠️ Invalid choice. Please select 1-3.")
        elif choice == len(flag_streams)+1:
            print("👋 Exiting tool. Review your findings carefully.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid number.")
            time.sleep(1)

    print("\n🎉 Investigation complete!")
    print(f"📄 Your saved notes are in: {os.path.basename(out_file)}")
    print("🚀 Return to the CTF hub to submit the correct flag.")
    pause()

if __name__ == "__main__":
    main()
