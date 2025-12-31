#!/usr/bin/env python3
import sys
import os
import time

# === 🎨 STANDARD COLORS (Matches Coach Mode) ===
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# === 🛠️ TERMINAL UTILITIES ===
def resize_terminal(rows=35, cols=90):
    """Forces the terminal window to a standard size."""
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()
    time.sleep(0.2)

def clear_screen():
    """Wipes the screen clean."""
    os.system('clear' if os.name == 'posix' else 'cls')

def header(title_text):
    """Standard header format for all challenges."""
    resize_terminal()
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}{title_text}{Colors.END}")
    print("=" * 50 + "\n")

def pause(prompt=None):
    """Pauses execution until Enter is pressed."""
    if prompt is None:
        prompt = f"{Colors.YELLOW}🔸 Press ENTER to continue...{Colors.END}"
    input(prompt)

def require_input(prompt, expected):
    """Forces the user to type a specific word to proceed."""
    while True:
        answer = input(f"{Colors.YELLOW}{prompt}{Colors.END}").strip().lower()
        if answer == expected.lower():
            return
        print(f"{Colors.RED}↪  Please type '{expected}' to continue!{Colors.END}\n")

def spinner(message="Working", duration=2.0, interval=0.15):
    """Shows a little spinning animation."""
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{Colors.CYAN}{message}... {frame}{Colors.END}")
        sys.stdout.flush()
        time.sleep(interval)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}ℹ️  {msg}{Colors.END}")