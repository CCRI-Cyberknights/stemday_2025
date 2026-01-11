#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shlex
import shutil
import stat
from pathlib import Path

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

# ---------- Wireshark / dumpcap ----------
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

    run(["sudo", "setcap", "cap_net_raw,cap_net_admin+eip", dumpcap], check=False)
    caps = getcap(dumpcap)
    if "cap_net_admin,cap_net_raw" in caps and "eip" in caps:
        print(f"✅ dumpcap caps OK: {caps}")
        return

    run("echo 'wireshark-common wireshark-common/install-setuid boolean true' | sudo debconf-set-selections", check=False)
    run(["sudo", "dpkg-reconfigure", "-f", "noninteractive", "wireshark-common"], check=False)
    if is_setuid(dumpcap):
        print(f"✅ dumpcap setuid OK: {dumpcap}")
        return

    local_dump = "/usr/local/bin/dumpcap"
    run(["sudo", "install", "-o", "root", "-g", "wireshark", "-m", "0750", dumpcap, local_dump], check=False)
    run(["sudo", "chmod", "u+s", local_dump], check=False)
    use_path = shutil.which("dumpcap") or local_dump
    print(f"🛠 Using dumpcap at: {use_path}")

def preseed_wireshark_and_install():
    print("🧪 Preseeding Wireshark (allow non-root capture) and installing non-interactively...")
    preseed = 'wireshark-common wireshark-common/install-setuid boolean true'
    run(f"echo '{preseed}' | sudo debconf-set-selections")
    apt_install_packages(["wireshark", "wireshark-common", "tshark", "libcap2-bin"])
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
    env_force_deb = os.environ.get("FORCE_STEGHIDE_DEB") == "1"
    if env_force_deb and mode == "auto":
        mode = "deb"
    if mode not in ("auto", "deb", "apt"):
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
    for cand in ("/usr/sbin/john", "/usr/bin/john"):
        if os.path.exists(cand) and os.access(cand, os.X_OK):
            run(["sudo", "ln", "-sf", cand, "/usr/local/bin/john"], check=False)
            break
    for root in ("/usr/sbin",):
        if os.path.isdir(root):
            for name in os.listdir(root):
                if name.endswith("2john"):
                    src = os.path.join(root, name)
                    if os.access(src, os.X_OK):
                        run(["sudo", "ln", "-sf", src, f"/usr/local/bin/{name}"], check=False)
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
    res = subprocess.run(["git", "config", "--global", key], capture_output=True, text=True)
    return res.stdout.strip() if res.returncode == 0 else None

def configure_git(git_name=None, git_email=None):
    print("\n🔧 Checking Git configuration...")
    if get_git_config("user.name") and get_git_config("user.email"):
        return
    if not git_name: git_name = os.environ.get("GIT_NAME")
    if not git_email: git_email = os.environ.get("GIT_EMAIL")
    
    if git_name and git_email:
        run(["git", "config", "--global", "user.name", git_name])
        run(["git", "config", "--global", "user.email", git_email])
        run(["git", "config", "--global", "credential.helper", "store"])
        print("✅ Git configuration saved.")
    else:
        print("⚠️  Skipping Git prompts (non-interactive).")

# ---------- Desktop Launcher Setup ----------
def setup_desktop_launcher():
    print("📎 Configuring desktop launcher for Main Repo...")
    repo_root = Path(__file__).resolve().parent
    icon_path = repo_root / "web_version_admin" / "static" / "assets" / "CyberKnights_2.png"
    launcher_path = repo_root / "Launch_CCRI_CTF_HUB.desktop"

    # Fallback if the custom icon isn't there
    final_icon = str(icon_path) if icon_path.exists() else "utilities-terminal"
    
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Terminal=true
Name=Launch_CCRI_CTF_Hub
Exec=bash -c "cd {repo_root} && python3 start_web_hub.py"
Icon={final_icon}
Name[en_US]=Launch_CCRI_CTF_Hub
Comment=Launch the Dev Environment for CCRI CTF
"""
    try:
        with open(launcher_path, "w") as f:
            f.write(content)
        os.chmod(launcher_path, 0o755)
        
        # Determine the user who owns the script to chown the launcher
        uid = os.stat(__file__).st_uid
        gid = os.stat(__file__).st_gid
        os.chown(launcher_path, uid, gid)
        
        # Try to mark trusted
        subprocess.run(["gio", "set", str(launcher_path), "metadata::trusted", "true"],
                       check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Launcher updated with absolute paths & custom icon.")
    except Exception as e:
        print(f"⚠️  Could not update launcher: {e}")

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

    install_steghide_auto(args.steghide_mode)
    ensure_john_and_helpers_on_path()
    install_cyberchef_offline()
    pip_install()
    install_zsteg()
    configure_git(args.git_name, args.git_email)
    
    # NEW: Fix the launcher icon in the main repo
    setup_desktop_launcher()

    print("\n✅ Base environment ready.")
    print("   • Admin run (dev):   python3 web_version_admin/server.py")
    print("   • Student run:       python3 ccri_ctf.pyz")
    print("   • Desktop launcher:  Updated with custom icon! Double-click to run.")
    print("\n🎉 Setup complete!")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️  This script may perform privileged operations via sudo.")
    main()