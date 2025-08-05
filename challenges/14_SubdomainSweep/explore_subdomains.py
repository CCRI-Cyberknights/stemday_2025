#!/usr/bin/env python3
import os
import sys
import subprocess

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def flatten_html_files(script_dir):
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.endswith(".html") and root != script_dir:
                src = os.path.join(root, f)
                dst = os.path.join(script_dir, f)
                if not os.path.exists(dst):
                    os.rename(src, dst)
        for d in dirs:
            try:
                os.rmdir(os.path.join(root, d))
            except OSError:
                pass

def check_html_files(domains, script_dir):
    missing = []
    for domain in domains:
        html_file = os.path.join(script_dir, f"{domain}.liber8.local.html")
        if not os.path.isfile(html_file):
            print(f"❌ ERROR: Missing file '{os.path.basename(html_file)}'")
            missing.append(html_file)
    return missing

def open_in_browser(file_path):
    try:
        subprocess.Popen(["xdg-open", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ ERROR: Could not open browser (xdg-open not found).")

def auto_scan_for_flags(script_dir):
    try:
        result = subprocess.run(
            ["grep", "-E", "CCRI-[A-Z]{4}-[0-9]{4}", os.path.join(script_dir, "*.html")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        print(result.stdout if result.stdout else "⚠️ No flags found in auto-scan.")
    except Exception as e:
        print(f"❌ ERROR during auto-scan: {e}")

def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    domains = ["alpha", "beta", "gamma", "delta", "omega"]

    flatten_html_files(script_dir)

    clear_screen()
    print("🌐 Subdomain Sweep")
    print("=================================\n")
    print("🎯 Mission Briefing:")
    print("You've discovered **five subdomains** hosted by the target organization.")
    print("Each one has an HTML page that *might* hide a secret flag.\n")
    print("🧠 Flag format: CCRI-AAAA-1111")
    print("💡 In real CTFs, you'd use tools like curl, grep, or open the page in a browser to search for hidden data.\n")

    if check_html_files(domains, script_dir):
        pause("\n⚠️ One or more HTML files are missing. Press ENTER to exit.")
        sys.exit(1)

    while True:
        print("\n📂 Available subdomains:")
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}.liber8.local")
        print("6. Auto-scan all subdomains for flag patterns")
        print("7. Exit\n")

        choice = input("Select an option (1–7): ").strip()

        if choice in {"1", "2", "3", "4", "5"}:
            idx = int(choice) - 1
            html_file = os.path.join(script_dir, f"{domains[idx]}.liber8.local.html")
            print(f"\n🌐 Opening {os.path.basename(html_file)} in your browser...")
            open_in_browser(html_file)
            print("\n💻 Tip: View the page AND its source (Ctrl+U) for hidden data.")
            pause("Press ENTER to return to the menu.")
            clear_screen()

        elif choice == "6":
            print("\n🔎 Auto-scanning all subdomains for flags using:")
            print("    grep -E 'CCRI-[A-Z]{4}-[0-9]{4}' *.html\n")
            auto_scan_for_flags(script_dir)
            pause("\nPress ENTER to return to the menu.")
            clear_screen()

        elif choice == "7":
            print("\n👋 Exiting Subdomain Sweep. Stay sharp, agent!")
            break

        else:
            print("\n❌ Invalid choice. Please enter a number from 1 to 7.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
