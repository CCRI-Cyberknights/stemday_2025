#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shlex
import shutil
import stat

STEGO_DEB_URL = "https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/debs/steghide_0.6.0-1_amd64.deb"

APT_ENV = {
    **os.environ,
    "DEBIAN_FRONTEND": "noninteractive",
    "NEEDRESTART_SUSPEND": "1",
    "UCF_FORCE_CONFOLD": "1",
}

def run(cmd, check=True, env=None):
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
    print("📦 Installing system dependencies (non-interactive)...")
    apt_update()
    base_cmd = [
        "sudo", "-E", "apt-get", "install", "-yq",
        "-o", 'Dpkg::Options::=--force-confdef',
        "-o", 'Dpkg::Options::=--force-confold',
    ]
    run(base_cmd + packages)

# ---------- OS helpers ----------
def read_os_release():
    info = {}
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().strip('"')
                info[k] = v
    except FileNotFoundError:
        pass
    return info

def is_parrot():
    info = read_os_release()
    id_ = info.get("ID", "").lower()
    like = (info.get("ID_LIKE", "") or "").lower()
    return id_ == "parrot" or "parrot" in like

def arch():
    try:
        return subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip()
    except Exception:
        return None

# ---------- Wireshark / dumpcap (parity with live-CD script) ----------
def ensure_group(name):
    rc = run(["getent", "group", name], check=False)
    if rc != 0:
        run(["sudo", "groupadd", "--system", name], check=False)

def add_users_to_group(group, users):
    for u in users:
        if not u:
            continue
        rc = run(["id", u], check=False)
        if rc == 0:
            run(["sudo", "usermod", "-aG", group, u], check=False)

def is_setuid(path):
    try:
        st = os.stat(path)
        return bool(st.st_mode & stat.S_ISUID)
    except FileNotFoundError:
        return False

def getcap(path):
    try:
        out = subprocess.check_output(["getcap", path], text=True).strip()
        return out
    except Exception:
        return ""

def ensure_dumpcap_nonroot():
    dumpcap = shutil.which("dumpcap")
    if not dumpcap:
        print("ℹ️ dumpcap not found; skipping perms setup.")
        return

    # Prefer capabilities
    run(["sudo", "setcap", "cap_net_raw,cap_net_admin+eip", dumpcap], check=False)
    caps = getcap(dumpcap)
    if "cap_net_admin,cap_net_raw" in caps and "eip" in caps:
        print(f"✅ dumpcap caps OK: {caps}")
        return

    # Maintainer setuid path
    run("echo 'wireshark-common wireshark-common/install-setuid boolean true' | sudo debconf-set-selections", check=False)
    run(["sudo", "dpkg-reconfigure", "-f", "noninteractive", "wireshark-common"], check=False)
    if is_setuid(dumpcap):
        print(f"✅ dumpcap setuid OK: {dumpcap}")
        return

    # Final fallback: local copy in /usr/local/bin (first in PATH)
    local_dump = "/usr/local/bin/dumpcap"
    run(["sudo", "install", "-o", "root", "-g", "wireshark", "-m", "0750", dumpcap, local_dump], check=False)
    run(["sudo", "chmod", "u+s", local_dump], check=False)
    # Verify
    use_path = shutil.which("dumpcap") or local_dump
    caps2 = getcap(use_path)
    suid2 = is_setuid(use_path)
    print(f"🛠 Using dumpcap at: {use_path}")
    print(f"    caps: {caps2 or 'none'}")
    print(f"    suid: {suid2}")

def preseed_wireshark_and_install():
    print("🧪 Preseeding Wireshark (allow non-root capture) and installing non-interactively...")
    preseed = 'wireshark-common wireshark-common/install-setuid boolean true'
    run(f"echo '{preseed}' | sudo debconf-set-selections")
    # Install GUI+CLI & caps tooling (parity with bash installer)
    apt_install_packages(["wireshark", "wireshark-common", "tshark", "libcap2-bin"])
    # Create group and add plausible users
    ensure_group("wireshark")
    env_user = os.environ.get("SUDO_USER") or os.environ.get("USER") or ""
    add_users_to_group("wireshark", [env_user, "user", "parrot"])

