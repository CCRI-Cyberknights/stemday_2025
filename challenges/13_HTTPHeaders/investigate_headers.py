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
    """
    Pauses and requires the user to type a specific word (case-insensitive) to continue.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

# === Network / Scan Helpers ===
def inspect_headers(endpoint_num):
    """
    Runs curl -I against the specific endpoint to show headers.
    """
    url = f"http://localhost:5000/mystery/endpoint_{endpoint_num}"
    print(f"\n🔍 Inspecting headers for Endpoint #{endpoint_num}...")
    print(f"💻 Running: curl -I {url}\n")
    print("-" * 60)
    
    try:
        # -I means "Fetch headers only" (HEAD request)
        subprocess.run(["curl", "-I", url], check=False)
    except FileNotFoundError:
        print("❌ ERROR: 'curl' command not found. Is it installed?")
    
    print("-" * 60)
    print("\n(Scroll up to see the headers)")
    pause()

def bulk_scan():
    """
    Loops through all 5 endpoints, fetches headers, and greps for the flag pattern.
    """
    print("\n🔎 Bulk scanning all endpoints for flags...")
    print("💻 Logic: for i in {1..5}; do curl -I ... | grep 'CCRI-'; done\n")
    
    found_any = False
    
    for i in range(1, 6):
        url = f"http://localhost:5000/mystery/endpoint_{i}"
        try:
            # Run curl silently (-s), fetch headers (-I), and pipe output to grep
            # We do this in python by capturing stdout and searching it
            result = subprocess.run(
                ["curl", "-I", "-s", url],
                capture_output=True,
                text=True
            )
            
            # Simple manual grep implementation
            for line in result.stdout.splitlines():
                if "CCRI-" in line:
                    print(f"✅ FOUND in Endpoint #{i}:")
                    print(f"   {line.strip()}")
                    found_any = True

        except Exception as e:
            print(f"❌ Error scanning Endpoint #{i}: {e}")

    if not found_any:
        print("⚠️ No flag-like patterns found in the headers.")

# === Main Flow ===
def main():
    resize_terminal(35, 90)

    clear_screen()
    print("📡 HTTP Headers Mystery (Live Network Edition)")
    print("=============================================\n")
    print("🎯 Mission Briefing:")
    print("---------------------------------")
    print("You have discovered **five active API endpoints** on the local network.")
    print("The real flag is hidden in the HTTP Headers of exactly ONE of them.\n")
    print("🧠 Flag format: CCRI-AAAA-1111\n")
    print("💡 Quick HTTP refresher:")
    print("   ➤ Web servers send 'Headers' before the actual content (HTML/JSON).")
    print("   ➤ These headers contain metadata like `Server:`, `Content-Type:`, etc.")
    print("   ➤ In this challenge, a custom header (`X-Flag`) contains the secret.\n")
    
    require_input("Type 'ready' when you're ready to learn the tools: ", "ready")

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("----------------------------")
    print("Since these are live web addresses, we can't just use `cat` or `less`.")
    print("We need a tool that talks to web servers. We will use **curl**.\n")
    print("1. To see headers ONLY (HEAD request):")
    print("   curl -I http://localhost:5000/mystery/endpoint_1\n")
    print("2. To search for the flag across all endpoints:")
    print("   curl -I http://localhost:5000/mystery/endpoint_1 | grep 'CCRI-'")
    print("   (Repeated for endpoints 1 through 5)\n")
    
    require_input("Type 'start' when you're ready to scan the network: ", "start")

    while True:
        clear_screen()
        print("🌐 Active Network Endpoints:")
        print("1. http://localhost:5000/mystery/endpoint_1")
        print("2. http://localhost:5000/mystery/endpoint_2")
        print("3. http://localhost:5000/mystery/endpoint_3")
        print("4. http://localhost:5000/mystery/endpoint_4")
        print("5. http://localhost:5000/mystery/endpoint_5")
        print("\n6. ⚡ Run Automated Bulk Scan (Check all headers)")
        print("7. Exit\n")

        choice = input("Select an option (1–7): ").strip().lower()

        if choice in {"1", "2", "3", "4", "5"}:
            inspect_headers(choice)

        elif choice == "6":
            bulk_scan()
            pause("\nPress ENTER to return to the menu.")

        elif choice == "7":
            print("\n👋 Exiting HTTP Headers Mystery. Good luck!")
            break

        else:
            print("\n❌ Invalid option.")
            pause()

if __name__ == "__main__":
    main()