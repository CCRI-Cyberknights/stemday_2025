#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import random
import re

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(prompt="Press ENTER to continue..."):
    input(prompt)

def extract_flag_candidates(text):
    """Extract and display a few plausible flag-like values from metadata."""
    pattern = r"\b[A-Z]{4}-[A-Z0-9]{4}-[0-9]{4}\b"
    matches = re.findall(pattern, text)

    # Add 2–4 random-looking fake flags if needed
    while len(matches) < 5:
        fake = f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))}-" \
               f"{''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=4))}-" \
               f"{random.randint(1000, 9999)}"
        if fake not in matches:
            matches.append(fake)

    random.shuffle(matches)
    return matches

def main():
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

    if not os.path.isfile(target_image):
        print(f"❌ ERROR: {os.path.basename(target_image)} not found in this folder!")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    print(f"📂 Inspecting: {os.path.basename(target_image)}")
    print(f"📄 Saving metadata to: {os.path.basename(output_file)}\n")
    pause("Press ENTER to run exiftool and extract metadata...")

    print(f"\n🛠️ Running: exiftool {os.path.basename(target_image)} > {os.path.basename(output_file)}\n")
    time.sleep(0.5)
    try:
        with open(output_file, "w") as out_f:
            subprocess.run(
                ["exiftool", target_image],
                stdout=out_f,
                stderr=subprocess.DEVNULL,
                check=True
            )
    except subprocess.CalledProcessError:
        print("❌ ERROR: exiftool failed to run.")
        sys.exit(1)

    print(f"✅ All metadata saved to: {os.path.basename(output_file)}\n")

    # Read metadata
    with open(output_file, "r") as f:
        metadata_text = f.read()

    print("👀 Let’s preview a few key fields:")
    print("----------------------------------------")
    preview_lines = []
    for line in metadata_text.splitlines():
        if any(keyword in line for keyword in ["Camera", "Date", "Comment", "Artist", "Profile", "CCRI"]):
            preview_lines.append(line)
    preview_lines = preview_lines[:10]  # Just first 10 key lines
    print("\n".join(preview_lines))
    print("----------------------------------------\n")

    keyword = input("🔎 Enter a keyword to search in the metadata (or press ENTER to skip): ").strip()
    if keyword:
        print(f"\n🔎 Searching for '{keyword}' in {os.path.basename(output_file)}...")
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
