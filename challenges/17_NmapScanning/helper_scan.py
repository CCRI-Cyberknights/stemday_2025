#!/usr/bin/env python3
import os
import sys
import subprocess
import time

BINARY_PORT_RANGE = "8000-8100"
BINARY_HOST = "localhost"
BINARY_URL = f"http://{BINARY_HOST}"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def run_nmap_scan():
    print(f"\n📡 Running: nmap -sV --version-light -p{BINARY_PORT_RANGE} {BINARY_HOST}\n")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "--version-light", f"-p{BINARY_PORT_RANGE}", BINARY_HOST],
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
            ["curl", "-s", f"{BINARY_URL}:{port}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: curl is not installed.")
        sys.exit(1)

def main():
    clear_screen()
    print("🛰️ Nmap Scan Puzzle")
    print("--------------------------------------\n")
    print("Several simulated services are running locally (inside your CTF app).\n")
    print("🎯 Your goal: Scan localhost for open ports in the range 8000–8100, and find the REAL flag.")
    print("⚠️ Some ports contain random junk responses. Only one flag is correct.\n")
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
        print("❌ No open ports found in the range.")
        pause("Press ENTER to exit...")
        sys.exit(1)

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
            print(f"\n🌐 Connecting to {BINARY_URL}:{port} ...")
            print("--------------------------------------")
            response = fetch_port_response(port)
            print(response if response else f"⚠️ No response received from port {port}.")
            print("--------------------------------------\n")

            while True:
                print("Options:")
                print("1. 🔁 Return to port list")
                print("2. 💾 Save this response to nmap_flag_response.txt\n")

                sub_choice = input("Choose an option (1-2): ").strip()
                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    with open("nmap_flag_response.txt", "a") as f:
                        f.write(f"Port: {port}\nResponse:\n{response}\n")
                        f.write("--------------------------------------\n")
                    print("✅ Response saved to nmap_flag_response.txt")
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
    main()
