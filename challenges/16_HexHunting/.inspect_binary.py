#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
from pathlib import Path

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, spinner, print_success, print_error, print_info, resize_terminal, clear_screen

# === Config ===
BINARY_NAME = "hex_flag.bin"
NOTES_NAME = "notes.txt"

# === Core Helpers ===
def extract_flag_candidates(binary_path):
    try:
        with open(binary_path, "rb") as f:
            data = f.read()

        # Match CCRI-AAAA-1111, XXXX-YYYY-1111, XXXX-1111-YYYY
        flag_pattern = re.compile(
            rb"(CCRI-[A-Z]{4}-\d{4})|([A-Z]{4}-[A-Z]{4}-\d{4})|([A-Z]{4}-\d{4}-[A-Z]{4})"
        )

        matches = []
        for match in flag_pattern.finditer(data):
            flag_bytes = match.group(0)
            try:
                flag_str = flag_bytes.decode("ascii")
                matches.append((match.start(), flag_str))
            except UnicodeDecodeError:
                continue

        return matches

    except Exception as e:
        print_error(f"Binary scan failed: {e}")
        return []

def show_hex_context(binary_path, offset, context=64):
    start = max(0, offset - 16)
    try:
        # Use str(binary_path) to ensure subprocess handles it correctly
        dd = subprocess.Popen(
            ["dd", f"if={str(binary_path)}", "bs=1", f"skip={start}", f"count={context}"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        xxd = subprocess.Popen(["xxd"], stdin=dd.stdout)
        dd.stdout.close()
        xxd.wait()
    except Exception as e:
        print_error(f"Could not show hex context: {e}")

# === Main Flow ===
def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    # RESOLVE ABSOLUTE PATHS
    script_dir = Path(__file__).resolve().parent
    binary_path = script_dir / BINARY_NAME
    notes_path = script_dir / NOTES_NAME

    # 2. Mission Briefing
    header("🔍 Hex Flag Hunter")
    
    print(f"🎯 Target binary: {Colors.BOLD}{BINARY_NAME}{Colors.END}")
    print(f"💡 Goal: Locate the real flag (format: {Colors.GREEN}CCRI-AAAA-1111{Colors.END}).")
    print(f"{Colors.RED}⚠️  Multiple candidate flags are embedded, but only ONE is correct!{Colors.END}\n")
    
    print(f"{Colors.CYAN}🧠 What are we actually doing here?{Colors.END}")
    print("   ➤ A compiled/binary file can contain lots of embedded text and data.")
    print("   ➤ Some of those bytes look like flags, others are decoys.")
    print("   ➤ We'll scan the raw bytes for anything that *looks* like a flag,")
    print("      then inspect a hex dump around each candidate to judge context.\n")
    
    # 3. Safety Check
    if not binary_path.is_file():
        print_error(f"CRITICAL ERROR: Cannot find '{BINARY_NAME}'")
        print_info(f"Looking in: {script_dir}")
        pause("Press ENTER to exit...") 
        sys.exit(1)

    # Clean previous notes
    if notes_path.exists():
        os.remove(notes_path)

    require_input("Type 'scan' when you're ready to begin scanning the binary: ", "scan")
    
    print(f"\n{Colors.CYAN}🔎 Scanning binary for flag-like patterns...{Colors.END}")
    spinner("Scanning")
    
    flags = extract_flag_candidates(binary_path)

    if not flags:
        print_error("No flag-like patterns found in binary.")
        pause("Press ENTER to exit...")
        sys.exit(1)

    print(f"\n{Colors.GREEN}✅ Detected {len(flags)} flag-like pattern(s)!{Colors.END}")
    print("🧪 You'll now investigate each one by reviewing its raw hex context.")
    print("   Use what you know about the story + placement to decide what's real.")
    
    require_input("🔬 Type 'view' to begin reviewing candidates: ", "view")

    # 4. Review Loop
    for i, (offset, flag) in enumerate(flags):
        clear_screen()
        print("-" * 50)
        print(f"[{i+1}/{len(flags)}] 🏷️  Candidate Flag: {Colors.BOLD}{flag}{Colors.END}")
        print(f"📍 Approximate Byte Offset: {Colors.YELLOW}{offset}{Colors.END}")
        print("📖 Hex Dump Around Candidate:")
        print("-" * 50)
        
        # Colorize the hex output if possible, but standard xxd is fine
        print(Colors.CYAN)
        show_hex_context(binary_path, offset)
        print(Colors.END)
        print("-" * 50)

        while True:
            print("\nActions:")
            print(f"  [1] ✅ Mark as {Colors.GREEN}POSSIBLE{Colors.END} (save to {NOTES_NAME})")
            print("  [2] ➡️  Skip to next candidate")
            print("  [3] 🚪 Quit investigation")
            
            choice = input(f"{Colors.YELLOW}Choose an action (1-3): {Colors.END}").strip()
            
            if choice == "1":
                with open(notes_path, "a") as f:
                    f.write(flag + "\n")
                print_success(f"Saved '{flag}' to {NOTES_NAME}")
                time.sleep(0.6)
                break
            elif choice == "2":
                print_info("Skipping to next candidate...")
                time.sleep(0.4)
                break
            elif choice == "3":
                print(f"\n{Colors.CYAN}👋 Exiting early. Your saved flags are in {NOTES_NAME}.{Colors.END}")
                sys.exit(0)
            else:
                print_error("Invalid input. Please enter 1, 2, or 3.")

    # 5. Conclusion
    print("\n")
    print_success("Flag inspection complete!")
    print(f"📁 Review your notes: {Colors.BOLD}{NOTES_NAME}{Colors.END}")
    print(f"{Colors.CYAN}🧠 Remember: Only one of those candidates is the *true* CCRI flag.{Colors.END}")
    pause("🔚 Press ENTER to exit.")

if __name__ == "__main__":
    main()