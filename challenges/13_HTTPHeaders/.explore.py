#!/usr/bin/env python3
import os
import subprocess
import sys
import socket
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, print_info, resize_terminal, clear_screen, spinner

# === Config ===
LOG_FILE = "server_logs.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def check_web_server():
    """Checks if the CTF web server is running on port 5000."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result != 0:
            print_error("The Web Server is not running!")
            print("   This challenge requires the background web services.")
            print(f"   👉 Open a new terminal and run: {Colors.BOLD}python3 start_web_hub.py{Colors.END}\n")
            sys.exit(1)
    except Exception:
        pass

def inspect_headers(endpoint_num):
    """Runs curl -I against the specific endpoint to show headers."""
    url = f"http://localhost:5000/mystery/endpoint_{endpoint_num}"
    
    print(f"\n🔍 Inspecting headers for {Colors.BOLD}Endpoint #{endpoint_num}{Colors.END}...")
    print(f"💻 Running: {Colors.CYAN}curl -I {url}{Colors.END}\n")
    print("-" * 60)
    
    try:
        # -I means "Fetch headers only" (HEAD request)
        subprocess.run(["curl", "-I", url], check=False)
    except FileNotFoundError:
        print_error("'curl' command not found. Is it installed?")
    
    print("-" * 60)
    print(f"\n{Colors.CYAN}👀 Look closely at the headers above. See any 'X-Flag'?{Colors.END}")
    pause()

def bulk_scan():
    """Loops through all 5 endpoints."""
    print(f"\n{Colors.CYAN}🔎 Bulk scanning all endpoints...{Colors.END}")
    print(f"💻 Simulation of: {Colors.BOLD}curl -I \"http://localhost:5000/mystery/endpoint_[1-5]\"{Colors.END}\n")
    
    found_any = False
    
    for i in range(1, 6):
        url = f"http://localhost:5000/mystery/endpoint_{i}"
        print(f"   Testing {url}...", end="", flush=True)
        time.sleep(0.2)
        
        try:
            # Run curl silently (-s), fetch headers (-I)
            result = subprocess.run(
                ["curl", "-I", "-s", url],
                capture_output=True,
                text=True
            )
            
            # Check output for flag
            if "CCRI-" in result.stdout:
                print(f" {Colors.GREEN}MATCH FOUND!{Colors.END}")
                print("-" * 50)
                # Find the specific line
                for line in result.stdout.splitlines():
                    if "CCRI-" in line:
                        print(f"   {Colors.BOLD}{line.strip()}{Colors.END}")
                print("-" * 50 + "\n")
                found_any = True
            else:
                print(f" {Colors.RED}No flag.{Colors.END}")

        except Exception as e:
            print_error(f"Error scanning Endpoint #{i}: {e}")

    if found_any:
        print_success("Target identified.")
    else:
        print_error("No flag-like patterns found in the headers.")
    
    pause()

def main():
    # 1. Setup
    resize_terminal(35, 90)
    check_web_server()
    log_path = get_path(LOG_FILE)

    # 2. Mission Briefing
    header("📡 HTTP Header Interceptor")
    
    print(f"📄 Log File: {Colors.BOLD}{LOG_FILE}{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}curl -I{Colors.END}\n")
    print("🎯 Goal: Interrogate the active endpoints to find the hidden header.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Concept:** Web servers send \"invisible data\" (Headers) before content.")
    print("   ➤ **The Lock:** The flag is hidden in a custom header (e.g., `X-Flag`).")
    print("   ➤ **The Tool:** `curl -I` fetches *only* the headers, skipping the body.\n")
    
    require_input("Type 'ready' to read the intercepted logs: ", "ready")

    # 3. Discovery
    header("🔍 Phase 1: Reconnaissance")
    print(f"Let's see which endpoints are active by reading {LOG_FILE}.\n")
    
    if os.path.exists(log_path):
        print("-" * 50)
        with open(log_path, "r") as f:
            print(f"{Colors.YELLOW}{f.read().strip()}{Colors.END}")
        print("-" * 50 + "\n")
    else:
        print_error(f"{LOG_FILE} missing. (The server might generate it automatically).")
        print("We will assume endpoints 1 through 5 are active.")

    print("We have identified 5 targets: endpoint_1 through endpoint_5.\n")
    require_input("Type 'load' to power up the curl tool: ", "load")

    # 4. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("To check these manually, we use `curl`.\n")
    print("Command to be executed:\n")
    print(f"   {Colors.GREEN}curl -I http://localhost:5000/mystery/endpoint_1{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}curl{Colors.END}       → Client URL (the web tool)")
    print(f"   {Colors.BOLD}-I{Colors.END}         → Info/Head (Fetch HEADERS only, ignore the page content)")
    
    require_input("Type 'start' to begin the interrogation: ", "start")

    # 5. Interactive Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}🌐 Interrogation Console{Colors.END}")
        print("1. Inspect Endpoint 1")
        print("2. Inspect Endpoint 2")
        print("3. Inspect Endpoint 3")
        print("4. Inspect Endpoint 4")
        print("5. Inspect Endpoint 5")
        print(f"\n6. {Colors.BOLD}⚡ Run Bulk Scan (Check all at once){Colors.END}")
        print("7. Exit\n")

        choice = input(f"{Colors.YELLOW}Select target (1–7): {Colors.END}").strip()

        if choice in {"1", "2", "3", "4", "5"}:
            inspect_headers(choice)

        elif choice == "6":
            bulk_scan()

        elif choice == "7":
            print(f"\n{Colors.CYAN}👋 Exiting.{Colors.END}")
            break

        else:
            print_error("Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    main()