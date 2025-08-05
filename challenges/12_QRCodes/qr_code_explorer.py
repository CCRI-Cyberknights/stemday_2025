#!/usr/bin/env python3
import os
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def open_image(file_path, duration=20):
    try:
        viewer = subprocess.Popen(["xdg-open", file_path],
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        time.sleep(duration)
        viewer.terminate()
        print("⏳ Time’s up! Closing the viewer...")
    except Exception as e:
        print(f"❌ Could not open image: {e}")

def decode_qr(file_path):
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

def main():
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
    print("📖 Behind the scenes: This script runs:")
    print("    zbarimg qr_XX.png\n")
    print("⏳ Each QR will open for 20 seconds, then decode + save the result.\n")
    pause("Press ENTER to begin exploring.")
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

        try:
            index = int(choice) - 1
            if 0 <= index < len(qr_codes):
                file_path = qr_codes[index]
                txt_file = file_path.replace(".png", ".txt")

                print(f"\n🖼️ Opening {os.path.basename(file_path)}...")
                open_image(file_path)

                print(f"\n🔎 Scanning {os.path.basename(file_path)}...")
                print(f"💻 Running: zbarimg \"{os.path.basename(file_path)}\"\n")

                result = decode_qr(file_path)

                if not result:
                    print("❌ No QR code found.")
                else:
                    print("✅ Decoded:")
                    print("----------------------------")
                    print(result)
                    print("----------------------------")
                    with open(txt_file, "w") as f:
                        f.write(result + "\n")
                    print(f"💾 Saved to: {os.path.basename(txt_file)}")

                pause("\nPress ENTER to continue...")
                clear_screen()
            else:
                print("❌ Invalid selection.")
                pause()
                clear_screen()
        except ValueError:
            print("❌ Invalid input. Enter a number.")
            pause()
            clear_screen()

if __name__ == "__main__":
    main()
