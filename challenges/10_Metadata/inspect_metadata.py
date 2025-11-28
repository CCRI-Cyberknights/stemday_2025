#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import random
import re

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
    Prevents students from just mashing ENTER through explanations.
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
        sys.stdout.write(f"\r{message}... {frame}")
        sys.stdout.flush()
        time.sleep(interval)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

# === Flag Candidate Helper ===
def extract_flag_candidates(text):
    """Extract and display a few plausible flag-like values from metadata."""
    pattern = r"\b[A-Z]{4}-[A-Z0-9]{4}-[0-9]{4}\b"
    matches = re.findall(pattern, text)

    # Add 2–4 random-looking fake flags if needed
    while len(matches) < 5:
        fake = (
            f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))}-"
            f"{''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=4))}-"
            f"{random.randint(1000, 9999)}"
        )
        if fake not in matches:
            matches.append(fake)

    random.shuffle(matches)
    return matches

# === Main Flow ===
def main():
    resize_terminal(35, 90)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = os.path.join(script_dir, "capybara.jpg")
    output_file = os.path.join(script_dir, "metadata_dump.txt")

    clear_screen()
    print("📸 Metadata Inspection Tool")
    print("============================\n")
    print(f"🎯 Target image: {os.path.basename(target_image)}")
    print("🔧 Tool in use: exiftool\n")
    print("💡 Why exiftool?")
    print("   ➡️ Images often carry *hidden metadata* like camera info, GPS tags, or embedded comments.")
    print("   ➡️ This data can hide secrets — including CTF flags!\n")
    pause_nonempty("Type 'ready' when you're ready to inspect the image metadata: ")

    if not os.path.isfile(target_image):
        print(f"❌ ERROR: {os.path.basename(target_image)} not found in this folder!")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    clear_screen()
    print("🛠️ Behind the Scenes")
    print("----------------------------")
    print("To inspect metadata, we'll use exiftool like this:\n")
    print(f"   exiftool {os.path.basename(target_image)} > {os.path.basename(output_file)}\n")
    print("🔍 Command breakdown:")
    print("   exiftool capybara.jpg        → Print all metadata fields for this image")
    print(f"   > {os.path.basename(output_file):<22}→ Redirect the output into a text file to review later\n")
    print("Once we have metadata_dump.txt, we can:")
    print("   ➤ Skim important fields (comments, artist, date, etc.)")
    print("   ➤ Search for keywords with grep (like 'CCRI' or 'Cryptkeepers')\n")
    pause_nonempty("Type 'run' when you're ready to extract metadata with exiftool: ")

    print(f"\n📂 Inspecting: {os.path.basename(target_image)}")
    print(f"📄 Saving metadata to: {os.path.basename(output_file)}\n")
    print(f"🛠️ Running: exiftool {os.path.basename(target_image)} > {os.path.basename(output_file)}\n")
    spinner("Extracting metadata")

    try:
        with open(output_file, "w", encoding="utf-8", errors="replace") as out_f:
            subprocess.run(
                ["exiftool", target_image],
                stdout=out_f,
                stderr=subprocess.DEVNULL,
                check=True
            )
    except subprocess.CalledProcessError:
        print("❌ ERROR: exiftool failed to run.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print(f"✅ All metadata saved to: {os.path.basename(output_file)}\n")

    # Read metadata
    with open(output_file, "r", encoding="utf-8", errors="replace") as f:
        metadata_text = f.read()

    print("👀 Let’s preview a few key fields:")
    print("----------------------------------------")
    preview_lines = []
    for line in metadata_text.splitlines():
        if any(keyword in line for keyword in ["Camera", "Date", "Comment", "Artist", "Profile", "CCRI"]):
            preview_lines.append(line)
    preview_lines = preview_lines[:10]  # Just first 10 key lines
    if preview_lines:
        print("\n".join(preview_lines))
    else:
        print("(No obvious Camera/Date/Comment/Artist/CCRI fields in the first pass.)")
    print("----------------------------------------\n")

    print("🧰 Next, you can search the metadata for any keyword you're curious about.")
    print("   Example commands in a normal terminal might be:")
    print(f"      grep -i 'CCRI' {os.path.basename(output_file)}")
    print(f"      grep -i 'Cryptkeepers' {os.path.basename(output_file)}\n")

    keyword = input("🔎 Enter a keyword to search in the metadata (or press ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {os.path.basename(output_file)}...\n")
        print("   Command being used under the hood:")
        print(f"      grep -i --color=always {keyword} {os.path.basename(output_file)}\n")
        subprocess.run(
            ["grep", "-i", "--color=always", keyword, output_file],
            check=False
        )
    else:
        print("⏭️  Skipping custom search.\n")

    # Blind flag hunt
    flag_candidates = extract_flag_candidates(metadata_text)

    print("🧠 One of these fields hides the correct flag in the format: CCRI-AAAA-1111")
    print("👁️‍🗨️ Candidate flag-like values found in metadata:")
    for fake in flag_candidates:
        print(f"   ➡️ {fake}")

    pause("\nPress ENTER to close this terminal...")

if __name__ == "__main__":
    main()
