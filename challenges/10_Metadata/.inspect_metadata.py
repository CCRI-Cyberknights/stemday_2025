#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import random
import re

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
IMAGE_FILE = "capybara.jpg"
OUTPUT_FILE = "metadata_dump.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def extract_flag_candidates(text):
    """Extract and display a few plausible flag-like values from metadata."""
    pattern = r"\b[A-Z]{4}-[A-Z0-9]{4}-[0-9]{4}\b"
    matches = re.findall(pattern, text)

    # Add random fakes if needed
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

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    # 2. Mission Briefing
    header("📸 Metadata Inspection Tool")
    
    print(f"🎯 Target image: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}exiftool{Colors.END}\n")
    print(f"{Colors.CYAN}💡 Why exiftool?{Colors.END}")
    print("   ➡️ Images often carry *hidden metadata* like camera info, GPS tags, or embedded comments.")
    print("   ➡️ This data can hide secrets — including CTF flags!\n")
    
    require_input("Type 'ready' when you're ready to inspect the image metadata: ", "ready")

    if not os.path.isfile(target_image):
        print_error(f"{IMAGE_FILE} not found in this folder!")
        sys.exit(1)

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("To inspect metadata, we'll use exiftool like this:\n")
    print(f"   {Colors.GREEN}exiftool {IMAGE_FILE} > {OUTPUT_FILE}{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}exiftool {IMAGE_FILE}{Colors.END}        → Print all metadata fields for this image")
    print(f"   {Colors.BOLD}> {OUTPUT_FILE:<22}{Colors.END}→ Redirect the output into a text file to review later\n")
    print("Once we have metadata_dump.txt, we can:")
    print("   ➤ Skim important fields (comments, artist, date, etc.)")
    print("   ➤ Search for keywords with grep (like 'CCRI' or 'Cryptkeepers')\n")
    
    require_input("Type 'run' when you're ready to extract metadata with exiftool: ", "run")

    print(f"\n📂 Inspecting: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"📄 Saving metadata to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}\n")
    print(f"🛠️ Running: exiftool {IMAGE_FILE} > {OUTPUT_FILE}")
    spinner("Extracting metadata")

    try:
        with open(output_path, "w", encoding="utf-8", errors="replace") as out_f:
            subprocess.run(
                ["exiftool", target_image],
                stdout=out_f,
                stderr=subprocess.DEVNULL,
                check=True
            )
    except subprocess.CalledProcessError:
        print_error("exiftool failed to run.")
        sys.exit(1)

    print_success(f"All metadata saved to: {OUTPUT_FILE}\n")

    # 4. Preview
    with open(output_path, "r", encoding="utf-8", errors="replace") as f:
        metadata_text = f.read()

    print("👀 Let’s preview a few key fields:")
    print("-" * 50)
    preview_lines = []
    for line in metadata_text.splitlines():
        if any(keyword in line for keyword in ["Camera", "Date", "Comment", "Artist", "Profile", "CCRI"]):
            preview_lines.append(line)
    preview_lines = preview_lines[:10]  # First 10 interesting lines
    
    if preview_lines:
        for line in preview_lines:
            print(f"{Colors.YELLOW}{line}{Colors.END}")
    else:
        print("(No obvious Camera/Date/Comment/Artist/CCRI fields in the first pass.)")
    print("-" * 50 + "\n")

    # 5. Interactive Search
    print("🧰 Next, you can search the metadata for any keyword you're curious about.")
    print("   Example commands in a normal terminal might be:")
    print(f"      {Colors.GREEN}grep -i 'CCRI' {OUTPUT_FILE}{Colors.END}")
    print(f"      {Colors.GREEN}grep -i 'Cryptkeepers' {OUTPUT_FILE}{Colors.END}\n")

    keyword = input(f"{Colors.YELLOW}🔎 Enter a keyword to search in the metadata (or press ENTER to skip): {Colors.END}").strip().lower()
    
    if keyword:
        print(f"\n🔎 Searching for '{Colors.BOLD}{keyword}{Colors.END}' in {OUTPUT_FILE}...\n")
        print("   Command being used under the hood:")
        print(f"      {Colors.GREEN}grep -i --color=always {keyword} {OUTPUT_FILE}{Colors.END}\n")
        subprocess.run(
            ["grep", "-i", "--color=always", keyword, output_path],
            check=False
        )
        print("\n") # Spacing after search results
    else:
        print_info("Skipping custom search.\n")

    # === NEW STEP: Pause before revealing flags ===
    require_input("Type 'scan' to check specifically for flag-like patterns: ", "scan")

    # 6. Flag Candidates
    flag_candidates = extract_flag_candidates(metadata_text)
    
    print(f"\n{Colors.CYAN}🧠 One of these fields hides the correct flag in the format: CCRI-AAAA-1111{Colors.END}")
    print("👁️‍🗨️ Candidate flag-like values found in metadata:")
    for fake in flag_candidates:
        print(f"   ➡️ {Colors.BOLD}{fake}{Colors.END}")

    pause("\nPress ENTER to close this terminal...")

if __name__ == "__main__":
    main()