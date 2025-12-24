#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

# === Terminal Utilities ===
def resize_terminal(rows=35, cols=90):
    """
    Forces the terminal window to resize to the specified dimensions.
    \x1b[8;{rows};{cols}t is the standard sequence for xterm/mate-terminal.
    """
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2) # Give the window manager a split second to react

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def pause(msg="Press ENTER to continue..."):
    input(msg)

def require_input(prompt, expected):
    """
    Pauses and requires the user to type a specific word (case-insensitive) to continue.
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer == expected.lower():
            return
        print(f"↪  Please type '{expected}' to continue!\n")

def spinner(message="Working", duration=2.0, interval=0.15):
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

# === Rotation Logic ===
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
    print("🔐 ROT13 Decoder Helper")
    print("=======================")
    
    for line in lines:
        print(f"> {line}")
    
    print("-----------------------")
    
    for f_line in footer_lines:
        print(f_line)

# === Animation Logic ===
def animate_decryption_wipe(lines, final_output_path):
    total_frames = 13
    
    # Animation Loop
    for i in range(1, total_frames + 1):
        shift = -i  
        
        current_frame_lines = [rotate_text(line, shift) for line in lines]
        
        status_footer = [
            f"🔓 Decrypting... (Pass {i}/{total_frames})",
            "   Watching for readable text..."
        ]
        
        render_frame(current_frame_lines, status_footer)
        time.sleep(0.3)

    # Final Result Screen (Stable)
    final_lines = [rotate_text(line, -13) for line in lines]
    
    success_footer = [
        "✅ Decryption Complete.",
        f"💾 Saved to: {os.path.basename(final_output_path)}",
        "",
        "🧠 Hint: The flag format is CCRI-AAAA-1111",
        "📋 Copy the flag above and paste it into the scoreboard."
    ]
    
    render_frame(final_lines, success_footer)
    return final_lines

# === Main Flow ===
def main():
    # 1. RESIZE TERMINAL FIRST
    # We ask for 35 rows (vertical) and 90 cols (horizontal)
    resize_terminal(35, 90)

    clear_screen()
    print("🔐 ROT13 Decoder Helper")
    print("===========================\n")
    print("📄 File to analyze: cipher.txt")
    print("🎯 Goal: Decode this message and find the hidden CCRI flag.\n")
    print("💡 What is ROT13?")
    print("   ➤ A Caesar cipher that shifts each letter 13 positions.")
    print("   ➤ Encoding and decoding are the same (apply ROT13 twice = original text).\n")
    
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / "cipher.txt"
    output_path = script_dir / "decoded_output.txt"

    if not input_path.is_file() or input_path.stat().st_size == 0:
        print("\n❌ ERROR: cipher.txt is missing or empty.")
        pause("Press ENTER to close this terminal...")
        sys.exit(1)

    require_input("Type 'ready' to load the file: ", "ready")

    # Load content
    lines = input_path.read_text(encoding="utf-8").splitlines()

    # Show initial state
    render_frame(lines, ["🔒 Status: Encrypted (ROT13)", "\nType 'crack' to brute-force the rotation."])
    
    require_input("Command > ", "crack")

    decoded_lines = animate_decryption_wipe(lines, output_path)
    
    output_path.write_text("\n".join(decoded_lines) + "\n", encoding="utf-8")

    print()
    pause("Press ENTER to close this terminal...")

if __name__ == "__main__":
    main()