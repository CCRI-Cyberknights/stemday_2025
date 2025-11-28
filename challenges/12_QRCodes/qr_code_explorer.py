#!/usr/bin/env python3
import os
import subprocess
import time
import sys
import shutil

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def pause_nonempty(prompt="Type anything, then press ENTER to continue: "):
    """
    Pause, but DO NOT allow empty input.
    Prevents students from just mashing ENTER through the briefing.
    """
    while True:
        answer = input(prompt)
        if answer.strip():
            return answer
        print("↪  Don't just hit ENTER — type something so we know you're following along!\n")

def spinner(message="Working", duration=1.8, interval=0.12):
    """
    Simple text spinner to give the feeling of work being done.
    """
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        print(f"\r{message}... {frame}", end="", flush=True)
        time.sleep(interval)
        i += 1
    print("\r" + " " * (len(message) + 10) + "\r", end="", flush=True)

# === QR Helpers ===
def open_image(file_path, duration=10):
    """Open an image using a specific viewer to ensure we can close it."""
    # List of viewers to try (Parrot OS usually uses eom or eog)
    viewers = ["eom", "eog", "feh", "display", "ristretto"]
    
    viewer_cmd = "xdg-open" # Fallback
    
    # Find the first available viewer from our list
    for v in viewers:
        if shutil.which(v):
            viewer_cmd = v
            break

    try:
        # Popen keeps a handle on the specific process (e.g., eom)
        viewer = subprocess.Popen(
            [viewer_cmd, file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Show a countdown timer while waiting
        for i in range(duration, 0, -1):
            print(f"\r⏳ Closing in {i} seconds... ", end="", flush=True)
            time.sleep(1)
            # If the student closes it early, stop counting
            if viewer.poll() is not None:
                print("\r✅ Image closed.             ", end="", flush=True)
                break
        else:
            print("\r⏳ Time’s up! Closing viewer.", end="", flush=True)

        # Force close if it's still running
        if viewer.poll() is None:
            viewer.terminate()
            
        print() # New Line

    except Exception as e:
        print(f"\n❌ Could not open image: {e}")

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
        print("❌ ERROR: zbarimg is not installed.")
        return ""

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    qr_codes = [os.path.join(script_dir, f"qr_0{i}.png") for i in range(1, 6)]

    clear_screen()
    print("📦 QR Code Explorer")
    print("==========================\n")
    print("🎯 Mission Briefing:")
    print("----------------------------")
    print("🔍 You’ve recovered 5 mysterious QR codes from a digital drop site.")
    print("Each one may contain:")
    print("  • A secret message")
    print("  • A fake flag")
    print("  • Or… the **real flag** in CCRI-AAAA-1111 format!\n")
    print("🛠️ Your options:")
    print("  • Scan with your phone’s QR scanner")
    print("  • OR use this tool to open and auto-decode them\n")
    print("📖 Behind the scenes, this script will use a command like:")
    print("     zbarimg qr_01.png")
    print("   to read the QR code and print its contents.\n")
    print("⏳ Each QR opens for 10 seconds so you can inspect it,")
    print("   then the script decodes the QR and saves the result to a .txt file.\n")

    pause_nonempty("Type 'start' when you're ready to explore the QR codes: ")
    clear_screen()

    while True:
        print("🗂️  Available QR codes:")
        for i, qr in enumerate(qr_codes, 1):
            print(f"{i}. {os.path.basename(qr)}")
        print("6. Exit Explorer\n")

        choice = input("Select a QR code (1-5) or 6 to exit: ").strip()

        if choice == "6":
            print("👋 Exiting QR Explorer.")
            break

        if not choice.isdigit():
            print("❌ Invalid input. Please enter a number.")
            pause()
            clear_screen()
            continue

        index = int(choice) - 1
        if 0 <= index < len(qr_codes):
            file_path = qr_codes[index]
            txt_file = file_path.replace(".png", ".txt")

            print(f"\n🖼️ Opening {os.path.basename(file_path)}...")
            open_image(file_path)

            print(f"\n🔎 Scanning {os.path.basename(file_path)}...")
            print(f"💻 Running: zbarimg \"{os.path.basename(file_path)}\"\n")

            spinner("Decoding QR")
            result = decode_qr(file_path)

            if not result:
                print("❌ No QR code found or could not decode.")
            else:
                print("✅ Decoded Result:")
                print("----------------------------")
                print(result)
                print("----------------------------")
                try:
                    with open(txt_file, "w", encoding="utf-8") as f:
                        f.write(result + "\n")
                    print(f"💾 Saved to: {os.path.basename(txt_file)}")
                except Exception as e:
                    print(f"⚠️ Could not save output: {e}")

            pause("\nPress ENTER to continue...")
            clear_screen()
        else:
            print("❌ Invalid selection. Please choose 1–5.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
