#!/usr/bin/env python3
import os
import subprocess
import sys

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, resize_terminal, clear_screen

# === Network / Scan Helpers ===
def inspect_headers(endpoint_num):
    """
    Runs curl -I against the specific endpoint to show headers.
    """
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
    print("\n(Scroll up to see the headers)")
    pause()

def bulk_scan():
    """
    Loops through all 5 endpoints, fetches headers, and greps for the flag pattern.
    """
    print(f"\n{Colors.CYAN}🔎 Bulk scanning all endpoints for flags...{Colors.END}")
    print(f"💻 Logic: {Colors.BOLD}for i in {{1..5}}; do curl -I ... | grep 'CCRI-'; done{Colors.END}\n")
    
    found_any = False
    
    for i in range(1, 6):
        url = f"http://localhost:5000/mystery/endpoint_{i}"
        try:
            # Run curl silently (-s), fetch headers (-I), and pipe output to grep
            result = subprocess.run(
                ["curl", "-I", "-s", url],
                capture_output=True,
                text=True
            )
            
            # Simple manual grep implementation
            for line in result.stdout.splitlines():
                if "CCRI-" in line:
                    print_success(f"FOUND in Endpoint #{i}:")
                    # Highlight the flag if found
                    parts = line.strip().split("CCRI-")
                    if len(parts) > 1:
                        print(f"   {parts[0]}{Colors.GREEN}{Colors.BOLD}CCRI-{parts[1]}{Colors.END}")
                    else:
                        print(f"   {line.strip()}")
                    found_any = True

        except Exception as e:
            print_error(f"Error scanning Endpoint #{i}: {e}")

    if not found_any:
        print_error("No flag-like patterns found in the headers.")

# === Main Flow ===
def main():
    resize_terminal(35, 90)

    # 1. Mission Briefing
    header("📡 HTTP Headers Mystery (Live Network Edition)")
    
    print("🎯 Mission Briefing:")
    print("-" * 40)
    print("You have discovered **five active API endpoints** on the local network.")
    print("The real flag is hidden in the HTTP Headers of exactly ONE of them.\n")
    print(f"{Colors.CYAN}🧠 Flag format: CCRI-AAAA-1111{Colors.END}\n")
    print(f"{Colors.YELLOW}💡 Quick HTTP refresher:{Colors.END}")
    print("   ➤ Web servers send 'Headers' before the actual content (HTML/JSON).")
    print("   ➤ These headers contain metadata like `Server:`, `Content-Type:`, etc.")
    print("   ➤ In this challenge, a custom header (`X-Flag`) contains the secret.\n")
    
    require_input("Type 'ready' when you're ready to learn the tools: ", "ready")

    # 2. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("Since these are live web addresses, we can't just use `cat` or `less`.")
    print("We need a tool that talks to web servers. We will use **curl**.\n")
    print("1. To see headers ONLY (HEAD request):")
    print(f"   {Colors.GREEN}curl -I http://localhost:5000/mystery/endpoint_1{Colors.END}\n")
    print("2. To search for the flag across all endpoints:")
    print(f"   {Colors.GREEN}curl -I http://localhost:5000/mystery/endpoint_1 | grep 'CCRI-'{Colors.END}")
    print("   (Repeated for endpoints 1 through 5)\n")
    
    require_input("Type 'start' when you're ready to scan the network: ", "start")

    # 3. Main Menu Loop
    while True:
        clear_screen()
        print(f"{Colors.CYAN}🌐 Active Network Endpoints:{Colors.END}")
        print("1. http://localhost:5000/mystery/endpoint_1")
        print("2. http://localhost:5000/mystery/endpoint_2")
        print("3. http://localhost:5000/mystery/endpoint_3")
        print("4. http://localhost:5000/mystery/endpoint_4")
        print("5. http://localhost:5000/mystery/endpoint_5")
        print(f"\n6. {Colors.BOLD}⚡ Run Automated Bulk Scan (Check all headers){Colors.END}")
        print("7. Exit\n")

        choice = input(f"{Colors.YELLOW}Select an option (1–7): {Colors.END}").strip().lower()

        if choice in {"1", "2", "3", "4", "5"}:
            inspect_headers(choice)

        elif choice == "6":
            bulk_scan()
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print(f"\n{Colors.CYAN}👋 Exiting HTTP Headers Mystery. Good luck!{Colors.END}")
            break

        else:
            print_error("Invalid option.")
            pause()

if __name__ == "__main__":
    main()