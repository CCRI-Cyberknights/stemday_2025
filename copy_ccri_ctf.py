#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import sys
import subprocess
import pwd
import grp
import re

# === Configuration ===
target_user = "ccri_stem"
target_group = "ccri_ctf"
target_folder_name = "stemday_2025"

# === Items to copy (relative to source_root) ===
include = [
    "challenges",          # Admin/Source versions (careful with secrets!)
    "challenges_solo",
    "web_version",         # Student assets (templates, json)
    "ccri_ctf.pyz",        # Student executable (The App)
    "start_web_hub.py",    # Launcher script
    "stop_web_hub.py",     # Cleanup script
    ".ccri_ctf_root",      # Root marker for exploration scripts
    "coach_core.py",       # ✅ Coach Mode Backend
    "worker_node.py",      # ✅ Coach Mode Worker
    "exploration_core.py", # ✅ Exploration Mode Backend
    "reset_environment.py" # Reset script
]

def ensure_group_and_members(group_name, users):
    """Create group if missing, and ensure listed users are members."""
    try:
        group = grp.getgrnam(group_name)
        print(f"✅ Group '{group_name}' already exists.")
    except KeyError:
        print(f"➕ Group '{group_name}' not found. Creating it...")
        subprocess.run(["groupadd", group_name], check=True)
        group = grp.getgrnam(group_name)

    current_members = set(group.gr_mem)
    for user in users:
        if user and user not in current_members:
            print(f"👥 Adding '{user}' to group '{group_name}'...")
            subprocess.run(["usermod", "-aG", group_name, user], check=True)
        else:
            print(f"✅ User '{user}' is already in group '{group_name}'.")
    return group.gr_gid

def copy_and_fix(src: Path, dst: Path, uid: int, gid: int):
    """Copy src to dst, replacing existing, then fix ownership and permissions."""
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

    def is_script(fname):
        return fname.endswith((".py", ".sh", ".desktop", ".pyz", ".command"))

    def is_plain_text(fname):
        return fname.endswith((".txt", ".md", ".json", ".log"))

    # Apply Permissions
    if dst.is_dir():
        for dirpath, _, filenames in os.walk(dst):
            os.chown(dirpath, uid, gid)
            os.chmod(dirpath, 0o2775)  # rwx for owner/group; setgid
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    os.chown(fpath, uid, gid)
                except FileNotFoundError:
                    continue
                
                if is_script(fname):
                    os.chmod(fpath, 0o775) # rwx for owner/group
                else:
                    os.chmod(fpath, 0o664) # rw for owner/group
    else:
        os.chown(dst, uid, gid)
        if is_script(dst.name):
            os.chmod(dst, 0o775)
        else:
            os.chmod(dst, 0o664)

def write_or_patch_desktop_launcher(launcher_dst: Path, icon_path: Path, uid: int, gid: int):
    """Ensure the .desktop launcher exists, points to start script, and uses the custom icon."""
    
    # Check if we successfully copied the icon to the target folder
    final_icon = icon_path if icon_path.exists() else "utilities-terminal"
    
    desired_exec = f'Exec=bash -c "cd $HOME/Desktop/{target_folder_name} && python3 start_web_hub.py"'
    
    template = (
        "[Desktop Entry]\n"
        "Version=1.0\n"
        "Type=Application\n"
        "Terminal=true\n"
        "Name=Launch_CCRI_CTF_Hub\n"
        f"{desired_exec}\n"
        f"Icon={final_icon}\n"
        "Name[en_US]=Launch_CCRI_CTF_Hub\n"
    )

    if launcher_dst.exists():
        try:
            text = launcher_dst.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            text = ""
        
        # Patch Exec
        if "Exec=" in text:
            text = re.sub(r"^Exec=.*$", desired_exec, text, flags=re.MULTILINE)
        else:
            text += f"\n{desired_exec}"
            
        # Patch Icon (if we have a custom one)
        if str(final_icon) != "utilities-terminal":
            if "Icon=" in text:
                 text = re.sub(r"^Icon=.*$", f"Icon={final_icon}", text, flags=re.MULTILINE)
            else:
                 text += f"\nIcon={final_icon}"
    else:
        text = template

    launcher_dst.write_text(text, encoding="utf-8")
    os.chown(launcher_dst, uid, gid)
    os.chmod(launcher_dst, 0o775)

    # Mark as trusted (Cinnamon/Nemo/Gnome)
    try:
        subprocess.run(
            ["gio", "set", str(launcher_dst), "metadata::trusted", "true"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("🔐 Marked launcher as trusted.")
    except Exception:
        pass

def main():
    # Set umask to allow group write by default
    old_umask = os.umask(0o002)

    # Elevation check
    if os.geteuid() != 0:
        print("🛡️ Elevation required. Re-running with sudo...")
        try:
            subprocess.run(["sudo", "python3"] + sys.argv, check=True)
        except Exception as e:
            print(f"❌ Failed to elevate: {e}")
        sys.exit(0)

    # Determine paths
    source_root = Path(__file__).resolve().parent
    
    # Try to find the real user if running via sudo
    invoking_user = os.environ.get("SUDO_USER")
    if not invoking_user:
        print("❌ Could not determine invoking user via SUDO_USER.")
        sys.exit(1)

    try:
        uid = pwd.getpwnam(target_user).pw_uid
    except KeyError:
        print(f"❌ Target user '{target_user}' does not exist on this system.")
        sys.exit(1)
        
    gid = ensure_group_and_members(target_group, [target_user, invoking_user])
    
    target_home = Path(f"/home/{target_user}")
    target_desktop = target_home / "Desktop"
    target_root = target_desktop / target_folder_name

    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Prepare Desktop
    if not target_desktop.exists():
        target_desktop.mkdir(parents=True, exist_ok=True)
        os.chown(target_desktop, uid, gid)
        os.chmod(target_desktop, 0o755)

    # Clean Target
    if target_root.exists():
        print(f"🗑️ Removing existing folder: {target_root}")
        shutil.rmtree(target_root)

    # Create Target Root
    target_root.mkdir(parents=True, exist_ok=True)
    os.chown(target_root, uid, gid)
    os.chmod(target_root, 0o2775)

    # Check for .ccri_ctf_root marker
    marker = source_root / ".ccri_ctf_root"
    if not marker.exists():
        print("⚠️ Marker .ccri_ctf_root missing in source. Creating it...")
        marker.touch()

    # Copy Items
    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst, uid, gid)
        else:
            print(f"⚠️ Skipping missing item: {item}")
            
    # Copy Custom Icon (Polish)
    icon_src = source_root / "web_version_admin" / "static" / "assets" / "CyberKnights_2.png"
    icon_dst = target_root / "icon.png"
    if icon_src.exists():
        print("🎨 Copying custom icon...")
        shutil.copy2(icon_src, icon_dst)
        os.chown(icon_dst, uid, gid)
        os.chmod(icon_dst, 0o664)

    # Create/Update Desktop Launcher
    launcher_dst = target_desktop / "Launch_CCRI_CTF_HUB.desktop"
    print("📎 Creating desktop launcher...")
    write_or_patch_desktop_launcher(launcher_dst, icon_dst, uid, gid)

    print("\n✅ Deployment Complete!")
    print(f"🚀 Student Folder: {target_root}")
    print("ℹ️  Note: If you just added users to the group, a logout/login may be required.")

    os.umask(old_umask)

if __name__ == "__main__":
    main()