# ---------- Python / pip(x) ----------
def pip_install():
    print("🐍 Installing Python CLI tools via pipx...")
    apt_install_packages(["pipx"])
    run(["pipx", "ensurepath"])
    run(["pipx", "install", "flask"])
    print("📚 Installing Flask and MarkupSafe via pip (for Python imports)...")
    run(["python3", "-m", "pip", "install", "--break-system-packages", "flask", "markupsafe"])

# ---------- zsteg ----------
def install_zsteg():
    print("💎 Installing Ruby and zsteg...")
    apt_install_packages(["ruby", "ruby-dev", "libmagic-dev"])
    run(["sudo", "gem", "install", "zsteg", "--no-document"])

# ---------- CyberChef (offline) ----------
def install_cyberchef_offline():
    print("🧁 Installing offline CyberChef + desktop entry...")
    apt_install_packages(["curl", "xdg-utils", "desktop-file-utils"])
    CYBER_DIR = "/opt/cyberchef"
    run(["sudo", "mkdir", "-p", CYBER_DIR])
    if not os.path.exists(f"{CYBER_DIR}/index.html") or os.path.getsize(f"{CYBER_DIR}/index.html") == 0:
        run(["sudo", "curl", "-fsSL", "https://gchq.github.io/CyberChef/", "-o", f"{CYBER_DIR}/index.html"], check=False)
    desktop_entry = """[Desktop Entry]
Type=Application
Name=CyberChef (Offline)
Exec=xdg-open file:///opt/cyberchef/index.html
Icon=utilities-terminal
Terminal=false
Categories=Utility;Education;Development;
"""
    run(["bash", "-lc", f"printf %s {shlex.quote(desktop_entry)} | sudo tee /usr/share/applications/cyberchef.desktop >/dev/null"])
    run(["bash", "-lc", "command -v update-desktop-database >/dev/null && sudo update-desktop-database || true"], check=False)

# ---------- Steghide (same logic as before) ----------
def install_steghide_deb():
    print("🕵️ Checking Steghide version...")
    try:
        version_output = subprocess.check_output(["steghide", "--version"], text=True).strip()
        if "0.6.0" in version_output:
            print("✅ Steghide 0.6.0 already installed.")
            return
    except Exception:
        print("ℹ️ Steghide not found or outdated. Installing patched version...")

    if arch() not in ("amd64",):
        print("⚠️  Patched .deb is built for amd64. Falling back to repo install.")
        apt_install_packages(["steghide"])
        return

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

    if is_parrot():
        print("📌 Pinning Steghide 0.6.0 on Parrot to prevent downgrade...")
        pin_file = "/etc/apt/preferences.d/steghide"
        pin_contents = """Package: steghide
Pin: version 0.6.0*
Pin-Priority: 1001
"""
        with open("/tmp/steghide-pin", "w") as f:
            f.write(pin_contents)
        run(["sudo", "mv", "/tmp/steghide-pin", pin_file])

def install_steghide_auto(mode: str = "auto"):
    """
    mode: 'auto' (default), 'deb', or 'apt'
    - auto: Parrot => deb, others => apt
    - deb: force .deb path (honors arch check)
    - apt: force repo install
    ENV override: FORCE_STEGHIDE_DEB=1 behaves like mode='deb'
    """
    env_force_deb = os.environ.get("FORCE_STEGHIDE_DEB") == "1"
    if env_force_deb and mode == "auto":
        mode = "deb"

    if mode not in ("auto", "deb", "apt"):
        print(f"⚠️ Unknown steghide mode '{mode}', falling back to 'auto'")
        mode = "auto"

    if mode == "apt" or (mode == "auto" and not is_parrot()):
        print("🧩 Installing Steghide from distro repositories...")
        apt_install_packages(["steghide"])
        return

    print("🧩 Installing Steghide via patched .deb...")
    install_steghide_deb()

