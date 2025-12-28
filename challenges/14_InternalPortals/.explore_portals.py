#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
    
def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def require_input(prompt, expected):
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

# === Network Helpers ===
def open_in_browser(subdomain):
    """
    Open the internal URL in the system's default browser.
    """
    url = f"http://localhost:5000/internal/{subdomain}"
    print(f"\n🌐 Opening {subdomain.upper()} Portal...")
    print(f"🔗 URL: {url}")
    
    try:
        # xdg-open works on Linux to open the default browser
        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("❌ ERROR: 'xdg-open' not found. Please open the URL manually.")

def auto_scan_network():
    """
    Simulates a vulnerability scanner by curling all endpoints and grepping for flags.
    """
    domains = ["alpha", "beta", "gamma", "delta", "omega"]
    print("\n🔎 Running Network Scraper (curl + grep)...")
    print("💻 Logic: for site in portals; do curl {site} | grep 'CCRI-'; done\n")
    
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
                    print(f"✅ FOUND in {dom.upper()} Portal:")
                    # This will print the <span> line
                    print(f"   {line.strip()}")
                    found_any = True
                    
        except Exception as e:
            print(f"❌ Connection failed for {dom}: {e}")

    if not found_any:
        print("⚠️ No flag patterns found in the visible HTML.")
        print("   (Did you check the Page Source for hidden tags?)")

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    
    clear_screen()
    print("🌐 Internal Portals Access")
    print("=================================\n")
    print("🎯 Mission Briefing:")
    print("We have identified five internal portals used by the target organization.")
    print("One of these portals has a secret flag hardcoded in its HTML source.\n")
    print("🧠 Flag format: CCRI-AAAA-1111")
    print("💡 Web Hacking Tip:")
    print("   Developers often hide system info in hidden DOM elements.")
    print("   These are invisible on the rendered page but visible in the **Source Code**.\n")
    print("   ➤ Look for tags with: style='display:none' or \n")
    
    require_input("Type 'start' when you're ready to begin the audit: ", "start")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("----------------------------")
    print("In a real engagement, you would visit these sites and inspect them.")
    print("\n1. Manual Method (Browser):")
    print("   - Visit http://localhost:5000/internal/alpha")
    print("   - Right-click -> **View Page Source** (or Ctrl+U)")
    print("   - Search (Ctrl+F) for 'CCRI' or 'flag'")
    print("\n2. Automated Method (Command Line):")
    print("   - Use `curl` to download the HTML code")
    print("   - Pipe it to `grep` to find the pattern")
    print("   - Example: curl -s http://localhost:5000/internal/alpha | grep 'CCRI-'")
    
    require_input("Type 'go' to access the network menu: ", "go")

    domains = ["alpha", "beta", "gamma", "delta", "omega"]

    while True:
        print("\n📂 Identified Internal Portals:")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain.upper()} Portal")
        print("6. 🔎 Auto-scan all portals (curl + grep)")
        print("7. ❌ Exit\n")

        choice = input("Select an option (1–7): ").strip().lower()

        if choice in {"1", "2", "3", "4", "5"}:
            idx = int(choice) - 1
            target = domains[idx]
            
            print(f"\n🚀 Launching browser for {target}...")
            open_in_browser(target)
            
            print("\n👉 ACTION REQUIRED:")
            print(f"   1. Switch to your browser window.")
            print(f"   2. Press **Ctrl+U** to view the source code.")
            print(f"   3. Look for hidden spans or system tags!")
            pause()
            clear_screen()

        elif choice == "6":
            auto_scan_network()
            pause("\nPress ENTER to return to the menu.")
            clear_screen()

        elif choice == "7":
            print("\n👋 Exiting Internal Portals. Happy hunting!")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 7.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()