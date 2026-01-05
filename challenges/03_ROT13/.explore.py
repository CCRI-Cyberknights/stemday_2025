#!/usr/bin/env python3
import os
import sys
import time

# === Import Core ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from exploration_core import Colors, header, pause, require_input, clear_screen, resize_terminal, print_success, print_error, print_info

# === Config ===
INPUT_FILE = "cipher.txt"
OUTPUT_FILE = "decoded_output.txt"

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# === Rotation Logic (Python Implementation for Animation) ===
def rotate_text(text: str, shift: int) -> str:
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            result.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(c)
    return "".join(result)

# === UI Renderer ===
def render_frame(lines, footer_lines=[]):
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}🔐 ROT13 Decryption Module{Colors.END}")
    print("=======================")
    
    # Print the text content (simulating a screen buffer)
    for line in lines:
        print(f"> {Colors.YELLOW}{line}{Colors.END}")
    
    print("-----------------------")
    
    for f_line in footer_lines:
        print(f_line)

# === Animation Logic ===
def animate_decryption_wipe(lines, final_output_path):
    # ROT13 is shift 13. We animate shifting 1 step at a time until 13.
    total_frames = 13
    
    # Animation Loop
    for i in range(1, total_frames + 1):
        shift = i  # Shift forward by i steps
        
        # We apply the shift to the *original* ROT13 text to move it towards plain text
        # (Since ROT13 is symmetrical, +13 is the same as -13)
        current_frame_lines = [rotate_text(line, shift) for line in lines]
        
        status_footer = [
            f"🔓 Realigning Alphabet... (Shift {i}/{total_frames})",
            "   Translating characters..."
        ]
        
        render_frame(current_frame_lines, status_footer)
        time.sleep(0.2) # Speed of animation

    # Final Result Screen (Stable)
    final_lines = [rotate_text(line, 13) for line in lines]
    
    success_footer = [
        f"{Colors.GREEN}✅ Decryption Complete.{Colors.END}",
        f"💾 Saved to: {Colors.BOLD}{os.path.basename(final_output_path)}{Colors.END}",
        "",
        f"{Colors.CYAN}🧠 Hint: The flag format is CCRI-AAAA-1111{Colors.END}",
        "📋 Copy the flag above and paste it into the scoreboard."
    ]
    
    render_frame(final_lines, success_footer)
    return final_lines

# === Main Flow ===
def main():
    # 1. Setup
    resize_terminal(35, 90)
    
    # 2. Mission Briefing
    header("🔐 ROT13 Decoder Helper")
    
    print(f"📄 File to analyze: {Colors.BOLD}{INPUT_FILE}{Colors.END}")
    print("🎯 Goal: Restore the intercepted message to its original state.\n")
    
    # Narrative Alignment: Reference the README Intel
    print(f"{Colors.CYAN}🧠 Intelligence Report (from README):{Colors.END}")
    print("   ➤ The message is obfuscated using **ROT13** (Rotate 13).")
    print("   ➤ This is a substitution cipher that shifts every letter 13 places.")
    print("   ➤ It is symmetrical: applying the shift again restores the text.\n")
    
    input_path = get_path(INPUT_FILE)
    output_path = get_path(OUTPUT_FILE)

    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        print_error(f"{INPUT_FILE} is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    require_input("Type 'ready' to inspect the cipher: ", "ready")

    # 3. Tool Explanation
    header("🛠️ Behind the Scenes")
    print("While this script will visualize the process for you, in a real terminal")
    print("you would use the `tr` (translate) command to swap the letters.\n")
    print("The command looks like this:\n")
    print(f"   {Colors.GREEN}cat {INPUT_FILE} | tr 'A-Za-z' 'N-ZA-Mn-za-m'{Colors.END}\n")
    print("🔍 Command breakdown:")
    print(f"   {Colors.BOLD}tr{Colors.END}             → The 'translate' tool")
    print(f"   {Colors.BOLD}'A-Za-z'{Colors.END}       → Input alphabet (A-Z, a-z)")
    print(f"   {Colors.BOLD}'N-ZA-Mn-za-m'{Colors.END} → Output alphabet (shifted by 13 places)\n")
    
    require_input("Type 'run' to start the decryption visualizer: ", "run")

    # Load content
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Show initial state
    render_frame(lines, [
        f"🔒 Status: {Colors.RED}Encrypted (ROT13){Colors.END}", 
        "\nPreparing to shift characters..."
    ])
    
    time.sleep(1.5)

    # Run Animation
    decoded_lines = animate_decryption_wipe(lines, output_path)
    
    # Save output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(decoded_lines) + "\n")

    print()
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()