# ---------- Helpers for john/*2john parity ----------
def ensure_john_and_helpers_on_path():
    print("🧰 Ensuring john/*2john helpers are in PATH...")
    # john symlink
    for cand in ("/usr/sbin/john", "/usr/bin/john"):
        if os.path.exists(cand) and os.access(cand, os.X_OK):
            run(["sudo", "ln", "-sf", cand, "/usr/local/bin/john"], check=False)
            break
    # /usr/sbin/*2john
    for root in ("/usr/sbin",):
        if os.path.isdir(root):
            for name in os.listdir(root):
                if name.endswith("2john"):
                    src = os.path.join(root, name)
                    if os.access(src, os.X_OK):
                        run(["sudo", "ln", "-sf", src, f"/usr/local/bin/{name}"], check=False)
    # /usr/share/john/*2john + *2john.py (wrap if non-executable)
    share = "/usr/share/john"
    if os.path.isdir(share):
        for name in os.listdir(share):
            if name.endswith("2john") or name.endswith("2john.py"):
                src = os.path.join(share, name)
                dst = f"/usr/local/bin/{name}"
                if os.access(src, os.X_OK):
                    run(["sudo", "ln", "-sf", src, dst], check=False)
                else:
                    wrapper = f"""#!/usr/bin/env bash
exec python3 "{src}" "$@"
"""
                    run(["bash", "-lc", f"printf %s {shlex.quote(wrapper)} | sudo tee {shlex.quote(dst)} >/dev/null"])
                    run(["sudo", "chmod", "+x", dst], check=False)

# ---------- Git ----------
def get_git_config(key):
    res = subprocess.run(["git", "config", "--global", key],
                         capture_output=True, text=True)
    if res.returncode == 0:
        val = res.stdout.strip()
        return val if val else None
    return None

def configure_git(git_name=None, git_email=None):
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
        run(["git", "config", "—global", "credential.helper", "store"])
        print("✅ Git configuration saved.")
    else:
        print("⚠️  Skipping Git prompts (non-interactive).")
        print("    Set these and rerun if needed:")
        print("    - Flags: --git-name 'Your Name' --git-email 'you@example.com'")
        print("    - Or env: GIT_NAME='Your Name' GIT_EMAIL='you@example.com'")

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="CCRI CyberKnights environment setup")
    p.add_argument("--git-name", help="Git user.name (non-interactive)")
    p.add_argument("--git-email", help="Git user.email (non-interactive)")
    p.add_argument("--steghide-mode",
                   choices=["auto", "deb"],
                   default="auto",
                   help="Install Steghide using patched deb or auto (Parrot=deb, others=apt)")
    return p.parse_args()

def main():
    args = parse_args()

    print("\n🚀 Setting up your CCRI_CTF contributor environment...")
    print("=" * 60 + "\n")

    preseed_wireshark_and_install()
    ensure_dumpcap_nonroot()

    apt_packages = [
        "git", "python3", "python3-pip", "python3-venv", "gcc", "build-essential",
        "fonts-noto-color-emoji",
        "python3-markdown", "python3-scapy",
        "curl", "lsof", "xdg-utils", "libglib2.0-bin",
        "gnome-terminal",
        "exiftool", "zbar-tools", "hashcat", "unzip", "libmcrypt4",
        "nmap", "qrencode", "vim-common", "util-linux",
        "binwalk", "fcrackzip", "john", "radare2", "imagemagick", "hexedit", "feh", "eog",
        "p7zip-full", "ncat",
    ]
    apt_install_packages(apt_packages)

    # Steghide (OS-aware)
    install_steghide_auto(args.steghide_mode)

    # PATH fixes & helpers
    ensure_john_and_helpers_on_path()

    # Optional extras to match live-CD UX
    install_cyberchef_offline()

    # Python tooling
    pip_install()
    install_zsteg()

    # Git config
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
