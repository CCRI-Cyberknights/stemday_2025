#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

# === 🌟 CCRI CyberKnights Full Environment Setup ===

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"

def run(cmd, check=True):
    """Run a command (str or list) and print it."""
    if isinstance(cmd, str):
        print(f"💻 Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
    else:
        print(f"💻 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
    if check and result.returncode != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)

def apt_install(packages):
    """Install system packages via apt."""
    print("📦 Installing system dependencies...")
    run("sudo apt update")
    run(f"sudo apt install -y {' '.join(packages)}")

def pip_install():
    """Install Python CLI tools via pipx and Python libs via pip."""
    print("🐍 Installing Python CLI tools via pipx...")
    run(["sudo", "apt", "install", "-y", "pipx"])
    run(["pipx", "ensurepath"])
    run(["pipx", "install", "flask"])

    print("📚 Installing Flask and MarkupSafe via pip (for Python imports)...")
    run(["python3", "-m", "pip", "install", "--break-system-packages", "flask", "markupsafe"])

def install_zsteg():
    """Install zsteg via Ruby gem."""
    print("💎 Installing Ruby and zsteg...")
    run(["sudo", "apt", "install", "-y", "ruby", "ruby-dev", "libmagic-dev"])
    run(["sudo", "gem", "install", "zsteg"])

def install_steghide_deb():
    """Download and install patched Steghide 0.6.0 from custom .deb."""
    print("🕵️ Checking Steghide version...")
    try:
        version_output = subprocess.check_output(["steghide", "--version"], text=True).strip()
        if "0.6.0" in version_output:
            print("✅ Steghide 0.6.0 already installed.")
            return
    except Exception:
        print("ℹ️ Steghide not found or outdated. Installing patched version...")

    print("⬇️ Downloading Steghide 0.6.0 .deb package...")
    run(["wget", "-q", STEGO_DEB_URL, "-O", "/tmp/steghide.deb"])

    print("📦 Installing patched Steghide...")
    run("sudo dpkg -i /tmp/steghide.deb || sudo apt --fix-broken install -y")
    run("rm /tmp/steghide.deb")

    print("📌 Pinning Steghide 0.6.0 to prevent downgrade...")
    pin_file = "/etc/apt/preferences.d/steghide"
    pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
    with open("/tmp/steghide-pin", "w") as f:
        f.write(pin_contents)
    run(["sudo", "mv", "/tmp/steghide-pin", pin_file])

def get_git_config(key):
    res = subprocess.run(["git", "config", "--global", key],
                         capture_output=True, text=True)
    if res.returncode == 0:
        val = res.stdout.strip()
        return val if val else None
    return None

def configure_git(git_name=None, git_email=None):
    """Configure Git non-interactively when stdin is not a TTY."""
    print("\n🔧 Checking Git configuration...")

    current_name = get_git_config("user.name")
    current_email = get_git_config("user.email")

    if current_name and current_email:
        print(f"✅ Git is already configured:\n   Name : {current_name}\n   Email: {current_email}")
        return

    # Prefer provided args/env if present
    if not git_name:
        git_name = os.environ.get("GIT_NAME")
    if not git_email:
        git_email = os.environ.get("GIT_EMAIL")

    if git_name and git_email:
        print("📝 Setting Git config from flags/env...")
        run(["git", "config", "--global", "user.name", git_name])
        run(["git", "config", "--global", "user.email", git_email])
        run(["git", "config", "--global", "credential.helper", "store"])
        print(f"✅ Git configuration saved:\n   Name : {git_name}\n   Email: {git_email}")
        return

    # If interactive, prompt; if not, skip safely
    if sys.stdin.isatty():
        try:
            git_name = input("Enter your Git name: ").strip()
            git_email = input("Enter your Git email: ").strip()
        except EOFError:
            git_name = git_email = None
    else:
        git_name = git_email = None  # ensure non-interactive path

    if git_name and git_email:
        run(["git", "config", "--global", "user.name", git_name])
        run(["git", "config", "--global", "user.email", git_email])
        run(["git", "config", "--global", "credential.helper", "store"])
        print("✅ Git configuration saved.")
    else:
        print("⚠️  Skipping Git prompts (non-interactive).")
        print("    Set these and rerun if needed:")
        print("    - Flags: --git-name 'Your Name' --git-email 'you@example.com'")
        print("    - Or env: GIT_NAME='Your Name' GIT_EMAIL='you@example.com'")

def parse_args():
    p = argparse.ArgumentParser(description="CCRI CyberKnights environment setup")
    p.add_argument("--git-name", help="Git user.name (non-interactive)")
    p.add_argument("--git-email", help="Git user.email (non-interactive)")
    return p.parse_args()

def main():
    args = parse_args()

    print("\n🚀 Setting up your CCRI_CTF contributor environment...")
    print("=" * 60 + "\n")

    apt_packages = [
        # Essential tools
        "git", "python3", "python3-pip", "python3-venv", "gcc", "build-essential", "fonts-noto-color-emoji",
        # Python libraries (system side)
        "python3-markdown", "python3-scapy",
        # Challenge tools
        "exiftool", "zbar-tools", "hashcat", "unzip", "libmcrypt4",
        "nmap", "tshark", "qrencode", "xdg-utils", "lsof", "vim-common", "util-linux",
        "binwalk", "fcrackzip", "john", "radare2", "imagemagick", "hexedit", "feh"
    ]

    apt_install(apt_packages)
    install_steghide_deb()
    pip_install()
    install_zsteg()
    configure_git(args.git_name, args.git_email)

    print("\n🎉 Setup complete! You are now ready to contribute to the CCRI CTF project.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script may require sudo for installing system packages.")
    main()
