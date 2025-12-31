#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, print_info, resize_terminal, clear_screen

# === Configuration ===
BINARY_PORT_RANGE = "8000-8100"
BINARY_HOST = "localhost"
BINARY_URL = f"http://{BINARY_HOST}"
SAVE_FILE = "nmap_flag_response.txt"

# === Nmap Scan ===
def run_nmap_scan():
    print(f"\n📡 Running: {Colors.BOLD}nmap -sV --version-light -p{BINARY_PORT_RANGE} {BINARY_HOST}{Colors.END}\n")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "--version-light", f"-p{BINARY_PORT_RANGE}", BINARY_HOST],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        return result.stdout
    except FileNotFoundError:
        print_error("`nmap` is not installed.")
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
        print_error("`curl` is not installed.")
        sys.exit(1)

# === Main Program ===
def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    # 2. Mission Briefing
    header("🛰️  Nmap Scan Puzzle")
    
    print("Several simulated services are running locally.")
    print("🎯 Your goal: Find the REAL flag by scanning ports 8000–8100.")
    print(f"{Colors.RED}⚠️  Beware! Many ports return fake or junk data.{Colors.END}\n")
    print(f"{Colors.CYAN}🧠 Flag format to watch for: CCRI-AAAA-1111{Colors.END}\n")
    
    print("In a real terminal, you might do something like:")
    print(f"   {Colors.GREEN}nmap -sV --version-light -p{BINARY_PORT_RANGE} {BINARY_HOST}{Colors.END}")
    print(f"   {Colors.GREEN}curl http://localhost:8000{Colors.END}")
    print(f"   {Colors.GREEN}curl http://localhost:8001{Colors.END}")
    print("   ...and so on, until you find something interesting.\n")
    
    print("This helper script automates that workflow by:")
    print("   ➤ Running the nmap scan for you")
    print("   ➤ Listing only the open ports")
    print("   ➤ Letting you query each port with curl and inspect the response\n")
    
    require_input("Type 'scan' when you're ready to run the nmap scan: ", "scan")

    scan_output = run_nmap_scan()
    
    clear_screen()
    print(f"{Colors.CYAN}📝 Nmap Scan Results{Colors.END}")
    print("======================================")
    print(scan_output)
    print("\n✅ Scan complete.\n")

    require_input("📖 Look over the open ports above, then type 'explore' to check them interactively: ", "explore")

    open_ports = extract_open_ports(scan_output)

    if not open_ports:
        print_error("No open ports found.")
        pause()
        sys.exit(1)

    while True:
        clear_screen()
        print(f"{Colors.CYAN}🌐 Open Ports:{Colors.END}")
        print("======================================")
        for idx, port in enumerate(open_ports, 1):
            print(f"{Colors.BOLD}{idx:2d}. Port {port}{Colors.END}")
        print(f"{len(open_ports)+1:2d}. 🚪 Exit\n")

        try:
            choice = int(input(f"{Colors.YELLOW}🔍 Select a port to explore (1-{len(open_ports)+1}): {Colors.END}").strip())
        except ValueError:
            print_error("Invalid input. Please enter a number.")
            time.sleep(1)
            continue

        if 1 <= choice <= len(open_ports):
            port = open_ports[choice - 1]
            clear_screen()
            print(f"🔎 Connecting to {Colors.BOLD}{BINARY_URL}:{port}{Colors.END}")
            print("======================================")
            print(f"(Under the hood this is running: {Colors.GREEN}curl -s {BINARY_URL}:{port}{Colors.END})\n")
            
            response = fetch_port_response(port)
            
            if response:
                print(f"{Colors.GREEN}{response}{Colors.END}")
            else:
                print(f"{Colors.RED}⚠️ No response received from port {port}.{Colors.END}")
            print("======================================\n")

            while True:
                print("Options:")
                print("  [1] 🔁 Return to port list")
                print("  [2] 💾 Save this response to file\n")
                sub_choice = input(f"{Colors.YELLOW}Choose an action (1-2): {Colors.END}").strip()

                if sub_choice == "1":
                    break
                elif sub_choice == "2":
                    with open(SAVE_FILE, "a", encoding="utf-8") as f:
                        f.write(f"Port: {port}\nResponse:\n{response}\n")
                        f.write("======================================\n")
                    print_success(f"Response saved to {SAVE_FILE}")
                    time.sleep(1)
                    break
                else:
                    print_error("Invalid choice. Please select 1 or 2.")
                    time.sleep(1)

        elif choice == len(open_ports)+1:
            print(f"\n{Colors.CYAN}👋 Exiting scanner. Good luck with the flag!{Colors.END}")
            break
        else:
            print_error("Invalid choice. Please choose a valid port.")
            time.sleep(1)

if __name__ == "__main__":
    main()