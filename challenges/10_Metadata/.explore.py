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
    """Ensure the file is saved next to this script, regardless of where it's run from."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def extract_flag_candidates(text):
    """Extract and display a few plausible flag-like values from metadata."""
    pattern = r"CCRI-[A-Z0-9]{4}-[0-9]{4}"
    matches = re.findall(pattern, text)
    return list(set(matches)) # Unique matches

def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    script_dir = os.path.abspath(os.path.dirname(__file__))
    target_image = get_path(IMAGE_FILE)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.isfile(target_image):
        print_error(f"{IMAGE_FILE} not found in this folder!")
        sys.exit(1)

    # 2. Mission Briefing
    header("📷 Metadata Inspection Tool")
    
    print(f"🎯 Target image: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"🔧 Tool in use: {Colors.BOLD}exiftool{Colors.END}\n")
    print("🎯 Goal: Extract hidden metadata from the image to find the flag.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ **The Lock:** Information is hidden in file headers (EXIF tags).")
    print("   ➤ **The Strategy:** Metadata Extraction (reading data about data).")
    print("   ➤ **The Tool:** `exiftool` is the industry standard for this task.\n")
    
    require_input("Type 'ready' to inspect the image headers: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("To inspect metadata, we'll use exiftool like this:\n")
    print(f"   {Colors.GREEN}exiftool {IMAGE_FILE} > {OUTPUT_FILE}{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}exiftool {IMAGE_FILE}{Colors.END}        → Print all metadata fields for this image")
    print(f"   {Colors.BOLD}> {OUTPUT_FILE:<22}{Colors.END}→ Redirect the output into a text file to review later\n")
    print("Once we have metadata_dump.txt, we can:")
    print("   ➤ Skim fields (comments, artist, GPS, etc.)")
    print("   ➤ Search for keywords using `grep` (like 'CCRI')\n")
    
    require_input("Type 'run' when you're ready to extract metadata: ", "run")

    # 4. Execution
    print(f"\n📂 Inspecting: {Colors.BOLD}{IMAGE_FILE}{Colors.END}")
    print(f"📄 Saving output to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}\n")
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
    except FileNotFoundError:
        print_error("exiftool command not found. Is it installed?")
        sys.exit(1)

    print_success(f"Metadata extraction complete.\n")

    # 5. Preview & Filter
    print("👀 Let’s preview the first few lines of the dump:")
    print("-" * 50)
    with open(output_path, "r", encoding="utf-8", errors="replace") as f:
        metadata_text = f.read()
        lines = metadata_text.splitlines()
        for line in lines[:10]: # Show first 10
            print(f"{Colors.YELLOW}{line}{Colors.END}")
    print("-" * 50 + "\n")

    require_input("Type 'filter' to search for the flag: ", "filter")
    
    # 6. Filtering (grep simulation)
    print(f"\n🔎 Searching for '{Colors.BOLD}CCRI{Colors.END}' in {OUTPUT_FILE}...\n")
    print("   Command being used under the hood:")
    print(f"      {Colors.GREEN}grep \"CCRI\" {OUTPUT_FILE}{Colors.END}\n")
    
    time.sleep(1)
    
    flag_candidates = extract_flag_candidates(metadata_text)
    
    if flag_candidates:
        print_success("Match found!")
        print("-" * 50)
        for flag in flag_candidates:
            print(f"   ➡️ {Colors.BOLD}{flag}{Colors.END}")
        print("-" * 50 + "\n")
        
        print(f"📁 Evidence saved to: {Colors.BOLD}{OUTPUT_FILE}{Colors.END}")
        print(f"{Colors.CYAN}🧠 This metadata field was hidden inside the file header.{Colors.END}\n")
    else:
        print_error("No flag format found in metadata.")
        print_info("Try inspecting the file manually or looking for other keywords.")

    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()