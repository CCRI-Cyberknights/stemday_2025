#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, print_success, print_error, print_info, resize_terminal, clear_screen

# === Network Helpers ===
def open_in_browser(subdomain):
    """
    Open the internal URL in the system's default browser.
    """
    url = f"http://localhost:5000/internal/{subdomain}"
    print_info(f"Opening {Colors.BOLD}{subdomain.upper()}{Colors.END} Portal...")
    print(f"🔗 URL: {Colors.CYAN}{url}{Colors.END}")
    
    try:
        # xdg-open works on Linux to open the default browser
        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print_error("'xdg-open' not found. Please open the URL manually.")

def auto_scan_network():
    """
    Simulates a vulnerability scanner by curling all endpoints and grepping for flags.
    """
    domains = ["alpha", "beta", "gamma", "delta", "omega"]
    print(f"\n{Colors.CYAN}🔎 Running Network Scraper (curl + grep)...{Colors.END}")
    print(f"💻 Logic: {Colors.BOLD}for site in portals; do curl {{site}} | grep 'CCRI-'; done{Colors.END}\n")
    
    found_any = False
    
    for dom in domains:
        url = f"http://localhost:5000/internal/{dom}"
        try:
            # -s = silent, -L = follow redirects
            result = subprocess.run(
                ["curl", "-s", "-L", url],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.splitlines():
                if "CCRI-" in line:
                    print_success(f"FOUND in {dom.upper()} Portal:")
                    # Highlight the flag
                    if "CCRI-" in line:
                        parts = line.strip().split("CCRI-")
                        print(f"   {parts[0]}{Colors.GREEN}{Colors.BOLD}CCRI-{parts[1]}{Colors.END}")
                    else:
                        print(f"   {line.strip()}")
                    found_any = True
                    
        except Exception as e:
            print_error(f"Connection failed for {dom}: {e}")

    if not found_any:
        print_error("No flag patterns found in the visible HTML.")
        print_info("(Did you check the Page Source for hidden tags?)")

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    
    # 1. Mission Briefing
    header("🌐 Internal Portals Access")
    
    print("🎯 Mission Briefing:")
    print("-" * 40)
    print("We have identified five internal portals used by the target organization.")
    print("One of these portals has a secret flag hardcoded in its HTML source.\n")
    print(f"{Colors.CYAN}🧠 Flag format: CCRI-AAAA-1111{Colors.END}")
    print(f"{Colors.YELLOW}💡 Web Hacking Tip:{Colors.END}")
    print("   Developers often hide system info in hidden DOM elements.")
    print("   These are invisible on the rendered page but visible in the **Source Code**.\n")
    print(f"   ➤ Look for tags with: {Colors.GREEN}style='display:none'{Colors.END} or {Colors.GREEN}{Colors.END}\n")
    
    require_input("Type 'start' when you're ready to begin the audit: ", "start")

    # 2. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("In a real engagement, you would visit these sites and inspect them.")
    print(f"\n1. {Colors.BOLD}Manual Method (Browser):{Colors.END}")
    print(f"   - Visit {Colors.CYAN}http://localhost:5000/internal/alpha{Colors.END}")
    print("   - Right-click -> **View Page Source** (or Ctrl+U)")
    print("   - Search (Ctrl+F) for 'CCRI' or 'flag'")
    print(f"\n2. {Colors.BOLD}Automated Method (Command Line):{Colors.END}")
    print("   - Use `curl` to download the HTML code")
    print("   - Pipe it to `grep` to find the pattern")
    print(f"   - Example: {Colors.GREEN}curl -s http://localhost:5000/internal/alpha | grep 'CCRI-'{Colors.END}")
    
    require_input("Type 'go' to access the network menu: ", "go")

    domains = ["alpha", "beta", "gamma", "delta", "omega"]

    # 3. Main Menu
    while True:
        clear_screen()
        print(f"{Colors.CYAN}📂 Identified Internal Portals:{Colors.END}")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain.upper()} Portal")
        print(f"6. {Colors.BOLD}🔎 Auto-scan all portals (curl + grep){Colors.END}")
        print("7. ❌ Exit\n")

        choice = input(f"{Colors.YELLOW}Select an option (1–7): {Colors.END}").strip().lower()

        if choice in {"1", "2", "3", "4", "5"}:
            idx = int(choice) - 1
            target = domains[idx]
            
            print(f"\n🚀 Launching browser for {Colors.BOLD}{target}{Colors.END}...")
            open_in_browser(target)
            
            print(f"\n{Colors.YELLOW}👉 ACTION REQUIRED:{Colors.END}")
            print(f"   1. Switch to your browser window.")
            print(f"   2. Press {Colors.BOLD}Ctrl+U{Colors.END} to view the source code.")
            print(f"   3. Look for hidden spans or system tags!")
            pause()

        elif choice == "6":
            auto_scan_network()
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print(f"\n{Colors.CYAN}👋 Exiting Internal Portals. Happy hunting!{Colors.END}")
            break

        else:
            print_error("Invalid choice. Please enter a number from 1 to 7.")
            pause()

if __name__ == "__main__":
    main()