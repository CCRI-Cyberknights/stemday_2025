#!/usr/bin/env python3
import os
import subprocess
import sys

def run_steghide(password, image_path, output_path):
    try:
        result = subprocess.run(
            ["steghide", "extract", "-sf", image_path, "-xf", output_path, "-p", password, "-f"],
            input=b"\n",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except FileNotFoundError:
        print("❌ ERROR: steghide is not installed.")
        return False

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

def main():
    clear_screen()
    print("🕵️ Stego Decode Helper")
    print("==========================\n")
    print("🎯 Target image: squirrel.jpg")
    print("🔍 Tool: steghide\n")
    print("💡 steghide can hide or extract secret data from files like images.\n")
    pause()

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("---------------------------")
    print("When you try a password, we'll run this command:\n")
    print("   steghide extract -sf squirrel.jpg -xf decoded_message.txt -p [your password]\n")
    pause()

    image_path = os.path.abspath("squirrel.jpg")
    output_path = os.path.abspath("decoded_message.txt")

    while True:
        pw = input("🔑 Enter a password to try (or type 'exit' to quit): ").strip()
        if not pw:
            print("⚠️ You must enter something.\n")
            continue
        if pw.lower() == "exit":
            print("👋 Exiting... Good luck!")
            pause("Press ENTER to close this window...")
            break

        print(f"\n🔓 Trying password: {pw}")
        print("📦 Scanning squirrel.jpg for hidden data...\n")

        if run_steghide(pw, image_path, output_path):
            print("🎉 ✅ SUCCESS! Hidden message recovered:\n")
            print("--------------- OUTPUT ---------------")
            with open(output_path, "r") as f:
                print(f.read())
            print("--------------------------------------\n")
            print("📁 Saved as decoded_message.txt in this folder.")
            print("💡 Look for a string like CCRI-ABCD-1234 to use as your flag.")
            pause("Press ENTER to close this terminal...")
            break
        else:
            print("❌ Extraction failed. No hidden data or incorrect password.")
            if os.path.exists(output_path):
                os.remove(output_path)
            print("🔁 Try again.\n")

if __name__ == "__main__":
    main()
