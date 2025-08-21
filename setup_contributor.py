#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shlex

# === 🌟 CCRI CyberKnights Full Environment Setup (Non-Interactive / Parrot & Mint ready) ===
#
# This prepares a contributor/dev box for:
# - Running the Admin hub from source (web_version_admin/server.py)
# - Running the Student hub via the zipapp (ccri_ctf.pyz) launched by start_web_hub.py
# - Copy scripts that mark .desktop files trusted (needs 'gio' from libglib2.0-bin)
#
# NOTE: We no longer rely on .pyc files. Student builds use the .pyz zipapp.

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"

# Environment to suppress interactive prompts (apt/needrestart/debconf)
APT_ENV = {
    **os.environ,
    "DEBIAN_FRONTEND": "noninteractive",
    "NEEDRESTART_SUSPEND": "1",      # avoid restart prompts
    "UCF_FORCE_CONFOLD": "1",        # keep existing confs by default
}

def run(cmd, check=True, env=None):
    """Run a command (str or list) with our non-interactive env and show it."""
    if isinstance(cmd, str):
        print(f"💻 Running: {cmd}")
        result = subprocess.run(cmd, shell=True, env=env or APT_ENV)
    else:
        print(f"💻 Running: {' '.join(shlex.quote(c) for c in cmd)}")
        result = subprocess.run(cmd, env=env or APT_ENV)
    if check and result.returncode != 0:
        print(f"❌ ERROR: Command failed -> {cmd}", file=sys.stderr)
        sys.exit(1)
    return result.returncode

def apt_update():
    run(["sudo", "-E", "apt-get", "update", "-y"])

def apt_install_packages(packages):
    """
    Install system packages via apt-get, non-interactively, with safe dpkg options.
    Using apt-get here is more scripting-friendly than 'apt'.
    """
    print("📦 Installing system dependencies (non-interactive)...")
    apt_update()
    base_cmd = [
        "sudo", "-E", "apt-get", "install", "-yq",
        "-o", 'Dpkg::Options::=--force-confdef',
        "-o", 'Dpkg::Options::=--force-confold',
    ]
    run(base_cmd + packages)

def preseed_wireshark_and_install():
    """
    Preseed wireshark-common so it won't prompt about setuid dumpcap,
    then install wireshark-common + tshark, reconfigure non-interactively,
    and add the current user to the 'wireshark' group.
    """
    print("🧪 Preseeding Wireshark (allow non-root capture) and installing non-interactively...")
    preseed = 'wireshark-common wireshark-common/install-setuid boolean true'
    run(f"echo '{preseed}' | sudo debconf-set-selections")

    apt_install_packages(["wireshark-common", "tshark"])
    run(["sudo", "dpkg-reconfigure", "-f", "noninteractive", "wireshark-common"])
    run(["sudo", "usermod", "-aG", "wireshark", os.environ.get("SUDO_USER") or os.environ.get("USER") or ""])

def pip_install():
    """Install Python CLI tools via pipx and libs via pip (system pip on Parrot/Mint)."""
    print("🐍 Installing Python CLI tools via pipx...")
    apt_install_packages(["pipx"])
    run(["pipx", "ensurepath"])

    # Flask via pipx (optional CLI) and via pip for imports at runtime
    run(["pipx", "install", "flask"])

    print("📚 Installing Flask and MarkupSafe via pip (for Python imports)...")
    run(["python3", "-m", "pip", "install", "--break-system-packages", "flask", "markupsafe"])

def install_zsteg():
    """Install zsteg via Ruby gem."""
    print("💎 Installing Ruby and zsteg...")
    apt_install_packages(["ruby", "ruby-dev", "libmagic-dev"])
    run(["sudo", "gem", "install", "zsteg", "--no-document"])

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

    apt_install_packages(["wget"])
    print("⬇️ Downloading Steghide 0.6.0 .deb package...")
    run(["wget", "-q", STEGO_DEB_URL, "-O", "/tmp/steghide.deb"])

    print("📦 Installing patched Steghide (auto-fix deps if needed)...")
    rc = run("sudo dpkg -i /tmp/steghide.deb", check=False)
    if rc != 0:
        run(["sudo", "-E", "apt-get", "-f", "install", "-yq",
             "-o", 'Dpkg::Options::=--force-confdef',
             "-o", 'Dpkg::Options::=--force-confold'])
    run("rm -f /tmp/steghide.deb")

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

    if sys.stdin.isatty():
        try:
            git_name = input("Enter your Git name: ").strip()
            git_email = input("Enter your Git email: ").strip()
        except EOFError:
            git_name = git_email = None
    else:
        git_name = git_email = None

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

    # --- Preseed + install Wireshark/Tshark first to avoid prompts
    preseed_wireshark_and_install()

    # --- System packages for your flow ---
    apt_packages = [
        # Essential tools
        "git", "python3", "python3-pip", "python3-venv", "gcc", "build-essential",
        "fonts-noto-color-emoji",

        # Python libs used by the app / challenges
        "python3-markdown", "python3-scapy",

        # Utilities your scripts rely on
        "curl", "lsof", "xdg-utils", "libglib2.0-bin",  # 'gio' comes from libglib2.0-bin
        "gnome-terminal",                               # used by /run_script endpoint

        # Challenge tools (same as before)
        "exiftool", "zbar-tools", "hashcat", "unzip", "libmcrypt4",
        "nmap", "qrencode", "vim-common", "util-linux",
        "binwalk", "fcrackzip", "john", "radare2", "imagemagick", "hexedit", "feh",
    ]
    apt_install_packages(apt_packages)

    # Challenge helpers / languages
    install_steghide_deb()
    pip_install()
    install_zsteg()
    configure_git(args.git_name, args.git_email)

    print("\n✅ Base environment ready.")
    print("   • Admin run (dev):   python3 web_version_admin/server.py")
    print("   • Student run:       python3 ccri_ctf.pyz")
    print("   • Desktop launcher:  start_web_hub.py decides Admin vs Student at runtime")
    print("\n🎉 Setup complete! If Wireshark group membership was added, log out/in once to capture without sudo.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script may perform privileged operations via sudo.")
    main()
