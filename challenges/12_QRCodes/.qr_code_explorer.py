#!/usr/bin/env python3
import os
import subprocess
import time
import sys
import shutil

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === QR Helpers ===
def open_image(file_path, duration=10):
    """Open an image using a specific viewer to ensure we can close it."""
    viewers = ["eom", "eog", "feh", "display", "ristretto"]
    viewer_cmd = "xdg-open" # Fallback
    
    for v in viewers:
        if shutil.which(v):
            viewer_cmd = v
            break

    try:
        # Popen keeps a handle on the specific process
        viewer = subprocess.Popen(
            [viewer_cmd, file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Show a countdown timer while waiting
        for i in range(duration, 0, -1):
            sys.stdout.write(f"\r{Colors.YELLOW}⏳ Closing in {i} seconds... {Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
            # If the student closes it early, stop counting
            if viewer.poll() is not None:
                sys.stdout.write(f"\r{Colors.GREEN}✅ Image closed.             {Colors.END}")
                sys.stdout.flush()
                break
        else:
            sys.stdout.write(f"\r{Colors.YELLOW}⏳ Time’s up! Closing viewer.{Colors.END}")
            sys.stdout.flush()

        # Force close if it's still running
        if viewer.poll() is None:
            viewer.terminate()
            
        print() # New Line

    except Exception as e:
        print_error(f"Could not open image: {e}")

def decode_qr(file_path):
    """Run zbarimg to extract QR content."""
    try:
        result = subprocess.run(
            ["zbarimg", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print_error("zbarimg is not installed.")
        return ""

def main():
    # 1. Setup
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    qr_codes = [os.path.join(script_dir, f"qr_0{i}.png") for i in range(1, 6)]

    # 2. Mission Briefing
    header("📦 QR Code Explorer")
    
    print("🎯 Mission Briefing:")
    print("-" * 30)
    print("🔍 You’ve recovered 5 mysterious QR codes from a digital drop site.")
    print("Each one may contain:")
    print("  • A secret message")
    print("  • A fake flag")
    print(f"  • Or… the {Colors.BOLD}real flag{Colors.END} in CCRI-AAAA-1111 format!\n")
    
    print(f"{Colors.CYAN}🛠️ Your options:{Colors.END}")
    print("  • Scan with your phone’s QR scanner")
    print("  • OR use this tool to open and auto-decode them\n")
    
    print(f"{Colors.CYAN}📖 Behind the scenes, this script will use a command like:{Colors.END}")
    print(f"     {Colors.GREEN}zbarimg qr_01.png{Colors.END}")
    print("   to read the QR code and print its contents.\n")
    
    print("⏳ Each QR opens for 10 seconds so you can inspect it,")
    print("   then the script decodes the QR and saves the result to a .txt file.\n")

    require_input("Type 'start' when you're ready to explore the QR codes: ", "start")
    clear_screen()

    # 3. Interactive Loop
    while True:
        header("🗂️  Available QR codes")
        for i, qr in enumerate(qr_codes, 1):
            print(f"{Colors.BOLD}{i}{Colors.END}. {os.path.basename(qr)}")
        print(f"{len(qr_codes)+1}. Exit Explorer\n")

        choice = input(f"{Colors.YELLOW}Select a QR code (1-{len(qr_codes)+1}): {Colors.END}").strip()

        if choice == str(len(qr_codes) + 1):
            print(f"\n{Colors.CYAN}👋 Exiting QR Explorer.{Colors.END}")
            break

        if not choice.isdigit():
            print_error("Invalid input. Please enter a number.")
            pause()
            continue

        index = int(choice) - 1
        if 0 <= index < len(qr_codes):
            file_path = qr_codes[index]
            txt_file = file_path.replace(".png", ".txt")

            clear_screen()
            print(f"🖼️ Opening {Colors.BOLD}{os.path.basename(file_path)}{Colors.END}...")
            open_image(file_path)

            print(f"\n🔎 Scanning {Colors.BOLD}{os.path.basename(file_path)}{Colors.END}...")
            print(f"💻 Running: {Colors.GREEN}zbarimg \"{os.path.basename(file_path)}\"{Colors.END}")

            spinner("Decoding QR")
            result = decode_qr(file_path)
            print("\n")

            if not result:
                print_error("No QR code found or could not decode.")
            else:
                print_success("Decoded Result:")
                print("-" * 40)
                print(f"{Colors.BOLD}{result}{Colors.END}")
                print("-" * 40)
                try:
                    with open(txt_file, "w", encoding="utf-8") as f:
                        f.write(result + "\n")
                    print(f"💾 Saved to: {Colors.BOLD}{os.path.basename(txt_file)}{Colors.END}")
                except Exception as e:
                    print_error(f"Could not save output: {e}")

            pause()
        else:
            print_error(f"Invalid selection. Please choose 1–{len(qr_codes)+1}.")
            pause()

if __name__ == "__main__":
    main()