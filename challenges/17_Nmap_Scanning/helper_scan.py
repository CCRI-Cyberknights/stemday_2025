#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import time

# === Nmap Scan Puzzle Helper ===

def find_project_root():
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.exists(os.path.join(dir_path, ".ccri_ctf_root")):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    if not validation_mode:
        os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    if not validation_mode:
        input(prompt)

def run_nmap_scan():
    if not validation_mode:
        print("\n📡 Running: nmap -sV --version-light -p8000-8100 localhost\n")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "--version-light", "-p8000-8100", "localhost"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout
    except FileNotFoundError:
        print("❌ ERROR: nmap is not installed.")
        sys.exit(1)

def extract_open_ports(scan_output):
    ports = []
    for line in scan_output.splitlines():
        if "open" in line:
            try:
                port = line.split("/")[0].strip()
                ports.append(port)
            except Exception:
                continue
    return ports

def fetch_port_response(port):
    try:
        result = subprocess.run(
            ["curl", "-s", f"http://localhost:{port}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: curl is not installed.")
        sys.exit(1)

def validate_flag_in_services(expected_flag, expected_port):
    print(f"🔎 Validating port {expected_port} for expected flag: {expected_flag}")
    response = fetch_port_response(expected_port)
    if expected_flag in response:
        print(f"✅ Validation success: found flag at port {expected_port}")
        return True
    else:
        print(f"❌ Validation failed: expected flag not found at port {expected_port}")
        print(f"   Got response: {response}")
        return False

def main():
    project_root = find_project_root()
    script_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(script_dir)

    if validation_mode:
        # Load expected flag and port from validation unlocks
        unlock_file = os.path.join(project_root, "web_version_admin", "validation_unlocks.json")
        try:
            with open(unlock_file, "r", encoding="utf-8") as f:
                unlocks = json.load(f)
            challenge_meta = unlocks["17_Nmap_Scanning"]
            expected_flag = challenge_meta["real_flag"]
            expected_port = int(challenge_meta["real_port"])
        except Exception as e:
            print(f"❌ ERROR: Could not load validation unlocks: {e}", file=sys.stderr)
            sys.exit(1)

        if validate_flag_in_services(expected_flag, expected_port):
            sys.exit(0)
        else:
            sys.exit(1)

    # === Student Interactive Mode ===
    clear_screen()
    print("🛰️ Nmap Scan Puzzle")
    print("--------------------------------------\n")
    print("Several simulated services are running locally (inside your CTF app).\n")
    print("🎯 Your goal: Scan localhost (127.0.0.1) for open ports in the range 8000–8100, and find the REAL flag.")
    print("⚠️ Some ports contain random junk responses. Only one flag is correct.\n")
    print("🔧 Under the hood:")
    print("   We'll use 'nmap' to scan the ports and see what services respond.")
    print("   Then we'll query each open port for its reported response.\n")
    pause()

    scan_output = run_nmap_scan()
    clear_screen()
    print("📝 Nmap Scan Results:")
    print("--------------------------------------")
    print(scan_output)
    print("\n✅ Scan complete.\n")

    pause("📖 Review the scan results above. Press ENTER to explore the open ports interactively...")

    open_ports = extract_open_ports(scan_output)

    if not open_ports:
        print("❌ No open ports found in the range 8000–8100.")
        pause("Press ENTER to exit...")
        sys.exit(1)

    # Interactive exploration
    while True:
        clear_screen()
        print("--------------------------------------")
        print("Open ports detected:")
        for idx, port in enumerate(open_ports, 1):
            print(f"{idx:2d}. {port}")
        print(f"{len(open_ports)+1:2d}. Exit\n")

        try:
            choice = int(input(f"Select a port to explore (1-{len(open_ports)+1}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        if 1 <= choice <= len(open_ports):
            port = open_ports[choice - 1]
            print(f"\n🌐 Connecting to http://localhost:{port} ...")
            print("--------------------------------------")
            response = fetch_port_response(port)

            if not response:
                print(f"⚠️ No response received from port {port}.")
            else:
                print(response)

            print("--------------------------------------\n")

            while True:
                print("Options:")
                print("1. 🔁 Return to port list")
                print("2. 💾 Save this response to nmap_flag_response.txt\n")

                sub_choice = input("Choose an option (1-2): ").strip()
                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    out_file = os.path.join(script_dir, "nmap_flag_response.txt")
                    with open(out_file, "a") as f:
                        f.write(f"Port: {port}\nResponse:\n{response}\n")
                        f.write("--------------------------------------\n")
                    print(f"✅ Response saved to {out_file}")
                    time.sleep(1)
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
                    time.sleep(1)

        elif choice == len(open_ports)+1:
            print("\n👋 Exiting helper. Return to the CTF portal to submit your flag.")
            break
        else:
            print("❌ Invalid choice. Please select a valid port.")
            time.sleep(1)

if __name__ == "__main__":
    validation_mode = os.getenv("CCRI_VALIDATE") == "1"
    main()
