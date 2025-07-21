#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

# === 🌟 CCRI CyberKnights Full Environment Setup ===

def run(cmd, check=True):
    """Run a system command and print output."""
    print(f"💻 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)

def apt_install(packages):
    """Install system packages via apt."""
    print("📦 Installing system dependencies...")
    run("sudo apt update")
    run(f"sudo apt install -y {' '.join(packages)}")

def pip_install(packages):
    """Install Python packages via pip."""
    print("🐍 Installing Python packages...")
    run("python3 -m pip install --upgrade pip")
    run(f"python3 -m pip install {' '.join(packages)}")

def configure_git():
    """Prompt user to configure Git if not already configured."""
    print("\n🔧 Checking Git configuration...")
    try:
        username = subprocess.check_output(
            ["git", "config", "user.name"], text=True).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True).strip()
        print(f"✅ Git is already configured:\n   Name : {username}\n   Email: {email}")
    except subprocess.CalledProcessError:
        print("⚠️  Git is not configured. Let's set it up:")
        git_name = input("Enter your Git name: ").strip()
        git_email = input("Enter your Git email: ").strip()
        run(f'git config --global user.name "{git_name}"')
        run(f'git config --global user.email "{git_email}"')
        run('git config --global credential.helper store')
        print("✅ Git configuration saved.")

def main():
    print("\n🚀 Setting up your CCRI_CTF contributor environment...")
    print("=" * 60 + "\n")

    # === Install system dependencies ===
    apt_packages = [
        # Essential tools
        "git", "python3", "python3-pip", "python3-venv", "gcc", "build-essential",
        # Python libraries (system side)
        "python3-markdown", "python3-scapy",
        # Challenge tools
        "exiftool", "zbar-tools", "steghide", "hashcat", "unzip",
        "nmap", "tshark", "qrencode", "xdg-utils", "lsof", "vim-common", "util-linux"
    ]
    apt_install(apt_packages)

    # === Install Python libraries ===
    pip_packages = [
        "flask", "markupsafe"
    ]
    pip_install(pip_packages)

    # === Configure Git ===
    configure_git()

    print("\n🎉 Setup complete! You are now ready to contribute to the CCRI CTF project.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script may require sudo for installing system packages.")
    main()
