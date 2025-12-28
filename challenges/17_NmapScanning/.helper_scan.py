#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Configuration ===
BINARY_PORT_RANGE = "8000-8100"
BINARY_HOST = "localhost"
BINARY_URL = f"http://{BINARY_HOST}"
SAVE_FILE = "nmap_flag_response.txt"

# === Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="🔸 Press ENTER to continue..."):
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

# === Nmap Scan ===
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
        print("❌ ERROR: `nmap` is not installed.")
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

# === Curl Requests ===
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
        print("❌ ERROR: `curl` is not installed.")
        sys.exit(1)

# === Main Program ===
def main():
    resize_terminal(35, 90)
    clear_screen()
    print("🛰️  Nmap Scan Puzzle")
    print("======================================\n")
    print("Several simulated services are running locally.")
    print("🎯 Your goal: Find the REAL flag by scanning ports 8000–8100.")
    print("⚠️  Beware! Many ports return fake or junk data.\n")
    print("🧠 Flag format to watch for: CCRI-AAAA-1111\n")
    print("In a real terminal, you might do something like:\n")
    print(f"   nmap -sV --version-light -p{BINARY_PORT_RANGE} {BINARY_HOST}")
    print("   curl http://localhost:8000")
    print("   curl http://localhost:8001")
    print("   ...and so on, until you find something interesting.\n")
    print("This helper script automates that workflow by:")
    print("   ➤ Running the nmap scan for you")
    print("   ➤ Listing only the open ports")
    print("   ➤ Letting you query each port with curl and inspect the response\n")
    
    require_input("Type 'scan' when you're ready to run the nmap scan: ", "scan")

    scan_output = run_nmap_scan()
    clear_screen()
    print("📝 Nmap Scan Results")
    print("======================================")
    print(scan_output)
    print("\n✅ Scan complete.\n")

    require_input("📖 Look over the open ports above, then type 'explore' to check them interactively: ", "explore")

    open_ports = extract_open_ports(scan_output)

    if not open_ports:
        print("❌ No open ports found.")
        pause()
        sys.exit(1)

    while True:
        clear_screen()
        print("🌐 Open Ports:")
        print("======================================")
        for idx, port in enumerate(open_ports, 1):
            print(f"{idx:2d}. Port {port}")
        print(f"{len(open_ports)+1:2d}. 🚪 Exit\n")

        try:
            choice = int(input(f"🔍 Select a port to explore (1-{len(open_ports)+1}): ").strip())
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        if 1 <= choice <= len(open_ports):
            port = open_ports[choice - 1]
            clear_screen()
            print(f"🔎 Connecting to {BINARY_URL}:{port}")
            print("======================================")
            print(f"(Under the hood this is running: curl -s {BINARY_URL}:{port})\n")
            response = fetch_port_response(port)
            print(response if response else f"⚠️ No response received from port {port}.")
            print("======================================\n")

            while True:
                print("Options:")
                print("  [1] 🔁 Return to port list")
                print("  [2] 💾 Save this response to file\n")
                sub_choice = input("Choose an action (1-2): ").strip()

                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    with open(SAVE_FILE, "a", encoding="utf-8") as f:
                        f.write(f"Port: {port}\nResponse:\n{response}\n")
                        f.write("======================================\n")
                    print(f"✅ Response saved to {SAVE_FILE}")
                    time.sleep(1)
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
                    time.sleep(1)

        elif choice == len(open_ports)+1:
            print("\n👋 Exiting scanner. Good luck with the flag!")
            break
        else:
            print("❌ Invalid choice. Please choose a valid port.")
            time.sleep(1)

if __name__ == "__main__":
    main()